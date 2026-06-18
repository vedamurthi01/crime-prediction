from flask import Flask, jsonify
from flask_cors import CORS
import logging
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from database.mongodb import get_db
from routes import train_bp, predict_bp, visualization_bp
from routes.hotspot_routes import hotspot_bp
from routes.risk_routes import risk_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Initialize directories
    Config.init_app()
    
    # Initialize MongoDB
    db = get_db(Config.MONGODB_URI, Config.MONGODB_DB)
    connected = db.connect()
    
    if connected:
        logger.info("✓ MongoDB connected successfully")
    else:
        logger.warning("✗ MongoDB connection failed - continuing without database")
    
    # Register blueprints
    app.register_blueprint(train_bp, url_prefix='/api/train')
    app.register_blueprint(predict_bp, url_prefix='/api/predict')
    app.register_blueprint(visualization_bp, url_prefix='/api/visualization')
    app.register_blueprint(hotspot_bp, url_prefix='/api/hotspot')
    app.register_blueprint(risk_bp, url_prefix='/api/risk')
    
    logger.info("✓ API routes registered")
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Crime Prediction & Criminal Identification System',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'training': {
                    'crime_type': '/api/train/crime-type',
                    'criminal_knn': '/api/train/criminal-knn',
                    'status': '/api/train/status'
                },
                'prediction': {
                    'crime_type': '/api/predict/crime-type',
                    'criminal': '/api/predict/criminal',
                    'status': '/api/predict/models/status'
                },
                'visualization': {
                    'heatmap': '/api/visualization/heatmap',
                    'statistics': '/api/visualization/statistics',
                    'hour_chart': '/api/visualization/charts/hour',
                    'type_chart': '/api/visualization/charts/type',
                    'monthly_chart': '/api/visualization/charts/monthly',
                    'all': '/api/visualization/all'
                },
                'hotspot': {
                    'data': '/api/hotspot/data',
                    'location_details': '/api/hotspot/location/<location_name>'
                },
                'risk': {
                    'assess': '/api/risk/assess',
                    'trends': '/api/risk/trends/<location>'
                }
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'database': db is not None and db.client is not None
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    return app

def main():
    """Run the Flask application"""
    app = create_app()
    
    logger.info("=" * 60)
    logger.info("Crime Prediction & Criminal Identification System")
    logger.info("=" * 60)
    logger.info(f"Server: http://{Config.HOST}:{Config.PORT}")
    logger.info(f"Environment: {'Development' if Config.DEBUG else 'Production'}")
    logger.info("=" * 60)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

if __name__ == '__main__':
    main()
