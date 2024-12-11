import dash_bootstrap_components as dbc
from dash import html
from layouts.modal import modal_layout

sidebar_layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.Img(
                    src="/assets/logo.jpg",  # Reference the image file in the 'assets' folder
                    height="55px",  # Set a height for the image
                    className="sidebar-logo",
                ),
                width={"size": 12, "offset": 0},
            )
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Home", href="/", active="exact", className="sidebar-nav-link"
                ),
                dbc.NavLink(
                    "Model Fitting",
                    href="/model",
                    active="exact",
                    className="sidebar-nav-link",
                ),
                dbc.NavLink(
                    "Forecast",
                    href="/forecast",
                    active="exact",
                    className="sidebar-nav-link",
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        dbc.Button(
            "Upload Data",
            id="open-upload-modal",
            color="primary",
            className="sidebar-upload-button",
        ),
        modal_layout,
    ],
    className="sidebar",
)
