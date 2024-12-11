from dash import Input, Output, State, callback_context
import pandas as pd
import base64, io
from dash import html, dcc
import csv
import plotly.graph_objects as go
import plotly.express as px
from layouts.main_content import main_content
import dash_bootstrap_components as dbc

from sklearn.metrics import mean_absolute_error

from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, SeasonalNaive, HoltWinters, HistoricAverage


def split_data(df, slider_value):
    """Split the data into training and testing sets based on the slider value"""
    split_index = int(len(df) * slider_value)
    training_data = df.iloc[:split_index]
    testing_data = df.iloc[split_index:]
    return training_data, testing_data


def validate_model(model, training_data, testing_data, freq):
    """Fit the model to training data and validate it against testing data"""
    sf = StatsForecast(models=[model], freq=freq, n_jobs=-1)
    sf.fit(df=training_data)

    # Prepare a DataFrame for forecasting
    forecast_horizon = len(testing_data)
    forecast_df = sf.forecast(h=forecast_horizon, df=training_data)

    # Ensure column names align for consistency
    forecast_df = forecast_df.rename(columns={"y_hat": "y"})
    forecast_df["Type"] = "Predicted"

    # Add labels to training and testing data
    training_data["Type"] = "Training"
    testing_data["Type"] = "Testing"

    # Combine all data for visualization
    combined_df = pd.concat(
        [training_data, testing_data, forecast_df], ignore_index=True
    )

    return combined_df


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


def get_model(selected_model, season_length):
    """Retrieve the model based on the selected type and season length."""
    model_map = {
        "AutoARIMA": AutoARIMA(season_length=int(season_length)),
        "HoltWinters": HoltWinters(season_length=int(season_length)),
        "SeasonalNaive": SeasonalNaive(season_length=int(season_length)),
        "HistoricAverage": HistoricAverage(),
    }
    return model_map.get(selected_model)


def validate_input_data(transformed_data, required_columns):
    """Validate that the transformed data has the required columns."""
    df = pd.DataFrame(transformed_data)
    if not all(col in df.columns for col in required_columns):
        return None
    return df


def get_hyperparameter_value(hyperparameter_data):
    """Extract all hyperparameter values from the hyperparameter data."""
    return {row["parameter"]: row["value"] for row in hyperparameter_data}


def create_model_graph(
    slider_value,
    selected_model,
    hyperparameter_data,
    transformed_data,
):
    # Validate data
    df = validate_input_data(transformed_data, ["ds", "y", "unique_id"])
    if df is None:
        return check_upload_data(transformed_data, "Invalid data format", slider_value)
    # Extract hyperparameters
    hyperparameter = get_hyperparameter_value(hyperparameter_data)

    freq = hyperparameter.get("freq")
    season_length = hyperparameter.get("season_length")
    if not freq:
        return check_upload_data(
            transformed_data, "Frequency parameter is required", slider_value
        )
    if not season_length:
        return check_upload_data(
            transformed_data,
            "Season length parameter is required",
            slider_value,
        )
    # Select and fit the model
    model = get_model(selected_model, season_length)
    if not model:
        return check_upload_data(
            transformed_data, "Invalid model selected", slider_value
        )
    # Split data into training und testing sets
    training_data, testing_data = split_data(df, slider_value)

    # fit the model
    forecast = validate_model(model, training_data, testing_data, freq)
    # Create the graph with a slider
    return create_graph_with_slider(
        testing_data, forecast, slider_value, selected_model
    )


def create_graph_with_slider(testing_data, forecast_data, slider_value, selected_model):
    """Create a graph showing training, testing, and forecasted values."""

    # Separate the forecast data for clarity
    train_test_data = forecast_data[forecast_data["Type"].isin(["Training", "Testing"])]
    forecast_only_data = forecast_data[forecast_data["Type"] == "Predicted"]

    slider_x = add_vertical_line(slider_value, train_test_data)

    # Base figure: Training and testing data
    fig = px.line(
        train_test_data,
        x="ds",
        y="y",
        color="Type",
        title="Training, Testing, and Forecast",
        labels={"ds": "Date", "y": "Value"},
    )

    # Add vertical line for slider
    fig.add_shape(
        type="line",
        x0=slider_x,
        x1=slider_x,
        y0=min(train_test_data["y"].min(), forecast_only_data[selected_model].min()),
        y1=max(train_test_data["y"].max(), forecast_only_data[selected_model].max()),
        line=dict(color="red", width=2, dash="dash"),
    )

    # Add forecast line dynamically based on the selected model
    fig.add_scatter(
        mode="lines",
        x=forecast_only_data["ds"],
        y=forecast_only_data[selected_model],
    )

    return fig


def register_callbacks(app):
    @app.callback(
        Output("selected-model-store", "data"),
        Input("model-fitting-dropdown", "value"),
    )
    def save_selected_model(selected_model):
        return selected_model or None

    @app.callback(
        Output("hyperparameters-store", "data"),
        Input("hyperparameter-table", "data"),
    )
    def store_hyperparameter(hyperparameter_data):
        return get_hyperparameter_value(hyperparameter_data) or None

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
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle uploaded data display
        if trigger_id == "uploaded-data-store" or trigger_id != "run-model-button":
            return check_upload_data(transformed_data, "Uploaded Data", slider_value)

        # Handle "Run Model" button trigger
        if trigger_id == "run-model-button":
            if not transformed_data:
                return check_upload_data(
                    transformed_data, "No data uploaded", slider_value
                )
            if not selected_model:
                return check_upload_data(
                    transformed_data, "No model selected", slider_value
                )
            if not hyperparameter_data:
                return check_upload_data(
                    transformed_data, "No hyperparameters provided", slider_value
                )
            return create_model_graph(
                slider_value, selected_model, hyperparameter_data, transformed_data
            )
