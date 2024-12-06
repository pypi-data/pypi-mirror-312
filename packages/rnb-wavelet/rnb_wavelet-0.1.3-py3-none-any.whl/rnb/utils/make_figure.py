from matplotlib.ticker import ScalarFormatter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

#matplotlib.use('TkAgg')

def plot_fft(fr, po,log_scale='none', ax=None ):
    """
    Plots average power

    Parameters:
    ----------
    fr : Frequecies (1D array)
    po : Average power (1D array)
    log_scale : Option to plot on a logarithmic scale. 
        Accepted values are 'none' (default), 'logx', 'logy', or 'loglog'.
    ax : Matplotlib Axes object to plot on. 
    """
    colR = [161/256, 22/256, 50/256]

    # Ensure 1D array
    po = po.flatten() 
    fr = fr.flatten() 

    if ax is None:
        fig, ax = plt.subplots()
    
    if log_scale == 'logx':
        ax.set_xscale('log', base=2)
    elif log_scale == 'logy':
        ax.set_yscale('log', base=2)
    elif log_scale == 'loglog':
        ax.set_xscale('log', base=2)
        ax.set_yscale('log', base=2)
 
    # Format major ticks
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ScalarFormatter())

    # Set up parameters and filter data
    param_frange = [0.5, 45]
    frange = np.where((fr >= param_frange[0]) & (fr <= param_frange[1]))
    ax.plot(fr[frange], po[frange], color=colR,)

    # Set log axis
    if log_scale in ['logx', 'loglog']:
        xtick_locs = [1, 2, 4, 8, 16, 32, 64]
        xtick_labels = ['1', '2', '4', '8', '16', '32', '64']
        ax.set_xticks(xtick_locs)
        ax.set_xticklabels(xtick_labels)

    # labels 
    ax.set_xlabel(r'Frequency (Hz)', fontsize=14) 
    ax.set_ylabel(r'Rhythmic Power Spectral Density (dB)', fontsize=14)


def plot_beta(betas,ax=None):
    """
    Plots spectral exponent distribution across epochs

    Parameters:
    ----------
    betas : Array of beta values to plot.
    ax : Matplotlib Axes object to plot on. 
    """
    colR = [161/256, 22/256, 50/256]

    if ax is None:
        fig, ax = plt.subplots()

    # histogram
    a, b = np.histogram(betas, bins=60)
    bin_width = b[1] - b[0] 
    p = a / np.sum(a) / bin_width

    # Plot normalized histogram
    ax.set_facecolor('none') 
    ax.plot(b[:-1], p, '.') 

    # plot smoothed histogram
    smoothed_p = savgol_filter(p, 10, 2)  
    ax.plot(b[:-1], smoothed_p, '-', color=colR, linewidth=1.35)

    # axis limits 
    ax.axvline(x=2, ymin=0, ymax=3.5/ax.get_ylim()[1], color='black', linestyle='--', linewidth=1.35)
    ax.set_xlim(0, 3)

    # labels 
    ax.set_xlabel(r'Spectral exponent ($\beta$)', fontsize=14)


