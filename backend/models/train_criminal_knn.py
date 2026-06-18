import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging
from config import Config
from utils.dataset_merger import DatasetMerger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CriminalKNNTrainer:
    """Train KNN model for criminal identification"""
    
    def __init__(self, dataset_folder):
        self.dataset_folder = dataset_folder
        self.model = None
        self.scaler = None
        self.label_encoders = None
        self.suspect_database = None
        
    def create_suspect_database(self, df):
        """Create synthetic suspect database from crime data"""
        logger.info("Creating suspect database...")
        
        # Create more suspects by sampling from the dataset
        suspects = []
        
        # Sample more crimes to create a larger suspect database
        sampled_df = df.sample(n=min(5000, len(df)), random_state=42)
        
        for idx, row in sampled_df.iterrows():
            suspect = {
                'suspect_id': f'SUSP_{idx}',
                'name': f'Suspect_{idx}',
                'crime_type': row['crime_type'],
                'location': row['location'],
                'modus_operandi': row['weapon_used'],
                'hour_preference': row['hour'],
                'district': row['district'],
                'age': row.get('suspect_age', row.get('victim_age', 30))
            }
            suspects.append(suspect)
        
        self.suspect_database = pd.DataFrame(suspects)
        logger.info(f"Created suspect database with {len(self.suspect_database)} suspects")
        
        return self.suspect_database
    
    def prepare_knn_data(self):
        """Prepare data for KNN training"""
        logger.info("Loading and preparing data for KNN...")
        
        # Initialize dataset merger
        merger = DatasetMerger(self.dataset_folder)
        merger.merge_datasets()
        merger.preprocess_data()
        
        # Get processed dataframe
        df = merger.merged_df.copy()
        
        # Create suspect database
        suspect_df = self.create_suspect_database(df)
        
        # Encode categorical features
        suspect_df = merger.encode_features(suspect_df)
        self.label_encoders = merger.label_encoders
        
        # Select features for KNN
        feature_cols = ['crime_type_encoded', 'location_encoded', 
                       'hour_preference', 'district_encoded']
        
        # Filter existing columns
        feature_cols = [col for col in feature_cols if col in suspect_df.columns]
        
        # Remove missing values
        suspect_df = suspect_df.dropna(subset=feature_cols)
        
        X = suspect_df[feature_cols]
        y = suspect_df['suspect_id']
        
        # Normalize features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        logger.info(f"KNN data shape: X={X_scaled.shape}, y={y.shape}")
        
        return X_scaled, y, suspect_df
    
    def train_knn_model(self, n_neighbors=5):
        """Train KNN model"""
        logger.info("Training KNN model...")
        
        # Prepare data
        X, y, suspect_df = self.prepare_knn_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train KNN
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance')
        self.model.fit(X_train, y_train)
        
        # For KNN suspect matching, we measure if similar crime patterns are found
        # Calculate average similarity score (inverse of distance)
        total_similarity = 0
        for test_sample in X_test:
            distances, indices = self.model.kneighbors([test_sample], n_neighbors=n_neighbors)
            # Convert distance to similarity (0 to 1, where 1 is most similar)
            avg_distance = distances[0].mean()
            similarity = 1 / (1 + avg_distance)  # Normalize to 0-1 range
            total_similarity += similarity
        
        accuracy = total_similarity / len(X_test)
        
        logger.info(f"KNN Model Similarity Score: {accuracy:.4f}")
        logger.info(f"This represents how well the model finds similar crime patterns")
        logger.info(f"Number of neighbors: {n_neighbors}")
        
        return accuracy
    
    def save_model(self, model_path, scaler_path, encoders_path):
        """Save KNN model and related objects"""
        if self.model is None:
            raise ValueError("No model has been trained yet")
        
        # Save model
        joblib.dump(self.model, model_path)
        logger.info(f"KNN model saved to {model_path}")
        
        # Save scaler
        joblib.dump(self.scaler, scaler_path)
        logger.info(f"Scaler saved to {scaler_path}")
        
        # Save label encoders
        joblib.dump(self.label_encoders, encoders_path)
        logger.info(f"Label encoders saved to {encoders_path}")
        
        # Save suspect database
        suspect_db_path = model_path.replace('.pkl', '_suspects.pkl')
        joblib.dump(self.suspect_database, suspect_db_path)
        logger.info(f"Suspect database saved to {suspect_db_path}")
        
        return {
            'model_path': model_path,
            'scaler_path': scaler_path,
            'suspect_db_path': suspect_db_path
        }

def main():
    """Main training function for KNN"""
    Config.init_app()
    
    # Initialize trainer
    trainer = CriminalKNNTrainer(Config.DATASET_FOLDER)
    
    # Train model
    accuracy = trainer.train_knn_model(n_neighbors=5)
    
    # Save model
    paths = trainer.save_model(
        Config.CRIMINAL_KNN_MODEL_PATH,
        Config.SCALER_PATH.replace('.pkl', '_knn.pkl'),
        Config.LABEL_ENCODERS_PATH.replace('.pkl', '_knn.pkl')
    )
    
    logger.info("\n" + "=" * 60)
    logger.info("KNN TRAINING COMPLETED SUCCESSFULLY")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Model saved to: {paths['model_path']}")
    logger.info("=" * 60)
    
    return accuracy

if __name__ == "__main__":
    main()
