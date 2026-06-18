from flask import Blueprint, request, jsonify
import sys
import os
import logging
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.dataset_merger import DatasetMerger
from config import Config

logger = logging.getLogger(__name__)
hotspot_bp = Blueprint('hotspot', __name__)

@hotspot_bp.route('/data', methods=['GET'])
def get_hotspot_data():
    """Get crime hotspot data with filters"""
    try:
        # Get filter parameters
        crime_type = request.args.get('crime_type', None)
        start_hour = request.args.get('start_hour', type=int)
        end_hour = request.args.get('end_hour', type=int)
        
        # Load dataset
        Config.init_app()
        merger = DatasetMerger(Config.DATASET_FOLDER)
        df = merger.merge_datasets()
        df = merger.preprocess_data()
        
        # Apply filters
        if crime_type and crime_type != 'ALL':
            df = df[df['crime_type'] == crime_type]
        
        if start_hour is not None and end_hour is not None:
            df = df[(df['hour'] >= start_hour) & (df['hour'] <= end_hour)]
        
        # Calculate hotspot data by location
        location_stats = df.groupby('location').agg({
            'crime_id': 'count',
            'crime_type': lambda x: x.mode()[0] if len(x) > 0 else 'UNKNOWN',
            'hour': 'mean',
            'victim_age': 'mean'
        }).reset_index()
        
        location_stats.columns = ['location', 'crime_count', 'most_common_crime', 'avg_hour', 'avg_victim_age']
        
        # Calculate risk level (0-100)
        max_crimes = location_stats['crime_count'].max()
        location_stats['risk_level'] = (location_stats['crime_count'] / max_crimes * 100).round(0).astype(int)
        
        # Get top crime types for each location
        location_crimes = df.groupby(['location', 'crime_type']).size().reset_index(name='count')
        
        hotspots = []
        for _, row in location_stats.iterrows():
            location = row['location']
            
            # Get top 3 crimes for this location
            loc_crimes = location_crimes[location_crimes['location'] == location].nlargest(3, 'count')
            top_crimes = loc_crimes[['crime_type', 'count']].to_dict('records')
            
            hotspots.append({
                'location': location,
                'crime_count': int(row['crime_count']),
                'risk_level': int(row['risk_level']),
                'most_common_crime': row['most_common_crime'],
                'avg_hour': round(row['avg_hour'], 1),
                'avg_victim_age': round(row['avg_victim_age'], 1),
                'top_crimes': top_crimes
            })
        
        # Sort by crime count
        hotspots.sort(key=lambda x: x['crime_count'], reverse=True)
        
        response = {
            'success': True,
            'total_locations': len(hotspots),
            'total_crimes': int(df['crime_id'].count()),
            'hotspots': hotspots,
            'filters_applied': {
                'crime_type': crime_type or 'ALL',
                'time_range': f"{start_hour or 0}:00 - {end_hour or 23}:00" if start_hour is not None else 'All Day'
            }
        }
        
        logger.info(f"Generated hotspot data for {len(hotspots)} locations")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error generating hotspot data: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@hotspot_bp.route('/location/<location_name>', methods=['GET'])
def get_location_details(location_name):
    """Get detailed statistics for a specific location"""
    try:
        # Load dataset
        Config.init_app()
        merger = DatasetMerger(Config.DATASET_FOLDER)
        df = merger.merge_datasets()
        df = merger.preprocess_data()
        
        # Filter by location
        location_df = df[df['location'] == location_name]
        
        if len(location_df) == 0:
            return jsonify({
                'success': False,
                'message': f'No data found for location: {location_name}'
            }), 404
        
        # Crime type distribution
        crime_distribution = location_df['crime_type'].value_counts().head(10).to_dict()
        
        # Hourly distribution
        hourly_distribution = location_df['hour'].value_counts().sort_index().to_dict()
        
        # Monthly trend
        monthly_trend = location_df['month'].value_counts().sort_index().to_dict()
        
        # Weapon usage
        weapon_distribution = location_df['weapon_used'].value_counts().head(5).to_dict()
        
        # Most dangerous hours (top 3)
        dangerous_hours = location_df['hour'].value_counts().head(3).to_dict()
        
        # Safest hours (bottom 3)
        safest_hours = location_df['hour'].value_counts().tail(3).to_dict()
        
        response = {
            'success': True,
            'location': location_name,
            'total_crimes': len(location_df),
            'statistics': {
                'crime_distribution': crime_distribution,
                'hourly_distribution': hourly_distribution,
                'monthly_trend': monthly_trend,
                'weapon_distribution': weapon_distribution,
                'avg_victim_age': round(location_df['victim_age'].mean(), 1),
                'most_dangerous_hours': dangerous_hours,
                'safest_hours': safest_hours
            }
        }
        
        logger.info(f"Generated detailed stats for {location_name}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error getting location details: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
