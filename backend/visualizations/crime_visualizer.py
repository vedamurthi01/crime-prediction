import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64
import os
import logging

logger = logging.getLogger(__name__)

class CrimeVisualizer:
    """Generate visualizations for crime data"""
    
    def __init__(self, output_dir='visualizations'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style('whitegrid')
        plt.rcParams['figure.figsize'] = (12, 8)
    
    def generate_heatmap(self, df, save_path=None):
        """Generate crime heatmap by location and time"""
        try:
            # Create hour x location heatmap
            if 'hour' not in df.columns or 'location' not in df.columns:
                logger.warning("Required columns not found for heatmap")
                return None
            
            # Get top 20 locations
            top_locations = df['location'].value_counts().head(20).index
            df_filtered = df[df['location'].isin(top_locations)]
            
            # Create pivot table
            heatmap_data = pd.crosstab(
                df_filtered['location'],
                df_filtered['hour']
            )
            
            # Create heatmap
            plt.figure(figsize=(14, 10))
            sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False, fmt='d', 
                       cbar_kws={'label': 'Number of Crimes'})
            plt.title('Crime Heatmap: Location vs Hour of Day', fontsize=16, fontweight='bold')
            plt.xlabel('Hour of Day', fontsize=12)
            plt.ylabel('Location', fontsize=12)
            plt.tight_layout()
            
            # Save or return base64
            if save_path:
                plt.savefig(save_path, dpi=150, bbox_inches='tight')
                logger.info(f"Heatmap saved to {save_path}")
                plt.close()
                return save_path
            else:
                # Convert to base64
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode()
                plt.close()
                return image_base64
                
        except Exception as e:
            logger.error(f"Error generating heatmap: {e}")
            plt.close()
            return None
    
    def generate_crime_by_hour(self, df, save_path=None):
        """Generate bar chart of crimes by hour"""
        try:
            plt.figure(figsize=(12, 6))
            
            if 'hour' in df.columns:
                hour_counts = df['hour'].value_counts().sort_index()
                
                plt.bar(hour_counts.index, hour_counts.values, color='steelblue', edgecolor='black')
                plt.title('Crime Distribution by Hour of Day', fontsize=16, fontweight='bold')
                plt.xlabel('Hour', fontsize=12)
                plt.ylabel('Number of Crimes', fontsize=12)
                plt.xticks(range(0, 24))
                plt.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                
                if save_path:
                    plt.savefig(save_path, dpi=150, bbox_inches='tight')
                    plt.close()
                    return save_path
                else:
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.read()).decode()
                    plt.close()
                    return image_base64
                    
        except Exception as e:
            logger.error(f"Error generating hour chart: {e}")
            plt.close()
            return None
    
    def generate_crime_by_type(self, df, save_path=None, top_n=10):
        """Generate pie chart of crimes by type"""
        try:
            plt.figure(figsize=(12, 8))
            
            if 'crime_type' in df.columns:
                type_counts = df['crime_type'].value_counts().head(top_n)
                
                colors = sns.color_palette('Set3', len(type_counts))
                plt.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
                       colors=colors, startangle=90)
                plt.title(f'Top {top_n} Crime Types Distribution', fontsize=16, fontweight='bold')
                plt.tight_layout()
                
                if save_path:
                    plt.savefig(save_path, dpi=150, bbox_inches='tight')
                    plt.close()
                    return save_path
                else:
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.read()).decode()
                    plt.close()
                    return image_base64
                    
        except Exception as e:
            logger.error(f"Error generating type chart: {e}")
            plt.close()
            return None
    
    def generate_monthly_trend(self, df, save_path=None):
        """Generate line chart of monthly crime trends"""
        try:
            plt.figure(figsize=(14, 6))
            
            if 'month' in df.columns:
                month_counts = df['month'].value_counts().sort_index()
                
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                
                plt.plot(month_counts.index, month_counts.values, marker='o', 
                        linewidth=2, markersize=8, color='darkred')
                plt.title('Monthly Crime Trend', fontsize=16, fontweight='bold')
                plt.xlabel('Month', fontsize=12)
                plt.ylabel('Number of Crimes', fontsize=12)
                plt.xticks(range(1, 13), [months[i-1] for i in range(1, 13)])
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                
                if save_path:
                    plt.savefig(save_path, dpi=150, bbox_inches='tight')
                    plt.close()
                    return save_path
                else:
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.read()).decode()
                    plt.close()
                    return image_base64
                    
        except Exception as e:
            logger.error(f"Error generating monthly trend: {e}")
            plt.close()
            return None
    
    def generate_statistics(self, df):
        """Generate crime statistics JSON"""
        try:
            stats = {}
            
            # Total crimes
            stats['total_crimes'] = len(df)
            
            # Crime by hour
            if 'hour' in df.columns:
                hour_counts = df['hour'].value_counts().sort_index()
                stats['crime_by_hour'] = hour_counts.to_dict()
            
            # Crime by month
            if 'month' in df.columns:
                month_counts = df['month'].value_counts().sort_index()
                stats['crime_by_month'] = month_counts.to_dict()
            
            # Top crime types
            if 'crime_type' in df.columns:
                type_counts = df['crime_type'].value_counts().head(10)
                stats['top_crime_types'] = type_counts.to_dict()
            
            # Top locations
            if 'location' in df.columns:
                location_counts = df['location'].value_counts().head(10)
                stats['top_locations'] = location_counts.to_dict()
            
            # Crime by weapon
            if 'weapon_used' in df.columns:
                weapon_counts = df['weapon_used'].value_counts().head(10)
                stats['weapons_used'] = weapon_counts.to_dict()
            
            # Average victim age
            if 'victim_age' in df.columns:
                stats['avg_victim_age'] = float(df['victim_age'].mean())
            
            # Crime category distribution
            if 'crime_category' in df.columns:
                category_counts = df['crime_category'].value_counts()
                stats['crime_categories'] = category_counts.to_dict()
            
            logger.info("Statistics generated successfully")
            return stats
            
        except Exception as e:
            logger.error(f"Error generating statistics: {e}")
            return {}
    
    def generate_all_visualizations(self, df):
        """Generate all visualizations and return base64 images"""
        visualizations = {}
        
        try:
            # Heatmap
            heatmap = self.generate_heatmap(df)
            if heatmap:
                visualizations['heatmap'] = heatmap
            
            # Crime by hour
            hour_chart = self.generate_crime_by_hour(df)
            if hour_chart:
                visualizations['hour_chart'] = hour_chart
            
            # Crime by type
            type_chart = self.generate_crime_by_type(df)
            if type_chart:
                visualizations['type_chart'] = type_chart
            
            # Monthly trend
            monthly_chart = self.generate_monthly_trend(df)
            if monthly_chart:
                visualizations['monthly_trend'] = monthly_chart
            
            # Statistics
            stats = self.generate_statistics(df)
            visualizations['statistics'] = stats
            
            logger.info(f"Generated {len(visualizations)} visualizations")
            return visualizations
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            return visualizations
