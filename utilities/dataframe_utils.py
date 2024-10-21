import pandas as pd
from pathlib import Path
from datetime import datetime
from utilities.print_utils import print_title, print_label, print_footer

# Function to save the DataFrames to CSV files
def save_data(df, file_path):
    """ 
    Save a DataFrame to a CSV file at the specified file path.

    Parameters:
    - df: DataFrame to save
    - file_path: Path to save the CSV file
    """

    # Ensure the file path is a Path object
    file_path = Path(file_path)
    
    # Check if the parent directory exists
    if not file_path.parent.exists():
        print_title(f"Error: The directory `{file_path.parent}` does not exist.", "bright_red", "red")
        return
    
    if file_path.exists():
        print_title(f"File `{file_path.name}` already exists. Overwriting file.", "bright_magenta", "magenta")
        file_path.unlink()
    
    # Save the DataFrame to the specified file path
    df.to_csv(file_path, index=False)
    print_title(f"File saved as `{file_path.name}`", "bright_green", "green")

def print_dataframe_report(df, df_name):
    """ 
    Print a summary report for the DataFrame.

    Parameters:
    - df: DataFrame to summarize
    - df_name: Name of the DataFrame
    """
    BORDER_COLOR = "blue"
    TEXT_COLOR = "bright_blue"

    print_title(f"`{df_name.capitalize()}` DataFrame Report", TEXT_COLOR, BORDER_COLOR, closed_corners=False)

    # First and Last Date (if index is a date)
    if pd.api.types.is_datetime64_any_dtype(df.index):
        index_range = f"{df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}"
        print_label("Index Range:", index_range, TEXT_COLOR, BORDER_COLOR)
    else:
        index_range = f"{df.index.min()} to {df.index.max()}"
        print_label("Index Range:", index_range, TEXT_COLOR, BORDER_COLOR)

    # Data Types
    print_label(f"`{df_name.capitalize()}` Data Types:", f"{df.dtypes.unique().tolist()}", TEXT_COLOR, BORDER_COLOR)

    # DataFrame Shape
    print_label(f"`{df_name.capitalize()}` DF Shape:", f"{df.shape}", TEXT_COLOR, BORDER_COLOR)

    # Columns with null values
    columns_with_nulls = df.columns[df.isnull().any()]
    print_label("Columns with null values:", f"{len(columns_with_nulls)}", TEXT_COLOR, BORDER_COLOR)

    # Rows with null values
    rows_with_nulls = df.index[df.isnull().any(axis=1)]
    print_label("Rows with null values:", f"{len(rows_with_nulls)}", TEXT_COLOR, BORDER_COLOR)

    # Number of Unique Values
    unique_values_count = df.nunique().sum()
    print_label("Total Unique Values:", f"{unique_values_count}", TEXT_COLOR, BORDER_COLOR, closed_corners=True)

