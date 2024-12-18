from src.fetch_data import StockDataFetcher
import pandas as pd
from utils.logger import logger

class DataIngestor:
    """
    DataIngestor is responsible for managing the data ingestion process for stock data.
    This class uses a StockDataFetcher to retrieve data for a specified stock ticker symbol.
    """

    def create_fetcher(self, ticker_symbol: str) -> StockDataFetcher:
        """
        Creates an instance of StockDataFetcher for the given ticker symbol.

        Args:
            ticker_symbol (str): The stock ticker symbol for which to fetch data.
        
        Returns:
            StockDataFetcher: An instance of StockDataFetcher initialized with the provided ticker symbol.
        """
        return StockDataFetcher(ticker_symbol)

    def ingest_data(self, ticker_symbol: str) -> 'pd.DataFrame':
        """
        Ingests stock data for a given ticker symbol by using a StockDataFetcher instance.

        This method initializes a fetcher for the given ticker symbol, fetches the stock data,
        and returns it in a structured format.

        Args:
            ticker_symbol (str): The stock ticker symbol for which to ingest data.

        Returns:
            DataFrame: A pandas DataFrame containing the stock data retrieved by the fetcher.
        """
        logger.info("Started Data Ingestion")
        
        # Create a fetcher for the given ticker symbol
        fetcher = self.create_fetcher(ticker_symbol)
        
        # Fetch the stock data using the fetcher instance
        stock_data = fetcher.fetch_data()
        
        logger.info("Data Ingestion Completed Successfully")
        return stock_data

if __name__ == "__main__":
    # Creating an instance of DataIngestor
    data_ingestor = DataIngestor()
    
    # Example ticker symbol for testing
    ticker_symbol = "AAPL"
    
    # Ingest data for the given ticker symbol and print the result
    stock_data = data_ingestor.ingest_data(ticker_symbol)

    print(f"Stock data for {ticker_symbol}:")
    print(stock_data.tail())


