
import os
import pandas as pd
from datetime import datetime


class FileManager:
    def __init__(self, filename="market_history.csv"):
        self.filename = filename
        print(f"File logger ready. Target output: {self.filename}")

    def log_snapshot(self, df):
        """
        Appends the latest market data to a CSV file.
        Adds a timestamp to every recorded stock.
        """

        if df.empty:
            return

        try:
            log_df = df.copy()

            log_df['Timestamp'] = datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'
            )

            # Keep Timestamp as the first column
            cols = ['Timestamp'] + [
                col for col in log_df.columns
                if col != 'Timestamp'
            ]

            log_df = log_df[cols]

            # Write headers only when creating a new or empty file
            file_exists = os.path.isfile(self.filename)

            write_header = (
                not file_exists
                or os.path.getsize(self.filename) == 0
            )

            log_df.to_csv(
                self.filename,
                mode='a',
                header=write_header,
                index=False
            )

            print(f"[DISK IO] Saved snapshot to {self.filename}")

        except Exception as e:
            print(f"Warning: Failed to save data snapshot: {e}")

    def generate_end_of_run_report(self):
        """
        Reads the accumulated CSV file and generates
        a summary of the captured market activity.
        """

        if not os.path.isfile(self.filename):
            print("No data log found to generate a final report.")
            return

        try:
            # Read CSV using its existing column headers
            full_history = pd.read_csv(self.filename)

            print(
                "\n"
                + "=" * 20
                + " DATA LOG METRICS SUMMARY "
                + "=" * 20
            )

            print(
                f"Total data entries captured: {len(full_history)}"
            )

            # Check that the required columns exist
            required_columns = [
                'Ticker',
                'Timestamp',
                'Value_Traded'
            ]

            for column in required_columns:
                if column not in full_history.columns:
                    raise ValueError(
                        f"Required CSV column missing: {column}"
                    )

            # Convert transaction values into numeric format
            full_history['Value_Traded'] = pd.to_numeric(
                full_history['Value_Traded'],
                errors='coerce'
            )

            # Ignore rows with invalid transaction values
            valid_history = full_history.dropna(
                subset=['Value_Traded']
            )

            if not valid_history.empty:

                # Find the highest recorded trading value
                max_row = valid_history.loc[
                    valid_history['Value_Traded'].idxmax()
                ]

                peak_value = max_row['Value_Traded'] / 1e6

                print(
                    f"Peak Activity: {max_row['Ticker']} "
                    f"at {max_row['Timestamp']} "
                    f"(${peak_value:.2f}M)"
                )

            else:
                print("No valid transaction values found.")

            print("=" * 66 + "\n")

        except Exception as e:
            print(
                f"Could not construct post-run analytics summary: {e}"
            )


