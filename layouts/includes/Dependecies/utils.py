import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from functools import partial
import plotly.graph_objects as go


def form_group(description, inp):
    #dbc.Tooltip("textooo", target='id-coso')
    return dbc.FormGroup([dbc.Label(dcc.Markdown(description), className='gray_text'), inp])

def create_control(control:dict, id_:str):
    kw = control.get("kwargs", {})
    if control.get("dropdown", False):
        wcls = partial(dcc.Dropdown, options=control["options"])
        kw["clearable"] = kw.get("clearable", False)
        kw["searchable"] = kw.get("searchable",False)
    elif control.get("slider", False):
        wcls = dcc.Slider
    else:
        wcls = partial(dcc.Input, type="number")
        kw["step"] = kw.get("step", 0.01)

    return form_group(control["desc"], wcls(id=id_,value=control["default"], **kw))

def create_title(name, _id='main-title', style_title={}, style_box = {}):
    styleTitle = {'color':'white'}
    styleBox = {'marginTop':'70px','marginBottom':'60px'}
    if style_title != {}:
        styleTitle = style_title

    if style_box != {}:
        styleBox = style_box
    
    title = html.H2(name, id=_id,style=styleTitle)
    return html.Div([title,
                  html.Hr(className='dividerlg'),
                 ],
                 className='text-center',style = styleBox
                )

def decimalFormat(val):
    return "{:.3f}".format(val)

def make_graph(x_, y_, name, case, xaxis, yaxis):
    # grafica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_, y=y_, name=name))
    fig.add_trace(go.Scatter(x=case[0], y=case[1],
                             name='Mejor y peor valor', mode="markers"))
    # titulo
    fig.update_layout(  xaxis=xaxis, yaxis=yaxis,\
                        legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                    )
    fig.layout.template = 'simple_white'
    return fig