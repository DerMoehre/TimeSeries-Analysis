from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc


def forecasting():
    return html.Div(
        [
            html.H1("Forecasting"),
            dbc.Row(
                [
                    dcc.Loading(
                        id="forecast-graph",
                        type="graph",
                        children=[
                            dcc.Graph(id="model-forecast-graph"),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Button(
                                "Run Forecast",
                                id="run-forecast-button",
                                n_clicks=0,
                                className="btn btn-primary",
                            ),
                        ],
                        width=4,
                    ),
                    # Right side: Hyperparameter tuning table
                    dbc.Col(
                        [
                            html.Label(
                                "How long should the forecast be?", className="mt-3"
                            ),
                            dash_table.DataTable(
                                id="forecast-horizon",
                                columns=[
                                    {
                                        "name": "Parameter",
                                        "id": "parameter",
                                        "editable": False,
                                    },
                                    {"name": "Value", "id": "value", "editable": True},
                                ],
                                data=[
                                    {"parameter": "length", "value": ""},
                                ],
                                editable=True,
                                persistence=True,
                                persistence_type="session",
                                style_table={"overflowX": "auto"},
                                style_cell={
                                    "textAlign": "left",
                                    "padding": "10px",
                                    "border": "1px solid lightgrey",
                                },
                                style_header={
                                    "backgroundColor": "rgb(230, 230, 230)",
                                    "fontWeight": "bold",
                                },
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
        ]
    )
