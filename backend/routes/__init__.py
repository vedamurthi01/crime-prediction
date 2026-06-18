"""Routes package"""
from .train_routes import train_bp
from .predict_routes import predict_bp
from .visualization_routes import visualization_bp

__all__ = ['train_bp', 'predict_bp', 'visualization_bp']
