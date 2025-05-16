# standar lib imports
import os

# 3rd party imports
from datetime import datetime
from pytz import timezone
import pandas as pd

import services.general as general

DB_ALIAS_VOL_MAYORISTAS = "339g-zjac"


def get_vmensual_fpath():
    if __name__ == "__main__":
        DATA_DIR_INF_MENSUAL_MAIN = '../data/informe_mensual/'
        return os.path.join(DATA_DIR_INF_MENSUAL_MAIN, 'vmensual.parquet')
    else:
        DATA_DIR_INF_MENSUAL = 'data/informe_mensual'
        return os.path.join(DATA_DIR_INF_MENSUAL, 'vmensual.parquet')


def get_vmensual():
    VMENSUAL_FILEPATH = get_vmensual_fpath()
    if os.path.exists(VMENSUAL_FILEPATH):
        return pd.read_parquet(VMENSUAL_FILEPATH, engine='pyarrow')
    else:
        print("scratch intilizacion for vmensual.parquet")
        return pd.DataFrame()

def data_integrity():
    df_old = get_vmensual()
    print(f"df_old len: {len(df_old)}")

    df_new = general.fetch_socrata_datosgov(get_query_vmensual(), DB_ALIAS_VOL_MAYORISTAS, 20)
    print(df_new)
    df_new["anio_despacho"] = pd.to_numeric(df_new["anio_despacho"], errors="coerce")
    df_new["mes_despacho"] = pd.to_numeric(df_new["mes_despacho"], errors="coerce")
    df_new["volumen_total"] = pd.to_numeric(df_new["volumen_total"], errors="coerce")

    print(f"df_new len: {len(df_new)}")

    KEYS = ["anio_despacho", "mes_despacho", "producto", "municipio"]
    df_union = (
        pd.concat([df_old, df_new], ignore_index=True)
        .drop_duplicates(subset=KEYS, keep="last")
    )

    print(f"df_union len: {len(df_union)}")
    df_union.to_parquet(get_vmensual_fpath(), engine='pyarrow', index=False)


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


class InformeMensualLoad:
    def __init__(self):
        self.df = get_vmensual()

    def format_zdf_list(self, zdf_list, n=10):
        return '\n'.join(', '.join(zdf_list[i:i + n]) for i in range(0, len(zdf_list), n))


if __name__ == "__main__":
    data_integrity()
