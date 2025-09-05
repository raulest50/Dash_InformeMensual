import os
import pandas as pd
import services.general as general

"""
Script to fetch and process data from the SICOM database and save it as a parquet file.
This script follows best practices for file handling, data type conversion, and error handling.
"""

DB_ALIAS_VOL_MAYORISTAS = "339g-zjac"

# Get absolute path for the parquet file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
PARQUET_FILE_PATH = os.path.join(project_root, 'data', 'informe_mensual', 'vmensual.parquet')


def get_query_vmensual():
    """
    Generate the SQL query to fetch data from the SICOM database.

    Returns:
        str: SQL query string
    """
    query = (
        f"SELECT SUM(volumen_despachado) as volumen_total, anio_despacho, mes_despacho, producto, municipio, departamento "
        f"WHERE subtipo_comprador IN ('{general.C1}', '{general.C2}', '{general.C3}') "
        f"AND producto IN ('{general.P1}', '{general.P2}', '{general.P3}') "
        f"GROUP BY anio_despacho, mes_despacho, producto, municipio, departamento "
        f"ORDER BY anio_despacho ASC "
        f"LIMIT 850000"
    )
    return query


def main(force_update=False):
    """
    Main function to process and save the data.

    Args:
        force_update (bool): If True, forces an update of the parquet file even if it exists.
    """
    global df_fresh

    if not os.path.exists(PARQUET_FILE_PATH) or force_update:
        print(f"Fetching data from SICOM database...")
        try:
            # Fetch data from SICOM
            df_fresh = general.fetch_socrata_datosgov(get_query_vmensual(), DB_ALIAS_VOL_MAYORISTAS, 30)

            # Convert numeric columns
            df_fresh['mes_despacho'] = pd.to_numeric(df_fresh['mes_despacho'], errors='coerce')
            df_fresh['anio_despacho'] = pd.to_numeric(df_fresh['anio_despacho'], errors='coerce')
            df_fresh['volumen_total'] = pd.to_numeric(df_fresh['volumen_total'], errors='coerce')

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(PARQUET_FILE_PATH), exist_ok=True)

            # Backup existing file if it exists and force_update is True
            if os.path.exists(PARQUET_FILE_PATH) and force_update:
                backup_dir = os.path.join(os.path.dirname(PARQUET_FILE_PATH), 'old')
                os.makedirs(backup_dir, exist_ok=True)

                # Create backup filename with timestamp
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(backup_dir, f"vmensual_backup_{timestamp}.parquet")

                # Copy existing file to backup
                import shutil
                shutil.copy2(PARQUET_FILE_PATH, backup_path)
                print(f"Backed up existing file to {backup_path}")

            # Save to parquet with compression
            df_fresh.to_parquet(
                PARQUET_FILE_PATH, 
                engine='pyarrow', 
                compression='snappy',  # Add compression
                index=False
            )
            print(f"Data successfully saved to {PARQUET_FILE_PATH}")
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            df_fresh = pd.DataFrame()  # Create empty DataFrame in case of error
    else:
        try:
            # Load existing parquet file
            df_fresh = pd.read_parquet(PARQUET_FILE_PATH, engine='pyarrow')
            print(f"Loaded existing parquet file: {PARQUET_FILE_PATH}")
        except Exception as e:
            print(f"Error reading parquet file: {str(e)}")
            df_fresh = pd.DataFrame()  # Create empty DataFrame in case of error

    return df_fresh


# Execute main function if script is run directly
if __name__ == "__main__":
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process vmensual data.')
    parser.add_argument('--force-update', action='store_true', help='Force update of vmensual.parquet file')
    args = parser.parse_args()

    # Run main function with force_update parameter
    df_fresh = main(force_update=args.force_update)

    # Print summary information (only when run directly)
    print(f"Total records: {len(df_fresh)}")
    print(f"Columns: {df_fresh.columns.tolist()}")

    # Check for latest data
    if 'anio_despacho' in df_fresh.columns:
        latest_year = df_fresh['anio_despacho'].max()
        records_latest_year = len(df_fresh[df_fresh['anio_despacho'] == latest_year])
        print(f"Latest year in data: {latest_year}")
        print(f"Records for latest year: {records_latest_year}")
else:
    # When imported as a module, just run main without force update
    df_fresh = main(force_update=False)
