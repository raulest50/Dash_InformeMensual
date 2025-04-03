

import pandas as pd


df_vmensual = pd.read_csv("../data/informe_mensual/vmensual.csv")

df_vmensual['producto'] = df_vmensual['producto'].replace('CORRIENTE', 'GASOLINA MOTOR CORRIENTE')
df_vmensual['producto'] = df_vmensual['producto'].replace('EXTRA', 'GASOLINA MOTOR EXTRA')
df_vmensual['producto'] = df_vmensual['producto'].replace('DIESEL', 'ACPM')

df_vmensual.to_csv("../data/informe_mensual/vmensual_ported.csv", index=False)
