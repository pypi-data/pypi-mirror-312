import numpy as np
import pandas as pd

def validate_input_data(trial_data):
    """
    Validate input data for pupil size processing.
    
    Args:
        trial_data (pd.DataFrame): Input data containing 'Pupil Size' column
    
    Raises:
        ValueError: If input data is invalid
    """
    if not isinstance(trial_data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    if 'Pupil Size' not in trial_data.columns:
        raise ValueError("DataFrame must contain 'Pupil Size' column")
    
    if trial_data['Pupil Size'].empty:
        raise ValueError("Pupil Size data cannot be empty")
    
    if not np.issubdtype(trial_data['Pupil Size'].dtype, np.number):
        raise ValueError("Pupil Size must contain numeric data")