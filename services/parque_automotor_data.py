
import os
import pandas as pd
from data_integrity.general import fetch_socrata_datosgov

DATA_DIR_INF_MENSUAL = 'data/pq_motor'
DF_MOTOR_FPATH = os.path.join(DATA_DIR_INF_MENSUAL, 'df_motor.csv')

# https://www.datos.gov.co/Transporte/CRECIMIENTO-DEL-PARQUE-AUTOMOTOR-RUNT2-0/u3vn-bdcy/about_data
BD_ALIAS = "u3vn-bdcy"


def ensure_pq_motor_data():
    os.makedirs(DATA_DIR_INF_MENSUAL, exist_ok=True)
    if os.path.exists(DF_MOTOR_FPATH):
        print(f"{__name__} : loaded local data ")
        return
    df = fetch_socrata_datosgov(get_query(), BD_ALIAS, 20)
    df.to_csv(DF_MOTOR_FPATH, index=False)


def get_query():
    query = (
        f"SELECT nombre_servicio, cantidad, fecha_de_registro "
        f"WHERE estado_del_vehiculo = 'ACTIVO' "
        f"GROUP BY nombre_servicio, cantidad, fecha_de_registro "
        f"LIMIT 250000"
    )
    return query


class PqMotorLoad:

    def __init__(self):
        print("inicializando data parque automotor")
        ensure_pq_motor_data()
        self.df = pd.read_csv(DF_MOTOR_FPATH)
        self.df['fecha_de_registro'] = self.df['fecha_de_registro'].astype(int)
        lista_nservice = list(self.df['nombre_servicio'].unique()) + ['TODOS']
        self.lista_servicios = [{'label': x, 'value': x} for x in lista_nservice]
        self.min_year = self.df['fecha_de_registro'].min()
        self.max_year = self.df['fecha_de_registro'].max()


