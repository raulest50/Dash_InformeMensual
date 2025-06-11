# standar lib imports
import os
import json

# 3rd party imports
import pandas as pd

import services.general as general

DB_ALIAS_VOL_MAYORISTAS = "339g-zjac"


def get_vmensual_fpath():
    if __name__ == "__main__":
        DATA_DIR_INF_MENSUAL_MAIN = '../data/informe_mensual/'
        return os.path.join(DATA_DIR_INF_MENSUAL_MAIN, 'vmensual.parquet')
    else:
        DATA_DIR_INF_MENSUAL = 'data/informe_mensual'
        return os.path.join(DATA_DIR_INF_MENSUAL, 'vmensual.parquet')


def get_vmensual():
    VMENSUAL_FILEPATH = get_vmensual_fpath()
    if os.path.exists(VMENSUAL_FILEPATH):
        return pd.read_parquet(VMENSUAL_FILEPATH, engine='pyarrow')
    else:
        print("scratch intilizacion for vmensual.parquet")
        return pd.DataFrame()

def data_integrity():
    df_old = get_vmensual()
    print(f"df_old len: {len(df_old)}")

    df_new = general.fetch_socrata_datosgov(get_query_vmensual(), DB_ALIAS_VOL_MAYORISTAS, 20)
    print(df_new)
    df_new["anio_despacho"] = pd.to_numeric(df_new["anio_despacho"], errors="coerce")
    df_new["mes_despacho"] = pd.to_numeric(df_new["mes_despacho"], errors="coerce")
    df_new["volumen_total"] = pd.to_numeric(df_new["volumen_total"], errors="coerce")

    print(f"df_new len: {len(df_new)}")

    # Check if departamento column exists in df_old
    if 'departamento' not in df_old.columns:
        print("departamento column not found in old data, adding it using mapping...")
        # Load the municipio-departamento mapping
        # Get the directory where vmensual.parquet is located
        vmensual_dir = os.path.dirname(get_vmensual_fpath())
        mapping_file = os.path.join(vmensual_dir, 'municipio_departamento_mapping.json')

        print(f"Looking for mapping file at: {mapping_file}")

        if os.path.exists(mapping_file):
            print(f"Mapping file found at: {mapping_file}")
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping_dict = json.load(f)
            # Add departamento column using the mapping
            df_old['departamento'] = df_old['municipio'].map(mapping_dict)
            print(f"Added departamento column to old data using mapping")
        else:
            # Try to run the mapping script to create the mapping file
            print(f"Mapping file not found, attempting to create it...")
            try:
                # Import the mapping script
                import sys
                sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prototyping_test'))
                from prototyping_test.adicion_departamento_col.municipio_departamento_mapping import create_municipio_departamento_mapping

                # Create the mapping
                mapping_dict, _ = create_municipio_departamento_mapping()

                # Add departamento column using the mapping
                df_old['departamento'] = df_old['municipio'].map(mapping_dict)
                print(f"Added departamento column to old data using newly created mapping")
            except Exception as e:
                print(f"Error creating mapping: {str(e)}")
                print(f"Warning: Could not create mapping, departamento column will have NaN values")
                df_old['departamento'] = None

    KEYS = ["anio_despacho", "mes_despacho", "producto", "municipio", "departamento"]
    df_union = (
        pd.concat([df_old, df_new], ignore_index=True)
        .drop_duplicates(subset=KEYS, keep="last")
    )

    print(f"df_union len: {len(df_union)}")
    df_union.to_parquet(get_vmensual_fpath(), engine='pyarrow', index=False)


def get_query_vmensual():
    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio, departamento "
        f"WHERE subtipo_comprador IN ('{general.C1}', '{general.C2}', '{general.C3}') "
        f"AND producto IN ('{general.P1}', '{general.P2}', '{general.P3}') "
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio, departamento "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 250000"
    )
    return query


class InformeMensualLoad:
    def __init__(self):
        self.df = get_vmensual()

    def format_zdf_list(self, zdf_list, n=10):
        return '\n'.join(', '.join(zdf_list[i:i + n]) for i in range(0, len(zdf_list), n))


if __name__ == "__main__":
    data_integrity()
