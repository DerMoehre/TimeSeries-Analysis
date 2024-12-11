from dash import Input, Output, State, callback_context
import plotly.express as px
import pandas as pd

from .model_fitting import get_model

from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, SeasonalNaive, HoltWinters, HistoricAverage


def check_upload_data(uploaded_data, title):
    """Helper function to create a graph from uploaded data"""
    if not uploaded_data:
        return {}
    df = pd.DataFrame(uploaded_data)
    fig = px.line(df, x=df.columns[1], y=df.columns[2], title=title)

    return fig


def create_forecast_graph(forecast, original_data, selected_model):
    """Create a graph showing training, testing, and forecasted values."""

    # Base figure
    fig = px.line(
        original_data,
        x="ds",
        y="y",
        # color="Type",
        title=f"Forecasting Data with {selected_model}",
        labels={"ds": "Date", "y": "Value"},
    )

    fig.add_scatter(
        mode="lines",
        x=forecast["ds"],
        y=forecast[selected_model],
    )

    return fig


def forecast_data(data, model, parameter, horizon_data):
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    data = pd.DataFrame(data)

    if trigger_id == "run-forecast-button":
        # Extract horizon value from the forecast-horizon table
        horizon_value = next(
            (row["value"] for row in horizon_data if row["parameter"] == "length"),
            None,
        )
        if not horizon_value or not horizon_value.isdigit():
            raise ValueError("Invalid forecast horizon value")

        # Convert the horizon to an integer
        horizon = int(horizon_value)

        freq = parameter.get("freq")
        season = parameter.get("season_length")

        stats_model = get_model(model, season)

        sf = StatsForecast(models=[stats_model], freq=freq, n_jobs=-1)
        sf.fit(df=data)

        forecast_df = sf.forecast(h=horizon, df=data)

        return forecast_df


def register_callbacks(app):
    @app.callback(
        Output("model-forecast-graph", "figure"),
        Input("run-forecast-button", "n_clicks"),
        Input("hyperparameters-store", "data"),
        State("transformed-data-store", "data"),
        State("selected-model-store", "data"),
        State("forecast-horizon", "data"),
    )
    def update_graph(
        run_button_clicks,
        hyperparameter,
        transformed_data,
        selected_model,
        horizon_data,
    ):
        ctx = callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle uploaded data display
        if trigger_id != "run-forecast-button":
            return check_upload_data(transformed_data, "Uploaded Data")

        # Handle "Run Model" button trigger

        if trigger_id == "run-forecast-button":
            if not transformed_data or not selected_model or not horizon_data:
                return check_upload_data(transformed_data, "No data or model selected")
            forecast = forecast_data(
                transformed_data, selected_model, hyperparameter, horizon_data
            )

            return create_forecast_graph(forecast, transformed_data, selected_model)
