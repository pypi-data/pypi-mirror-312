import pandas as pd

def load_csv_files(file_paths):
    """
    Load multiple CSV files into a dictionary of DataFrames.

    Args:
        file_paths (dict): Dictionary with keys as identifiers and values as file paths.

    Returns:
        dict: Dictionary of DataFrames.
    """
    dataframes = {}
    for key, path in file_paths.items():
        df = pd.read_csv(path)
        dataframes[key] = df
    return dataframes