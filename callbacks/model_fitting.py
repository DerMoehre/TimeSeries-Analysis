from dash import Input, Output, State, callback_context
import pandas as pd
import base64, io
from dash import html, dcc
import csv
import plotly.express as px
from layouts.main_content import main_content
import dash_bootstrap_components as dbc


def register_callbacks(app):
    @app.callback(
        Output("model-fitting-graph", "figure"),
        [Input("uploaded-data-store", "data"), Input("model-data-store", "data")],
    )
    def initialize_graph(uploaded_data, model_data):
        if not uploaded_data:
            return {}  # Return an empty graph if no data is uploaded

        df = pd.DataFrame(uploaded_data)

        # Plot the uploaded data
        fig = px.line(df, x=df.columns[0], y=df.columns[1], title="Uploaded Data")

        # Overlay model data if available
        if model_data:
            for model_line in model_data:
                fig.add_scatter(
                    x=model_line["x"],
                    y=model_line["y"],
                    mode="lines",
                    name=model_line.get("name", "Model Prediction"),
                )

        return fig
