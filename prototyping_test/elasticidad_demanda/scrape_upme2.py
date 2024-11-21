
import pandas as pd

df = pd.read_csv("upm_urls.csv", sep=';', index_col=False)

import pandas as pd

import pandas as pd


def extract_precios(df):
    # df is the initial DataFrame containing anio, mes, url
    data_list = []

    for idx, row in df.iterrows():
        anio = row['anio']
        mes = row['mes']
        url = row['url']
        print(f"Processing {url}")
        current_data_list = []
        try:
            # Read the Excel file without setting a header
            excel_df = pd.read_excel(url, header=None)
        except Exception as e:
            print(f"Error reading Excel file from {url}: {e}")
            continue

        # Process 'corriente' data
        try:
            # Find the 'CIUDAD' row for corriente
            corriente_ciudad_rows = excel_df[excel_df[0].astype(str).str.strip().str.upper() == 'CIUDAD'].index
            if len(corriente_ciudad_rows) == 0:
                print(f"Could not find 'CIUDAD' row for corriente in {url}")
            else:
                corriente_ciudad_row = corriente_ciudad_rows[0]
                # Get cities
                cities = excel_df.loc[corriente_ciudad_row, 1:].dropna().astype(str).str.strip().tolist()
                # Find the 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA' row after 'CIUDAD'
                precio_rows = excel_df[0][corriente_ciudad_row + 1:].astype(str).str.strip().str.upper()
                if 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA' in precio_rows.values:
                    corriente_precio_row_rel_idx = \
                    precio_rows[precio_rows == 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA'].index[0]
                    corriente_precio_row_idx = corriente_precio_row_rel_idx
                    # Get precios
                    precios = excel_df.loc[corriente_precio_row_idx, 1:1 + len(cities) - 1].values.tolist()
                    # Collect data
                    for ciudad, precio in zip(cities, precios):
                        current_data_list.append({
                            'anio': anio,
                            'mes': mes,
                            'ciudad': ciudad,
                            'tipo': 'corriente',
                            'precio': precio
                        })
                else:
                    print(
                        f"Could not find 'PRECIO MAXIMO DE VENTA POR GALON INCLUIDA SOBRETASA' row for corriente in {url}")
        except Exception as e:
            print(f"Error processing corriente data in {url}: {e}")

        # Process 'acpm' data
        try:
            n_rows = excel_df.shape[0]
            if n_rows > 55:
                # Check if B56 (pandas row 55, col 1) is empty
                if pd.isna(excel_df.iloc[55, 1]):
                    # 'CIUDAD' row is at row 57 (Excel numbering)
                    acpm_ciudad_row = 56
                    acpm_precio_row = 73
                else:
                    # 'CIUDAD' row is at row 56 (Excel numbering)
                    acpm_ciudad_row = 55
                    acpm_precio_row = 72
                # Check if the rows exist
                if n_rows > acpm_ciudad_row and n_rows > acpm_precio_row:
                    # Get cities
                    acpm_cities = excel_df.loc[acpm_ciudad_row, 1:].dropna().astype(str).str.strip().tolist()
                    # Get precios
                    precios = excel_df.loc[acpm_precio_row, 1:1 + len(acpm_cities) - 1].values.tolist()
                    # Collect data
                    for ciudad, precio in zip(acpm_cities, precios):
                        current_data_list.append({
                            'anio': anio,
                            'mes': mes,
                            'ciudad': ciudad,
                            'tipo': 'acpm',
                            'precio': precio
                        })
                else:
                    print(f"Not enough rows to process acpm data in {url}")
            else:
                print(f"Not enough rows to process acpm data in {url}")
        except Exception as e:
            print(f"Error processing acpm data in {url}: {e}")

        # After processing both 'corriente' and 'acpm', compute averages
        # Compute average precio_corriente
        corriente_precios = [d['precio'] for d in current_data_list if
                             d['tipo'] == 'corriente' and pd.notnull(d['precio'])]
        promedio_corriente = sum(corriente_precios) / len(corriente_precios) if corriente_precios else None
        # Compute average precio_acpm
        acpm_precios = [d['precio'] for d in current_data_list if d['tipo'] == 'acpm' and pd.notnull(d['precio'])]
        promedio_acpm = sum(acpm_precios) / len(acpm_precios) if acpm_precios else None
        # Add average row
        current_data_list.append({
            'anio': anio,
            'mes': mes,
            'ciudad': 'promedio',
            'tipo': 'corriente',
            'precio': promedio_corriente
        })
        current_data_list.append({
            'anio': anio,
            'mes': mes,
            'ciudad': 'promedio',
            'tipo': 'acpm',
            'precio': promedio_acpm
        })
        # Append current_data_list to data_list
        data_list.extend(current_data_list)

    # Create a DataFrame from the collected data
    result_df = pd.DataFrame(data_list)
    # Pivot the DataFrame to get 'precio_corriente' and 'precio_acpm' in separate columns
    result_df = result_df.pivot_table(
        index=['anio', 'mes', 'ciudad'],
        columns='tipo',
        values='precio',
        aggfunc='first'
    ).reset_index()
    # Flatten the MultiIndex columns
    result_df.columns.name = None
    result_df = result_df.rename(columns={'corriente': 'precio_corriente', 'acpm': 'precio_acpm'})
    return result_df

pdf = extract_precios(df)
pdf.to_csv("df_precios.csv", index=False)






