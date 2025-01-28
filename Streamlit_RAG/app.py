# Import the libraries
import streamlit as st
import os
import faiss
from io import BytesIO
from docx import Document
import numpy as np
from langchain_community.document_loaders import WebBaseLoader
from PyPDF2 import PdfReader
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv



# Import the Hugging Face API key
load_dotenv()
HUGGING_FACE_API = os.getenv("HUGGING_FACE_API")




def main():
    st.set_page_config(page_title="RAG App", page_icon=":books:")
    st.title("40-Tech RAG Q&A App 🚀")
    
    input_type = st.selectbox("Select a source", ["Web", "PDF", "DOCX", "Text", "TXT"])
    if input_type == "Web":
        number_input = st.number_input(min_value=1, max_value=10, step=1, label="Enter the number of URLs")
        input_data = []
        for i in range(number_input):
            url = st.sidebar.text_input(f"Enter the URL of Page:  {i+1}")
            input_data.append(url)
    elif input_type == "PDF":
        input_data = st.file_uploader("Upload a PDF file", type="pdf")
    elif input_type == "DOCX":
        input_data = st.file_uploader("Upload a DOCX file", type=["docx", "doc"])
    elif input_type == "Text":
        input_data = st.text_area("Enter the text")
    elif input_type == "TXT":
        input_data = st.file_uploader("Upload a TXT file", type="txt")
    else:
        st.error("Please select a valid source")
        return

    if st.button("Submit"):
        pass


if __name__ == "__main__":
    main()