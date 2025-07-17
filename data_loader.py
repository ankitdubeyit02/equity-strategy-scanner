import yfinance as yf
from datetime import datetime

def get_data(symbol="^NSEI", start="2023-01-01"):
    end = datetime.today().strftime('%Y-%m-%d')  # Current date
    data = yf.download(symbol, start=start, end=end)
    data = data.dropna()
    data.index.name = "Date"
    return data
