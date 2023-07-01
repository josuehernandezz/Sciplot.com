from bokeh.plotting import figure, curdoc, show
from bokeh.palettes import Category10, Category10, TolRainbow, Sunset, Cividis, BrBG, BuPu
from bokeh.models import Range1d, ColumnDataSource
from bokeh.models.tools import PanTool, SaveTool, WheelZoomTool, BoxZoomTool, ResetTool, UndoTool, RedoTool, HoverTool, FullscreenTool
from bokeh.embed import components
from .helper import plotColors, determine_delimiter
import pandas as pd
import numpy as np

def abspl_plotter(files, legend_labels, title, x_label, y_label):

    colors = plotColors(Category10, len(files))

    p = figure(title=str(title),
        sizing_mode='stretch_both',
        x_axis_label=str(x_label), 
        y_axis_label=str(y_label),
        active_scroll="wheel_zoom")
    
    for i in np.arange(len(files)):
        delimiter = determine_delimiter(files[i].read().decode())
        files[i].seek(0)  # Reset the file cursor to the beginning
        data = pd.read_csv(files[i], delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        # y = y / np.max(y)
        y = y

        p.toolbar.logo = None

        # p.toolbar.active_drag = p.select(PanTool)[0].name  # Set the name of the first PanTool as the active drag tool
        p.toolbar.active_scroll = p.select(WheelZoomTool)[0].name  # Set the name of the first WheelZoomTool as the active scroll tool

        p.tools = [SaveTool(filename=title), FullscreenTool(), PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool(), UndoTool(), RedoTool(), HoverTool()]
        hover = HoverTool()
        hover.tooltips = [("(x,y)", "($x, $y)")]
        p.line(x, y, legend_label=legend_labels[i], line_width=2, line_color=colors[i])
        p.legend.click_policy="hide"

        p.x_range = Range1d(300, 800)  # Set the x-axis range from 300 to 800
        p.y_range = Range1d(0, 1)     # Set the y-axis range from 0 to 1

    # text_input = TextInput(value="default", title="Label:")
    x_min = 300  # Minimum x value
    x_max = 700  # Maximum x value
    y_min = 0     # Minimum y value
    y_max = max(y)       # Maximum y value
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)

    script, div = components(p)
    return script, div

# def xrd_plotter(files, legend_labels, title, x_label, y_label):
def xrd_plotter(cardfiles, files, cardfile_labels, legend_labels, title, x_label, y_label):

    ########################### CARD UPLOADED FILES ###########################
    cardColors = plotColors(Cividis, len(cardfiles))

    for cardfile in np.arange(len(cardfiles)):
        delimiter = determine_delimiter(cardfiles[cardfile].read().decode())
        cardfiles[cardfile].seek(0)
        data = pd.read_csv(cardfiles[cardfile], delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        y = y / np.max(y)
        # Create a ColumnDataSource
        legend = cardfile_labels * len(x)
        color = cardColors * len(x)
        source = ColumnDataSource(data=dict(legend=legend, x=x, y=y, color=color))
        # Create the figure
        p = figure(sizing_mode='stretch_both', title=title, active_scroll="wheel_zoom")
        
        # Add the VBar glyph
        p.vbar(x='x', top='y', width=0.05, legend_field='legend', color='color', source=source)
    
    ########################### XRD UPLOADED FILES ###########################
    colors = plotColors(Category10, len(files))

    for i in np.arange(len(files)):
        delimiter = determine_delimiter(files[i].read().decode())
        files[i].seek(0)  # Reset the file cursor to the beginning
        data = pd.read_csv(files[i], delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        y = y / np.max(y)
        p.toolbar.logo = None
        # p.tools = [SaveTool(filename=title), PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool()]
        p.tools = [SaveTool(filename=title), FullscreenTool(), PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool(), UndoTool(), RedoTool(), HoverTool()]
        hover = HoverTool()
        hover.tooltips = [("(x,y)", "($x, $y)")]

        p.line(x, y, legend_label=legend_labels[i], line_width=3, line_color=colors[i])
        p.legend.click_policy="hide"

    # Set axis labels
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = y_label
    x_min = min(x)  # Minimum x value
    x_max = max(x)  # Maximum x value
    y_min = 0     # Minimum y value
    y_max = max(y)     # Maximum y value
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)

    script, div = components(p)
    return script, div
