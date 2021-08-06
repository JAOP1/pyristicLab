import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from layouts import pyristic_layout

from app import app, BASE_URL_PREFIX

items_bar = []


navigation_bar = dbc.Navbar(
    dbc.Container(
        [
            html.Span("pyristicLab",style={'color':'#4CAF50'})
        ]
    ),
    color="white",
    light=True,
    className="mb-5",
    fixed='top'
)


app.layout = html.Div([
    html.Div(id='blank-output'),
    dcc.Location(id='url', refresh=False),
    navigation_bar,
    html.Div(id='page-content')
])

#Modificar el encabezado en el cambio de pagina.
app.clientside_callback(
    f"""
    function(path) {{
        if (path === '{BASE_URL_PREFIX}') {{
            document.title = 'pyristicLab'
        }} else
        {{
            document.title = '404 Not Found...' 
        }}
    }}
    """,
    Output('blank-output', 'children'),
    Input('url', 'pathname')
)

#Moverse entre páginas.
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname:str):
    return pyristic_layout.layout


# Required for gunicorn 
server = app.server

if __name__ == '__main__':
    #Linea para probar local.
    app.run_server(host='127.0.0.1', port='8050', debug=True)
