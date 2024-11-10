import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logger
from ingest_data import DataIngestor
from handle_missing_value import MissingValueHandler

"""
Here I am using template design pattern for Feature Engineering
"""

class FeatureEngineer:
    """
    A class for feature engineering of stock data.

    Methods
    -------
    engineer(stock_data : pd.DataFrame) -> pd.DataFrame
        public method for stock data feature engineering

    _create_features(stock_data : pd.DataFrame) -> pd.DataFrame
        private method for stock data feature engineering. It will add 3 columns
        i.e. Return, Volatility, Moving Average    
    """

    def engineer(self, stock_data : pd.DataFrame) -> pd.DataFrame:
        """
        Public method for stock data feature engineering.

        Parameters:
        ----------
        stock_data : pd.DataFrame

        Returns:
        -------
        stock_data : pd.DataFrame
            stock data with 3 more features added.
        """
        logger.info("Feature Engineering started")
        return self._create_features(stock_data)

    def _create_features(self, stock_data : pd.DataFrame) -> pd.DataFrame:
        """
        private method to create new features for stock data

        This method adds the following columns:
        - 'Return': The percentage change in closing price from the previous day.
        - 'Volatility': The rolling standard deviation of 'Return' over a 5 day window.
        - 'Moving Average': The rolling average of the 'Close' price over a 20 day window.

        Parameters:
        ----------
        stock_data : pd.DataFrame

        Returns:
        -------
        stock_data : pd.DataFrame
            A stock data with 3 columns added i.e. Return, Volatility, Moving Average
        """
        stock_data['Return'] = stock_data['Close'].pct_change()
        stock_data['Volatility'] = stock_data['Return'].rolling(window=5).std()
        stock_data['Moving Average'] = stock_data['Close'].rolling(window=5).mean()
        logger.info("Feature Engineering completed successfully")
        return stock_data
    

if __name__=="__main__":
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

    # Instantiate the FeatureEngineer
    feature_engineering = FeatureEngineer()

    # Feature engineering processed data and storing it in stock_data variable
    stock_data = feature_engineering.engineer(processed_data)
    print(stock_data.tail())
