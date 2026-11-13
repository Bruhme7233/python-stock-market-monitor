from authentication import LoginScreen
from markoverview import MarketOverview
from stockselector import StockSelector
from fetcher import DataFetcher
from visualiser import StockDashboard
from file_manager import FileManager


# Predefined list of available stocks
WATCHLIST = [
    "AAPL",
    "NVDA",
    "MSFT",
    "GOOGL",
    "AMZN",
    "INTC",
    "TSM",
    "META",
    "TSLA",
    "AMD"
]


# CSV file used to store market history
OUTPUT_LOG_FILE = "live_market_data.csv"


def main():

    print("Starting Stock Market Monitoring System...")

    # STEP 1: Login
    login = LoginScreen()

    if not login.show():
        print("Login unsuccessful. Exiting program.")
        return

    print("Login successful!")


    # STEP 2: Initialise market data fetcher
    fetcher = DataFetcher(
        watch_list=WATCHLIST
    )


    # STEP 3: Initialise CSV file manager
    file_logger = FileManager(
        filename=OUTPUT_LOG_FILE
    )


    # STEP 4: Display complete market overview
    print("Loading market overview...")

    overview = MarketOverview(
        fetcher_instance=fetcher
    )

    proceed, market_data = overview.show()

    if not proceed:
        print("Market overview closed. Exiting program.")
        return


    # STEP 5: Allow the user to select stocks
    print("Opening stock selection screen...")

    selector = StockSelector()

    proceed, selected_stocks = selector.show()

    if not proceed:
        print("Stock selection cancelled. Exiting program.")
        return

    if not selected_stocks:
        print("No stocks selected. Exiting program.")
        return


    print("\nSelected stocks:")

    for stock in selected_stocks:
        print("-", stock)


    # STEP 6: Launch personalised dashboard
    print("\nLaunching personalised dashboard...")

    dashboard = StockDashboard(
        fetcher_instance=fetcher,
        selected_stocks=selected_stocks,
        file_logger=file_logger,
        refresh_seconds=2
    )


    # STEP 7: Run dashboard and generate final report
    try:

        dashboard.run()

    except KeyboardInterrupt:

        print("\nApplication interrupted by user.")

    finally:

        print("\nGenerating final CSV report...")

        file_logger.generate_end_of_run_report()

        print("Application stopped. Goodbye!")


# Start the application
if __name__ == "__main__":
    main()
