from dash import Input, Output, State, callback_context
import plotly.express as px
import pandas as pd


def check_upload_data(uploaded_data, title):
    """Helper function to create a graph from uploaded data"""
    if not uploaded_data:
        return {}
    df = pd.DataFrame(uploaded_data)
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title=title)

    return fig


def register_callbacks(app):
    @app.callback(
        Output("model-forecast-graph", "figure"),
        Input("run-forecast-button", "n_clicks"),
        State("uploaded-data-store", "data"),
        State("selected-model-store", "data"),
        # State("forecast-horizon", "data"),
        # prevent_initial_call=True,
    )
    def update_graph(run_button_clicks, uploaded_data, selected_model):
        ctx = callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle uploaded data display
        if trigger_id != "run-forecast-button":
            return check_upload_data(uploaded_data, "Uploaded Data")

        # Handle "Run Model" button trigger
        if trigger_id == "run-forecast-button":
            if not uploaded_data or not selected_model:
                return check_upload_data(uploaded_data, "No data or model selected")
