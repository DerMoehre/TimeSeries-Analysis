from dash import Input, Output, State, callback_context
import pandas as pd
import base64, io
from dash import html, dcc
import csv
import plotly.express as px
from layouts.main_content import main_content
import dash_bootstrap_components as dbc


def detect_delimiter(data_string):
    """Detect the delimiter of a CSV file"""
    try:
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(data_string).delimiter
        return delimiter
    except Exception as e:
        return ","


def process_data(df, x_col=None, y_col=None):
    """Helper function to generate content from a DataFrame."""
    if not x_col or not y_col:
        return (
            {},
            html.Div("Please select columns for the X and Y axes."),
            "No data available",
        )

    # Generate the graph
    fig = px.line(df, x=x_col, y=y_col, title=f"Plot: {x_col} vs {y_col}")
    # Data description
    description = df.describe()
    description.insert(0, "Metric", description.index)
    description_table = html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in description.columns])),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(description.iloc[row][col])
                            for col in description.columns
                        ]
                    )
                    for row in range(len(description))
                ]
            ),
        ]
    )

    # Data overview
    overview_table = html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody(
                [
                    html.Tr([html.Td(df.iloc[row][col]) for col in df.columns])
                    for row in range(len(df))
                ]
            ),
        ]
    )

    # Scrollable overview table
    overview_table_scrollable = html.Div(
        overview_table,
        className="scrollable-overview-table",
    )

    # Return content
    return fig, description_table, overview_table_scrollable


def register_callbacks(app):
    @app.callback(
        [
            Output("x-axis-column", "options"),
            Output("y-axis-column", "options"),
            Output("upload-status", "children"),
        ],
        [Input("upload-data", "contents")],
    )
    def load_file(contents):
        if contents is None:
            return [], [], "No file uploaded."

        content_type, content_string = contents.split(",", 1)
        decoded = base64.b64decode(content_string)

        try:
            delimiter = detect_delimiter(decoded.decode("utf-8"))

            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=delimiter)

            # Store the uploaded data in a dcc.Store
            app.layout.children.append(
                dcc.Store(id="uploaded-data-store", data=df.to_dict("records"))
            )

            column_options = [{"label": col, "value": col} for col in df.columns]
            return column_options, column_options, f"Uploaded file with {len(df)} rows."
        except Exception as e:
            return [], [], f"Error reading file: {e}"

    @app.callback(
        [
            Output("overview-graph", "figure"),
            Output("description-table", "children"),
            Output("overview-table", "children"),
        ],
        [
            Input("x-axis-column", "value"),
            Input("y-axis-column", "value"),
            State("uploaded-data-store", "data"),
        ],
    )
    def update_graph(x_col, y_col, data):
        if data is None or not x_col or not y_col:
            return {}, "No data available", "No data available"

        df = pd.DataFrame(data)
        fig, description_table, overview_table = process_data(df, x_col, y_col)
        return fig, description_table, overview_table

    @app.callback(
        Output("upload-modal", "is_open"),
        [
            Input("open-upload-modal", "n_clicks"),
            Input("close-upload-modal", "n_clicks"),
        ],
        [State("upload-modal", "is_open")],
    )
    def toggle_modal(n_clicks_open, n_clicks_close, is_open):
        if n_clicks_open or n_clicks_close:
            return not is_open
        return is_open
