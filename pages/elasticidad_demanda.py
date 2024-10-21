
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback, Output, Input
from Constants import style_header1

dash.register_page(__name__)

layout = dbc.Container([
dbc.Row([
        dbc.Col([
            html.H1("Analisis Estadistico Elasticidad de la Demanda", style=style_header1)
        ], width=9, xl=9, lg=9, md=6, sm=6, xs=4, className='text-center', style={'textAlign': 'center'}),
        dbc.Col([
            html.Img(src='/assets/logoComce-Soldicom.png', style={'width': '100%', 'height': 'auto'}),
        ], width=3, xl=3, lg=3, md=6, sm=6, xs=12),
    ], justify='center', align='center', style={'padding': '2em'}),

], fluid=True)