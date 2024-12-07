import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.fetch_data import StockDataFetcher
from src.ingest_data import DataIngestor

class TestDataIngestor(unittest.TestCase):

    @patch('src.ingest_data.StockDataFetcher.fetch_data')
    def test_ingest_data(self, mock_fetch_data):
        # Simulate fetched stock data
        mock_data = pd.DataFrame({'Close': [150, 151, 152]})
        mock_fetch_data.return_value = mock_data
        
        # Initialize DataIngestor
        data_ingestor = DataIngestor()
        
        # Call the method to ingest data
        ticker_symbol = "AAPL"
        result = data_ingestor.ingest_data(ticker_symbol)
        
        # Assertions
        self.assertIsNotNone(result)
        pd.testing.assert_frame_equal(result, mock_data)
        mock_fetch_data.assert_called_once()

    @patch('src.ingest_data.StockDataFetcher.fetch_data')
    def test_create_fetcher(self, mock_fetch_data):
        # Simulate fetched stock data
        mock_data = pd.DataFrame({'Close': [150, 151, 152]})
        mock_fetch_data.return_value = mock_data
        
        # Initialize DataIngestor
        data_ingestor = DataIngestor()
        
        # Test the create_fetcher method
        ticker_symbol = "AAPL"
        fetcher = data_ingestor.create_fetcher(ticker_symbol)
        
        # Assertions
        self.assertIsInstance(fetcher, StockDataFetcher)
        self.assertEqual(fetcher.ticker_symbol, ticker_symbol)

if __name__ == "__main__":
    unittest.main()
