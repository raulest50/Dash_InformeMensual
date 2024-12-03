import os
import pandas as pd
import unicodedata
import re
from services.upme_urls import upme_urls
from services.general import P1, P2, C1, C2, C3, fetch_socrata_datosgov

DATA_DIR_ELASTICIDAD_DEMANDA = 'data/elasticidad_demanda'
DF_VOLS_FPATH = os.path.join(DATA_DIR_ELASTICIDAD_DEMANDA, "df_vols.csv")
DF_PRECIOS_FPATH = os.path.join(DATA_DIR_ELASTICIDAD_DEMANDA, "df_precios.csv")
DF_DEMANDA_PATH = os.path.join(DATA_DIR_ELASTICIDAD_DEMANDA, "df_demanda.csv")
DB_ALIAS_MAYORISTAS = "339g-zjac"
dc_map = {
    'BARRANQUILLA': 'BARRANQUILLA',
    'BOGOTÁ': 'BOGOTA, D.C.',
    'BUCARAMANGA': 'BUCARAMANGA',
    'CALI': 'CALI',
    'CARTAGENA': 'CARTAGENA DE INDIAS',
    'MEDELLÍN': 'MEDELLIN',
    'NEIVA': 'NEIVA',
    'PEREIRA': 'PEREIRA',
    'POPAYAN': 'POPAYAN',
    'SANTA MARTA': 'SANTA MARTA',
    'TUNJA': 'TUNJA',
    'VALLEDUPAR': 'VALLEDUPAR',
    'VILLAVICENCIO': 'VILLAVICENCIO',
    'MANIZALES': 'MANIZALES',
    'ARMENIA': 'ARMENIA',
    'IBAGUE': 'IBAGUE',
    'SINCELEJO': 'SINCELEJO',
    'MONTERIA': 'MONTERIA',
    'promedio': 'NACIONAL'
}


def ensure_data_elasticidad_demanda():
    os.makedirs(DATA_DIR_ELASTICIDAD_DEMANDA, exist_ok=True)
    if os.path.exists(DF_DEMANDA_PATH):
        return
    df_precios = extract_precios(upme_urls)
    df_precios['ciudad'] = df_precios['ciudad'].map(dc_map)
    cities = df_precios['ciudad'].unique()
    df_vols = get_vols(cities)
    df_vols['municipio'] = df_vols['municipio'].apply(clean_city_name)
    df_precios['ciudad'] = df_precios['ciudad'].apply(clean_city_name)

    # 2. Pivot the volume data to get 'vol_corriente' and 'vol_acpm' in separate columns
    df_vol_pivot = df_vols.pivot_table(
        index=['anio_despacho', 'mes_despacho', 'municipio'],
        columns='producto',
        values='volumen_total',
        aggfunc='sum'
    ).reset_index()

    # Rename columns to match for merging
    df_vol_pivot = df_vol_pivot.rename(columns={
        'anio_despacho': 'anio',
        'mes_despacho': 'mes',
        'municipio': 'ciudad',
        'CORRIENTE': 'vol_corriente',
        'DIESEL': 'vol_acpm'
    })

    # 3. Merge the price and volume DataFrames
    df_merged = pd.merge(
        df_precios,
        df_vol_pivot,
        on=['anio', 'mes', 'ciudad'],
        how='left'
    )
    df_merged.to_csv(DF_DEMANDA_PATH, index=False)


def extract_precios(urls_df):
    if os.path.exists(DF_PRECIOS_FPATH):
        return pd.read_csv(DF_PRECIOS_FPATH)
    # df is the initial DataFrame containing anio, mes, url
    data_list = []

    for idx, row in urls_df.iterrows():
        anio = row['anio']
        mes = row['mes']
        url = row['url']
        #print(f"Processing {url}")
        current_data_list = []
        try:
            # Read the Excel file without setting a header
            excel_df = pd.read_excel(url, header=None)
        except Exception as e:
            print(f"Error reading Excel file from {url}: {e}")
            continue

        # Process 'corriente' data
        try:
            # Find the 'CIUDAD' row for corriente
            corriente_ciudad_rows = excel_df[excel_df[0].astype(str).str.strip().str.upper() == 'CIUDAD'].index
            if len(corriente_ciudad_rows) == 0:
                print(f"Could not find 'CIUDAD' row for corriente in {url}")
            else:
                corriente_ciudad_row = corriente_ciudad_rows[0]
                # Get cities
                cities = excel_df.loc[corriente_ciudad_row, 1:].dropna().astype(str).str.strip().tolist()
                # Find the 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA' row after 'CIUDAD'
                precio_rows = excel_df[0][corriente_ciudad_row + 1:].astype(str).str.strip().str.upper()
                if 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA' in precio_rows.values:
                    corriente_precio_row_rel_idx = \
                    precio_rows[precio_rows == 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA'].index[0]
                    corriente_precio_row_idx = corriente_precio_row_rel_idx
                    # Get precios
                    precios = excel_df.loc[corriente_precio_row_idx, 1:1 + len(cities) - 1].values.tolist()
                    # Collect data
                    for ciudad, precio in zip(cities, precios):
                        current_data_list.append({
                            'anio': anio,
                            'mes': mes,
                            'ciudad': ciudad,
                            'tipo': 'corriente',
                            'precio': precio
                        })
                else:
                    print(
                        f"Could not find 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA' row for corriente in {url}")
        except Exception as e:
            print(f"Error processing corriente data in {url}: {e}")

        # Process 'acpm' data
        try:
            n_rows = excel_df.shape[0]
            if n_rows > 55:
                # Check if B56 (pandas row 55, col 1) is empty
                if pd.isna(excel_df.iloc[55, 1]):
                    # 'CIUDAD' row is at row 57 (Excel numbering)
                    acpm_ciudad_row = 56
                    acpm_precio_row = 73
                else:
                    # 'CIUDAD' row is at row 56 (Excel numbering)
                    acpm_ciudad_row = 55
                    acpm_precio_row = 72
                # Check if the rows exist
                if n_rows > acpm_ciudad_row and n_rows > acpm_precio_row:
                    # Get cities
                    acpm_cities = excel_df.loc[acpm_ciudad_row, 1:].dropna().astype(str).str.strip().tolist()
                    # Get precios
                    precios = excel_df.loc[acpm_precio_row, 1:1 + len(acpm_cities) - 1].values.tolist()
                    # Collect data
                    for ciudad, precio in zip(acpm_cities, precios):
                        current_data_list.append({
                            'anio': anio,
                            'mes': mes,
                            'ciudad': ciudad,
                            'tipo': 'acpm',
                            'precio': precio
                        })
                else:
                    print(f"Not enough rows to process acpm data in {url}")
            else:
                print(f"Not enough rows to process acpm data in {url}")
        except Exception as e:
            print(f"Error processing acpm data in {url}: {e}")

        # After processing both 'corriente' and 'acpm', compute averages
        # Compute average precio_corriente
        corriente_precios = [d['precio'] for d in current_data_list if
                             d['tipo'] == 'corriente' and pd.notnull(d['precio'])]
        promedio_corriente = sum(corriente_precios) / len(corriente_precios) if corriente_precios else None
        # Compute average precio_acpm
        acpm_precios = [d['precio'] for d in current_data_list if d['tipo'] == 'acpm' and pd.notnull(d['precio'])]
        promedio_acpm = sum(acpm_precios) / len(acpm_precios) if acpm_precios else None
        # Add average row
        current_data_list.append({
            'anio': anio,
            'mes': mes,
            'ciudad': 'promedio',
            'tipo': 'corriente',
            'precio': promedio_corriente
        })
        current_data_list.append({
            'anio': anio,
            'mes': mes,
            'ciudad': 'promedio',
            'tipo': 'acpm',
            'precio': promedio_acpm
        })
        # Append current_data_list to data_list
        data_list.extend(current_data_list)

    # Create a DataFrame from the collected data
    result_df = pd.DataFrame(data_list)
    # Pivot the DataFrame to get 'precio_corriente' and 'precio_acpm' in separate columns
    result_df = result_df.pivot_table(
        index=['anio', 'mes', 'ciudad'],
        columns='tipo',
        values='precio',
        aggfunc='first'
    ).reset_index()
    # Flatten the MultiIndex columns
    result_df.columns.name = None
    result_df = result_df.rename(columns={'corriente': 'precio_corriente', 'acpm': 'precio_acpm'})
    result_df.to_csv(DF_PRECIOS_FPATH, index=False)
    return result_df


def get_vols(cities):
    if os.path.exists(DF_VOLS_FPATH):
        return pd.read_csv(DF_VOLS_FPATH)

    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
        f"WHERE subtipo_comprador IN ('{C1}', '{C2}', '{C3}') "
        f"AND producto IN ('{P1}', '{P2}') "
        f"AND anio_despacho IN ('2020', '2021', '2022', '2023', '2024')"
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 200000 "
    )

    df = fetch_socrata_datosgov(query, DB_ALIAS_MAYORISTAS, 20)
    df["volumen_total"] = pd.to_numeric(df["volumen_total"], errors="coerce")

    # Add "ALL CITIES" row
    nacional_row = df.groupby(["anio_despacho", "mes_despacho", "producto"], as_index=False)["volumen_total"].sum()
    nacional_row["municipio"] = "NACIONAL"

    # Concatenate the original DataFrame with the aggregated row
    df = pd.concat([df, nacional_row], ignore_index=True)
    df = df[df["municipio"].isin(cities)]
    df.to_csv(DF_VOLS_FPATH, index=False)
    return pd.read_csv(DF_VOLS_FPATH)


def clean_city_name(name):
    if pd.isnull(name):
        return name
    # Remove accents
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    # Remove punctuation
    name = re.sub(r'[^\w\s]', '', name)
    # Remove extra spaces
    name = ' '.join(name.split())
    # Convert to uppercase
    name = name.upper()
    return name


class ElasticidadDemandaLoad:
    def __init__(self):
        ensure_data_elasticidad_demanda()
        self.df_demanda = pd.read_csv(DF_DEMANDA_PATH)
        self.df_demanda['fecha'] = pd.to_datetime(
            self.df_demanda['anio'].astype(int).astype(str) + '-' + self.df_demanda['mes'].astype(int).astype(str),
            format='%Y-%m'
        )
        self.min_fecha = self.df_demanda['fecha'].min()
        self.max_fecha = self.df_demanda['fecha'].max()
        self.unique_fechas = sorted(self.df_demanda['fecha'].unique())
        self.ciudades = self.df_demanda['ciudad'].unique()
        self.fecha_indices = {i: fecha.strftime('%Y-%m') for i, fecha in enumerate(self.unique_fechas)}

