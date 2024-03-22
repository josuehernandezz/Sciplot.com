from bokeh.models import Range1d, ColumnDataSource, CustomJS, TextInput, Button, Spinner, NumericInput
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Category20, Cividis, Iridescent
from bokeh.embed import components
from bokeh.models import Styles
from . import calculation as calc
from .settings import plotSettings
from .colors import palette22, palette23
from bokeh.themes import Theme

def abspl_plotter(abs_files, pl_files, abs_labels, pl_labels, norm_num: int = None, theme: str = "",
                title: str = 'Abs PL', x_label: str = 'Wavelength (nm)', y_label: str = 'Intensity (a.u.)',
                x_min: float = 300, x_max: float = 700, 
                y_min: float = 0, y_max: float = 1.1):

    p = figure(sizing_mode='stretch_both', title = title, x_axis_label = x_label, y_axis_label = y_label)
    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)

    if theme == "":
        calc.abs(abs_files, abs_labels, norm_num, Cividis, p)
        print('Cividis')
        calc.pl(pl_files, pl_labels, Category20, p)
        p = plotSettings(p, x_label, y_label, title, 'abspl')
        return components(p)
    else:
        calc.abs(abs_files, abs_labels, norm_num, palette23, p)
        print('Palette23')
        calc.pl(pl_files, pl_labels, palette22, p)
        p, theme = plotSettings(p, x_label, y_label, title, 'abspl', theme=theme)
        return components(p, theme=theme)

def xrd_plotter(card_files, xrd_files, card_labels, xrd_labels,
    title: str = 'Powder XRD', x_label: str = r'2θ (degree)', y_label: str = 'Intensity (a.u.)',
    theme: str = "", 
    x_min: float = 0, x_max: float = 60, y_min: float = 0, y_max: float = 1):
    
    p = figure(sizing_mode='stretch_both', title = title, x_axis_label = x_label, y_axis_label = y_label)
    
    if theme == "":
        calc.card(card_files, card_labels, Cividis, p)
        x, y = calc.xrd(xrd_files, xrd_labels, Category20, p)
        x_min = min(x)
        x_max = max(x)
        p.x_range = Range1d(x_min, x_max)
        p.y_range = Range1d(y_min, y_max)
        p = plotSettings(p, x_label, y_label, title, 'pxrd')
        return components(p)
    else:
        calc.card(card_files, card_labels, palette22, p)
        x, y = calc.xrd(xrd_files, xrd_labels, palette23, p)
        x_min = min(x)
        x_max = max(x)
        p.x_range = Range1d(x_min, x_max)
        p.y_range = Range1d(y_min, y_max)
        p, theme = plotSettings(p, x_label, y_label, title, 'pxrd', theme=theme)
        return components(p, theme=theme)

def ftir_plotter(ftir_files, ftir_labels,
                title: str = 'Abs PL', x_label: str = 'Wavenumbers (cm-1)', y_label: str = '% Transmittance',
                theme: str = "",
                x_min: float = 450, x_max: float = 4000, y_min: float = 0, y_max: float = 1.1):

    p = figure(sizing_mode='stretch_both',
               title = title, x_axis_label = x_label, y_axis_label = y_label)
    p.x_range = Range1d(x_max, x_min)
    p.y_range = Range1d(y_min, y_max)

    if theme == "":
        calc.ftir(ftir_files, ftir_labels, Cividis, p)
        p = plotSettings(p, x_label, y_label, title, 'ftir')
        return components(p)
    else:
        calc.ftir(ftir_files, ftir_labels, palette22, p)
        p, theme = plotSettings(p, x_label, y_label, title, 'ftir', theme=theme)
        return components(p, theme=theme)

def plqy_plotter(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label, reabsorbance_checkbox,
                title: str = 'PLQY', x_label: str = 'Wavelength (nm)', y_label: str = 'Intensity (a.u.)',
                theme: str = "",
                x_min: float = 450, x_max: float = 590, y_min: float = 0, y_max: float = 1.2):

    p = figure(sizing_mode='stretch_both',
               title = title, x_axis_label = x_label, y_axis_label = y_label)

    p.x_range = Range1d(x_min, x_max)
    p.y_range = Range1d(y_min, y_max)

    if theme == "":
        qy, scaler = calc.plqy(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label, p, reabsorbance_checkbox)
        p = plotSettings(p, x_label, y_label, title, 'plqy', scaler = scaler)
        return components(p), qy
    else:
        qy, scaler = calc.plqy(cor_file, blk_file, sct_file, emi_file, cor_label, blk_label, sct_label, emi_label, p, reabsorbance_checkbox)
        p, theme = plotSettings(p, x_label, y_label, title, 'plqy', theme=theme, scaler = scaler)
        return components(p, theme=theme), qy

def universal_plotter(files, labels, theme: str = "",
            title: str = 'Universal', x_label: str = 'x-axis', y_label: str = 'y-axis'):

    p = figure(sizing_mode='stretch_both', title = title, x_axis_label = x_label, y_axis_label = y_label)
    if theme == "":
        plots, x_min, x_max, y_min, y_max = calc.universal(files, labels, Cividis, p)
        p.x_range = Range1d(x_min, x_max)
        p.y_range = Range1d(y_min, y_max)
        p = plotSettings(p, x_label, y_label, title, 'universal')
        return components(p)
    else:
        plots, x_min, x_max, y_min, y_max = calc.universal(files, labels, palette23, p)
        p.x_range = Range1d(x_min, x_max)
        p.y_range = Range1d(y_min, y_max)
        p, theme = plotSettings(p, x_label, title, 'universal', theme=theme)
        return components(p, theme=theme)
