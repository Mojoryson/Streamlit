# This script demonstrates the use of text elements in Streamlit.
# It includes various text formatting options.
import streamlit as st


# st.title("Text Elements in Streamlit")
st.title("Text Elements in Streamlit :smiley:")  # Title with an emoji
st.write(" For icons on MacOS: Press Command + Control + Spacebar to open the emoji picker.")

# st.header("Header")
st.header("This is a Header 🎉")

# st.subheader("Subheader")
st.subheader("This is a Subheader")

# st.caption("Caption")
st.caption("This is a Caption, which provides additional context or notes.")

# st.code("print('Hello, World!')")

code_text = """
import streamlit as st
import pandas as pd

st.title('Hello, Streamlit!')
for i in range(10):
    st.write(f'Iteration {i}')
    
# st.code syntax    
st.code(code_text, language='python', wrap_lines=True, line_numbers=True)
"""

st.write("Here is a code snippet:")
st.code(code_text, language='python', wrap_lines=True, line_numbers=True)

# st.text("This is a plain text element.")

st.text("This is a plain text element.")

# st.latex(r"""
st.write("Here is a LaTeX equation, this is good for mathematical expressions:")
st.latex(r"""
    E = mc^2
""")
st.divider()
# st.divider("This is a divider")
st.write("Below is a divider:")
st.divider()
st.write("This is after the divider.")

