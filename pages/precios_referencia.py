
import dash
import pandas as pd
from dash import dcc, html, dash_table, callback, Output, Input
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import Constants

import pickle
from os.path import exists

import plotly.express as px

from Constants import style_header1, style_text_bottom, style_drop_label, style_header4,\
style_cell, style_header, style_data, style_table

from methods import scrape_url_list, get_data_frames_from_excel_url

import numpy as np



lista_informes_tuple = scrape_url_list()
# Create the options for the lista informes dropdown
lista_informes = [{'label': item[0], 'value': item[0]} for item in lista_informes_tuple]

def get_dataframes_dict(lista_informes):
    r = {}
    for name, url in lista_informes_tuple:
        r[name] = [get_data_frames_from_excel_url(url)]
    return r


fname_df_dict = 'df_dictionary.pkl'
if not exists(fname_df_dict):
    df_dictionary = get_dataframes_dict(lista_informes)
    with open(fname_df_dict, 'wb') as file:
        pickle.dump(df_dictionary, file)
else:
    with open(fname_df_dict, 'rb') as file:
        df_dictionary = pickle.load(file)

columnas_ciudades = df_dictionary[lista_informes[0]['value']][0][0].columns[1:]



lista_informes_tuple = scrape_url_list()
# Create the options for the lista informes dropdown
lista_informes = [{'label': item[0], 'value': item[0]} for item in lista_informes_tuple]

def get_dataframes_dict(lista_informes):
    r = {}
    for name, url in lista_informes_tuple:
        r[name] = [get_data_frames_from_excel_url(url)]
    return r

fname_df_dict = 'df_dictionary.pkl'
if not exists(fname_df_dict):
    df_dictionary = get_dataframes_dict(lista_informes)
    with open(fname_df_dict, 'wb') as file:
        pickle.dump(df_dictionary, file)
else:
    with open(fname_df_dict, 'rb') as file:
        df_dictionary = pickle.load(file)

columnas_ciudades = df_dictionary[lista_informes[0]['value']][0][0].columns[1:]


dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
                html.H1(" Precios de Referencia Combustibles Liquidos ", style=style_header1)
            ], width=9, xl=9, lg=9, md=6, sm=6, xs=4, className='text-center', style={'textAlign': 'center'}),
            dbc.Col([
                html.Img(src='../assets/logoComce-Soldicom.png', style={'width': '100%', 'height': 'auto'}),
            ], width=3, xl=3, lg=3, md=6, sm=6, xs=12),
        ], justify='center', align='center', style={'padding': '2em'}),

    dbc.Row([
            dbc.Col([
                html.P("A continuación puede consultar la estructura de precios de referencia de la UPME para las principales ciudades del país:", style=style_text_bottom)
            ], width=12)
        ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
                html.Label("Seleccionar Mes Informe:", style=style_drop_label),  # Add label
                dcc.Dropdown(
                    id='mes-informe-dropdown',
                    options=lista_informes,
                    value=lista_informes[0]['value'],  # Default selected month
                    clearable=False
                )
            ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
                html.Label("Seleccionar Ciudad:", style=style_drop_label),  # Add label
                dcc.Dropdown(
                    id='ciudad-dropdown',
                    options=columnas_ciudades, # en [0] esta la palabra "ciudad" entonces se omite, lista empieza desde 1 (barranquilla)
                    value=columnas_ciudades[0],  # Default selected ciudad
                    clearable=False
                )
            ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),

        dbc.Col([
                html.Div(),
                ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        ], justify='left', align='center', style={'padding': '2em'}
    ),


    dbc.Row([
        dbc.Col([
            html.H4("Precios de Referencia - Corriente", style=style_header4),
            dash_table.DataTable(id='corriente-precios-table',
                                 style_cell=style_cell, style_header=style_header, style_data=style_data, style_table=style_table,
                                 )
        ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),
        dbc.Col([
            html.H4("Precios de Referencia - ACPM", style=style_header4),
            dash_table.DataTable(id='acpm-precios-table',
                                 style_cell=style_cell, style_header=style_header, style_data=style_data, style_table=style_table,
                                 )
        ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),],
        style={'padding': '2em'}
    ),


    dbc.Row([
            dbc.Col([
                html.H4("Tabla Agregada - Corriente", style=style_header4),
                dash_table.DataTable(id='corriente-aggr-table',
                                     style_cell=style_cell, style_header=style_header, style_data=style_data, style_table=style_table,
                                     )
            ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),
            dbc.Col([
                        dcc.Graph(id='pie-chart')
                    ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),
            ],
            style={'padding': '2em'}
        ),


    dbc.Row([
            dbc.Col([
                html.P("Elaborado por la Coordinación de Regulación y Análisis del Sector con datos de la Unidad de Planeación Minero Energética (UPME)", style=style_text_bottom)
            ], width=12)
    ], style={'padding': '2em'}),


    dbc.Row([
            dbc.Col([
                html.P("Raul Esteban Alzate", style=style_text_bottom),
                html.P(Constants.correo_esteban, style=style_text_bottom),
                html.P(Constants.cel_esteban, style=style_text_bottom),
            ], width=6),
            dbc.Col([
                    html.P("Juan David Bonilla", style=style_text_bottom),
                    html.P(Constants.correo_juan, style=style_text_bottom),
                    html.P(Constants.cel_juan, style=style_text_bottom),
            ], width=6)
        ], style={'padding': '2em'}),

], fluid=True)


def sum_cells_dt_frame(df, row_indices):
    # Ensure the DataFrame's second column is numeric
    ciudad_name = df.columns[1]
    df[ciudad_name] = pd.to_numeric(df[ciudad_name], errors='coerce')
    # Select the rows based on the given indices and sum the values in the second column
    selected_sum = df.iloc[row_indices, 1].sum()
    return selected_sum



@callback(
    [
        Output('corriente-precios-table', 'data'),
        Output('corriente-precios-table', 'columns'),
        Output('corriente-precios-table', 'style_data_conditional'),
        Output('acpm-precios-table', 'data'),
        Output('acpm-precios-table', 'columns'),
        Output('acpm-precios-table', 'style_data_conditional'),
        Output('corriente-aggr-table', 'data'),
        Output('corriente-aggr-table', 'columns'),
        Output('corriente-aggr-table', 'style_data_conditional'),
        Output('pie-chart', 'figure')
    ],
    [
        Input('mes-informe-dropdown', 'value'),
        Input('ciudad-dropdown', 'value')
    ]
)
def update_precios_ref(informe_name, ciudad_name):

    df_precios_corriente, df_precios_acpm = df_dictionary[informe_name][0]
    df_precios_table_corriente = df_precios_corriente[['CIUDAD', ciudad_name]].copy()
    df_precios_table_acpm = df_precios_acpm[['CIUDAD', ciudad_name]].copy()

    df_precios_table_corriente.iloc[0, 1] = f"{df_precios_table_corriente.iloc[0, 1] * 100:.2f} %"
    df_precios_table_acpm.iloc[0, 1] = f"{df_precios_table_acpm.iloc[0, 1] * 100:.2f} %"

    df_precios_table_corriente[ciudad_name] = df_precios_table_corriente[ciudad_name].apply(
        lambda x: f"{x:.2f}" if isinstance(x, (int, float)) and not np.isnan(x) else x
    )

    df_precios_table_acpm[ciudad_name] = df_precios_table_acpm[ciudad_name].apply(
        lambda x: f"{x:.2f}" if isinstance(x, (int, float)) and not np.isnan(x) else x
    )

    acpm_data = df_precios_table_acpm.to_dict('records')
    corriente_data = df_precios_table_corriente.to_dict('records')

    style_data_conditional = [
        {
            'if': {
                'filter_query': '{CIUDAD} = "PORCENTAJE DE MEZCLA POR CIUDAD" || {CIUDAD} = "INGRESO AL PRODUCTOR " || {CIUDAD} = "PRECIO MAXIMO DE VENTA DISTRIBUIDOR MAYORISTA" || {CIUDAD} = "PRECIO MAXIMO DE VENTA PLANTA DE ABASTO" || {CIUDAD} = "PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA"'
            },
            'fontWeight': 'bold',
            'backgroundColor': 'rgb(232, 232, 232)',
        }
    ]

    t_columns = [
        {"name": "CIUDAD", "id": "CIUDAD"},
        {"name": ciudad_name, "id": ciudad_name},
    ]

    data = {
        'CIUDAD': ["INGRESO AL PRODUCTOR", "CARGA IMPOSITIVA", "TRANSPORTE", "MARGEN MAYORISTA", "MARGEN MINORISTA", "OTROS COSTOS", "PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA"],
        ciudad_name:
            [
                df_precios_table_corriente.iloc[1, 1],
                sum_cells_dt_frame(df_precios_table_corriente, [2, 3, 4, 11, 12]),
                sum_cells_dt_frame(df_precios_table_corriente, [6, 7, 16]),
                df_precios_table_corriente.iloc[10, 1],
                df_precios_table_corriente.iloc[14, 1],
                sum_cells_dt_frame(df_precios_table_corriente, [5, 15]),
                df_precios_table_corriente.iloc[17, 1],
            ]
    }


    df_aggr_corriente = pd.DataFrame(data=data, columns=['CIUDAD', ciudad_name])

    df_aggr_corriente[ciudad_name] = df_aggr_corriente[ciudad_name].apply(
        lambda x: f"{x:.2f}" if isinstance(x, (int, float)) and not np.isnan(x) else x
    )

    aggr_table_data = df_aggr_corriente.to_dict('records')

    style_data_conditional_aggr = [
        {
            'if': {
                'filter_query': '{CIUDAD} = "INGRESO AL PRODUCTOR" || {CIUDAD} = "PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA"'
            },
            'fontWeight': 'bold',
            'backgroundColor': 'rgb(232, 232, 232)',
        }
    ]


    fig = px.pie(df_aggr_corriente[:-1], names='CIUDAD', values=ciudad_name, title=f'PRECIOS DE REFERENCIA {ciudad_name}')

    return corriente_data, t_columns, style_data_conditional, acpm_data, t_columns, style_data_conditional, aggr_table_data, t_columns, style_data_conditional_aggr, fig


