
import pandas as pd
from sodapy import Socrata
from os.path import exists
import unicodedata
import re

df_price = pd.read_csv("df_precios.csv")
#print(df1['ciudad'].unique())
#print(df1['ciudad'].nunique())
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
#print(len(dc_map))

df_price['ciudad'] = df_price['ciudad'].map(dc_map)
cities = df_price['ciudad'].unique()

def get_vols():

    if exists("df_vols.csv"):
        return pd.read_csv("df_vols.csv")

    client = Socrata("www.datos.gov.co", None, timeout=30)
    p1 = "CORRIENTE"
    p2 = "DIESEL"
    p3 = "EXTRA"
    c1 = "COMERCIALIZADOR INDUSTRIAL"
    c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
    c3 = "ESTACION DE SERVICIO FLUVIAL"

    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
        f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
        f"AND producto IN ('{p1}', '{p2}') "
        f"AND anio_despacho IN ('2020', '2021', '2022', '2023', '2024')"
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 200000 "
    )

    results = client.get("339g-zjac", query=query)
    df = pd.DataFrame.from_records(results)

    df["volumen_total"] = pd.to_numeric(df["volumen_total"], errors="coerce")

    # Add "ALL CITIES" row
    nacional_row = df.groupby(["anio_despacho", "mes_despacho", "producto"], as_index=False)["volumen_total"].sum()
    nacional_row["municipio"] = "NACIONAL"

    # Concatenate the original DataFrame with the aggregated row
    df = pd.concat([df, nacional_row], ignore_index=True)

    df = df[df["municipio"].isin(cities)]

    df.to_csv("df_vols.csv", index=False)
    print(len(df))
    return pd.read_csv("df_vols.csv")

df_vol = get_vols()

#print(df_vol)
#print(df_price)

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

# Assume df_vol is your volume DataFrame and df_price is your price DataFrame

# 1. Standardize city names in both DataFrames
df_vol['municipio'] = df_vol['municipio'].apply(clean_city_name)
df_price['ciudad'] = df_price['ciudad'].apply(clean_city_name)

# 2. Pivot the volume data to get 'vol_corriente' and 'vol_acpm' in separate columns
df_vol_pivot = df_vol.pivot_table(
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
    df_price,
    df_vol_pivot,
    on=['anio', 'mes', 'ciudad'],
    how='left'
)

# Display the merged DataFrame
print(df_merged.head())
df_merged.to_csv("demanda_df.csv", index=False)


