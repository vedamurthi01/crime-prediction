from flask import Blueprint, request, jsonify
import logging
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from models.train_crime_type import CrimeTypeTrainer
from models.train_criminal_knn import CriminalKNNTrainer

logger = logging.getLogger(__name__)
train_bp = Blueprint('train', __name__)

@train_bp.route('/crime-type', methods=['POST'])
def train_crime_type_model():
    """Train crime type prediction models"""
    try:
        logger.info("Starting crime type model training...")
        
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
        
        # Save best model
        model_info = trainer.save_best_model(
            Config.CRIME_TYPE_MODEL_PATH,
            Config.LABEL_ENCODERS_PATH
        )
        
        # Prepare response
        response = {
            'success': True,
            'message': 'Crime type models trained successfully',
            'best_model': model_info['model_name'],
            'accuracy': float(model_info['accuracy']),
            'model_path': model_info['model_path'],
            'all_models': {}
        }
        
        # Add all model results
        for model_name, result in results.items():
            response['all_models'][model_name] = {
                'accuracy': float(result['accuracy']),
                'precision': float(result['precision']),
                'recall': float(result['recall']),
                'f1_score': float(result['f1_score'])
            }
        
        logger.info(f"Training completed. Best model: {model_info['model_name']}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error training crime type model: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@train_bp.route('/criminal-knn', methods=['POST'])
def train_criminal_knn_model():
    """Train KNN model for criminal identification"""
    try:
        logger.info("Starting KNN model training...")
        
        # Get parameters from request
        data = request.get_json() or {}
        n_neighbors = data.get('n_neighbors', 5)
        
        # Initialize configuration
        Config.init_app()
        
        # Initialize trainer
        trainer = CriminalKNNTrainer(Config.DATASET_FOLDER)
        
        # Train model
        accuracy = trainer.train_knn_model(n_neighbors=n_neighbors)
        
        # Save model
        paths = trainer.save_model(
            Config.CRIMINAL_KNN_MODEL_PATH,
            Config.SCALER_PATH.replace('.pkl', '_knn.pkl'),
            Config.LABEL_ENCODERS_PATH.replace('.pkl', '_knn.pkl')
        )
        
        response = {
            'success': True,
            'message': 'KNN model trained successfully',
            'accuracy': float(accuracy),
            'n_neighbors': n_neighbors,
            'model_path': paths['model_path'],
            'suspect_count': len(trainer.suspect_database) if trainer.suspect_database is not None else 0
        }
        
        logger.info(f"KNN training completed. Accuracy: {accuracy:.4f}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error training KNN model: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@train_bp.route('/status', methods=['GET'])
def training_status():
    """Check training status and model availability"""
    try:
        Config.init_app()
        
        status = {
            'crime_type_model': os.path.exists(Config.CRIME_TYPE_MODEL_PATH),
            'criminal_knn_model': os.path.exists(Config.CRIMINAL_KNN_MODEL_PATH),
            'label_encoders': os.path.exists(Config.LABEL_ENCODERS_PATH),
            'scaler': os.path.exists(Config.SCALER_PATH)
        }
        
        return jsonify({
            'success': True,
            'models': status,
            'all_trained': all(status.values())
        }), 200
        
    except Exception as e:
        logger.error(f"Error checking training status: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
