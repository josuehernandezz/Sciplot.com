from bokeh.models.tools import PanTool, BoxZoomTool, WheelZoomTool, SaveTool, FullscreenTool, ResetTool, UndoTool, RedoTool, HoverTool
from bokeh.models import CustomJS, TextInput, Button, Spinner, Toggle
from bokeh.plotting import figure
from bokeh.layouts import layout, column, row
from bokeh.models import Styles
from bokeh.themes import Theme
from .colors import themePicker

############ Bokeh Plot Settings ############

def plotSettings(p: figure, x_label, y_label, 
                title: str = None, plot_type: str = None, 
                theme:str = None, scaler = None):
    
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

        # norm_num = Spinner(title='Normalize to' , low=0, high=10, step=0.1, value=1, width=60, visible=False)
        # norm_callback = CustomJS(args=dict(t= 't'), code='''''')
        # norm_num.js_on_change("value", norm_callback)

        # tog_btn = Button(label="Normalize", button_type="primary", visible=False)
        # tog_btn_cb = (CustomJS(args=dict(norm_num=norm_num), code="""
        # if (norm_num.visible === false){
        #     norm_num.visible = true;
        # } else {
        #     norm_num.visible = false;
        # }
        # """))
        # tog_btn.js_on_click(tog_btn_cb)
    elif plot_type == 'pxrd':
        low = -10
        high = 80
        step = 5
        value_l = 10
        value_u = 45
    elif plot_type == 'plqy':
        low = 450
        high = 590
        step = 5
        value_l = low
        value_u = high
    else:
        low = 450
        high = 4000
        step = 5
        value_l = low
        value_u = high

    # Define the input text element
    title = TextInput(title='Title', value=title, width=200, align='center', visible=False)
    callback = CustomJS(args=dict(p=p, title=title), code=""" p.title.text = title.value;""")
    title.js_on_change("value", callback)

    x_axis = TextInput(title='x-axis', value=x_label, width=120, align='center', visible=False,)
    x_callback = CustomJS(args=dict(xaxis=p.xaxis[0], x_axis=x_axis), code="""xaxis.axis_label = x_axis.value""")
    x_axis.js_on_change("value", x_callback)

    y_axis = TextInput(title='y-axis', value=y_label, width=100, align='center', margin=(0, -20, 0, -20), 
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
    if scaler is not None:
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
        h2 = row([x_lim_l, x_lim_u, scaler])
    # elif plot_type == 'abspl':
    #     plot_settings_cb = CustomJS(args=dict(title=title, x_axis=x_axis, 
    #     y_axis=y_axis, x_lim_l=x_lim_l, x_lim_u=x_lim_u, tog_btn=tog_btn,
    #     norm_num=norm_num), code="""
    #     if (title.visible === false){
    #         title.visible = true;
    #         x_axis.visible = true;
    #         y_axis.visible = true;
    #         x_lim_l.visible = true;
    #         x_lim_u.visible = true;
    #         tog_btn.visible = true;
    #     } else {
    #         title.visible = false;
    #         x_axis.visible = false;
    #         y_axis.visible = false;
    #         x_lim_l.visible = false;
    #         x_lim_u.visible = false;
    #         tog_btn.visible = false;
    #         norm_num.visible = false;
    #     }
    #     """)
    #     h2 = row([x_lim_l, x_lim_u])
    else:
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
        h2 = row([x_lim_l, x_lim_u])

    plot_settings_button.js_on_click(plot_settings_cb)
    h = row([y_axis, p], sizing_mode='stretch_both')
    p = column(title, h, x_axis, h2, 
            # row(
            plot_settings_button, 
            # column(tog_btn, norm_num)), 
            sizing_mode='stretch_both')

    if theme is not None:
        return p, Theme(filename=themePicker(theme))
    else:
        return p
