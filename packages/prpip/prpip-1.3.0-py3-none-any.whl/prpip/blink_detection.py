from .validation import validate_input_data

def detect_blinks(trial_data, blink_threshold=1000):
    """
    Detect blink intervals with enhanced error handling.
    """
    validate_input_data(trial_data)
    
    blink_intervals = []
    in_blink = False
    start_idx = None
    
    for idx, pupil_size in trial_data['Pupil Size'].items():
        try:
            if pupil_size <= blink_threshold and not in_blink:
                in_blink = True
                start_idx = idx
            elif pupil_size > blink_threshold and in_blink:
                in_blink = False
                end_idx = idx
                blink_intervals.append((start_idx, end_idx))
        except Exception as e:
            print(f"Error processing index {idx}: {e}")
    
    if in_blink and start_idx is not None:
        blink_intervals.append((start_idx, len(trial_data) - 1))
    
    return blink_intervals