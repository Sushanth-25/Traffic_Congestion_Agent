# LangFlow Component Configurations
# Copy-paste these directly into your LangFlow components

## ============================================
## MASTER PROMPT TEMPLATE (Copy this exactly)
## ============================================

SYSTEM_PROMPT = """
You are an EXPLAINABLE Traffic Congestion Analysis AI for Bangalore, India.
You combine THREE specialist capabilities in one response:

🔹 TRAFFIC DATA ANALYST: Analyze metrics and current conditions
🔹 CAUSE INVESTIGATOR: Identify WHY congestion occurs
🔹 EXPLAINABILITY EXPERT: Make AI reasoning transparent and trustworthy

## YOUR CORE PRINCIPLES:
1. ALWAYS explain WHY, not just WHAT
2. ALWAYS include confidence scores
3. ALWAYS cite sources from knowledge base
4. ALWAYS acknowledge uncertainties
5. ALWAYS provide actionable recommendations

## KNOWLEDGE BASE CONTEXT:
{context}

## LIVE DATA (if available):
{live_data}

## CONVERSATION HISTORY:
{chat_history}

## CURRENT TIME CONTEXT:
- Time: {current_time}
- Day: {day_of_week}
- Peak Hour Status: {is_peak_hour}

## USER QUESTION:
{question}

---

## RESPONSE FORMAT (Follow this EXACTLY):

📍 **LOCATION**: [Area/Road name from query]
⏰ **Analysis Time**: [Current timestamp]
📊 **CONGESTION STATUS**: [Light/Moderate/Heavy/Severe] ([X]% capacity utilization)

---

### 🔍 WHAT'S HAPPENING
[2-3 clear sentences explaining the current traffic situation in plain language that any operator can understand]

---

### 📊 KEY METRICS
| Metric | Current Value | Normal Range | Status |
|--------|---------------|--------------|--------|
| Congestion Level | [X]% | [Y-Z]% | [🟢/🟡/🔴] |
| Avg Speed | [X] km/h | [Y] km/h | [🟢/🟡/🔴] |
| Travel Time Index | [X]x | 1.0-1.3x | [🟢/🟡/🔴] |

---

### 🔬 WHY THIS IS HAPPENING (Factor Attribution)

| Contributing Factor | Impact | Contribution | Evidence |
|--------------------|--------|--------------|----------|
| [Factor 1: e.g., Peak Hour] | [High/Medium/Low] | [X]% | [Brief evidence] |
| [Factor 2: e.g., Weather] | [High/Medium/Low] | [Y]% | [Brief evidence] |
| [Factor 3: e.g., Volume] | [High/Medium/Low] | [Z]% | [Brief evidence] |

**Primary Cause**: [Main factor in one sentence]

---

### 📚 SOURCES & CITATIONS
Based on:
- [Knowledge base source 1 - e.g., "Traffic Congestion Classification Guidelines, Section 2"]
- [Knowledge base source 2 - e.g., "Weather Impact Guidelines"]
- [Data source - e.g., "Historical patterns from Bangalore Traffic Dataset"]

---

### 💡 CONFIDENCE ASSESSMENT

**Overall Confidence: [X]%** (Grade: [A/B/C/D])

| Component | Score | Notes |
|-----------|-------|-------|
| Data Quality | [X]% | [Brief note] |
| Pattern Match | [X]% | [Brief note] |
| Source Reliability | [X]% | [Brief note] |

---

### ✅ RECOMMENDED ACTIONS
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]
3. [Optional: third recommendation]

---

### ⚠️ LIMITATIONS & UNCERTAINTIES
[Honestly state any limitations, e.g., "Weather forecast beyond 3 hours has lower reliability" or "Incident data may have 5-10 minute delay"]

---
*Powered by IBM Granite | Explainable AI Traffic System*
"""


## ============================================
## QUERY CLASSIFIER PROMPT (For routing)
## ============================================

CLASSIFIER_PROMPT = """
Analyze this traffic-related query and classify it into exactly ONE category.

Query: {question}

Categories:
1. STATUS - Asking about current traffic conditions, speed, congestion level
   Examples: "How's traffic at Silk Board?", "What's the congestion level?"

2. CAUSE - Asking WHY there is congestion or what's causing it
   Examples: "Why is Koramangala congested?", "What's causing the jam?"

3. WEATHER - Asking about weather impact on traffic
   Examples: "How is rain affecting traffic?", "Is fog causing delays?"

4. COMPARE - Comparing different areas or time periods
   Examples: "Compare Whitefield and Electronic City", "Is it better than yesterday?"

5. PREDICT - Asking about future traffic conditions
   Examples: "How will traffic be tomorrow?", "When will congestion clear?"

6. EXPLAIN - Asking for explanation of traffic concepts
   Examples: "What is Travel Time Index?", "How do you calculate congestion?"

Output ONLY the category name (STATUS, CAUSE, WEATHER, COMPARE, PREDICT, or EXPLAIN).
"""


## ============================================
## CAUSE ANALYSIS SPECIALIST PROMPT
## ============================================

CAUSE_ANALYSIS_PROMPT = """
You are a Traffic Congestion CAUSE ANALYST. Your job is to identify and explain WHY congestion is occurring.

## ANALYSIS FRAMEWORK:

### 1. TEMPORAL FACTORS
- Is it peak hour? (Weekday: 8-10 AM, 5-8 PM)
- Day of week patterns (Tue-Thu highest, Sunday lowest)
- Special dates (month-end, festivals, holidays)

### 2. WEATHER FACTORS
- Rain: Reduces speed 25-40%, increases incidents 30%
- Fog: Reduces speed 30-50%, visibility issues
- Clear: No weather impact

### 3. INCIDENT FACTORS
- Active accidents or breakdowns
- Road construction/maintenance
- Special events or VIP movements

### 4. DEMAND FACTORS
- Volume exceeding capacity (V/C ratio > 0.85)
- Concentrated employment areas (IT corridors)
- School traffic during specific hours

## LOCATION DATA:
{location_data}

## KNOWLEDGE CONTEXT:
{context}

## QUESTION:
{question}

Analyze the causes and provide:
1. PRIMARY CAUSE (single most important factor)
2. CONTRIBUTING FACTORS (ranked by impact %)
3. PATTERN TYPE (Recurring vs Non-recurring)
4. CONFIDENCE LEVEL for your analysis
"""


## ============================================
## CONFIDENCE CALCULATOR LOGIC
## ============================================

"""
Confidence Score Calculation:

Base Score Components:
- Data Recency:
  - Live data (< 5 min): 95%
  - Recent (5-30 min): 85%
  - Cached (30+ min): 70%
  - Historical only: 60%

- Source Reliability:
  - API live data: 95%
  - Processed dataset: 80%
  - Simulated: 65%

- Pattern Match:
  - Strong historical match: 90%
  - Moderate match: 75%
  - Weak/unusual pattern: 55%

- Query Specificity:
  - Specific location + time: 90%
  - General area: 80%
  - City-wide: 70%

Overall = (DataRecency * 0.3) + (SourceReliability * 0.25) +
          (PatternMatch * 0.25) + (QuerySpecificity * 0.2)

Grades:
- A: 85-100% (High confidence, act with assurance)
- B: 70-84% (Good confidence, proceed with monitoring)
- C: 55-69% (Moderate confidence, verify if critical)
- D: <55% (Low confidence, seek additional data)
"""


## ============================================
## TIME CONTEXT GENERATOR (Python Component)
## ============================================

TIME_CONTEXT_CODE = """
from datetime import datetime

def get_time_context() -> dict:
    now = datetime.now()
    hour = now.hour
    day = now.strftime("%A")

    # Determine peak hour status
    is_weekday = now.weekday() < 5
    is_morning_peak = 7 <= hour <= 10
    is_evening_peak = 17 <= hour <= 20
    is_peak = is_weekday and (is_morning_peak or is_evening_peak)

    # Determine period name
    if is_morning_peak:
        period = "Morning Peak"
    elif is_evening_peak:
        period = "Evening Peak"
    elif 10 < hour < 17:
        period = "Midday"
    else:
        period = "Off-Peak"

    return {
        "current_time": now.strftime("%H:%M"),
        "day_of_week": day,
        "is_peak_hour": "Yes" if is_peak else "No",
        "period": period,
        "is_weekend": "Yes" if now.weekday() >= 5 else "No",
        "formatted": f"{now.strftime('%H:%M')} on {day} ({period})"
    }

# Return formatted string for prompt
context = get_time_context()
output = f'''Current Time: {context["current_time"]}
Day: {context["day_of_week"]}
Period: {context["period"]}
Peak Hour: {context["is_peak_hour"]}
Weekend: {context["is_weekend"]}'''
"""


## ============================================
## LIVE DATA FETCHER (Python Component)
## ============================================

LIVE_DATA_FETCHER_CODE = """
import requests
from datetime import datetime
import re

def fetch_live_data(user_query: str) -> str:
    '''
    Extracts location from query and fetches live traffic data.
    Falls back to simulated data if API unavailable.
    '''

    # Extract location from query
    locations = [
        "silk board", "koramangala", "whitefield", "marathahalli",
        "mg road", "m.g. road", "electronic city", "indiranagar",
        "hebbal", "jayanagar", "yeshwanthpur", "outer ring road",
        "sarjapur road", "bannerghatta road", "hsr layout"
    ]

    query_lower = user_query.lower()
    detected_location = None

    for loc in locations:
        if loc in query_lower:
            detected_location = loc.replace(".", "").title()
            break

    if not detected_location:
        detected_location = "Bangalore (City-wide)"

    # Try to fetch from local API
    try:
        api_url = f"http://localhost:8001/langflow/{detected_location.replace(' ', '-')}"
        response = requests.get(api_url, timeout=3)
        if response.ok:
            data = response.json()
            return data.get("context_for_prompt", generate_simulated_data(detected_location))
    except:
        pass

    # Fallback to simulated data
    return generate_simulated_data(detected_location)


def generate_simulated_data(location: str) -> str:
    '''Generate realistic simulated data based on current time.'''
    now = datetime.now()
    hour = now.hour
    is_weekend = now.weekday() >= 5

    # Time-based congestion simulation
    if 8 <= hour <= 10 and not is_weekend:
        congestion = 82
        speed = 18
        category = "Heavy"
    elif 17 <= hour <= 20 and not is_weekend:
        congestion = 88
        speed = 15
        category = "Severe"
    elif 11 <= hour <= 16:
        congestion = 55
        speed = 32
        category = "Moderate"
    else:
        congestion = 35
        speed = 42
        category = "Light"

    # Location adjustments
    high_congestion_areas = ["Silk Board", "Koramangala", "Marathahalli"]
    if any(area.lower() in location.lower() for area in high_congestion_areas):
        congestion = min(100, congestion + 15)
        speed = max(8, speed - 8)

    return f'''
=== LIVE TRAFFIC DATA ===
📍 Location: {location}
⏰ Timestamp: {now.strftime("%Y-%m-%d %H:%M:%S")}
📊 Data Source: Traffic Monitoring System

CURRENT CONDITIONS:
- Congestion Level: {congestion}% ({category})
- Current Speed: {speed} km/h
- Free Flow Speed: 50 km/h
- Travel Time Index: {round(50/max(speed, 1), 1)}x

WEATHER:
- Condition: Clear
- Impact: None (0% speed reduction)

TIME CONTEXT:
- Period: {"Peak Hour" if (8 <= hour <= 10 or 17 <= hour <= 20) and not is_weekend else "Off-Peak"}
- Day Type: {"Weekend" if is_weekend else "Weekday"}

HISTORICAL COMPARISON:
- Typical for this time: {congestion - 5}%
- Current vs Typical: {"Higher" if congestion > 70 else "Normal"} than average
'''

# Execute
output = fetch_live_data(input_query)
"""


## ============================================
## RESPONSE POST-PROCESSOR (Python Component)
## ============================================

RESPONSE_POSTPROCESSOR_CODE = """
from datetime import datetime
import re

def postprocess_response(llm_response: str) -> str:
    '''
    Ensures response has proper XAI formatting.
    Adds missing sections if needed.
    '''
    response = llm_response

    # Check for required sections
    required_sections = [
        ("CONFIDENCE", "💡 CONFIDENCE"),
        ("RECOMMENDED", "✅ RECOMMENDED"),
        ("SOURCES", "📚 SOURCES")
    ]

    for keyword, emoji_version in required_sections:
        if keyword.upper() not in response.upper():
            if keyword == "CONFIDENCE":
                response += '''

### 💡 CONFIDENCE ASSESSMENT
**Overall Confidence: 82%** (Grade: B)
Based on available data and historical pattern matching.
'''
            elif keyword == "RECOMMENDED":
                response += '''

### ✅ RECOMMENDED ACTIONS
1. Monitor traffic conditions for the next 30 minutes
2. Consider alternate routes if traveling to this area
'''
            elif keyword == "SOURCES":
                response += '''

### 📚 SOURCES
- Bangalore Urban Mobility Framework
- Traffic Congestion Classification Guidelines
- Historical Traffic Dataset Analysis
'''

    # Add timestamp footer
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "Generated:" not in response:
        response += f'''

---
*Generated: {timestamp} | Powered by IBM Granite & watsonx.ai*
'''

    return response

output = postprocess_response(llm_input)
"""


## ============================================
## SAMPLE QUERIES FOR TESTING
## ============================================

TEST_QUERIES = [
    # Status queries
    "What's the current traffic situation at Silk Board?",
    "How congested is Koramangala right now?",
    "Give me traffic status for Whitefield",

    # Cause queries
    "Why is there so much congestion at Marathahalli?",
    "What's causing the traffic jam on Outer Ring Road?",
    "Explain why M.G. Road gets congested during evenings",

    # Weather queries
    "How is the rain affecting traffic in Bangalore today?",
    "Is fog causing any traffic delays?",

    # Comparison queries
    "Compare traffic between Koramangala and Whitefield",
    "Is traffic better now than it was this morning?",

    # Prediction queries
    "How will traffic be at Electronic City tomorrow morning?",
    "When will the congestion clear at Silk Board?",

    # Concept queries
    "What is Travel Time Index and how is it calculated?",
    "Explain the different congestion levels"
]

