
import requests
from sodapy import Socrata
import pandas as pd

p1 = "CORRIENTE"
p2 = "DIESEL"
p3 = "EXTRA"

c1 = "COMERCIALIZADOR INDUSTRIAL"
c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
c3 = "ESTACION DE SERVICIO FLUVIAL"

# colores Institucionales
verde = "#41B75C"
azul = "#0D6ABF"
gris = "#808080"


def getDataFrame():
    cliente = Socrata("www.datos.gov.co", None, timeout=10)

    not_success = True

    while not_success:
        try:
            query = (
                f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto "
                f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
                f"AND producto IN ('{p1}', '{p2}', '{p3}') "
                f"GROUP BY anio_despacho, mes_despacho, producto "
                f"ORDER BY anio_despacho ASC "
                f"LIMIT 5000 "
            )

            results = cliente.get("339g-zjac", query=query)
            df = pd.DataFrame.from_records(results)
            return df
        except requests.exceptions.Timeout:
            print("time out exception")
            not_success = True

"""dataframe superset"""
def getDataFrame_suset():
    cliente = Socrata("www.datos.gov.co", None, timeout=10)

    not_success = True

    while not_success:
        try:
            query = (
                f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
                f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
                f"AND producto IN ('{p1}', '{p2}', '{p3}') "
                f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
                f"ORDER BY anio_despacho ASC "
                f"LIMIT 250000 "
            )

            results = cliente.get("339g-zjac", query=query)
            df = pd.DataFrame.from_records(results)
            return df
        except requests.exceptions.Timeout:
            print("time out exception")
            not_success = True


def format_zdf_list(zdf_list, n=10):
    return '\n'.join(', '.join(zdf_list[i:i + n]) for i in range(0, len(zdf_list), n))