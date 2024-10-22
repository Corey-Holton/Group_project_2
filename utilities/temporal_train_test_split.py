import pandas as pd
from datetime import datetime

def temporal_train_test_split(df, date_column, cutoff_date):
  """
  Split a dataset into training and testing sets based on a cutoff date.
  
  Parameters:
  -----------
  df : pandas.DataFrame
    The input DataFrame containing the time-series data
  date_column : str
    Name of the column containing datetime information
  cutoff_date : str or datetime
    The cutoff date. Data before this date goes to train, after to test.
  
  Returns:
  --------
  train_df : pandas.DataFrame
    Training dataset (data before cutoff_date)
  test_df : pandas.DataFrame
    Testing dataset (data from cutoff_date onwards)
      
  Raises:
  -------
  ValueError:
    If date_column cannot be converted to datetime
    If no data is found before or after the cutoff date
  """

  df = df.copy()
  
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
  
  # Split the data based on cutoff date
  train_df = df[df[date_column] < cutoff_date].copy()
  test_df = df[df[date_column] >= cutoff_date].copy()
  
  if len(train_df) == 0:
    raise ValueError("No training data found before the cutoff date")
  if len(test_df) == 0:
    raise ValueError("No test data found after the cutoff date")
  
  return train_df, test_df

if __name__ == "__main__":
  valid_df = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'value': range(100)
  })
  
  train_df, test_df = temporal_train_test_split(
    valid_df,
    date_column='date',
    cutoff_date='2023-03-15'
  )
  
  print(f"Train set shape: {train_df.shape}")
  print(f"Test set shape: {test_df.shape}")
  print(f"\nTrain date range: {train_df['date'].min()} to {train_df['date'].max()}")
  print(f"Test date range: {test_df['date'].min()} to {test_df['date'].max()}")
  
  invalid_df = pd.DataFrame({
    'date': ['not a date', 'also not a date'],
    'value': [1, 2]
  })
  
  try:
    temporal_train_test_split(invalid_df, 'date', '2023-03-15')
  except ValueError as e:
    print(f"\nExpected error with invalid dates: {str(e)}")