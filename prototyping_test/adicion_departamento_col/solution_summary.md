# Solution Summary: Handling Departamento Column in vmensual.parquet

## Issue Description
The issue was related to updating the vmensual.parquet file with new data. The data source provides information with a 5-year window, and older data that falls outside this window would be lost if we simply replaced the entire file. To avoid this, a process was implemented to identify only new rows to add to the existing parquet file.

However, a recent improvement added a new column called "departamento" to the data. This caused a problem when comparing old data (without the departamento column or with NaN values) with new data (with the departamento column). The comparison would fail because of the difference in this column, causing duplications of data for older months.

## Solution Approach
The solution involved two main components:

1. **Creating a Municipality-Department Mapping**:
   - We found that there was already a script (`prototyping_test/municipio_departamento_mapping.py`) that creates a mapping between municipalities and departments.
   - This script queries the data source to get unique municipality-department pairs and saves them to both JSON and CSV files.
   - It can also update the vmensual.parquet file with the departamento column.

2. **Modifying the Data Integrity Process**:
   - We updated the `data_integrity()` function in `services/informe_mensual_data.py` to check if the departamento column exists in the old data.
   - If the column doesn't exist, it tries to load the municipality-department mapping from a JSON file.
   - If the mapping file doesn't exist, it attempts to create it by running the mapping script.
   - It then adds the departamento column to the old data using the mapping before concatenating with the new data.
   - This ensures that the deduplication process works correctly, as both old and new data now have the departamento column.

## Implementation Details
1. Added code to check if the departamento column exists in the old data.
2. Added robust error handling for loading and creating the mapping.
3. Added detailed logging to help diagnose any issues.
4. Ensured that the code works even if the mapping file doesn't exist or can't be loaded.

## Testing
We created test scripts to verify the solution:
1. `check_vmensual_structure.py`: Checks the structure of vmensual.parquet.
2. `check_nan_values.py`: Checks for NaN values in the departamento column.
3. `test_data_integrity.py`: Tests the data_integrity function with the current vmensual.parquet.
4. `test_without_departamento.py`: Tests the data_integrity function with a modified vmensual.parquet that doesn't have the departamento column.

The tests confirmed that our solution successfully addresses the issue. When the old data doesn't have the departamento column, the code now adds it using the mapping before concatenation, preventing the duplication issue.

## Remaining Considerations
There are still some duplicates in the data, but these are legitimate cases where the same municipality name exists in multiple departments. For example:
- ALBAN exists in both CUNDINAMARCA and NARIÑO
- ALBANIA exists in both CAQUETA and LA GUAJIRA
- ARGELIA exists in ANTIOQUIA, CAUCA, and VALLE DEL CAUCA

These duplicates are due to the nature of the data itself, not an error in our code. The deduplication process correctly identifies these as different municipalities because they have different department values.

## Future Improvements
1. Consider adding more robust validation of the mapping data.
2. Implement a more efficient way to update the departamento column for large datasets.
3. Add unit tests to ensure the data_integrity function continues to work correctly with future changes.