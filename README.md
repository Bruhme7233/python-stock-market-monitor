# Real-Time Stock Market Monitoring, Analysis and Visualisation System

A Python-based stock market monitoring project that retrieves stock market data, displays market information, and provides a personalised dashboard for selected stocks.

## Features

- Simple demonstration login system.
- Overview of 10 predefined stocks.
- Stock selection based on user interest.
- Personalised dashboard with charts and market information.
- BUY, SELL, and HOLD indicators using a basic educational analysis.
- CSV-based data storage and report generation.
- Automatic dashboard updates.

## Technologies Used

- Python
- Matplotlib
- Pandas
- yfinance
- CSV

## Predefined Stocks

AAPL, NVDA, MSFT, GOOGL, AMZN, INTC, TSM, META, TSLA, AMD.

## Project Structure

| File | Purpose |
|---|---|
| `main.py` | Connects all project modules |
| `authentication.py` | Demonstration login |
| `markoverview.py` | Displays the market overview |
| `stockselector.py` | Allows users to select stocks |
| `fetcher.py` | Retrieves stock market data |
| `visualiser.py` | Displays the personalised dashboard |
| `file_manager.py` | Handles CSV storage and reports |

## Installation

1. Install Python 3.
2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

Open a terminal in the project directory and run:

```bash
python3 main.py
```

## Demonstration Login

- Username: `demo`
- Password: `market123`

These are demonstration credentials, not secure production authentication.

## Data and Limitations

The project uses Yahoo Finance data through the `yfinance` library. Data availability and update frequency depend on the source.

The BUY, SELL, and HOLD indicators are basic educational indicators and should not be treated as financial advice. This project is intended for learning and demonstration purposes.
