import sys
sys.path.append('/Users/mdayanarshad/Desktop/Data_Science_Projects/HFT_RealTime_DataPipeline')


from zenml.pipelines import pipeline
from zenml.steps import step
from steps import ingest_data_step, handle_missing_value_step, feature_engineering_step, storing_preprocessed_data_step

ticker_symbol = "AAPL"

@pipeline
def run_pipeline():
    stock_data = ingest_data_step(ticker_symbol="AAPL")
    stock_data = handle_missing_value_step(stock_data)
    stock_data = feature_engineering_step(stock_data)
    storing_preprocessed_data_step(stock_data, ticker_symbol)

# run_pipeline = pipeline()(run_pipeline)

if __name__ == "__main__":
    run_pipeline()
