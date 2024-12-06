import numpy as np
from .validation import validate_input_data

def reconstruct_pupil(trial_data, blink_intervals, tau_base=50, noise_scale=0.05):
    """
    Reconstruct pupil size with improved error handling and logging.
    """
    validate_input_data(trial_data)
    
    # Ensure the Pupil Size column is float
    trial_data['Pupil Size'] = trial_data['Pupil Size'].astype(float)
    interpolated_pupil = trial_data['Pupil Size'].copy()
    
    for start, end in blink_intervals:
        if start >= end or end > len(trial_data):
            print(f"Invalid blink interval: {start}-{end}")
            continue
        
        blink_length = end - start
        
        # Robust pre and post value selection
        pre_value = interpolated_pupil.iloc[max(0, start - 1)] if start > 0 else interpolated_pupil.mean()
        post_value = interpolated_pupil.iloc[min(end, len(interpolated_pupil) - 1)] if end < len(interpolated_pupil) else interpolated_pupil.mean()
        
        # Dynamic tau adjustment
        tau = tau_base + blink_length / 10
        
        # Recovery curve generation with error handling
        try:
            t = np.arange(0, blink_length)
            recovery_curve = pre_value + (post_value - pre_value) * (1 - np.exp(-t / tau))
            
            # Noise generation
            noise = np.random.normal(0, noise_scale * abs(post_value - pre_value), blink_length)
            recovery_curve += noise
            
            # Cast recovery_curve to float explicitly to match the dtype
            interpolated_pupil.iloc[start:end] = recovery_curve.astype(interpolated_pupil.dtype)
        except Exception as e:
            print(f"Error reconstructing blink interval {start}-{end}: {e}")
    
    # Robust interpolation
    interpolated_pupil = interpolated_pupil.interpolate(method='linear', limit_direction='both')
    
    return interpolated_pupil