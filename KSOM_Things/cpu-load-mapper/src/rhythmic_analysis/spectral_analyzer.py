def compute_spectral_features(signal, window_size):
    import numpy as np
    from scipy.signal import stft

    # Compute the Short-Time Fourier Transform (STFT)
    f, t, Zxx = stft(signal, nperseg=window_size)

    # Calculate the spectral features
    spectral_centroid = np.sum(f * np.abs(Zxx), axis=0) / np.sum(np.abs(Zxx), axis=0)
    spectral_bandwidth = np.sqrt(np.sum((f - spectral_centroid[:, None])**2 * np.abs(Zxx), axis=0) / np.sum(np.abs(Zxx), axis=0))

    # Return the computed features
    return {
        'frequencies': f,
        'times': t,
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth
    }