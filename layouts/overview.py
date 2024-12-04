from dash import html, dcc
import dash_bootstrap_components as dbc


def overview_layout():
    return html.Div(
        [
            html.H1("Data Overview"),
            dcc.Graph(id="overview-graph"),
            dbc.Row(
                [
                    dbc.Col(html.Div(id="description-table"), width=6),
                    dbc.Col(html.Div(id="overview-table"), width=6),
                ]
            ),
        ]
    )
