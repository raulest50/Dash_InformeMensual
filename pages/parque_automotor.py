import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import Constants
from Constants import style_header1, style_text_bottom, style_drop_label
from services.parque_automotor_data import PqMotorLoad

pml = PqMotorLoad()

dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Parque Automotor", style=style_header1)
        ], width=9, className='text-center'),
        dbc.Col([
            html.Img(src='../assets/logoComce-Soldicom.png', style={'width': '100%', 'height': 'auto'}),
        ], width=3),
    ], justify='center', align='center', style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            html.P("Crecimiento del parque automotor de acuerdo a los datos suministrados por el RUNT 2.0:", style=style_text_bottom)
        ], width=12)
    ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            html.Label("Seleccionar Tipo de Servicio:", style=style_drop_label),
            dcc.Dropdown(
                id='mes-informe-dropdown',
                options=pml.lista_servicios,
                value=pml.lista_servicios[0]['value'],  # Default selected value
                clearable=False
            ),
        ], width=4),
        dbc.Col([
            html.Label("Seleccionar Rango de Años:", style=style_drop_label),
            dcc.RangeSlider(
                id='year-range-slider',
                min=pml.min_year,
                max=pml.max_year,
                value=[pml.min_year, pml.max_year],
                marks={str(year): str(year) for year in range(pml.min_year, pml.max_year+1, 5)},
                step=1,
                allowCross=False
            ),
        ], width=8)
    ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='cantidad-timeseries')
        ], width=12)
    ]),

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

@callback(
    Output('cantidad-timeseries', 'figure'),
    Input('mes-informe-dropdown', 'value'),
    Input('year-range-slider', 'value')
)
def update_timeseries(nombre_servicio, year_range):
    df = pml.df.copy()
    # Filter by selected year range
    df = df[(df['fecha_de_registro'] >= year_range[0]) & (df['fecha_de_registro'] <= year_range[1])]

    if nombre_servicio == 'TODOS':
        df_grouped = df.groupby(['fecha_de_registro', 'nombre_servicio'])['cantidad'].sum().reset_index()
        df_grouped = df_grouped.sort_values('fecha_de_registro')
        fig = px.line(
            df_grouped,
            x='fecha_de_registro',
            y='cantidad',
            color='nombre_servicio',
            labels={
                'fecha_de_registro': 'Año de registro',
                'cantidad': 'Cantidad',
                'nombre_servicio': 'Nombre del servicio'
            },
            title='Cantidad por Año y Tipo de Servicio'
        )
    else:
        df_filtered = df[df['nombre_servicio'] == nombre_servicio]
        df_grouped = df_filtered.groupby('fecha_de_registro')['cantidad'].sum().reset_index()
        df_grouped = df_grouped.sort_values('fecha_de_registro')
        fig = px.line(
            df_grouped,
            x='fecha_de_registro',
            y='cantidad',
            labels={
                'fecha_de_registro': 'Año de registro',
                'cantidad': 'Cantidad'
            },
            title=f'Cantidad por Año para {nombre_servicio}'
        )

    fig.update_layout(
        xaxis_title='Año de registro',
        yaxis_title='Cantidad',
        legend_title='Nombre del servicio',
        hovermode='x'
    )
    return fig
