

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL to scrape
url = "https://creg.gov.co/publicaciones/15565/precios-de-combustibles-liquidos/"

# Send a GET request to the URL
response = requests.get(url)
html_content = response.content

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Mapping of Spanish month names to their numerical representation
months = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

# Find all tables in the page
tables = soup.find_all('table')

# List to hold all the data
data_list = []

# Iterate over each table
for table in tables:
    # Extract the date from the caption within the table
    caption = table.find('caption')
    if caption:
        h3 = caption.find('h3')
        if h3:
            date_text = h3.get_text(strip=True)
            # Use regex to extract day, month, and year
            match = re.search(r'(\d{1,2}) de (\w+) del (\d{4})', date_text)
            if match:
                day = int(match.group(1))
                month_text = match.group(2).lower()
                year = int(match.group(3))
                # Convert month name to number
                month = months.get(month_text)
                if not month:
                    print(f"Could not parse month: {month_text}")
                    continue
            else:
                print(f"Could not parse date from text: {date_text}")
                continue
        else:
            print("No h3 tag in caption")
            continue
    else:
        print("No caption in table")
        continue

    # Find all rows in the table body
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cells = row.find_all(['td', 'th'])
        # Skip rows that are "Promedio PVP"
        if len(cells) >= 2:
            first_cell_text = cells[1].get_text(strip=True)
            if 'Promedio PVP' in first_cell_text:
                continue  # Skip the "Promedio PVP" row
            elif len(cells) >= 4:
                # Extract data from the cells
                num = cells[0].get_text(strip=True)
                ciudad = cells[1].get_text(strip=True)
                precio_gasolina = cells[2].get_text(strip=True).replace('.', '').replace(',', '.')
                precio_acpm = cells[3].get_text(strip=True).replace('.', '').replace(',', '.')
                # Convert prices to float
                try:
                    precio_gasolina = float(precio_gasolina)
                    precio_acpm = float(precio_acpm)
                except ValueError:
                    precio_gasolina = None
                    precio_acpm = None
                # Append the data to the list
                data_list.append({
                    'anio': year,
                    'mes': month,
                    'ciudad': ciudad,
                    'precio_gasolina': precio_gasolina,
                    'precio_acpm': precio_acpm
                })

# Create a DataFrame from the list of data
df = pd.DataFrame(data_list)

# Display the DataFrame
print(df)

df.to_csv("creg.csv", index=False)

print(df['ciudad'])