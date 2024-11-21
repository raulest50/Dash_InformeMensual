
import pandas as pd
from sodapy import Socrata



"""
El problema de estas base de datos abiertas de precios de combustible es que hace mucho tiempo que
no se actualizan, los datos ya son muy viejos, pro ejemplo esta solo tiene informacion hasta el 2022
"""

p1 = "CORRIENTE"
p2 = "DIESEL"
p3 = "EXTRA"

municipios_list = [
    "BOGOTA, D.C.",
    "MEDELLIN",
    "CALI",
    "CARTAGENA DE INDIAS",
    "BARRANQUILLA",
    "BUCARAMANGA",
    "VALLEDUPAR",
    "SAN JOSE DE CUCUTA",
    "PEREIRA",
    "IBAGUE",
    "VILLAVICENCIO",
    "PASTO"]

def see_top12_vol():
    import pandas as pd
    from sodapy import Socrata
    client = Socrata("www.datos.gov.co", None, timeout=30)
    c1 = "COMERCIALIZADOR INDUSTRIAL"
    c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
    c3 = "ESTACION DE SERVICIO FLUVIAL"
    p1 = "CORRIENTE"
    p2 = "DIESEL"
    p3 = "EXTRA"
    # Format the list for the SQL query
    municipios_str = ', '.join(f"'{municipio}'" for municipio in municipios_list)
    query = (
        f"SELECT municipio, anio_despacho, mes_despacho, producto, SUM(volumen_despachado) as sum_volumen "
        f"WHERE producto IN ('{p1}', '{p2}', '{p3}') "
        f"AND subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
        f"AND municipio IN ({municipios_str})"
        f"GROUP BY municipio, anio_despacho, mes_despacho, producto "
        f"ORDER BY municipio, anio_despacho, mes_despacho, producto "
        f"LIMIT 120000 "
    )
    results = client.get("339g-zjac", query=query)
    df = pd.DataFrame.from_records(results)
    df.to_csv("demanda_top12.csv", index=False)
    print(df)


def see_bd_precios():
    client = Socrata("www.datos.gov.co", None)
    query = (
        f"SELECT municipio, periodo, mes, producto, precio "
        f"GROUP BY  "
        f"ORDER BY municipio, periodo, mes, producto, precio "
        f"LIMIT 120000 "
    )
    results = client.get("gjy9-tpph", query=query)
    results_df = pd.DataFrame.from_records(results)
    results_df.to_csv("precios_month.csv", index=False)
    print(results_df)

def see_oldest():
    import pandas as pd
    from sodapy import Socrata
    client = Socrata("www.datos.gov.co", None, timeout=30)
    c1 = "COMERCIALIZADOR INDUSTRIAL"
    c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
    c3 = "ESTACION DE SERVICIO FLUVIAL"
    p1 = "CORRIENTE"
    p2 = "DIESEL"
    p3 = "EXTRA"
    # Format the list for the SQL query
    municipios_str = ', '.join(f"'{municipio}'" for municipio in municipios_list)
    query = (
        f"SELECT municipio, anio_despacho, mes_despacho, producto, SUM(volumen_despachado) as sum_volumen "
        f"WHERE producto IN ('{p1}', '{p2}', '{p3}') "
        f"AND subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
        f"AND municipio IN ({municipios_str}) "
        f"GROUP BY municipio, anio_despacho, mes_despacho, producto "
        f"ORDER BY municipio, anio_despacho, mes_despacho, producto "
        f"LIMIT 120000 "
    )
    results = client.get("339g-zjac", query=query)
    df = pd.DataFrame.from_records(results)
    # Find the oldest year and month
    oldest_date = df.sort_values(by=['anio_despacho', 'mes_despacho']).iloc[0]

    # Display the result
    print("Oldest year and month:", oldest_date['anio_despacho'], oldest_date['mes_despacho'])
    print(df)

see_oldest()
