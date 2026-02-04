"""
Traffic Data Preprocessor for Bangalore Traffic Dataset
=========================================================
This script prepares the raw traffic data for the AI agents.

Aligns with Requirements:
- FR-TDA-001: Ingest traffic data
- FR-TDA-002: Normalize and standardize data formats
- FR-TDA-003: Generate comprehensive traffic summaries

Author: IBM Hackathon Team
Date: January 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

# Paths
RAW_DATA_PATH = "data/raw/Banglore_traffic_Dataset.csv"
PROCESSED_DATA_PATH = "data/processed/"
KNOWLEDGE_BASE_PATH = "data/knowledge_base/"


def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load the raw Bangalore traffic dataset."""
    print(f"📂 Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} records with {len(df.columns)} columns")
    return df


def enrich_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based features for temporal analysis.
    Supports FR-CCA-001: Correlate congestion with time-of-day patterns
    """
    print("⏰ Enriching temporal features...")
    
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    df['Quarter'] = df['Date'].dt.quarter
    df['Is_Weekend'] = df['Date'].dt.dayofweek >= 5
    
    # Classify time periods (simulating if time was available)
    # For demo, we'll use date patterns to simulate peak hours
    df['Day_Type'] = df['Is_Weekend'].apply(lambda x: 'Weekend' if x else 'Weekday')
    
    print("✅ Added: Day_of_Week, Month, Quarter, Is_Weekend, Day_Type")
    return df


def categorize_congestion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize congestion levels into readable categories.
    Supports FR-EIA-001: Generate human-readable explanations
    """
    print("🚦 Categorizing congestion levels...")
    
    def get_congestion_category(level):
        if level < 30:
            return "Light"
        elif level < 60:
            return "Moderate"
        elif level < 85:
            return "Heavy"
        else:
            return "Severe"
    
    df['Congestion_Category'] = df['Congestion Level'].apply(get_congestion_category)
    
    print("✅ Added: Congestion_Category (Light/Moderate/Heavy/Severe)")
    return df


def categorize_weather_impact(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add weather impact severity for cause analysis.
    Supports FR-CCA-003: Incorporate weather condition impacts
    """
    print("🌦️ Categorizing weather impact...")
    
    weather_impact = {
        'Clear': 'None',
        'Overcast': 'Low',
        'Windy': 'Low',
        'Rain': 'High',
        'Fog': 'High'
    }
    
    df['Weather_Impact'] = df['Weather Conditions'].map(weather_impact)
    
    print("✅ Added: Weather_Impact (None/Low/High)")
    return df


def create_incident_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create incident-related flags for cause analysis.
    Supports FR-CCA-002: Integrate road incident data
    """
    print("🚨 Creating incident flags...")
    
    df['Has_Incidents'] = df['Incident Reports'] > 0
    df['Has_Roadwork'] = df['Roadwork and Construction Activity'] == 'Yes'
    df['Incident_Severity'] = pd.cut(
        df['Incident Reports'], 
        bins=[-1, 0, 1, 3, 100], 
        labels=['None', 'Low', 'Medium', 'High']
    )
    
    print("✅ Added: Has_Incidents, Has_Roadwork, Incident_Severity")
    return df


def calculate_congestion_factors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate which factors likely contribute to congestion.
    Supports FR-CCA-004: Analyze traffic volume changes
    """
    print("📊 Calculating congestion contributing factors...")
    
    # Determine primary cause based on correlation analysis
    def determine_primary_cause(row):
        causes = []
        
        # High congestion scenarios
        if row['Congestion Level'] >= 60:
            # Check weather
            if row['Weather Conditions'] in ['Rain', 'Fog']:
                causes.append('Weather')
            
            # Check incidents
            if row['Incident Reports'] >= 2:
                causes.append('Incidents')
            
            # Check roadwork
            if row['Roadwork and Construction Activity'] == 'Yes':
                causes.append('Roadwork')
            
            # Check if high volume
            if row['Road Capacity Utilization'] >= 80:
                causes.append('High Volume')
            
            # Check time patterns (weekday)
            if not row['Is_Weekend']:
                causes.append('Peak Hours')
        
        if not causes:
            if row['Congestion Level'] >= 60:
                causes.append('Regular Traffic Pattern')
            else:
                causes.append('Normal Flow')
        
        return ', '.join(causes)
    
    df['Contributing_Factors'] = df.apply(determine_primary_cause, axis=1)
    
    print("✅ Added: Contributing_Factors")
    return df


def generate_area_summary(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics per area for agent consumption.
    Supports FR-TDA-003: Generate comprehensive traffic summaries
    """
    print("📈 Generating area summaries...")
    
    summary = {}
    
    for area in df['Area Name'].unique():
        area_df = df[df['Area Name'] == area]
        
        summary[area] = {
            'total_records': len(area_df),
            'roads': area_df['Road/Intersection Name'].unique().tolist(),
            'avg_congestion_level': round(area_df['Congestion Level'].mean(), 2),
            'max_congestion_level': round(area_df['Congestion Level'].max(), 2),
            'avg_speed': round(area_df['Average Speed'].mean(), 2),
            'total_incidents': int(area_df['Incident Reports'].sum()),
            'roadwork_days': int(area_df['Has_Roadwork'].sum()),
            'severe_congestion_days': int((area_df['Congestion Level'] >= 85).sum()),
            'weather_distribution': area_df['Weather Conditions'].value_counts().to_dict(),
            'congestion_by_day': area_df.groupby('Day_of_Week')['Congestion Level'].mean().to_dict()
        }
    
    print(f"✅ Generated summaries for {len(summary)} areas")
    return summary


def generate_dataset_statistics(df: pd.DataFrame) -> dict:
    """Generate overall dataset statistics for context."""
    print("📊 Generating dataset statistics...")
    
    stats = {
        'total_records': len(df),
        'date_range': {
            'start': df['Date'].min().strftime('%Y-%m-%d'),
            'end': df['Date'].max().strftime('%Y-%m-%d')
        },
        'areas_count': df['Area Name'].nunique(),
        'areas': df['Area Name'].unique().tolist(),
        'roads_count': df['Road/Intersection Name'].nunique(),
        'weather_conditions': df['Weather Conditions'].unique().tolist(),
        'overall_avg_congestion': round(df['Congestion Level'].mean(), 2),
        'congestion_distribution': df['Congestion_Category'].value_counts().to_dict(),
        'weather_distribution': df['Weather Conditions'].value_counts().to_dict(),
        'weekday_vs_weekend': {
            'weekday_avg_congestion': round(df[~df['Is_Weekend']]['Congestion Level'].mean(), 2),
            'weekend_avg_congestion': round(df[df['Is_Weekend']]['Congestion Level'].mean(), 2)
        }
    }
    
    print("✅ Dataset statistics generated")
    return stats


def save_processed_data(df: pd.DataFrame, area_summary: dict, stats: dict):
    """Save all processed data to files."""
    print("\n💾 Saving processed data...")
    
    # Ensure directory exists
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    # Save enriched dataset
    csv_path = os.path.join(PROCESSED_DATA_PATH, "enriched_traffic_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ Saved: {csv_path}")
    
    # Save as JSON for agent consumption
    json_path = os.path.join(PROCESSED_DATA_PATH, "traffic_data.json")
    df.to_json(json_path, orient='records', date_format='iso')
    print(f"✅ Saved: {json_path}")
    
    # Save area summaries
    summary_path = os.path.join(PROCESSED_DATA_PATH, "area_summaries.json")
    with open(summary_path, 'w') as f:
        json.dump(area_summary, f, indent=2, default=str)
    print(f"✅ Saved: {summary_path}")
    
    # Save statistics
    stats_path = os.path.join(PROCESSED_DATA_PATH, "dataset_statistics.json")
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    print(f"✅ Saved: {stats_path}")


def create_sample_queries_for_demo() -> list:
    """
    Create sample queries that demonstrate the system capabilities.
    Aligned with demo scenarios from OBJECTIVES.md
    """
    queries = [
        {
            "scenario": "Peak Hour Analysis",
            "query": "Why is there heavy congestion on Sarjapur Road during weekday mornings?",
            "expected_factors": ["Peak Hours", "High Volume", "Regular Traffic Pattern"]
        },
        {
            "scenario": "Incident Impact",
            "query": "What caused the severe congestion on M.G. Road yesterday?",
            "expected_factors": ["Incidents", "Roadwork"]
        },
        {
            "scenario": "Weather Effect",
            "query": "How does rain affect traffic congestion in Koramangala?",
            "expected_factors": ["Weather", "Reduced Speed"]
        },
        {
            "scenario": "Trend Query",
            "query": "Why is Marathahalli Bridge always congested on Fridays?",
            "expected_factors": ["Peak Hours", "Weekend Exodus", "High Volume"]
        },
        {
            "scenario": "Comparison Query",
            "query": "Compare congestion patterns between Indiranagar and Whitefield",
            "expected_factors": ["Area Comparison", "Volume Differences"]
        }
    ]
    
    return queries


def main():
    """Main preprocessing pipeline."""
    print("=" * 60)
    print("🚦 TRAFFIC DATA PREPROCESSING PIPELINE")
    print("=" * 60)
    print()
    
    # Step 1: Load raw data
    df = load_raw_data(RAW_DATA_PATH)
    print()
    
    # Step 2: Enrich with temporal features
    df = enrich_temporal_features(df)
    print()
    
    # Step 3: Categorize congestion
    df = categorize_congestion(df)
    print()
    
    # Step 4: Categorize weather impact
    df = categorize_weather_impact(df)
    print()
    
    # Step 5: Create incident flags
    df = create_incident_flags(df)
    print()
    
    # Step 6: Calculate contributing factors
    df = calculate_congestion_factors(df)
    print()
    
    # Step 7: Generate summaries
    area_summary = generate_area_summary(df)
    print()
    
    # Step 8: Generate statistics
    stats = generate_dataset_statistics(df)
    print()
    
    # Step 9: Save all processed data
    save_processed_data(df, area_summary, stats)
    
    # Print summary
    print()
    print("=" * 60)
    print("✅ PREPROCESSING COMPLETE")
    print("=" * 60)
    print(f"""
📊 Processed {len(df)} records
📍 {df['Area Name'].nunique()} areas covered
🛣️  {df['Road/Intersection Name'].nunique()} roads/intersections
📅 Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}

New columns added:
  - Day_of_Week, Month, Quarter, Is_Weekend, Day_Type
  - Congestion_Category (Light/Moderate/Heavy/Severe)
  - Weather_Impact (None/Low/High)
  - Has_Incidents, Has_Roadwork, Incident_Severity
  - Contributing_Factors

Output files:
  - data/processed/enriched_traffic_data.csv
  - data/processed/traffic_data.json
  - data/processed/area_summaries.json
  - data/processed/dataset_statistics.json
""")
    
    # Save sample queries
    queries_path = os.path.join(PROCESSED_DATA_PATH, "sample_queries.json")
    with open(queries_path, 'w') as f:
        json.dump(create_sample_queries_for_demo(), f, indent=2)
    print(f"✅ Sample demo queries saved to: {queries_path}")


if __name__ == "__main__":
    main()
