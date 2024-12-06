from dash import Input, Output, State, callback_context
import pandas as pd
import base64, io
from dash import html, dcc
import csv
import plotly.graph_objects as go
import plotly.express as px
from layouts.main_content import main_content
import dash_bootstrap_components as dbc

from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, SeasonalNaive, HoltWinters, HistoricAverage


def check_upload_data(uploaded_data, title, slider_value):
    """Helper function to create a graph from uploaded data"""
    if not uploaded_data:
        return {}
    df = pd.DataFrame(uploaded_data)
    fig = px.line(df, x=df.columns[1], y=df.columns[2], title=title)

    slider_pos = add_vertical_line(slider_value, df)

    fig.add_shape(
        type="line",
        x0=slider_pos,
        x1=slider_pos,
        y0=df["y"].min(),
        y1=df["y"].max(),
        line=dict(color="red", width=2, dash="dash"),
        name="Slider Position",
    )
    return fig


def add_vertical_line(slider_value, df):
    """Compute x-axis position for the slider value"""
    slider_index = int(slider_value * len(df))  # Percentage-based position
    slider_x = df.iloc[slider_index]["ds"]
    return slider_x


def register_callbacks(app):
    @app.callback(
        Output("model-fitting-graph", "figure"),
        [
            Input("uploaded-data-store", "data"),
            Input("run-model-button", "n_clicks"),
            Input("model-fitting-slider", "value"),
        ],
        [
            State("model-fitting-dropdown", "value"),
            State("hyperparameter-table", "data"),
            State("transformed-data-store", "data"),
        ],
    )
    def update_graph(
        uploaded_data,
        run_button_clicks,
        slider_value,
        selected_model,
        hyperparameter_data,
        transformed_data,
    ):
        ctx = callback_context

        # Handle trigger determination
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # If triggered by uploaded data
        if trigger_id == "uploaded-data-store" or trigger_id != "run-model-button":
            return check_upload_data(transformed_data, "Uploaded Data", slider_value)

        # If triggered by the "Run Model" button
        if trigger_id == "run-model-button":
            if not transformed_data or not selected_model:
                return check_upload_data(
                    transformed_data, "No data or model selected", slider_value
                )

            # Transform data
            df = pd.DataFrame(transformed_data)
            if not all(col in df.columns for col in ["ds", "y", "unique_id"]):
                return check_upload_data(
                    transformed_data, "invalid data format", slider_value
                )

            # Extract frequency
            freq = next(
                (
                    row["value"]
                    for row in hyperparameter_data
                    if row["parameter"] == "freq"
                ),
                None,
            )
            if not freq:
                return check_upload_data(
                    transformed_data, "Frequency parameter is required", slider_value
                )

            # Extract seasonal_length
            season = next(
                (
                    row["value"]
                    for row in hyperparameter_data
                    if row["parameter"] == "season_length"
                ),
                None,
            )
            if not season:
                return check_upload_data(
                    transformed_data,
                    "Season length parameter is required",
                    slider_value,
                )

            # Select the model
            model_map = {
                "AutoARIMA": AutoARIMA(season_length=int(season)),
                "HoltWinters": HoltWinters(),
                "SeasonalNaive": SeasonalNaive(season_length=int(season)),
                "HistoricAverage": HistoricAverage(),
            }
            model = model_map.get(selected_model)
            if not model:
                return check_upload_data(
                    transformed_data, "invalid model selected", slider_value
                )

            # Fit model and forecast
            sf = StatsForecast(models=[model], freq=freq, n_jobs=-1)
            sf.fit(df=df)
            fitted_values = model.model_.fittedvalues

            # Combine original and fitted data for plotting
            df["Type"] = "Original"
            df_fitted = df.copy()
            df_fitted["y"] = fitted_values
            df_fitted["Type"] = "Fitted"
            combined_df = pd.concat([df, df_fitted])

            # Plot the fitted values
            fig = px.line(
                combined_df,
                x="ds",
                y="y",
                color="Type",
                title=f"Model: {selected_model} | Fitted Data",
            )

            return fig

        # Default empty graph
        check_upload_data(transformed_data, "Uploaded data", slider_value)
