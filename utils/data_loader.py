import yfinance as yf
import pandas as pd
from streamlit import cache_data

@cache_data(ttl=3600)  # Cache data for 1 hour
def load_stock_data(symbol, start_date, end_date):
    """
    Load stock data from Yahoo Finance with caching
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            raise ValueError(f"No data found for symbol {symbol}")

        return df

    except Exception as e:
        raise Exception(f"Error loading data for {symbol}: {str(e)}")