import numpy as np
import pandas as pd
from bokeh.plotting import figure
from scipy.signal import argrelextrema

def norm(y, x = None, num: int = None):
    '''
    This function normalizes an array `y` to either of the following: the `y` array's maximum value, or
    optionally, to a specific value `num` in the `x` array.
    
    Args:
    -
        `y` the array of values that will be normalized.
    
        `x` the array of values that is used in normalizing the `y` array with the value `num`.
        
        `num` the value that the `y` array is normalized to along the `x` array.
    '''
    if num is None:
        y = y / max(y)
        return y
    else:
        i = 0 # Normalize to N nm
        # sheldon: <, fout: >
        while x[i] < num and i < len(x): i += 1
        y = y / y[i]
        return y, i
    
def fwhm(pl_wave: pd.core.series.Series, pl_int: pd.core.series.Series):

    pl_norm_inten = pl_int / np.max(pl_int)
    x_eV = 1239.84 / pl_wave
    y_eV = pl_int * (1239.84/pl_wave)**2

    #Identify peak
    max_idx = y_eV.argmax(axis=0)
    half_max_int = (y_eV[max_idx] / 2) + 1000

    hf_mx_int = pl_norm_inten[max_idx] / 2

    # Identifying the lower and upper indexes for the PL peak
    min_idx = max_idx
    while y_eV[min_idx] > half_max_int: min_idx -=1
    while y_eV[max_idx] > half_max_int: max_idx += 1

    # Full Width at Half Max value
    fwhm = (x_eV[min_idx] - x_eV[max_idx]) * 1000

    # Visual Plost of the FWHM
    hm_x = np.linspace(pl_wave[min_idx],pl_wave[max_idx],100)
    hm_y = np.linspace(hf_mx_int,hf_mx_int,100)

    # p = figure(title=str('title'),
    #     sizing_mode='stretch_both',
    #     x_axis_label=str('x_label'), 
    #     y_axis_label=str('y_label'),
    #     active_scroll="wheel_zoom")

    return hm_x, hm_y, fwhm

def localMaxima(series, nth:int =1):
    x = np.array(series)

    local_maxima_indices = argrelextrema(x, np.greater)[0]
    local_maxima_values = x[local_maxima_indices]

    if len(local_maxima_indices) < nth:
        print(f"There are not enough local maxima in the series to retrieve the {nth}th highest local maximum.")
        return None

    # Sort local maxima values in descending order
    sorted_maxima_indices = np.argsort(local_maxima_values)[::-1]
    sorted_maxima_values = local_maxima_values[sorted_maxima_indices]

    # Select the nth highest peak
    nth_max_idx = local_maxima_indices[sorted_maxima_indices[nth - 1]]
    nth_max_val = sorted_maxima_values[nth - 1]

    return nth_max_idx, nth_max_val

