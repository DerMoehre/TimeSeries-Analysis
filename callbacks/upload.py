from dash import Input, Output, State, callback_context
import pandas as pd
import base64, io
from io import StringIO
from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc  # Import dbc for layout components

def process_data(df):
    """Helper function to generate content from a DataFrame."""
    # Generate graph
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
    
    # Combine content
    content = html.Div([
        dcc.Graph(figure=fig),
        dbc.Row([
            dbc.Col([
                html.H4("Data Description"),
                description_table,
            ], className="table-column"),
            dbc.Col([
                html.H4("Data Overview"),
                overview_table_scrollable,
            ], className="table-column"),
        ]),
    ])
    return content

def register_callbacks(app):
    @app.callback(
        [
            Output("main-content", "children"),
            Output("upload-modal", "is_open"),
            Output("upload-status", "children"),
            Output("uploaded-data-store", "data"),
        ],
        [
            Input("url", "pathname"),
            Input("open-upload-modal", "n_clicks"),
            Input("close-upload-modal", "n_clicks"),
            Input("upload-data", "contents"),
            Input('delete-data-button', 'n_clicks'),
            Input("uploaded-data-store", "data"),
        ],
        [
            State("upload-modal", "is_open"),
            State("upload-data", "filename"),
        ],
    )
    def handle_content_and_upload(pathname, open_clicks, close_clicks, file_contents, delete_clicks, stored_data, is_open, filename):
        ctx = callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if delete_clicks is None:
            delete_clicks = 0

        # Handle page navigation
        if triggered_id == "url":
            if pathname == "/forecast":
                return html.Div("Forecast page coming soon!"), is_open, "", None
            elif pathname == "/results":
                return html.Div("Results page coming soon!"), is_open, "", None
            else:
                return html.H3("Welcome to the Murtfeldt TimeSeries Analysis Dashboard!"), is_open, "", None

        # Handle modal toggle
        if triggered_id in ["open-upload-modal", "close-upload-modal"]:
            is_open = not is_open

        # Clear uploaded data
        if delete_clicks > 0:
            return html.H3("Welcome to the Murtfeldt TimeSeries Analysis Dashboard!"), is_open, "Uploaded data deleted", None

        # Handle stored or uploaded data
        if stored_data or file_contents:
            # Only process file_contents if it is valid (not an integer or None)
            if isinstance(file_contents, str):
                content_type, content_string = file_contents.split(",")
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
                stored_data = df.to_json(date_format="iso", orient="split")
            else:
                # If file_contents is not a valid string, load data from session storage
                df = pd.read_json(StringIO(stored_data), orient="split")
            
            content = process_data(df)
            message = f"File {filename} uploaded successfully!" if file_contents else "Data loaded from session storage"
            return content, is_open, message, stored_data

        # Default response
        return html.H3("Welcome to the Murtfeldt TimeSeries Analysis Dashboard!"), is_open, "", None
