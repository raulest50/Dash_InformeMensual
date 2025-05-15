import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from flask import request, abort
import Constants

# Determine the environment
ENV_APP_MODE = os.environ.get('APP_ENV', 'development')
ENV_PORT = os.environ.get('PORT', 8050)

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap",
        dbc.icons.BOOTSTRAP,
    ],
    suppress_callback_exceptions=True,
    use_pages=True
)

server = app.server  # expose the underlying Flask server

# 1. Block unwanted referers
@server.before_request
def block_specific_referer():
    referer = request.headers.get("Referer", "")
    if referer.startswith("https://fondosoldicom.com"):
        abort(403)

# 2. Add clickjacking protections
@server.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'self';"
    return response

# Set configuration based on the environment
if ENV_APP_MODE == 'production':
    app.config.suppress_callback_exceptions = False
    app.enable_dev_tools(debug=False)
else:
    app.config.suppress_callback_exceptions = True
    app.enable_dev_tools(debug=True)

# Layout definition
app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Link(f"{page['name']}", href=page["relative_path"], style=Constants.style_navbar_link)
                ), style=Constants.style_navbar_col, width=3
            ) for page in dash.page_registry.values()
        ], style=Constants.style_navbar),
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=ENV_PORT, debug=True)
