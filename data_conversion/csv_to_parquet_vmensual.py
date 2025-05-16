# Script to convert vmensual.csv to Parquet format
import os
import sys
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def convert_vmensual_to_parquet():
    """
    Convert vmensual.csv to Parquet format and save it in the same directory.
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

        # Convert to Parquet format
        df.to_parquet(parquet_file_path, engine='pyarrow')

        print(f"Successfully converted to {parquet_file_path}")
        print(f"Original CSV size: {os.path.getsize(csv_file_path) / (1024 * 1024):.2f} MB")
        print(f"Parquet size: {os.path.getsize(parquet_file_path) / (1024 * 1024):.2f} MB")

        return True
    except Exception as e:
        print(f"Error converting file: {e}")
        return False

if __name__ == "__main__":
    convert_vmensual_to_parquet()
