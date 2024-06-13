import pandas as pd
from sodapy import Socrata

reporte_anio = 2024
reporte_trim = 1

client = Socrata("www.datos.gov.co", None, timeout=30)

p1 = "CORRIENTE"
p2 = "DIESEL"
p3 = "EXTRA"

c1 = "COMERCIALIZADOR INDUSTRIAL"
c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
c3 = "ESTACION DE SERVICIO FLUVIAL"

anio_2 = str(reporte_anio)
anio_1 = str(reporte_anio-1)

query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, producto "
        f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
        f"AND producto IN ('{p1}', '{p2}', '{p3}') "
        f"AND mes_despacho = '05' "
        f"GROUP BY anio_despacho, producto "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 2000 "
        )

results = client.get("339g-zjac", query=query)
df = pd.DataFrame.from_records(results)

print(df)