from dash import html, dcc
import dash_table
import dash_bootstrap_components as dbc


def model_fitting():
    return html.Div(
        [
            html.H1("Model Fitting"),
            dbc.Row(
                [
                    dcc.Graph(id="model-fitting-graph"),
                    dbc.Col(
                        [
                            html.Label("Select Model:", className="form-label"),
                            dcc.Dropdown(
                                id="model-fitting-dropdown",
                                options=[
                                    "AutoARIMA",
                                    "HoltWinters",
                                    "SeasonalNaive",
                                    "HistoricAverage",
                                ],
                                placeholder="Select Model",
                                className="mb-3",
                                style={
                                    "width": "100%",
                                    "padding": "5px",
                                    "borderRadius": "5px",
                                    "border": "1px solid #ced4da",
                                    "boxShadow": "0px 1px 2px rgba(0, 0, 0, 0.1)",
                                },
                            ),
                            html.Button(
                                "Run Model",
                                id="run-model-button",
                                n_clicks=0,
                                className="btn btn-primary",
                            ),
                        ],
                        width=4,
                    ),
                    # Right side: Hyperparameter tuning table
                    dbc.Col(
                        [
                            html.H5("Hyperparameter Tuning", className="mt-3"),
                            dash_table.DataTable(
                                id="hyperparameter-table",
                                columns=[
                                    {
                                        "name": "Parameter",
                                        "id": "parameter",
                                        "editable": False,
                                    },
                                    {"name": "Value", "id": "value", "editable": True},
                                ],
                                data=[
                                    {"parameter": "learning_rate", "value": ""},
                                    {"parameter": "max_depth", "value": ""},
                                    {"parameter": "n_estimators", "value": ""},
                                ],
                                editable=True,
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
