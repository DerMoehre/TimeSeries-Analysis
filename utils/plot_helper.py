import plotly.graph_objects as go

def create_forecast_plot(original_data, forecast_data):
    """
    Create a Plotly graph to visualize the original time series and the forecast.

    Args:
        original_data (pd.DataFrame): DataFrame with original `ds` and `y`.
        forecast_data (pd.DataFrame): DataFrame with forecast `ds` and `y_hat`.

    Returns:
        go.Figure: Plotly graph object.
    """
    fig = go.Figure()

    # Plot original data
    fig.add_trace(go.Scatter(
        x=original_data['ds'],
        y=original_data['y'],
        mode='lines',
        name='Original Data'
    ))

    # Plot forecast data
    fig.add_trace(go.Scatter(
        x=forecast_data['ds'],
        y=forecast_data['y_hat'],
        mode='lines',
        name='Forecast'
    ))

    fig.update_layout(
        title="Time Series Forecast",
        xaxis_title="Date",
        yaxis_title="Value",
        legend_title="Legend"
    )

    return fig