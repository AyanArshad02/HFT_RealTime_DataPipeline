import pandas as pd
from zenml import step
from src.handle_missing_value import MissingValueHandler

@step
def handle_missing_value_step(stock_data: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values in the given stock data using the MissingValueHandler class.

    Parameters:
        stock_data (pd.DataFrame): A pandas DataFrame containing stock data.

    Returns:
        pd.DataFrame: A pandas DataFrame with missing values handled.
    """
    handler = MissingValueHandler()
    return handler.handle(stock_data)

# handle_missing_value_step = step()(handle_missing_value_step)