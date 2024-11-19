import sys
sys.path.append('/Users/mdayanarshad/Desktop/Data_Science_Projects/HFT_RealTime_DataPipeline')

# Correct imports for the decorators
from zenml import pipeline
from zenml.steps import step
from steps.ingest_data_step import ingest_data_step
from steps.handle_missing_value_step import handle_missing_value_step
from steps.feature_engineering_step import feature_engineering_step
from steps.storing_preprocessed_data_step import storing_preprocessed_data_step

@pipeline
def run_pipeline():
    ticker_symbol = "AAPL"
    stock_data = ingest_data_step(ticker_symbol=ticker_symbol)
    stock_data = handle_missing_value_step(stock_data)
    stock_data = feature_engineering_step(stock_data)
    storing_preprocessed_data_step(stock_data, ticker_symbol)

if __name__ == "__main__":
    run_pipeline()
