from bokeh.models import Range1d, ColumnDataSource, CustomJS, TextInput, Button, Spinner, NumericInput
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Category20, Cividis, Iridescent
from bokeh.embed import components
from bokeh.models import Styles
from . import plotCalc as pc
from .plotHelper import palette22, palette23

def abspl_plotter(abs_files, pl_files, abs_labels, pl_labels,
                title: str = 'Abs PL', x_label: str = 'Wavelength (nm)', y_label: str = 'Intensity (a.u.)',
                theme: str = None,
                x_min: float = 300, x_max: float = 700, y_min: float = 0, y_max: float = 1.1):

    p = figure(sizing_mode='stretch_both',
               title = title, x_axis_label = x_label, y_axis_label = y_label)

    if theme == None:
        pc.abs(abs_files, abs_labels, Cividis, p)
        pc.pl(pl_files, pl_labels, Category20, p)
    else:
        pc.abs(abs_files, abs_labels, palette23, p)
        pc.pl(pl_files, pl_labels, palette22, p)
    
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)
    p = pc.plotSettings(p, x_label, y_label, title, 'abspl')
    return components(p)

def xrd_plotter(card_files, xrd_files, card_labels, xrd_labels, 
    title: str = 'Powder XRD', x_label: str = r'2θ (degree)', y_label: str = 'Intensity (a.u.)',
    x_min: float = 0, x_max: float = 60, y_min: float = 0, y_max: float = 1):
    
    p = figure(sizing_mode='stretch_both', title = title, x_axis_label = x_label, y_axis_label = y_label)

    pc.card(card_files, card_labels, Cividis, p)
    x, y = pc.xrd(xrd_files, xrd_labels, Category20, p)

    x_min = min(x)
    x_max = max(x)
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)
    p = pc.plotSettings(p, x_label, y_label, title, 'pxrd')
    return components(p)

def plqy_plotter(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label,
                title: str = 'PLQY', x_label: str = 'Wavelength (nm)', y_label: str = 'Intensity (a.u.)',
                theme: str = None,
                x_min: float = 450, x_max: float = 590, y_min: float = 0, y_max: float = 2):

    p = figure(sizing_mode='stretch_both',
               title = title, x_axis_label = x_label, y_axis_label = y_label)

    if theme == None:
        qy, scaler = pc.plqy(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label, p)
    else:
        qy, scaler = pc.plqy(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label, p)
    
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)
    p = pc.plotSettings(p, x_label, y_label, title, 'plqy', scaler = scaler)
    return components(p), qy
