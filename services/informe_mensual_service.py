# standar lib imports
import os

# 3rd party imports
from datetime import datetime
from pytz import timezone
import pandas as pd

# local application imports
from init_service import InitService

class InformeMensualService(InitService):

    DATA_DIR_INF_MENSUAL = 'data/informe_mensual'
    VMENSUAL_FILEPATH = os.path.join(DATA_DIR_INF_MENSUAL, 'vmensual.csv')

    DB_ALIAS_VOL_MAYOTISTAS = "339g-zjac"

    def __init__(self):
        self.df = self.resolve_df_vmensual()

    def resolve_df_vmensual(self):
        try:
            status = self.check_data_status()
            if status == self.SCRATCH:
                return self.scratch_initialization()
            elif status == self.OUTDATED:
                return self.update_data()
            elif status == self.UPTODATE:
                print("Data vmensual is up to date")
                return pd.read_csv(self.VMENSUAL_FILEPATH)
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_data_status(self):
        status = self.SCRATCH
        if os.path.exists(self.DATA_DIR_INF_MENSUAL) & os.path.exists(self.VMENSUAL_FILEPATH):
            if self.it_is_outdated():
                status = self.OUTDATED
            else:
                status = self.UPTODATE
        return status

    def scratch_initialization(self):
        df = self.fetch_socrata_datosgov(self, query=self.build_query(), db_alias=self.DB_ALIAS_VOL_MAYOTISTAS, t_out=20)
        df.to_csv(self.VMENSUAL_FILEPATH, index=False)
        return df

    def update_data(self):
        return self.scratch_initialization()

    def it_is_outdated(self):
        df = pd.read_csv(self.VMENSUAL_FILEPATH)
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
            return True  # Data is ou
        else:
            return False  # Data is up-to-date

    def build_query(self):
        query = (
            f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
            f"WHERE subtipo_comprador IN ('{self.C1}', '{self.C2}', '{self.C3}') "
            f"AND producto IN ('{self.P1}', '{self.P2}', '{self.P3}') "
            f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
            f"ORDER BY anio_despacho ASC "
            f"LIMIT 250000"
        )
        return query

    def format_zdf_list(zdf_list, n=10):
        return '\n'.join(', '.join(zdf_list[i:i + n]) for i in range(0, len(zdf_list), n))

