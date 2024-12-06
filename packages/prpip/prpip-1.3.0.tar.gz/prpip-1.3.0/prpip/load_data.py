# load_data.py
import pandas as pd
import numpy as np
import os

def load_data(file_path):
    """
    Load data from various file formats.
    
    Supported formats: CSV, XLSX, XLS, TXT, JSON, PARQUET
    
    Args:
        file_path (str): Path to the data file
    
    Returns:
        pd.DataFrame: Loaded data
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif file_ext == '.txt':
            return pd.read_csv(file_path, delim_whitespace=True)
        elif file_ext == '.json':
            return pd.read_json(file_path)
        elif file_ext == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        raise

def validate_pupil_data(df):
    """
    Validate and prepare pupil size data.
    
    Args:
        df (pd.DataFrame): Input dataframe
    
    Returns:
        pd.DataFrame: Validated dataframe
    """
    if df is None or df.empty:
        raise ValueError("Empty dataset")
    
    pupil_columns = [col for col in df.columns if 'pupil' in col.lower()]
    
    if not pupil_columns:
        raise ValueError("No pupil size column found")
    
    pupil_col = pupil_columns[0]
    
    try:
        df[pupil_col] = pd.to_numeric(df[pupil_col], errors='coerce')
    except Exception as e:
        raise ValueError(f"Cannot convert pupil size to numeric: {e}")
    
    df = df.dropna(subset=[pupil_col])
    
    return df.rename(columns={pupil_col: 'Pupil Size'})