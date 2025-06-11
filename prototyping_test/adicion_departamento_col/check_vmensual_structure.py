import os
import sys
import pandas as pd

# Add the parent directory to the path so we can import from services
sys.path.append('../..')
from services.informe_mensual_data import get_vmensual

def check_vmensual_structure():
    """
    Checks the structure of vmensual.parquet file
    """
    # Read the vmensual.parquet file
    df = get_vmensual()
    
    # Print basic information
    print(f"Shape of vmensual.parquet: {df.shape}")
    print(f"Columns in vmensual.parquet: {df.columns.tolist()}")
    
    # Check if departamento column exists
    has_departamento = 'departamento' in df.columns
    print(f"Has 'departamento' column: {has_departamento}")
    
    # Print a few sample rows
    print("\nSample rows:")
    print(df.head(3))

if __name__ == "__main__":
    check_vmensual_structure()