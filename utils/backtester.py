import pandas as pd
import numpy as np

def backtest_strategy(df, signals, initial_capital, stop_loss):
    """
    Backtest the trading strategy
    """
    position = 0
    portfolio_value = float(initial_capital)
    holdings = 0.0

    # Initialize results DataFrame with proper dtypes
    results = pd.DataFrame(index=df.index)
    results['position'] = 0
    results['portfolio_value'] = float(initial_capital)
    results['position_changed'] = False
    results['trade_type'] = ''  # New column for trade type
    results['Close'] = df['Close']  # Add Close price to results

    stop_loss_decimal = stop_loss / 100
    entry_price = 0.0

    for i in range(len(df)):
        current_price = float(df['Close'].iloc[i])

        # Check stop loss
        if position == 1 and entry_price > 0:
            loss_percentage = (entry_price - current_price) / entry_price
            if loss_percentage >= stop_loss_decimal:
                signals.iloc[i] = -1  # Force sell

        # Process signals
        if signals.iloc[i] == 1 and position == 0:  # Buy signal
            position = 1
            holdings = portfolio_value / current_price
            entry_price = current_price
            results.iloc[i, results.columns.get_loc('position_changed')] = True
            results.iloc[i, results.columns.get_loc('trade_type')] = 'Buy'

        elif signals.iloc[i] == -1 and position == 1:  # Sell signal
            position = 0
            portfolio_value = holdings * current_price
            holdings = 0.0
            entry_price = 0.0
            results.iloc[i, results.columns.get_loc('position_changed')] = True
            results.iloc[i, results.columns.get_loc('trade_type')] = 'Sell'

        # Update portfolio value
        results.iloc[i, results.columns.get_loc('position')] = position
        if holdings > 0:
            results.iloc[i, results.columns.get_loc('portfolio_value')] = float(holdings * current_price)
        else:
            results.iloc[i, results.columns.get_loc('portfolio_value')] = float(portfolio_value)

    return results