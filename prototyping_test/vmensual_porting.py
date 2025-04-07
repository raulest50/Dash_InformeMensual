

import pandas as pd


df_vmensual = pd.read_csv("../data/informe_mensual/vmensual.csv")
print(df_vmensual['producto'].value_counts())

df_vmensual['producto'] = df_vmensual['producto'].replace('CORRIENTE', 'GASOLINA MOTOR CORRIENTE')
df_vmensual['producto'] = df_vmensual['producto'].replace('DIESEL', 'BIODIESEL CON MEZCLA')
df_vmensual['producto'] = df_vmensual['producto'].replace('EXTRA', 'GASOLINA MOTOR EXTRA')

df_vmensual.to_csv("../data/informe_mensual/vmensual_ported.csv", index=False)

"""
diferentes tipos de productos en vmensual

producto
CORRIENTE    55071
DIESEL       54083
EXTRA        13334
Name: count, dtype: int64
"""




"""
diferentes tipos de productos en la base abierta de mayoristas:

                   producto    count
0  GASOLINA MOTOR CORRIENTE  2918444
1      BIODIESEL CON MEZCLA  2853848
2      GASOLINA MOTOR EXTRA   160664
3                    JET A1    91817
4             DIESEL MARINO    37984
5                    AVIGAS     2475
6     FUEL OIL- COMBUSTOLEO     1768
7             FUEL OIL Nº 4      362
8                  KEROSENE      322
9        BIODIESEL DE PALMA       14
"""