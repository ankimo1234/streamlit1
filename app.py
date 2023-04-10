import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
import streamlit as st

st.title("株価可視化アプリ")

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider("日数",1,50,20)

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

@st.cache_data
def get_data(days,tickers): 
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f"{days}d")
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[["Close"]]
        hist.columns = [company]
        hist = hist.head().T
        hist.index.name = "Name"
        df = pd.concat([df,hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
        "範囲を指定して下さい。",
        0.0, 500.0, (0.0, 500.0)
    )

    tickers = {
        "apple" : "AAPL",
        "facebook" : "META",
        "google" : "GOOGL",
        "microsoft" : "MSFT",
        "netflix" : "NFLX",
        "amazon" : "AMZN"
    }

    df = get_data(days,tickers)
    companies = st.multiselect(
        "会社名を選択してください",
        list(df.index),
        ["google","amazon","facebook","apple"]
    )

    if not companies:
        st.error("少なくとも1社は選んでください")
    else:
        data = df.loc[companies]
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data,id_vars=["Date"]).rename(
            columns={"value" : "Stock Price(USD)"}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Price(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color="Name:N"
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error("エラーです")