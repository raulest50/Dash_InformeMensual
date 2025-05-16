# Conversión de CSV a Parquet

Este directorio contiene scripts para convertir archivos CSV a formato Parquet, lo que permite reducir el consumo de memoria RAM y mejorar el rendimiento de la aplicación.

## Archivos Convertidos

Los siguientes archivos CSV se convierten a formato Parquet:

1. `data/informe_mensual/vmensual.csv` → `data/informe_mensual/vmensual.parquet`
2. `data/mercado_eds/info_mercado.csv` → `data/mercado_eds/info_mercado.parquet`

## Scripts Disponibles

- `csv_to_parquet_vmensual.py`: Convierte vmensual.csv a formato Parquet
- `csv_to_parquet_info_mercado.py`: Convierte info_mercado.csv a formato Parquet
- `convert_all_to_parquet.py`: Script principal que ejecuta ambas conversiones

## Cómo Usar

Para convertir todos los archivos CSV a formato Parquet, ejecute:

```bash
python data_conversion/convert_all_to_parquet.py
```

Para convertir archivos individuales:

```bash
python data_conversion/csv_to_parquet_vmensual.py
python data_conversion/csv_to_parquet_info_mercado.py
```

## Ventajas de Parquet

- **Formato columnar**: Permite cargar solo las columnas necesarias
- **Compresión eficiente**: Reduce el tamaño de los archivos
- **Tipos de datos optimizados**: Mejora el rendimiento y reduce el consumo de memoria
- **Carga parcial de datos**: Posibilidad de cargar solo las columnas requeridas

## Modificaciones en el Código

Los siguientes archivos han sido modificados para usar Parquet en lugar de CSV:

1. `services/informe_mensual_data.py`: Ahora usa `pd.read_parquet()` en lugar de `pd.read_csv()`
2. `services/mercado_eds_data.py`: Ahora usa `pd.read_parquet()` en lugar de `pd.read_csv()`

## Requisitos

- PyArrow: `pip install pyarrow` o ya incluido en el entorno Poetry