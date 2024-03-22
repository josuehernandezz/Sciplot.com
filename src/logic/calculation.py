# bokeh
from bokeh.plotting import figure, ColumnDataSource

# custom
from .calc_helper import norm, fwhm, localMaxima, nthPeakPlotter, integral
from .colors import plotColors
from . import calc_helper as ph
from .file2data import file2df

# other
from scipy.interpolate import pchip_interpolate
from statsmodels.nonparametric.smoothers_lowess import lowess

############ Absorbance & Photoluminesence Plots ############

def abs(abs_files, abs_labels, norm_num, color, p: figure):
    colors = plotColors(color, len(abs_files))
    plots = []
    for i, file in enumerate(abs_files):
        df = file2df(file)
        x = df.iloc[:, 0]
        # x = x.iloc[::-1] # reverse x axis for testing.
        y = df.iloc[:, 1]
        y_norm = norm(y, x, None)
        plots.append([
            p.line(x, y_norm, legend_label=abs_labels[i], line_width=2, line_color=colors[i]),
        ])
    return plots

def pl(pl_files, pl_labels, color, p: figure):    
    if len(pl_files) != 0:
        colors = plotColors(color, len(pl_labels))

    plots = []
    for i, file in enumerate(pl_files):
        df = file2df(file)
        x = df.iloc[:, 0] # gets first and second column for x and y data
        y = df.iloc[:, 1]
        y_norm = norm(y)
        xf, yf, fwhmv = fwhm(x, y)
        nth_max_idx, nth_max_val = localMaxima(y_norm)
        pl_x_max = x[nth_max_idx]
        color = colors[i]
        plots.append([
            p.line(x, y_norm, legend_label=pl_labels[i], line_width=2, line_color=color), 
            p.line(xf, yf, legend_label='FWHM = %.1f meV' % fwhmv, line_width=2, line_color=color), 
            p.circle(pl_x_max, nth_max_val, size=8, 
                    legend_label='Max = %.1f meV' % pl_x_max, 
                    line_color=color, fill_color='black')
            ])
    return plots

############ FTIR ############

def ftir(ftir_files, ftir_labels, color, p):
    colors = plotColors(color, len(ftir_files))
    plots = []
    for i, file in enumerate(ftir_files):
        df = file2df(file)
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
        y_norm = norm(y, x, None)
        plots.append([
            p.line(x, y_norm, legend_label=ftir_labels[i], line_width=2, line_color=colors[i]),
        ])
    return plots

############ Powder XRD Plots ############

def card(files, labels, color, p: figure):
    if len(files) != 0:
        colors = plotColors(color, len(files))
        labels = labels[:len(files)]
    
    plots = []
    for i, file in enumerate(files):
        df = file2df(file)
        x = df.iloc[:, 0] # gets first and second column for x and y data
        y = df.iloc[:, 1]
        y_norm = norm(y)

        # Select the appropriate legend label and color for the current card file
        legend = labels[i]
        color = colors[i]

        # Create a new data source for each card file
        source = ColumnDataSource(data=dict(legend=[legend] * len(x), x=x, y=y_norm, color=[color] * len(x)))
        
        # Add the VBar glyph for the current card file, using the data source
        plots.append(p.vbar(x='x', top='y', width=0.05, legend_label=legend, color='color', source=source))
    return plots

def xrd(files, labels, color, p: figure):
    if len(files) != 0:
        colors = plotColors(color, len(files))
        labels = labels[:len(files)]  # Truncate legend_labels to match the number of files

    plots = []
    for i, file in enumerate(files):
        df = file2df(file)
        x = df.iloc[:, 0] # gets first and second column for x and y data
        y = df.iloc[:, 1]
        y_norm = norm(y)
        plots.append(p.line(x, y_norm, legend_label=labels[i], line_width=2.5, line_color=colors[i]))
    return x, y

############ Photoluminesence Quantum Yield Plots ############

def qy_xy(files):
    for i, file in enumerate(files):
        df = file2df(file)
        # gets first and second column for x and y data
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
    return x, y

# after x and y, we need to perform calculations on each file

def qyCalc(Obs_2N, En_t, Obs_2, Blk, Obs_1, dilute) -> str:
    '''
    Takes the normalized emission peak of the concentrated sample (Obs) `Obs_2N`, the enhanced emission of the 
    diluted peak `En_t`, the un-normalized emission peak of the (Obs) `Obs_2`, the blank integral `Blk`, the (Obs) excitation 
    peak `Obs_1`, and the boolean indicating the Quantum yield calculation of just the dilute sample `dilute`

    Args
    -
        `Obs_2N` Normalized observed emission integral.

        `En_t` Enhanced emission integral.
        
        `Obs_2` Observed emission integral
        
        `Blk` Blank excitation integral
        
        `Obs_1` Observed excitation integral
        
        `dilute` Boolean for calculating the quantum yield of Observed `QY`

    Returns
    -
        `Qy` The quantum yield of the sample.

    Theory
    -
        QY = (QYobs) / 1 - a

        a = 1 - int_ratio

        int_ratio = int(Normalized Undiluted Emission)/int(Enhanced diluted emission)
    '''

    a = 1 - (Obs_2N / (En_t)) # Normalized emission of Concentrated sample, divided by the diluted scaled emission such that the red tails touch.
    Qy_obs = Obs_2 / (Blk - Obs_1) # 'Normal' QY calculation. Accounting for the blank excitation
    
    if dilute == True:
        Qy = Qy_obs * 100
        Qy = ph.format_float(Qy, 2) + '%'
        return Qy
    
    Qy = ((Qy_obs) / ((1 - a) + (a * Qy_obs))) * 100 # QY calculation found in paper
    Qy = ph.format_float(Qy, 2) + '%'
    return Qy

def xy_qy(corx, cory, blkx, blky, sctx, scty, emix, emiy, p, 
    threshold: float, blk_label, sct_label, emi_label, reabsorbance_checkbox):
    cor_l_b = pchip_interpolate(corx,cory,blkx)
    cor_l_s = pchip_interpolate(corx,cory,sctx)
    cor_u = pchip_interpolate(corx,cory,emix)
    blky = blky * cor_l_b * (blkx * 10 ** -9)
    scty =  scty * cor_l_s * (sctx * 10 ** -9)
    emiy = emiy * cor_u * (emix * 10 ** -9)
    blk_int = ph.nth_integral(blkx, blky, p, nth=1, plot=True, scale=True, type='Blk')
    
    # Integral calculation and plot for the Undiluted QY spectrum
    for label in emi_label:
        Obs_1 = ph.nth_integral(emix, emiy, p, label, nth=1, type='Obs_1')
        Obs_2, idx_tup = ph.nth_integral(emix, emiy, p, label, nth=2, type='Obs_2')
        Obs_2N = ph.nth_integral(emix, emiy, p, label, nth=2, scale=1, plot=True, l_idx=idx_tup[0], r_idx=idx_tup[1])

    f = 1
    dilute = reabsorbance_checkbox
    print(f'DILUTE VALUE: {dilute}')
    for label in sct_label:
        lowess_tight = lowess(scty, sctx, frac = .05)
        en_int, scaler = ph.nth_integral(lowess_tight[:,0], lowess_tight[:,1], p, label + ' Lowess tightEnhanced', 
                        nth=2, scale=f, color='green', plot=True, plot_type='enhanced', 
                        qy_vals = (Obs_2N, Obs_2, blk_int, Obs_1, dilute), l_idx=idx_tup[0], r_idx=idx_tup[1])
        # en_int, scaler = ph.nth_integral(sctx, scty, p, label + ' Enhanced', 
        #                 nth=2, scale=f, color='green', plot=True, plot_type='enhanced', 
        #                 qy_vals = (Obs_2N, Obs_2, blk_int, Obs_1, dilute), l_idx=idx_tup[0], r_idx=idx_tup[1])
        
    return qyCalc(Obs_2N, en_int, Obs_2, blk_int, Obs_1, dilute=dilute), scaler

def plqy(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, 
    sct_label, emi_label, p, reabsorbance_checkbox, threshold: float = 0.01):
    
    corx, cory = qy_xy(cor_file)
    blkx, blky = qy_xy(blk_file)
    sctx, scty = qy_xy(sct_file)
    emix, emiy = qy_xy(emi_file)

    return xy_qy(corx, cory, blkx, blky, sctx, scty, emix, emiy, p, threshold, blk_label, sct_label, emi_label, reabsorbance_checkbox)


###################### Universal #########################

def universal(files, labels, color, p: figure):
    colors = plotColors(color, len(files))
    plots = []
    for i, file in enumerate(files):
        df = file2df(file)
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
        plots.append([
            p.line(x, y, legend_label=labels[i], line_width=2, line_color=colors[i]),
        ])
    return plots, min(x), max(x), min(y), max(y)
