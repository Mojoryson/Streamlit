import streamlit as st
import pandas as pd
import base64
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

st.title("S&P 500 App")

st.markdown("""
        This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
        * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
        * **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
        """)

st.sidebar.header("User Inputs")

# load the S&P 500 data from the web
@st.cache_data
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby("GICS Sector")

# Build out the sidebar with the sector selection
sorted_sector_unique = sorted(df["GICS Sector"].unique())
selected_sector = st.sidebar.multiselect("Sector", sorted_sector_unique, sorted_sector_unique)

# Filter the data
df_selected_sector = df[(df["GICS Sector"].isin(selected_sector))]

# Display the selected sector data in the UI
st.header("Display Companies in Selected Sector")
st.write("Data Dimension: " + str(df_selected_sector.shape[0]) + " rows and " + str(df_selected_sector.shape[1]) + " columns.")
st.dataframe(df_selected_sector)

# Download S&P 500 data
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(file_download(df_selected_sector), unsafe_allow_html=True)

if not df_selected_sector.empty:

        # Pull thes stock data from yfinance
        data = yf.download(
                tickers = list(df_selected_sector[:10].Symbol),
                period = "ytd",
                interval = "1d",
                group_by = "ticker",
                auto_adjust = True,
                prepost = True,
                threads = True,
                proxy = None
        )

        # Plot the closing price of the selected companies

        def price_plot(symbol):
                df = pd.DataFrame(data[symbol].Close)
                df["Date"] = df.index
                fig, ax = plt.subplots()
                plt.fill_between(df.Date, df.Close, color="darkblue", alpha=0.3)
                plt.plot(df.Date, df.Close, color="darkblue", alpha=0.8)
                plt.xticks(rotation=90)
                plt.title(symbol, fontweight="bold")
                plt.xlabel("Date", fontweight="bold")
                plt.ylabel("Closing Price", fontweight="bold")
                st.pyplot(fig)

        num_company = st.sidebar.slider("Number of Companies Stock Display", 1, 10)

        if st.button("Show Plots"):
                st.header("Stock Closing Price")
                for i in list(df_selected_sector.Symbol)[:num_company]:
                        price_plot(i)
else:
        st.markdown("### No Sectors Selected")