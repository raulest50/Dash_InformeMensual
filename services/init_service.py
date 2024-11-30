

import pandas as pd
import requests
from sodapy import Socrata

class InitService:
    # Constants for data statuses
    SCRATCH = 0
    OUTDATED = 1
    UPTODATE = 2

    P1 = "CORRIENTE"
    P2 = "DIESEL"
    P3 = "EXTRA"

    C1 = "COMERCIALIZADOR INDUSTRIAL"
    C2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
    C3 = "ESTACION DE SERVICIO FLUVIAL"

    # colores Institucionales
    VERDE = "#41B75C"
    AZUL = "#0D6ABF"
    GRIS = "#808080"

    def fetch_socrata_datosgov(self, query, db_alias, t_out):
        cliente = Socrata("www.datos.gov.co", None, timeout=t_out)
        not_success = True
        while not_success:
            try:
                results = cliente.get(db_alias, query=query)
                df = pd.DataFrame.from_records(results)
                return df
            except requests.exceptions.Timeout:
                print("time out exception")
                not_success = True