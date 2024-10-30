
import pickle
import pandas as pd

dc_map = {'BARRANQUILLA':'BARRANQUILLA', 'BOGOTÁ':'BOGOTA, D.C.', 'BUCARAMANGA':'BUCARAMANGA', 'CALI':'CALI', 'CARTAGENA':'CARTAGENA DE INDIAS',
       'MEDELLÍN':'MEDELLIN', 'NEIVA':'NEIVA', 'PEREIRA':'PEREIRA', 'POPAYAN':'POPAYAN', 'SANTA MARTA':'SANTA MARTA', 'TUNJA':'TUNJA',
       'VALLEDUPAR':'VALLEDUPAR', 'VILLAVICENCIO':'VILLAVICENCIO', 'MANIZALES':'MANIZALES', 'ARMENIA':'ARMENIA', 'IBAGUE':'IBAGUE',
       'SINCELEJO':'SINCELEJO'}

def organizar_diccionario(diccionario):
    # Crear una copia de las claves para evitar modificar el diccionario mientras se itera
    keys = list(diccionario.keys())
    for key in keys:
        if ' - Actualización' in key:
            # Obtener el nombre base del mes sin ' - Actualización'
            base_key = key.replace(' - Actualización', '')
            # Reemplazar o agregar el valor en el diccionario con la clave base
            diccionario[base_key] = diccionario[key]
            # Eliminar la clave con ' - Actualización'
            del diccionario[key]
    return diccionario

def convertir_claves_a_fechas(claves_dict):
    import numpy as np  # Asegúrate de importar numpy al inicio de tu script
    meses_es = {
        'Enero': '01',
        'Febrero': '02',
        'Marzo': '03',
        'Abril': '04',
        'Mayo': '05',
        'Junio': '06',
        'Julio': '07',
        'Agosto': '08',
        'Septiembre': '09',
        'Octubre': '10',
        'Noviembre': '11',
        'Diciembre': '12'
    }
    fechas = []
    for clave in claves_dict:
        # Eliminar ' - Actualización' si está presente
        clave = clave.replace(' - Actualización', '')
        partes = clave.strip().split()
        if len(partes) == 2:
            mes_nombre, anio = partes
            mes_numero = meses_es.get(mes_nombre)
            if mes_numero:
                fecha_str = f"{anio}-{mes_numero}-01"
                fecha = pd.to_datetime(fecha_str)
                fechas.append(fecha)
    return fechas

def get_precio_mes_ciudad(fecha, ciudad, dictionary):
    precio_corriente = dictionary[fecha][0][0][ciudad][17]
    precio_diesel = dictionary[fecha][0][1][ciudad][17]
    return precio_corriente, precio_diesel

def get_vol(fecha, municipio, dft):
    vol_corriente = dft[(dft['fecha'] == fecha) & (dft['municipio'] == municipio) & (dft['producto'] == "CORRIENTE")]['volumen_total'].values[0]
    vol_acpm = dft[(dft['fecha'] == fecha) & (dft['municipio'] == municipio) & (dft['producto'] == "DIESEL")]['volumen_total'].values[0]
    return vol_corriente, vol_acpm



def create_demanda_time_series_dtframe(lista_fehas, lista_ciudades, df_vols, dict_precios):
    out_df = pd.DataFrame(columns=['vol_corriente', 'vol_acpm', 'fecha', 'precio_corriente', 'precio_acpm', 'ciudad'])
    for ciudad in lista_ciudades:
        for fecha in lista_fehas:
            vol_corriente, vol_acpm = get_vol(fecha, dc_map[ciudad], df_vols)
            precio_corriente, precio_acpm = get_precio_mes_ciudad(fecha, ciudad, dict_precios)
            out_df.loc[len(out_df)] = {'fecha': fecha, 'vol_corriente': vol_corriente, 'precio_corriente': precio_corriente,
                                         'vol_acpm': vol_acpm, 'precio_acpm': precio_acpm, 'ciudad': ciudad}
    return out_df

def load_dframe_test():
    fname_df_dict = 'df_dictionary.pkl'

    df_dict_filepath = "../data/estructura_precios/df_dictionary.pkl"
    with open(df_dict_filepath, 'rb') as file:
        df_dictionary = organizar_diccionario(pickle.load(file))

    df = pd.read_csv("../data/informe_mensual/vmensual.csv")

    df['anio_despacho'] = df['anio_despacho'].astype(int)
    df['mes_despacho'] = df['mes_despacho'].astype(int)
    df['fecha'] = pd.to_datetime(
        df['anio_despacho'].astype(str) + '-' + df['mes_despacho'].astype(str) + '-01')

    fechas_keys = convertir_claves_a_fechas(df_dictionary.keys())
    dft = df[df['fecha'].isin(fechas_keys)]
    df_new_dict = dict(zip(fechas_keys, df_dictionary.values()))
    lista_ciudades_precios = df_new_dict[fechas_keys[0]][0][0].columns[1:-1]

    demanda_df = create_demanda_time_series_dtframe(fechas_keys, lista_ciudades_precios, dft, df_new_dict)

    print(demanda_df)
    demanda_df.to_csv('demanda_ts.csv', index=False)
    return demanda_df

df = load_dframe_test()
print(df)



