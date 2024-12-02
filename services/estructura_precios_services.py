
import os

import requests
from bs4 import BeautifulSoup

from init_service import InitService


class EstructuraPreciosService(InitService):

    DATA_DIR_ESTRUCTURA_PRECIOS = 'data/estructura_precios'

    def __init__(self):
        pass

    def check_data_status(self):
        status = self.SCRATCH
        if os.path.exists(self.DATA_DIR_INF_MENSUAL) & os.path.exists(self.VMENSUAL_FILEPATH):
            if self.it_is_outdated():
                status = self.OUTDATED
            else:
                status = self.UPTODATE
        return status

    def scratch_initialization(self):
        df = self.fetch_socrata_datosgov(self, query=self.build_query(), db_alias=self.DB_ALIAS_VOL_MAYOTISTAS, t_out=20)
        df.to_csv(self.VMENSUAL_FILEPATH, index=False)
        return df

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

        df_precios_corriente = excel_file_precios_to_dframe(excel_filepath, 32, 19, 19)
        df_precios_acpm = excel_file_precios_to_dframe(excel_filepath, 56, 18, 19)

        return df_precios_corriente, df_precios_acpm


    