from dash import Input, Output, State, callback_context
import pandas as pd
import base64, io
from dash import html, dcc
import plotly.express as px
from layouts.main_content import main_content
import dash_bootstrap_components as dbc

def process_data(df):
    """Helper function to generate content from a DataFrame."""
    # Graph
    fig = px.line(df, x="Time", y="Revenue", title="Uploaded Data Plot")
    # Data description
    description = df.describe()
    description.insert(0, "Metric", description.index)
    description_table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in description.columns])),
        html.Tbody([
            html.Tr([html.Td(description.iloc[row][col]) for col in description.columns])
            for row in range(len(description))
        ])
    ])
    
    # Data overview
    overview_table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[row][col]) for col in df.columns])
            for row in range(len(df))
        ])
    ])

    # Scrollable overview table
    overview_table_scrollable = html.Div(
        overview_table,
        className="scrollable-overview-table",
    )

    # Return content
    return fig, description_table, overview_table_scrollable

def register_callbacks(app):
    @app.callback(
        [Output("overview-graph", "figure"),
         Output("description-table", "children"),
         Output("overview-table", "children")],
        Input("upload-data", "contents")
    )
    def update_overview(contents):
        if contents is None:
            return {}, "No data available", "No data available"

        content_type, content_string = contents.split(",", 1)
        decoded = base64.b64decode(content_string)
        
        try:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            fig, description_table, overview_table = process_data(df)
            return fig, description_table, overview_table
        except Exception as e:
            return {}, f"Error processing file: {str(e)}", "No data available"
    # Callback to toggle the modal's visibility when the "Upload Data" button is clicked
    @app.callback(
        Output("upload-modal", "is_open"),
        [Input("open-upload-modal", "n_clicks")],
        [State("upload-modal", "is_open")]
    )
    def toggle_modal(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
