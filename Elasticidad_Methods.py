
import pickle
import pandas as pd
import os
from Constants import DATA_DIR_ELASTICIDAD, DATA_DIR_ESTRUCTURA_PRECIOS




dc_map = {'BARRANQUILLA': 'BARRANQUILLA', 'BOGOTÁ': 'BOGOTA, D.C.', 'BUCARAMANGA': 'BUCARAMANGA', 'CALI': 'CALI',
          'CARTAGENA': 'CARTAGENA DE INDIAS', 'MEDELLÍN': 'MEDELLIN', 'NEIVA': 'NEIVA', 'PEREIRA': 'PEREIRA',
          'POPAYAN': 'POPAYAN', 'SANTA MARTA': 'SANTA MARTA', 'TUNJA': 'TUNJA', 'VALLEDUPAR': 'VALLEDUPAR',
          'VILLAVICENCIO': 'VILLAVICENCIO', 'MANIZALES': 'MANIZALES', 'ARMENIA': 'ARMENIA', 'IBAGUE': 'IBAGUE',
          'SINCELEJO': 'SINCELEJO'}

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
    precio_corriente = dictionary[fecha][0][0][ciudad][18]
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


def add_demanda_nacional(df_demanda, df_vmensual):
    df_vmensual = df_vmensual.groupby(['producto', 'fecha'])['volumen_total'].sum().reset_index()
    meses = df_demanda['fecha'].unique().tolist()

    df_vmensual = df_vmensual[df_vmensual['producto'] != 'EXTRA'].copy()
    product_mapping = {'CORRIENTE': 'vol_corriente', 'DIESEL': 'vol_acpm'}
    df_vmensual['producto'] = df_vmensual['producto'].map(product_mapping)
    df_vmensual = df_vmensual.pivot_table(
        index='fecha',
        columns='producto',
        values='volumen_total',
        aggfunc='sum'
    ).copy()
    df_vmensual = df_vmensual.reset_index()
    df_vmensual.columns.name = None
    df_vmensual = df_vmensual[['fecha', 'vol_corriente', 'vol_acpm']].copy()

    df_vmensual['fecha'] = pd.to_datetime(df_vmensual['fecha'])
    meses = pd.to_datetime(meses)
    df_vmensual = df_vmensual[df_vmensual['fecha'].isin(meses)].reset_index()

    df_demanda_avg = df_demanda[['fecha', 'precio_corriente', 'precio_acpm']].copy()
    df_demanda_avg = df_demanda_avg.groupby('fecha', as_index=False).mean().copy()
    df_demanda_avg['fecha'] = pd.to_datetime(df_demanda_avg['fecha'])

    df_demanda_avg = pd.merge(df_demanda_avg, df_vmensual, on='fecha')
    df_demanda_avg['ciudad'] = 'NACIONAL'

    columns_order = df_demanda.columns.tolist()
    df_demanda_avg = df_demanda_avg[columns_order]  #reorder columns to match df_demanda

    df_demanda = pd.concat([df_demanda, df_demanda_avg], ignore_index=True)

    return df_demanda


def load_demanda_df_time_series():
    file_name = 'demanda_df.csv'
    demanda_df_file_path = os.path.join(DATA_DIR_ELASTICIDAD, file_name)

    #demanda_df = pd.DataFrame()

    if os.path.exists(demanda_df_file_path): #  si el archivo existe se carga y se retorna
        with open(demanda_df_file_path, 'rb') as archivo:
            demanda_df = pd.read_csv(demanda_df_file_path)

    else:  # si no existe se crea desde cero
        fname_precios_dict = 'df_dictionary.pkl'
        dict_dfs_precios_filepath = os.path.join(DATA_DIR_ESTRUCTURA_PRECIOS, fname_precios_dict)

        with open(dict_dfs_precios_filepath, 'rb') as file:
            df_dictionary = organizar_diccionario(pickle.load(file))

        df_vmensual = pd.read_csv("./data/informe_mensual/vmensual.csv")

        df_vmensual['anio_despacho'] = df_vmensual['anio_despacho'].astype(int)
        df_vmensual['mes_despacho'] = df_vmensual['mes_despacho'].astype(int)
        df_vmensual['fecha'] = pd.to_datetime(
            df_vmensual['anio_despacho'].astype(str) + '-' + df_vmensual['mes_despacho'].astype(str) + '-01')

        fechas_keys = convertir_claves_a_fechas(df_dictionary.keys())
        dft = df_vmensual[df_vmensual['fecha'].isin(fechas_keys)]
        df_new_dict = dict(zip(fechas_keys, df_dictionary.values()))
        lista_ciudades_precios = df_new_dict[fechas_keys[0]][0][0].columns[1:-1]

        demanda_df = create_demanda_time_series_dtframe(fechas_keys, lista_ciudades_precios, dft, df_new_dict)

        #add_demanda_nacional(demanda_df, df_vmensual)

        os.makedirs(DATA_DIR_ELASTICIDAD, exist_ok=True)  # Crea la carpeta si no existe. si existe no hace nada
        demanda_df.to_csv(demanda_df_file_path, index=False)

        demanda_df = add_demanda_nacional(demanda_df, df_vmensual)

    return demanda_df

