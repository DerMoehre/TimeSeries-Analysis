from .upload import register_callbacks as register_upload_callbacks
from .model_fitting import register_callbacks as register_model_fitting_callbacks

# from .sidebar import register_callbacks as register_sidebar_callbacks
from .forecast import register_callbacks as register_forecast_callbacks


def register_callbacks(app):
    register_upload_callbacks(app)
    register_model_fitting_callbacks(app)
    # register_sidebar_callbacks(app)
    register_forecast_callbacks(app)
