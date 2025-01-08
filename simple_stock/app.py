# Simple stock example using Streamlit

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.write("""
        # Simple Stock Price App
          
        Simple app to show the **Volume** and **Closing Price** of a selected stock. 
        """)

# Get the ticker symbol from the user
ticker_symbol = st.text_input("Enter the ticker symbol of the stock you want to analyze", 'IBM')

# Clean the ticker symbol
cleaned_ticker_symbol = ticker_symbol.strip().replace('$', '')

# Display the cleaned ticker symbol for debugging
st.write(f"Ticker symbol being used: {cleaned_ticker_symbol}")

# Get the user input for the date range
start_date = st.date_input("Start Date", datetime(2018, 5, 31))
end_date = st.date_input("End Date", datetime(2024, 12, 31))

# Add a submit button
if st.button("Submit"):
    try:
        # Get the data on this ticker from yahoo finance
        ticker_data = yf.Ticker(cleaned_ticker_symbol)

        # Get the historical prices for this ticker and store in a dataframe
        ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date)

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
            st.error(f"Invalid symbol or No data available for {cleaned_ticker_symbol} for the specified date range." , icon="🚫")
    except Exception as e:
        st.write(f"An error occurred: {e}")