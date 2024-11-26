import dash_bootstrap_components as dbc
from dash import html
from layouts.modal import modal_layout

sidebar_layout = html.Div(
    [
         dbc.Row(
            dbc.Col(
                html.Img(
                    src='/assets/logo.jpg',  # Reference the image file in the 'assets' folder
                    height='55px',  # Set a height for the image
                    style={'marginBottom': '10px'}
                ),
                width={'size': 12, 'offset': 0}
            )
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Model Fitting", href="/model", active="exact"),
                dbc.NavLink("Forecast", href="/forecast", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        dbc.Button("Upload Data", id="open-upload-modal", color="primary", className="mt-3"),
        dbc.Button("Delete Uploaded Data", id="delete-data-button", color="danger", n_clicks=0),
        modal_layout
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "250px",
        "padding": "10px",
        "backgroundColor": "#343a40",
        "color": "white",
    },
)