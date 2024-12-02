
import os
import pickle

import requests
from bs4 import BeautifulSoup
import pandas as pd
from init_service import InitService


class EstructuraPreciosService(InitService):

    DATA_DIR_ESTRUCTURA_PRECIOS = 'data/estructura_precios'
    FNAME_DF_DICT = 'df_dictionary.pkl'
    DICT_FILEPATH = os.path.join(DATA_DIR_ESTRUCTURA_PRECIOS, FNAME_DF_DICT)

    def __init__(self):
        status = self.check_data_status()
        if status == self.SCRATCH:
            self.df_dictionary, self.columnas_ciudades, self.lista_informes = self.scratch_initialization()
        if status == self.OUTDATED:
            self.df_dictionary, self.columnas_ciudades, self.lista_informes = self.scratch_initialization()
        if status == self.UPTODATE:
            self.df_dictionary, self.columnas_ciudades, self.lista_informes = self.scratch_initialization()

    def check_data_status(self):
        status = self.SCRATCH
        if os.path.exists(self.DATA_DIR_ESTRUCTURA_PRECIOS) & os.path.exists(self.DICT_FILEPATH):
            if self.it_is_outdated():
                status = self.OUTDATED
            else:
                status = self.UPTODATE
        return status

    def scratch_initialization(self):
        os.makedirs(self.DATA_DIR_ESTRUCTURA_PRECIOS)  # se crea folder en carpeta persistente render.com
        lista_informes_tuple = self.scrape_url_list()
        lista_informes = [{'label': item[0], 'value': item[0]} for item in lista_informes_tuple]
        df_dictionary = self.get_dataframes_dict(lista_informes, lista_informes_tuple)
        with open(self.DICT_FILEPATH, 'wb') as file:
            pickle.dump(df_dictionary, file)
        columnas_ciudades = df_dictionary[lista_informes[0]['value']][0][0].columns[1:]
        return df_dictionary, columnas_ciudades, lista_informes

    def get_dataframes_dict(self, lista_informes, lista_informes_tuple):
        r = {}
        for name, url in lista_informes_tuple:
            r[name] = [self.get_data_frames_from_excel_url(url, self.DATA_DIR_ESTRUCTURA_PRECIOS)]
        return r

    def it_is_outdated(self):
        pass

    """
    scrapea la pagina donde se pueden ver los precios de referencia y obtiene una lista con la estructura:
    [ (texto, link (href)) ]
    """
    def scrape_url_list(self):
        # URL of the webpage
        url = "https://www1.upme.gov.co/sipg/Paginas/Estructura-precios-combustibles.aspx"

        # Fetch the HTML content of the page
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links in the page
        links = soup.find_all('a', href=True)

        # Extract (text, link) pairs and filter those ending with .xlsx
        xlsx_links = [(link.text.strip(), link['href']) for link in links if link['href'].endswith('.xlsx')]
        return xlsx_links

    def get_data_frames_from_excel_url(self, excel_url, folder):
        # URL of the .xlsx file
        # url = xlsx_links[0][1]
        # Fetch the content of the file
        response = requests.get(excel_url)
        response.raise_for_status()  # Ensure the request was successful
        excel_file = 'temp_file.xlsx'
        excel_filepath = os.path.join(folder, excel_file)

        # Save the content to a temporary file
        with open(excel_filepath, 'wb') as temp_file:
            temp_file.write(response.content)
        df_precios_corriente = self.excel_file_precios_to_dframe(excel_filepath, 32, 19, 19)
        df_precios_acpm = self.excel_file_precios_to_dframe(excel_filepath, 56, 18, 19)
        return df_precios_corriente, df_precios_acpm

    def excel_file_precios_to_dframe(self, excel_file, skip, rows, columns):
        df = pd.read_excel(excel_file, header=None, skiprows=skip)# Read the Excel file into a DataFrame
        column_headers_corriente = df.iloc[0, 0:columns].tolist() # Extract the column headers from the first row of the relevant slice
        # df_corriente = df.iloc[32:51, 0:19].copy()
        df_corriente = df.iloc[1:rows, 0:columns].copy()
        df_corriente.columns = column_headers_corriente
        return df_corriente
    