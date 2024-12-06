import dash_bootstrap_components as dbc
from dash import dcc


def full_width_input(*args, **kwargs):
    if "style" in kwargs:
        kwargs["style"].update({"width": "100%"})
    else:
        kwargs["style"] = {"width": "100%"}
    return dcc.Input(*args, **kwargs)


def create_row(label, component, label_width=6):
    return dbc.Row([
        dbc.Col([
           dbc.Button(label, className="float-left", color="primary", disabled=True)
        ], width=label_width, className="mr-0 pr-0"),
        dbc.Col([
            component
        ], width=12 - label_width, className="ml-0 pl-0")
    ], className="py-1")
