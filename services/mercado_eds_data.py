import pandas as pd
import numpy as np
import os
import json

class MercadoEDSLoad:
    """
    Class to load and process data for the Estudio de mercado EDS page.
    """

    def __init__(self):
        """
        Initialize the data loader and load only the SICOM codes.
        """
        self.df = None
        self.sicom_codes = []
        self.load_data()  # Solo cargará los códigos SICOM, no todo el dataset

    def load_data(self, sicom_code=None):
        """
        Load the data from the Parquet file, optionally filtering by SICOM code.
        """
        try:
            file_path = os.path.join('data', 'mercado_eds', 'info_mercado.parquet')

            if sicom_code is not None:
                # Solo cargar las filas relevantes para el código SICOM específico
                # Usar la función read_parquet con parámetros para filtrar durante la carga
                self.df = pd.read_parquet(
                    file_path,
                    engine='pyarrow',
                    columns=[
                        'SICOM', 'COMPETIDOR', 'NOMBRE COMERCIAL', 'BANDERA',
                        'Coord_X', 'Coord_Y', 'DEPARTAMENTO', 'MUNICIPIO', 'URBANO',
                        'IHH_ACPM', 'IHH_CORRIENTE', 'IHH_EXTRA2', 
                        'Stenbacka_ACPM', 'Stenbacka_CORRIENTE', 'Stenbacka_EXTRA',
                        'Coord_X_Com', 'Coord_Y_Com', 'Nom_Com', 'BANDERA_COM', 'DISTANCIA'
                    ]
                )
                # Filtrar solo para el código SICOM solicitado
                self.df = self.df[self.df['SICOM'] == sicom_code]

                # Convert coordinates to float
                self.df['Coord_X'] = pd.to_numeric(self.df['Coord_X'], errors='coerce')
                self.df['Coord_Y'] = pd.to_numeric(self.df['Coord_Y'], errors='coerce')
                self.df['Coord_X_Com'] = pd.to_numeric(self.df['Coord_X_Com'], errors='coerce')
                self.df['Coord_Y_Com'] = pd.to_numeric(self.df['Coord_Y_Com'], errors='coerce')
            else:
                # Para la inicialización, solo cargar los códigos SICOM únicos
                sicom_df = pd.read_parquet(
                    file_path,
                    engine='pyarrow',
                    columns=['SICOM']
                )
                self.sicom_codes = sorted(sicom_df['SICOM'].unique())
                # Liberar memoria
                self.df = None

        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()
            self.sicom_codes = []

    def get_eds_details(self, sicom_code):
        """
        Get details for a specific EDS.

        Args:
            sicom_code (str): The SICOM code of the EDS.

        Returns:
            dict: A dictionary with the EDS details.
        """
        # Cargar datos solo para este código SICOM si aún no están cargados
        if self.df is None or len(self.df) == 0 or self.df['SICOM'].iloc[0] != sicom_code:
            self.load_data(sicom_code)

        if self.df is None or self.df.empty:
            return {}

        # Filter for the specific EDS
        eds_data = self.df[self.df['SICOM'] == sicom_code].iloc[0] if not self.df[self.df['SICOM'] == sicom_code].empty else None

        if eds_data is None:
            return {}

        # Get the number of competitors
        competitors = self.df[self.df['SICOM'] == sicom_code]['COMPETIDOR'].nunique()

        # Determine the market radius based on URBANO flag
        market_radius = "4 km" if eds_data['URBANO'] == 1 else "10 km"

        return {
            'nombre_comercial': eds_data['NOMBRE COMERCIAL'],
            'bandera': eds_data['BANDERA'],
            'departamento': eds_data['DEPARTAMENTO'],
            'municipio': eds_data['MUNICIPIO'],
            'num_competidores': competitors,
            'radio_mercado': market_radius,
            'coords': [eds_data['Coord_X'], eds_data['Coord_Y']],
            'ihh_acpm': eds_data['IHH_ACPM'],
            'ihh_corriente': eds_data['IHH_CORRIENTE'],
            'ihh_extra': eds_data['IHH_EXTRA2'],
            'stenbacka_acpm': eds_data['Stenbacka_ACPM'],
            'stenbacka_corriente': eds_data['Stenbacka_CORRIENTE'],
            'stenbacka_extra': eds_data['Stenbacka_EXTRA']
        }

    def get_competitors(self, sicom_code):
        """
        Get the competitors for a specific EDS.

        Args:
            sicom_code (int or str): The SICOM code of the EDS.

        Returns:
            DataFrame: A DataFrame with columns
                ['SICOM', 'Nombre Comercial', 'Bandera', 'Longitud', 'Latitud', 'Distancia'].
                Longitude/latitude columns will be strings (empty if missing).
        """
        # Cargar datos solo para este código SICOM si aún no están cargados
        if self.df is None or len(self.df) == 0 or self.df['SICOM'].iloc[0] != sicom_code:
            self.load_data(sicom_code)

        # If there's no data loaded, return empty DataFrame
        if self.df is None or self.df.empty:
            return pd.DataFrame()

        # Filter to only the rows matching the requested SICOM
        competitors = self.df[self.df['SICOM'] == sicom_code].copy()

        # Keep only the relevant columns
        competitor_cols = [
            'COMPETIDOR',  # will become SICOM
            'Nom_Com',  # Nombre Comercial
            'BANDERA_COM',  # Bandera
            'Coord_X_Com',  # Longitud (string→float→string)
            'Coord_Y_Com',  # Latitud  (string→float→string)
            'DISTANCIA'  # Distancia
        ]
        competitors = competitors[competitor_cols].copy()

        # Normalize the decimal separator and convert to numeric
        for col in ['Coord_X_Com', 'Coord_Y_Com']:
            competitors[col] = (
                competitors[col]
                .astype(str)  # ensure we can call .str.replace
                .str.replace(',', '.', regex=False)
                .pipe(pd.to_numeric, errors='coerce')
            )

        # Fill NaN with empty string and cast back to str for display
        competitors['Coord_X_Com'] = competitors['Coord_X_Com'].fillna('').astype(str)
        competitors['Coord_Y_Com'] = competitors['Coord_Y_Com'].fillna('').astype(str)

        # Rename columns for the table
        competitors.columns = [
            'SICOM',
            'Nombre Comercial',
            'Bandera',
            'Longitud',
            'Latitud',
            'Distancia'
        ]

        return competitors

    def get_competitor_brands_distribution(self, sicom_code):
        """
        Get the distribution of competitor brands for a specific EDS.

        Args:
            sicom_code (str): The SICOM code of the EDS.

        Returns:
            DataFrame: A DataFrame with the brand distribution.
        """
        # Cargar datos solo para este código SICOM si aún no están cargados
        if self.df is None or len(self.df) == 0 or self.df['SICOM'].iloc[0] != sicom_code:
            self.load_data(sicom_code)

        if self.df is None or self.df.empty:
            return pd.DataFrame()

        # Filter for the specific EDS's competitors
        competitors = self.df[self.df['SICOM'] == sicom_code].copy()

        # Count occurrences of each brand
        brand_counts = competitors['BANDERA_COM'].value_counts().reset_index()
        brand_counts.columns = ['Bandera', 'Cantidad']

        return brand_counts

    def get_map_data(self, sicom_code):
        """
        Get the data for the map visualization.

        Args:
            sicom_code (str): The SICOM code of the EDS.

        Returns:
            dict: A dictionary with the map data.
        """
        # Cargar datos solo para este código SICOM si aún no están cargados
        if self.df is None or len(self.df) == 0 or self.df['SICOM'].iloc[0] != sicom_code:
            self.load_data(sicom_code)

        if self.df is None or self.df.empty:
            return {'eds': {}, 'competitors': []}

        # Get the EDS data
        eds_data = self.df[self.df['SICOM'] == sicom_code].iloc[0] if not self.df[self.df['SICOM'] == sicom_code].empty else None

        if eds_data is None:
            return {'eds': {}, 'competitors': []}

        # Get the competitors data
        competitors = self.df[self.df['SICOM'] == sicom_code].copy()

        # Ensure coordinates are numeric
        eds_coord_x = pd.to_numeric(eds_data['Coord_X'], errors='coerce')
        eds_coord_y = pd.to_numeric(eds_data['Coord_Y'], errors='coerce')

        # Prepare the EDS data for the map
        eds_map_data = {
            'sicom': sicom_code,
            'nombre': eds_data['NOMBRE COMERCIAL'],
            'bandera': eds_data['BANDERA'],
            'coords': [eds_coord_x, eds_coord_y]
        }

        # Prepare the competitors data for the map
        competitors_map_data = []
        for _, comp in competitors.iterrows():
            # Ensure coordinates are numeric
            comp_coord_x = pd.to_numeric(comp['Coord_X_Com'], errors='coerce')
            comp_coord_y = pd.to_numeric(comp['Coord_Y_Com'], errors='coerce')

            # Only add competitors with valid coordinates
            if not (pd.isna(comp_coord_x) or pd.isna(comp_coord_y)):
                competitors_map_data.append({
                    'sicom': comp['COMPETIDOR'],
                    'nombre': comp['Nom_Com'],
                    'bandera': comp['BANDERA_COM'],
                    'coords': [comp_coord_x, comp_coord_y],
                    'distancia': comp['DISTANCIA']
                })

        return {
            'eds': eds_map_data,
            'competitors': competitors_map_data
        }

    def get_minimal_data(self, sicom_code):
        """
        Get minimal data for client-side processing.

        Args:
            sicom_code (str): The SICOM code of the EDS.

        Returns:
            dict: A dictionary with minimal data for client-side processing.
        """
        # Cargar datos solo para este código SICOM si aún no están cargados
        if self.df is None or len(self.df) == 0 or self.df['SICOM'].iloc[0] != sicom_code:
            self.load_data(sicom_code)

        if self.df is None or self.df.empty:
            return {}

        # Get EDS details
        eds_details = self.get_eds_details(sicom_code)

        # Get competitors data in a simplified format for client-side processing
        competitors_data = []
        competitors = self.df[self.df['SICOM'] == sicom_code].copy()

        for _, comp in competitors.iterrows():
            competitors_data.append({
                'sicom': comp['COMPETIDOR'],
                'nombre': comp['Nom_Com'],
                'bandera': comp['BANDERA_COM'],
                'distancia': comp['DISTANCIA']
            })

        return {
            'eds': eds_details,
            'competitors': competitors_data
        }
