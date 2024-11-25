from dash import html, dcc
from layouts.upload import upload_layout

model_fitting_layout = html.Div(
    [
        upload_layout,  # Reuse the upload layout for consistency
        dcc.Store(id='uploaded-data-store', storage_type='session'),
        html.Div(id="model-fitting-content", className='main-content'),
    ],
    className='main-container',
)
