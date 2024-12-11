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
                            dcc.Graph(
                                id="model-forecast-graph",
                                className="graph-style",
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Button(
                                "Run Forecast",
                                id="run-forecast-button",
                                n_clicks=0,
                                className="btn btn-primary forecast-run-button",
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
                                style_cell={"className": "forecast-horizon-cell"},
                                style_header={"className": "forecast-horizon-header"},
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
        ]
    )
