# LangFlow Implementation Guide

## Step-by-Step Guide for Building the Traffic Congestion Analysis System

### Overview

This guide walks you through building the 3-agent system in Astra DataStax LangFlow with IBM Granite.

---

## Prerequisites

1. ✅ Astra DataStax account with LangFlow access
2. ✅ IBM watsonx.ai API Key and Project ID
3. ✅ Processed traffic data (from preprocessing script)
4. ✅ Knowledge base documents uploaded

---

## Step 1: Set Up IBM Granite Connection

### 1.1 Add IBM watsonx LLM Component

1. In LangFlow, search for **"watsonx"** or **"IBM"** in components
2. If not available, use **"Custom Component"** or **"API Request"**

### 1.2 Configure Credentials

```
API Key: [Your IBM watsonx API Key]
Project ID: [Your watsonx Project ID]
URL: https://us-south.ml.cloud.ibm.com
Model ID: ibm/granite-13b-chat-v2
```

### 1.3 Alternative: Using OpenAI-compatible Endpoint

If direct watsonx integration isn't available, use the OpenAI-compatible API:

```
Base URL: https://us-south.ml.cloud.ibm.com/ml/v1
API Key: Bearer [Your API Key]
Model: ibm/granite-13b-chat-v2
```

---

## Step 2: Set Up RAG with Astra Vector Store

### 2.1 Create Vector Collection

1. Go to Astra DB in your DataStax console
2. Create a new collection: `traffic_knowledge`
3. Set dimensions: 1536 (for OpenAI embeddings) or appropriate for your embedder

### 2.2 Upload Knowledge Documents

Upload these files from `data/knowledge_base/`:
- `traffic_congestion_classification.txt`
- `weather_impact_guidelines.txt`
- `incident_management_guidelines.txt`
- `time_patterns_analysis.txt`
- `bangalore_urban_mobility.txt`

### 2.3 LangFlow RAG Setup

1. Add **"Astra DB"** component
2. Configure connection to your database
3. Add **"Text Embeddings"** component (OpenAI or HuggingFace)
4. Connect: Documents → Embeddings → Astra DB

---

## Step 3: Build Agent 1 - Traffic Data Analysis Agent

### Purpose
Synthesizes traffic data into comprehensive summaries.

### 3.1 LangFlow Components Needed

```
[Chat Input] → [Traffic Data Tool] → [IBM Granite LLM] → [Chat Output]
```

### 3.2 Traffic Data Tool (Custom Component)

Create a **Python Function** component with this logic:

```python
def get_traffic_summary(area: str = None, date: str = None):
    """
    Retrieves traffic summary for specified area and date.
    Uses pre-processed data from area_summaries.json
    """
    import json
    
    # Load area summaries
    with open('data/processed/area_summaries.json', 'r') as f:
        summaries = json.load(f)
    
    if area and area in summaries:
        return json.dumps(summaries[area], indent=2)
    else:
        # Return overview of all areas
        overview = {area: {
            'avg_congestion': data['avg_congestion_level'],
            'total_incidents': data['total_incidents']
        } for area, data in summaries.items()}
        return json.dumps(overview, indent=2)
```

### 3.3 System Prompt for Traffic Data Agent

```
You are a Traffic Data Analysis Agent for Bangalore city.

Your role is to:
1. Analyze traffic data from multiple sources
2. Provide comprehensive traffic summaries
3. Identify patterns and anomalies
4. Present data in a clear, structured format

When responding:
- Always include specific numbers and metrics
- Compare current conditions to historical averages
- Highlight any unusual patterns
- Structure your response with clear sections

Available data includes:
- Traffic volume and average speeds
- Congestion levels (Light/Moderate/Heavy/Severe)
- Road capacity utilization
- Area-specific statistics
```

---

## Step 4: Build Agent 2 - Congestion Cause Analysis Agent

### Purpose
Correlates congestion with various factors to identify causes.

### 4.1 LangFlow Flow Structure

```
[Chat Input] → [Multi-Factor Analysis] → [RAG Retrieval] → [IBM Granite LLM] → [Chat Output]
                      ↓
              [Weather Data]
              [Incident Data]
              [Time Context]
```

### 4.2 Cause Analysis Tool

```python
def analyze_congestion_causes(area: str, congestion_level: float, 
                              weather: str, incidents: int, 
                              is_weekend: bool, road_utilization: float):
    """
    Analyzes potential causes of congestion based on multiple factors.
    """
    causes = []
    confidence = 0
    
    # Weather impact analysis
    if weather in ['Rain', 'Fog']:
        causes.append({
            'factor': 'Weather',
            'description': f'{weather} conditions reducing visibility and road grip',
            'impact': 'High',
            'confidence': 0.85
        })
    
    # Incident analysis
    if incidents >= 2:
        causes.append({
            'factor': 'Incidents',
            'description': f'{incidents} incidents reported causing lane blockages',
            'impact': 'High' if incidents >= 3 else 'Medium',
            'confidence': 0.90
        })
    
    # Capacity analysis
    if road_utilization >= 85:
        causes.append({
            'factor': 'Volume',
            'description': 'Road capacity near or at maximum',
            'impact': 'High',
            'confidence': 0.95
        })
    
    # Time-based analysis
    if not is_weekend and congestion_level >= 70:
        causes.append({
            'factor': 'Peak Hour',
            'description': 'Weekday peak hour traffic demand',
            'impact': 'High',
            'confidence': 0.88
        })
    
    if not causes:
        causes.append({
            'factor': 'Normal Pattern',
            'description': 'Traffic within expected parameters',
            'impact': 'Low',
            'confidence': 0.80
        })
    
    return causes
```

### 4.3 System Prompt for Cause Analysis Agent

```
You are a Congestion Cause Analysis Agent for Bangalore traffic.

Your role is to:
1. Identify the PRIMARY cause of congestion
2. List CONTRIBUTING factors in order of impact
3. Correlate multiple data sources to explain causes
4. Provide CONFIDENCE scores for each identified cause

When analyzing congestion, consider these factors:
- Time of day and day of week (peak hours, weekday vs weekend)
- Weather conditions (rain, fog, clear)
- Incidents (accidents, breakdowns, roadwork)
- Traffic volume and road capacity utilization
- Historical patterns for the location

Response format:
1. Primary Cause: [Main factor] - Confidence: [X%]
2. Contributing Factors:
   - Factor 1: [Description] - Impact: [High/Medium/Low]
   - Factor 2: [Description] - Impact: [High/Medium/Low]
3. Evidence: [Data points supporting the analysis]
4. Pattern Type: [Recurring/Non-recurring]
```

---

## Step 5: Build Agent 3 - Explainable Insight Assistant

### Purpose
Generates human-readable explanations with citations.

### 5.1 LangFlow Flow Structure

```
[User Query] → [Query Router] → [Agent 1 OR Agent 2] → [RAG Context] → [Explanation Generator] → [Response]
                                                              ↓
                                                    [Knowledge Base]
```

### 5.2 System Prompt for Explainable Insight Assistant

```
You are an Explainable Insight Assistant for traffic operators.

Your PRIMARY goal is to provide CLEAR, HUMAN-READABLE explanations that build TRUST in AI-driven analysis.

When explaining congestion:

1. START with a simple summary (1-2 sentences)
2. EXPLAIN the cause in plain language
3. PROVIDE evidence from data and knowledge base
4. CITE your sources (reference documents when applicable)
5. GIVE a confidence level
6. SUGGEST actionable recommendations (when appropriate)

Format your response as:

📍 LOCATION: [Area/Road name]
📊 STATUS: [Congestion level - Light/Moderate/Heavy/Severe]

🔍 EXPLANATION:
[Clear, plain-language explanation of why congestion is occurring]

📋 CONTRIBUTING FACTORS:
• [Factor 1] - [Brief explanation]
• [Factor 2] - [Brief explanation]

📚 BASED ON:
• [Data source or knowledge base reference]
• [Historical pattern if applicable]

💡 CONFIDENCE: [X%]

✅ RECOMMENDED ACTIONS:
• [Action 1]
• [Action 2]

IMPORTANT GUIDELINES:
- Use simple language, avoid jargon
- Always explain WHY, not just WHAT
- Be honest about uncertainty
- Make explanations actionable
- Reference time context (peak hours, weather, etc.)
```

---

## Step 6: Connect the Agents (Orchestration)

### 6.1 Router Logic

Create a router that directs queries to appropriate agents:

```python
def route_query(query: str) -> str:
    """
    Routes user query to appropriate agent based on intent.
    """
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['summary', 'overview', 'status', 'data', 'statistics']):
        return 'traffic_data_agent'
    
    elif any(word in query_lower for word in ['why', 'cause', 'reason', 'because', 'factor']):
        return 'cause_analysis_agent'
    
    elif any(word in query_lower for word in ['explain', 'understand', 'what happened', 'tell me']):
        return 'insight_assistant'
    
    else:
        # Default to insight assistant for general queries
        return 'insight_assistant'
```

### 6.2 Full Flow in LangFlow

```
                                    ┌─→ [Traffic Data Agent] ──┐
                                    │                          │
[Chat Input] → [Query Router] ──────┼─→ [Cause Analysis Agent] ┼──→ [Response Combiner] → [Chat Output]
                                    │                          │
                                    └─→ [Insight Assistant] ───┘
                                              ↓
                                    [RAG: Knowledge Base]
```

---

## Step 7: Test Scenarios

### Test Query 1: Data Summary
```
"Give me a traffic summary for Koramangala area"
```
Expected: Traffic Data Agent responds with area statistics

### Test Query 2: Cause Analysis
```
"Why is there heavy congestion on M.G. Road today?"
```
Expected: Cause Analysis Agent identifies factors

### Test Query 3: Explanation
```
"Explain the traffic situation on Sarjapur Road"
```
Expected: Insight Assistant provides full explanation with citations

### Test Query 4: Weather Impact
```
"How is the rain affecting traffic in Indiranagar?"
```
Expected: Cause Analysis + RAG retrieval about weather impacts

### Test Query 5: Trend Analysis
```
"Why does Marathahalli Bridge always get congested on Friday evenings?"
```
Expected: Insight Assistant explains recurring pattern with evidence

---

## Step 8: Final Checklist

### Before Demo

- [ ] All 3 agents respond correctly
- [ ] RAG retrieves relevant knowledge
- [ ] Explanations include confidence scores
- [ ] Sources are cited in responses
- [ ] Response time < 5 seconds
- [ ] No errors on edge cases

### Judging Criteria Alignment

| Criterion | How We Address It |
|-----------|-------------------|
| IBM Cloud Usage | watsonx.ai + Granite Model |
| Scalability | Multi-agent modular design |
| Innovativeness | Explainability-first approach |
| Societal Benefit | Helps operators make better decisions |
| Deployment Ready | Working demo on LangFlow |
| Commercial Viability | SaaS model for traffic authorities |
| Future Scope | Expandable to other cities |

---

## Troubleshooting

### Issue: watsonx connection fails
- Verify API key is correct
- Check Project ID format
- Ensure URL includes region (us-south)

### Issue: RAG not retrieving relevant context
- Check embedding dimensions match
- Verify documents are indexed
- Try more specific queries

### Issue: Slow responses
- Reduce max tokens in LLM settings
- Limit RAG retrieval to top 3-5 chunks
- Check network latency

---

## Next Steps

1. Build the flow in LangFlow following this guide
2. Test with sample queries
3. Refine prompts based on responses
4. Prepare demo scenarios
5. Create presentation slides
