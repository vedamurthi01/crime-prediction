import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import logging
from config import Config
from utils.dataset_merger import DatasetMerger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrimeTypeTrainer:
    """Train and evaluate multiple models for crime type prediction"""
    
    def __init__(self, dataset_folder):
        self.dataset_folder = dataset_folder
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.best_accuracy = 0
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.label_encoders = None
        
    def load_and_prepare_data(self):
        """Load and prepare data for training"""
        logger.info("Loading and merging datasets...")
        
        # Initialize dataset merger
        merger = DatasetMerger(self.dataset_folder)
        
        # Merge datasets
        merger.merge_datasets()
        
        # Preprocess data
        merger.preprocess_data()
        
        # Get feature matrix
        X, y, df = merger.get_feature_matrix(target_col='crime_type')
        
        logger.info(f"Data shape: X={X.shape}, y={y.shape}")
        
        # Store label encoders
        self.label_encoders = merger.label_encoders
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training set: {self.X_train.shape}")
        logger.info(f"Test set: {self.X_test.shape}")
        
        return merger
    
    def initialize_models(self):
        """Initialize all ML models"""
        self.models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
            'XGBoost': XGBClassifier(n_estimators=100, random_state=42, max_depth=6, 
                                    eval_metric='mlogloss', use_label_encoder=False),
            'SVM': SVC(kernel='rbf', random_state=42, probability=True),
            'Naive Bayes': GaussianNB()
        }
        
        logger.info(f"Initialized {len(self.models)} models")
    
    def train_all_models(self):
        """Train all models and compare performance"""
        results = {}
        
        logger.info("=" * 60)
        logger.info("TRAINING CRIME TYPE PREDICTION MODELS")
        logger.info("=" * 60)
        
        for model_name, model in self.models.items():
            logger.info(f"\nTraining {model_name}...")
            
            try:
                # Train model
                model.fit(self.X_train, self.y_train)
                
                # Make predictions
                y_pred = model.predict(self.X_test)
                
                # Calculate metrics
                accuracy = accuracy_score(self.y_test, y_pred)
                precision = precision_score(self.y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(self.y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(self.y_test, y_pred, average='weighted', zero_division=0)
                
                results[model_name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1,
                    'predictions': y_pred
                }
                
                logger.info(f"Accuracy: {accuracy:.4f}")
                logger.info(f"Precision: {precision:.4f}")
                logger.info(f"Recall: {recall:.4f}")
                logger.info(f"F1 Score: {f1:.4f}")
                
                # Update best model
                if accuracy > self.best_accuracy:
                    self.best_accuracy = accuracy
                    self.best_model = model
                    self.best_model_name = model_name
                    
            except Exception as e:
                logger.error(f"Error training {model_name}: {e}")
                continue
        
        logger.info("\n" + "=" * 60)
        logger.info(f"BEST MODEL: {self.best_model_name}")
        logger.info(f"BEST ACCURACY: {self.best_accuracy:.4f}")
        logger.info("=" * 60)
        
        return results
    
    def get_detailed_report(self, results):
        """Generate detailed classification report for best model"""
        if self.best_model_name and self.best_model_name in results:
            y_pred = results[self.best_model_name]['predictions']
            
            logger.info(f"\nDetailed Classification Report for {self.best_model_name}:")
            logger.info("\n" + classification_report(self.y_test, y_pred))
            
            # Confusion matrix
            cm = confusion_matrix(self.y_test, y_pred)
            logger.info(f"\nConfusion Matrix shape: {cm.shape}")
    
    def save_best_model(self, model_path, encoders_path):
        """Save the best model and encoders"""
        if self.best_model is None:
            raise ValueError("No model has been trained yet")
        
        # Save model
        joblib.dump(self.best_model, model_path)
        logger.info(f"Best model ({self.best_model_name}) saved to {model_path}")
        
        # Save label encoders
        joblib.dump(self.label_encoders, encoders_path)
        logger.info(f"Label encoders saved to {encoders_path}")
        
        # Save metadata
        metadata = {
            'model_name': self.best_model_name,
            'accuracy': self.best_accuracy,
            'feature_names': list(self.X_train.columns)
        }
        
        metadata_path = model_path.replace('.pkl', '_metadata.pkl')
        joblib.dump(metadata, metadata_path)
        logger.info(f"Model metadata saved to {metadata_path}")
        
        return {
            'model_name': self.best_model_name,
            'accuracy': self.best_accuracy,
            'model_path': model_path
        }

def main():
    """Main training function"""
    # Initialize configuration
    Config.init_app()
    
    # Initialize trainer
    trainer = CrimeTypeTrainer(Config.DATASET_FOLDER)
    
    # Load and prepare data
    merger = trainer.load_and_prepare_data()
    
    # Save encoders
    merger.save_encoders(Config.LABEL_ENCODERS_PATH, Config.SCALER_PATH)
    
    # Initialize and train models
    trainer.initialize_models()
    results = trainer.train_all_models()
    
    # Get detailed report
    trainer.get_detailed_report(results)
    
    # Save best model
    model_info = trainer.save_best_model(
        Config.CRIME_TYPE_MODEL_PATH,
        Config.LABEL_ENCODERS_PATH
    )
    
    logger.info("\n" + "=" * 60)
    logger.info("TRAINING COMPLETED SUCCESSFULLY")
    logger.info(f"Model: {model_info['model_name']}")
    logger.info(f"Accuracy: {model_info['accuracy']:.4f}")
    logger.info(f"Saved to: {model_info['model_path']}")
    logger.info("=" * 60)
    
    return model_info

if __name__ == "__main__":
    main()
