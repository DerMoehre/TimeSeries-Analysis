from dash import html, dcc
import dash_bootstrap_components as dbc

modal_layout = dbc.Modal(
    [
        dbc.ModalHeader("Upload Data"),
        dbc.ModalBody(
            [
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and drop or ", html.A("Select Files")]),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    multiple=False,
                ),
                html.Div(id="upload-status", style={"marginTop": "10px"}),
                # Dropdowns for column selection
                html.Div(
                    [
                        html.Label("Select X-axis Column:", className="form-label"),
                        dcc.Dropdown(
                            id="x-axis-column",
                            options=[],  # Will be dynamically populated
                            placeholder="Select X-axis column",
                            className="mb-3",
                            style={
                                "width": "100%",
                                "padding": "5px",
                                "borderRadius": "5px",
                                "border": "1px solid #ced4da",
                                "boxShadow": "0px 1px 2px rgba(0, 0, 0, 0.1)",
                            },
                        ),
                        html.Label("Select Y-axis Column:", className="form-label"),
                        dcc.Dropdown(
                            id="y-axis-column",
                            options=[],  # Will be dynamically populated
                            placeholder="Select Y-axis column",
                            className="mb-3",
                            style={
                                "width": "100%",
                                "padding": "5px",
                                "borderRadius": "5px",
                                "border": "1px solid #ced4da",
                                "boxShadow": "0px 1px 2px rgba(0, 0, 0, 0.1)",
                            },
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
            ]
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Close", id="close-upload-modal", className="ms-auto", n_clicks=0
            )
        ),
    ],
    id="upload-modal",
    is_open=False,
)
