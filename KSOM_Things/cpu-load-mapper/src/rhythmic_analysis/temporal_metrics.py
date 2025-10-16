def calculate_temporal_variability(signal):
    """
    Calculate the temporal variability of a given signal.
    
    Parameters:
    signal (list or np.array): The input time series signal.
    
    Returns:
    float: A measure of the variability in the signal.
    """
    import numpy as np

    # Calculate the differences between consecutive points
    differences = np.diff(signal)

    # Calculate the normalized rate of change
    rate_of_change = np.abs(differences) / (np.abs(signal[:-1]) + 1e-10)  # Avoid division by zero

    # Calculate the temporal variability as the mean of the rate of change
    temporal_variability = np.mean(rate_of_change)

    return temporal_variability