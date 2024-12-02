import pandas as pd

# Define the data as a list of dictionaries
data = [
    {"anio": 2024, "mes": 10, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_octubre_2024.xlsx"},
    {"anio": 2024, "mes": 9, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_septiembre_2024.xlsx"},
    {"anio": 2024, "mes": 8, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_agosto_2024.xlsx"},
    {"anio": 2024, "mes": 7, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_julio_2024.xlsx"},
    {"anio": 2024, "mes": 6, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_junio_2024_actualizacion.xlsx"},
    {"anio": 2024, "mes": 5, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_Mayo_2024.xlsx"},
    {"anio": 2024, "mes": 4, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_Abril_2024.xlsx"},
    {"anio": 2024, "mes": 3, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_Marzo_2024.xlsx"},
    {"anio": 2024, "mes": 2, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_Febrero_2024.xlsx"},
    {"anio": 2024, "mes": 1, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_Enero_2024.xlsx"},
    {"anio": 2023, "mes": 12, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Diciembre_2023.xlsx"},
    {"anio": 2023, "mes": 11, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Noviembre_2023.xlsx"},
    {"anio": 2023, "mes": 10, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Octubre_2023.xlsx"},
    {"anio": 2023, "mes": 9, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Septiembre_2023.xlsx"},
    {"anio": 2023, "mes": 8, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Agosto_2023.xlsx"},
    {"anio": 2023, "mes": 7, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Julio_2023.xlsx"},
    {"anio": 2023, "mes": 6, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Junio_2023.xlsx"},
    {"anio": 2023, "mes": 5, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Mayo_2023.xlsx"},
    {"anio": 2023, "mes": 4, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Abril_2023.xlsx"},
    {"anio": 2023, "mes": 3, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Marzo_2023.xlsx"},
    {"anio": 2023, "mes": 2, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Febrero_2023.xlsx"},
    {"anio": 2023, "mes": 1, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_Enero_2023.xlsx"},
    {"anio": 2022, "mes": 12, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_diciembre_2022.xlsx"},
    {"anio": 2022, "mes": 11, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_noviembre_2022.xlsx"},
    {"anio": 2022, "mes": 10, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_octubre_2022.xlsx"},
    {"anio": 2022, "mes": 9, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_septiembre_2022.xlsx"},
    {"anio": 2022, "mes": 8, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_agosto_2022.xlsx"},
    {"anio": 2022, "mes": 7, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_julio_2022.xlsx"},
    {"anio": 2022, "mes": 6, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_junio_2022.xlsx"},
    {"anio": 2022, "mes": 5, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_mayo_2022.xlsx"},
    {"anio": 2022, "mes": 4, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_abril_2022.xlsx"},
    {"anio": 2022, "mes": 3, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_marzo_2022.xlsx"},
    {"anio": 2022, "mes": 2, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_febrero_2022.xlsx"},
    {"anio": 2022, "mes": 1, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_enero_2022.xlsx"},
    {"anio": 2021, "mes": 12, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_diciembre_2021.xlsx"},
    {"anio": 2021, "mes": 11, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_noviembre_2021.xlsx"},
    {"anio": 2021, "mes": 10, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_octubre_2021.xlsx"},
    {"anio": 2021, "mes": 9, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_septiembre_2021.xlsx"},
    {"anio": 2021, "mes": 8, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_agosto_2021.xlsx"},
    {"anio": 2021, "mes": 7, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_julio_2021.xlsx"},
    {"anio": 2021, "mes": 6, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_junio_2021.xlsx"},
    {"anio": 2021, "mes": 5, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_mayo_2021.xlsx"},
    {"anio": 2021, "mes": 4, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_abril_2021.xlsx"},
    {"anio": 2021, "mes": 3, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_marzo_2021.xlsx"},
    {"anio": 2021, "mes": 2, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_febrero_2021.xlsx"},
    {"anio": 2021, "mes": 1, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_enero_2021.xlsx"},
    {"anio": 2020, "mes": 12, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Dic_2020.xlsx"},
    {"anio": 2020, "mes": 11, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Nov_2020.xlsx"},
    {"anio": 2020, "mes": 10, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Octubre_2020.xlsx"},
    {"anio": 2020, "mes": 9, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Septiembre_2020.xlsx"},
    {"anio": 2020, "mes": 8, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Agosto_2020.xlsx"},
    {"anio": 2020, "mes": 7, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Julio_2020.xlsx"},
    {"anio": 2020, "mes": 6, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Junio_2020.xlsx"},
    {"anio": 2020, "mes": 5, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Mayo_2020.xlsx"},
    {"anio": 2020, "mes": 4, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Abril_2020.xlsx"},
    {"anio": 2020, "mes": 3, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Marzo_2020.xlsx"},
    {"anio": 2020, "mes": 2, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_precios_febrero_2020.xlsx"},
    {"anio": 2020, "mes": 1, "url": "https://www1.upme.gov.co/sipg/Precios%20combustibles%20principales%20ciudades/Estructura_Precios_Enero_2020.xlsx"},
]

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Specify the CSV file name
output_file = 'urls_upme.csv'

# Export the DataFrame to a CSV file with comma as the separator
df.to_csv(output_file, index=False, sep=',')

