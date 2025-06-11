import os
import sys
import pandas as pd

# Add the parent directory to the path so we can import from services
sys.path.append('../..')
from services.informe_mensual_data import get_vmensual

def check_nan_values():
    """
    Checks for NaN values in the departamento column of vmensual.parquet
    """
    # Read the vmensual.parquet file
    df = get_vmensual()
    
    # Check for NaN values in departamento column
    nan_count = df['departamento'].isna().sum()
    print(f"Number of NaN values in departamento column: {nan_count}")
    print(f"Percentage of NaN values: {nan_count / len(df) * 100:.2f}%")
    
    # Show a few rows with NaN values in departamento
    if nan_count > 0:
        print("\nSample rows with NaN values in departamento:")
        print(df[df['departamento'].isna()].head(5))
        
        # Count unique municipalities with NaN departamento
        unique_municipios = df[df['departamento'].isna()]['municipio'].nunique()
        print(f"\nNumber of unique municipalities with NaN departamento: {unique_municipios}")
        print("\nSample of municipalities with NaN departamento:")
        print(df[df['departamento'].isna()]['municipio'].value_counts().head(10))

if __name__ == "__main__":
    check_nan_values()