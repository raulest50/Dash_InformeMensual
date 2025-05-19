import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from flask import request, abort
import Constants

# Importar memory_profiler y psutil solo en modo desarrollo
if os.environ.get('APP_ENV', 'development') == 'development':
    #import memory_profiler
    try:
        import psutil
    except ImportError:
        print("Warning: psutil module not found. Memory monitoring will be disabled.")
        psutil = None
    import time
    from dash.dependencies import Input, Output

# Determine the environment
ENV_APP_MODE = os.environ.get('APP_ENV', 'development')
ENV_PORT = os.environ.get('PORT', 8050)
DEBUG = os.environ.get('DEBUG', True)

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&display=swap",
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

# Componente de monitoreo de memoria (solo en desarrollo y si psutil está disponible)
memory_monitor = html.Div(id='memory-monitor', style={
    'position': 'fixed',
    'bottom': '10px',
    'left': '10px',
    'backgroundColor': 'rgba(65, 183, 92, 0.8)',  # Verde COMCE con transparencia
    'color': 'white',
    'padding': '10px',
    'borderRadius': '5px',
    'zIndex': '1000',
    'fontSize': '14px',
    'fontFamily': 'Plus Jakarta Sans',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
}) if ENV_APP_MODE == 'development' and 'psutil' in globals() and psutil is not None else None

# Layout definition
app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Link(f"{page['name']}", href=page["relative_path"], style=Constants.style_navbar_link, className="navbar-link")
                ), style=Constants.style_navbar_col, width=3
            ) for page in dash.page_registry.values()
        ], style=Constants.style_navbar, className="navbar-container"),
    ]),
    dash.page_container,
    # Añadir el monitor de memoria solo en desarrollo y si psutil está disponible
    memory_monitor,
    # Intervalo para actualizar el monitor de memoria (solo si psutil está disponible)
    dcc.Interval(
        id='memory-interval', 
        interval=2000, 
        disabled=ENV_APP_MODE != 'development' or 'psutil' not in globals() or psutil is None
    )  # Actualizar cada 2 segundos
])

# Callback para actualizar el monitor de memoria (solo en desarrollo)
if ENV_APP_MODE == 'development' and psutil is not None:
    @app.callback(
        Output('memory-monitor', 'children'),
        Input('memory-interval', 'n_intervals')
    )
    def update_memory_usage(n):
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()

        # Convertir a MB para mejor legibilidad
        rss_mb = memory_info.rss / (1024 * 1024)
        vms_mb = memory_info.vms / (1024 * 1024)

        return [
            html.Div([
                html.Strong("Monitoreo de Memoria"),
                html.Br(),
                f"RAM Física: {rss_mb:.2f} MB",
                html.Br(),
                f"RAM Virtual: {vms_mb:.2f} MB",
                html.Br(),
                f"Actualizado: {time.strftime('%H:%M:%S')}"
            ])
        ]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=ENV_PORT, debug=DEBUG)
