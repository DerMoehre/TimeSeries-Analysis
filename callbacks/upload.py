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
    return html.Div([
        dcc.Graph(figure=fig),
        dbc.Row([
            dbc.Col(description_table, width=6),  # Description table on the left
            dbc.Col(overview_table_scrollable, width=6),  # Overview table on the right
        ])
    ])

def register_callbacks(app):
    # Callback to handle the file upload and update the main content
    @app.callback(
        Output("main-content", "children"),
        [Input("url", "pathname"),
         Input("upload-data", "contents")],
        [State("upload-data", "filename")]
    )
    def update_main_content(pathname, contents, filename=None):
        if contents is None or contents == "":
            return html.Div("No file uploaded yet.")

        # Check if contents has the expected format
        if ',' not in contents:
            return html.Div("Invalid file format.")

        content_type, content_string = contents.split(',', 1)  # Split into two parts (max 1 split)

        try:
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return process_data(df)
        except Exception as e:
            return html.Div(f"Error processing the file: {str(e)}")

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
