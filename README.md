# Indian Stock Market Backtesting Application

A Python-based web application for backtesting trading strategies on Indian stocks using Streamlit.

## Features

- Test multiple trading strategies:
  - Buy and Hold
  - Simple Moving Average Crossover (with customizable periods)
- Interactive visualizations:
  - Price charts with technical indicators
  - Portfolio value over time
  - Trade log with entry/exit points
- Risk Management:
  - Configurable stop-loss
  - Position sizing
- Support for Indian stock symbols (NSE)

## Getting Started

### Prerequisites

Make sure you have Python 3.11+ installed on your system.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/indian-stock-backtester.git
cd indian-stock-backtester
```

2. Install the required packages:
```bash
pip install streamlit pandas yfinance plotly
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter a valid NSE stock symbol (e.g., RELIANCE.NS, TCS.NS)
2. Select your desired strategy:
   - Buy and Hold: Simple long-term holding strategy
   - SMA Crossover: Uses moving average crossovers for trading signals
3. Configure strategy parameters:
   - For SMA Crossover: Adjust short and long moving average periods
4. Set risk management parameters:
   - Initial capital
   - Stop loss percentage
5. View the results in the interactive dashboard:
   - Price chart with indicators
   - Portfolio value curve
   - Performance metrics
   - Detailed trade log...

## Project Structure

```
├── utils/
│   ├── data_loader.py    # Stock data fetching
│   ├── indicators.py     # Technical indicators
│   ├── strategies.py     # Trading strategies
│   └── backtester.py     # Backtesting engine
├── app.py               # Main Streamlit application
└── README.md           # Project documentation
```

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.