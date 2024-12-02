
from datetime import datetime, timedelta
from pytz import timezone

from init_service import InitService


class InformeOnlineService(InitService):

    DB_ALIAS_VOL_MAYOTISTAS = "339g-zjac"


    def __init__(self):
        pass

    def buildQuery(self):
        today = datetime.today().strftime('%Y-%m-%d')
        sixty_days_ago = (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')
        query = (
                    f"SELECT SUM(volumen_despachado) as volumen_total, producto, fecha_despacho "
                    f"WHERE subtipo_comprador IN ('{self.C1}', '{self.C2}', '{self.C3}') "
                    f"AND producto IN ('{self.P1}', '{self.P2}', '{self.P3}') "
                    f"AND fecha_despacho BETWEEN '{sixty_days_ago}' AND '{today}' "
                    f"GROUP BY producto, fecha_despacho "
                    f"ORDER BY fecha_despacho ASC "
                    f"LIMIT 20000 "
                )
        return query
    def getDataFrame_OnlineReport(self):
        query = self.buildQuery()
        df = self.fetch_socrata_datosgov(self, db_alias=self.DB_ALIAS_VOL_MAYOTISTAS, query=query, t_out=20)
        return df