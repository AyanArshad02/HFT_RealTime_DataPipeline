import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from abc import ABC, abstractmethod
import yfinance as yf
import psycopg2
from utils.config import DB_PARAMS
from datetime import timedelta
from utils.logger import logger

#Define an abstract class for fetching data
class DataFetchingStrategy:
    "Abstract method to fetch data"
    @abstractmethod
    def fetch(self, ticker_symbol):
        raise NotImplementedError("This method should be overridden by subclasses.")

class MaxPeriodFetchingStrategy(DataFetchingStrategy):
    def fetch(self, ticker_symbol):
        stock_data = yf.download(ticker_symbol, period='max')
        return stock_data

class HistoricalFetchingStrategy(DataFetchingStrategy):
    def fetch(self, ticker_symbol, start_date):
        stock_data = yf.download(ticker_symbol, start=start_date)
        return stock_data

class StockDataFetcher:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol

    def get_last_date_from_db(self):
        conn = psycopg2.connect(**DB_PARAMS)
        try:
            query = "SELECT MAX(date) FROM processed_data WHERE symbol = %s"
            with conn.cursor() as cur:
                cur.execute(query, (self.ticker_symbol,))
                result = cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error fetching last date from DB: {e}")
            raise
        finally:
            conn.close()

    def fetch_data(self):
        last_date = self.get_last_date_from_db()
        if last_date:
            start_date = last_date + timedelta(days=1)
            strategy = HistoricalFetchingStrategy()
            stock_data = strategy.fetch(self.ticker_symbol, start_date)
        else:
            strategy = MaxPeriodFetchingStrategy()
            stock_data = strategy.fetch(self.ticker_symbol)

        logger.info(f"Fetched data for {self.ticker_symbol} from {start_date if last_date else 'beginning'}")
        return stock_data

if __name__ == "__main__":
    # Example ticker symbol for testing
    ticker_symbol = "AAPL"
    
    # Initialize the StockDataFetcher with the ticker symbol
    stock_data_fetcher = StockDataFetcher(ticker_symbol)
    
    # Fetch the stock data
    stock_data = stock_data_fetcher.fetch_data()
    
    # Display the fetched data (for testing purposes, you can adjust this as needed)
    print(stock_data.tail())  # Print the first few rows of the stock data
