import pandas as pd
import numpy as np
import os
import logging
from sklearn.preprocessing import LabelEncoder, StandardScaler
from datetime import datetime
import joblib

logger = logging.getLogger(__name__)

class DatasetMerger:
    """Merge and preprocess crime datasets from multiple sources"""
    
    def __init__(self, dataset_folder):
        self.dataset_folder = dataset_folder
        self.merged_df = None
        self.label_encoders = {}
        self.scaler = None
        
    def load_india_dataset(self):
        """Load and preprocess Indian crime dataset"""
        try:
            file_path = os.path.join(self.dataset_folder, 'crime_dataset_india.csv')
            if not os.path.exists(file_path):
                logger.warning(f"India dataset not found: {file_path}")
                return None
            
            df = pd.read_csv(file_path)
            logger.info(f"Loaded India dataset: {len(df)} records")
            
            # Standardize column names
            df_processed = pd.DataFrame()
            df_processed['crime_id'] = df['Report Number'].astype(str)
            df_processed['crime_type'] = df['Crime Description']
            df_processed['location'] = df['City']
            df_processed['date'] = pd.to_datetime(df['Date of Occurrence'], format='%d-%m-%Y %H:%M', errors='coerce')
            df_processed['time'] = df['Time of Occurrence']
            df_processed['victim_age'] = pd.to_numeric(df['Victim Age'], errors='coerce')
            df_processed['victim_gender'] = df['Victim Gender']
            df_processed['weapon_used'] = df['Weapon Used']
            df_processed['district'] = df['City']  # Using city as district
            df_processed['latitude'] = np.nan
            df_processed['longitude'] = np.nan
            df_processed['suspect_age'] = np.nan
            
            return df_processed
            
        except Exception as e:
            logger.error(f"Error loading India dataset: {e}")
            return None
    
    def load_us_dataset(self):
        """Load and preprocess US crime dataset (sample due to large size)"""
        try:
            file_path = os.path.join(self.dataset_folder, 'Crime_Data_from_2020_to_Present.csv')
            if not os.path.exists(file_path):
                logger.warning(f"US dataset not found: {file_path}")
                return None
            
            # Read only a sample due to large file size
            df = pd.read_csv(file_path, nrows=50000)  # Limit rows for performance
            logger.info(f"Loaded US dataset sample: {len(df)} records")
            
            # Standardize column names (adjust based on actual columns)
            df_processed = pd.DataFrame()
            
            # Map columns appropriately
            if 'DR_NO' in df.columns:
                df_processed['crime_id'] = df['DR_NO'].astype(str)
            if 'Crm Cd Desc' in df.columns:
                df_processed['crime_type'] = df['Crm Cd Desc']
            if 'AREA NAME' in df.columns:
                df_processed['location'] = df['AREA NAME']
                df_processed['district'] = df['AREA NAME']
            if 'DATE OCC' in df.columns:
                df_processed['date'] = pd.to_datetime(df['DATE OCC'], errors='coerce')
            if 'TIME OCC' in df.columns:
                df_processed['time'] = df['TIME OCC'].astype(str)
            if 'Vict Age' in df.columns:
                df_processed['victim_age'] = pd.to_numeric(df['Vict Age'], errors='coerce')
            if 'Vict Sex' in df.columns:
                df_processed['victim_gender'] = df['Vict Sex']
            if 'Weapon Desc' in df.columns:
                df_processed['weapon_used'] = df['Weapon Desc']
            if 'LAT' in df.columns:
                df_processed['latitude'] = pd.to_numeric(df['LAT'], errors='coerce')
            if 'LON' in df.columns:
                df_processed['longitude'] = pd.to_numeric(df['LON'], errors='coerce')
            
            df_processed['suspect_age'] = np.nan
            
            return df_processed
            
        except Exception as e:
            logger.error(f"Error loading US dataset: {e}")
            return None
    
    def merge_datasets(self):
        """Load only India dataset"""
        datasets = []
        
        # Load India dataset only
        india_df = self.load_india_dataset()
        if india_df is not None:
            datasets.append(india_df)
        else:
            raise ValueError("India dataset could not be loaded")
        
        # Merge all datasets (only India in this case)
        self.merged_df = pd.concat(datasets, ignore_index=True)
        logger.info(f"Loaded India dataset: Total {len(self.merged_df)} records")
        
        return self.merged_df
    
    def preprocess_data(self):
        """Preprocess the merged dataset"""
        if self.merged_df is None:
            raise ValueError("No data to preprocess. Call merge_datasets() first")
        
        df = self.merged_df.copy()
        
        # Handle missing values
        df['crime_type'] = df['crime_type'].fillna('UNKNOWN')
        df['location'] = df['location'].fillna('UNKNOWN')
        df['district'] = df['district'].fillna('UNKNOWN')
        df['weapon_used'] = df['weapon_used'].fillna('UNKNOWN')
        df['victim_gender'] = df['victim_gender'].fillna('U')
        
        # Fill numeric missing values with median
        df['victim_age'] = df['victim_age'].fillna(df['victim_age'].median())
        df['suspect_age'] = df['suspect_age'].fillna(df['victim_age'])  # Use victim age as proxy
        
        # Extract datetime features
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['weekday'] = df['date'].dt.dayofweek
        
        # Extract hour from time
        df['hour'] = df['time'].apply(self._extract_hour)
        
        # Clean crime types
        df['crime_type'] = df['crime_type'].str.upper().str.strip()
        
        # Create crime categories
        df['crime_category'] = df['crime_type'].apply(self._categorize_crime)
        
        self.merged_df = df
        logger.info("Data preprocessing completed")
        
        return df
    
    def _extract_hour(self, time_str):
        """Extract hour from time string"""
        try:
            if pd.isna(time_str):
                return 12  # Default to noon
            time_str = str(time_str).strip()
            
            # Handle datetime format like "01-01-2020 01:11"
            if ' ' in time_str:
                # Split by space to get time part
                time_part = time_str.split(' ')[-1]  # Get the last part (time)
                if ':' in time_part:
                    return int(time_part.split(':')[0])
            # Handle time format like "14:30"
            elif ':' in time_str:
                return int(time_str.split(':')[0])
            # Handle numeric format
            elif len(time_str) >= 2:
                return int(time_str[:2])
            else:
                return 12
        except:
            return 12
    
    def _categorize_crime(self, crime_type):
        """Categorize crimes into broader categories"""
        crime_type = str(crime_type).upper()
        
        violent_crimes = ['HOMICIDE', 'MURDER', 'ASSAULT', 'ROBBERY', 'RAPE', 'KIDNAPPING']
        property_crimes = ['BURGLARY', 'THEFT', 'LARCENY', 'VEHICLE THEFT', 'VANDALISM']
        white_collar = ['FRAUD', 'EMBEZZLEMENT', 'IDENTITY THEFT', 'FORGERY']
        
        for violent in violent_crimes:
            if violent in crime_type:
                return 'VIOLENT'
        
        for prop in property_crimes:
            if prop in crime_type:
                return 'PROPERTY'
        
        for wc in white_collar:
            if wc in crime_type:
                return 'WHITE_COLLAR'
        
        return 'OTHER'
    
    def encode_features(self, df=None):
        """Encode categorical features"""
        if df is None:
            df = self.merged_df.copy()
        
        # Categorical columns to encode
        categorical_cols = ['crime_type', 'location', 'district', 'weapon_used', 
                           'victim_gender', 'crime_category']
        
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        logger.info("Feature encoding completed")
        return df
    
    def normalize_features(self, df, features_to_scale):
        """Normalize numerical features"""
        self.scaler = StandardScaler()
        df[features_to_scale] = self.scaler.fit_transform(df[features_to_scale])
        logger.info("Feature normalization completed")
        return df
    
    def save_preprocessed_data(self, output_path):
        """Save preprocessed data to CSV"""
        if self.merged_df is not None:
            self.merged_df.to_csv(output_path, index=False)
            logger.info(f"Saved preprocessed data to {output_path}")
    
    def save_encoders(self, encoders_path, scaler_path):
        """Save label encoders and scaler"""
        joblib.dump(self.label_encoders, encoders_path)
        if self.scaler:
            joblib.dump(self.scaler, scaler_path)
        logger.info("Saved encoders and scaler")
    
    def get_feature_matrix(self, target_col='crime_type'):
        """Get feature matrix and target for ML models"""
        df = self.merged_df.copy()
        
        # Select features
        feature_cols = ['location_encoded', 'hour', 'weapon_used_encoded', 
                       'victim_age', 'suspect_age', 'month', 'weekday', 
                       'district_encoded']
        
        # Remove rows with missing values first
        df = df.dropna(subset=['location', 'hour', 'weapon_used', 
                               'victim_age', 'suspect_age', 'month', 
                               'weekday', 'district', target_col])
        
        # Filter out rare crime types (less than 2 samples) to avoid stratify error
        crime_counts = df[target_col].value_counts()
        valid_crimes = crime_counts[crime_counts >= 2].index
        df = df[df[target_col].isin(valid_crimes)]
        
        logger.info(f"Filtered to {len(valid_crimes)} crime types with at least 2 samples")
        
        # Now encode features
        df = self.encode_features(df)
        
        # Filter only existing columns
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        X = df[feature_cols]
        y = df[target_col + '_encoded']
        
        return X, y, df
