def filter_long_term_data(history_length_minutes, log_file):
    import pandas as pd
    from datetime import datetime, timedelta

    # Load the log data
    data = pd.read_csv(log_file)
    
    # Convert timestamp to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Calculate the cutoff time for the history length
    cutoff_time = datetime.now() - timedelta(minutes=history_length_minutes)
    
    # Filter the data for the specified history length
    filtered_data = data[data['timestamp'] >= cutoff_time]
    
    return filtered_data