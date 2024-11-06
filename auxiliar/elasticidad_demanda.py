import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback, Output, Input
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

import seaborn as sns
import statsmodels.api as sm

import Constants
from Constants import style_header1, style_text_bottom, style_drop_label
import Elasticidad_Methods as em

df = em.load_demanda_df_time_series()
lista_lugares = df['ciudad'].unique().tolist()

#dash.register_page(__name__)

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
            html.Label("Seleccionar Lugar:", htmlFor='lugar-dropdown', style=style_drop_label),
            dcc.Dropdown(
                id='lugar-dropdown',
                options=[{'label': value, 'value': value} for value in lista_lugares],
                value=lista_lugares[0],
                clearable=False
            )
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
    ], justify='left', align='center', style={'padding': '2em'}),

    # First Time Series Chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='elasticidad-corriente')
        ], width=12)
    ], style={'padding': '2em'}),

    # Second Time Series Chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='elasticidad-acpm')
        ], width=12)
    ], style={'padding': '2em'}),

], fluid=True)



def create_regression_plot(x, y, model, title):
    # Create a scatter plot with regression line
    fig = go.Figure()

    # Scatter plot
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='Datos'
    ))

    # Regression line
    x_vals = np.linspace(x.min(), x.max(), 100)
    X_vals = sm.add_constant(x_vals)
    y_predicted = model.predict(X_vals)

    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_predicted,
        mode='lines',
        name='Línea de Regresión'
    ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Log Precio',
        yaxis_title='Log Volumen',
        template='plotly_white'
    )

    return fig




@callback(
    [Output('elasticidad-corriente', 'figure'),
     Output('elasticidad-acpm', 'figure')],
    [Input('lugar-dropdown', 'value')]
)
def update_time_series(selected_lugar):
    # Filter the dataframe based on the selected place
    df_ciudad = df[df['ciudad'] == selected_lugar].copy()

    df_ciudad['log_volumen_corriente'] = np.log(df_ciudad['vol_corriente'])
    df_ciudad['log_precio_corriente'] = np.log(df_ciudad['precio_corriente'])

    df_ciudad['log_volumen_acpm'] = np.log(df_ciudad['vol_acpm'])
    df_ciudad['log_precio_acpm'] = np.log(df_ciudad['precio_acpm'])

    # Prepare the data for the linear model
    X_corriente = sm.add_constant(df_ciudad['log_precio_corriente'])  # Adds a constant term to the predictor
    y_corriente = df_ciudad['log_volumen_corriente']

    # Fit the linear model
    modelo_corriente = sm.OLS(y_corriente, X_corriente).fit()

    # Prepare the data for the linear model
    X_acpm = sm.add_constant(df_ciudad['log_precio_acpm'])  # Adds a constant term to the predictor
    y_acpm = df_ciudad['log_volumen_acpm']

    # Fit the linear model
    modelo_acpm = sm.OLS(y_acpm, X_acpm).fit()

    # Create the scatter plots with regression lines
    fig1 = create_regression_plot(
        x=df_ciudad['log_precio_corriente'],
        y=df_ciudad['log_volumen_corriente'],
        model=modelo_corriente,
        title='Elasticidad de Demanda - Corriente'
    )

    fig2 = create_regression_plot(
        x=df_ciudad['log_precio_acpm'],
        y=df_ciudad['log_volumen_acpm'],
        model=modelo_acpm,
        title='Elasticidad de Demanda - ACPM'
    )

    return fig1, fig2



