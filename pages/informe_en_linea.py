

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, dash_table, callback, Output, Input
from Constants import style_header1, style_text_bottom, style_drop_label, style_header4,\
style_cell, style_header, style_data, style_table

import datetime

import plotly.express as px

import methods


def create_timeline_plot(df, titulo, color):
    fig = px.line(df,
                  x='fecha_despacho',
                  y='volumen_total',
                  title=f" {titulo} ",
                  markers=True,
                  color_discrete_sequence=[color],
                  labels={"value": "Volumen Total", "variable": "Año"}
                  )
    return fig

dash.register_page(__name__)

layout = dbc.Container([


    dbc.Row([
        dbc.Col([
            html.H1(" Informe En Tiempo Real: Despacho Combustibles Liquidos ", style=style_header1)
        ], width=9, xl=9, lg=9, md=6, sm=6, xs=4, className='text-center', style={'textAlign': 'center'}),
        dbc.Col([
            html.Img(src='../assets/logoComce-Soldicom.png', style={'width': '100%', 'height': 'auto'}),
        ], width=3, xl=3, lg=3, md=6, sm=6, xs=12),
    ], justify='center', align='center', style={'padding': '2em'}),


    dbc.Row([
        dbc.Col([
            html.P("Se muestra el despacho de combustible a nivel nacional "
                   "dentro de una ventana de 60 dias de acuerdo a la informacion "
                   "reportada por el cubo de SICOM. Las cifras se actualizan cada hora.", style=style_text_bottom)
        ], width=12)
    ], style={'padding': '2em'}),


    dbc.Row([
        dbc.Col([
            html.P("Actualizado última vez: "),
            html.Span(id='last-update-label', style=style_drop_label),
        ], width=12)
    ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([dcc.Graph(id='corriente-60win')], width=12)
    ], style={}),

    dbc.Row([
        dbc.Col([dcc.Graph(id='acpm-60win')], width=12)
    ], style={}),

    dbc.Row([
        dbc.Col([dcc.Graph(id='extra-60win')], width=12)
    ], style={}),

    dcc.Interval(id='interval-component', interval=(3600/4)*1000, n_intervals=0)

], fluid=True)


@callback(
    Output('corriente-60win', 'figure'),
    Output('acpm-60win', 'figure'),
    Output('extra-60win', 'figure'),
    Output('last-update-label', 'children'),
    #Output('interval-component', 'interval'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):

    #print("Interval Update")
    # Load or update your DataFrame here
    df = methods.getDataFrame_OnlineReport()  # Function that fetches/updates the DataFrame

    df['fecha_despacho'] = pd.to_datetime(df['fecha_despacho'], format='%Y-%m-%d')
    df['volumen_total'] = df['volumen_total'].astype(float)

    #print(df)

    df_corriente = df[df['producto'] == methods.p1].copy()
    df_acpm = df[df['producto'] == methods.p2].copy()
    df_extra = df[df['producto'] == methods.p3].copy()

    fig1 = create_timeline_plot(df_corriente, 'Corriente', 'blue')
    fig2 = create_timeline_plot(df_acpm, 'ACPM', 'green')
    fig3 = create_timeline_plot(df_extra, 'Extra', 'gray')

    last_updated = datetime.datetime.now().strftime('fecha:  %Y-%m-%d    hora:  %H:%M:%S')

    #intervalo = (3600/4)*1000

    return fig1, fig2, fig3, last_updated, #intervalo


