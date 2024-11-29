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
    def __init__(self,):
        pass

    def checkDataStatus(self):
        status = self.SCRATCH
        if os.path.exists(self.DATA_DIR_INF_MENSUAL) & os.path.exists(self.VMENSUAL_FILEPATH):
            if self.it_is_outdated():
                status = self.OUTDATED
            else:
                status = self.UPTODATE
        return status

    def scratchInitialization(self):
        df = self.fetch_socrata_datosgov(self, self.build_query(), self.DB_ALIAS_VOL_MAYOTISTAS, 10)
        df.to_csv(self.VMENSUAL_FILEPATH, index=False)

    def updateData(self):
        print("InformeMensual: Updating data...")

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