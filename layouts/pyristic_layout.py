from layouts.includes.configPyristicLayout import   continuosAlgorithmsConfig,\
                                                    discreteAlgorithmsConfig,\
                                                    pyristicBoard
from layouts.includes.Dependecies.baseClass import SidebarOptions
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app

continuosLayout = []
for configuration in continuosAlgorithmsConfig:
    configuration.setup()
    continuosLayout += configuration.layout()

discreteLayout = []
for configuration in discreteAlgorithmsConfig:
    configuration.setup()
    discreteLayout += configuration.layout()


_optionsSidebar = [
        {   'label': 'Optimización combinatoria',\
            'layout_items':discreteLayout
        },\
        {   'label':'Optimización continua',\
            'layout_items':continuosLayout
        }
    ]

pyristicSidebar = SidebarOptions(_optionsSidebar)
pyristicSidebar.setup()
pyristicBoard.setup()

sidebarButton = html.Button(children=[html.I(className="fas fa-angle-right fa-3x")],
                            id='openSidebar', className='button-left-bottom gear-button')
          
main_content = dbc.Container([sidebarButton] + pyristicBoard.layout(),
                            className='content-transition',
                            id='pyristic-dashboard',fluid=True,
                            style={'marginLeft': '0', 'marginTop': '25px'})

sidebar_content = html.Div(pyristicSidebar.layout(),
                            id='pyristic-sidebar',
                            className='sidebar',
                            style={'width':'0'})

layout = html.Div([sidebar_content, main_content])

@app.callback(
    [
        Output('pyristic-sidebar','style'),
        Output('pyristic-dashboard', 'style')
    ],
    [
        Input('openSidebar','n_clicks'),
        Input('closeSidebar','n_clicks')
    ],
    # prevent_initial_call=True
)
def display_sidebar(open_clicks,close_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'closeSidebar':
        return  {'width':'0'}, {'marginLeft':'0'}
    return {'width':'290px'}, {'marginLeft':'290px'}