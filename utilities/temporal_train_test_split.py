import pandas as pd
from datetime import datetime

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Import in-house utilities
if current_dir in sys.path:
    # If current directory is in sys.path, use relative import
    from print_utils import print_title, print_label
    from dataframe_utils import load_data
else:
    # Otherwise, use absolute import
    from utilities.print_utils import print_title, print_label
    from utilities.dataframe_utils import load_data

def temporal_train_test_split(df, date_column, target_column, cutoff_date, feature_columns=None):
  """
  Split a dataset into training and testing sets based on a cutoff date,
  separating features (X) and target (y).
  
  Parameters:
  -----------
  df : pandas.DataFrame
    The input DataFrame containing the time-series data
  date_column : str
    Name of the column containing datetime information
  target_column : str
    Name of the column containing the target variable
  cutoff_date : str or datetime
    The cutoff date. Data before this date goes to train, after to test.
  feature_columns : list of str, optional
    Specific columns to use as features. If None, all columns except
    date_column and target_column will be used.

  Returns:
  --------
  X_train : pandas.DataFrame
    Training features
  X_test : pandas.DataFrame
    Testing features
  y_train : pandas.Series
    Training target values
  y_test : pandas.Series
    Testing target values
      
  Raises:
  -------
  ValueError:
    If date_column cannot be converted to datetime
    If no data is found before or after the cutoff date
    If target_column is not in the DataFrame
  """
  df = df.copy()
  
  if target_column not in df.columns:
    raise ValueError(f"Target column '{target_column}' not found in DataFrame")
  
  if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
    try:
      df[date_column] = pd.to_datetime(df[date_column])
    except (ValueError, TypeError) as e:
      raise ValueError(f"Could not convert '{date_column}' to datetime. Please ensure the column contains valid dates.") from e
  
  if isinstance(cutoff_date, str):
    try:
      cutoff_date = pd.to_datetime(cutoff_date)
    except (ValueError, TypeError) as e:
      raise ValueError(f"Invalid cutoff_date format. Please provide a valid date string or datetime object.") from e
  
  df = df.sort_values(by=date_column)
  
  if feature_columns is None:
    feature_columns = [col for col in df.columns 
                      if col not in [date_column, target_column]]
  else:
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
      raise ValueError(f"Feature columns {missing_cols} not found in DataFrame")
  
  # Split data based on cutoff date
  train_mask = df[date_column] < cutoff_date
  test_mask = df[date_column] >= cutoff_date
  
  # Create X and y splits
  X_train = df.loc[train_mask, feature_columns].copy()
  X_test = df.loc[test_mask, feature_columns].copy()
  y_train = df.loc[train_mask, target_column].copy()
  y_test = df.loc[test_mask, target_column].copy()
  
  if len(X_train) == 0:
    raise ValueError("No training data found before the cutoff date")
  if len(X_test) == 0:
    raise ValueError("No test data found after the cutoff date")
  
  return X_train, X_test, y_train, y_test

if __name__ == "__main__":
  valid_df = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'feature1': range(100),
    'feature2': range(100, 200),
    'target': range(200, 300)
  })
  
  test_cases = [
    {
      "case": "Real Data",
      "date_column": 'Date',
      "target_column": 'Return',
      "cutoff_date": '2023-01-01',
      "feature_columns": None,
      "df": load_data("data/raw_data/sp500_adj_close_raw")
    },
    {
      "case": "Valid Sample Data",
      "date_column": 'date',
      "target_column": 'target',
      "cutoff_date": '2023-01-02',
      "feature_columns": None,
      "df": valid_df
    },
    {
      "case": "Feature Columns",
      "date_column": 'date',
      "target_column": 'target',
      "cutoff_date": '2023-03-02',
      "feature_columns": ["feature1"],
      "df": valid_df
    },
    {
      "case": "Invalid Dates",
      "date_column": 'date',
      "target_column": 'target',
      "cutoff_date": '2023-03-15',
      "feature_columns": None,
      "df": pd.DataFrame({
        'date': ['not a date', 'also not a date'],
        'feature1': [1, 2],
        'target': [3, 4]
      })
    }
  ]

  for test_case in test_cases:
    print_title(f"Test Case: {test_case['case']}")
    try:
      X_train, X_test, y_train, y_test = temporal_train_test_split(
        test_case['df'],
        test_case['date_column'],
        test_case['target_column'],
        test_case['cutoff_date'],
        feature_columns=test_case['feature_columns']
      )
      
      # Convert shape tuples to strings before printing
      print_label("X_train Shape", f"{X_train.shape[0]} rows, {X_train.shape[1]} columns")
      print_label("X_test Shape", f"{X_test.shape[0]} rows, {X_test.shape[1]} columns")
      print_label("y_train Shape", f"{y_train.shape[0]} rows")
      print_label("y_test Shape", f"{y_test.shape[0]} rows")
    except Exception as e:
      if test_case['case'] == "Invalid Dates":
        print_title("Expected Error:", "bright_green", "green")
        print_label("Error Message", str(e))
      else:
        raise e
    print()