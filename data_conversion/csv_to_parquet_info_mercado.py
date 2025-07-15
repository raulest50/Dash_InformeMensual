# Script to convert info_mercado.csv to Parquet format
import os
import sys
import pandas as pd

def convert_info_mercado_to_parquet():
    """
    Convert info_mercado.csv to Parquet format and save it in the same directory.
    Includes data type conversions and compression for optimal storage.
    """
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))

    # Define file paths with absolute paths
    csv_file_path = os.path.join(project_root, 'data', 'mercado_eds', 'info_mercado.csv')
    parquet_file_path = os.path.join(project_root, 'data', 'mercado_eds', 'info_mercado.parquet')

    print(f"Converting {csv_file_path} to Parquet format...")

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file {csv_file_path} not found.")
        return False

    try:
        # Read CSV file with specific parameters
        df = pd.read_csv(
            csv_file_path,
            sep=';',
            encoding='utf-8',
            decimal=','
        )

        # Convert numeric columns to ensure proper data types
        # This helps with filtering and calculations in the application
        numeric_columns = df.select_dtypes(include=['object']).columns
        for col in numeric_columns:
            # Try to convert columns that might contain numeric values
            try:
                # Check if column contains numeric-like strings
                if df[col].str.match(r'^-?\d+\.?\d*$').any():
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                # Skip columns that can't be converted
                pass

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
    convert_info_mercado_to_parquet()
