from flask import Blueprint, request, jsonify
import sys
import os
import logging
import pandas as pd
import numpy as np
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.dataset_merger import DatasetMerger
from config import Config

logger = logging.getLogger(__name__)
risk_bp = Blueprint('risk', __name__)

# Global variables for model
crime_type_model = None
label_encoders = None

def load_model():
    """Load crime type prediction model"""
    global crime_type_model, label_encoders
    
    try:
        if crime_type_model is None:
            Config.init_app()
            crime_type_model = joblib.load(Config.CRIME_TYPE_MODEL_PATH)
            label_encoders = joblib.load(Config.LABEL_ENCODERS_PATH)
            logger.info("Risk assessment model loaded")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@risk_bp.route('/assess', methods=['POST'])
def assess_risk():
    """Assess crime risk for given location and time"""
    try:
        # Load model
        if not load_model():
            return jsonify({
                'success': False,
                'message': 'Model not trained. Please train the model first.'
            }), 400
        
        # Get input data
        data = request.get_json()
        location = data.get('location', 'UNKNOWN')
        time = data.get('time', 12)  # hour
        date = data.get('date', None)  # optional
        
        # Load historical data for this location
        Config.init_app()
        merger = DatasetMerger(Config.DATASET_FOLDER)
        df = merger.merge_datasets()
        df = merger.preprocess_data()
        
        # Filter by location
        location_df = df[df['location'] == location]
        
        if len(location_df) == 0:
            return jsonify({
                'success': False,
                'message': f'No historical data for location: {location}'
            }), 404
        
        # Calculate risk score based on historical data
        total_crimes = len(location_df)
        crimes_at_hour = len(location_df[location_df['hour'] == time])
        
        # Risk factors
        hour_risk = (crimes_at_hour / total_crimes * 100) if total_crimes > 0 else 0
        
        # Overall location risk
        all_locations = df.groupby('location').size()
        max_location_crimes = all_locations.max()
        location_risk = (total_crimes / max_location_crimes * 100)
        
        # Combined risk score (weighted average)
        risk_score = int((hour_risk * 0.6 + location_risk * 0.4))
        risk_score = min(max(risk_score, 20), 95)  # Clamp between 20-95
        
        # Determine risk level
        if risk_score >= 75:
            risk_level = 'High'
            risk_color = '#ef4444'
        elif risk_score >= 50:
            risk_level = 'Medium'
            risk_color = '#f59e0b'
        else:
            risk_level = 'Low'
            risk_color = '#10b981'
        
        # Predict most likely crime types
        try:
            location_encoded = label_encoders['location'].transform([location])[0]
        except:
            location_encoded = 0
        
        # Use median values for unknown features
        weapon_encoded = 0
        victim_age = int(df['victim_age'].median())
        suspect_age = int(df['suspect_age'].median())
        month = int(pd.Timestamp.now().month)
        weekday = int(pd.Timestamp.now().dayofweek)
        district_encoded = location_encoded
        
        # Create feature vector
        features = np.array([[
            location_encoded,
            time,
            weapon_encoded,
            victim_age,
            suspect_age,
            month,
            weekday,
            district_encoded
        ]])
        
        # Get predictions
        probabilities = crime_type_model.predict_proba(features)[0]
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        
        # Scale probabilities
        top_3_probs = probabilities[top_3_indices]
        prob_sum = np.sum(top_3_probs)
        
        likely_crimes = []
        if prob_sum > 0:
            normalized_probs = top_3_probs / prob_sum
            scaled_probs = [
                70 + (normalized_probs[0] * 25),
                70 + (normalized_probs[1] * 20),
                70 + (normalized_probs[2] * 15)
            ]
            
            for i, idx in enumerate(top_3_indices):
                crime_type = label_encoders['crime_type'].inverse_transform([idx])[0]
                likely_crimes.append({
                    'crime_type': crime_type,
                    'probability': round(scaled_probs[i], 1)
                })
        
        # Generate safety recommendations
        safety_tips = generate_safety_tips(risk_level, likely_crimes[0]['crime_type'] if likely_crimes else 'UNKNOWN')
        
        # Find safest and most dangerous hours
        hourly_crimes = location_df.groupby('hour').size().sort_values()
        safest_hours = hourly_crimes.head(3).index.tolist()
        dangerous_hours = hourly_crimes.tail(3).index.tolist()
        
        response = {
            'success': True,
            'risk_assessment': {
                'location': location,
                'time': time,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_color': risk_color,
                'total_historical_crimes': total_crimes,
                'crimes_at_this_hour': crimes_at_hour
            },
            'likely_crimes': likely_crimes,
            'safety_tips': safety_tips,
            'time_recommendations': {
                'safest_hours': [f"{h}:00" for h in safest_hours],
                'most_dangerous_hours': [f"{h}:00" for h in dangerous_hours]
            }
        }
        
        logger.info(f"Risk assessment for {location} at {time}:00 - Score: {risk_score}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error assessing risk: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

def generate_safety_tips(risk_level, crime_type):
    """Generate contextual safety recommendations"""
    tips = []
    
    # General tips based on risk level
    if risk_level == 'High':
        tips.append("⚠️ High risk area - Consider avoiding this location/time")
        tips.append("🚨 If you must travel, go with a companion")
        tips.append("📱 Keep emergency contacts on speed dial")
    elif risk_level == 'Medium':
        tips.append("⚡ Moderate risk - Stay alert and aware")
        tips.append("👥 Travel in groups when possible")
    else:
        tips.append("✓ Low risk area - Generally safe")
        tips.append("👁️ Still maintain basic awareness")
    
    # Crime-specific tips
    crime_tips = {
        'THEFT': "💰 Keep valuables hidden and secured",
        'BURGLARY': "🏠 Ensure doors and windows are locked",
        'ASSAULT': "🚶 Stay in well-lit, populated areas",
        'ROBBERY': "💳 Don't display expensive items or cash",
        'HOMICIDE': "🚓 Report any suspicious activity immediately",
        'KIDNAPPING': "👶 Keep children close and supervised",
        'FRAUD': "🔒 Protect personal and financial information",
        'VEHICLE THEFT': "🚗 Park in secure, visible locations",
        'DOMESTIC VIOLENCE': "📞 Contact support services if needed",
        'DRUG OFFENSE': "🚫 Avoid suspicious gatherings or areas"
    }
    
    if crime_type in crime_tips:
        tips.append(crime_tips[crime_type])
    
    # Always add emergency tip
    tips.append("🚨 Emergency: Dial 100 (India Police)")
    
    return tips

@risk_bp.route('/trends/<location>', methods=['GET'])
def get_risk_trends(location):
    """Get risk trends over time for a location"""
    try:
        Config.init_app()
        merger = DatasetMerger(Config.DATASET_FOLDER)
        df = merger.merge_datasets()
        df = merger.preprocess_data()
        
        location_df = df[df['location'] == location]
        
        if len(location_df) == 0:
            return jsonify({
                'success': False,
                'message': f'No data for location: {location}'
            }), 404
        
        # Monthly trend
        monthly = location_df.groupby('month').size().to_dict()
        
        # Hourly trend
        hourly = location_df.groupby('hour').size().to_dict()
        
        # Weekday trend
        weekday = location_df.groupby('weekday').size().to_dict()
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_labeled = {weekday_names[k]: v for k, v in weekday.items() if k < 7}
        
        response = {
            'success': True,
            'location': location,
            'trends': {
                'monthly': monthly,
                'hourly': hourly,
                'weekday': weekday_labeled
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error getting risk trends: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
