
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback, Output, Input

import Constants
from Constants import style_header1, style_text_bottom, style_drop_label
import Elasticidad_Methods as em

df = em.load_demanda_df_time_series()
lista_lugares = df['ciudad'].unique().tolist()

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

    dbc.Row([
        dbc.Col([
            html.P("Analisis de la elasticidad de la demanda", style=style_text_bottom)
        ], width=12)
    ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
                html.Label("Seleccionar Mes:", htmlFor='month-dropdown', style=style_drop_label),  # Add label
                dcc.Dropdown(
                    id='lugar-dropdown',
                    options=[{'label':value, 'value':value} for value in lista_lugares],
                    value=lista_lugares[0],  # Default selected month
                    clearable=False
                )
            ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
    ], justify='left', align='center', style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([

        ])
    ])

], fluid=True)