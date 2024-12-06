from rnb.utils.tools import compute_spectrum
from rnb.utils.make_figure import plot_fft, plot_beta

import matplotlib.pyplot as plt

def display_rhythmic_analysis(signal, spectral_exponent,fs,  log_scale='logx'):
    """
    Wrapper function to display the rhythmic spectrum and spectral exponent distribution .

    Parameters:
    ----------
    signal : Input signal
    fs : Sampling frequency
    spectral_exponent : Spectral exponent across signal  
    log_scale : Scale for the FFT plot (default: 'logx').
    """
    fr, F = compute_spectrum(signal, fs)

    fig, axes = plt.subplots(1, 2, figsize=(12,5))
    
    plot_fft(fr, F, log_scale=log_scale, ax=axes[0])
    
    plot_beta(spectral_exponent, ax=axes[1])
    
    plt.show()
