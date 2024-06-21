import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd

import Constants
import methods
from methods import getDataFrame, getDataFrame_suset
from os.path import exists

from Constants import style_data, style_cell, style_header, style_table, style_graph, style_graph2,\
    style_header1, style_header4, style_H3, style_text_bottom, style_H2, style_drop_label

# this for production
df = getDataFrame_suset()
df['mes_despacho'] = df['mes_despacho'].astype(int)


#this piece of code only for debuging
# df = None
# if(exists('./vmensual.csv')):
#     df = pd.read_csv('vmensual.csv')
#     print("dataframe obtained locally")
# else:
#     df = getDataFrame_suset()
#     print("dataframe obtained from remote origin")
#     df.to_csv('vmensual.csv', index=False)


# Initialize the Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap"
])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1(" Reporte Mensual Ventas Combustible Liquido", style=style_header1)
        ], width=9, xl=9, lg=9, md=6, sm=6, xs=4, className='text-center', style={'textAlign': 'center'}),
        dbc.Col([
            html.Img(src='/assets/logoComce-Soldicom.png', style={'width': '100%', 'height': 'auto'}),
        ], width=3, xl=3, lg=3, md=6, sm=6, xs=12),
    ], justify='center', align='center', style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            html.P(Constants.parrafoTop, style=style_text_bottom)
        ], width=12)
    ], style={'padding': '2em'}),

    dbc.Row([
            dbc.Col([
                    html.Label("Seleccionar Mes:", htmlFor='month-dropdown', style=style_drop_label),  # Add label
                    dcc.Dropdown(
                        id='month-dropdown',
                        options=[{'label': f"{i:02}", 'value': f"{i:02}"} for i in range(1, 13)],
                        value='01',  # Default selected month
                        clearable=False
                    )
                ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
            dbc.Col([
                    html.Label("Seleccionar Lugar:", style=style_drop_label),  # Add label
                    dcc.Dropdown(
                        id='geo-dropdown',
                        options=Constants.geo,
                        value=Constants.geo[0],  # Default selected month
                        clearable=False
                    )
                ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
            dbc.Col([
                    html.Div(),
                ], width=4, xl=4, lg=4, md=0, sm=0, xs=0),
        ], justify='left', align='center', style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='corriente', style=style_graph)  # Placeholder for the plot
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            dcc.Graph(id='acpm', style=style_graph)  # Placeholder for the plot
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            dcc.Graph(id='extra', style=style_graph)  # Placeholder for the plot
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12)
    ], style={'padding': '2em'}),

    dbc.Row([ # no tiene efecto en la visual de la pagina, solo para un page break cuando se haga ctrl + p
    ], style={'pageBreakBefore': 'always'}),

    dbc.Row([
        dbc.Col([
            html.H4("Corriente", style=style_header4),
            dash_table.DataTable(id='corriente-table',
                                 style_cell=style_cell, style_header=style_header, style_data=style_data, style_table=style_table,
                                 )
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            html.H4("ACPM", style=style_header4),
            dash_table.DataTable(id='acpm-table',
                                 style_cell=style_cell, style_header=style_header, style_data=style_data, style_table=style_table,
                                 )
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12),
        dbc.Col([
            html.H4("Extra", style=style_header4),
            dash_table.DataTable(id='extra-table',
                                 style_cell=style_cell, style_header=style_header, style_data=style_data, style_table=style_table,
                                 )
        ], width=4, xl=4, lg=4, md=12, sm=12, xs=12)
    ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            html.H2("RESUMEN EJECUTIVO INFORME MENSUAL DE VENTAS MAYO 2024", style=style_H2),
            html.H3("Información sobre la fuente de datos.", style=style_H3),
            html.P(Constants.parrafo_dt_source, style=style_text_bottom),
            html.H3("Reporte de la variación mensual de ventas MAYO 2024:", style=style_H3),
            html.P(Constants.Gen_parrafoBottom(), style=style_text_bottom),
        ])
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
    ], style={'padding': '2em'})

], fluid=True)


@app.callback(
    [Output('corriente', 'figure'),
     Output('acpm', 'figure'),
     Output('extra', 'figure'),

     Output('corriente-table', 'data'),
     Output('corriente-table', 'columns'),
     Output('acpm-table', 'data'),
     Output('acpm-table', 'columns'),
     Output('extra-table', 'data'),
     Output('extra-table', 'columns'),

     ],
    [
        Input('month-dropdown', 'value'),
        Input('geo-dropdown', 'value'),
     ]
)
def update_graph(mes_seleccionado, geo_seleccionada):
    # Pivot the DataFrame to get years as columns and fuel types as rows

    dfm = None

    if(geo_seleccionada == Constants.geo_translate[0]):
        g_df = df.groupby(['anio_despacho', 'mes_despacho', 'producto'])['volumen_total'].sum().reset_index()
        dfm = g_df[g_df['mes_despacho'] == int(mes_seleccionado)].copy()
        #print(f"geo: {geo_seleccionada}")
        #print(f"mes: {mes_seleccionado}")
    else:
        #print(f"dict res: {Constants.geo_dict.get(geo_seleccionada)}")
        dfmm = df[df['municipio'] == Constants.geo_dict.get(geo_seleccionada)].copy()

        dfm = dfmm[dfmm['mes_despacho'] == int(mes_seleccionado)].copy()


    def create_figure(producto, color, plegend):
        dfc = dfm[dfm['producto'] == producto].copy()
        dfc['volumen_total'] = dfc['volumen_total'].astype(float)
        dfc['anio_despacho'] = dfc['anio_despacho'].astype(int)

        # Create the Plotly figure
        fig = px.line(
            dfc,
            x='anio_despacho',
            y='volumen_total',
            title=f" {plegend} ",
            labels={"value": "Volumen Total", "variable": "Año"},
            markers=True,
            color_discrete_sequence=[color]
        )

        fig.update_layout(
            xaxis_title="Año",
            yaxis_title="Volumen Despachado"
        )
        # Return the figure to be displayed in the graph
        return fig

    def create_table_data(producto):
        dfc = dfm[dfm['producto'] == producto].copy()
        dfc['volumen_total'] = dfc['volumen_total'].astype(float) / 1_000_000
        dfc['volumen_total'] = dfc['volumen_total'].round(4)
        dfc['anio_despacho'] = dfc['anio_despacho'].astype(int)
        dfc = dfc.sort_values(by='anio_despacho')

        dfc['percentage_variation'] = dfc['volumen_total'].pct_change().fillna(0) * 100
        dfc['percentage_variation'] = dfc['percentage_variation'].round(2)

        dfc['percentage_variation'] = dfc['percentage_variation'].astype(str)
        dfc.loc[dfc.index[0], 'percentage_variation'] = '-'

        return dfc[['anio_despacho', 'volumen_total', 'percentage_variation']].to_dict('records'), [
            {"name": "Año", "id": "anio_despacho"},
            {"name": "Millones de Galones", "id": "volumen_total"},
            {"name": "Variación Relativa (%)", "id": "percentage_variation"}
        ]

    fig_corriente = create_figure(methods.p1, methods.verde, "Gasolina Corriente")
    fig_acpm = create_figure(methods.p2, methods.azul, "ACPM")
    fig_extra = create_figure(methods.p3, methods.gris, "Gasolina Extra")

    corriente_table_data, corriente_table_columns = create_table_data(methods.p1)
    acpm_table_data, acpm_table_columns = create_table_data(methods.p2)
    extra_table_data, extra_table_columns = create_table_data(methods.p3)

    return (fig_corriente, fig_acpm, fig_extra,
            corriente_table_data, corriente_table_columns,
            acpm_table_data, acpm_table_columns,
            extra_table_data, extra_table_columns)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
    #app.run_server(debug=True)
