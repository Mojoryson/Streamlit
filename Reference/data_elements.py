# This script will review the various options of working data element in Streamlit


# Import the libraries
import streamlit as st
import pandas as pd

# Set up the page config

st.set_page_config(
    page_title="Data Elements",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
    
)
st.title("Data Elements in Streamlit", anchor="center")

# Create an example dataframe
df = pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [10, 20, 30, 40],
    "C": [100, 200, 300, 400]
})

st.markdown("#### Demo using st.metric()")
col1, col2, col3 = st.columns(3)
col1.metric("Column A", df["A"].sum(), delta=-10)
col2.metric("Column B", df["B"].sum(), 200)
col3.metric("Column C", df["C"].sum(), 50)

st.header("Display the DataFrame - st.dataframe()")
st.dataframe(df,width=500, height=300, hide_index=False)


st.header("Display the DataFrame as a Table - st.table()")
st.table(df)

st.header("Display the DataFrame as a JSON - st.json()")
st.json(df.to_json(orient="records"), expanded=False)

st.header("Display the DataFrame as a CSV - st.download_button()")
csv = df.to_csv(index=False)
st.dataframe(df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)

st.markdown("#### Editable DataFrame - st.data_editor()")
st.data_editor(df)

st.header("Display the DataFrame using st.column.config()")
st.column_config



