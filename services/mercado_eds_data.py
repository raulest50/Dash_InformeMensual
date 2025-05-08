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
        Initialize the data loader and load the data.
        """
        self.df = None
        self.load_data()
        
    def load_data(self):
        """
        Load the data from the CSV file.
        """
        try:
            # Load the data from the CSV file
            file_path = os.path.join('data', 'mercado_eds', 'info_mercado.csv')
            self.df = pd.read_csv(file_path, sep=';', encoding='utf-8')
            
            # Convert coordinates to float
            self.df['Coord_X'] = pd.to_numeric(self.df['Coord_X'], errors='coerce')
            self.df['Coord_Y'] = pd.to_numeric(self.df['Coord_Y'], errors='coerce')
            self.df['Coord_X_Com'] = pd.to_numeric(self.df['Coord_X_Com'], errors='coerce')
            self.df['Coord_Y_Com'] = pd.to_numeric(self.df['Coord_Y_Com'], errors='coerce')
            
            # Get unique SICOM codes for dropdown
            self.sicom_codes = sorted(self.df['SICOM'].unique())
            
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
            sicom_code (str): The SICOM code of the EDS.
            
        Returns:
            DataFrame: A DataFrame with the competitors.
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        # Filter for the specific EDS's competitors
        competitors = self.df[self.df['SICOM'] == sicom_code].copy()
        
        # Select only the competitor columns
        competitor_cols = ['COMPETIDOR', 'Nom_Com', 'BANDERA_COM', 'Coord_X_Com', 'Coord_Y_Com', 'DISTANCIA']
        competitors = competitors[competitor_cols].copy()
        
        # Rename columns for clarity
        competitors.columns = ['SICOM', 'Nombre Comercial', 'Bandera', 'Longitud', 'Latitud', 'Distancia']
        
        return competitors
    
    def get_competitor_brands_distribution(self, sicom_code):
        """
        Get the distribution of competitor brands for a specific EDS.
        
        Args:
            sicom_code (str): The SICOM code of the EDS.
            
        Returns:
            DataFrame: A DataFrame with the brand distribution.
        """
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
        if self.df is None or self.df.empty:
            return {'eds': {}, 'competitors': []}
        
        # Get the EDS data
        eds_data = self.df[self.df['SICOM'] == sicom_code].iloc[0] if not self.df[self.df['SICOM'] == sicom_code].empty else None
        
        if eds_data is None:
            return {'eds': {}, 'competitors': []}
        
        # Get the competitors data
        competitors = self.df[self.df['SICOM'] == sicom_code].copy()
        
        # Prepare the EDS data for the map
        eds_map_data = {
            'sicom': sicom_code,
            'nombre': eds_data['NOMBRE COMERCIAL'],
            'bandera': eds_data['BANDERA'],
            'coords': [eds_data['Coord_X'], eds_data['Coord_Y']]
        }
        
        # Prepare the competitors data for the map
        competitors_map_data = []
        for _, comp in competitors.iterrows():
            competitors_map_data.append({
                'sicom': comp['COMPETIDOR'],
                'nombre': comp['Nom_Com'],
                'bandera': comp['BANDERA_COM'],
                'coords': [comp['Coord_X_Com'], comp['Coord_Y_Com']],
                'distancia': comp['DISTANCIA']
            })
        
        return {
            'eds': eds_map_data,
            'competitors': competitors_map_data
        }