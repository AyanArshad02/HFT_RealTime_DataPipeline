import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import DB_PARAMS
from utils.logger import logger

from src.ingest_data import DataIngestor
from src.handle_missing_value import MissingValueHandler
from src.feature_engineering import FeatureEngineer


class DataStorer:
    """
    A class to handle storing processed stock data in a PostgreSQL database.

    Methods:
    --------
    store(stock_data, ticker_symbol):
        Stores stock data for a specified ticker symbol in the database.
        Inserts data row-by-row, and handles conflicts by ignoring duplicates.
    """

    def store(self, stock_data, ticker_symbol):
        """
        Stores processed stock data in the 'processed_data' table of the PostgreSQL database.

        Parameters:
        -----------
        stock_data : DataFrame
            A DataFrame containing processed stock data with columns 'Open', 'High', 'Low', 'Close', 'Volume',
            'Moving Average', 'Volatility', and 'Return'.
        ticker_symbol : str
            The stock ticker symbol associated with the data.

        Raises:
        -------
        Exception
            If any error occurs during the data storage process, the transaction is rolled back, and an error is logged.
        """
        conn = psycopg2.connect(**DB_PARAMS)
        try:
            with conn.cursor() as cur:
                for index, row in stock_data.iterrows():
                    # Format the index (date) to a string
                    date_str = index.strftime('%Y-%m-%d')  # Ensure correct date format
                    
                    # Extract each value from the row as a scalar
                    open_price = row['Open'].item()
                    high_price = row['High'].item()
                    low_price = row['Low'].item()
                    close_price = row['Close'].item()
                    volume = row['Volume'].item()
                    moving_average = row['Moving Average'].item()
                    volatility = row['Volatility'].item()
                    daily_returns = row['Return'].item()

                    # Execute the SQL insert statement
                    cur.execute("""
                        INSERT INTO processed_data (date, ticker_symbol, open_price, high_price, low_price, close_price, volume, moving_average, volatility, daily_returns)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (date, ticker_symbol) DO NOTHING
                    """, (date_str, ticker_symbol, open_price, high_price, low_price, close_price, volume, moving_average, volatility, daily_returns))
                
                conn.commit()
            logger.info(f"Stored data for {ticker_symbol} in the database.")
        except Exception as e:
            logger.error(f"Error storing data for {ticker_symbol}: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()


if __name__ == "__main__":
    # Create an instance of DataIngestor
    data_ingestor = DataIngestor()
    
    # Example ticker symbol for testing
    ticker_symbol = "AAPL"
    
    # Ingest data for the given ticker symbol
    stock_data = data_ingestor.ingest_data(ticker_symbol)

    # Instantiate the MissingValueHandler
    handler = MissingValueHandler()

    # Process the DataFrame to handle missing values
    processed_data = handler.handle(stock_data)

    # Instantiate the FeatureEngineer
    feature_engineering = FeatureEngineer()

    # Feature engineer the processed data and store it in stock_data variable
    stock_data = feature_engineering.engineer(processed_data)

    # Instantiate DataStorer and store data with ticker symbol
    store_data = DataStorer()
    store_data.store(stock_data, ticker_symbol)

