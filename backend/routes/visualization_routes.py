from flask import Blueprint, request, jsonify, send_file
import logging
import os
import sys
from io import BytesIO
import base64

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from utils.dataset_merger import DatasetMerger
from visualizations.crime_visualizer import CrimeVisualizer

logger = logging.getLogger(__name__)
visualization_bp = Blueprint('visualization', __name__)

@visualization_bp.route('/heatmap', methods=['GET'])
def get_heatmap():
    """Generate and return crime heatmap as base64 image"""
    try:
        logger.info("Generating crime heatmap...")
        
        # Load data
        merger = DatasetMerger(Config.DATASET_FOLDER)
        merger.merge_datasets()
        merger.preprocess_data()
        df = merger.merged_df
        
        # Generate heatmap
        visualizer = CrimeVisualizer(Config.VISUALIZATION_DIR)
        heatmap_base64 = visualizer.generate_heatmap(df)
        
        if heatmap_base64:
            return jsonify({
                'success': True,
                'image': heatmap_base64,
                'format': 'base64'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate heatmap'
            }), 500
            
    except Exception as e:
        logger.error(f"Error generating heatmap: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@visualization_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Return crime statistics as JSON"""
    try:
        logger.info("Generating crime statistics...")
        
        # Load data
        merger = DatasetMerger(Config.DATASET_FOLDER)
        merger.merge_datasets()
        merger.preprocess_data()
        df = merger.merged_df
        
        # Generate statistics
        visualizer = CrimeVisualizer(Config.VISUALIZATION_DIR)
        stats = visualizer.generate_statistics(df)
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating statistics: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@visualization_bp.route('/charts/hour', methods=['GET'])
def get_hour_chart():
    """Generate crime by hour chart"""
    try:
        logger.info("Generating hourly crime chart...")
        
        merger = DatasetMerger(Config.DATASET_FOLDER)
        merger.merge_datasets()
        merger.preprocess_data()
        df = merger.merged_df
        
        visualizer = CrimeVisualizer(Config.VISUALIZATION_DIR)
        chart_base64 = visualizer.generate_crime_by_hour(df)
        
        if chart_base64:
            return jsonify({
                'success': True,
                'image': chart_base64,
                'format': 'base64'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate chart'
            }), 500
            
    except Exception as e:
        logger.error(f"Error generating hour chart: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@visualization_bp.route('/charts/type', methods=['GET'])
def get_type_chart():
    """Generate crime by type chart"""
    try:
        logger.info("Generating crime type chart...")
        
        merger = DatasetMerger(Config.DATASET_FOLDER)
        merger.merge_datasets()
        merger.preprocess_data()
        df = merger.merged_df
        
        visualizer = CrimeVisualizer(Config.VISUALIZATION_DIR)
        chart_base64 = visualizer.generate_crime_by_type(df)
        
        if chart_base64:
            return jsonify({
                'success': True,
                'image': chart_base64,
                'format': 'base64'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate chart'
            }), 500
            
    except Exception as e:
        logger.error(f"Error generating type chart: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@visualization_bp.route('/charts/monthly', methods=['GET'])
def get_monthly_chart():
    """Generate monthly trend chart"""
    try:
        logger.info("Generating monthly trend chart...")
        
        merger = DatasetMerger(Config.DATASET_FOLDER)
        merger.merge_datasets()
        merger.preprocess_data()
        df = merger.merged_df
        
        visualizer = CrimeVisualizer(Config.VISUALIZATION_DIR)
        chart_base64 = visualizer.generate_monthly_trend(df)
        
        if chart_base64:
            return jsonify({
                'success': True,
                'image': chart_base64,
                'format': 'base64'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate chart'
            }), 500
            
    except Exception as e:
        logger.error(f"Error generating monthly chart: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@visualization_bp.route('/all', methods=['GET'])
def get_all_visualizations():
    """Generate all visualizations and statistics"""
    try:
        logger.info("Generating all visualizations...")
        
        # Load data
        merger = DatasetMerger(Config.DATASET_FOLDER)
        merger.merge_datasets()
        merger.preprocess_data()
        df = merger.merged_df
        
        # Generate all visualizations
        visualizer = CrimeVisualizer(Config.VISUALIZATION_DIR)
        visualizations = visualizer.generate_all_visualizations(df)
        
        return jsonify({
            'success': True,
            'visualizations': visualizations
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating all visualizations: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
