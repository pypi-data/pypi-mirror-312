import dash_bootstrap_components as dbc
from dash import html
from dash_extensions.enrich import Dash
from dash import dcc

from vizer.control import create_layout, create_callbacks
from vizer.ids import CHARTS_STORE_ID, SELECTED_CHART_STORE_ID, GENERAL_STORE_ID, PLOT_LAYOUT_STORE_ID, URL_ID
from vizer import workspace

STORAGE_TYPE = 'session'


def create_webapp():

    css = [dbc.themes.BOOTSTRAP] + ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"]

    app = Dash(
        __name__, external_stylesheets=css, prevent_initial_callbacks=True
    )

    app.layout = html.Div([
            dcc.Store(id=CHARTS_STORE_ID, data=workspace.cws.charts, storage_type=STORAGE_TYPE),
            dcc.Store(id=SELECTED_CHART_STORE_ID, data=workspace.cws.selected, storage_type=STORAGE_TYPE),
            dcc.Store(id=GENERAL_STORE_ID, data=workspace.cws.general, storage_type=STORAGE_TYPE),
            dcc.Store(id=PLOT_LAYOUT_STORE_ID, data=workspace.cws.plot, storage_type=STORAGE_TYPE),
            dcc.Location(id=URL_ID),
            create_layout()
        ], style={'height': '100vh'})

    create_callbacks(app)

    return app
