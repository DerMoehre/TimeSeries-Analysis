from dash import html, dcc
import dash_bootstrap_components as dbc


def model_fitting():
    return html.Div(
        [
            html.H1("Model Fitting"),
            dcc.Graph(id="model-fitting-graph"),
            html.Button("Run Model", id="run-model-button", n_clicks=0),
        ]
    )
