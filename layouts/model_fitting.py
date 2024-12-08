from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc


def model_fitting():
    return html.Div(
        [
            html.H1("Model Fitting"),
            dbc.Row(
                [
                    dcc.Loading(
                        id="loding-graph",
                        type="graph",
                        children=[
                            dcc.Graph(id="model-fitting-graph"),
                        ],
                    ),
                    html.Div(
                        dcc.Slider(
                            id="model-fitting-slider",
                            min=0.5,
                            max=0.8,
                            step=0.05,
                            value=0.7,
                            marks={i: f"{i: .2}" for i in [0.5, 0.6, 0.7, 0.8]},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                        style={"margin-top": "20px", "text-align": "center"},
                    ),
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
                            html.Label("Hyperparameter Tuning", className="mt-3"),
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
                                    {"parameter": "freq", "value": ""},
                                    {"parameter": "season_length", "value": ""},
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
