# Actualización de vmensual.parquet

Este documento describe cómo actualizar el archivo `vmensual.parquet` con datos frescos de la API de Socrata.

## Contexto

El servicio de Socrata tiene una ventana de 5 años sobre los datos, lo que significa que datos anteriores (por ejemplo, de 2019 y 2020) ya no están disponibles. Este documento describe dos soluciones para actualizar el archivo `vmensual.parquet` con los datos más recientes disponibles en Socrata.

## Solución 1: Usar vmensual_fresh.py con --force-update

El script `vmensual_fresh.py` ha sido modificado para aceptar un parámetro `--force-update` que fuerza la actualización del archivo `vmensual.parquet` con datos frescos de Socrata, incluso si el archivo ya existe.

### Uso

```bash
python prototyping_test\vmensual_fresh.py --force-update
```

Este comando:
1. Crea una copia de seguridad del archivo `vmensual.parquet` existente en el directorio `data\informe_mensual\old` con un timestamp en el nombre del archivo
2. Descarga datos frescos de Socrata
3. Guarda los datos frescos en `data\informe_mensual\vmensual.parquet`

## Solución 2: Usar update_vmensual.py

Se ha creado un nuevo script `update_vmensual.py` que está diseñado específicamente para actualizar el archivo `vmensual.parquet` con datos frescos de Socrata.

### Uso

```bash
python prototyping_test\update_vmensual.py
```

Este comando:
1. Crea una copia de seguridad del archivo `vmensual.parquet` existente en el directorio `data\informe_mensual\old` con un timestamp en el nombre del archivo
2. Descarga datos frescos de Socrata
3. Guarda los datos frescos en `data\informe_mensual\vmensual.parquet`

## Diferencias entre las soluciones

Ambas soluciones hacen lo mismo: actualizar el archivo `vmensual.parquet` con datos frescos de Socrata. La diferencia principal es que `vmensual_fresh.py` está diseñado para ser utilizado tanto para cargar datos existentes como para actualizar datos, mientras que `update_vmensual.py` está diseñado específicamente para actualizar datos.

## Notas importantes

- Ambas soluciones crean una copia de seguridad del archivo `vmensual.parquet` existente antes de reemplazarlo con datos frescos
- Ambas soluciones reemplazan completamente los datos existentes con datos frescos de Socrata
- El tiempo de ejecución depende del tamaño de los datos y de la velocidad de la conexión a Internet
- Se recomienda ejecutar estos scripts durante horas de baja carga para minimizar el impacto en el rendimiento del sistema