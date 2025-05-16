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

## Medicion Consumo de RAM de la Aplicacion

para estimar el consumo de ram se usa psutil pero este solo esta disponible
como un module en dev mode. corriendolo con la app run configuration no 
encontraba el modulo. Pero ejecutando:
```
poetry run python app.py
```
si me funcionaba con psutil y muestra un burbuja en la esquina inferior 
izquierda con la estimacion del consumo de RAM