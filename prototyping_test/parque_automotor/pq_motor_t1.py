
import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None)
query = (
        f"SELECT nombre_departamento, nombre_municipio, nombre_servicio, estado_del_vehiculo, nombre_de_la_clase, "
        f"cantidad, fecha_de_registro "
        f"GROUP BY nombre_departamento, nombre_municipio, nombre_servicio, estado_del_vehiculo, nombre_de_la_clase, "
        f"cantidad, fecha_de_registro "
        f"LIMIT 250000"
    )
results = client.get("u3vn-bdcy", query=query)
df = pd.DataFrame.from_records(results)
df.to_csv("pq_motor.csv", index=False)

