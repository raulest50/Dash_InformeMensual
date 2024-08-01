import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

import Constants

# Initialize the Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap",
    dbc.icons.BOOTSTRAP,  # para usar bootstrap icons
], suppress_callback_exceptions=True, use_pages=True)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Link(f"{page['name']}", href=page["relative_path"], style=Constants.style_navbar_link)
            ), style=Constants.style_navbar_col, width=6) for page in dash.page_registry.values()
        ], style=Constants.style_navbar),
    ]),
    dash.page_container
])


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True, dev_tools_ui=False)
    #app.run_server(debug=True)


# supress error callback in production
# https://stackoverflow.com/questions/59568510/dash-suppress-callback-exceptions-not-working/59569568#59569568
# https://stackoverflow.com/questions/59568510/dash-suppress-callback-exceptions-not-working

