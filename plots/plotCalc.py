# bokeh
from bokeh.models.tools import PanTool, BoxZoomTool, WheelZoomTool, SaveTool, FullscreenTool, ResetTool, UndoTool, RedoTool, HoverTool
from bokeh.models import Range1d, ColumnDataSource, CustomJS, TextInput, Button, Spinner, NumericInput
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import layout, column, row
from bokeh.models import Styles
from bokeh.themes import Theme

# custom
from .plotHelper import plotColors, norm, fwhm, localMaxima, themePicker
from .helper import file2df

############ Bokeh Plot Settings ############

def plotSettings(p: figure, x_label, y_label, title: str = None, plot_type: str = None, theme:str = None):
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
    else:
        low = -10
        high = 80
        step = 5
        value_l = 10
        value_u = 45

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

    h = row([y_axis, p], sizing_mode='stretch_both')
    h2 = row([x_lim_l, x_lim_u])
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
            p.line(x, yNorm, legend_label=abs_labels[i], line_width=2, line_color=colors[i])
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
