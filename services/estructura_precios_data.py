
import os
import pickle

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import services.general as general

DATA_DIR_ESTRUCTURA_PRECIOS = 'data/estructura_precios'
DF_DICT_FNAME = 'df_dictionary.pkl'
DICT_FILEPATH = os.path.join(DATA_DIR_ESTRUCTURA_PRECIOS, DF_DICT_FNAME)

URL_LIST_FPATH = os.path.join(DATA_DIR_ESTRUCTURA_PRECIOS, 'xlsx_links.json')
LISTA_INFORMES_FPATH = os.path.join(DATA_DIR_ESTRUCTURA_PRECIOS, 'lista_informes.json')
COLS_CIUDADES_FPATH = os.path.join(DATA_DIR_ESTRUCTURA_PRECIOS, 'columnas_ciudades.json')


def ensure_data_estructura_precios():
    status = check_data_status()
    if status == general.SCRATCH:
        scratch_initialization()
    elif status == general.OUTDATED:
        if os.path.exists(DATA_DIR_ESTRUCTURA_PRECIOS):
            os.rmdir(DATA_DIR_ESTRUCTURA_PRECIOS)
        scratch_initialization()
    elif status == general.UPTODATE:
        pass


def check_data_status():
    status = general.SCRATCH
    if os.path.exists(DATA_DIR_ESTRUCTURA_PRECIOS) and os.path.exists(DICT_FILEPATH):
        if it_is_outdated():
            status = general.OUTDATED
        else:
            status = general.UPTODATE
    return status


def scratch_initialization():
    os.makedirs(DATA_DIR_ESTRUCTURA_PRECIOS, exist_ok=True)  # se crea folder en carpeta persistente render.com
    lista_informes_tuple = scrape_url_list()
    lista_informes = [{'label': item[0], 'value': item[0]} for item in lista_informes_tuple]
    save_json(LISTA_INFORMES_FPATH, lista_informes)
    df_dictionary = get_dataframes_dict(lista_informes_tuple)
    with open(DICT_FILEPATH, 'wb') as file:
        pickle.dump(df_dictionary, file)
    columnas_ciudades = df_dictionary[lista_informes[0]['value']][0][0].columns[1:].to_list()
    save_json(COLS_CIUDADES_FPATH, columnas_ciudades)


"""
scrapea la pagina donde se pueden ver los precios de referencia y obtiene una lista de urls de la forma:
[ (texto, link (href)) ]
"""
def scrape_url_list():
    url = "https://www1.upme.gov.co/sipg/Paginas/Estructura-precios-combustibles.aspx"  # URL of the webpage to scrape
    response = requests.get(url)  # Fetch the HTML content of the page
    response.raise_for_status()  # Ensure the request was successful
    soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content using BeautifulSoup
    links = soup.find_all('a', href=True)  # Find all links in the page
    # Extract (text, link) pairs and filter those ending with .xlsx
    xlsx_links = [(link.text.strip(), link['href']) for link in links if link['href'].endswith('.xlsx')]
    save_json(URL_LIST_FPATH, xlsx_links)
    return xlsx_links


def excel_url_to_df(excel_url, folder):
    # URL of the .xlsx file
    # url = xlsx_links[0][1]
    # Fetch the content of the file
    response = requests.get(excel_url)
    response.raise_for_status()  # Ensure the request was successful
    excel_file = 'temp_file.xlsx'
    excel_filepath = os.path.join(folder, excel_file)
    with open(excel_filepath, 'wb') as temp_file:
        temp_file.write(response.content)  # Save the content to a temporary file
    df_precios_corriente = excel_file_precios_to_dframe(excel_filepath, 32, 19, 19)
    df_precios_acpm = excel_file_precios_to_dframe(excel_filepath, 56, 18, 19)
    return df_precios_corriente, df_precios_acpm


def excel_file_precios_to_dframe(excel_file, skip, rows, columns):
    df = pd.read_excel(excel_file, header=None, skiprows=skip)# Read the Excel file into a DataFrame
    column_headers_corriente = df.iloc[0, 0:columns].tolist() # Extract the column headers from the first row of the relevant slice
    # df_corriente = df.iloc[32:51, 0:19].copy()
    df_corriente = df.iloc[1:rows, 0:columns].copy()
    df_corriente.columns = column_headers_corriente
    return df_corriente


def get_dataframes_dict(lista_informes_tuple):
    r = {}
    for name, url in lista_informes_tuple:
        r[name] = [excel_url_to_df(url, DATA_DIR_ESTRUCTURA_PRECIOS)]
    return r


def it_is_outdated():
    pass


def save_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:  # save to a file
        json.dump(data, f, ensure_ascii=False, indent=4)


class EstructuraPreciosLoad:

    def __init__(self):
        ensure_data_estructura_precios()
        self.xlsx_links = self.load_json(URL_LIST_FPATH)
        self.lista_informes = self.load_json(LISTA_INFORMES_FPATH)
        self.columnas_ciudades = self.load_json(COLS_CIUDADES_FPATH)
        with open(DICT_FILEPATH, 'rb') as file:
            self.df_dictionary = pickle.load(file)

    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

