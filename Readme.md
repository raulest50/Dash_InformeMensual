# Automatizacion de Procesos COMCE-SOLDICOM


## setup starting from zero - poetry setup

se agrega python 3.12 a variables de entorno
comandos tomados de: "https://www.linkedin.com/pulse/poetry-installation-understanding-pip-vs-pipx-approach-shoukat-jybkf/"
```
python -m ensurepip --upgrade
python -m pip install setuptools
python -m pip install pipreqs

python -m pip install pipx 
python -m pipx ensurepath # Add pipx to PATH
pipx install poetry
```

## Funcionamiento De Cada Pagina de la Dash App

### Informe mensual
al iniciar, revisa si vmensual.csv (datos de consumo) existe. si no existe lo crea. si existe revisa si esta 
desactualizado. si esta actualizado lo carga de la carpeta data que contiene los datos persistentes de la app.
si esta desactualizado hace un query al cubo del SICOM para actualizar los datos.

### Estructura De Precios
1. si la carpeta data/estructura_precios no existe la crea
2. se hace un scraping de las listas de precios en la pagina de la upme
3. se crea una lista de diccionarios con keys label, value para uno de los dropdowns de la pagina
4. si ya existe un pkl file con los datos de precios se carga, de lo contrario, se usa la lista scrapeada en 1. para hacer fetch de data y construir un pkl
5. se crea la lista de opciones para el dropdown de ciudades

### Informe En Linea
Hace un fetch al cubo del SICOM cada N minutos y grafica las correspondientes series de tiempo

### Elasticidad de la Demanda
