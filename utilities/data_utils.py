import pandas as pd
from pathlib import Path
from utilities.print_utils import print_title

# Create a function to save the DataFrames to CSV files
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

# Create a function to load the DataFrames from CSV files
def load_data(file_path):
    """ 
    Load a DataFrame from a CSV file at the specified file path.

    Parameters:
    - file_path: Path to load the CSV file
    """

    # Ensure the file path is a Path object
    file_path = Path(file_path)
    
    # Check if the file exists
    if not file_path.exists():
        print_title(f"Error: File `{file_path.name}` does not exist.", "bright_red", "red")
        return None
    
    # Load the DataFrame from the specified file path
    df = pd.read_csv(file_path)
    print_title(f"File loaded: `{file_path.name}`", "bright_green", "green")
    return df