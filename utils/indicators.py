import pandas as pd

def add_indicators(df, strategy):
    """
    Add technical indicators based on selected strategy
    """
    if strategy == "Simple Moving Average Crossover":
        return add_sma_indicators(df)
    return df

def add_sma_indicators(df):
    """
    Add Simple Moving Average indicators
    """
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    return df
