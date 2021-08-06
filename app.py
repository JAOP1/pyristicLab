from re import U
import dash
import dash_bootstrap_components as dbc
# Bootstrap CSS and favicon.
external_stylesheets_ = [dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
BASE_URL_PREFIX = '/home/'
app = dash.Dash(__name__,\
                suppress_callback_exceptions=True,\
                external_stylesheets = external_stylesheets_,\
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],\
                title='pyristicLab',\
                update_title='Cargando...',\
                url_base_pathname=BASE_URL_PREFIX)

# app.config.suppress_callback_exceptions = True