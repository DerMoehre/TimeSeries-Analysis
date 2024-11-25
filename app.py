from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
from layouts.sidebar import sidebar_layout
from layouts.main_content import main_content
from layouts.model_fitting import model_fitting_layout
from layouts.upload import upload_layout
from callbacks import register_callbacks

# Initialize app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
app.title = "Murtfeldt TimeSeries Analysis"

# Set app layout
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="uploaded-data-store", storage_type="session"),
    sidebar_layout,
    html.Div(id="dynamic-layout", className="dynamic-layout"),
    upload_layout,  # Upload layout remains in the main app layout
])

# Callback to update the layout dynamically based on the URL
#@app.callback(
#    Output("dynamic-layout", "children"),
#    Input("url", "pathname"),
#)
def update_layout(pathname):
    if pathname == "/model-fitting":
        return model_fitting_layout  # Render model fitting page
    elif pathname == "/":  # Default page
        return main_content
    else:
        return html.Div("404: Page not found.", className="error-page")  # Handle unknown URLs

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
