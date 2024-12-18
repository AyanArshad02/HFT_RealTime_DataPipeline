import pandas as pd
from zenml import step
from src.feature_engineering import FeatureEngineer

@step
def feature_engineering_step(stock_data: pd.DataFrame) -> pd.DataFrame:
    """
    Performs feature engineering on the provided stock data using the FeatureEngineer class.

    Parameters:
        stock_data (pd.DataFrame): A pandas DataFrame containing the stock data to process.

    Returns:
        pd.DataFrame: A pandas DataFrame with engineered features added or modified.
    """
    engineer = FeatureEngineer()
    return engineer.engineer(stock_data)

# feature_engineering_step = step()(feature_engineering_step)