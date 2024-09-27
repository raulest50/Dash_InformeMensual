
import methods
import pandas as pd
import Constants
from sodapy import Socrata

from methods import c1, c2, c3, p1, p2, p3


def distinct_count(departamento):

    cliente = Socrata("www.datos.gov.co", None, timeout=10)

    query = (
        f"SELECT DISTINCT municipio "
        f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
        f"AND producto IN ('{p1}', '{p2}', '{p3}') "
        f"AND departamento = '{departamento}' "
        f"GROUP BY municipio "
        f"ORDER BY municipio ASC "
        f"LIMIT 1000 "
    )

    results = cliente.get("339g-zjac", query=query)
    df = pd.DataFrame.from_records(results)

    print(df)
    df.to_csv('municipios_departamento_test.csv')


def get_without_zdf():

    cliente = Socrata("www.datos.gov.co", None, timeout=20)

    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio, departamento "
        f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
        f"AND producto IN ('{p1}', '{p2}', '{p3}') "
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio, departamento "
        f"ORDER BY anio_despacho, mes_despacho, municipio, departamento ASC "
        f"LIMIT 200000 "
    )

    results = cliente.get("339g-zjac", query=query)
    df = pd.DataFrame.from_records(results)

    filtered_df = df[~df['municipio'].isin(Constants.zdf_list)]

    print(filtered_df)

    filtered_df.to_csv('vol_ts_no_zdf.csv', index=False)

get_without_zdf()