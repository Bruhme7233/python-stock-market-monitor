import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pandas as pd


class MarketOverview:

    def __init__(self, fetcher_instance):

        plt.style.use("dark_background")

        self.fetcher = fetcher_instance
        self.market_data = pd.DataFrame()
        self.continue_requested = False

        # Main window
        self.fig = plt.figure(figsize=(15, 8))
        self.fig.patch.set_facecolor("#20252B")

        self.fig.canvas.manager.set_window_title(
            "Stock Market Monitor - Market Overview"
        )

        # Heading
        self.fig.text(
            0.5, 0.94,
            "GLOBAL MARKET OVERVIEW",
            ha="center",
            fontsize=21,
            weight="bold",
            color="#70E0EB"
        )

        self.fig.text(
            0.5, 0.89,
            "Live overview of all 10 available stocks",
            ha="center",
            fontsize=11,
            color="#D7DEE7"
        )

        # Table area
        self.ax_table = self.fig.add_axes(
            [0.035, 0.19, 0.93, 0.64]
        )
        self.ax_table.axis("off")

        # Status message
        self.status = self.fig.text(
            0.5, 0.12,
            "Initializing market data...",
            ha="center",
            fontsize=10,
            color="#70E0EB"
        )

        # Refresh button
        ax_refresh = self.fig.add_axes(
            [0.28, 0.035, 0.18, 0.06]
        )

        self.refresh_button = Button(
            ax_refresh,
            "REFRESH",
            color="#43C6D9",
            hovercolor="#70E0EB"
        )

        self.refresh_button.on_clicked(
            self.refresh_data
        )

        # Continue button
        ax_continue = self.fig.add_axes(
            [0.54, 0.035, 0.22, 0.06]
        )

        self.continue_button = Button(
            ax_continue,
            "SELECT STOCKS",
            color="#43C6D9",
            hovercolor="#70E0EB"
        )

        self.continue_button.on_clicked(
            self.continue_to_selection
        )

        # Exit button
        ax_exit = self.fig.add_axes(
            [0.80, 0.035, 0.14, 0.06]
        )

        self.exit_button = Button(
            ax_exit,
            "EXIT",
            color="#FF8BAA",
            hovercolor="#FFB3C5"
        )

        self.exit_button.on_clicked(
            self.exit_application
        )

    def refresh_data(self, event=None):

        self.status.set_text(
            "Fetching latest market information..."
        )
        self.fig.canvas.draw_idle()

        # Fetch all 10 stocks
        self.market_data = self.fetcher.get_all_metrics()

        self.draw_table()

        self.status.set_text(
            "Market data updated successfully."
        )

        self.fig.canvas.draw_idle()

    def draw_table(self):

        self.ax_table.clear()
        self.ax_table.axis("off")

        if self.market_data.empty:
            self.ax_table.text(
                0.5, 0.5,
                "No market data available",
                ha="center",
                color="white"
            )
            return

        # Format data for display
        display_data = []

        for _, row in self.market_data.iterrows():

            display_data.append([
                row["Ticker"],
                f"${row['Price']:,.2f}",
                f"{row['Volume']:,}",
                f"${row['Value_Traded'] / 1e6:,.2f}M",
                row["Direction"],
                row["Recommendation"],
                str(row["Status"])[:18]
            ])

        headers = [
            "STOCK",
            "PRICE (USD)",
            "VOLUME",
            "VALUE TRADED",
            "DIRECTION",
            "SIGNAL",
            "STATUS"
        ]

        table = self.ax_table.table(
            cellText=display_data,
            colLabels=headers,
            cellLoc="center",
            loc="center",
            colWidths=[
                0.10, 0.12, 0.14, 0.17,
                0.14, 0.13, 0.15
            ]
        )

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.0)

        # Style table cells
        for (row, col), cell in table.get_celld().items():

            cell.set_edgecolor("#45515C")

            if row == 0:

                cell.set_facecolor("#263C46")
                cell.set_text_props(
                    color="#70E0EB",
                    weight="bold"
                )

            else:

                cell.set_facecolor(
                    "#252C33" if row % 2 else "#303840"
                )

                cell.set_text_props(
                    color="#D7DEE7"
                )

                # Direction colours
                if col == 4:

                    direction = display_data[row - 1][4]

                    if direction == "Up":
                        cell.set_text_props(color="#A9E6B4")

                    elif direction == "Down":
                        cell.set_text_props(color="#FF8BAA")

                # Recommendation colours
                if col == 5:

                    signal = display_data[row - 1][5]

                    if signal == "BUY":
                        cell.set_text_props(color="#A9E6B4")

                    elif signal == "SELL":
                        cell.set_text_props(color="#FF8BAA")

                    else:
                        cell.set_text_props(color="#F5D18A")

    def continue_to_selection(self, event):

        self.continue_requested = True
        plt.close(self.fig)

    def exit_application(self, event):

        self.continue_requested = False
        plt.close(self.fig)

    def show(self):

        self.refresh_data()
        plt.show()

        return self.continue_requested, self.market_data


# Independent testing
if __name__ == "__main__":

    from fetcher import DataFetcher

    WATCHLIST = [
        "AAPL", "NVDA", "MSFT", "GOOGL", "AMZN",
        "INTC", "TSM", "META", "TSLA", "AMD"
    ]

    fetcher = DataFetcher(watch_list=WATCHLIST)

    overview = MarketOverview(fetcher)

    proceed, data = overview.show()

    if proceed:
        print("Proceeding to stock selection...")
        print(data)

    else:
        print("Market overview closed.")