
import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None)

p1 = "CORRIENTE"
p2 = "DIESEL"
p3 = "EXTRA"

c1 = "COMERCIALIZADOR INDUSTRIAL"
c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
c3 = "ESTACION DE SERVICIO FLUVIAL"

query = (
        f"SELECT SUM(beneficio) as beneficio, municipio, departamento "
        f"GROUP BY municipio, departamento "
        f"ORDER BY municipio ASC "
        f"LIMIT 250000 "
        )

query_dcount = (
    f"SELECT COUNT(DISTINCT municipio) as distinct_municipios "
)

results = client.get("shbt-hqy9", query=query)

df = pd.DataFrame.from_records(results)

print(df)

def print_1(df):
        print(f"dataframe: \n {df}")
        print("-------\n\n\n")
        print(f"municipios : \n  {df['municipio'].unique()}")
        print("-------\n\n\n")
        print(f" LEN municipios : \n  {len(df['municipio'].unique())}")
        print("-------\n\n\n")
        print(f"departamentos : \n  {df['departamento'].unique()}")
        print("-------\n\n\n")
        ndf = df.copy().drop(columns=['beneficio'])
        ndf.to_csv("lista_1_zdf.csv", index=False)

print_1(df)

"""

FROM https://www.datos.gov.co/Minas-y-Energ-a/Beneficio-de-estaciones-de-servicio-en-zona-de-fro/shbt-hqy9/about_data

Conjunto de datos con los registros de asignación o beneficio máximo a despachar de combustibles
 desde un mayorista a una estación de servicio en zona de frontera.

Conjunto de datos consumo de combustibles con beneficios sobre el precio de venta al consumidor final para los 171 
municipios ubicados en 12 departamentos del país, los cuales son considerados como zona de frontera de 
acuerdo con la Ley 191 de 1995.

"""