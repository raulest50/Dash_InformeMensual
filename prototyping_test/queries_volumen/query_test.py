import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None, timeout=30)

p1 = "CORRIENTE"
p2 = "DIESEL"
p3 = "EXTRA"

c1 = "COMERCIALIZADOR INDUSTRIAL"
c2 = "ESTACION DE SERVICIO AUTOMOTRIZ"
c3 = "ESTACION DE SERVICIO FLUVIAL"

query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio "
        f"WHERE subtipo_comprador IN ('{c1}', '{c2}', '{c3}') "
        f"AND producto IN ('{p1}', '{p2}', '{p3}') "
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 250000 "
        )

results = client.get("339g-zjac", query=query)
df = pd.DataFrame.from_records(results)
df.to_csv("qtest.csv", index=False)

print(len(df['municipio'].unique()))
print(len(df))

# Group by municipio and count the unique product types
product_counts = df.groupby('municipio')['producto'].nunique()

# Classify municipios based on the number of unique products
one_type = product_counts[product_counts == 1].count()
two_types = product_counts[product_counts == 2].count()
three_types = product_counts[product_counts == 3].count()

# Print the results
print(f'Municipios buying 1 type of fuel: {one_type}')
print(f'Municipios buying 2 types of fuel: {two_types}')
print(f'Municipios buying 3 types of fuel: {three_types}')

year = '2021'

df_year = df[df['anio_despacho'] == year]
month_bought_counts_23 = df_year.groupby('municipio')['mes_despacho'].nunique()

for n in range(1, 13):
        print(f"n month:{n}  count:{month_bought_counts_23[month_bought_counts_23 == n ].count()}")



print("********")


# Define the possible combinations
combinations = [
    ('CORRIENTE',),
    ('DIESEL',),
    ('EXTRA',),
    ('CORRIENTE', 'DIESEL'),
    ('CORRIENTE', 'EXTRA'),
    ('DIESEL', 'EXTRA'),
    ('CORRIENTE', 'DIESEL', 'EXTRA')
]

# Create a dictionary to store the count for each category
category_counts = {comb: 0 for comb in combinations}

# Helper function to convert sets to sorted tuples
def set_to_sorted_tuple(s):
    return tuple(sorted(s))

# Create a dictionary to store the unique products for each municipio
unique_products = {}

# Populate the dictionary with the set of products for each municipio
for index, row in df.iterrows():
    municipio = row['municipio']
    producto = row['producto']
    if municipio not in unique_products:
        unique_products[municipio] = set()
    unique_products[municipio].add(producto)

# Count the number of municipios falling into each category
for products in unique_products.values():
    category = set_to_sorted_tuple(products)
    if category in category_counts:
        category_counts[category] += 1

# Print the results
for category, count in category_counts.items():
    print(f'Municipios buying {", ".join(category)}: {count}')


