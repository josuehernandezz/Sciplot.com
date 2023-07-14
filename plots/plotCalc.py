# bokeh
from bokeh.models.tools import PanTool, BoxZoomTool, WheelZoomTool, SaveTool, FullscreenTool, ResetTool, UndoTool, RedoTool, HoverTool
from bokeh.models import Range1d, ColumnDataSource, CustomJS, TextInput, Button, Spinner, NumericInput
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import layout, column, row
from bokeh.models import Styles
from bokeh.themes import Theme

# other
from scipy.interpolate import pchip_interpolate

# custom
from .plotHelper import plotColors, norm, fwhm, localMaxima, themePicker, nthPeakPlotter, integral
from . import plotHelper as ph
from .helper import file2df

############ Bokeh Plot Settings ############

def plotSettings(p: figure, x_label, y_label, 
                title: str = None, plot_type: str = None, 
                theme:str = None, scaler = None,
                ):
    p.tools = [PanTool(), BoxZoomTool(), WheelZoomTool(), SaveTool(filename=title), FullscreenTool(),  ResetTool(), UndoTool(), RedoTool(), HoverTool()]
    p.toolbar.active_drag = p.select_one(BoxZoomTool)
    p.toolbar.active_scroll = p.select_one(WheelZoomTool)
    p.legend.click_policy="hide"
    p.toolbar.logo = None

    if plot_type == 'abspl':
        low = 150
        high = 900
        step = 10
        value_l = 300
        value_u = 700
    elif plot_type == 'pxrd':
        low = -10
        high = 80
        step = 5
        value_l = 10
        value_u = 45
    else:
        low = 450
        high = 590
        step = 5
        value_l = low
        value_u = high

    # Define the input text element
    title = TextInput(value=title, width=200, align='center', visible=False)
    callback = CustomJS(args=dict(p=p, title=title), code=""" p.title.text = title.value;""")
    title.js_on_change("value", callback)

    x_axis = TextInput(value=x_label, width=120, align='center', visible=False,)
    x_callback = CustomJS(args=dict(xaxis=p.xaxis[0], x_axis=x_axis), code="""xaxis.axis_label = x_axis.value""")
    x_axis.js_on_change("value", x_callback)

    y_axis = TextInput(value=y_label, width=100, align='center', margin=(0, -20, 0, -20), 
                       styles=Styles(transform='rotate(-90deg)'), visible=False)
    y_callback = CustomJS(args=dict(yaxis=p.yaxis[0], y_axis=y_axis), code="""yaxis.axis_label = y_axis.value""")
    y_axis.js_on_change("value", y_callback)

    x_lim_l = Spinner(title='x-lower' , low=low, high=high, step=step, value=value_l, width=60, visible=False)
    x_lim_cb_l = CustomJS(args=dict(xrange=p.x_range, x_lim=x_lim_l), code='''xrange.start = x_lim.value''')
    x_lim_l.js_on_change("value", x_lim_cb_l)

    x_lim_u = Spinner(title='x-upper' , low=low, high=high, step=step, value=value_u, width=60, visible=False)
    x_lim_cb_u = CustomJS(args=dict(xrange=p.x_range, x_lim=x_lim_u), code='''xrange.end = x_lim.value''')
    x_lim_u.js_on_change("value", x_lim_cb_u)

    if scaler is not None:
        plot_settings_button = Button(label="Plot settings", button_type="primary")
        plot_settings_cb = CustomJS(args=dict(title=title, x_axis=x_axis, y_axis=y_axis, x_lim_l=x_lim_l, x_lim_u=x_lim_u, scaler=scaler), code="""
        if (title.visible === false){
            title.visible = true;
            x_axis.visible = true;
            y_axis.visible = true;
            x_lim_l.visible = true;
            x_lim_u.visible = true;
            scaler.visible = true;
        } else {
            title.visible = false;
            x_axis.visible = false;
            y_axis.visible = false;
            x_lim_l.visible = false;
            x_lim_u.visible = false;
            scaler.visible = false;
        }
        """)
        plot_settings_button.js_on_click(plot_settings_cb)
        h2 = row([x_lim_l, x_lim_u, scaler])
    else:
        plot_settings_button = Button(label="Plot settings", button_type="primary")
        plot_settings_cb = CustomJS(args=dict(title=title, x_axis=x_axis, y_axis=y_axis, x_lim_l=x_lim_l, x_lim_u=x_lim_u), code="""
        if (title.visible === false){
            title.visible = true;
            x_axis.visible = true;
            y_axis.visible = true;
            x_lim_l.visible = true;
            x_lim_u.visible = true;
        } else {
            title.visible = false;
            x_axis.visible = false;
            y_axis.visible = false;
            x_lim_l.visible = false;
            x_lim_u.visible = false;
        }
        """)
        plot_settings_button.js_on_click(plot_settings_cb)
        h2 = row([x_lim_l, x_lim_u])

    h = row([y_axis, p], sizing_mode='stretch_both')
    p = column(title, h, x_axis, h2, plot_settings_button, sizing_mode='stretch_both')

    if theme is not None:
        return p, Theme(filename=themePicker(theme))
    else:
        return p

############ Absorbance & Photoluminesence Plots ############

def abs(abs_files, abs_labels, color, p: figure):
    colors = plotColors(color, len(abs_files))
    plots = []
    for i, file in enumerate(abs_files):
        df = file2df(file)
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
        # normNum = 300
        yNorm = norm(y)

        plots.append([
            p.line(x, yNorm, legend_label=abs_labels[i], line_width=2, line_color=colors[i]),
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
        yNorm = norm(y)
        xf, yf, fwhmv = fwhm(x, y)
        nth_max_idx, nth_max_val = localMaxima(yNorm)
        pl_x_max = x[nth_max_idx]
        color = colors[i]
        plots.append([
            p.line(x, yNorm, legend_label=pl_labels[i], line_width=2, line_color=color), 
            p.line(xf, yf, legend_label='FWHM = %.1f meV' % fwhmv, line_width=2, line_color=color), 
            p.circle(pl_x_max, nth_max_val, size=8, 
                    legend_label='Max = %.1f meV' % pl_x_max, 
                    line_color=color, fill_color='black')
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
        yNorm = norm(y)

        # Select the appropriate legend label and color for the current card file
        legend = labels[i]
        color = colors[i]

        # Create a new data source for each card file
        source = ColumnDataSource(data=dict(legend=[legend] * len(x), x=x, y=yNorm, color=[color] * len(x)))
        
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
        yNorm = norm(y)
        plots.append(p.line(x, yNorm, legend_label=labels[i], line_width=2.5, line_color=colors[i]))
    return x, y

############ Photoluminesence Quantum Yield Plots ############

def qy_xy(files):
    for i, file in enumerate(files):
        df = file2df(file)
        x = df.iloc[:, 0] # gets first and second column for x and y data
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
    Qy = ((Qy_obs) / ((1 - a) + (a * Qy_obs))) * 100 # QY calculation found in paper
    if dilute == True:
        Qy = Qy_obs * 100
        Qy = ph.format_float(Qy, 2) + '%'
        return Qy
    Qy = ph.format_float(Qy, 2) + '%'
    return Qy

def xy_qy(corx, cory, blkx, blky, sctx, scty, emix, emiy, p, threshold: float, blk_label, sct_label, emi_label):
    cor_l = pchip_interpolate(corx,cory,blkx)
    cor_u = pchip_interpolate(corx,cory,blkx)
    blky = blky * cor_l * (blkx * 10 ** -9)
    scty =  scty * cor_l * (sctx * 10 ** -9)
    emiy = emiy * cor_u * (emix * 10 ** -9)
    blk_int = integral(blkx, blky)
    
    for label in emi_label:
        Obs_1 = ph.nth_integral(emix, emiy, p, label, nth=1, threshold=threshold)
        Obs_2 = ph.nth_integral(emix, emiy, p, label, nth=2, threshold=threshold)
        Obs_2N = ph.nth_integral(emix, emiy, p, label, nth=2, scale=1, plot=True, threshold=threshold)
    
    f = 1
    dilute = False
    for label in sct_label:
        en_int, scaler = ph.nth_integral(sctx, scty, p, label + ' Enhanced', 
                        nth=2, scale=f, color='green', plot=True, plot_type='enhanced', 
                        threshold=threshold, qy_vals = (Obs_2N, Obs_2, blk_int, Obs_1, dilute))
    return qyCalc(Obs_2N, en_int, Obs_2, blk_int, Obs_1, dilute=dilute), scaler

def plqy(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label, p, threshold: float = 0.01):
    
    corx, cory = qy_xy(cor_file)
    blkx, blky = qy_xy(blk_file)
    sctx, scty = qy_xy(sct_file)
    emix, emiy = qy_xy(emi_file)

    return xy_qy(corx, cory, blkx, blky, sctx, scty, emix, emiy, p, threshold, blk_label, sct_label, emi_label)
