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


def main():
    """Main function to process and save the data."""
    global df_fresh

    if not os.path.exists(PARQUET_FILE_PATH):
        print(f"Fetching data from SICOM database...")
        try:
            # Fetch data from SICOM
            df_fresh = general.fetch_socrata_datosgov(get_query_vmensual(), DB_ALIAS_VOL_MAYORISTAS, 20)

            # Convert numeric columns
            df_fresh['mes_despacho'] = pd.to_numeric(df_fresh['mes_despacho'], errors='coerce')
            df_fresh['anio_despacho'] = pd.to_numeric(df_fresh['anio_despacho'], errors='coerce')
            df_fresh['volumen_total'] = pd.to_numeric(df_fresh['volumen_total'], errors='coerce')

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
    df_fresh = main()

    # Print summary information (only when run directly)
    print(f"Total records: {len(df_fresh)}")
    print(f"Columns: {df_fresh.columns.tolist()}")

    # Check for 2025 data
    if 'anio_despacho' in df_fresh.columns:
        year_2025_count = len(df_fresh[df_fresh['anio_despacho'] == 2025])
        print(f"Records for year 2025: {year_2025_count}")
else:
    # When imported as a module, just run main without debug output
    df_fresh = main()
