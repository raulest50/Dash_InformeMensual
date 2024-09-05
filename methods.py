
import requests
from sodapy import Socrata
import pandas as pd
from bs4 import BeautifulSoup

from datetime import datetime, timedelta

p1 = "CORRIENTE"
p2 = "DIESEL"
p3 = "EXTRA"

c1 = "COMERCIALIZADOR INDUSTRIAL"
c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
c3 = "ESTACION DE SERVICIO FLUVIAL"

# colores Institucionales
verde = "#41B75C"
azul = "#0D6ABF"
gris = "#808080"



def getDataFrame():
    cliente = Socrata("www.datos.gov.co", None, timeout=10)

    not_success = True

    while not_success:
        try:
            query = (
                f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto "
                f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
                f"AND producto IN ('{p1}', '{p2}', '{p3}') "
                f"GROUP BY anio_despacho, mes_despacho, producto "
                f"ORDER BY anio_despacho ASC "
                f"LIMIT 5000 "
            )

            results = cliente.get("339g-zjac", query=query)
            df = pd.DataFrame.from_records(results)
            return df
        except requests.exceptions.Timeout:
            print("time out exception")
            not_success = True



"""dataframe superset"""
def getDataFrame_suset():
    cliente = Socrata("www.datos.gov.co", None, timeout=10)

    not_success = True

    while not_success:
        try:
            query = (
                f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
                f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
                f"AND producto IN ('{p1}', '{p2}', '{p3}') "
                f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
                f"ORDER BY anio_despacho ASC "
                f"LIMIT 250000 "
            )

            results = cliente.get("339g-zjac", query=query)
            df = pd.DataFrame.from_records(results)
            return df
        except requests.exceptions.Timeout:
            print("time out exception")
            not_success = True



def format_zdf_list(zdf_list, n=10):
    return '\n'.join(', '.join(zdf_list[i:i + n]) for i in range(0, len(zdf_list), n))


"""
scrapea la pagina donde se pueden ver los precios de referencia y obtiene una lista con la estructura:
[ (texto, link (href)) ]
"""
def scrape_url_list():
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



def get_data_frames_from_excel_url(excel_url):
    # URL of the .xlsx file
    #url = xlsx_links[0][1]
    # Fetch the content of the file
    response = requests.get(excel_url)
    response.raise_for_status()  # Ensure the request was successful

    excel_file = 'temp_file.xlsx'
    # Save the content to a temporary file
    with open(excel_file, 'wb') as temp_file:
        temp_file.write(response.content)

    df_precios_corriente = excel_file_precios_to_dframe(excel_file, 32, 19, 19)
    df_precios_acpm = excel_file_precios_to_dframe(excel_file, 56, 18, 19)

    return df_precios_corriente, df_precios_acpm


def excel_file_precios_to_dframe(excel_file, skip, rows, columns):

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file, header=None, skiprows=skip)

    # Extract the column headers from the first row of the relevant slice
    column_headers_corriente = df.iloc[0, 0:columns].tolist()

    # df_corriente = df.iloc[32:51, 0:19].copy()
    df_corriente = df.iloc[1:rows, 0:columns].copy()

    df_corriente.columns = column_headers_corriente
    return df_corriente


def getDataFrame_OnlineReport():

    # Get today's date and 60 days before
    today = datetime.today().strftime('%Y-%m-%d')
    sixty_days_ago = (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')

    cliente = Socrata("www.datos.gov.co", None, timeout=10)

    not_success = True
    while not_success:
        try:
            query = (
                f"SELECT SUM(volumen_despachado) as volumen_total, producto, fecha_despacho "
                f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
                f"AND producto IN ('{p1}', '{p2}', '{p3}') "
                f"AND fecha_despacho BETWEEN '{sixty_days_ago}' AND '{today}' "
                f"GROUP BY producto, fecha_despacho "
                f"ORDER BY fecha_despacho ASC "
                f"LIMIT 20000 "
            )

            results = cliente.get("339g-zjac", query=query)
            df = pd.DataFrame.from_records(results)
            return df
        except requests.exceptions.Timeout:
            print("time out exception - get dtframe online report")
            not_success = True
