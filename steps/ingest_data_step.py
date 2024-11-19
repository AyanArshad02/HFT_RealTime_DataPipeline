import pandas as pd
from zenml import step
from src.ingest_data import DataIngestor


@step
def ingest_data_step(ticker_symbol: str) -> pd.DataFrame:
    """
    Ingests stock data for a given ticker symbol using the DataIngestor class.

    Parameters:
        ticker_symbol (str): The ticker symbol of the stock to ingest data for (e.g., 'TSLA' for Tesla).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the ingested stock data.
    """
    # Initialize the DataIngestor and ingest stock data
    ingestor = DataIngestor()
    stock_data = ingestor.ingest_data(ticker_symbol)
    return stock_data


# if __name__ == "__main__":
#     ingest_data_step("AAPL")