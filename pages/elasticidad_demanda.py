import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input
from Constants import style_header1, style_text_bottom, style_drop_label
import Constants
from services.elasticidad_demanda_data import ElasticidadDemandaLoad
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go

edl = ElasticidadDemandaLoad()

dash.register_page(__name__)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Elasticidad de la Demanda", style=style_header1)
        ], width=9, className='text-center'),
        dbc.Col([
            html.Img(src='../assets/logoComce-Soldicom.png', style={'width': '100%', 'height': 'auto'}),
        ], width=3),
    ], justify='center', align='center', style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            html.P("Análisis de la elasticidad de la demanda de combustibles líquidos:", style=style_text_bottom)
        ], width=12)
    ], style={'padding': '2em'}),

    dbc.Row([
        dbc.Col([
            html.Label("Seleccionar Ciudad:", style=style_drop_label),
            dcc.Dropdown(
                id='ciudad-dropdown',
                options=[{'label': ciudad, 'value': ciudad} for ciudad in edl.ciudades],
                value='NACIONAL',
                clearable=False
            ),
        ], width=4),
        dbc.Col([
            html.Label("Seleccionar Rango de Fechas:", style=style_drop_label),
            dcc.RangeSlider(
                id='fecha-range-slider',
                min=0,
                max=len(edl.unique_fechas) - 1,
                value=[0, len(edl.unique_fechas) - 1],
                marks={i: fecha.strftime('%Y-%m') for i, fecha in enumerate(edl.unique_fechas) if i % 6 == 0},
                step=1,
                allowCross=False
            ),
        ], width=8),
    ], style={'padding': '2em'}),

    dbc.Row([
        # Regression plot and table for Corriente
        dbc.Col([
            dcc.Graph(id='regression-corriente-graph'),
            html.H4('Estadísticas de Regresión', style={'textAlign': 'center'}),
            html.Div(id='regression-corriente-table')
        ], width=6),
        # Regression plot and table for ACPM
        dbc.Col([
            dcc.Graph(id='regression-acpm-graph'),
            html.H4('Estadísticas de Regresión', style={'textAlign': 'center'}),
            html.Div(id='regression-acpm-table')
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='price-corriente-graph')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='price-acpm-graph')
        ], width=6),
    ]),

    # Footer
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


def interpret_elasticity(coef):
    if coef > -1 and coef < 0:
        return 'Inelástica'
    elif coef <= -1:
        return 'Elástica'
    elif coef >= 0:
        return 'Anómala'
    else:
        return ''

def interpret_intercept(intercept):
    if intercept > 0:
        return 'Positivo'
    elif intercept < 0:
        return 'Negativo'
    else:
        return 'Cero'

def interpret_r_squared(r_squared):
    if r_squared >= 0.9:
        return 'Excelente ajuste'
    elif r_squared >= 0.7:
        return 'Buen ajuste'
    elif r_squared >= 0.5:
        return 'Ajuste moderado'
    else:
        return 'Pobre ajuste'

def interpret_p_value(p_value):
    if p_value < 0.01:
        return 'Altamente significativo'
    elif p_value < 0.05:
        return 'Significativo'
    elif p_value < 0.1:
        return 'Marginalmente significativo'
    else:
        return 'No significativo'

@callback(
    Output('regression-corriente-graph', 'figure'),
    Output('regression-corriente-table', 'children'),
    Output('regression-acpm-graph', 'figure'),
    Output('regression-acpm-table', 'children'),
    Output('price-corriente-graph', 'figure'),
    Output('price-acpm-graph', 'figure'),
    Input('ciudad-dropdown', 'value'),
    Input('fecha-range-slider', 'value')
)
def update_graphs(ciudad, fecha_range):
    start_idx, end_idx = fecha_range
    start_date = edl.unique_fechas[start_idx]
    end_date = edl.unique_fechas[end_idx]

    df = edl.df_demanda.copy()
    # Filter by city
    df = df[df['ciudad'] == ciudad]
    # Filter by date range
    df = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date)]

    # Ensure there is data to process
    if df.empty:
        no_data_fig = go.Figure()
        no_data_fig.add_annotation(
            text='No hay datos disponibles',
            xref='paper', yref='paper',
            showarrow=False,
            font=dict(size=20)
        )
        return no_data_fig, 'No hay datos disponibles', no_data_fig, 'No hay datos disponibles', no_data_fig, no_data_fig

    # Regression for 'corriente'
    df_corriente = df[['precio_corriente', 'vol_corriente']].dropna()
    if df_corriente.empty or df_corriente['precio_corriente'].le(0).any() or df_corriente['vol_corriente'].le(0).any():
        fig_corriente = go.Figure()
        table_corriente = 'No hay datos disponibles'
    else:
        df_corriente['log_precio'] = np.log(df_corriente['precio_corriente'])
        df_corriente['log_volumen'] = np.log(df_corriente['vol_corriente'])
        X_corriente = sm.add_constant(df_corriente['log_precio'])
        y_corriente = df_corriente['log_volumen']
        model_corriente = sm.OLS(y_corriente, X_corriente).fit()
        coef_corriente = model_corriente.params['log_precio']
        intercept_corriente = model_corriente.params['const']
        r_squared_corriente = model_corriente.rsquared
        p_value_corriente = model_corriente.pvalues['log_precio']
        y_pred_corriente = model_corriente.predict(X_corriente)

        # Create scatter plot with regression line
        fig_corriente = go.Figure()
        fig_corriente.add_trace(go.Scatter(
            x=df_corriente['log_precio'],
            y=df_corriente['log_volumen'],
            mode='markers',
            name='Datos'
        ))
        fig_corriente.add_trace(go.Scatter(
            x=df_corriente['log_precio'],
            y=y_pred_corriente,
            mode='lines',
            name='Ajuste Lineal'
        ))
        fig_corriente.update_layout(
            title='Regresión Log-Log para Corriente',
            xaxis_title='Log(Precio Corriente)',
            yaxis_title='Log(Volumen Corriente)',
            legend_title='Leyenda',
        )

        # Interpretations
        interpretation_coef_corriente = interpret_elasticity(coef_corriente)
        interpretation_intercept_corriente = interpret_intercept(intercept_corriente)
        interpretation_r2_corriente = interpret_r_squared(r_squared_corriente)
        interpretation_pvalue_corriente = interpret_p_value(p_value_corriente)

        # Create regression statistics table
        table_corriente = dbc.Table([
            html.Thead(html.Tr([
                html.Th('Parámetro'),
                html.Th('Valor'),
                html.Th('Interpretación')
            ])),
            html.Tbody([
                html.Tr([
                    html.Td('Coeficiente (Elasticidad de la demanda)'),
                    html.Td(f"{coef_corriente:.4f}"),
                    html.Td(interpretation_coef_corriente)
                ]),
                html.Tr([
                    html.Td('Intercepto'),
                    html.Td(f"{intercept_corriente:.4f}"),
                    html.Td(interpretation_intercept_corriente)
                ]),
                html.Tr([
                    html.Td('R²'),
                    html.Td(f"{r_squared_corriente:.4f}"),
                    html.Td(interpretation_r2_corriente)
                ]),
                html.Tr([
                    html.Td('Valor p'),
                    html.Td(f"{p_value_corriente:.4f}"),
                    html.Td(interpretation_pvalue_corriente)
                ]),
            ])
        ], bordered=True)

    # Regression for 'acpm'
    df_acpm = df[['precio_acpm', 'vol_acpm']].dropna()
    if df_acpm.empty or df_acpm['precio_acpm'].le(0).any() or df_acpm['vol_acpm'].le(0).any():
        fig_acpm = go.Figure()
        table_acpm = 'No hay datos disponibles'
    else:
        df_acpm['log_precio'] = np.log(df_acpm['precio_acpm'])
        df_acpm['log_volumen'] = np.log(df_acpm['vol_acpm'])
        X_acpm = sm.add_constant(df_acpm['log_precio'])
        y_acpm = df_acpm['log_volumen']
        model_acpm = sm.OLS(y_acpm, X_acpm).fit()
        coef_acpm = model_acpm.params['log_precio']
        intercept_acpm = model_acpm.params['const']
        r_squared_acpm = model_acpm.rsquared
        p_value_acpm = model_acpm.pvalues['log_precio']
        y_pred_acpm = model_acpm.predict(X_acpm)

        # Create scatter plot with regression line
        fig_acpm = go.Figure()
        fig_acpm.add_trace(go.Scatter(
            x=df_acpm['log_precio'],
            y=df_acpm['log_volumen'],
            mode='markers',
            name='Datos'
        ))
        fig_acpm.add_trace(go.Scatter(
            x=df_acpm['log_precio'],
            y=y_pred_acpm,
            mode='lines',
            name='Ajuste Lineal'
        ))
        fig_acpm.update_layout(
            title='Regresión Log-Log para ACPM',
            xaxis_title='Log(Precio ACPM)',
            yaxis_title='Log(Volumen ACPM)',
            legend_title='Leyenda',
        )

        # Interpretations
        interpretation_coef_acpm = interpret_elasticity(coef_acpm)
        interpretation_intercept_acpm = interpret_intercept(intercept_acpm)
        interpretation_r2_acpm = interpret_r_squared(r_squared_acpm)
        interpretation_pvalue_acpm = interpret_p_value(p_value_acpm)

        # Create regression statistics table
        table_acpm = dbc.Table([
            html.Thead(html.Tr([
                html.Th('Parámetro'),
                html.Th('Valor'),
                html.Th('Interpretación')
            ])),
            html.Tbody([
                html.Tr([
                    html.Td('Coeficiente (Elasticidad de la demanda)'),
                    html.Td(f"{coef_acpm:.4f}"),
                    html.Td(interpretation_coef_acpm)
                ]),
                html.Tr([
                    html.Td('Intercepto'),
                    html.Td(f"{intercept_acpm:.4f}"),
                    html.Td(interpretation_intercept_acpm)
                ]),
                html.Tr([
                    html.Td('R²'),
                    html.Td(f"{r_squared_acpm:.4f}"),
                    html.Td(interpretation_r2_acpm)
                ]),
                html.Tr([
                    html.Td('Valor p'),
                    html.Td(f"{p_value_acpm:.4f}"),
                    html.Td(interpretation_pvalue_acpm)
                ]),
            ])
        ], bordered=True)

    # Time series plot of precio_corriente
    fig_price_corriente = go.Figure()
    if not df['precio_corriente'].isna().all():
        fig_price_corriente.add_trace(go.Scatter(
            x=df['fecha'],
            y=df['precio_corriente'],
            mode='lines+markers',
            name='Precio Corriente'
        ))
    fig_price_corriente.update_layout(
        title='Serie de Tiempo de Precio Corriente',
        xaxis_title='Fecha',
        yaxis_title='Precio Corriente',
        legend_title='Producto',
    )

    # Time series plot of precio_acpm
    fig_price_acpm = go.Figure()
    if not df['precio_acpm'].isna().all():
        fig_price_acpm.add_trace(go.Scatter(
            x=df['fecha'],
            y=df['precio_acpm'],
            mode='lines+markers',
            name='Precio ACPM'
        ))
    fig_price_acpm.update_layout(
        title='Serie de Tiempo de Precio ACPM',
        xaxis_title='Fecha',
        yaxis_title='Precio ACPM',
        legend_title='Producto',
    )

    return fig_corriente, table_corriente, fig_acpm, table_acpm, fig_price_corriente, fig_price_acpm
