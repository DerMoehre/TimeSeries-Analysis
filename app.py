from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from layouts.sidebar import sidebar_layout
from layouts.main_content import main_content
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
    sidebar_layout,
    main_content,
])

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)