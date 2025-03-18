import pandas as pd
import numpy as np

def apply_strategy(df, strategy_name, params=None):
    """
    Apply selected trading strategy to the data
    """
    if strategy_name == "Buy and Hold":
        return apply_buy_and_hold(df)
    elif strategy_name == "Simple Moving Average Crossover":
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
    SMA crossover strategy
    """
    short_window = params['short_window']
    long_window = params['long_window']
    
    signals = pd.Series(0, index=df.index)
    
    # Generate signals
    signals[df[f'SMA_{short_window}'] > df[f'SMA_{long_window}']] = 1
    
    # Remove whipsaws
    signals = signals.diff()
    signals = signals.fillna(0)
    
    return signals
