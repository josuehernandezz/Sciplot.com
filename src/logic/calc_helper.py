from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CustomJS, Slider
from scipy.signal import argrelextrema
from scipy import integrate
import pandas as pd
import numpy as np

def norm(y, x = None, num: int = None, return_idx: bool =False):
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
        if return_idx == True:
            return y, i
        else:
            return y

def index(x_array, x: int):
    try:
        # Getting the index whose value is equal to x
        i = 0
        while x_array[i] < x:
            i += 1
        return i
    except IndexError:
        return np.argmax(x_array)

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

def format_float(num:float, dec:int =1) -> str:
    float_formatter = "{:.{}f}".format
    formatted = float_formatter(num, dec)
    return formatted

#################### PLQY Plot Helpers ####################

def baseline(series: pd.core.series.Series, threshold: int = 0.01) -> float:
    series = np.array(series)
    max = np.max(series)
    # newX = series[series <= max * threshold]
    newX = series[series <= (max * threshold)]
    avg = np.average(newX)
    return avg

def localMaxima(series, nth:int =1):
    x = np.array(series)

    loc_max_idxs = argrelextrema(x, np.greater)[0]
    loc_max_vals = x[loc_max_idxs]

    if len(loc_max_idxs) < nth:
        print(f"There are not enough local maxima in the series to retrieve the {nth}th highest local maximum.")
        return None

    # Sort local maxima values in descending order
    sorted_max_idxs = np.argsort(loc_max_vals)[::-1]
    sorted_max_vals = loc_max_vals[sorted_max_idxs]

    # Select the nth highest peak
    nth_max_idx = loc_max_idxs[sorted_max_idxs[nth - 1]]
    nth_max_val = sorted_max_vals[nth - 1]

    return nth_max_idx, nth_max_val

def nthPeakPlotter(series, series2, p,
                nth: int = 1, 
                plot: bool= False, 
                label:str = None, 
                threshold: float = 0.1, 
                plotMax: bool = False,
                fill: bool = False,
                integral: bool = False,
                scale: int = None):
    """
    Retrieve's the `nth` highest peak array and point of a given array, optionally plotting the point.

    Args:
    -
        `series`: The array for x values.

        `series2`: The array for y values whose highest peak will be determined.

        `nth`: The value for the `nth` highest peak.

        `plot`: Boolean value for displaying the plot.

    Returns:
    -
        A new `x` and `y` array that contains the `nth` highest peak and the index `i` associated with the `nth` peak.
    
    Optionally Returns:
    -
        If `plot` set to `True`, then optionally returns a matplotlib plot for the `nth` highest peak point.
    """
    base = baseline(series2, threshold=threshold)
    i, val = localMaxima(series2, nth)
    l_idx = i
    r_idx = i

    while l_idx > 0 and series2[l_idx] > base: l_idx -= 1
    while r_idx < len(series2) - 1 and series2[r_idx] > base: r_idx += 1  

    series = series[l_idx:r_idx]
    series2 = series2[l_idx:r_idx]

    i = i - l_idx
    x = np.array(series)
    y = np.array(series2)
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    suf = suffixes.get(nth, 'th')

    if scale is not None:
        y = (y / np.max(y)) * scale

    if plot == True:
        if label is not None:
            label = label
        else:
            label = f'{nth}{suf} Peak'
        p.line(x, y, label=label)

        if plotMax == True:
            p.line(x[i], y[i], marker='o', markerfacecolor='black', label='Max ' + format_float(x[i], 1) + ' nm')
        if fill == True:
            integral = integrate.trapezoid(y, x)
            p.varea(x, y)
            return x, y, integral
    if integral == True:
        integral = integrate.trapezoid(y, x)
        return x, y, integral
    return x, y, i

def integral(x, y):
    return integrate.trapezoid(y, x)

# def plotMaxPoint(x_array: pd.core.series.Series, y_array: pd.core.series.Series, min_x: int, max_x: int):
#     # Getting the index who's value is equal to min_x
#     min_idx = 0
#     while x_array[min_idx] < min_x: min_idx += 1

#     # Getting the index who's value is equal to max_x
#     max_idx = 0
#     while x_array[max_idx] < max_x: max_idx += 1

#     # Creating a new series with the new min and max indexes
#     series_y = y_array[min_idx:max_idx]

#     x = x_array[series_y.argmax(axis=0)+min_idx]
#     y = np.max(series_y)
#     float_formatter = "{:.1f}".format
#     return min_idx, max_idx

# def nth_integral(x, y, p, 
#                 legend_label: str = None,
#                 nth: float = 1,
#                 scale: float = None,
#                 color: str = None,
#                 plot: bool = False,
#                 plot_type: str = None, 
#                 threshold: float = 0.01,
#                 qy_vals: tuple = None,
#                 l_idx: float = None,
#                 r_idx: float = None,
#                 type: str = None,
#                 ):

#     base = baseline(y, threshold=threshold)
#     i, val = localMaxima(y, nth)
#     l_idx = i
#     r_idx = i
#     while l_idx > 0 and y[l_idx] > base: l_idx -= 1
#     while r_idx < len(y) - 1 and y[r_idx] > base: r_idx += 1  

#     x = x[l_idx:r_idx]
#     y = y[l_idx:r_idx]
#     x = np.array(x)
#     y = np.array(y)

#     if type == 'Obs_1':
#         return integrate.trapezoid(y, x)
#     elif type == 'Obs_2':
#         return integrate.trapezoid(y, x), (l_idx, r_idx)

#     if scale is not None:
#         y = (y / np.max(y)) * scale

#     if legend_label is not None:
#         legend_label = legend_label
#     else:
#         suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
#         suf = suffixes.get(nth, 'th')
#         label = f'{nth}{suf} Peak'
#         legend_label = legend_label + ' ' + label

#     if plot == True:
#         if plot_type == 'enhanced':
#             source = ColumnDataSource(data=dict(x=x, y=y))
#             initial = 1
#             Obs_2N, Obs_2, blk_int, Obs_1, dilute = qy_vals
#             En_t = integrate.trapezoid(y, x)
#             print('En_t', En_t)
#             print("Obs_2N, Obs_2, blk_int, Obs_1", Obs_2N, Obs_2, blk_int, Obs_1)
#             scaler = Slider(start=1, end=5, value=initial, step=0.1, title="Scale Enhanced spectrum", visible=False)
#             callback = CustomJS(args=dict(source=source, scaler=scaler, initial=initial, 
#                                 En_t=En_t,
#                                 Obs_2N=Obs_2N,
#                                 Obs_2=Obs_2,
#                                 blk_int=blk_int,
#                                 Obs_1=Obs_1,
#                                 dilute=dilute),
#                     code="""
#                         const x = source.data.x;
#                         const y1 = source.data.y;

#                         var currentF = Math.max(1, scaler.value); // Ensure currentF is at least 1
#                         var previousF = scaler.previousValue !== undefined ? scaler.previousValue : initial; // Initialize previousF to 1

#                         var y2;
#                         if (currentF !== previousF) {
#                         y2 = y1.map(value => (value / previousF) * currentF);
#                         console.log('previousF:', previousF);
#                         console.log('currentF:', currentF);
#                         } else {
#                         y2 = y1.slice(); // Keep the original y1 values if the scaling factor hasn't changed
#                         }
#                         source.data = { x: x, y: y2 };
#                         scaler.previousValue = currentF;
#                         console.log('y1:', y1);
#                         console.log('y2:', y2);

#                         function calculateQY(Obs_2N, En_t, Obs_2, Blk, Obs_1, dilute) {
#                             var a = 1 - (Obs_2N / En_t);
#                             var Qy_obs = Obs_2 / (Blk - Obs_1);
#                             var Qy = ((Qy_obs) / ((1 - a) + (a * Qy_obs))) * 100;

#                             if (dilute === true) {
#                                 Qy = Qy_obs * 100;
#                                 Qy = Qy.toFixed(2) + '%';
#                                 return Qy;
#                             }

#                             Qy = Qy.toFixed(2) + '%';
#                             return Qy;
#                         }
#                         console.log(calculateQY(Obs_2N, En_t * scaler.value, Obs_2, blk_int, Obs_1, dilute))
#                     const calculatedQY = calculateQY(Obs_2N, En_t * scaler.value, Obs_2, blk_int, Obs_1, dilute);
#                     const quantumYieldElement = document.getElementById("quantum-yield");
#                     quantumYieldElement.innerHTML = '<h4 style="text-align: center;">Quantum yield = ' + calculatedQY + '</h4>';
#                     """)
#             scaler.js_on_change("value", callback)

#             if color is not None: 
#                 p.line('x', 'y', source=source, line_width=2, legend_label=legend_label, color=color)
#             else: 
#                 p.line('x', 'y', source=source, line_width=2, legend_label=legend_label)
            
#             return integrate.trapezoid(y, x), scaler
#         else:
#             if color is not None: 
#                 p.line(x, y, line_width=2, legend_label=legend_label, color=color)
#             else: 
#                 p.line(x, y, line_width=2, legend_label=legend_label)

#     return integrate.trapezoid(y, x)


def nth_integral(x, y, p,
                legend_label: str = None,
                nth: float = 1,
                scale: float = None,
                color: str = None,
                plot: bool = False,
                plot_type: str = None, 
                qy_vals: tuple = None,
                l_idx: float = None,
                r_idx: float = None,
                type: str = None,
                ):
    if type == 'Obs_1' or type == 'Blk':
        x_min = index(x, 448)
        x_max = index(x, 460)
    else:
        x_min = index(x, 467)
        x_max = index(x, 560)

    x = x[x_min:x_max]
    y = y[x_min:x_max]
    x = np.array(x)
    y = np.array(y)

    if type == 'Obs_1' or type == 'Blk':
        return integrate.trapezoid(y, x)
    elif type == 'Obs_2':
        return integrate.trapezoid(y, x), (l_idx, r_idx)

    if scale is not None:
        y = (y / np.max(y)) * scale

    if legend_label is not None:
        legend_label = legend_label
    else:
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        suf = suffixes.get(nth, 'th')
        label = f'{nth}{suf} Peak'
        legend_label = label

    if plot == True:
        if plot_type == 'enhanced':
            source = ColumnDataSource(data=dict(x=x, y=y))
            initial = 1
            Obs_2N, Obs_2, blk_int, Obs_1, dilute = qy_vals
            En_t = integrate.trapezoid(y, x)
            scaler = Slider(start=1, end=5, value=initial, step=0.1, title="Scale Enhanced spectrum", visible=False)
            callback = CustomJS(args=dict(source=source, scaler=scaler, initial=initial, 
                                En_t=En_t,
                                Obs_2N=Obs_2N,
                                Obs_2=Obs_2,
                                blk_int=blk_int,
                                Obs_1=Obs_1,
                                dilute=dilute),
                    code="""
                        const x = source.data.x;
                        const y1 = source.data.y;

                        var currentF = Math.max(1, scaler.value); // Ensure currentF is at least 1
                        var previousF = scaler.previousValue !== undefined ? scaler.previousValue : initial; // Initialize previousF to 1

                        var y2;
                        if (currentF !== previousF) {
                        y2 = y1.map(value => (value / previousF) * currentF);
                        console.log('previousF:', previousF);
                        console.log('currentF:', currentF);
                        } else {
                        y2 = y1.slice(); // Keep the original y1 values if the scaling factor hasn't changed
                        }
                        source.data = { x: x, y: y2 };
                        scaler.previousValue = currentF;
                        console.log('y1:', y1);
                        console.log('y2:', y2);

                        function calculateQY(Obs_2N, En_t, Obs_2, Blk, Obs_1, dilute) {
                            var a = 1 - (Obs_2N / En_t);
                            var Qy_obs = Obs_2 / (Blk - Obs_1);

                            if (dilute === true) {
                                Qy = Qy_obs * 100;
                                Qy = Qy.toFixed(2) + '%';
                                console.log('Returing the dilute calculation')
                                return Qy;
                            }
                            var Qy = ((Qy_obs) / ((1 - a) + (a * Qy_obs))) * 100;
                            Qy = Qy.toFixed(2) + '%';
                            return Qy;
                        }

                        console.log(calculateQY(Obs_2N, En_t * scaler.value, Obs_2, blk_int, Obs_1, dilute))
                        const calculatedQY = calculateQY(Obs_2N, En_t * scaler.value, Obs_2, blk_int, Obs_1, dilute);
                        
                        const quantumYieldElement = document.getElementById("quantum-yield");
                        quantumYieldElement.innerHTML = '<h4 style="text-align: center;">Quantum yield = ' + calculatedQY + '</h4>';""")
            scaler.js_on_change("value", callback)

            if color is not None: 
                p.line('x', 'y', source=source, line_width=2, legend_label=legend_label, color=color)
            else: 
                p.line('x', 'y', source=source, line_width=2, legend_label=legend_label)
            
            return integrate.trapezoid(y, x), scaler
        else:
            if color is not None: 
                p.line(x, y, line_width=2, legend_label=legend_label, color=color)
            else: 
                p.line(x, y, line_width=2, legend_label=legend_label)

    return integrate.trapezoid(y, x)
