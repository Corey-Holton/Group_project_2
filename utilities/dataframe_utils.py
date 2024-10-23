import pandas as pd
from pathlib import Path

from zipfile import ZipFile, ZIP_DEFLATED # ZIP file operations / Used for saving DataFrames to ZIP files
import io # String IO buffer / Used for in-memory file operations
import bz2 # BZIP2 compression / Used for compressing the CSV data

# Import in-house utilities
from utilities.print_utils import print_title, print_label

# Function to save the DataFrames to ZIP files
def save_data(df, file_path):
    """ 
    Save a DataFrame to a ZIP file with a CSV file inside using BZIP2 compression.

    Parameters:
    - df: DataFrame to save
    - file_path: Path to save the zip file
    """

    # Ensure the file path is a Path object and set the suffix to .zip
    file_path = Path(file_path).with_suffix('.zip')
    
    # Check if the parent directory exists
    if not file_path.parent.exists():
        print_title(f"Error: The directory `{file_path.parent}` does not exist.", "bright_red", "red")
        return
    
    # Check if the zip file already exists and remove it if it does
    if file_path.exists():
        print_title(f"File `{file_path.name}` already exists. Overwriting file.", "bright_magenta", "magenta")
        file_path.unlink()
    
    # Save the DataFrame to a CSV file inside the zip file using BZIP2 compression
    with ZipFile(file_path, 'w', compression=ZIP_DEFLATED) as zipf:
        # Create a buffer to hold the CSV data
        csv_buffer = io.StringIO()
        
        # Write the DataFrame to the buffer as CSV
        df.to_csv(csv_buffer, index=False)

        # Compress the CSV data using BZ2
        compressed_data = bz2.compress(csv_buffer.getvalue().encode('utf-8'))
        
        # Write the compressed CSV data to the zip file
        zipf.writestr(file_path.stem + '.csv.bz2', compressed_data)
    
    # Print a success message
    print_title(f"File saved and zipped as `{file_path.name}`", "bright_green", "green")

# Function to load the DataFrames from ZIP files
def load_data(zip_file_path):
    """
    Load a DataFrame from a CSV file inside a zip file.

    Parameters:
    - zip_file_path: Path to the zip file containing the CSV

    Returns:
    - DataFrame loaded from the CSV file
    """
    
    # Ensure the file path is a Path object and set the suffix to .zip
    zip_file_path = Path(zip_file_path).with_suffix('.zip')
    
    # Check if the zip file exists
    if not zip_file_path.exists():
        print_title(f"Error: The file `{zip_file_path}` does not exist.", "bright_red", "red")
        return None
    
    # Open the zip file and read the CSV file inside it using BZIP2 compression
    with ZipFile(zip_file_path, 'r') as zipf:
        
        # Get the name of the CSV file inside the zip
        csv_file_name = zipf.namelist()[0]
        with zipf.open(csv_file_name) as csv_file:

            # Load the CSV file into a DataFrame
            df = pd.read_csv(csv_file)
    
    # Print a success message
    print_title(f"File `{csv_file_name}` loaded from `{zip_file_path.name}`", "bright_cyan", "cyan")
    
    return df

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

