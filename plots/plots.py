from bokeh.plotting import figure, curdoc, show
from bokeh.palettes import Category20, Cividis
from bokeh.models import Range1d, ColumnDataSource, CustomJS, TextInput
from bokeh.models.tools import PanTool, SaveTool, WheelZoomTool, BoxZoomTool, ResetTool, UndoTool, RedoTool, HoverTool, FullscreenTool
from bokeh.embed import components
from .helper import plotColors, determine_delimiter
from .plotHelper import norm, fwhm, localMaxima
import pandas as pd
import numpy as np

def abspl_plotter(abs_files, pl_files, abs_labels, pl_labels, title, x_label, y_label):

    abs_colors = plotColors(Cividis, len(abs_files))

    p = figure(title=str(title),
        sizing_mode='stretch_both',
        x_axis_label=str(x_label), 
        y_axis_label=str(y_label),
        )

    ########################### ABS UPLOADED FILES ###########################
    for i in np.arange(len(abs_files)):
        delimiter = determine_delimiter(abs_files[i].read().decode())
        abs_files[i].seek(0)  # Reset the file cursor to the beginning
        data = pd.read_csv(abs_files[i], delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        normNum = 300
        yNorm, idx = norm(y, x, normNum)
        p.line(x, yNorm, legend_label=abs_labels[i], line_width=2, line_color=abs_colors[i])

    ########################### PL UPLOADED FILES ###########################
    if len(pl_files) != 0:
        pl_colors = plotColors(Category20, len(pl_labels))
    
    for i in np.arange(len(pl_files)):
        delimiter = determine_delimiter(pl_files[i].read().decode())
        pl_files[i].seek(0)  # Reset the file cursor to the beginning
        data = pd.read_csv(pl_files[i], delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        yNorm = norm(y)
        xf, yf, fwhmv = fwhm(x, y)
        nth_max_idx, nth_max_val = localMaxima(yNorm)
        pl_x_max = x[nth_max_idx]
        p.line(x, yNorm, legend_label=pl_labels[i], line_width=2, line_color=pl_colors[i])
        p.line(xf, yf, legend_label='FWHM = %.1f meV' % fwhmv, line_width=2, line_color=abs_colors[i])
        p.circle(pl_x_max, nth_max_val, size=8, legend_label='Max = %.1f meV' % pl_x_max, fill_color='black')

    p.toolbar.logo = None
    p.tools = [SaveTool(filename=title), FullscreenTool(), PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool(), UndoTool(), RedoTool(), HoverTool()]
    p.toolbar.active_drag = p.select_one(BoxZoomTool)
    p.toolbar.active_scroll = p.select_one(WheelZoomTool)
    p.legend.click_policy="hide"
    x_min = 300  # Minimum x value
    x_max = 700  # Maximum x value
    y_min = 0     # Minimum y value
    y_max = 1.1       # Maximum y value
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)

    return components(p)

def xrd_plotter(card_files, xrd_files, card_labels, xrd_labels, title, x_label, y_label):
    ########################### CARD UPLOADED FILES ###########################
    if len(card_files) != 0:
        card_colors = plotColors(Cividis, len(card_files))
        card_labels = card_labels[:len(card_files)]  # Truncate legend_labels to match the number of files

    # Create the figure
    p = figure(sizing_mode='stretch_both', title=title)
    
    for i, cardfile in enumerate(card_files):
        delimiter = determine_delimiter(cardfile.read().decode())
        cardfile.seek(0)
        data = pd.read_csv(cardfile, delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        y = y / np.max(y)

        # Select the appropriate legend label and color for the current card file
        legend = card_labels[i]
        color = card_colors[i]

        # Create a new data source for each card file
        source = ColumnDataSource(data=dict(legend=[legend] * len(x), x=x, y=y, color=[color] * len(x)))
        
        # Add the VBar glyph for the current card file, using the data source
        p.vbar(x='x', top='y', width=0.05, legend_label=legend, color='color', source=source)

    ########################### XRD UPLOADED FILES ###########################
    if len(xrd_files) != 0:
        xrd_colors = plotColors(Category20, len(xrd_files))
        xrd_labels = xrd_labels[:len(xrd_files)]  # Truncate legend_labels to match the number of files

    for i, file in enumerate(xrd_files):
        delimiter = determine_delimiter(file.read().decode())
        file.seek(0)
        data = pd.read_csv(file, delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        y = y / np.max(y)

        p.line(x, y, legend_label=xrd_labels[i], line_width=2.5, line_color=xrd_colors[i])

    # Set axis labels
    p.toolbar.logo = None
    p.tools = [SaveTool(filename=title), FullscreenTool(), PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool(), UndoTool(), RedoTool(), HoverTool()]
    p.toolbar.active_drag = p.select_one(BoxZoomTool)
    p.toolbar.active_scroll = p.select_one(WheelZoomTool)
    p.legend.click_policy = "hide"
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = y_label
    x_min = min(x)  # Minimum x value
    x_max = max(x)  # Maximum x value
    y_min = 0  # Minimum y value
    y_max = max(y)  # Maximum y value
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)

    return components(p)
