from dash import Input, Output, html, State, callback_context
from callbacks.upload import process_data
import pandas as pd
import io

def register_callbacks(app):
    @app.callback(
        Output("model-fitting-content", "children"),
        [
            Input("uploaded-data-store", "data"),
        ]
    )
    def render_model_fitting_content(stored_data):
        if stored_data:
            try:
                df = pd.read_json(io.StringIO(stored_data), orient="split")
                content = process_data(df)
                return content
            except Exception as e:
                return html.Div(f"Error processing stored data: {str(e)}")

        return html.H4("No data uploaded. Please upload data on the Upload page.")
