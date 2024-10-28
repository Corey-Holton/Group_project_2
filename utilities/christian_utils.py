import pandas as pd
from .print_utils import print_title, print_label

def split_dataset_by_date(raw_data: pd.DataFrame, todays_date: str) -> tuple:
    """
    Split the dataset into historical data and today's data based on the given date.

    Parameters:
    raw_data (pd.DataFrame): The raw data containing a 'Date' column.
    todays_date (str): The date to filter today's data.

    Returns:
    tuple: A tuple containing the historical data and today's data.
    """
    # Filter data by today's date
    filter_data_by_date = raw_data["Date"] == todays_date
    
    # Create a new dataframe with today's data
    todays_data = raw_data[filter_data_by_date].reset_index(drop=True)
    
    # Create a new dataframe with historical data (excluding today's data)
    historical_data = raw_data[~filter_data_by_date].reset_index(drop=True)
    
    return historical_data, todays_data

def clean_historical_data(historical_data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the historical data by removing rows with specific conditions and backfilling missing values.

    Parameters:
    historical_data (pd.DataFrame): The historical data to be cleaned.

    Returns:
    pd.DataFrame: The cleaned historical data.
    """
    # Remove all rows where `Adjusted Close` is 0
    historical_data = historical_data[historical_data["Adjusted Close"] != 0].reset_index(drop=True)
    
    # Remove all rows where `Volatility` is NaN
    historical_data = historical_data.dropna(subset=["Volatility"]).reset_index(drop=True)
    
    # Backfill the `RSI` column
    historical_data["RSI"] = historical_data["RSI"].bfill()
    
    # Backfill the `Action` column
    historical_data["Action"] = historical_data["Action"].bfill()
    
    return historical_data

def check_tickers_for_missing_values(historical_data: pd.DataFrame) -> tuple:
    """
    Check tickers for missing values and print relevant information.

    Parameters:
    historical_data (pd.DataFrame): The historical data containing tickers and other columns.

    Returns:
    tuple: A tuple containing arrays of tickers with no missing values and tickers with missing values.
    """
    # Print tickers that do not have any missing values
    print_title("Tickers that do not have any missing values", closed_corners=False)

    num_tickers = len(historical_data["Ticker"].unique())
    print_label("Number of unique tickers:", num_tickers)

    # Group by ticker and check for missing values within each group
    grouped = historical_data.groupby("Ticker")

    # Tickers with no missing values
    tickers_no_missing_values = grouped.filter(lambda x: not x.isnull().any().any())["Ticker"].unique()
    print_label("Number of tickers with no missing values:", len(tickers_no_missing_values))

    # Tickers with missing values
    tickers_missing_values = grouped.filter(lambda x: x.isnull().any().any())["Ticker"].unique()
    print_label("Number of tickers with missing values:", len(tickers_missing_values), closed_corners=True)

    return tickers_no_missing_values, tickers_missing_values