from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
from layouts.sidebar import sidebar_layout
from layouts.main_content import main_content
from layouts.modal import modal_layout
from callbacks import register_callbacks

# Initialize app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)
app.title = "Murtfeldt TimeSeries Analysis"

# Set app layout
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="uploaded-data-store", storage_type="session"),
    dbc.Row([
        dbc.Col(sidebar_layout, width=2),  # Static sidebar
        dbc.Col(html.Div(id="main-content"), width=10),  # Dynamic main content
    ]),
    modal_layout
])

def update_layout(pathname):
    if pathname == "/model":
        return html.Div("404: Page not found.", className="error-page")  # Render model fitting page
    elif pathname == "/":  # Default page
        return main_content
    else:
        return html.Div("404: Page not found.", className="error-page")  # Handle unknown URLs

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
