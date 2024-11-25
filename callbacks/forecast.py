from dash.dependencies import Input, Output
from models.forecast_models import get_forecast
from utils.plot_helper import create_forecast_plot

def register_callbacks(app):
    @app.callback(
        Output("forecast-plot", "figure"),
        [Input("model-select", "value"),
         Input("uploaded-data", "data")]
    )
    def update_forecast(selected_model, uploaded_data):
        if not uploaded_data:
            return {}
        
        # Convert uploaded data to DataFrame
        data = pd.DataFrame(uploaded_data)

        # Use the selected Nixtla model for forecasting
        forecast_data = get_forecast(selected_model, data)
        
        # Plot the forecast
        return create_forecast_plot(data, forecast_data)