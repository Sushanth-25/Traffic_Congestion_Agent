"""
Traffic Analysis API Server
=============================
FastAPI server that provides endpoints for LangFlow to call.

This bridges LangFlow with our live data and XAI services!

Endpoints:
- GET /traffic/{location} - Get live traffic data
- GET /weather - Get current weather
- GET /analyze/{location} - Get full XAI analysis
- GET /areas - List all available areas
- GET /smart-traffic - Dynamic location extraction from query (FOR LANGFLOW)

Run with: uvicorn src.api.traffic_api:app --reload --port 8001

Author: IBM Hackathon Team
Date: February 2026
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
import sys
import os
import requests
import json
import re
from pathlib import Path
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# ==================== CONFIGURATION FROM ENVIRONMENT ====================
LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY")
LANGFLOW_BASE_URL = os.getenv("LANGFLOW_BASE_URL", "https://api.langflow.astra.datastax.com")
LANGFLOW_FLOW_ID = os.getenv("LANGFLOW_FLOW_ID")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("PORT", os.getenv("API_PORT", "8001")))  # PORT for cloud platforms
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

# Cloud detection
IS_CLOUD = bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER") or os.getenv("HEROKU_APP_NAME") or os.getenv("PORT"))

# Validate required configuration
def validate_config():
    """Validate that required environment variables are set."""
    missing = []
    if not LANGFLOW_API_KEY or LANGFLOW_API_KEY == "your-langflow-api-key-here":
        missing.append("LANGFLOW_API_KEY")
    if not LANGFLOW_FLOW_ID or LANGFLOW_FLOW_ID == "your-flow-id-here":
        missing.append("LANGFLOW_FLOW_ID")
    return missing

def validate_all_config():
    """Validate all API keys including TomTom and OpenWeather."""
    missing = validate_config()
    tomtom_key = os.getenv("TOMTOM_API_KEY", "")
    openweather_key = os.getenv("OPENWEATHER_API_KEY", "")

    if not tomtom_key or tomtom_key == "your-tomtom-api-key-here":
        missing.append("TOMTOM_API_KEY")
    if not openweather_key or openweather_key == "your-openweather-api-key-here":
        missing.append("OPENWEATHER_API_KEY")
    return missing

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.live_traffic_service import (
    LiveTrafficService,
    BANGALORE_AREAS,
    format_for_langflow
)
from services.explainability_engine import ExplainabilityEngine, create_xai_response
from dataclasses import asdict

# Initialize FastAPI app
app = FastAPI(
    title="Traffic Analysis API",
    description="Live traffic data and XAI analysis for IBM Hackathon",
    version="2.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
traffic_service = LiveTrafficService()
xai_engine = ExplainabilityEngine()


# ==================== LANGFLOW API FUNCTIONS ====================

def call_langflow(question: str, location: str = None) -> dict:
    """
    Call LangFlow API (Astra DataStax) to get AI-powered traffic analysis.

    Args:
        question: User's question about traffic
        location: Optional location to fetch live data for

    Returns:
        LangFlow response with AI analysis
    """
    # Check if LangFlow is configured
    missing_config = validate_config()
    if missing_config:
        return {
            "success": False,
            "error": f"Missing configuration: {', '.join(missing_config)}. Please update .env file.",
            "fallback": True
        }

    # Get live traffic data if location is provided
    live_data_context = ""
    if location:
        try:
            insight = traffic_service.get_combined_insight(location)
            live_data_context = format_for_langflow(insight)
        except:
            live_data_context = "Live data unavailable"

    # Prepare the API request to LangFlow (Astra DataStax format)
    # Astra DataStax URL format: https://api.langflow.astra.datastax.com/lf/<FLOW_ID>/api/v1/run/<ENDPOINT>
    url = f"{LANGFLOW_BASE_URL}/lf/{LANGFLOW_FLOW_ID}/api/v1/run/flow"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LANGFLOW_API_KEY}"
    }

    payload = {
        "input_value": question,
        "output_type": "chat",
        "input_type": "chat"
    }

    # Add tweaks if we have live data to inject
    if live_data_context:
        payload["tweaks"] = {}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        result = response.json()

        # Extract the AI response from LangFlow output
        if "outputs" in result:
            outputs = result["outputs"]
            if outputs and len(outputs) > 0:
                output_data = outputs[0].get("outputs", [{}])[0]
                message = output_data.get("results", {}).get("message", {})
                ai_response = message.get("text", str(result))
                return {
                    "success": True,
                    "response": ai_response,
                    "location": location,
                    "live_data_used": bool(live_data_context)
                }

        return {"success": True, "response": str(result), "location": location}

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to LangFlow. Make sure it's running on " + LANGFLOW_BASE_URL,
            "fallback": True
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "LangFlow request timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/")
async def root():
    """Health check and API info."""
    return {
        "status": "online",
        "service": "Traffic Analysis API",
        "version": "2.0.0",
        "environment": "cloud" if IS_CLOUD else "local",
        "endpoints": {
            "langflow_primary": "/smart-traffic?query={user_question}",
            "traffic_data": "/traffic/{location}",
            "weather": "/weather",
            "xai_analysis": "/analyze/{location}",
            "langflow_static": "/langflow/{location}",
            "all_areas": "/areas",
            "api_status": "/api/status"
        },
        "documentation": "/docs"
    }


@app.get("/areas")
async def list_areas():
    """List all available Bangalore areas."""
    return {
        "areas": list(BANGALORE_AREAS.keys()),
        "count": len(BANGALORE_AREAS),
        "city": "Bangalore"
    }


@app.get("/traffic/{location}")
async def get_traffic(location: str):
    """
    Get live traffic data for a specific location.

    Args:
        location: Area name (e.g., "Koramangala", "Silk Board")
    """
    # Normalize location name
    location = location.replace("-", " ").replace("_", " ").title()

    if location not in BANGALORE_AREAS:
        # Try fuzzy matching
        for area in BANGALORE_AREAS:
            if location.lower() in area.lower() or area.lower() in location.lower():
                location = area
                break
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Location '{location}' not found. Use /areas to see available locations."
            )

    try:
        traffic = traffic_service.get_live_traffic(location)
        return asdict(traffic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weather")
async def get_weather(location: str = "Bangalore"):
    """Get current weather conditions."""
    try:
        weather = traffic_service.get_weather(location)
        return asdict(weather)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyze/{location}")
async def analyze_traffic(location: str):
    """
    Get full XAI analysis for a location.

    This is the MAIN endpoint that provides explainable insights!
    """
    # Normalize location
    location = location.replace("-", " ").replace("_", " ").title()

    if location not in BANGALORE_AREAS:
        for area in BANGALORE_AREAS:
            if location.lower() in area.lower() or area.lower() in location.lower():
                location = area
                break

    try:
        # Get combined insight
        insight = traffic_service.get_combined_insight(location)

        # Generate XAI response
        xai_response = create_xai_response(insight)

        return {
            "location": location,
            "analysis": xai_response["structured"],
            "formatted_explanation": xai_response["formatted_text"],
            "raw_data": {
                "traffic": asdict(insight.traffic),
                "weather": asdict(insight.weather),
                "time_context": insight.time_context,
                "factors": insight.contributing_factors
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/langflow/{location}")
async def langflow_context(location: str):
    """
    Get formatted context for LangFlow prompt injection.

    This endpoint returns data formatted specifically for the IBM Granite prompt!
    """
    location = location.replace("-", " ").replace("_", " ").title()

    if location not in BANGALORE_AREAS:
        for area in BANGALORE_AREAS:
            if location.lower() in area.lower() or area.lower() in location.lower():
                location = area
                break

    try:
        insight = traffic_service.get_combined_insight(location)
        formatted = format_for_langflow(insight)

        return {
            "location": location,
            "context_for_prompt": formatted,
            "confidence": insight.confidence_score,
            "timestamp": insight.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/all-areas-status")
async def all_areas_status():
    """
    Compact live traffic report for all Bangalore areas.
    Optimized for LLM context window — minimal tokens, maximum data.
    """
    from fastapi.responses import PlainTextResponse

    now = datetime.now()
    hour = now.hour
    is_weekend = now.weekday() >= 5

    if 7 <= hour < 10:
        period = "Morning Peak"
        is_peak = True
    elif 10 <= hour < 16:
        period = "Midday"
        is_peak = False
    elif 16 <= hour < 20:
        period = "Evening Peak"
        is_peak = True
    else:
        period = "Off-Peak"
        is_peak = False

    # Get weather once
    try:
        weather = traffic_service.get_weather("Bangalore")
        weather_line = f"{weather.condition}, {weather.temperature}°C, Humidity {weather.humidity}%, Wind {weather.wind_speed}km/h, Visibility {weather.visibility}km, Impact: {weather.weather_impact} ({weather.impact_percentage}% speed reduction)"
    except Exception:
        weather_line = "Clear, 27°C, Impact: None"

    # Header
    lines = []
    lines.append(f"LIVE BANGALORE TRAFFIC REPORT | {now.strftime('%Y-%m-%d %H:%M')} | {now.strftime('%A')} {period} | Peak: {'Yes' if is_peak else 'No'} | Weekend: {'Yes' if is_weekend else 'No'}")
    lines.append(f"Weather: {weather_line}")
    lines.append(f"Sources: TomTom Traffic API + OpenWeatherMap API")
    lines.append("")

    # Collect and sort areas
    area_rows = []
    for area in BANGALORE_AREAS:
        try:
            insight = traffic_service.get_combined_insight(area)
            t = insight.traffic
            hist_avg = insight.historical_comparison.get("historical_avg_congestion", 0)
            factors = ", ".join([f"{f['factor']}:{f['contribution_pct']}%" for f in insight.contributing_factors])
            
            area_rows.append({
                "area": area,
                "congestion": t.congestion_level,
                "cat": t.congestion_category,
                "speed": t.current_speed,
                "freeflow": t.free_flow_speed,
                "tti": t.travel_time_ratio,
                "incidents": t.incidents_nearby,
                "closure": t.road_closure,
                "factors": factors,
                "hist": hist_avg,
                "conf": insight.confidence_score,
            })
        except:
            continue

    area_rows.sort(key=lambda x: x["congestion"], reverse=True)

    # Compact format: one area per 2 lines
    for i, a in enumerate(area_rows, 1):
        comp = "Higher" if a["congestion"] > a["hist"] else "Lower"
        lines.append(f"{i}. {a['area']}: {a['congestion']}% ({a['cat']}) | Speed: {a['speed']}/{a['freeflow']}km/h | TTI: {a['tti']}x | Incidents: {a['incidents']} | Closure: {'Yes' if a['closure'] else 'No'}")
        lines.append(f"   Factors: {a['factors']} | Historical: {a['hist']}% ({comp}) | Confidence: {a['conf']*100:.0f}%")

    # Quick summary
    if area_rows:
        avg = sum(a["congestion"] for a in area_rows) / len(area_rows)
        lines.append("")
        lines.append(f"SUMMARY: {len(area_rows)} areas | Avg: {avg:.1f}% | Worst: {area_rows[0]['area']} ({area_rows[0]['congestion']}%) | Best: {area_rows[-1]['area']} ({area_rows[-1]['congestion']}%)")

    return {"report": "\n".join(lines)}


# ==================== SMART ENDPOINT FOR LANGFLOW (NO HARDCODING) ====================

def extract_location_from_query(query: str) -> Optional[str]:
    """
    Intelligently extract Bangalore location from user query.
    Uses fuzzy matching and common variations.
    """
    query_lower = query.lower()

    # Direct match first
    for area in BANGALORE_AREAS:
        if area.lower() in query_lower:
            return area

    # Common variations and aliases
    location_aliases = {
        "silk board": "Silk Board Junction",
        "silkboard": "Silk Board Junction",
        "koramangala": "Koramangala",
        "kormangala": "Koramangala",
        "indiranagar": "Indiranagar",
        "indira nagar": "Indiranagar",
        "whitefield": "Whitefield",
        "white field": "Whitefield",
        "electronic city": "Electronic City",
        "ec": "Electronic City",
        "e-city": "Electronic City",
        "mg road": "M.G. Road",
        "m.g. road": "M.G. Road",
        "majestic": "Majestic",
        "kempegowda": "Majestic",
        "jayanagar": "Jayanagar",
        "jaya nagar": "Jayanagar",
        "jp nagar": "J.P. Nagar",
        "jpnagar": "J.P. Nagar",
        "hebbal": "Hebbal",
        "yeshwanthpur": "Yeshwanthpur",
        "yeshwantpur": "Yeshwanthpur",
        "marathahalli": "Marathahalli",
        "marthahalli": "Marathahalli",
        "kr puram": "K.R. Puram",
        "krpuram": "K.R. Puram",
        "btm": "BTM Layout",
        "btm layout": "BTM Layout",
        "hsr": "HSR Layout",
        "hsr layout": "HSR Layout",
        "bannerghatta": "Bannerghatta Road",
        "outer ring road": "Outer Ring Road",
        "orr": "Outer Ring Road",
        "sarjapur": "Sarjapur Road",
        "bellandur": "Bellandur",
        "madiwala": "Madiwala",
        "domlur": "Domlur",
        "ulsoor": "Ulsoor",
        "mg road": "M.G. Road",
        "brigade road": "Brigade Road",
        "cunningham road": "Cunningham Road",
        "residency road": "Residency Road",
    }

    for alias, actual in location_aliases.items():
        if alias in query_lower:
            # Verify the actual location exists in our data
            for area in BANGALORE_AREAS:
                if actual.lower() in area.lower() or area.lower() in actual.lower():
                    return area
            return actual

    return None


@app.get("/smart-traffic")
async def smart_traffic(query: str = Query(..., description="User's traffic query")):
    """
    🚀 SMART ENDPOINT FOR LANGFLOW - Dynamically extracts location from query.

    This is the PRIMARY endpoint for LangFlow API Request component.
    It intelligently parses the user's question to find the location.

    Example queries:
    - "How is traffic at Silk Board?"
    - "What's the congestion level in Koramangala?"
    - "Why is Whitefield so congested?"

    Returns formatted context for LangFlow prompt injection.
    """
    # Extract location from query
    location = extract_location_from_query(query)

    if not location:
        # Return general Bangalore traffic info if no specific location found
        return {
            "location": "Bangalore (General)",
            "location_found": False,
            "query_received": query,
            "context_for_prompt": f"""
=== BANGALORE TRAFFIC OVERVIEW ===
Timestamp: {datetime.now().isoformat()}
Query: {query}

Note: No specific location detected in query.
Available areas: {', '.join(list(BANGALORE_AREAS.keys())[:10])}...

General Bangalore Traffic Patterns:
- Peak Hours: 8:30-10:30 AM and 5:30-8:30 PM
- Most Congested: Silk Board, Marathahalli, Whitefield
- Current Time Context: {'Peak Hour' if 8 <= datetime.now().hour <= 10 or 17 <= datetime.now().hour <= 20 else 'Off-Peak'}

Please ask about a specific area for detailed analysis.
""",
            "tip": "Try asking about specific areas like Koramangala, Silk Board, Whitefield, etc."
        }

    try:
        # Get full traffic insight for the detected location
        insight = traffic_service.get_combined_insight(location)
        formatted = format_for_langflow(insight)

        return {
            "location": location,
            "location_found": True,
            "query_received": query,
            "context_for_prompt": formatted,
            "traffic_data": {
                "congestion_level": insight.traffic.congestion_level,
                "congestion_category": insight.traffic.congestion_category,
                "current_speed": insight.traffic.current_speed,
                "free_flow_speed": insight.traffic.free_flow_speed,
            },
            "weather": {
                "condition": insight.weather.condition,
                "temperature": insight.weather.temperature,
                "humidity": insight.weather.humidity,
            },
            "factors": insight.contributing_factors,
            "confidence": insight.confidence_score,
            "timestamp": insight.timestamp
        }
    except Exception as e:
        return {
            "location": location,
            "location_found": True,
            "error": str(e),
            "context_for_prompt": f"""
=== TRAFFIC DATA FOR {location.upper()} ===
Timestamp: {datetime.now().isoformat()}
Status: Data fetch error - {str(e)}

Fallback information:
- Location: {location}
- Current Time: {datetime.now().strftime('%H:%M')}
- Is Peak Hour: {'Yes' if 8 <= datetime.now().hour <= 10 or 17 <= datetime.now().hour <= 20 else 'No'}
"""
        }


@app.get("/live-data")
async def live_data_text(query: str = Query(..., description="User's traffic query")):
    """
    🎯 SIMPLE TEXT ENDPOINT FOR LANGFLOW - Returns ONLY plain text, no JSON.

    Use this endpoint if LangFlow has trouble parsing JSON.
    Returns the formatted traffic data as plain text string.

    URL: http://localhost:8001/live-data?query=traffic at silk board
    """
    from fastapi.responses import PlainTextResponse

    # Extract location from query
    location = extract_location_from_query(query)

    if not location:
        return PlainTextResponse(content=f"""
=== BANGALORE TRAFFIC INFO ===
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Query: {query}

No specific location detected. Please ask about:
Silk Board, Koramangala, Whitefield, Marathahalli, Electronic City, etc.
""")

    try:
        insight = traffic_service.get_combined_insight(location)
        formatted = format_for_langflow(insight)
        return PlainTextResponse(content=formatted)
    except Exception as e:
        return PlainTextResponse(content=f"""
=== TRAFFIC DATA FOR {location.upper()} ===
Timestamp: {datetime.now().isoformat()}
Error: {str(e)}
Location: {location}
""")


@app.get("/smart-traffic/{query_path:path}")
async def smart_traffic_path(query_path: str):
    """
    Alternative path-based endpoint for LangFlow.
    Allows: /smart-traffic/How is traffic at Silk Board
    """
    return await smart_traffic(query=query_path)


# ==================== LANGFLOW AI ENDPOINTS ====================

@app.post("/ask")
async def ask_traffic_ai(question: str, location: Optional[str] = None):
    """
    Ask the AI about traffic conditions.

    This calls LangFlow with your question and optionally injects live data.

    Args:
        question: Your traffic-related question
        location: Optional area name for live data context
    """
    if location:
        location = location.replace("-", " ").replace("_", " ").title()
        # Find matching area
        for area in BANGALORE_AREAS:
            if location.lower() in area.lower() or area.lower() in location.lower():
                location = area
                break

    result = call_langflow(question, location)

    if not result.get("success") and result.get("fallback"):
        # Fallback: Use local XAI engine if LangFlow is unavailable
        if location:
            try:
                insight = traffic_service.get_combined_insight(location)
                xai_response = create_xai_response(insight)
                return {
                    "success": True,
                    "response": xai_response["formatted_text"],
                    "source": "local_fallback",
                    "note": "LangFlow unavailable, using local analysis"
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            raise HTTPException(status_code=503, detail=result.get("error"))

    return result


@app.get("/chat/{question}")
async def chat_simple(question: str):
    """
    Simple GET endpoint for quick questions.

    Example: /chat/How is traffic at Silk Board?
    """
    # Try to extract location from question
    location = None
    question_lower = question.lower()

    for area in BANGALORE_AREAS:
        if area.lower() in question_lower:
            location = area
            break

    return await ask_traffic_ai(question, location)


@app.get("/langflow/status")
async def langflow_status():
    """Check if LangFlow (Astra DataStax) is connected and configured."""
    missing_config = validate_config()

    # For Astra DataStax, we can't ping /health, so we check if config is set
    langflow_configured = not missing_config

    # Check if it's Astra DataStax URL
    is_astra = "datastax" in LANGFLOW_BASE_URL.lower() if LANGFLOW_BASE_URL else False

    return {
        "langflow_url": LANGFLOW_BASE_URL,
        "flow_id": LANGFLOW_FLOW_ID if LANGFLOW_FLOW_ID else "NOT SET",
        "api_key_configured": not any("LANGFLOW_API_KEY" in m for m in missing_config),
        "flow_id_configured": not any("LANGFLOW_FLOW_ID" in m for m in missing_config),
        "is_astra_datastax": is_astra,
        "config_status": "OK" if not missing_config else f"Missing: {', '.join(missing_config)}",
        "env_file": str(env_path),
        "instructions": {
            "1": f"Edit .env file at: {env_path}",
            "2": "Set LANGFLOW_API_KEY from LangFlow: Settings > API Keys",
            "3": "Set LANGFLOW_FLOW_ID from your flow URL",
            "4": "Restart the API server"
        }
    }


@app.get("/api/status")
async def api_status():
    """Check all API configurations - LangFlow, TomTom, OpenWeather."""
    all_missing = validate_all_config()

    # Get individual key statuses
    tomtom_key = os.getenv("TOMTOM_API_KEY", "")
    openweather_key = os.getenv("OPENWEATHER_API_KEY", "")

    # Check if LangFlow is configured (for Astra DataStax, we can't ping health)
    is_astra = "datastax" in LANGFLOW_BASE_URL.lower() if LANGFLOW_BASE_URL else False
    langflow_configured = bool(LANGFLOW_API_KEY and LANGFLOW_FLOW_ID and
                               LANGFLOW_API_KEY != "your-langflow-api-key-here" and
                               LANGFLOW_FLOW_ID != "your-flow-id-here")

    # Check TomTom connectivity (if key is set)
    tomtom_working = False
    if tomtom_key and tomtom_key != "your-tomtom-api-key-here":
        try:
            test_url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point=12.9716,77.5946&key={tomtom_key}"
            response = requests.get(test_url, timeout=5)
            tomtom_working = response.status_code == 200
        except:
            pass

    # Check OpenWeather connectivity (if key is set)
    openweather_working = False
    if openweather_key and openweather_key != "your-openweather-api-key-here":
        try:
            test_url = f"https://api.openweathermap.org/data/2.5/weather?lat=12.9716&lon=77.5946&appid={openweather_key}"
            response = requests.get(test_url, timeout=5)
            openweather_working = response.status_code == 200
        except:
            pass

    return {
        "status": "OK" if not all_missing else "INCOMPLETE",
        "env_file": str(env_path),
        "apis": {
            "langflow": {
                "configured": langflow_configured,
                "is_astra_datastax": is_astra,
                "url": LANGFLOW_BASE_URL,
                "flow_id": LANGFLOW_FLOW_ID if LANGFLOW_FLOW_ID else "NOT SET"
            },
            "tomtom": {
                "configured": bool(tomtom_key and tomtom_key != "your-tomtom-api-key-here"),
                "working": tomtom_working,
                "purpose": "Live traffic data"
            },
            "openweather": {
                "configured": bool(openweather_key and openweather_key != "your-openweather-api-key-here"),
                "working": openweather_working,
                "purpose": "Weather conditions"
            }
        },
        "missing_keys": all_missing if all_missing else None,
        "instructions": "Edit .env file and restart the server to configure missing APIs"
    }


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn

    # Print configuration status on startup
    all_missing = validate_all_config()
    tomtom_key = os.getenv("TOMTOM_API_KEY", "")
    openweather_key = os.getenv("OPENWEATHER_API_KEY", "")

    print("🚀 Starting Traffic Analysis API Server...")
    print(f"📍 Access at: http://localhost:{API_PORT}")
    print(f"📚 API Docs: http://localhost:{API_PORT}/docs")
    print(f"📁 ENV file: {env_path}")
    print("")
    print("📊 API Configuration Status:")
    print(f"   • LangFlow API Key: {'✅ Set' if LANGFLOW_API_KEY and LANGFLOW_API_KEY != 'your-langflow-api-key-here' else '❌ Not set'}")
    print(f"   • LangFlow Flow ID: {'✅ Set' if LANGFLOW_FLOW_ID and LANGFLOW_FLOW_ID != 'your-flow-id-here' else '❌ Not set'}")
    print(f"   • TomTom API Key:   {'✅ Set' if tomtom_key and tomtom_key != 'your-tomtom-api-key-here' else '❌ Not set'}")
    print(f"   • OpenWeather Key:  {'✅ Set' if openweather_key and openweather_key != 'your-openweather-api-key-here' else '❌ Not set'}")
    print("")

    if all_missing:
        print(f"⚠️  Missing config: {', '.join(all_missing)}")
        print("   Edit .env file to configure APIs")
    else:
        print("✅ All API configurations OK")

    print("")
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=DEBUG)

