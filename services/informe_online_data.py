
from datetime import datetime, timedelta
import services.general as general


DB_ALIAS_VOL_MAYORISTAS = "339g-zjac"



def ensure_ionline_data():
    pass


def build_query():
    today = datetime.today().strftime('%Y-%m-%d')
    sixty_days_ago = (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')
    query = (
                f"SELECT SUM(volumen_despachado) as volumen_total, producto, fecha_despacho "
                f"WHERE subtipo_comprador IN ('{general.C1}', '{general.C2}', '{general.C3}') "
                f"AND producto IN ('{general.P1}', '{general.P2}', '{general.P3}') "
                f"AND fecha_despacho BETWEEN '{sixty_days_ago}' AND '{today}' "
                f"GROUP BY producto, fecha_despacho "
                f"ORDER BY fecha_despacho ASC "
                f"LIMIT 20000 "
            )
    return query


def get_data_frame_online_report():
    df = general.fetch_socrata_datosgov(build_query(), DB_ALIAS_VOL_MAYORISTAS, 20)
    return df

