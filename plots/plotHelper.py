from scipy.signal import argrelextrema
import pandas as pd
import numpy as np

palette15 = {
    3: ('#FF8A80', '#FFD180', '#CCFF90'),
    4: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF'),
    5: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB'),
    6: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC'),
    7: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740'),
    8: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40'),
    9: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5'),
    10: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081'),
    11: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59'),
    12: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF'),
    13: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF', '#FFAB40'),
    14: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF', '#FFAB40', '#607D8B'),
    15: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF', '#FFAB40', '#607D8B', '#FFD180'),
}

palette22 = {
    2: ('#aec7e8', '#ff7f0e'),
    3: ('#aec7e8', '#ff7f0e', '#ffbb78'),
    4: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c'),
    5: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a'),
    6: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728'),
    7: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896'),
    8: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd'),
    9: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5'),
    10: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b'),
    11: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94'),
    12: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2'),
    13: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'),
    14: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f'),
    15: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7'),
    16: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22'),
    17: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d'),
    18: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf'),
    19: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5'),
    20: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363'),
    21: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7'),
    22: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7', '#bcbd22')
}

palette23 = {
    3: ('#1f77b4', '#aec7e8', '#ff7f0e'),
    4: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78'),
    5: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c'),
    6: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a'),
    7: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728'),
    8: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896'),
    9: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd'),
    10: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5'),
    11: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b'),
    12: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94'),
    13: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2'),
    14: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'),
    15: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f'),
    16: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7'),
    17: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22'),
    18: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d'),
    19: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf'),
    20: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5'),
    21: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363'),
    22: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7'),
    23: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7', '#bcbd22')
}

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
    
def fwhm(pl_wave, pl_int):

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

def plotColors(pallete: dict, file_length: int) -> list[str]:
    if file_length in [1, 2]:
        color = pallete[3]
        if file_length == 1:
            color = color[:-2]
            return color
        else:
            color = color[:-1]
            return color
    else:
        color = pallete[file_length]
        return color

def themePicker(theme: str):
    theme_name = 'static/files/bokehThemes/' + theme + '_theme.json'
    return theme_name
