
# colores Institucionales
verde = "#41B75C"
azul = "#0D6ABF"
gris = "#808080"

correo_esteban = "ralzate@comce-soldicom.com"
cel_esteban = "+57 313 515 86 11"
correo_juan = "jbonilla@comce-soldicom.com"
cel_juan = "+57 315 560 43 22"


contacto1 = f"""
            Raúl Esteban Alzate \n
            {correo_esteban} \n
            TEL {cel_esteban}"""

contacto2 = f"""
            Juan David Bonilla \n
            {correo_juan} \n
            TEL {cel_juan}"""

# otros colores
dc_bbcolor = '#92CEC2'

parrafoTop = """
    A continuación, se exponen las gráficas y tablas que muestran el comportamiento en volumen de ventas 
    de combustibles líquidos a través de Estaciones de servicio a nivel nacional (acpm, corriente y extra), 
    de manera comparativa, para cada mes del año (2020-2024). 
    El mes se puede seleccionar mediante el DropDown menú.
"""

parrafo_dt_source = """
        Este informe es presentado por la Coordinación de Regulación y 
        Análisis de datos de COMCE, en la administración de los recursos parafiscales de SOLDICOM. 
        La fuente de los datos es el acceso remoto a Cubo Sicom otorgado por el Ministerio de Minas y Energía para COMCE-SOLDICOM. 
        Los datos reportan el volumen agregado del sector, a nivel país, reporte de ventas de combustibles líquidos a 
        través de los agentes compradores COMERCIALIZADOR INDUSTRIAL, ESTACION DE SERVICIO AUTOMOTRIZ y ESTACION DE SERVICIO FLUVIAL.
        Se incluyeron Zonas de frontera. *Si se requieren datos de un departamento, municipio o
        ciudad en específico favor contactarse con la Coordinación.
"""

def Gen_parrafoBottom():

    #mes_str = get_mes_name(mes)

    return f"""
        Reporte de la variación mensual de ventas mayo 2024: 
        El informe mensual refleja que la variación relativa para gasolina corriente sigue cayendo, esta vez con una 
        caída del 9,99% respecto al mes de mayo en 2023. Igual sucede con la variación de ACPM, la cual reporta una 
        diferencia negativa el -1,87%. Llama la atención que en los 05 primeros meses del año 2024, 
        la variación en ventas en gasolina corriente, a nivel agregado, ha sido negativa en todos los meses de 2024. 
        Las ventas de gasolina extra reportan un repunte positivo del 19,64% para el mes de mayo.
        Más información contactarse a los siguientes canales: 
        """

style_cell = {
    'textAlign': 'center',
    'padding': '5px',
    'fontFamily': "'Plus Jakarta Sans', sans-serif",
    'borderLeft': '0px',
    'borderRight': '0px',
    'borderTop': '0px',
    }

style_header = {
    'backgroundColor': '#19B698',
    'fontWeight': 'bold',
    'textAlign': 'center',
    'fontSize': '18px'
    }

style_data = {
    'backgroundColor': 'rgb(248, 248, 248)',
    'borderBottom': f'1px solid {dc_bbcolor}'
    }

style_table = {
    'border': None,
}


style_graph = {
    'boxShadow': '0 2px 1px 0 rgba(0, 0, 0, 0.05), 0 3px 5px 0 rgba(0, 0, 0, 0.1)'
}

style_graph2 = {
    'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'
}


style_header1 = {
    'fontFamily': "'Plus Jakarta Sans', sans-serif",
    'textAlign': 'left',
    'borderLeft': f'20px solid {verde}',
    'padding': '0.2em',
}

style_header4 = {
    'fontFamily': "'Plus Jakarta Sans', sans-serif",
    'textAlign': 'center',
}


style_H2 = {
    'fontFamily': "'Plus Jakarta Sans', sans-serif",
}

style_H3 = {
    'fontFamily': "'Plus Jakarta Sans', sans-serif",
}

style_text_bottom = {
    'fontFamily': "'Plus Jakarta Sans', sans-serif",
    'textAlign': 'justify',
    'fontSize': '20px'
}

style_drop_label = {
    'fontFamily': "'Plus Jakarta Sans', sans-serif",
    'fontSize': '18px',
    'padding': '0.2em'
}



geo = [
    "Todo el Pais",
    "Bogotá, D.C.",
    "Santiago de Cali, Valle del Cauca",
    "Barranquilla, Atlántico",
    "Medellín, Antioquia",
    "Montería, Córdoba",
    "Cartagena de Indias, Bolívar",
    "Pereira, Risaralda",
    "Ibagué, Tolima",
    "Bucaramanga, Santander",
    "Sincelejo, Sucre",
    "Manizales, Caldas",
    "Villavicencio, Meta",
    "Popayán, Cauca",
    "Santiago de Tunja, Boyacá",
    "Barrancabermeja, Santander",
    "Chía, Cundinamarca",
    "Palmira, Valle del Cauca",
    "Soacha, Cundinamarca",
    "Tuluá, Valle del Cauca",
    "Cartago, Valle del Cauca",
    "Armenia, Quindío",
    "Rionegro, Antioquia",
    "Neiva, Huila",
    "Santa Marta, Magdalena",
    "Sogamoso, Boyacá"
]




geo_translate = [
    "Todo el Pais",
    "BOGOTA, D.C.",
    "CALI",
    "BARRANQUILLA",
    "MEDELLIN",
    "MONTERIA",
    "CARTAGENA DE INDIAS",
    "PEREIRA",
    "IBAGUE",
    "BUCARAMANGA",
    "SINCELEJO",
    "MANIZALES",
    "VILLAVICENCIO",
    "POPAYAN",
    "TUNJA",
    "BARRANCABERMEJA",
    "CHIA",
    "PALMIRA",
    "SOACHA",
    "TULUA",
    "CARTAGO",
    "ARMENIA",
    "RIONEGRO",
    "NEIVA",
    "SANTA MARTA",
    "SOGAMOSO"
]


"""
hay ciudades de colobia que el nombre puede ser confuso, por ejemplo santiago de tunja es tunja y cartagena de indias
es diferente de cartagena (hay 2 cartagenas). por eso es util colocar el nombre del municipio como en el array geo.
pero en la base de datos abierta de mayoriastas el string es diferente. por ejemplo en la bd es CALI en lugar de 
santiago de cali. entonces por eso se hace este diccionario para poder traducir entre el string que se muestra
en la uui con el string que se requiere para filtrar en la bd y el dataframe. 
"""
geo_dict = dict(zip(geo, geo_translate))

def get_mes_name(month_number):
    """Returns the Spanish name of the month given the month number (1-12)."""

    month_names = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    return month_names.get(month_number)

