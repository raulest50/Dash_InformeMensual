# standar lib imports
import os

# 3rd party imports
from datetime import datetime
from pytz import timezone
import pandas as pd

import services.general as general


DATA_DIR_INF_MENSUAL = 'data/informe_mensual'
VMENSUAL_FILEPATH = os.path.join(DATA_DIR_INF_MENSUAL, 'vmensual.csv')

DB_ALIAS_VOL_MAYORISTAS = "339g-zjac"

def ensure_data_vmensual():
    status = check_data_status()
    if status == general.SCRATCH:
        scratch_initialization()
    elif status == general.OUTDATED:
        update_data()
    elif status == general.UPTODATE:
        pass


def check_data_status():
    status = general.SCRATCH
    if os.path.exists(DATA_DIR_INF_MENSUAL) and os.path.exists(VMENSUAL_FILEPATH):
        if it_is_outdated():
            status = general.OUTDATED
        else:
            status = general.UPTODATE
    return status


def it_is_outdated():
    df = pd.read_csv(VMENSUAL_FILEPATH)
    df['anio_despacho'] = df['anio_despacho'].astype(int)
    df['mes_despacho'] = df['mes_despacho'].astype(int)
    latest_year = df['anio_despacho'].max()  # Find the maximum year
    df_latest_year = df[df['anio_despacho'] == latest_year]
    latest_month = df_latest_year['mes_despacho'].max()

    # Get the current date and time in UTC-5 (Bogota time)
    bogota_tz = timezone('America/Bogota')
    current_datetime = datetime.now(bogota_tz)
    current_year = current_datetime.year
    current_month = current_datetime.month
    if latest_year != current_year or latest_month != current_month:
        return True  # Data is out of date
    else:
        return False  # Data is up-to-date


def scratch_initialization():
    os.makedirs(DATA_DIR_INF_MENSUAL, exist_ok=True)
    df = general.fetch_socrata_datosgov(get_query_vmensual(), DB_ALIAS_VOL_MAYORISTAS, 20)
    df.to_csv(VMENSUAL_FILEPATH, index=False)


def update_data():
    scratch_initialization()


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
        ensure_data_vmensual()
        self.df = pd.read_csv(VMENSUAL_FILEPATH)

    def format_zdf_list(self, zdf_list, n=10):
        return '\n'.join(', '.join(zdf_list[i:i + n]) for i in range(0, len(zdf_list), n))

