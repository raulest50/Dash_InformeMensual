import os
import pandas as pd
import services.general as general

"""
Script to update the vmensual.parquet file with fresh data from Socrata.
This script completely replaces the existing data with fresh data from Socrata.
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


def update_vmensual():
    """
    Update the vmensual.parquet file with fresh data from Socrata.
    This function completely replaces the existing data with fresh data.
    """
    print(f"Fetching fresh data from SICOM database...")
    try:
        # Fetch data from SICOM
        df_fresh = general.fetch_socrata_datosgov(get_query_vmensual(), DB_ALIAS_VOL_MAYORISTAS, 30)
        
        # Convert numeric columns
        df_fresh['mes_despacho'] = pd.to_numeric(df_fresh['mes_despacho'], errors='coerce')
        df_fresh['anio_despacho'] = pd.to_numeric(df_fresh['anio_despacho'], errors='coerce')
        df_fresh['volumen_total'] = pd.to_numeric(df_fresh['volumen_total'], errors='coerce')
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(PARQUET_FILE_PATH), exist_ok=True)
        
        # Backup existing file if it exists
        if os.path.exists(PARQUET_FILE_PATH):
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
        
        # Save fresh data to parquet with compression
        df_fresh.to_parquet(
            PARQUET_FILE_PATH, 
            engine='pyarrow', 
            compression='snappy',
            index=False
        )
        print(f"Fresh data successfully saved to {PARQUET_FILE_PATH}")
        print(f"Total records: {len(df_fresh)}")
        
        return df_fresh
    except Exception as e:
        print(f"Error updating vmensual.parquet: {str(e)}")
        return None


if __name__ == "__main__":
    df = update_vmensual()
    
    if df is not None:
        # Print summary information
        print(f"Columns: {df.columns.tolist()}")
        
        # Check for recent data
        if 'anio_despacho' in df.columns:
            latest_year = df['anio_despacho'].max()
            records_latest_year = len(df[df['anio_despacho'] == latest_year])
            print(f"Latest year in data: {latest_year}")
            print(f"Records for latest year: {records_latest_year}")