import sys
import os

import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from abc import ABC, abstractmethod
import yfinance as yf
import psycopg2
from utils.config import DB_PARAMS
from datetime import timedelta
from utils.logger import logger

"""
Here we are using Strategy Design Pattern for Fetching Stock Data.
"""

#Defining an abstract class for fetching data
class DataFetchingStrategy:
    """
    Abstract class to define the strategy for fetching stock data.
    
    Methods:
    ----------
    fetch(ticker_symbol: str) -> pd.DataFrame:
        Fetches stock data for the given ticker symbol.
    """
    @abstractmethod
    def fetch(self, ticker_symbol : str) -> 'pd.DataFrame':
        """
        Abstract method to fetch stock data.

        Args:
            ticker_symbol (str): The stock ticker symbol to fetch data for.

        Returns:
            pd.DataFrame: The stock data for the given ticker symbol.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

class MaxPeriodFetchingStrategy(DataFetchingStrategy):
    """
    Concrete strategy for fetching the maximum period of stock data.

    Methods:
    ----------
    fetch(ticker_symbol: str) -> pd.DataFrame:
        Fetches stock data for the given ticker symbol for the maximum available period.
    """

    def fetch(self, ticker_symbol : str) -> 'pd.DataFrame':
        """
        Fetches stock data for the given ticker symbol for the maximum available period.

        Args:
            ticker_symbol (str): The stock ticker symbol to fetch data for.

        Returns:
            pd.DataFrame: The stock data for the maximum available period.
        """

        stock_data = yf.download(ticker_symbol, period='max')
        return stock_data

class HistoricalFetchingStrategy(DataFetchingStrategy):
    """
    Concrete strategy for fetching historical stock data starting from a given date.

    Methods:
    ----------
    fetch(ticker_symbol: str, start_date: str) -> pd.DataFrame:
        Fetches stock data for the given ticker symbol starting from a specific date.
    """

    def fetch(self, ticker_symbol : str, start_date : str) -> 'pd.DataFrame':
        """
        Fetches stock data for the given ticker symbol starting from a specific date.

        Args:
            ticker_symbol (str): The stock ticker symbol to fetch data for.
            start_date (str): The start date to fetch data from.

        Returns:
            pd.DataFrame: The stock data starting from the given date.
        """
        stock_data = yf.download(ticker_symbol, start=start_date)
        return stock_data

class StockDataFetcher:
    """
    Class to fetch stock data using different strategies based on the availability of data in the database.

    Attributes:
    -----------
    ticker_symbol (str): The stock ticker symbol to fetch data for.

    Methods:
    --------
    get_last_date_from_db() -> str:
        Retrieves the last date of processed data for the ticker symbol from the database.

    fetch_data() -> pd.DataFrame:
        Fetches stock data based on the last date in the database or from the start.
    """
    def __init__(self, ticker_symbol:str) -> None:
        """
        Initializes the StockDataFetcher with the given ticker symbol.

        Args:
            ticker_symbol (str): The stock ticker symbol to fetch data for.
        """
        self.ticker_symbol = ticker_symbol

    def get_last_date_from_db(self) -> str:
        """
        Retrieves the last date of processed data for the ticker symbol from the database.

        Returns:
            str: The last date of processed data for the ticker symbol, or None if no data exists.
        
        Raises:
            Exception: If there is an error while fetching data from the database.
        """

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

    def fetch_data(self) -> 'pd.DataFrame':
        """
        Fetches stock data based on the last date in the database or from the start if no data exists.

        Returns:
            pd.DataFrame: The stock data for the ticker symbol.

        Notes:
            If there is a record of previous data in the database, it will fetch data starting from the day after the last processed date.
            Otherwise, it fetches the entire available stock data.
        """
        
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
    
    # Initializing the StockDataFetcher with the ticker symbol
    stock_data_fetcher = StockDataFetcher(ticker_symbol)
    
    # Fetching the stock data
    stock_data = stock_data_fetcher.fetch_data()
    
    # Display the fetched data (for testing purposes, you can adjust this as needed)
    print(stock_data.tail())  # Print the last few rows of the stock data
