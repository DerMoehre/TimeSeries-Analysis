from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, ETS, SeasonalNaive
import pandas as pd

# Placeholder: Replace with dynamic data handling
def get_forecast(model_name, data, freq='D', horizon=30):
    """
    Forecast using Nixtla's StatsForecast.

    Args:
        model_name (str): The selected model name.
        data (pd.DataFrame): DataFrame with `ds` (timestamps) and `y` (values).
        freq (str): Frequency of the data (e.g., 'D' for daily).
        horizon (int): Forecast horizon.

    Returns:
        pd.DataFrame: Forecasts with columns ['ds', 'y_hat'].
    """
    # Ensure data is in the required format
    data = data.rename(columns={'timestamp': 'ds', 'value': 'y'})

    # Initialize StatsForecast with the selected model
    if model_name == "autoarima":
        model = [AutoARIMA()]
    elif model_name == "ets":
        model = [ETS()]
    elif model_name == "seasonalnaive":
        model = [SeasonalNaive()]
    else:
        raise ValueError(f"Model {model_name} is not supported!")

    stats_forecast = StatsForecast(
        models=model,
        freq=freq
    )

    # Fit and forecast
    forecasts = stats_forecast.forecast(df=data, h=horizon)
    return forecasts.reset_index()