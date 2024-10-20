import pandas as pd
from pathlib import Path
from utilities.print_utils import print_title

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