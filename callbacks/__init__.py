from .upload import register_callbacks as register_upload_callbacks
from .model_fitting import register_callbacks as register_model_fitting_callbacks


def register_callbacks(app):
    register_upload_callbacks(app)
    register_model_fitting_callbacks(app)
