import pandas as pd
from zenml.steps import step

from src.storing_preprocessed_data import DataStorer

@step
def storing_preprocessed_data_step(stock_data, ticker_symbol) -> None:
    """
    Stores the preprocessed stock data for a given ticker symbol using the DataStorer class.

    Parameters:
        stock_data (pd.DataFrame): A pandas DataFrame containing the preprocessed stock data to be stored.
        ticker_symbol (str): The ticker symbol of the stock, used to label or identify the stored data.

    Returns:
        None
    """
    storer = DataStorer()
    storer.store(stock_data, ticker_symbol)