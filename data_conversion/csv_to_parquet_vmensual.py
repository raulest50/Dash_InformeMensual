# Script to convert vmensual.csv to Parquet format
import os
import sys
import pandas as pd

def convert_vmensual_to_parquet():
    """
    Convert vmensual.csv to Parquet format and save it in the same directory.
    Includes data type conversions and compression for optimal storage.
    """
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))

    # Define file paths with absolute paths
    csv_file_path = os.path.join(project_root, 'data', 'informe_mensual', 'vmensual.csv')
    parquet_file_path = os.path.join(project_root, 'data', 'informe_mensual', 'vmensual.parquet')

    print(f"Converting {csv_file_path} to Parquet format...")

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file {csv_file_path} not found.")
        return False

    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)

        # Convert numeric columns to ensure proper data types
        # This helps with filtering and calculations in the application
        df['mes_despacho'] = pd.to_numeric(df['mes_despacho'], errors='coerce')
        df['anio_despacho'] = pd.to_numeric(df['anio_despacho'], errors='coerce')
        df['volumen_total'] = pd.to_numeric(df['volumen_total'], errors='coerce')

        # Convert to Parquet format with compression
        df.to_parquet(
            parquet_file_path, 
            engine='pyarrow',
            compression='snappy',  # Add compression for smaller file size
            index=False
        )

        print(f"Successfully converted to {parquet_file_path}")
        print(f"Original CSV size: {os.path.getsize(csv_file_path) / (1024 * 1024):.2f} MB")
        print(f"Parquet size: {os.path.getsize(parquet_file_path) / (1024 * 1024):.2f} MB")
        print(f"Compression ratio: {os.path.getsize(parquet_file_path) / os.path.getsize(csv_file_path):.2f}")

        return True
    except Exception as e:
        print(f"Error converting file: {e}")
        return False

if __name__ == "__main__":
    convert_vmensual_to_parquet()
