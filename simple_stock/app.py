# Simple stock example using Streamlit

import streamlit as st
import pandas as pd
import yfinance as yf


st.write("""
        # Simple Stock Price App
          
        Simple app to show the **Volume** and **Closing Price** of IBM. 
        """)
# Define the ticker symbol
ticker_symbol = 'IBM'

# Get the data on this ticker from yahoo finance
ticker_data = yf.Ticker(ticker_symbol)

# Get the historical prices for this ticker and store in a dataframe
ticker_df = ticker_data.history(period='1d', start='2018-05-31', end='2024-12-31')

# Print stock data to line charts if data is available
if not ticker_df.empty:
    st.write("""
            ## Closing Price
            """)
    st.line_chart(ticker_df.Close)
    st.write("""
            ## Volume
            """)
    st.line_chart(ticker_df.Volume)
else:
    st.write("""
             > No data available for the specified date range. 
             """)