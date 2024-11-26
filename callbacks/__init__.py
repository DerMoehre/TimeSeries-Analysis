from .upload import register_callbacks as register_upload_callbacks

def register_callbacks(app):
    register_upload_callbacks(app)