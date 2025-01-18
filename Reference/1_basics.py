import streamlit as st
import pandas as pd
import time


# App title
st.title("Basic Streamlit App & Syntax")
st.write("""
         This is s simple Streamlit application to demonstrate basic syntax.
         How to write text, markdown, and stream text.
         
         """)

# Sub Title
st.subheader("Subheader: Displaying DataFrame")

# Write text
st.write("**Populate a dataframe using st.write()**")
st.markdown("### You can also use st.markdown() to write markdown text")
st.text("### Or use st.text() to write plain text")

# Build & write DataFrame
df = pd.DataFrame({
    'Column 1': [1, 2, 3],
    'Column 2': [4, 5, 6]
})

st.write(df)
# Write markdown
md_text = """
### This is a markdown text\
- Item 1
- Item 2
### H-tags in markdown
1. Item 1
2. Item 2
"""
st.markdown(md_text)


# Stream text
st.write("### Streaming data using st.write_stream() function")
stream_btn = st.button("Click Button to Stream Data")

STREAM_DATA = """
   #### Stream data example, this is a long text to demonstrate the streaming feature of Streamlit.
"""

# Function to stream data word by word with a delay
def stream_data(txt):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.1)

# If the button is clicked, start streaming the data
if stream_btn:
    st.write_stream(stream_data(STREAM_DATA))