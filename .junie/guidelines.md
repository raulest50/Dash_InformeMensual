#%% md
# Guías de Desarrollo para COMCE Dashboard

## Colores Institucionales
Los siguientes colores institucionales DEBEN ser utilizados en todo el proyecto:
- Verde COMCE: `#41B75C`
- Azul COMCE: `#0D6ABF` 
- Gris COMCE: `#808080`

## Estándares de Diseño

### Cabecera de Páginas
- Cada página debe incluir el logo de COMCE ubicado en la esquina superior derecha
- Ruta del logo: `assets/logoComce.png`
- El logo debe ocupar el 50% del ancho y alto de su contenedor
- El título debe estar alineado al centro y usar la fuente 'Plus Jakarta Sans'

### Estilos de Texto
- Fuente principal: 'Plus Jakarta Sans'
- Texto justificado para párrafos largos
- Tamaño de fuente para párrafos: 20px
- Títulos con borde izquierdo verde institucional (#41B75C)

### Gráficas y Tablas
- Sombras suaves para gráficos: `boxShadow: '0 2px 1px 0 rgba(0, 0, 0, 0.05), 0 3px 5px 0 rgba(0, 0, 0, 0.1)'`
- Tablas con estilo minimalista sin bordes laterales
- Encabezados de tabla en verde institucional

## Estructura del Proyecto
#%%

## Despliegue
- Producción: Despliegue en render.com mediante Docker
- Desarrollo: Ejecución directa de app.py sin Docker

## Stack Tecnológico
- Python 3.12.4  
- Dash Bootstrap Components
- Pandas para manejo de datos
- Plotly Express para visualizaciones

## Estándares de Código
- Indentación: 4 espacios
- Nombres de variables en snake_case
- Comentarios descriptivos en español
- Docstrings para funciones principales

## Convenciones de Datos
- Fechas en formato 'YYYY-MM-DD'
- Valores numéricos como float para volúmenes

## Variables de Estilo Comunes
- Utilizar los estilos definidos en Constants.py
- Mantener consistencia en márgenes y padding
- Usar unidades relativas (em) para espaciado