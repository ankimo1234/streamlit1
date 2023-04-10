import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt



def get_data(days,tickers):
    global df 
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

days = 20
tickers = {
    "apple" : "AAPL",
    "facebook" : "META",
    "google" : "GOOGL",
    "microsoft" : "MSFT",
    "netflix" : "NFLX",
    "amazon" : "AMZN"
}
data = get_data(days,tickers)
# print(data)
companies = ["apple", "facebook"]
data = df.loc[companies]

data = data.T.reset_index().head()
data = pd.melt(data, id_vars=["Date"]).rename(
    columns={"value" : "Stock Prices(USD)"}
)
print(data)

[ymin, ymax] = [200, 300]
chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Data:T",
        y=alt.Y("Stock prices(USD) : Q", stack =None, scale=alt.Scale(domain=[ymin, ymax])),
        color="Name:N"
    )
)
print(chart)