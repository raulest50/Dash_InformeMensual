import os
import sys
import pandas as pd

# Add the parent directory to the path so we can import from services
sys.path.append('../..')
from services.informe_mensual_data import data_integrity, get_vmensual

def test_data_integrity():
    """
    Tests the data_integrity function to see how it handles the departamento column
    """
    # First, let's check the current vmensual.parquet
    print("Before data_integrity:")
    df_before = get_vmensual()
    print(f"Shape: {df_before.shape}")
    print(f"Columns: {df_before.columns.tolist()}")
    print(f"Has departamento column: {'departamento' in df_before.columns}")
    
    # Make a backup of the current file
    backup_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              'data', 'informe_mensual', 'vmensual_backup.parquet')
    df_before.to_parquet(backup_path, engine='pyarrow', index=False)
    print(f"Backup created at: {backup_path}")
    
    # Run data_integrity
    print("\nRunning data_integrity...")
    data_integrity()
    
    # Check the updated vmensual.parquet
    print("\nAfter data_integrity:")
    df_after = get_vmensual()
    print(f"Shape: {df_after.shape}")
    print(f"Columns: {df_after.columns.tolist()}")
    print(f"Has departamento column: {'departamento' in df_after.columns}")
    
    # Compare before and after
    print("\nComparison:")
    print(f"Rows added: {len(df_after) - len(df_before)}")
    
    # Restore from backup
    print("\nRestoring from backup...")
    df_before.to_parquet(os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                     'data', 'informe_mensual', 'vmensual.parquet'), 
                        engine='pyarrow', index=False)
    print("Restore complete")

if __name__ == "__main__":
    test_data_integrity()