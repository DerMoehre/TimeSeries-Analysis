from dash import html, dcc
import dash_bootstrap_components as dbc


def overview_layout():
    return html.Div(
        [
            html.H1("Data Overview", className="text-center"),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(
                        id="overview-graph", responsive=True, className="graph-style"
                    ),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(id="description-table", children="No data available."),
                    width="auto",
                ),
                justify="center",
            ),
        ],
        className="overview-container",
    )
