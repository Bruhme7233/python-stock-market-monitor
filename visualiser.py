import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from datetime import datetime


class StockDashboard:

    def __init__(self, fetcher_instance, selected_stocks=None,
                 file_logger=None, refresh_seconds=2):

        self.fetcher = fetcher_instance
        self.selected_stocks = selected_stocks
        self.file_logger = file_logger

        # Convert seconds into milliseconds
        self.interval_ms = int(refresh_seconds * 1000)

        self.time_labels = []
        self.total_values = []

        self.fig, self.axes = plt.subplots(
            2, 2, figsize=(13, 8)
        )

        self.fig.suptitle(
            "Personalised Stock Market Dashboard",
            fontsize=16,
            fontweight="bold"
        )

        try:
            self.fig.canvas.manager.set_window_title(
                "Stock Market Monitoring System"
            )
        except Exception:
            pass

        # Leave space at the bottom for the Exit button
        plt.tight_layout(rect=[0, 0.08, 1, 0.94])

        # Exit button
        ax_exit = self.fig.add_axes(
            [0.84, 0.015, 0.12, 0.05]
        )

        self.exit_button = Button(
            ax_exit,
            "EXIT",
            color="#FF8BAA",
            hovercolor="#FFB3C5"
        )

        self.exit_button.on_clicked(
            self.exit_dashboard
        )


    def draw_pie_chart(self, df):

        ax = self.axes[0, 0]
        ax.clear()

        ax.set_title("Value Traded Share")

        if df.empty or df["Value_Traded"].sum() <= 0:
            ax.text(
                0.5, 0.5,
                "No data available",
                ha="center",
                va="center"
            )
            return

        ax.pie(
            df["Value_Traded"],
            labels=df["Ticker"],
            autopct="%1.1f%%",
            startangle=90
        )


    def draw_bar_chart(self, df):

        ax = self.axes[0, 1]
        ax.clear()

        ax.set_title("Value Traded by Stock")

        if df.empty:
            ax.text(
                0.5, 0.5,
                "No data available",
                ha="center",
                va="center"
            )
            return

        sorted_df = df.sort_values(
            by="Value_Traded",
            ascending=True
        )

        ax.barh(
            sorted_df["Ticker"],
            sorted_df["Value_Traded"]
        )

        ax.set_xlabel("Value Traded")


    def draw_trend_line(self, current_time, df):

        ax = self.axes[1, 0]
        ax.clear()

        ax.set_title("Selected Stocks Value Over Time")

        if df.empty:
            ax.text(
                0.5, 0.5,
                "No data available",
                ha="center",
                va="center"
            )
            return

        total_value = df["Value_Traded"].sum()

        self.time_labels.append(current_time)
        self.total_values.append(total_value)

        # Keep the latest 30 readings
        self.time_labels = self.time_labels[-30:]
        self.total_values = self.total_values[-30:]

        ax.plot(
            range(len(self.total_values)),
            self.total_values,
            marker="o"
        )

        ax.set_xlabel("Refresh Number")
        ax.set_ylabel("Total Value Traded")
        ax.grid(True)


    def draw_summary_table(self, current_time, df):

        ax = self.axes[1, 1]
        ax.clear()
        ax.axis("off")

        ax.set_title(
            "Personal Market Analytics",
            fontsize=12,
            fontweight="bold"
        )

        if df.empty:
            ax.text(
                0.5, 0.5,
                "No stock data available",
                ha="center",
                va="center"
            )
            return

        total_volume = df["Volume"].sum()
        total_value = df["Value_Traded"].sum()

        most_active = df.loc[
            df["Volume"].idxmax()
        ]

        summary = (
            f"Last Updated: {current_time}\n\n"
            f"Selected Stocks: {len(df)}\n\n"
            f"Total Trading Volume: {total_volume:,.0f}\n\n"
            f"Total Value Traded: {total_value:,.2f}\n\n"
            f"Most Active Stock: {most_active['Ticker']}\n\n"
            f"Highest Volume: {most_active['Volume']:,.0f}\n\n"
            f"Refresh Interval: 2 Seconds"
        )

        ax.text(
            0.05,
            0.95,
            summary,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top"
        )


    def update_plots(self, frame):

        try:

            # Fetch market data once for this refresh
            all_market_data = self.fetcher.get_all_metrics()

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            # Save all 10 stocks to the CSV file
            if self.file_logger is not None:
                self.file_logger.log_snapshot(
                    all_market_data
                )

            # Filter data for the personalised dashboard
            if self.selected_stocks is not None:

                df = all_market_data[
                    all_market_data["Ticker"].isin(
                        self.selected_stocks
                    )
                ].copy()

            else:
                df = all_market_data.copy()

            # Update all four dashboard panels
            self.draw_pie_chart(df)
            self.draw_bar_chart(df)
            self.draw_trend_line(current_time, df)
            self.draw_summary_table(current_time, df)

            self.fig.suptitle(
                "Personalised Stock Market Dashboard",
                fontsize=16,
                fontweight="bold"
            )

            self.fig.tight_layout(
                rect=[0, 0.08, 1, 0.94]
            )

            print(
                f"\nDashboard refreshed at {current_time}"
            )

            print(df.to_string(index=False))

        except Exception as error:

            print("Dashboard update error:", error)


    def exit_dashboard(self, event=None):

        # Stop automatic updates before closing the window
        if hasattr(self, "animation"):
            if self.animation.event_source is not None:
                self.animation.event_source.stop()

        plt.close(self.fig)

    def run(self):

        self.animation = animation.FuncAnimation(
            self.fig,
            self.update_plots,
            interval=self.interval_ms,
            cache_frame_data=False
        )

        plt.show()