
import os
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, callback, Output, Input
from Constants import style_header1, style_text_bottom, style_drop_label

import datetime
import pytz

import plotly.express as px

from services.general import P1, P2, P3, AZUL, VERDE, GRIS
from services.informe_online_data import get_data_frame_online_report


def create_timeline_plot(df, titulo, color):
    fig = px.line(df,
                  x='fecha_despacho',
                  y='volumen_total',
                  title=f" {titulo} ",
                  markers=True,
                  color_discrete_sequence=[color],
                  labels={"volumen_total": "Volumen Total", "fecha_despacho": "Fecha"}
                  )
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Volumen Total (gal)"
    )
    return fig


DATA_DIR_INF_ONLINE = 'data/informe_online'
os.makedirs(DATA_DIR_INF_ONLINE, exist_ok=True)
CORRIENTE_ION_FPATH = os.path.join(DATA_DIR_INF_ONLINE, 'or_corriente.csv')
ACPM_ION_FPATH = os.path.join(DATA_DIR_INF_ONLINE, 'or_acpm.csv')
EXTRA_ION_FPATH = os.path.join(DATA_DIR_INF_ONLINE, 'or_extra.csv')


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
            html.P("Se muestra el despacho de combustible, a nivel nacional dia por dia, "
                   "dentro de una ventana de 60 dias de acuerdo a la informacion "
                   "reportada por el cubo de SICOM. Solo se tienen en cuenta los agentes: "
                   "COMERCIALIZADOR INDUSTRIAL, ESTACION DE SERVICIO AUTOMOTRIZ y ESTACION DE SERVICIO FLUVIAL"
                   ".Las cifras se actualizan cada 15 minutos. (LA PAGINA PODRIA TOMAR VARIOS SEGUNDOS ANTES DE CARGAR COMPLETAMENTE)", style=style_text_bottom)
        ], width=12)
    ], style={'padding': '2em'}),


    dbc.Row([
        dbc.Col([
            html.P("Actualizado última vez: "),
            html.Span(id='last-update-label', style=style_drop_label),
        ], width=12)
    ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([dcc.Graph(id='corriente-60win')], width=12),
        dbc.Col([html.Button("Download Corriente CSV", id='btn-csv-corriente'),
                 dcc.Download(id="download-csv-corriente")], width=12)
    ], style={}),

    dbc.Row([
        dbc.Col([dcc.Graph(id='acpm-60win')], width=12),
        dbc.Col([html.Button("Download ACPM CSV", id='btn-csv-acpm'),
                 dcc.Download(id="download-csv-acpm")], width=12)
    ], style={}),

    dbc.Row([
        dbc.Col([dcc.Graph(id='extra-60win')], width=12),
        dbc.Col([html.Button("Download Extra CSV", id='btn-csv-extra'),
                 dcc.Download(id="download-csv-extra")], width=12)
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

    df = get_data_frame_online_report()  # Function that fetches/updates the DataFrame

    df['fecha_despacho'] = pd.to_datetime(df['fecha_despacho'], format='%Y-%m-%d')
    df['volumen_total'] = df['volumen_total'].astype(float)

    df_corriente = df[df['producto'] == P1].copy()
    df_acpm = df[df['producto'] == P2].copy()
    df_extra = df[df['producto'] == P3].copy()

    fig1 = create_timeline_plot(df_corriente, 'Corriente', color=VERDE)
    fig2 = create_timeline_plot(df_acpm, 'ACPM', color=AZUL)
    fig3 = create_timeline_plot(df_extra, 'Extra', color=GRIS)

    tz = pytz.timezone('America/Bogota')
    now = datetime.datetime.now(tz)
    last_updated = now.strftime('fecha:  %Y-%m-%d    hora:  %H:%M:%S')

    df_corriente.to_csv(CORRIENTE_ION_FPATH, index=False)
    df_acpm.to_csv(ACPM_ION_FPATH, index=False)
    df_extra.to_csv(EXTRA_ION_FPATH, index=False)

    return fig1, fig2, fig3, last_updated, #intervalo


@callback(
    Output('download-csv-corriente', 'data'),
    Input('btn-csv-corriente', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv_corriente(n_clicks):
    #df = methods.getDataFrame_OnlineReport()  # Function that fetches/updates the DataFrame
    df = pd.read_csv(CORRIENTE_ION_FPATH)
    df['fecha_despacho'] = pd.to_datetime(df['fecha_despacho'], format='%Y-%m-%d')
    df['volumen_total'] = df['volumen_total'].astype(float)
    df_corriente = df[df['producto'] == P1].copy()
    return dcc.send_data_frame(df_corriente.to_csv, "corriente.csv")


@callback(
    Output('download-csv-acpm', 'data'),
    Input('btn-csv-acpm', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv_acpm(n_clicks):
    #df = methods.getDataFrame_OnlineReport()  # Function that fetches/updates the DataFrame
    df = pd.read_csv(ACPM_ION_FPATH)
    df['fecha_despacho'] = pd.to_datetime(df['fecha_despacho'], format='%Y-%m-%d')
    df['volumen_total'] = df['volumen_total'].astype(float)
    df_acpm = df[df['producto'] == P2].copy()
    return dcc.send_data_frame(df_acpm.to_csv, "acpm.csv")

@callback(
    Output('download-csv-extra', 'data'),
    Input('btn-csv-extra', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv_extra(n_clicks):
    #df = methods.getDataFrame_OnlineReport()  # Function that fetches/updates the DataFrame
    df = pd.read_csv(EXTRA_ION_FPATH)
    df['fecha_despacho'] = pd.to_datetime(df['fecha_despacho'], format='%Y-%m-%d')
    df['volumen_total'] = df['volumen_total'].astype(float)
    df_extra = df[df['producto'] == P3].copy()
    return dcc.send_data_frame(df_extra.to_csv, "extra.csv")


