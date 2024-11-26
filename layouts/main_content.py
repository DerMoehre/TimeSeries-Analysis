from dash import html, dcc
from layouts.modal import modal_layout

main_content = html.Div(
    [
        modal_layout,
        dcc.Store(id='uploaded-data-store', storage_type='session'),
        html.Div(id="main-content", className='main-content'),
    ],
    className='main-container',
)