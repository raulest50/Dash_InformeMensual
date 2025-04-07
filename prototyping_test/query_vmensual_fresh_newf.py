
import pandas as pd
import services.general as general
DB_ALIAS_VOL_MAYORISTAS = "339g-zjac"

def get_query_vmensual():
    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
        f"WHERE subtipo_comprador IN ('{general.C1}', '{general.C2}', '{general.C3}') "
        f"AND producto IN ('{general.P1}', '{general.P2}', '{general.P3}') "
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 250000"
    )
    return query


df_vmensual_newf = general.fetch_socrata_datosgov(get_query_vmensual(), DB_ALIAS_VOL_MAYORISTAS, 20)
df_vmensual_newf.to_csv("vmensual_7_4_2025.csv.csv", index=False)

