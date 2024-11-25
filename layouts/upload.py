from dash import html, dcc
import dash_bootstrap_components as dbc

upload_layout = dbc.Modal(
    [
        dbc.ModalHeader("Upload Data"),
        dbc.ModalBody(
            [
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and drop or click to upload a file"]),
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
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-upload-modal", className="ms-auto", n_clicks=0)
        ),
    ],
    id="upload-modal",
    is_open=False,
)