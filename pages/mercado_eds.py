import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

import Constants
from Constants import style_data, style_cell, style_header, style_table, style_graph, \
    style_header1, style_header4, style_H3, style_text_bottom, style_H2, style_drop_label, verde, azul, gris, brand_colors

from dash.dependencies import Input, Output, State
from services.mercado_eds_data import MercadoEDSLoad

# Initialize the data loader
meds = MercadoEDSLoad()

# Register the page
dash.register_page(
    __name__,
    path='/mercado-eds',
    title='Estudio de mercado EDS',
    name='Estudio de mercado EDS'
)

# Load GeoJSON for Colombia map
with open('colombiaMod.json', 'r', encoding='utf-8') as f:
    colombia_geojson = json.load(f)

# Layout definition
layout = dbc.Container([
    # Header row with title and logo
    dbc.Row([
        dbc.Col([
            html.H1("Estudio de mercado EDS", style=style_header1)
        ], width=9, xl=9, lg=9, md=6, sm=6, xs=4, className='text-center', style={'textAlign': 'center'}),
        dbc.Col([
            html.Img(src='/assets/logoComce.png', style={'width': '50%', 'height': '50%'}),
        ], width=3, xl=3, lg=3, md=6, sm=6, xs=12),
    ], justify='center', align='center', style={'padding': '2em'}),

    # Introduction text
    dbc.Row([
        dbc.Col([
            html.P(
                "Este tablero permite analizar el mercado relevante de las Estaciones de Servicio (EDS) en Colombia. "
                "Ingrese el código SICOM de una EDS para visualizar su información y la de sus competidores.",
                style=style_text_bottom
            )
        ], width=12)
    ], style={'padding': '2em'}),

    # SICOM search filter
    dbc.Row([
        dbc.Col([
            html.Label("Buscar por código SICOM:", htmlFor='sicom-input', style=style_drop_label),
            dbc.InputGroup([
                dbc.Input(
                    id='sicom-input',
                    type='text',
                    placeholder='Ingrese código SICOM',
                    value='',
                ),
                dbc.Button("Buscar", id="search-button", color="primary", className="ml-2"),
            ]),
            dcc.Dropdown(
                id='sicom-dropdown',
                options=[{'label': str(code), 'value': code} for code in meds.sicom_codes],
                placeholder="O seleccione un código SICOM",
                clearable=True
            ),
        ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),
    ], justify='left', align='center', style={'padding': '2em'}),

    # EDS details and map section
    dbc.Row([
        # EDS details
        dbc.Col([
            html.Div(id='eds-details', children=[
                html.H3("Detalles de la EDS", style=style_H3),
                html.Div(id='eds-info', children=[
                    html.P("Seleccione un código SICOM para ver los detalles.", style=style_text_bottom)
                ])
            ])
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),

        # Map
        dbc.Col([
            html.H3("Mapa de Mercado Relevante", style=style_H3),
            dcc.Graph(id='market-map', style=style_graph)
        ], width=8, xl=8, lg=8, md=12, sm=12, xs=12),
    ], style={'padding': '2em'}),

    # Competition metrics and brand distribution
    dbc.Row([
        # Competition metrics
        dbc.Col([
            html.H3("Métricas de Competencia", style=style_H3),
            html.Div(id='competition-metrics', children=[
                html.P("Seleccione un código SICOM para ver las métricas de competencia.", style=style_text_bottom)
            ])
        ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),

        # Brand distribution pie chart
        dbc.Col([
            html.H3("Distribución de Banderas", style=style_H3),
            dcc.Graph(id='brand-distribution', style=style_graph)
        ], width=6, xl=6, lg=6, md=12, sm=12, xs=12),
    ], style={'padding': '2em'}),

    # Competitors table
    dbc.Row([
        dbc.Col([
            html.H3("Competidores", style=style_H3),
            dash_table.DataTable(
                id='competitors-table',
                style_cell=style_cell,
                style_header=style_header,
                style_data=style_data,
                style_table=style_table,
                page_size=10,
                sort_action='native',
                filter_action='native',
            )
        ], width=12)
    ], style={'padding': '2em'}),

    # Information about the data source
    dbc.Row([
        dbc.Col([
            html.H3("Información sobre la fuente de datos", style=style_H3),
            html.P(
                "Los datos presentados en este tablero provienen de un análisis del mercado relevante de las Estaciones de Servicio. "
                "Para definir el mercado relevante, se establece una distancia de referencia que depende de la categorización del municipio según el DANE: "
                "en municipios clasificados como Nodo, Aglomeración o Intermedio, el radio es de 4 km, mientras que en municipios Rurales o Rurales Dispersos, "
                "se amplía a 10 km. El Índice de Herfindahl-Hirschman (IHH) mide el grado de concentración del mercado, considerándose desconcentrados "
                "aquellos con un índice menor o igual a 2500. El indicador Stenbacka ofrece otra medida de competencia, estableciendo un umbral específico "
                "para la cuota de mercado.",
                style=style_text_bottom
            ),
        ])
    ], style={'padding': '2em'}),

    # Store for selected SICOM code
    dcc.Store(id='selected-sicom'),

], fluid=True)

# Callback to update selected SICOM from input or dropdown
@callback(
    Output('selected-sicom', 'data'),
    [Input('search-button', 'n_clicks'),
     Input('sicom-dropdown', 'value')],
    [State('sicom-input', 'value')],
    prevent_initial_call=True
)
def update_selected_sicom(n_clicks, dropdown_value, input_value):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'search-button' and input_value:
        # Convert to integer if possible
        try:
            sicom_code = int(input_value)
            if sicom_code in meds.sicom_codes:
                return sicom_code
        except:
            return None
    elif trigger_id == 'sicom-dropdown' and dropdown_value:
        return dropdown_value

    return None

# Callback to update EDS details
@callback(
    Output('eds-info', 'children'),
    Input('selected-sicom', 'data'),
    prevent_initial_call=True
)
def update_eds_details(sicom_code):
    if not sicom_code:
        return [html.P("Seleccione un código SICOM para ver los detalles.", style=style_text_bottom)]

    eds_details = meds.get_eds_details(sicom_code)

    if not eds_details:
        return [html.P("No se encontró información para el código SICOM seleccionado.", style=style_text_bottom)]

    return [
        html.Div([
            html.P(f"Código SICOM: {sicom_code}", style=style_text_bottom),
            html.P(f"Nombre Comercial: {eds_details['nombre_comercial']}", style=style_text_bottom),
            html.P(f"Bandera: {eds_details['bandera']}", style=style_text_bottom),
            html.P(f"Ubicación: {eds_details['municipio']}, {eds_details['departamento']}", style=style_text_bottom),
            html.P(f"Número de Competidores: {eds_details['num_competidores']}", style=style_text_bottom),
            html.P(f"Radio de Mercado Relevante: {eds_details['radio_mercado']}", style=style_text_bottom),
        ])
    ]

# Callback to update competition metrics
@callback(
    Output('competition-metrics', 'children'),
    Input('selected-sicom', 'data'),
    prevent_initial_call=True
)
def update_competition_metrics(sicom_code):
    if not sicom_code:
        return [html.P("Seleccione un código SICOM para ver las métricas de competencia.", style=style_text_bottom)]

    eds_details = meds.get_eds_details(sicom_code)

    if not eds_details:
        return [html.P("No se encontró información para el código SICOM seleccionado.", style=style_text_bottom)]

    # Function to determine concentration status
    def get_concentration_status(ihh_value):
        if ihh_value == "NO HAY INFORMACIÓN":
            return "No hay información disponible"
        try:
            ihh_float = float(ihh_value)
            return "Mercado Desconcentrado" if ihh_float <= 2500 else "Mercado Concentrado"
        except:
            return "No hay información disponible"

    # Create metrics cards
    metrics_cards = [
        dbc.Card([
            dbc.CardHeader("Gasolina Corriente"),
            dbc.CardBody([
                html.P(f"IHH: {eds_details['ihh_corriente']}"),
                html.P(f"Estado: {get_concentration_status(eds_details['ihh_corriente'])}"),
                html.P(f"Stenbacka: {eds_details['stenbacka_corriente']}")
            ])
        ], className="mb-3"),

        dbc.Card([
            dbc.CardHeader("ACPM"),
            dbc.CardBody([
                html.P(f"IHH: {eds_details['ihh_acpm']}"),
                html.P(f"Estado: {get_concentration_status(eds_details['ihh_acpm'])}"),
                html.P(f"Stenbacka: {eds_details['stenbacka_acpm']}")
            ])
        ], className="mb-3"),

        dbc.Card([
            dbc.CardHeader("Gasolina Extra"),
            dbc.CardBody([
                html.P(f"IHH: {eds_details['ihh_extra']}"),
                html.P(f"Estado: {get_concentration_status(eds_details['ihh_extra'])}"),
                html.P(f"Stenbacka: {eds_details['stenbacka_extra']}")
            ])
        ])
    ]

    return metrics_cards

# Callback to update brand distribution chart
@callback(
    Output('brand-distribution', 'figure'),
    Input('selected-sicom', 'data'),
    prevent_initial_call=True
)
def update_brand_distribution(sicom_code):
    if not sicom_code:
        # Return empty figure
        return {
            'data': [],
            'layout': {
                'title': 'Seleccione un código SICOM para ver la distribución de banderas',
                'height': 400
            }
        }

    brand_distribution = meds.get_competitor_brands_distribution(sicom_code)

    if brand_distribution.empty:
        # Return empty figure with message
        return {
            'data': [],
            'layout': {
                'title': 'No hay datos disponibles para la distribución de banderas',
                'height': 400
            }
        }

    # Create pie chart
    fig = px.pie(
        brand_distribution,
        values='Cantidad',
        names='Bandera',
        title=f'Distribución de Banderas de Competidores',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )

    return fig

# Callback to update competitors table
@callback(
    Output('competitors-table', 'data'),
    Output('competitors-table', 'columns'),
    Input('selected-sicom', 'data'),
    prevent_initial_call=True
)
def update_competitors_table(sicom_code):
    if not sicom_code:
        return [], []

    competitors = meds.get_competitors(sicom_code)

    if competitors.empty:
        return [], []

    columns = [{"name": col, "id": col} for col in competitors.columns]

    return competitors.to_dict('records'), columns

# Callback to update market map
@callback(
    Output('market-map', 'figure'),
    Input('selected-sicom', 'data'),
)
def update_market_map(sicom_code):
    if not sicom_code:
        # Return Colombia map when no SICOM code is selected
        # Create a list of department names from the GeoJSON
        dept_names = [feature['properties']['NAME_1'] for feature in colombia_geojson['features']]
        # Create a list of values (1 for each department to give them all the same color)
        dept_values = [1] * len(dept_names)

        fig = go.Figure(go.Choroplethmapbox(
            geojson=colombia_geojson,
            locations=dept_names,
            z=dept_values,
            featureidkey="properties.NAME_1",
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker_opacity=0.5,
            marker_line_width=1,
            marker_line_color='white',
            showscale=False,
            hoverinfo='none'
        ))

        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=4.5,
            mapbox_center={"lat": 4.5709, "lon": -74.2973},
            height=600,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            title={
                'text': 'Mapa de Colombia - Seleccione un código SICOM para ver el mercado relevante',
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        return fig

    map_data = meds.get_map_data(sicom_code)

    if not map_data['eds']:
        # Return empty map with Colombia boundaries
        fig = go.Figure(go.Choroplethmapbox(
            geojson=colombia_geojson,
            locations=["Colombia"],
            z=[0],
            featureidkey="properties.NAME_1",
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker_opacity=0.1,
            marker_line_width=0.5,
            showscale=False
        ))

        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=4,
            mapbox_center={"lat": 4.5709, "lon": -74.2973},
            height=600,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        return fig

    # Create map with EDS and competitors
    fig = go.Figure()

    # Add Colombia boundaries
    fig.add_trace(go.Choroplethmapbox(
        geojson=colombia_geojson,
        locations=["Colombia"],
        z=[0],
        featureidkey="properties.NAME_1",
        colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
        marker_opacity=0.1,
        marker_line_width=0.5,
        showscale=False
    ))

    # Add EDS marker
    fig.add_trace(go.Scattermapbox(
        lat=[map_data['eds']['coords'][1]],
        lon=[map_data['eds']['coords'][0]],
        mode='markers',
        marker=dict(
            size=15,
            color='black',  # Punto negro para la estación seleccionada
            symbol='circle'
        ),
        text=[f"SICOM: {map_data['eds']['sicom']}<br>Nombre: {map_data['eds']['nombre']}<br>Bandera: {map_data['eds']['bandera']}"],
        hoverinfo='text',
        name='EDS Seleccionada'
    ))

    # Group competitors by brand for better legend display
    competitors_by_brand = {}
    for comp in map_data['competitors']:
        brand = comp['bandera']
        if brand not in competitors_by_brand:
            competitors_by_brand[brand] = {
                'lats': [],
                'lons': [],
                'texts': []
            }
        competitors_by_brand[brand]['lats'].append(comp['coords'][1])
        competitors_by_brand[brand]['lons'].append(comp['coords'][0])
        competitors_by_brand[brand]['texts'].append(
            f"SICOM: {comp['sicom']}<br>Nombre: {comp['nombre']}<br>Bandera: {comp['bandera']}<br>Distancia: {comp['distancia']}"
        )

    # Add competitors markers by brand
    for brand, data in competitors_by_brand.items():
        # Get brand color or use a default color
        color = brand_colors.get(brand, azul)  # Use azul as default if brand not in dictionary

        fig.add_trace(go.Scattermapbox(
            lat=data['lats'],
            lon=data['lons'],
            mode='markers',
            marker=dict(
                size=10,
                color=color,
                symbol='circle'
            ),
            text=data['texts'],
            hoverinfo='text',
            name=f'{brand}'
        ))

    # Update layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=12,
        mapbox_center={"lat": map_data['eds']['coords'][1], "lon": map_data['eds']['coords'][0]},
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="center",
            x=0.5
        )
    )

    return fig
