def extract_instantaneous_phase(signal, frequency_band):
    """
    Extracts the instantaneous phase from a time-series signal using the Hilbert transform.
    
    Parameters:
    - signal: A 1D array-like structure containing the time-series data.
    - frequency_band: A tuple specifying the low and high cutoff frequencies for bandpass filtering.
    
    Returns:
    - instantaneous_phase: A 1D array containing the instantaneous phase of the signal.
    """
    from scipy.signal import hilbert, butter, filtfilt
    import numpy as np

    # Bandpass filter the signal
    lowcut, highcut = frequency_band
    fs = 1  # Assuming the signal is sampled at 1 Hz for simplicity
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(1, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)

    # Compute the analytic signal
    analytic_signal = hilbert(filtered_signal)

    # Extract the instantaneous phase
    instantaneous_phase = np.angle(analytic_signal)

    return instantaneous_phase