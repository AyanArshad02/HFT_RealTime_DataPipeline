from ingest_data import DataIngestor
import pandas as pd
from utils.logger import logger

"""
Here I am using Template Design Patter for handling Missing values.
"""

class MissingValueHandler:
    """
    A class to handle missing values in a stock data DataFrame.

    Methods
    -------
    handle(stock_data: DataFrame) -> DataFrame
        Public method to handle missing values in stock data.
        
    _handle_missing_values(stock_data: DataFrame) -> DataFrame
        Private method to process missing values by forward filling and dropping
        remaining NaNs if present.
    """
    
    def handle(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        Public method to handle missing values in the stock data.

        Parameters
        ----------
        stock_data : DataFrame
            The DataFrame containing stock data with potential missing values.

        Returns
        -------
        DataFrame
            The DataFrame with missing values handled.
        """
        logger.info("Started Handling Missing Valuess")
        return self._handle_missing_values(stock_data)

    def _handle_missing_values(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        Private method to handle missing values by forward filling and
        dropping remaining rows with NaNs.

        Parameters
        ----------
        stock_data : DataFrame
            The DataFrame containing stock data with potential missing values.

        Returns
        -------
        DataFrame
            The DataFrame with missing values handled (forward-filled and
            dropped where NaNs are still present).
        """
        
        # Check if any missing values are present in the DataFrame
        if stock_data.isnull().values.any():
            # Forward fill then Backward fill
            stock_data = stock_data.fillna(method='ffill').fillna(method='bfill')
            
            # Drop rows where NaNs still exist after forward filling
            stock_data = stock_data.dropna()
        
        logger.info("Handling Missing Value Completed Successfully")
        return stock_data


if __name__ == "__main__":
    # Create an instance of DataIngestor
    data_ingestor = DataIngestor()
    
    # Example ticker symbol for testing
    ticker_symbol = "AAPL"
    
    # Ingest data for the given ticker symbol and print the result
    stock_data = data_ingestor.ingest_data(ticker_symbol)

    # Instantiate the MissingValueHandler
    handler = MissingValueHandler()

    # Process the DataFrame to handle missing values
    processed_data = handler.handle(stock_data)
    print(processed_data.tail())
