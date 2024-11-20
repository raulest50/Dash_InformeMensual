

import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None, timeout=30)

p1 = "CORRIENTE"
p2 = "DIESEL"
p3 = "EXTRA"

c1 = "COMERCIALIZADOR INDUSTRIAL"
c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
c3 = "ESTACION DE SERVICIO FLUVIAL"

query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, departamento_proveedor, municipio_proveedor, departamento, municipio "
        f"WHERE subtipo_comprador = '{c1}' "
        f"AND producto = '{p2}' "
        f"AND anio_despacho = '2024' "
        f"GROUP BY anio_despacho, mes_despacho, producto, departamento_proveedor, municipio_proveedor, departamento, municipio "
        f"ORDER BY mes_despacho ASC "
        f"LIMIT 250000 "
        )

results = client.get("339g-zjac", query=query)
df = pd.DataFrame.from_records(results)
df.to_csv("c_ind_data2.csv", index=False)

print(df)
