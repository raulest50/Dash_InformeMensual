
"""
script para prototipar el scrapeo de datos de precios de referencia para la gasolina
"""

# C:\Users\raule\AppData\local\Programs\Python\Python39\.\Scripts\pip.exe freeze
# https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_junio_2024_actualizacion.xlsx

import pandas as pd
import requests
from bs4 import BeautifulSoup

from methods import scrape_url_list, get_data_frames_from_excel_url

xlsx_links = scrape_url_list()

for x in xlsx_links:
    print(x)

# URL of the .xlsx file
url = xlsx_links[0][1]

df_corriente, df_acpm = get_data_frames_from_excel_url(url)

# Display the DataFrame
print(df_corriente)
df_corriente.to_csv("corriente_precios.csv", index=False)

print(df_corriente)
df_corriente.to_csv("acpm_precios.csv", index=False)

