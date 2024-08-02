
import dash
from dash import dcc, html, dash_table, callback, Output, Input
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import pickle
from os.path import exists

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
                html.P("Parrafo pagina precios referencia", style=style_text_bottom)
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

], fluid=True)



@callback(
    [
        Output('corriente-precios-table', 'data'),
        Output('corriente-precios-table', 'columns'),
        Output('corriente-precios-table', 'style_data_conditional'),
        Output('acpm-precios-table', 'data'),
        Output('acpm-precios-table', 'columns'),
        Output('acpm-precios-table', 'style_data_conditional')
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
    return corriente_data, t_columns, style_data_conditional, acpm_data, t_columns, style_data_conditional


