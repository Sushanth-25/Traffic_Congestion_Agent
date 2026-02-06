# 🚦 Smart Traffic API - Complete Documentation

## Overview

The **Smart Traffic API** (`/smart-traffic` and `/live-data`) is the core endpoint that bridges your **LangFlow AI flow** with **real-time traffic and weather data** from TomTom and OpenWeather APIs. It's specifically designed to provide live, accurate data for the AI to analyze and explain traffic conditions.

---

## 🎯 Two Endpoints Available

| Endpoint | Returns | Best For |
|----------|---------|----------|
| `/smart-traffic?query=...` | JSON object | When you need structured data |
| `/live-data?query=...` | **Plain text only** | **Recommended for LangFlow** - easier to use |

### Why Use `/live-data` Instead?
The `/live-data` endpoint returns **ONLY the formatted text** without any JSON wrapper. This means:
- No need to parse JSON in LangFlow
- The response goes directly to `{live_data}` variable
- Less chance of LLM seeing JSON and getting confused

---

## 📡 Endpoint Details

### Option 1: `/live-data` (RECOMMENDED for LangFlow)

```
GET http://<YOUR_IP>:8001/live-data?query={user_question}
```

**Returns**: Plain text only (no JSON)

**Example Response**:
```
=== LIVE TRAFFIC DATA FOR SILK BOARD ===
Timestamp: 2026-02-06T21:00:00
Data Source: TomTom Live API

CURRENT CONDITIONS:
- Congestion Level: 29.6% (Light)
- Current Speed: 19 km/h
- Free Flow Speed: 27 km/h
...
```

### Option 2: `/smart-traffic` (Returns JSON)

```
GET http://<YOUR_IP>:8001/smart-traffic?query={user_question}
```

**Returns**: JSON object with multiple fields

```
User asks question in LangFlow
        ↓
LangFlow calls Smart Traffic API
        ↓
API extracts location from question
        ↓
API fetches REAL data from TomTom + OpenWeather
        ↓
API returns formatted data to LangFlow
        ↓
LLM uses REAL data (not hallucinated) to generate response
```

**Without this API**: The LLM would make up fake statistics (like saying 85% congestion when it's actually 30%)

**With this API**: The LLM receives actual live data and reports accurate numbers

---

## 📡 Endpoint Details

### URL
```
GET http://localhost:8001/smart-traffic?query={user_question}
```

For Docker/LangFlow (since localhost doesn't work inside containers):
```
GET http://<YOUR_IP_ADDRESS>:8001/smart-traffic?query={user_question}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | The user's natural language question about traffic |

### Example Requests

```bash
# Simple location query
curl "http://localhost:8001/smart-traffic?query=whats+traffic+at+silk+board"

# Weather impact query
curl "http://localhost:8001/smart-traffic?query=how+is+rain+affecting+koramangala"

# Comparison query
curl "http://localhost:8001/smart-traffic?query=compare+whitefield+and+electronic+city"
```

---

## 📤 Response Structure

### Successful Response

```json
{
  "location": "Silk Board",
  "location_found": true,
  "query_received": "whats traffic at silk board",
  "context_for_prompt": "=== LIVE TRAFFIC DATA FOR SILK BOARD ===\n...",
  "traffic_data": {
    "congestion_level": 29.6,
    "congestion_category": "Light",
    "current_speed": 19,
    "free_flow_speed": 27
  },
  "weather": {
    "condition": "Clear",
    "temperature": 22.4,
    "humidity": 55
  },
  "factors": [
    {
      "factor": "Time Pattern",
      "description": "Off-Peak - Lower demand period",
      "impact": "Low",
      "contribution_pct": 52.9,
      "confidence": 0.9,
      "source": "Time Pattern Analysis Guidelines"
    },
    {
      "factor": "Traffic Volume",
      "description": "Current capacity utilization at 30%",
      "impact": "Medium",
      "contribution_pct": 47.1,
      "confidence": 0.95,
      "source": "Traffic Congestion Classification"
    }
  ],
  "confidence": 0.88,
  "timestamp": "2026-02-06T20:41:43.238462"
}
```

### Response Fields Explained

| Field | Description | Used For |
|-------|-------------|----------|
| `location` | Detected area name from query | Display in response header |
| `location_found` | Whether location was recognized | Error handling |
| `query_received` | Original user question | Debugging |
| `context_for_prompt` | **MAIN FIELD** - Formatted text for LLM | This goes to `{live_data}` in prompt |
| `traffic_data` | Raw traffic metrics | LLM extracts exact numbers |
| `weather` | Current weather conditions | Weather impact analysis |
| `factors` | XAI contributing factors | "Why this is happening" section |
| `confidence` | Analysis confidence (0-1) | Confidence score in response |
| `timestamp` | When data was fetched | "As of" timestamp |

---

## 🔑 The `context_for_prompt` Field

This is the **most important field**. It's a pre-formatted text block that gets injected into the `{live_data}` variable in your LangFlow prompt template.

### Example `context_for_prompt` Content:

```
=== LIVE TRAFFIC DATA FOR SILK BOARD ===
Timestamp: 2026-02-06T20:41:43.238462
Data Source: TomTom Live API

CURRENT CONDITIONS:
- Congestion Level: 29.6% (Light)
- Current Speed: 19 km/h
- Free Flow Speed: 27 km/h
- Travel Time Index: 1.42x normal

WEATHER CONDITIONS:
- Condition: Clear
- Temperature: 22.4°C
- Weather Impact: None (0% speed reduction)

TIME CONTEXT:
- Current Time: 20:41
- Day: Friday
- Period: Off-Peak
- Peak Hour: No

HISTORICAL COMPARISON:
- Typical for this day: 80% congestion
- Current vs Historical: Lower than usual

CONTRIBUTING FACTORS (XAI Analysis):
  - Time Pattern: 52.9% contribution (Low impact) - Off-Peak - Lower demand period
  - Traffic Volume: 47.1% contribution (Medium impact) - Current capacity utilization at 30%

ANALYSIS CONFIDENCE: 88%
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER                                        │
│                    "What's traffic at Silk Board?"                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         LANGFLOW FLOW                                    │
│  ┌──────────────┐                                                        │
│  │  Chat Input  │ ──────────────────────────────────────┐                │
│  └──────────────┘                                       │                │
│         │                                               │                │
│         ▼                                               ▼                │
│  ┌──────────────┐    GET request              ┌─────────────────┐       │
│  │ API Request  │ ──────────────────────────► │  YOUR LOCAL API │       │
│  │              │                             │  (port 8001)    │       │
│  └──────────────┘ ◄────────────────────────── └─────────────────┘       │
│         │              JSON response                    │               │
│         │                                               │               │
│         ▼                                               ▼               │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                    PROMPT TEMPLATE                            │      │
│  │  {context} ◄── Astra DB (knowledge base)                      │      │
│  │  {live_data} ◄── API Response (real TomTom/Weather data)      │      │
│  │  {question} ◄── Chat Input                                    │      │
│  │  {chat_history} ◄── Message History                           │      │
│  └──────────────────────────────────────────────────────────────┘      │
│         │                                                               │
│         ▼                                                               │
│  ┌──────────────┐                                                       │
│  │ IBM Granite  │ ── Uses REAL data to generate accurate response       │
│  │   (LLM)      │                                                       │
│  └──────────────┘                                                       │
│         │                                                               │
│         ▼                                                               │
│  ┌──────────────┐                                                       │
│  │ Chat Output  │ ── Response with ACTUAL statistics                    │
│  └──────────────┘                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 External APIs Used

### 1. TomTom Traffic Flow API

**Purpose**: Real-time traffic speed and congestion data

**What it provides**:
- Current road speed (km/h)
- Free flow speed (km/h) - speed with no traffic
- Congestion level (calculated as % difference)
- Travel time estimates

**API Call Made**:
```
GET https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json
    ?point={latitude},{longitude}
    &key={TOMTOM_API_KEY}
```

**Free Tier**: 2,500 requests/day

### 2. OpenWeather Current Weather API

**Purpose**: Real-time weather conditions

**What it provides**:
- Weather condition (Clear, Rain, Fog, etc.)
- Temperature (°C)
- Humidity (%)
- Visibility (km)
- Wind speed

**API Call Made**:
```
GET https://api.openweathermap.org/data/2.5/weather
    ?q=Bangalore,IN
    &appid={OPENWEATHER_API_KEY}
    &units=metric
```

**Free Tier**: 1,000 calls/day

---

## 📍 Supported Locations

The API recognizes these Bangalore areas:

| Area | Coordinates | Traffic Profile |
|------|-------------|-----------------|
| Silk Board | 12.9172, 77.6227 | Critical bottleneck |
| Koramangala | 12.9352, 77.6245 | IT hub, high congestion |
| Whitefield | 12.9698, 77.7500 | Tech corridor |
| Marathahalli | 12.9591, 77.6971 | ORR junction |
| Electronic City | 12.8456, 77.6603 | IT hub |
| MG Road | 12.9756, 77.6066 | Commercial center |
| Indiranagar | 12.9784, 77.6408 | Residential/commercial |
| Hebbal | 13.0358, 77.5970 | Airport route |
| Jayanagar | 12.9308, 77.5838 | Residential |
| HSR Layout | 12.9116, 77.6389 | IT residential |
| Bannerghatta Road | 12.8876, 77.5973 | South corridor |
| Sarjapur Road | 12.9100, 77.6800 | Tech corridor |
| Outer Ring Road | 12.9300, 77.6800 | Main arterial |
| Yeshwanthpur | 13.0294, 77.5415 | Industrial/Metro |

---

## 🔧 How Location Extraction Works

The API uses pattern matching to extract locations from natural language:

```python
# User query: "How's the traffic at silk board junction?"

# Step 1: Convert to lowercase
query_lower = "how's the traffic at silk board junction?"

# Step 2: Check against known locations
locations = ["silk board", "koramangala", "whitefield", ...]

# Step 3: Find match
for loc in locations:
    if loc in query_lower:  # "silk board" found!
        detected_location = "Silk Board"
        break

# Step 4: Get coordinates for API call
coords = BANGALORE_AREAS["Silk Board"]  # (12.9172, 77.6227)

# Step 5: Call TomTom & OpenWeather APIs with these coordinates
```

---

## 🧮 XAI (Explainability) Engine

The API includes an **Explainability Engine** that calculates WHY congestion is happening:

### Factor Calculation

```python
Contributing Factors:
├── Time Pattern (40-60% weight)
│   ├── Peak Hour: +30% congestion impact
│   ├── Off-Peak: -20% congestion impact
│   └── Weekend: -25% congestion impact
│
├── Weather Impact (15-25% weight)
│   ├── Rain: +25-40% congestion
│   ├── Fog: +15-30% congestion
│   └── Clear: 0% impact
│
├── Traffic Volume (25-35% weight)
│   └── Based on current speed vs free flow speed
│
└── Historical Pattern (10-20% weight)
    └── Comparison with typical conditions
```

### Confidence Calculation

```
Confidence Score = 
    (Data Recency × 0.30) +      # How fresh is the data?
    (Source Reliability × 0.25) + # API vs simulated?
    (Pattern Match × 0.25) +      # Does it match historical?
    (Query Specificity × 0.20)    # How specific is the location?

Grades:
- 85-100%: Grade A (High confidence)
- 70-84%:  Grade B (Good confidence)
- 55-69%:  Grade C (Moderate confidence)
- <55%:    Grade D (Low confidence)
```

---

## ⚙️ Configuration Required

### Environment Variables (`.env`)

```env
# Required for live data
TOMTOM_API_KEY=your_tomtom_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here

# API Server config
API_HOST=0.0.0.0
API_PORT=8001
```

### Starting the API Server

```cmd
cd C:\Users\Ullas N\Desktop\IBM_Hackathon
python -m uvicorn src.api.traffic_api:app --reload --host 0.0.0.0 --port 8001
```

**Important**: Use `--host 0.0.0.0` to make the API accessible from Docker/LangFlow containers.

---

## 🔗 LangFlow Integration

### API Request Component Settings

| Setting | Value |
|---------|-------|
| **Mode** | URL |
| **URL** | `http://<YOUR_IP>:8001/smart-traffic` |
| **Method** | GET |
| **Query Parameters** | `query` → Connect to Chat Input |

### Finding Your IP (for Docker access)

```cmd
ipconfig | findstr "IPv4"
```

Use the IP address shown (e.g., `10.178.186.164`) instead of `localhost`.

### Connecting in LangFlow

```
Chat Input ──────┬──────────────────────────► Prompt Template (question)
                 │
                 └──► API Request ──────────► Prompt Template (live_data)
                       (GET /smart-traffic)

Astra DB ────────────────────────────────────► Prompt Template (context)

Message History ─────────────────────────────► Prompt Template (chat_history)
```

---

## 🧪 Testing the API

### 1. Health Check
```bash
curl http://localhost:8001/
```

### 2. Test Smart Traffic Endpoint
```bash
curl "http://localhost:8001/smart-traffic?query=traffic+at+koramangala"
```

### 3. Test with Python
```python
import requests
response = requests.get(
    "http://localhost:8001/smart-traffic",
    params={"query": "How is traffic at Silk Board?"}
)
print(response.json())
```

### 4. View API Documentation
Open in browser: `http://localhost:8001/docs`

---

## ❌ Common Issues & Solutions

### Issue 1: "Invalid URL" in LangFlow
**Cause**: LangFlow runs in Docker, can't reach `localhost`
**Solution**: Use your machine's IP address instead of `localhost`

### Issue 2: LLM shows fake/hallucinated data (85% instead of real 30%)
**Cause**: Prompt template not strict enough
**Solution**: Use the updated prompt from `langflow_prompts_config.py` with CRITICAL INSTRUCTIONS

### Issue 3: "Connection refused"
**Cause**: API server not running or wrong port
**Solution**: Start the API with `python -m uvicorn src.api.traffic_api:app --host 0.0.0.0 --port 8001`

### Issue 4: API returns simulated data instead of live
**Cause**: Missing or invalid API keys
**Solution**: Check `.env` has valid `TOMTOM_API_KEY` and `OPENWEATHER_API_KEY`

---

## 📊 Example Complete Flow

**User Input**: "What's the traffic situation at Silk Board?"

**API Response** (context_for_prompt):
```
=== LIVE TRAFFIC DATA FOR SILK BOARD ===
Timestamp: 2026-02-06T20:41:43
Data Source: TomTom Live API

CURRENT CONDITIONS:
- Congestion Level: 29.6% (Light)
- Current Speed: 19 km/h
- Free Flow Speed: 27 km/h

WEATHER CONDITIONS:
- Condition: Clear
- Temperature: 22.4°C

CONTRIBUTING FACTORS:
- Time Pattern: 52.9% (Off-Peak)
- Traffic Volume: 47.1%

ANALYSIS CONFIDENCE: 88%
```

**LLM Output** (using real data):
```
📍 **LOCATION**: Silk Board
⏰ **As of**: 8:41 PM, Friday, Feb 6, 2026
📊 **STATUS**: Light (29.6%)

### 🔍 CURRENT SITUATION
Silk Board is currently experiencing Light congestion at 29.6%. 
Current speed is 19 km/h compared to free flow speed of 27 km/h.

### 📊 LIVE METRICS
| Metric | Value | Source |
|--------|-------|--------|
| Congestion Level | 29.6% | TomTom API |
| Current Speed | 19 km/h | TomTom API |
| Weather | Clear | OpenWeather API |
| Temperature | 22.4°C | OpenWeather API |

### 💡 CONFIDENCE: 88%
```

---

## 📁 Related Files

| File | Purpose |
|------|---------|
| `src/api/traffic_api.py` | Main API server code |
| `src/services/live_traffic_service.py` | TomTom & OpenWeather integration |
| `src/services/explainability_engine.py` | XAI factor calculation |
| `langflow/prompts/langflow_prompts_config.py` | Prompt templates |
| `.env` | API keys configuration |

---

## 🎯 Summary

The Smart Traffic API is the **bridge between real-world data and AI analysis**:

1. **Receives** natural language queries from LangFlow
2. **Extracts** location from the query
3. **Fetches** real-time data from TomTom (traffic) and OpenWeather (weather)
4. **Calculates** XAI factors (why congestion is happening)
5. **Returns** formatted data for the LLM to use

This ensures your AI reports **actual, accurate statistics** instead of hallucinated numbers.

---

*Last Updated: February 6, 2026*
*Version: 2.0*

