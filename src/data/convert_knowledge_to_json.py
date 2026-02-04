import json
import os

def convert_knowledge_base_to_json():
    """Convert knowledge base .txt files to JSON for Astra DB ingestion."""
    
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    
    knowledge_base_dir = os.path.join(project_root, "data", "knowledge_base")
    output_dir = os.path.join(project_root, "data", "processed")
    output_file = os.path.join(output_dir, "knowledge_base.json")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    documents = []
    
    # Check if knowledge base directory exists
    if not os.path.exists(knowledge_base_dir):
        print(f"❌ Knowledge base directory not found: {knowledge_base_dir}")
        print("Creating sample knowledge base files...")
        create_knowledge_base_files(knowledge_base_dir)
    
    # Read all .txt files from knowledge base
    for filename in os.listdir(knowledge_base_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(knowledge_base_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks (500 chars with overlap)
            chunks = split_into_chunks(content, chunk_size=500, overlap=50)
            
            for i, chunk in enumerate(chunks):
                documents.append({
                    "id": f"{filename.replace('.txt', '')}_{i}",
                    "source": filename,
                    "content": chunk,
                    "type": "knowledge_base"
                })
    
    # Save as JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2)
    
    print(f"✅ Created {output_file} with {len(documents)} chunks")
    return output_file

def split_into_chunks(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence end
        if end < len(text):
            last_period = chunk.rfind('.')
            if last_period > chunk_size * 0.5:
                chunk = chunk[:last_period + 1]
                end = start + last_period + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks

def create_knowledge_base_files(knowledge_base_dir):
    """Create the knowledge base files if they don't exist."""
    
    os.makedirs(knowledge_base_dir, exist_ok=True)
    
    files = {
        "traffic_congestion_classification.txt": """# Traffic Congestion Classification Framework

## Congestion Levels

### Level 1: Free Flow (Green)
- Road Capacity Utilization: 0-30%
- Average Speed: Above 80% of speed limit
- Travel Time Index: 1.0-1.2
- Characteristics: Vehicles move freely, minimal delays

### Level 2: Light Congestion (Yellow-Green)
- Road Capacity Utilization: 30-50%
- Average Speed: 60-80% of speed limit
- Travel Time Index: 1.2-1.5
- Characteristics: Slight slowdowns, stable flow

### Level 3: Moderate Congestion (Yellow)
- Road Capacity Utilization: 50-70%
- Average Speed: 40-60% of speed limit
- Travel Time Index: 1.5-2.0
- Characteristics: Noticeable delays, speed variations

### Level 4: Heavy Congestion (Orange)
- Road Capacity Utilization: 70-85%
- Average Speed: 20-40% of speed limit
- Travel Time Index: 2.0-3.0
- Characteristics: Significant delays, stop-and-go traffic

### Level 5: Severe Congestion (Red)
- Road Capacity Utilization: 85-100%
- Average Speed: Below 20% of speed limit
- Travel Time Index: Above 3.0
- Characteristics: Gridlock conditions, extensive delays

## Key Performance Indicators
1. Travel Time Index (TTI): Ratio of peak travel time to free-flow travel time
2. Road Capacity Utilization: Percentage of road capacity being used
3. Average Speed: Mean vehicle speed on the road segment
4. Queue Length: Length of vehicle queues at intersections""",

        "weather_impact_guidelines.txt": """# Weather Impact on Traffic Congestion

## Clear Weather Conditions
- Impact Level: Baseline (No additional impact)
- Speed Reduction: 0%
- Congestion Multiplier: 1.0x
- Recommendations: Normal traffic management

## Rain Conditions
- Impact Level: Moderate to High
- Speed Reduction: 10-30%
- Congestion Multiplier: 1.3-1.5x
- Visibility: Reduced
- Road Conditions: Wet, slippery
- Recommendations:
  * Increase signal timing
  * Deploy dynamic message signs
  * Advise reduced speeds

## Fog Conditions
- Impact Level: High
- Speed Reduction: 20-40%
- Congestion Multiplier: 1.4-1.7x
- Visibility: Severely reduced (below 200m)
- Recommendations:
  * Activate fog warnings
  * Reduce speed limits dynamically
  * Increase headway recommendations

## Overcast Conditions
- Impact Level: Low
- Speed Reduction: 0-5%
- Congestion Multiplier: 1.0-1.1x
- Recommendations: Monitor for weather changes

## Windy Conditions
- Impact Level: Low to Moderate
- Speed Reduction: 5-15%
- Congestion Multiplier: 1.1-1.2x
- Special Concerns: High-profile vehicles, two-wheelers
- Recommendations:
  * Warn high-profile vehicle drivers
  * Monitor bridge and elevated road sections""",

        "incident_management_guidelines.txt": """# Traffic Incident Management Guidelines

## Incident Classification

### Minor Incidents
- Duration: Less than 30 minutes
- Lane Blockage: Shoulder or single lane
- Impact Radius: 1-2 km
- Congestion Increase: 10-20%
- Examples: Minor fender-benders, disabled vehicles

### Moderate Incidents
- Duration: 30 minutes to 2 hours
- Lane Blockage: 1-2 lanes
- Impact Radius: 2-5 km
- Congestion Increase: 20-50%
- Examples: Multi-vehicle accidents, cargo spills

### Major Incidents
- Duration: More than 2 hours
- Lane Blockage: Multiple lanes or full closure
- Impact Radius: 5-15 km
- Congestion Increase: 50-200%
- Examples: Serious accidents, hazmat incidents

## Roadwork Impact Assessment

### Planned Roadwork
- Advance Notice: Required 48-72 hours
- Peak Hour Restrictions: Avoid if possible
- Congestion Increase: 15-40% depending on lane closure
- Mitigation: Advance signage, alternate route suggestions

### Emergency Repairs
- Immediate response required
- Congestion Increase: 30-60%
- Mitigation: Real-time traveler information, police assistance

## Response Strategies
1. Detection: Average 2-5 minutes
2. Verification: Average 3-5 minutes
3. Response Dispatch: Average 5-10 minutes
4. Clearance: Varies by incident severity
5. Recovery: Traffic normalization period""",

        "time_patterns_analysis.txt": """# Time-Based Traffic Pattern Analysis

## Daily Patterns

### Morning Peak (7:00 AM - 10:00 AM)
- Congestion Level: High
- Primary Flow: Residential to Commercial/Industrial
- Peak Hour: 8:30 AM - 9:30 AM
- Typical Congestion Increase: 40-70%
- Key Corridors: Inbound arterials, IT corridors

### Midday Off-Peak (10:00 AM - 4:00 PM)
- Congestion Level: Low to Moderate
- Flow Pattern: Mixed, commercial activity
- Typical Congestion: Baseline + 10-20%
- Opportunities: Optimal for roadwork, deliveries

### Evening Peak (5:00 PM - 9:00 PM)
- Congestion Level: Highest
- Primary Flow: Commercial/Industrial to Residential
- Peak Hour: 6:00 PM - 7:30 PM
- Typical Congestion Increase: 50-100%
- Duration: Longer than morning peak

### Night Off-Peak (9:00 PM - 7:00 AM)
- Congestion Level: Minimal
- Flow Pattern: Sparse, freight movement
- Typical Congestion: Baseline
- Opportunities: Major roadwork, infrastructure maintenance

## Weekly Patterns

### Monday
- Congestion: High (weekly peak start)
- Characteristics: Return to work traffic

### Tuesday-Thursday
- Congestion: Highest weekday levels
- Characteristics: Regular commute patterns

### Friday
- Congestion: High with early evening peak
- Characteristics: Weekend travel begins

### Saturday
- Congestion: Moderate, shopping-focused
- Peak: 11:00 AM - 2:00 PM, 5:00 PM - 8:00 PM

### Sunday
- Congestion: Lowest
- Peak: Evening return traffic (5:00 PM - 9:00 PM)""",

        "bangalore_urban_mobility.txt": """# Bangalore Urban Mobility Framework

## City Traffic Characteristics

### Key Commercial Areas
1. **M.G. Road**: Central business district, high pedestrian activity
2. **Koramangala**: IT hub, startup ecosystem, mixed residential-commercial
3. **Whitefield**: Major IT corridor, high morning/evening peaks
4. **Indiranagar**: Commercial + residential, nightlife traffic
5. **Electronic City**: IT SEZ, severe peak hour congestion
6. **Jayanagar**: Residential with commercial pockets
7. **Hebbal**: Gateway to airport, junction congestion
8. **Banashankari**: Residential area, school traffic impact

## Unique Congestion Factors

### IT Sector Impact
- Shift Timings: 9 AM, 6 PM major peaks
- Cab Aggregators: Significant road space usage
- Tech Parks: Concentrated employment centers

### Public Transport Integration
- BMTC Buses: 6,500+ buses daily
- Metro: Green and Purple lines operational
- Suburban Rail: Under development
- Impact: Mode shift reducing road congestion by 15-20%

### Two-Wheeler Dominance
- Two-wheeler Share: 70%+ of vehicles
- Lane Filtering: Common practice
- Impact: Higher vehicle density per lane

## Recommended Interventions

### Short-term (Immediate)
- Adaptive signal control
- Real-time traveler information
- Incident quick-response teams

### Medium-term (1-2 years)
- Congestion pricing pilots
- Enhanced public transport
- Parking management systems

### Long-term (3-5 years)
- Metro network expansion
- Transit-oriented development
- Smart corridor implementation"""
    }
    
    for filename, content in files.items():
        filepath = os.path.join(knowledge_base_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Created: {filename}")

if __name__ == "__main__":
    convert_knowledge_base_to_json()