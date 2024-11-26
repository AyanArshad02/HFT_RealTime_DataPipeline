import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from src.fetch_data import (
    MaxPeriodFetchingStrategy,
    HistoricalFetchingStrategy,
    StockDataFetcher,
)

class TestDataFetchingStrategies(unittest.TestCase):
    
    @patch('yfinance.download')
    def test_max_period_fetching_strategy(self, mock_yfinance_download):
        # Simulate yfinance data
        mock_data = pd.DataFrame({'Close': [150, 151, 152]})
        mock_yfinance_download.return_value = mock_data
        
        strategy = MaxPeriodFetchingStrategy()
        data = strategy.fetch("AAPL")
        
        mock_yfinance_download.assert_called_once_with("AAPL", period='max')
        pd.testing.assert_frame_equal(data, mock_data)
    
    @patch('yfinance.download')
    def test_historical_fetching_strategy(self, mock_yfinance_download):
        # Simulate yfinance data
        mock_data = pd.DataFrame({'Close': [153, 154, 155]})
        mock_yfinance_download.return_value = mock_data
        
        strategy = HistoricalFetchingStrategy()
        data = strategy.fetch("AAPL", "2023-01-01")
        
        mock_yfinance_download.assert_called_once_with("AAPL", start="2023-01-01")
        pd.testing.assert_frame_equal(data, mock_data)

class TestStockDataFetcher(unittest.TestCase):
    
    @patch('psycopg2.connect')
    def test_get_last_date_from_db(self, mock_connect):
        # Mocking the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (datetime(2023, 1, 1),)
        
        mock_connect.return_value = mock_conn
        
        fetcher = StockDataFetcher("AAPL")
        last_date = fetcher.get_last_date_from_db()
        
        self.assertEqual(last_date, datetime(2023, 1, 1))
        mock_cursor.execute.assert_called_once_with(
            "SELECT MAX(date) FROM processed_data WHERE ticker_symbol = %s", ("AAPL",)
        )
    
    @patch('src.fetch_data.MaxPeriodFetchingStrategy.fetch')
    @patch('src.fetch_data.HistoricalFetchingStrategy.fetch')
    @patch('psycopg2.connect')
    def test_fetch_data_with_last_date(self, mock_connect, mock_hist_fetch, mock_max_fetch):
        # Mocking database to return a last date
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (datetime(2023, 1, 1),)
        mock_connect.return_value = mock_conn
        
        # Mocking data fetching strategies
        mock_hist_data = pd.DataFrame({'Close': [156, 157, 158]})
        mock_hist_fetch.return_value = mock_hist_data
        
        fetcher = StockDataFetcher("AAPL")
        data = fetcher.fetch_data()
        
        self.assertIsNotNone(data)
        pd.testing.assert_frame_equal(data, mock_hist_data)
        mock_hist_fetch.assert_called_once_with("AAPL", datetime(2023, 1, 2))
    
    @patch('src.fetch_data.MaxPeriodFetchingStrategy.fetch')
    @patch('psycopg2.connect')
    def test_fetch_data_without_last_date(self, mock_connect, mock_max_fetch):
        # Mocking database to return no last date
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        
        # Mocking data fetching strategy
        mock_max_data = pd.DataFrame({'Close': [150, 151, 152]})
        mock_max_fetch.return_value = mock_max_data
        
        fetcher = StockDataFetcher("AAPL")
        data = fetcher.fetch_data()
        
        self.assertIsNotNone(data)
        pd.testing.assert_frame_equal(data, mock_max_data)
        mock_max_fetch.assert_called_once_with("AAPL")

if __name__ == "__main__":
    unittest.main()
