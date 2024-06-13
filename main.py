import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd

import Constants
import methods
from methods import getDataFrame
from os.path import exists

df = pd.read_csv('vmensual.csv')

# Sample data
if(exists('./vmensual.csv')):
    df = pd.read_csv('vmensual.csv')
    print("dataframe obtained locally")
else:
    df = getDataFrame()
    print("dataframe obtained from remote origin")
    df.to_csv('vmensual.csv', index=False)

# Initialize the Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap"
])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Reporte Mensual Ventas Combustible Liquido", style={'fontFamily': "'Plus Jakarta Sans', sans-serif", 'textAlign': 'left'})
        ], width=9, className='text-center', style={'textAlign': 'center'}),
        dbc.Col([
            html.Img(src='/assets/logoComce-Soldicom.png', style={'width': '100%', 'height': 'auto'}),
        ], width=3),
    ], justify='center', align='center', style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            html.P(Constants.parrafoTop, style={})
        ], width=12)
    ], style={'padding': '2em'}),

    dbc.Row([
            dbc.Col([
                    html.Label("Seleccionar Mes:", htmlFor='month-dropdown'),  # Add label
                    dcc.Dropdown(
                        id='month-dropdown',
                        options=[{'label': f"{i:02}", 'value': f"{i:02}"} for i in range(1, 13)],
                        value='01',  # Default selected month
                        clearable=False
                    )
                ], width=3),
        ], justify='left', align='center', style={'padding': '1em'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='corriente')  # Placeholder for the plot
        ], width=4),
        dbc.Col([
            dcc.Graph(id='acpm')  # Placeholder for the plot
        ], width=4),
        dbc.Col([
            dcc.Graph(id='extra')  # Placeholder for the plot
        ], width=4)
    ]),

dbc.Row([
        dbc.Col([
            dash_table.DataTable(id='corriente-table',
                                 style_cell={'textAlign': 'center'}
                                 )
        ], width=4),
        dbc.Col([
            dash_table.DataTable(id='acpm-table',
                                 style_cell={'textAlign': 'center'}
                                 )
        ], width=4),
        dbc.Col([
            dash_table.DataTable(id='extra-table',
                                 style_cell={'textAlign': 'center'}
                                 )
        ], width=4)
    ], style={'padding': '2em'}),

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
    [Input('month-dropdown', 'value'), ]
)
def update_graph(mes_seleccionado):
    # Pivot the DataFrame to get years as columns and fuel types as rows

    dfm = df[df['mes_despacho'] == int(mes_seleccionado)]

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
        dfc['anio_despacho'] = dfc['anio_despacho'].astype(int)
        dfc = dfc.sort_values(by='anio_despacho')

        dfc['percentage_variation'] = dfc['volumen_total'].pct_change().fillna(0) * 100
        dfc['percentage_variation'] = dfc['percentage_variation'].round(2)

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
    app.run_server(debug=True)
