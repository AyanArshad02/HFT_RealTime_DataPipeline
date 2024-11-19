from zenml import step
from src.fetch_data import StockDataFetcher
import pandas as pd


@step
def fetch_data_step(ticker_symbol: str) -> pd.DataFrame:
    """
    Fetches stock data for a given ticker symbol using the StockDataFetcher class.

    Parameters:
        ticker_symbol (str): The ticker symbol of the stock to fetch data for (e.g. 'AAPL' for Apple).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the fetched stock data.
    """
    # Initialize the StockDataFetcher with the provided ticker symbol
    fetcher = StockDataFetcher(ticker_symbol)
    stock_data = fetcher.fetch_data()
    return stock_data


# if __name__ == "__main__":
#     fetch_data_step("AAPL")