import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_loader import load_stock_data
from utils.strategies import apply_strategy
from utils.indicators import add_indicators
from utils.backtester import backtest_strategy

def main():
    st.title("Indian Stock Market Backtesting")

    # Sidebar inputs
    st.sidebar.header("Configuration")

    # Stock Selection
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, TCS.NS)", "RELIANCE.NS")

    # Date Range Selection
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    start_date = st.sidebar.date_input("Start Date", start_date)
    end_date = st.sidebar.date_input("End Date", end_date)

    # Strategy Selection
    strategy = st.sidebar.selectbox(
        "Select Strategy",
        ["Buy and Hold", "Simple Moving Average Crossover"]
    )

    # Capital Input
    initial_capital = st.sidebar.number_input("Initial Capital (₹)", 
                                          min_value=10000, 
                                          value=100000, 
                                          step=10000)

    # Strategy Parameters
    strategy_params = {}
    if strategy == "Simple Moving Average Crossover":
        short_window = st.sidebar.slider("Short MA Period", 5, 50, 20)
        long_window = st.sidebar.slider("Long MA Period", 20, 200, 50)
        strategy_params = {
            "short_window": short_window,
            "long_window": long_window
        }

    # Risk Management
    stop_loss = st.sidebar.number_input("Stop Loss (%)", 
                                     min_value=0.0, 
                                     max_value=100.0, 
                                     value=5.0)

    try:
        # Load Data
        df = load_stock_data(stock_symbol, start_date, end_date)

        if df is not None and not df.empty:
            # Add indicators
            df = add_indicators(df, strategy, strategy_params)

            # Apply strategy
            signals = apply_strategy(df, strategy, strategy_params)

            # Run backtest
            results = backtest_strategy(df, signals, initial_capital, stop_loss)

            # Display Results
            st.header("Backtesting Results")

            # Price Chart with Signals
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'],
                                  mode='lines',
                                  name='Close Price'))

            if strategy == "Simple Moving Average Crossover":
                fig.add_trace(go.Scatter(x=df.index, 
                                      y=df[f'SMA_{strategy_params["short_window"]}'],
                                      mode='lines',
                                      name=f'SMA {strategy_params["short_window"]}'))
                fig.add_trace(go.Scatter(x=df.index, 
                                      y=df[f'SMA_{strategy_params["long_window"]}'],
                                      mode='lines',
                                      name=f'SMA {strategy_params["long_window"]}'))

            fig.update_layout(title='Price and Indicators',
                          xaxis_title='Date',
                          yaxis_title='Price (₹)',
                          template='plotly_white')
            st.plotly_chart(fig)

            # Equity Curve
            fig_equity = go.Figure()
            fig_equity.add_trace(go.Scatter(x=results.index, 
                                        y=results['portfolio_value'],
                                        mode='lines',
                                        name='Portfolio Value'))
            fig_equity.update_layout(title='Portfolio Value Over Time',
                                 xaxis_title='Date',
                                 yaxis_title='Value (₹)',
                                 template='plotly_white')
            st.plotly_chart(fig_equity)

            # Performance Metrics
            col1, col2, col3 = st.columns(3)
            total_return = ((results['portfolio_value'].iloc[-1] - initial_capital) / 
                         initial_capital * 100)

            col1.metric("Total Return", f"{total_return:.2f}%")
            col2.metric("Number of Trades", len(results[results['position_changed']]))
            col3.metric("Final Portfolio Value", f"₹{results['portfolio_value'].iloc[-1]:,.2f}")

            # Trade Log
            st.subheader("Trade Log")
            trade_log = results[results['position_changed']].copy()
            if not trade_log.empty:
                # Format the trade log for display
                display_log = pd.DataFrame({
                    'Date': trade_log.index.strftime('%Y-%m-%d'),
                    'Action': trade_log['trade_type'],
                    'Price': trade_log['Close'],
                    'Portfolio Value': trade_log['portfolio_value']
                })
                st.dataframe(
                    display_log,
                    column_config={
                        'Portfolio Value': st.column_config.NumberColumn(
                            'Portfolio Value',
                            format="₹%.2f"
                        ),
                        'Price': st.column_config.NumberColumn(
                            'Price',
                            format="₹%.2f"
                        )
                    }
                )
            else:
                st.info("No trades were executed during this period.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()