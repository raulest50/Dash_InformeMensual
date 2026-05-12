import dash
import dash_bootstrap_components as dbc
from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output

import Constants
from components.loading import loading_overlay
from Constants import (
    style_cell,
    style_data,
    style_drop_label,
    style_graph,
    style_header,
    style_header1,
    style_H3,
    style_table,
)
from services import municipal_map_data as map_data


DEFAULT_PRODUCT = "GASOLINA MOTOR CORRIENTE"


dash.register_page(
    __name__,
    path="/mapa-consumo-municipal",
    title="Mapa coroplético",
    name="Mapa coroplético",
)


def summary_item(label, value):
    return html.Div(
        [
            html.Div(label, style={"fontSize": "0.85rem", "color": "#555"}),
            html.Div(value, style={"fontSize": "1.25rem", "fontWeight": "700"}),
        ],
        style={
            "borderBottom": f"3px solid {Constants.verde}",
            "fontFamily": "'Plus Jakarta Sans', sans-serif",
            "padding": "0.6rem 0",
        },
    )


def format_volume(value):
    return f"{float(value):,.0f}"


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.H1("Mapa coroplético", style=style_header1)],
                    width=9,
                    xl=9,
                    lg=9,
                    md=6,
                    sm=6,
                    xs=12,
                ),
                dbc.Col(
                    [html.Img(src="/assets/logoComce.png", style={"width": "50%", "height": "50%"})],
                    width=3,
                    xl=3,
                    lg=3,
                    md=6,
                    sm=6,
                    xs=12,
                ),
            ],
            align="center",
            justify="center",
            style={"padding": "2em"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Producto:", htmlFor="municipal-map-product", style=style_drop_label),
                        dcc.Dropdown(
                            id="municipal-map-product",
                            options=map_data.product_options(),
                            value=DEFAULT_PRODUCT,
                            clearable=False,
                        ),
                    ],
                    width=4,
                    xl=4,
                    lg=4,
                    md=6,
                    sm=12,
                    xs=12,
                ),
                dbc.Col(
                    [
                        html.Label("A\u00f1o:", htmlFor="municipal-map-year", style=style_drop_label),
                        dcc.Dropdown(
                            id="municipal-map-year",
                            options=map_data.year_options(),
                            value=map_data.default_year(),
                            clearable=False,
                        ),
                    ],
                    width=2,
                    xl=2,
                    lg=2,
                    md=3,
                    sm=6,
                    xs=6,
                ),
                dbc.Col(
                    [
                        html.Label("Mes:", htmlFor="municipal-map-month", style=style_drop_label),
                        dcc.Dropdown(
                            id="municipal-map-month",
                            options=map_data.month_options(map_data.default_year()),
                            value="all",
                            clearable=False,
                        ),
                    ],
                    width=2,
                    xl=2,
                    lg=2,
                    md=3,
                    sm=6,
                    xs=6,
                ),
                dbc.Col(
                    [
                        html.Label("Escala:", htmlFor="municipal-map-scale", style=style_drop_label),
                        dcc.Dropdown(
                            id="municipal-map-scale",
                            options=[
                                {"label": "Logar\u00edtmica", "value": "log"},
                                {"label": "Lineal", "value": "linear"},
                            ],
                            value="log",
                            clearable=False,
                        ),
                    ],
                    width=2,
                    xl=2,
                    lg=2,
                    md=6,
                    sm=12,
                    xs=12,
                ),
            ],
            align="center",
            justify="left",
            style={"padding": "1em 2em"},
        ),
        loading_overlay(
            [
                dbc.Row(
                    [
                        dbc.Col([html.Div(id="municipal-map-summary-total")], width=3, md=3, sm=6, xs=12),
                        dbc.Col([html.Div(id="municipal-map-summary-observed")], width=3, md=3, sm=6, xs=12),
                        dbc.Col([html.Div(id="municipal-map-summary-zero")], width=3, md=3, sm=6, xs=12),
                        dbc.Col([html.Div(id="municipal-map-summary-no-geometry")], width=3, md=3, sm=6, xs=12),
                    ],
                    style={"padding": "0 2em 1em"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="municipal-consumption-map",
                                    style=style_graph,
                                    config={"scrollZoom": True, "displayModeBar": True},
                                )
                            ],
                            width=8,
                            xl=8,
                            lg=8,
                            md=12,
                            sm=12,
                            xs=12,
                        ),
                        dbc.Col(
                            [
                                html.H3(
                                    id="municipal-map-selected-title",
                                    children="Municipio seleccionado",
                                    style=style_H3,
                                ),
                                loading_overlay(
                                    dcc.Graph(id="municipal-map-timeseries", style=style_graph),
                                    loading_id="municipal-map-timeseries-loading",
                                    message="Cargando serie municipal...",
                                    spinner_size="sm",
                                    target_components={"municipal-map-timeseries": "figure"},
                                ),
                                html.H3("Principales municipios", style=style_H3),
                                dash_table.DataTable(
                                    id="municipal-map-top-table",
                                    columns=[
                                        {"name": "Departamento", "id": "departamento"},
                                        {"name": "Municipio", "id": "municipio"},
                                        {"name": "Volumen", "id": "volumen_total", "type": "numeric"},
                                        {"name": "Participaci\u00f3n %", "id": "participacion_pct", "type": "numeric"},
                                    ],
                                    page_size=10,
                                    style_cell=style_cell,
                                    style_data=style_data,
                                    style_header=style_header,
                                    style_table=style_table,
                                ),
                            ],
                            width=4,
                            xl=4,
                            lg=4,
                            md=12,
                            sm=12,
                            xs=12,
                        ),
                    ],
                    style={"padding": "1em 2em 2em"},
                ),
            ],
            loading_id="municipal-map-results-loading",
            message="Procesando informaci\u00f3n del mapa...",
            target_components={
                "municipal-consumption-map": "figure",
                "municipal-map-summary-total": "children",
                "municipal-map-summary-observed": "children",
                "municipal-map-summary-zero": "children",
                "municipal-map-summary-no-geometry": "children",
                "municipal-map-top-table": "data",
            },
        ),
    ],
    fluid=True,
)


@callback(
    Output("municipal-map-month", "options"),
    Output("municipal-map-month", "value"),
    Input("municipal-map-year", "value"),
)
def update_month_options(year):
    options = map_data.month_options(int(year))
    return options, "all"


@callback(
    Output("municipal-consumption-map", "figure"),
    Output("municipal-map-summary-total", "children"),
    Output("municipal-map-summary-observed", "children"),
    Output("municipal-map-summary-zero", "children"),
    Output("municipal-map-summary-no-geometry", "children"),
    Output("municipal-map-top-table", "data"),
    Input("municipal-map-product", "value"),
    Input("municipal-map-year", "value"),
    Input("municipal-map-month", "value"),
    Input("municipal-map-scale", "value"),
)
def update_map(product, year, month, scale):
    selected_month = None if month == "all" else int(month)
    fig, summary = map_data.make_map_figure(product, int(year), selected_month, scale)
    top_rows = map_data.top_municipalities(product, int(year), selected_month)

    return (
        fig,
        summary_item("Volumen total", format_volume(summary.get("total_volume", 0))),
        summary_item("Municipios con dato", f"{summary.get('observed_municipalities', 0):,}"),
        summary_item("Municipios en cero", f"{summary.get('zero_filled_municipalities', 0):,}"),
        summary_item("Sin geometr\u00eda", f"{summary.get('without_geometry', 0):,}"),
        top_rows,
    )


@callback(
    Output("municipal-map-selected-title", "children"),
    Output("municipal-map-timeseries", "figure"),
    Input("municipal-consumption-map", "clickData"),
    Input("municipal-map-product", "value"),
)
def update_selected_municipality(click_data, product):
    selected_pair = map_data.get_pair_from_click(click_data)
    return map_data.municipality_label(selected_pair), map_data.make_timeseries_figure(selected_pair, product)
