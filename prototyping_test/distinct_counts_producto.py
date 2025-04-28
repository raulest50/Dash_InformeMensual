

import pandas as pd
from sodapy import Socrata
import services.general as general

bd_mayoristas = "339g-zjac"
bd_eds = "fbht-2fzd"


client = Socrata("www.datos.gov.co", None)

def get_query_vmensual():
    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
        f"WHERE subtipo_comprador IN ('{general.C1}', '{general.C2}', '{general.C3}') "
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 250000"
    )
    return query

def get_product_counts():
    query = (
        "SELECT subtipo_comprador, COUNT(*) AS count "
        "GROUP BY subtipo_comprador "
        "ORDER BY count DESC"
    ).format(general.C1, general.C2, general.C3)
    return query


# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
#results = client.get("339g-zjac", limit=2000)

results = client.get(bd_mayoristas, query=get_product_counts())

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
print(results_df)

results_df.to_csv("test.csv")


#print(results_df['producto'].value_counts())


"""
los tipos de agentes compradores en la bd mayoristas

                                   subtipo_comprador    count
0                    ESTACION DE SERVICIO AUTOMOTRIZ  5443924
1                         COMERCIALIZADOR INDUSTRIAL   383566
2                   ESTACION DE SERVICIO DE AVIACION    84558
3                               CON INSTALACION FIJA    70007
4                      ESTACION DE SERVICIO MARITIMA    31565
5                       ESTACION DE SERVICIO FLUVIAL    18265
6  DISTRIBUIDOR MAYORISTA DE QUEMADORES INDUSTRIALES    14993
7     CON INTALACION FIJA VOLUMEN MENOR A 20.000 GLS    10487
8                           TEMPORAL CON INSTALACION    10287
9    CON INSTALACION FIJA VOLUMEN MENOR A 20.000 GLS       46

"""
