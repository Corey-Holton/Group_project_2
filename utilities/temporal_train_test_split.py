import pandas as pd
from datetime import datetime

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
  
  X_train, X_test, y_train, y_test = temporal_train_test_split(
    valid_df,
    date_column='date',
    target_column='target',
    cutoff_date='2023-03-15'
  )
  
  print(f"X_train shape: {X_train.shape}")
  print(f"X_test shape: {X_test.shape}")
  print(f"y_train shape: {y_train.shape}")
  print(f"y_test shape: {y_test.shape}")
  
  # Example usage with specific feature columns
  X_train, X_test, y_train, y_test = temporal_train_test_split(
    valid_df,
    date_column='date',
    target_column='target',
    cutoff_date='2023-03-15',
    feature_columns=['feature1']
  )
  
  print("\nWith specific feature selection:")
  print(f"X_train shape: {X_train.shape}")
  print(f"X_test shape: {X_test.shape}")
  
  invalid_df = pd.DataFrame({
    'date': ['not a date', 'also not a date'],
    'feature1': [1, 2],
    'target': [3, 4]
  })
  
  try:
    temporal_train_test_split(invalid_df, 'date', 'target', '2023-03-15')
  except ValueError as e:
    print(f"\nExpected error with invalid dates: {str(e)}")