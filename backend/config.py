import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'crime_prediction_db')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Model Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    CRIME_TYPE_MODEL_PATH = os.path.join(MODELS_DIR, 'crime_type_model.pkl')
    CRIMINAL_KNN_MODEL_PATH = os.path.join(MODELS_DIR, 'criminal_knn.pkl')
    SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')
    LABEL_ENCODERS_PATH = os.path.join(MODELS_DIR, 'label_encoders.pkl')
    
    # Dataset Configuration
    DATASET_FOLDER = os.path.join(BASE_DIR, '..', 'datasets')
    
    # Visualization Configuration
    VISUALIZATION_DIR = os.path.join(BASE_DIR, 'visualizations')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        os.makedirs(Config.MODELS_DIR, exist_ok=True)
        os.makedirs(Config.VISUALIZATION_DIR, exist_ok=True)
