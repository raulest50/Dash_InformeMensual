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

## Funcionamiento De Cada Pagina

### Informe mensual
al iniciar, revisa si vmensual.csv (datos de consumo) existe. si no existe lo crea. si existe revisa si esta 
desactualizado. si esta actualizado lo carga de la carpeta data que contiene los datos persistentes de la app.
si esta desactualizado hace un query al cubo del SICOM para actualizar los datos.

### Estructura De Precios

### Informe En Linea

### Elasticidad de la Demanda
