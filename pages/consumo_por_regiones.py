# Importaciones estándar
import dash
from dash import html, dcc, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

# Importaciones del proyecto
from Constants import style_data, style_cell, style_header, style_table, style_graph, \
    style_header1, style_header4, style_H3, style_text_bottom, style_H2, style_drop_label, verde, azul, gris, brand_colors
from dash.dependencies import Input, Output, State
from services.informe_mensual_data import InformeMensualLoad
from services.general import P1, P2, P3, AZUL, VERDE, GRIS

# Inicializar el cargador de datos
ims = InformeMensualLoad()

# Cargar GeoJSON para el mapa de Colombia
with open('colombiaMod.json', 'r', encoding='utf-8') as f:
    colombia_geojson = json.load(f)

# Obtener lista de departamentos únicos
df = ims.df
departamentos = sorted(df['departamento'].dropna().unique().tolist())

# Obtener lista de meses únicos
meses_disponibles = sorted(df['mes_despacho'].dropna().unique().tolist())

# Función para convertir número de mes a nombre
def get_mes_name(month_number):
    """Returns the Spanish name of the month given the month number (1-12)."""
    month_names = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    return month_names.get(month_number)

# Registro de la página en la aplicación
dash.register_page(__name__, path='/consumo-por-regiones', name='Consumo por Regiones')

# Layout principal de la página
layout = dbc.Container([
    # Cabecera de la página con título y logo en la misma fila
    dbc.Row([
        dbc.Col([
            html.H1("Consumo por Regiones", style=style_header1)
        ], width=9, xl=9, lg=9, md=6, sm=6, xs=4, className='text-center', style={'textAlign': 'center'}),
        dbc.Col([
            html.Img(src='/assets/logoComce.png', style={'width': '50%', 'height': '50%'}),
        ], width=3, xl=3, lg=3, md=6, sm=6, xs=12),
    ], justify='center', align='center', style={'padding': '2em'}),

    # Texto explicativo
    dbc.Row([
        dbc.Col([
            html.P(
                "Esta página permite discriminar el consumo de combustible por departamento en Colombia. "
                "Seleccione un departamento para visualizar su consumo histórico de combustibles.",
                style={
                    'textAlign': 'justify',
                    'fontFamily': "'Plus Jakarta Sans', sans-serif",
                    'fontSize': '20px',
                    'color': gris,
                    'marginBottom': '20px'
                }
            )
        ], width=12)
    ], style={'padding': '0 2em 2em 2em'}),

    # Selector de departamento y mapa
    dbc.Row([
        # Selector de departamento
        dbc.Col([
            html.Label("Seleccionar departamento:", htmlFor='departamento-input', style=style_drop_label),
            dbc.InputGroup([
                dbc.Input(
                    id='departamento-input',
                    type='text',
                    placeholder='Ingrese nombre del departamento',
                    value='',
                ),
                dbc.Button("Buscar", id="search-departamento-button", color="primary", className="ml-2"),
            ]),
            dcc.Dropdown(
                id='departamento-dropdown',
                options=[{'label': dept, 'value': dept} for dept in departamentos],
                placeholder="O seleccione un departamento",
                clearable=True
            ),
        ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),

        # Mapa de Colombia - Comentado temporalmente
        # dbc.Col([
        #     dcc.Graph(id='colombia-map', style=style_graph)
        # ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),
    ], style={'padding': '0 2em 2em 2em'}),

    # Selector de tipo de comparación
    dbc.Row([
        dbc.Col([
            html.Label("Tipo de comparación:", style=style_drop_label),
            dcc.RadioItems(
                id='comparison-type',
                options=[
                    {'label': ' Comparación interanual', 'value': 'interanual'},
                    {'label': ' Serie de tiempo mensual', 'value': 'serie_tiempo'}
                ],
                value='interanual',
                style={'fontFamily': "'Plus Jakarta Sans', sans-serif", 'fontSize': '18px'},
                inputStyle={"marginRight": "10px"},
                labelStyle={"marginRight": "20px"}
            ),
        ], width=12)
    ], style={'padding': '0 2em 2em 2em'}),

    # Selector de mes (solo visible cuando se selecciona comparación interanual)
    dbc.Row([
        dbc.Col([
            html.Label("Seleccionar mes para comparación interanual:", style=style_drop_label),
            dcc.Dropdown(
                id='month-selector',
                options=[{'label': get_mes_name(mes), 'value': mes} for mes in meses_disponibles],
                value=meses_disponibles[-1],  # Seleccionar el último mes disponible por defecto
                clearable=False
            ),
        ], width=6, xl=6, lg=6, md=12, sm=12, xs=12)
    ], id='month-selector-row', style={'padding': '0 2em 2em 2em', 'display': 'block'}),

    # Store para el departamento seleccionado
    dcc.Store(id='selected-departamento'),

    # Contenedor para gráficas y tablas (se actualizará dinámicamente)
    html.Div(id='graphs-tables-container')
], fluid=True, style={'padding': '20px'})

# Callback para actualizar la visibilidad del selector de mes
@callback(
    Output('month-selector-row', 'style'),
    Input('comparison-type', 'value')
)
def update_month_selector_visibility(comparison_type):
    if comparison_type == 'interanual':
        return {'padding': '0 2em 2em 2em', 'display': 'block'}
    else:
        return {'padding': '0 2em 2em 2em', 'display': 'none'}

# Callback para actualizar el departamento seleccionado
@callback(
    Output('selected-departamento', 'data'),
    [Input('search-departamento-button', 'n_clicks'),
     Input('departamento-dropdown', 'value')],
    [State('departamento-input', 'value')],
    prevent_initial_call=True
)
def update_selected_departamento(n_clicks, dropdown_value, input_value):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'search-departamento-button' and input_value:
        # Buscar departamento que coincida con el texto ingresado
        matching_depts = [dept for dept in departamentos if input_value.lower() in dept.lower()]
        if matching_depts:
            return matching_depts[0]
    elif trigger_id == 'departamento-dropdown' and dropdown_value:
        return dropdown_value

    return None

# Callback para actualizar el mapa de Colombia - Comentado temporalmente
# @callback(
#     Output('colombia-map', 'figure'),
#     Input('selected-departamento', 'data'),
# )
# def update_colombia_map(departamento_seleccionado):
#     # Crear una lista de nombres de departamentos desde el GeoJSON
#     dept_names = [feature['properties']['NAME_1'] for feature in colombia_geojson['features']]
# 
#     # Crear una lista de valores (0 para todos los departamentos excepto el seleccionado)
#     dept_values = [0] * len(dept_names)
# 
#     # Si hay un departamento seleccionado, asignarle un valor de 1
#     if departamento_seleccionado:
#         for i, dept in enumerate(dept_names):
#             if dept.lower() == departamento_seleccionado.lower():
#                 dept_values[i] = 1
# 
#     # Crear el mapa
#     fig = go.Figure(go.Choroplethmapbox(
#         geojson=colombia_geojson,
#         locations=dept_names,
#         z=dept_values,
#         featureidkey="properties.NAME_1",
#         colorscale=[[0, gris], [1, verde]],  # Gris para no seleccionados, verde para seleccionado
#         marker_opacity=0.7,
#         marker_line_width=1,
#         marker_line_color='white',
#         showscale=False,
#         hoverinfo='text',
#         hovertext=dept_names
#     ))
# 
#     # Actualizar el layout del mapa
#     fig.update_layout(
#         mapbox_style="carto-positron",
#         mapbox_zoom=4.5,
#         mapbox_center={"lat": 4.5709, "lon": -74.2973},
#         height=400,
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},
#     )
# 
#     return fig

# Callback para actualizar gráficas y tablas
@callback(
    Output('graphs-tables-container', 'children'),
    [Input('selected-departamento', 'data'),
     Input('comparison-type', 'value'),
     Input('month-selector', 'value')],
)
def update_graphs_and_tables(departamento_seleccionado, comparison_type, selected_month):
    if not departamento_seleccionado:
        return html.Div([
            html.P("Seleccione un departamento para visualizar los datos de consumo.",
                  style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '30px'})
        ])

    # Filtrar datos por departamento
    df = ims.df
    df_dept = df[df['departamento'] == departamento_seleccionado].copy()

    if df_dept.empty:
        return html.Div([
            html.P(f"No hay datos disponibles para el departamento {departamento_seleccionado}.",
                  style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '30px'})
        ])

    # Crear contenido según el tipo de comparación seleccionado
    if comparison_type == 'interanual':
        return create_interanual_content(df_dept, selected_month)
    else:  # serie_tiempo
        return create_serie_tiempo_content(df_dept)

def create_interanual_content(df_dept, selected_month):
    # Filtrar por el mes seleccionado para todos los años
    dfm = df_dept[df_dept['mes_despacho'] == selected_month].copy()

    # Agregar todos los municipios para obtener el total del departamento
    # Agrupar por año y producto, sumando los volúmenes
    dfm = dfm.groupby(['anio_despacho', 'mes_despacho', 'producto'])['volumen_total'].sum().reset_index()

    # Crear contenido con 3 gráficas y 3 tablas
    content = []

    # Título para la sección
    content.append(dbc.Row([
        dbc.Col([
            html.H3(f"Comparación interanual para el mes de {get_mes_name(selected_month)}", style=style_H3)
        ], width=12)
    ], style={'padding': '0 2em 1em 2em'}))

    # Crear fila para las gráficas
    graphs_row = dbc.Row([
        dbc.Col([
            dcc.Graph(figure=create_figure(dfm, P1, AZUL, "Gasolina Corriente"))
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            dcc.Graph(figure=create_figure(dfm, P2, VERDE, "ACPM"))
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            dcc.Graph(figure=create_figure(dfm, P3, GRIS, "Gasolina Extra"))
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
    ], style={'padding': '0 2em 2em 2em'})

    content.append(graphs_row)

    # Crear fila para las tablas
    tables_row = dbc.Row([
        dbc.Col([
            html.H4("Gasolina Corriente", style=style_header4),
            create_table(dfm, P1)
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            html.H4("ACPM", style=style_header4),
            create_table(dfm, P2)
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            html.H4("Gasolina Extra", style=style_header4),
            create_table(dfm, P3)
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
    ], style={'padding': '0 2em 2em 2em'})

    content.append(tables_row)

    return content

def create_serie_tiempo_content(df_dept):
    # Crear contenido con 3 gráficas y 3 tablas a pantalla completa
    content = []

    # Título para la sección
    content.append(dbc.Row([
        dbc.Col([
            html.H3("Serie de tiempo mensual", style=style_H3)
        ], width=12)
    ], style={'padding': '0 2em 1em 2em'}))

    # Preparar datos para serie de tiempo
    df_dept['fecha_despacho'] = pd.to_datetime(
        df_dept['anio_despacho'].astype(str) + '-' + df_dept['mes_despacho'].astype(str) + '-01')

    # Crear fila para las gráficas
    graphs_row = dbc.Row([
        dbc.Col([
            dcc.Graph(figure=create_figure_ts(df_dept, P1, AZUL, "Gasolina Corriente"))
        ], width=12),
        dbc.Col([
            dcc.Graph(figure=create_figure_ts(df_dept, P2, VERDE, "ACPM"))
        ], width=12),
        dbc.Col([
            dcc.Graph(figure=create_figure_ts(df_dept, P3, GRIS, "Gasolina Extra"))
        ], width=12),
    ], style={'padding': '0 2em 2em 2em'})

    content.append(graphs_row)

    # Crear fila para las tablas
    tables_row = dbc.Row([
        dbc.Col([
            html.H4("Gasolina Corriente", style=style_header4),
            create_table_ts(df_dept, P1)
        ], width=12),
        dbc.Col([
            html.H4("ACPM", style=style_header4),
            create_table_ts(df_dept, P2)
        ], width=12),
        dbc.Col([
            html.H4("Gasolina Extra", style=style_header4),
            create_table_ts(df_dept, P3)
        ], width=12),
    ], style={'padding': '0 2em 2em 2em'})

    content.append(tables_row)

    return content

def create_figure(dfm, producto, color, plegend):
    dfc = dfm[dfm['producto'] == producto].copy()
    dfc['volumen_total'] = dfc['volumen_total'].astype(float)
    dfc['anio_despacho'] = dfc['anio_despacho'].astype(int)

    # Convertir a millones de galones
    dfc['volumen_millones'] = dfc['volumen_total'] / 1000000

    # Crear la figura de Plotly
    fig = px.line(
        dfc,
        x='anio_despacho',
        y='volumen_millones',
        title=f"{plegend}",
        labels={"volumen_millones": "Millones de Galones", "anio_despacho": "Año"},
        markers=True,
        color_discrete_sequence=[color]
    )

    # Create a modified version of style_graph without the boxShadow property
    # boxShadow is not a valid property for plotly.graph_objs.Layout
    # style_graph contains: 'boxShadow': '0 2px 1px 0 rgba(0, 0, 0, 0.05), 0 3px 5px 0 rgba(0, 0, 0, 0.1)'
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Millones de Galones",
        # **style_graph  # Commented out due to boxShadow error
    )

    return fig

def create_figure_ts(df_dept, producto, color, plegend):
    dfc = df_dept[df_dept['producto'] == producto].copy()
    dfc['volumen_total'] = dfc['volumen_total'].astype(float)

    # Convertir a millones de galones
    dfc['volumen_millones'] = dfc['volumen_total'] / 1000000

    # Encontrar la fecha más reciente y excluirla
    last_date = dfc['fecha_despacho'].max()
    dfc = dfc[dfc['fecha_despacho'] < last_date]

    # Agrupar por fecha
    dfc_grouped = dfc.groupby('fecha_despacho')['volumen_millones'].sum().reset_index()

    # Crear la figura de Plotly
    fig = px.line(
        dfc_grouped,
        x='fecha_despacho',
        y='volumen_millones',
        title=f"{plegend}",
        labels={"volumen_millones": "Millones de Galones", "fecha_despacho": "Fecha"},
        markers=True,
        color_discrete_sequence=[color]
    )

    # Create a modified version of style_graph without the boxShadow property
    # boxShadow is not a valid property for plotly.graph_objs.Layout
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Millones de Galones",
        # **style_graph  # Commented out due to boxShadow error
    )

    return fig

def create_table(dfm, producto):
    dfc = dfm[dfm['producto'] == producto].copy()
    dfc['volumen_total'] = dfc['volumen_total'].astype(float)
    dfc['anio_despacho'] = dfc['anio_despacho'].astype(int)

    # Convertir a millones de galones
    dfc['volumen_millones'] = dfc['volumen_total'] / 1000000

    # Ordenar por año
    dfc = dfc.sort_values('anio_despacho')

    # Calcular variación relativa
    dfc['variacion_relativa'] = dfc['volumen_millones'].pct_change() * 100

    # Preparar datos para la tabla
    table_data = dfc[['anio_despacho', 'volumen_millones', 'variacion_relativa']].copy()
    table_data.columns = ['Año', 'Volumen (Millones de Galones)', 'Variación (%)']

    # Formatear valores
    table_data['Volumen (Millones de Galones)'] = table_data['Volumen (Millones de Galones)'].round(2)
    table_data['Variación (%)'] = table_data['Variación (%)'].round(2)

    # Crear tabla
    return dash_table.DataTable(
        data=table_data.to_dict('records'),
        columns=[{"name": col, "id": col} for col in table_data.columns],
        style_cell=style_cell,
        style_header=style_header,
        style_data=style_data,
        style_table=style_table
    )

def create_table_ts(df_dept, producto):
    dfc = df_dept[df_dept['producto'] == producto].copy()
    dfc['volumen_total'] = dfc['volumen_total'].astype(float)

    # Convertir a millones de galones
    dfc['volumen_millones'] = dfc['volumen_total'] / 1000000

    # Encontrar la fecha más reciente y excluirla
    last_date = dfc['fecha_despacho'].max()
    dfc = dfc[dfc['fecha_despacho'] < last_date]

    # Agrupar por fecha
    dfc_grouped = dfc.groupby(['fecha_despacho'])['volumen_millones'].sum().reset_index()

    # Ordenar por fecha
    dfc_grouped = dfc_grouped.sort_values('fecha_despacho')

    # Formatear fecha para mostrar
    dfc_grouped['Fecha'] = dfc_grouped['fecha_despacho'].dt.strftime('%Y-%m')

    # Preparar datos para la tabla
    table_data = dfc_grouped[['Fecha', 'volumen_millones']].copy()
    table_data.columns = ['Fecha', 'Volumen (Millones de Galones)']

    # Formatear valores
    table_data['Volumen (Millones de Galones)'] = table_data['Volumen (Millones de Galones)'].round(2)

    # Crear tabla
    return dash_table.DataTable(
        data=table_data.to_dict('records'),
        columns=[{"name": col, "id": col} for col in table_data.columns],
        style_cell=style_cell,
        style_header=style_header,
        style_data=style_data,
        style_table=style_table,
        page_size=12
    )
