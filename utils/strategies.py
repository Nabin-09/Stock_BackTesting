import pandas as pd
import numpy as np

def apply_strategy(df, strategy_name, params=None):
    """
    Apply selected trading strategy to the data
    """
    if strategy_name == "Buy and Hold":
        return apply_buy_and_hold(df)
    elif strategy_name == "Simple Moving Average Crossover":
        if params is None:
            params = {"short_window": 20, "long_window": 50}
        return apply_sma_crossover(df, params)
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")

def apply_buy_and_hold(df):
    """
    Simple buy and hold strategy
    """
    signals = pd.Series(1, index=df.index)
    signals.iloc[0] = 0
    return signals

def apply_sma_crossover(df, params):
    """
    SMA crossover strategy with dynamic periods
    """
    short_window = params.get('short_window', 20)
    long_window = params.get('long_window', 50)

    # Check if required columns exist
    short_col = f'SMA_{short_window}'
    long_col = f'SMA_{long_window}'

    if short_col not in df.columns or long_col not in df.columns:
        raise ValueError(f"Required SMA columns not found. Make sure indicators are added before applying strategy.")

    signals = pd.Series(0, index=df.index)

    # Generate signals
    signals[df[short_col] > df[long_col]] = 1

    # Remove whipsaws
    signals = signals.diff()
    signals = signals.fillna(0)

    return signals