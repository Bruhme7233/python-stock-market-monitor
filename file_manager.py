import os
import pandas as pd
from datetime import datetime

class FileManager:
    def __init__(self, filename="market_history.csv"):
        self.filename = filename
        print(f"File logger ready. Target output: {self.filename}")

    def log_snapshot(self, df):
        """
        Appends the latest market data dataframe onto a local CSV file.
        Includes a timestamp so historical trends can be traced later.
        """
        if df.empty:
            return

        try:
            # Create a copy of the dataframe to avoid altering the main runtime data
            log_df = df.copy()
            
            # Add timestamp markings to every single row
            log_df['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Reorder columns slightly just to make the CSV sheet look clean
            cols = ['Timestamp'] + [col for col in log_df.columns if col != 'Timestamp']
            log_df = log_df[cols]
            
            # Check if file exists. If it doesn't, write headers. If it does, just append rows.
            file_exists = os.path.isfile(self.filename)
            
            log_df.to_csv(
                self.filename, 
                mode='a', 
                header=not file_exists, 
                index=False
            )
            print(f"[DISK IO] Saved snapshot to {self.filename}")
            
        except Exception as e:
            # Catching errors like permission issues or the file being locked open in Excel
            print(f"Warning: Failed to save data snapshot to disk: {e}")

    def generate_end_of_run_report(self):
        """
        Reads the entire accumulated CSV and prints out basic analytical conclusions.
        Great feature to show off data aggregation concepts to your teacher.
        """
        if not os.path.isfile(self.filename):
            print("No data log found to generate a final report.")
            return

        try:
            full_history = pd.read_csv(self.filename)
            print("\n" + "="*20 + " DATA LOG METRICS SUMMARY " + "="*20)
            print(f"Total data entries captured: {len(full_history)}")
            
            # Find the stock with the single highest value transaction frame recorded
            max_row = full_history.loc[full_history['Value_Traded'].idxmax()]
            print(f"Peak Activity: {max_row['Ticker']} at {max_row['Timestamp']} (${max_row['Value_Traded']/1e6:.2f}M)")
            print("="*66 + "\n")
            
        except Exception as e:
            print(f"Could not construct post-run analytics summary: {e}")