from zenml.pipelines import pipeline
from steps import ingest_data_step, handle_missing_value_step, feature_engineering_step, storing_preprocessed_data_step

@pipeline
def run_pipeline(ticker_symbol: str):
    stock_data = ingest_data_step(ticker_symbol=ticker_symbol)
    stock_data = handle_missing_value_step(stock_data)
    stock_data = feature_engineering_step(stock_data)
    storing_preprocessed_data_step(stock_data, ticker_symbol)
