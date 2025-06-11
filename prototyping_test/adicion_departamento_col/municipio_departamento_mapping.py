# Script to create a mapping of municipalities to departments and update vmensual.parquet
import os
import sys
import pandas as pd
import json

# Add the parent directory to the path so we can import from services
sys.path.append('../..')
import services.general as general
from services.informe_mensual_data import DB_ALIAS_VOL_MAYORISTAS, get_vmensual, get_vmensual_fpath

def create_municipio_departamento_mapping():
    """
    Creates a mapping of municipalities to departments by querying the data source.
    Saves the mapping to both JSON and CSV files for future use.
    Updates vmensual.parquet with the departamento column.
    """
    # Query to get unique municipality-department pairs
    query = (
        f"SELECT DISTINCT municipio, departamento "
        f"WHERE subtipo_comprador IN ('{general.C1}', '{general.C2}', '{general.C3}') "
        f"AND producto IN ('{general.P1}', '{general.P2}', '{general.P3}') "
        f"AND departamento IS NOT NULL "
        f"AND municipio IS NOT NULL "
        f"ORDER BY departamento, municipio "
        f"LIMIT 50000"
    )
    
    print("Fetching municipality-department mapping from data source...")
    df_mapping = general.fetch_socrata_datosgov(query, DB_ALIAS_VOL_MAYORISTAS, 20)
    
    # Check the results
    print(f"Retrieved {len(df_mapping)} unique municipality-department pairs")
    
    # Create mapping dictionary
    mapping_dict = dict(zip(df_mapping['municipio'], df_mapping['departamento']))
    
    # Save mapping to JSON file
    mapping_file_json = '../../data/informe_mensual/municipio_departamento_mapping.json'
    os.makedirs(os.path.dirname(mapping_file_json), exist_ok=True)
    with open(mapping_file_json, 'w', encoding='utf-8') as f:
        json.dump(mapping_dict, f, ensure_ascii=False, indent=4)
    
    # Save mapping to CSV file for easier viewing
    mapping_file_csv = '../../data/informe_mensual/municipio_departamento_mapping.csv'
    df_mapping.to_csv(mapping_file_csv, index=False, encoding='utf-8')
    
    print(f"Mapping saved to {mapping_file_json} and {mapping_file_csv}")
    
    # Read vmensual.parquet
    df_vmensual = get_vmensual()
    print(f"Read vmensual.parquet with shape: {df_vmensual.shape}")
    
    # Check if departamento column exists
    has_departamento = 'departamento' in df_vmensual.columns
    print(f"vmensual.parquet has 'departamento' column: {has_departamento}")
    
    if has_departamento:
        # Count NaN values in departamento column
        nan_count = df_vmensual['departamento'].isna().sum()
        print(f"Number of NaN values in departamento column: {nan_count}")
        
        # Update NaN values in departamento column using the mapping
        for idx, row in df_vmensual.iterrows():
            if pd.isna(row['departamento']) and row['municipio'] in mapping_dict:
                df_vmensual.at[idx, 'departamento'] = mapping_dict[row['municipio']]
        
        # Count NaN values after update
        nan_count_after = df_vmensual['departamento'].isna().sum()
        print(f"Number of NaN values in departamento column after update: {nan_count_after}")
    else:
        # Add departamento column using the mapping
        df_vmensual['departamento'] = df_vmensual['municipio'].map(mapping_dict)
        print("Added departamento column to vmensual.parquet")
    
    # Save updated dataframe back to vmensual.parquet
    df_vmensual.to_parquet(get_vmensual_fpath(), engine='pyarrow', index=False)
    print(f"Updated vmensual.parquet saved with shape: {df_vmensual.shape}")
    
    return mapping_dict, df_mapping

def display_mapping_sample(mapping_dict, df_mapping):
    """Displays a sample of the mapping for verification"""
    print("\nSample of municipio to departamento mapping:")
    count = 0
    for municipio, departamento in list(mapping_dict.items())[:10]:
        print(f"{municipio}: {departamento}")
        count += 1
        if count >= 10:
            break
    
    print(f"\nTotal municipalities mapped: {len(mapping_dict)}")
    
    # Display statistics by department
    print("\nMunicipalities per department:")
    dept_counts = df_mapping.groupby('departamento').size().sort_values(ascending=False)
    for dept, count in dept_counts.head(10).items():
        print(f"{dept}: {count} municipalities")

if __name__ == '__main__':
    mapping_dict, df_mapping = create_municipio_departamento_mapping()
    display_mapping_sample(mapping_dict, df_mapping)