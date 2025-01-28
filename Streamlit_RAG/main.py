# Import the libraries
import streamlit as st
import os
import faiss
from io import BytesIO
from docx import Document
import numpy as np
import torch
from langchain_community.document_loaders import WebBaseLoader
from PyPDF2 import PdfReader
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv

# Streamlit page config
st.set_page_config(page_title="40-Tech RAG Q&A App", page_icon="🤖")

# Load environment variables
load_dotenv()
HUGGING_FACE_API = os.getenv("HUGGING_FACE_API")

# Validate the Hugging Face API key
if not HUGGING_FACE_API:
    st.error("Hugging Face API key not found. Please set it in the environment variables.")
    st.stop()

# Helper functions
def load_file(file, file_type):
    """Load content from a file (PDF, DOCX, or TXT)."""
    try:
        if file_type == "PDF":
            pdf_reader = PdfReader(BytesIO(file.read()))
            return "".join([page.extract_text() for page in pdf_reader.pages])
        elif file_type == "DOCX":
            doc = Document(BytesIO(file.read()))
            return "\n".join([para.text for para in doc.paragraphs])
        elif file_type == "TXT":
            return file.read().decode("utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        raise ValueError(f"Error processing {file_type} file: {e}")

def process_input(input_type, input_data):
    """Process the input data based on the input type and create a vector store."""
    # Handle input types
    if input_type == "Web":
        loader = WebBaseLoader(input_data)
        documents = loader.load()
    else:
        documents = load_file(input_data, input_type)

    # Split documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    if input_type == "Web":
        texts = [str(doc.page_content) for doc in text_splitter.split_documents(documents)]
    else:
        texts = text_splitter.split_text(documents)

    # Create embeddings
    hf_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

    # Create FAISS index
    sample_embedding = np.array(hf_embeddings.embed_query("sample text"))
    dimension = sample_embedding.shape[0]
    index = faiss.IndexFlatL2(dimension)

    # Create FAISS vector store
    vector_store = FAISS(
        embedding_function=hf_embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    # Add documents to the vector store
    vector_store.add_texts(texts)
    return vector_store

def answer_question(vectorstore, query):
    """Answers a question based on the provided vector store."""
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        api_key=HUGGING_FACE_API,
        temperature=0.5
    )
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    return qa({"query": query})

# Main application
def main():
    st.title("40-Tech RAG Q&A App 🚀")
    
    # Select input type
    input_type = st.selectbox("Select a source", ["Web", "PDF", "DOCX", "Text", "TXT"])
    input_data = None

    if input_type == "Web":
        number_input = st.number_input("Number of URLs", min_value=1, max_value=10, step=1)
        input_data = [st.text_input(f"Enter URL {i+1}") for i in range(number_input)]
    elif input_type in ["PDF", "DOCX", "TXT"]:
        input_data = st.file_uploader(f"Upload a {input_type} file", type=input_type.lower())
    elif input_type == "Text":
        input_data = st.text_area("Enter the text")
    else:
        st.error("Invalid input type")
        return

    if st.button("Process"):
        if not input_data:
            st.error("Please provide valid input.")
            return

        with st.spinner("Processing input..."):
            try:
                vectorstore = process_input(input_type, input_data)
                st.session_state["vectorstore"] = vectorstore
                st.success("Vector store created successfully!")
            except Exception as e:
                st.error(f"Error processing input: {e}")
                return

    # Question-answering section
    if "vectorstore" in st.session_state:
        query = st.text_input("Ask your question")
        if st.button("Submit"):
            with st.spinner("Generating answer..."):
                try:
                    answer = answer_question(st.session_state["vectorstore"], query)
                    st.write(f"**Answer**: {answer}")
                except Exception as e:
                    st.error(f"Error generating answer: {e}")

if __name__ == "__main__":
    import os
    os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disable tokenizers parallelism
    os.environ["PYTHONHASHSEED"] = "0"  # Ensure consistent hash seed for multiprocessing
    main()

