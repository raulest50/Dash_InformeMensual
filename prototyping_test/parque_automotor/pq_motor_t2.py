

import pandas as pd

df = pd.read_csv("pq_motor.csv")

print(len(df['nombre_departamento'].unique()))
print(df['fecha_de_registro'].unique())
print(len(df['nombre_municipio'].unique()))
print(df['nombre_servicio'].unique())
print(df['estado_del_vehiculo'].unique())
print(df['nombre_de_la_clase'].unique())

