
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

# seleccionar el mes actual para t'odo el texto de conclusion al final del dashboard
current_mes = 'junio'

def Gen_parrafoBottom():

    #mes_str = get_mes_name(mes)

    return f"""
        Reporte mensual de la variación de ventas {current_mes} 2024 (conclusión generada el 02 de {current_mes}): 
        El informe mensual refleja que la variación relativa para gasolina corriente sigue cayendo, esta vez con una 
        caída del 9,54% respecto al mes de {current_mes} en 2023. Igual sucede con la variación de ACPM, la cual reporta 
        una diferencia negativa el -2,57%. Llama la atención que en los 06 primeros meses del año 2024, 
        la variación en ventas en gasolina corriente, a nivel agregado, ha sido negativa en todos los meses de 2024. 
        Las ventas de gasolina extra reportan un repunte positivo del 14,73% para el mes de {current_mes}.
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

zdf_options = ['Incluir Zonas De Frontera', 'Sin Zonas De Frontera', 'Solo Zonas De Frontera']



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


# lista de 158 municipios que son zona de frontera.
# en total son 171 de acuerdo a
# https://www.datos.gov.co/Minas-y-Energ-a/Beneficio-de-estaciones-de-servicio-en-zona-de-fro/shbt-hqy9/about_data
# .
zdf_list = ['ABREGO', 'ACANDI', 'AGUACHICA', 'AGUSTIN CODAZZI', 'ALBAN', 'ALBANIA', 'ALDANA', 'ANCUYA', 'ARAUCA',
            'ARAUQUITA', 'ARBOLEDA', 'BARBACOAS', 'BARRANCAS', 'BECERRIL', 'BELEN', 'BOCHALEMA', 'BOSCONIA',
            'BUCARASICA', 'BUESACO', 'CACHIRA', 'CHACHAGUI', 'CHINACOTA', 'CHIRIGUANA', 'COLON', 'COLON', 'CONSACA',
            'CONTADERO', 'CONVENCION', 'CORDOBA', 'CRAVO NORTE', 'CUASPUD', 'CUBARA', 'CUMARIBO', 'CUMBAL',
            'CUMBITARA', 'CURUMANI', 'DIBULLA', 'DISTRACCION', 'DURANIA', 'EL CARMEN', 'EL CHARCO', 'EL COPEY',
            'EL MOLINO', 'EL PASO', 'EL PEÑOL', 'EL ROSARIO', 'EL TABLON DE GOMEZ', 'EL TAMBO', 'EL TARRA', 'EL ZULIA',
            'FONSECA', 'FORTUL', 'FRANCISCO PIZARRO', 'FUNES', 'GAMARRA', 'GUACHUCAL', 'GUAITARILLA', 'GUALMATAN',
            'HACARI', 'HATONUEVO', 'ILES', 'IMUES', 'IPIALES', 'JURADO', 'LA CRUZ', 'LA ESPERANZA', 'LA FLORIDA',
            'LA GLORIA', 'LA JAGUA DE IBIRICO', 'LA JAGUA DEL PILAR', 'LA LLANADA', 'LA PAZ', 'LA PEDRERA', 'LA PLAYA',
            'LA PRIMAVERA', 'LA TOLA', 'LA UNION', 'LEIVA', 'LETICIA', 'LINARES', 'LOS ANDES', 'LOS PATIOS', 'MAGUI',
            'MAICAO', 'MALLAMA', 'MANAURE', 'MANAURE BALCON DEL CESAR', 'MITU', 'MOCOA', 'MOSQUERA', 'NARIÑO', 'OCAÑA',
            'OLAYA HERRERA', 'ORITO', 'OSPINA', 'PAILITAS', 'PAMPLONA', 'PASTO', 'PELAYA', 'POLICARPA', 'POTOSI',
            'PROVIDENCIA', 'PUERRES', 'PUERTO ASIS', 'PUERTO CAICEDO', 'PUERTO CARREÑO', 'PUERTO GUZMAN',
            'PUERTO LEGUIZAMO', 'PUERTO RONDON', 'PUPIALES', 'RAGONVALIA', 'RICAURTE', 'RIO DE ORO', 'RIOHACHA',
            'RIOSUCIO', 'ROBERTO PAYAN', 'SAMANIEGO', 'SAN ALBERTO', 'SAN ANDRES', 'SAN ANDRES DE TUMACO',
            'SAN BERNARDO', 'SAN CALIXTO', 'SAN CAYETANO', 'SAN DIEGO', 'SANDONA', 'SAN FRANCISCO',
            'SAN JOSE DE CUCUTA', 'SAN JUAN DEL CESAR', 'SAN LORENZO', 'SAN MARTIN', 'SAN MIGUEL', 'SAN PABLO',
            'SAN PEDRO DE CARTAGO', 'SANTA BARBARA', 'SANTACRUZ', 'SANTIAGO', 'SAPUYES', 'SARAVENA', 'SARDINATA',
            'SIBUNDOY', 'TAME', 'TAMINANGO', 'TANGUA', 'TARAIRA', 'TEORAMA', 'TIBU', 'TOLEDO', 'TUQUERRES', 'UNGUIA',
            'URIBIA', 'URUMITA', 'VALLE DEL GUAMUEZ', 'VALLEDUPAR', 'VILLA DEL ROSARIO', 'VILLAGARZON', 'VILLANUEVA',
            'YACUANQUER', 'INIRIDA']


