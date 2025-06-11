import os
import sys
import pandas as pd

# Add the parent directory to the path so we can import from services
sys.path.append('../..')
from services.informe_mensual_data import data_integrity

def test_import_fix():
    """
    Tests if the fix for the import statement in informe_mensual_data.py works correctly
    """
    print("Testing import fix...")
    try:
        # Try to run data_integrity
        data_integrity()
        print("Success! The import statement works correctly.")
    except ImportError as e:
        print(f"Import error: {str(e)}")
    except Exception as e:
        print(f"Other error: {str(e)}")

if __name__ == "__main__":
    test_import_fix()