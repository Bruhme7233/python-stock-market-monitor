import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button


class StockSelector:

    WATCHLIST = [
        "AAPL", "NVDA", "MSFT", "GOOGL", "AMZN",
        "INTC", "TSM", "META", "TSLA", "AMD"
    ]

    def __init__(self):

        self.selected_stocks = []
        self.continue_requested = False
        self.stock_buttons = {}

        self.fig = plt.figure(figsize=(12, 8))
        self.fig.patch.set_facecolor("#20252B")

        self.fig.canvas.manager.set_window_title(
            "Stock Market Monitor - Stock Selection"
        )

        # Heading
        self.fig.text(
            0.5, 0.94,
            "PERSONALISED STOCK SELECTION",
            ha="center",
            fontsize=22,
            weight="bold",
            color="#70E0EB"
        )

        self.fig.text(
            0.5, 0.885,
            "Choose the stocks you want to monitor",
            ha="center",
            fontsize=13,
            color="#D7DEE7"
        )

        # Search field
        search_ax = self.fig.add_axes(
            [0.20, 0.79, 0.60, 0.055]
        )

        self.search_box = TextBox(
            search_ax,
            "Search: ",
            initial=""
        )

        self.search_box.label.set_color("#70E0EB")
        self.search_box.text_disp.set_color("#D7DEE7")

        self.search_box.on_submit(
            self.search_stocks
        )

        # Stock selection buttons
        self.create_stock_buttons()

        # Selection status
        self.status = self.fig.text(
            0.5, 0.175,
            "0 stocks selected",
            ha="center",
            fontsize=13,
            color="#70E0EB"
        )

        # Select All
        all_ax = self.fig.add_axes(
            [0.16, 0.065, 0.19, 0.075]
        )

        self.all_button = Button(
            all_ax,
            "SELECT ALL",
            color="#43C6D9",
            hovercolor="#70E0EB"
        )

        self.all_button.on_clicked(
            self.select_all
        )

        # Clear
        clear_ax = self.fig.add_axes(
            [0.405, 0.065, 0.19, 0.075]
        )

        self.clear_button = Button(
            clear_ax,
            "CLEAR",
            color="#45515C",
            hovercolor="#687582"
        )

        self.clear_button.on_clicked(
            self.clear_selection
        )

        # Continue
        continue_ax = self.fig.add_axes(
            [0.65, 0.065, 0.19, 0.075]
        )

        self.continue_button = Button(
            continue_ax,
            "CONTINUE",
            color="#43C6D9",
            hovercolor="#70E0EB"
        )

        self.continue_button.on_clicked(
            self.continue_selection
        )

    def create_stock_buttons(self):

        # Arrange stocks in two columns
        for index, ticker in enumerate(self.WATCHLIST):

            column = index % 2
            row = index // 2

            x_position = 0.16 + column * 0.36
            y_position = 0.67 - row * 0.105

            stock_ax = self.fig.add_axes(
                [x_position, y_position, 0.30, 0.075]
            )

            stock_button = Button(
                stock_ax,
                "[ ] " + ticker,
                color="#303840",
                hovercolor="#45515C"
            )

            stock_button.label.set_color("#70E0EB")
            stock_button.label.set_fontsize(16)

            stock_button.on_clicked(
                lambda event, stock=ticker:
                self.toggle_stock(stock)
            )

            self.stock_buttons[ticker] = stock_button

    def toggle_stock(self, ticker):

        if ticker in self.selected_stocks:
            self.selected_stocks.remove(ticker)
        else:
            self.selected_stocks.append(ticker)

        self.update_buttons()

    def update_buttons(self):

        for ticker, button in self.stock_buttons.items():

            if ticker in self.selected_stocks:

                button.label.set_text("[✓] " + ticker)
                button.ax.set_facecolor("#155766")

            else:

                button.label.set_text("[ ] " + ticker)
                button.ax.set_facecolor("#303840")

        self.status.set_text(
            str(len(self.selected_stocks)) + " stocks selected"
        )

        self.fig.canvas.draw_idle()

    def select_all(self, event):

        self.selected_stocks = self.WATCHLIST.copy()
        self.update_buttons()

    def clear_selection(self, event):

        self.selected_stocks = []
        self.update_buttons()

    def search_stocks(self, text):

        query = text.strip().upper()

        matches = [
            ticker for ticker in self.WATCHLIST
            if query in ticker
        ]

        for ticker, button in self.stock_buttons.items():

            if not query or ticker in matches:
                button.label.set_color("#70E0EB")
            else:
                button.label.set_color("#687582")

        if matches:

            self.status.set_text(
                "Matching stocks: " + ", ".join(matches)
            )

        else:

            self.status.set_text(
                "No matching stocks in the available catalogue."
            )

        self.fig.canvas.draw_idle()

    def continue_selection(self, event):

        if not self.selected_stocks:

            self.status.set_text(
                "Please select at least one stock!"
            )

            self.fig.canvas.draw_idle()
            return

        self.continue_requested = True
        plt.close(self.fig)

    def show(self):

        plt.show()

        return (
            self.continue_requested,
            self.selected_stocks
        )


# Independent testing
if __name__ == "__main__":

    selector = StockSelector()

    proceed, selected = selector.show()

    if proceed:

        print("\nSelected stocks:")

        for ticker in selected:
            print(ticker)

    else:
        print("Stock selection cancelled.")
