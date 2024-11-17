from zenml.steps import step
from src.fetch_data import StockDataFetcher
import pandas as pd


@step
def fetch_data_step(ticker_symbol: str) -> 'pd.DataFrame':
    """
    Fetches stock data for a given ticker symbol using the StockDataFetcher class.

    This ZenML step integrates with the `StockDataFetcher` module to retrieve
    historical stock data for a specified ticker symbol.

    Parameters:
        ticker_symbol (str): The ticker symbol of the stock to fetch data for (e.g., 'AAPL' for Apple Inc.).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the fetched stock data.

    """
    fetcher = StockDataFetcher(ticker_symbol)
    stock_data = fetcher.fetch_data()
    return stock_data