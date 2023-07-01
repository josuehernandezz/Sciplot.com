from bokeh.plotting import figure
from bokeh.palettes import Category10, Category10, TolRainbow, Sunset, Cividis, BrBG, BuPu
from bokeh.models import Range1d
from bokeh.models.tools import PanTool, SaveTool, WheelZoomTool, BoxZoomTool, ResetTool, UndoTool, RedoTool, HoverTool, FullscreenTool
from bokeh.embed import components
from .helper import plotColors, det_delim_ex
import pandas as pd
import numpy as np

def exampleplot(files, legend_labels, title, x_label, y_label):

    colors = plotColors(Category10, len(files))

    p = figure(title=str(title),
        sizing_mode='stretch_both',
        x_axis_label=str(x_label), 
        y_axis_label=str(y_label),
        active_scroll="wheel_zoom")
    
    for i in np.arange(len(files)):
        delimiter = det_delim_ex(files[i])
        # files[i].seek(0)  # Reset the file cursor to the beginning
        data = pd.read_csv(files[i], delimiter=delimiter, names=('wavelength', 'intensity'))
        x = data.wavelength
        y = data.intensity
        y = y / np.max(y)

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
