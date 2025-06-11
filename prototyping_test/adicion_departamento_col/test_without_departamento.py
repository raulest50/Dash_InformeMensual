import os
import sys
import pandas as pd

# Add the parent directory to the path so we can import from services
sys.path.append('../..')
from services.informe_mensual_data import data_integrity, get_vmensual, get_vmensual_fpath

def test_without_departamento():
    """
    Tests the data_integrity function with a vmensual.parquet file that doesn't have the departamento column
    """
    # First, let's check the current vmensual.parquet
    print("Original vmensual.parquet:")
    df_original = get_vmensual()
    print(f"Shape: {df_original.shape}")
    print(f"Columns: {df_original.columns.tolist()}")
    
    # Make a backup of the current file
    backup_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              'data', 'informe_mensual', 'vmensual_backup.parquet')
    df_original.to_parquet(backup_path, engine='pyarrow', index=False)
    print(f"Backup created at: {backup_path}")
    
    # Create a modified version without the departamento column
    df_modified = df_original.drop(columns=['departamento'])
    print("\nModified dataframe (without departamento):")
    print(f"Shape: {df_modified.shape}")
    print(f"Columns: {df_modified.columns.tolist()}")
    
    # Save the modified dataframe to vmensual.parquet
    df_modified.to_parquet(get_vmensual_fpath(), engine='pyarrow', index=False)
    print("Modified dataframe saved to vmensual.parquet")
    
    # Run data_integrity
    print("\nRunning data_integrity...")
    data_integrity()
    
    # Check the updated vmensual.parquet
    print("\nAfter data_integrity:")
    df_after = get_vmensual()
    print(f"Shape: {df_after.shape}")
    print(f"Columns: {df_after.columns.tolist()}")
    print(f"Has departamento column: {'departamento' in df_after.columns}")
    
    # Check for duplicates
    print("\nChecking for duplicates...")
    keys_without_dept = ["anio_despacho", "mes_despacho", "producto", "municipio"]
    duplicates = df_after.duplicated(subset=keys_without_dept, keep=False)
    duplicate_count = duplicates.sum()
    print(f"Number of rows that are duplicates based on keys without departamento: {duplicate_count}")
    
    if duplicate_count > 0:
        print("\nSample of duplicates:")
        print(df_after[duplicates].sort_values(by=keys_without_dept).head(10))
    
    # Restore from backup
    print("\nRestoring from backup...")
    pd.read_parquet(backup_path, engine='pyarrow').to_parquet(
        get_vmensual_fpath(), engine='pyarrow', index=False)
    print("Restore complete")

if __name__ == "__main__":
    test_without_departamento()