# summary_layout.py
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc

from Constants import style_header1, style_text_bottom, style_drop_label

from methods import scrape_url_list, get_data_frames_from_excel_url

lista_informes_tuple = scrape_url_list()
# Create the options for the lista informes dropdown
lista_informes = [{'label': item[0], 'value': item[0]} for item in lista_informes_tuple]

df_precios_corriente, df_precios_acpm = get_data_frames_from_excel_url(lista_informes_tuple[0][1])
# Display the DataFrame
print(df_precios_corriente)
df_precios_corriente.to_csv("corriente_precios.csv", index=False)

print(df_precios_acpm)
df_precios_acpm.to_csv("acpm_precios.csv", index=False)


precios_layout = dbc.Container([

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
                        id='geo-dropdown',
                        options=df_precios_corriente.columns[1:], # en [0] esta la palabra "ciudad" entonces se omite, lista empieza desde 1 (barranquilla)
                        value=df_precios_corriente.columns[1],  # Default selected ciudad
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
                dbc.Button("Regresar a Informe Mensual de Ventas", id="navigate-button", color="primary", href="/", style={'marginTop': '2em'})
            ], width=12, style={'textAlign': 'center'})
        ], style={'padding': '2em'}),

], fluid=True)

