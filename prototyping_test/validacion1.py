
"""
En la base de datos abierta de mayoristas los productos de interes se han designado como
EXTRA, DIESEL, CORRIENTE. sin embargo a inicios del 2025, se cambiaron las designaciones
a GASOLINA MOTOR CORRIENTE, BIODIESEL CON MEZCLA, GASOLINA MOTOR EXTRA. esto me genero dudas con
los datos pero ya sabemos que DIESEL ACPM Y BIODIESEL CON MEZCLA son lo mismo y en efecto
los valores de volumen despachado cuadran comparando con el dataframe vmensual viejo
vs un dataframe fresco de la base de datos comparando 2024 solamente, que por ahora es
lo que nos interesa.

la conclusion de este script es que si cuadran para corriente, diesel y extra, con muy
ligeras variaciones que son perfectamente aceptables.
"""

import pandas as pd

corriente_0 = "CORRIENTE"
corriente_f = "GASOLINA MOTOR CORRIENTE"

acpm_0 = "DIESEL"
acpm_f = "BIODIESEL CON MEZCLA"

extra_0 = "EXTRA"
extra_f = "GASOLINA MOTOR EXTRA"

df0 = pd.read_csv("../data/informe_mensual/old/vmensual_01_2025(old_f).csv")

dff = pd.read_csv("./vmensual_fresh.csv")

df0_24 = df0[(df0["anio_despacho"] == 2024) & (df0["producto"] == acpm_0)]
dff_24 = dff[(dff["anio_despacho"] == 2024) & (dff["producto"] == acpm_f)]

df0_24 = df0_24.groupby("mes_despacho")["volumen_total"].sum()
df0_24 = df0_24/1e6

dff_24 = dff_24.groupby("mes_despacho")["volumen_total"].sum()
dff_24 = dff_24/1e6

df0_24 = df0_24.reset_index()
dff_24 = dff_24.reset_index()

# Merge the two DataFrames on 'mes_despacho'
merged_df = pd.merge(df0_24, dff_24, on="mes_despacho", how="outer", suffixes=('_df0', '_dff'))

print(merged_df)



"""

EXTRA :
    mes_despacho  volumen_total_df0  volumen_total_dff
0              1           3.879581           3.877371
1              2           3.666724           3.664514
2              3           3.871556           3.869344
3              4           3.972191           3.969979
4              5           3.955165           3.954059
5              6           3.965784           3.962466
6              7           4.051945           4.049733
7              8           4.388261           4.387561
8              9           4.245466           4.242152
9             10           4.643663           4.642559
10            11           4.529238           4.529238
11            12           5.526560           5.518724

CORRIENTE:
mes_despacho  volumen_total_df0  volumen_total_dff
0              1         185.506804         185.405838
1              2         173.069848         172.966157
2              3         179.312034         179.204924
3              4         178.869818         178.761626
4              5         181.650561         181.547289
5              6         175.003985         174.896977
6              7         183.052854         182.936204
7              8         182.692117         182.587544
8              9         175.355860         175.268071
9             10         187.821636         187.701448
10            11         181.047743         180.867259
11            12         204.637945         204.319270

ACPM:
mes_despacho  volumen_total_df0  volumen_total_dff
0              1         157.630172         157.614018
1              2         160.528078         160.506545
2              3         157.240143         157.216198
3              4         168.557274         168.541609
4              5         164.245852         164.218725
5              6         155.576250         155.554682
6              7         171.340998         171.318176
7              8         170.530507         170.496048
8              9         160.988200         160.970304
9             10         176.324152         176.293666
10            11         175.162125         175.042196
11            12         173.196532         173.002537

los datos de un fresh query parecen confiables, almenos para hacer una comparacion 
para el 2024 vs 2025, ya que concuerdan con los datos validados del año pasado y para
el presente año no hay con que constrastar asi que por definicion toca confiar
en ellos para el 2025.
"""