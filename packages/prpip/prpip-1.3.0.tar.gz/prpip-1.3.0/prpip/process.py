from .load_data import load_data, validate_pupil_data
from .blink_detection import detect_blinks
from .reconstruction import reconstruct_pupil
import pandas as pd

def process_pupil(input_data, blink_threshold=1000, tau_base=50, noise_scale=0.05):
    """
    Comprehensive pupil data processing pipeline.
    
    Args:
        input_data (str or pd.DataFrame): File path or DataFrame of pupil data.
        blink_threshold (int): Threshold for detecting blinks.
        tau_base (float): Base recovery time constant.
        noise_scale (float): Scale of noise for recovery.
    
    Returns:
        pd.DataFrame: Processed data with reconstructed pupil size.
    """
    try:
        # Check if input is a file path or a DataFrame
        if isinstance(input_data, str):
            # Load data from file
            raw_data = load_data(input_data)
        elif isinstance(input_data, pd.DataFrame):
            # Use provided DataFrame directly
            raw_data = input_data
        else:
            raise ValueError("Input must be a file path or a pandas DataFrame.")
        
        # Validate and prepare data
        processed_data = validate_pupil_data(raw_data)
        
        # Detect blinks
        blink_intervals = detect_blinks(processed_data, blink_threshold)
        
        # Reconstruct pupil size
        processed_data['Reconstructed Pupil Size'] = reconstruct_pupil(
            processed_data, 
            blink_intervals, 
            tau_base, 
            noise_scale
        )
        
        return processed_data
    
    except Exception as e:
        print(f"Error processing pupil data: {e}")
        raise
