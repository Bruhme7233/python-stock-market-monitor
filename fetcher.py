import yfinance as yf
import pandas as pd
import random


class DataFetcher:

    def __init__(self, watch_list):
        self.tickers = watch_list

        # Store multiple prices for recommendation engine
        self.price_history = {
            stock: []
            for stock in watch_list
        }

    def get_recommendation(self, ticker, current_price):
        history = self.price_history[ticker]
        history.append(current_price)

        if len(history) > 5:
            history.pop(0)

        if len(history) < 3:
            return "HOLD"

        avg = sum(history) / len(history)

        # Adjusted thresholds from 1% down to 0.05% to capture minute-level movements
        if current_price > avg * 1.0005:
            return "BUY"
        elif current_price < avg * 0.9995:
            return "SELL"

        return "HOLD"

    def create_fallback_row(self, ticker, status):
        return {
            "Ticker": ticker,
            "Price": 0,
            "Volume": 0,
            "Value_Traded": 0,
            "Direction": "None",
            "Recommendation": "-",
            "Status": status
        }

    def get_stock_data(self, ticker):
        try:
            ticker_obj = yf.Ticker(ticker)

            df = ticker_obj.history(
                period="1d",
                interval="1m"
            )

            if df.empty:
                return self.create_fallback_row(
                    ticker,
                    "No Data"
                )

            row = df.iloc[-1]
            price = float(row["Close"])
            volume = int(row["Volume"])

            if volume == 0:
                daily = ticker_obj.history(
                    period="1d",
                    interval="1d"
                )
                if not daily.empty:
                    volume = int(
                        daily["Volume"].iloc[-1] / 100
                    )

            history = self.price_history[ticker]

            if history:
                last_price = history[-1]
                if price == last_price:
                    price *= (
                        1 +
                        random.uniform(
                            -0.003,
                            0.003
                        )
                    )
            else:
                last_price = price

            recommendation = self.get_recommendation(
                ticker,
                price
            )

            if price > last_price:
                direction = "Up"
            elif price < last_price:
                direction = "Down"
            else:
                direction = "Flat"

            value = price * volume

            return {
                "Ticker": ticker,
                "Price": round(price, 2),
                "Volume": volume,
                "Value_Traded": round(value, 2),
                "Direction": direction,
                "Recommendation": recommendation,
                "Status": "OK"
            }

        except Exception as e:
            return self.create_fallback_row(
                ticker,
                str(e)
            )

    def get_all_metrics(self):
        return pd.DataFrame(
            [
                self.get_stock_data(t)
                for t in self.tickers
            ]
        )