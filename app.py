import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import Constants

# Determine the environment
ENV_APP_MODE = os.environ.get('APP_ENV', 'development')
ENV_PORT = os.environ.get('PORT', 8050)

# Initialize the Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap",
    dbc.icons.BOOTSTRAP,
], suppress_callback_exceptions=True, use_pages=True)

# Set configuration based on the environment
if ENV_APP_MODE == 'production':
    app.config.suppress_callback_exceptions = False
    app.enable_dev_tools(debug=False)
else:
    app.config.suppress_callback_exceptions = True
    app.enable_dev_tools(debug=True)

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
    app.run(host='0.0.0.0', port=ENV_PORT)
