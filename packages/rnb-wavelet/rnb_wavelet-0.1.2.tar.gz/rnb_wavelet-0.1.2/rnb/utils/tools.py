import numpy as np
import math


def compute_spectrum(data_epocs, fs):
    """
    Calculates the average spectral analysis 

    Parameters:
    ----------
    data_epocs: EEG Data (Nepocs X Nsample) 
    fs : Sampling frequency

    Returns:
    -------
    freq: Frequencies
    F: Average power
    """
    if data_epocs.ndim == 1:
        data_epocs = data_epocs[np.newaxis, :]
            
    n_epochs, n_time = data_epocs.shape

    # Frenquency 
    freq = fs / 2 * np.linspace(0, 1, n_time // 2 + 1)

    # Perform fft
    F = np.fft.fft(data_epocs) / n_time
    F = F[:, :n_time // 2 + 1]
    F = np.abs(F) ** 2

    # Delete null frequency
    F = F[:, 1:]
    freq = freq[1:] 

    # average across power across epochs
    if n_epochs > 1:
        F = np.mean(F, axis=0, keepdims=True)

    return freq, F

