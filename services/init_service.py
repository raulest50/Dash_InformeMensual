

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

    def inicializar(self):
        """
        Shared initialization logic for all service classes.
        """
        try:
            status = self.check_data_status()
            if status == self.SCRATCH:
                self.scratch_initialization()
            elif status == self.OUTDATED:
                self.update_data()
            elif status == self.UPTODATE:
                print("Data is up to date")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_data_status(self):
        """
        To be implemented by child classes to determine the data status.
        """
        raise NotImplementedError("Subclasses must implement checkDataStatus")

    def scratch_initialization(self):
        """
        To be implemented by child classes for scratch initialization.
        """
        raise NotImplementedError("Subclasses must implement scratchInitialization")

    def update_data(self):
        """
        To be implemented by child classes for data updates.
        """
        raise NotImplementedError("Subclasses must implement updateData")


    def it_is_outdated(self):
        """
        To be implemented by child classes for data updates.
        """
        raise NotImplementedError("Subclasses must implement it_is_outdated")


    def fetch_socrata_datosgov(self, query, t_out, db_alias):
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