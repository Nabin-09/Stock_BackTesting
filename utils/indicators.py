import pandas as pd

def add_indicators(df, strategy, params=None):
    """
    Add technical indicators based on selected strategy
    """
    if strategy == "Simple Moving Average Crossover":
        if params is None:
            params = {"short_window": 20, "long_window": 50}
        return add_sma_indicators(df, params)
    return df

def add_sma_indicators(df, params):
    """
    Add Simple Moving Average indicators with dynamic periods
    """
    short_window = params.get('short_window', 20)
    long_window = params.get('long_window', 50)

    df[f'SMA_{short_window}'] = df['Close'].rolling(window=short_window).mean()
    df[f'SMA_{long_window}'] = df['Close'].rolling(window=long_window).mean()
    return df