import os
import sys

# Add the parent directory to the path so we can import from services
sys.path.append('../..')
from services.informe_mensual_data import data_integrity, get_vmensual_fpath

def run_data_integrity():
    """
    Runs the data_integrity function to fetch data and create vmensual.parquet
    """
    # Create the directory if it doesn't exist
    vmensual_path = get_vmensual_fpath()
    directory = os.path.dirname(vmensual_path)
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)

    print("Running data_integrity to fetch data and create vmensual.parquet...")
    data_integrity()
    print("Completed data_integrity.")

if __name__ == "__main__":
    run_data_integrity()
