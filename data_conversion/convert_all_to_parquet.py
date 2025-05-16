# Main script to convert all CSV files to Parquet format
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the conversion functions from the data_conversion package
from data_conversion.csv_to_parquet_vmensual import convert_vmensual_to_parquet
from data_conversion.csv_to_parquet_info_mercado import convert_info_mercado_to_parquet

def main():
    """
    Run all conversion scripts to convert CSV files to Parquet format.
    """
    # Print debugging information
    print("Starting conversion of all CSV files to Parquet format...")
    print(f"Current working directory: {os.getcwd()}")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    print(f"Script directory: {script_dir}")
    print(f"Project root: {project_root}")

    # Check if the CSV files exist
    vmensual_csv = os.path.join(project_root, 'data', 'informe_mensual', 'vmensual.csv')
    info_mercado_csv = os.path.join(project_root, 'data', 'mercado_eds', 'info_mercado.csv')
    print(f"Checking if vmensual.csv exists: {os.path.exists(vmensual_csv)}")
    print(f"Checking if info_mercado.csv exists: {os.path.exists(info_mercado_csv)}")

    # Convert vmensual.csv
    print("\n=== Converting vmensual.csv ===")
    vmensual_success = convert_vmensual_to_parquet()

    # Convert info_mercado.csv
    print("\n=== Converting info_mercado.csv ===")
    info_mercado_success = convert_info_mercado_to_parquet()

    # Summary
    print("\n=== Conversion Summary ===")
    print(f"vmensual.csv: {'Success' if vmensual_success else 'Failed'}")
    print(f"info_mercado.csv: {'Success' if info_mercado_success else 'Failed'}")

    if vmensual_success and info_mercado_success:
        print("\nAll files successfully converted to Parquet format.")
    else:
        print("\nSome files failed to convert. Check the logs above for details.")

if __name__ == "__main__":
    main()
