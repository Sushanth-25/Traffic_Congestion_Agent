# Agentic AI System for Explainable Traffic Congestion Analysis
## IBM Hackathon 2026 - Complete Presentation Guide

---

# PROJECT OVERVIEW

## What We Built

An **Explainable AI-powered traffic analysis system** for Bangalore using:
- **IBM Granite Model** (ibm/granite-3-8b-instruct) via watsonx.ai
- **DataStax LangFlow** for orchestration
- **AstraDB** as vector store for RAG

## Core Innovation

A **single IBM Granite model** with intelligent prompt engineering that simulates **3 specialized agent behaviors**:
1. Traffic Data Analysis Agent
2. Congestion Cause Analysis Agent
3. Explainable Insight Assistant

This approach is efficient (1 API call), cost-effective, and leverages Granite's advanced reasoning capabilities.

---

# SLIDE 1: Title Slide

**Title:** Agentic AI System for Explainable Traffic Congestion Analysis

**Subtitle:** Powered by IBM Granite & DataStax LangFlow

**Team Name:** [Your Team Name]

**Event:** IBM Hackathon 2026

---

# SLIDE 2: Problem Statement

## The Challenge

### Current Issues in Traffic Management:

| Problem | Real-World Impact |
|---------|-------------------|
| **Black Box Alerts** | Operators see "Congestion detected" but don't know WHY |
| **Low Trust in AI** | Without explanations, operators hesitate to act |
| **Data Overload** | Too many data sources, no unified analysis |
| **Slow Decision Making** | Time wasted cross-referencing multiple systems |

### What Operators Get Today:
> ❌ "Alert: Heavy traffic on Silk Board"

### What Operators Actually Need:
> ✅ "Heavy traffic on Silk Board due to evening rush hour (6:30 PM) + light rain reducing capacity by 15%. Confidence: 88%. Recommend: Use HSR Layout alternate route."

---

# SLIDE 3: Our Solution

## Explainable AI Traffic System

### Single Model, Multi-Agent Behavior

We use **one IBM Granite model** with smart prompt engineering to activate **3 agent behaviors** based on query type:

```
┌─────────────────────────────────────────────────────────┐
│                    USER QUERY                            │
│          "Why is Koramangala congested?"                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              IBM GRANITE MODEL                           │
│     (with 3-Agent Behavior Prompt)                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Agent 1: Traffic Data   → Activated if needed   │   │
│  │ Agent 2: Cause Analysis → Activated if needed   │   │
│  │ Agent 3: Explanation    → Always activated      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              EXPLAINABLE OUTPUT                          │
│  • Traffic Status with data                             │
│  • Cause identification with confidence                 │
│  • Human-readable explanation                           │
│  • Actionable recommendations                           │
│  • Source citations from knowledge base                 │
└─────────────────────────────────────────────────────────┘
```

### Why This Works:
- **1 API call** instead of 3 (cost-effective)
- **Faster response** (no chaining delays)
- **Coherent output** (single model = consistent formatting)
- **IBM Granite's capability** handles multi-role reasoning effectively

---

# SLIDE 4: System Architecture

## Technical Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                                    │
│                    LangFlow Playground Chat                              │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      LANGFLOW ORCHESTRATION                               │
│                                                                           │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐   │
│  │ Chat Input │───▶│  AstraDB   │───▶│   Parser   │───▶│  Prompt    │   │
│  │            │    │  (Search)  │    │ Component  │    │  Template  │   │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘   │
│        │                 ▲                                   │           │
│        │                 │                                   ▼           │
│        │          ┌────────────┐                      ┌────────────┐    │
│        └─────────▶│ Embeddings │                      │IBM Granite │    │
│        (question) │  (Search)  │                      │   Model    │    │
│                   └────────────┘                      └────────────┘    │
│                                                              │           │
│                                                              ▼           │
│                                                       ┌────────────┐    │
│                                                       │Chat Output │    │
│                                                       └────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                     KNOWLEDGE BASE (RAG)                                  │
│                                                                           │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ • Traffic Congestion Classification                              │   │
│   │ • Weather Impact Guidelines                                      │   │
│   │ • Incident Management Protocols                                  │   │
│   │ • Time Patterns Analysis                                         │   │
│   │ • Bangalore Urban Mobility Framework                             │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│   Stored in AstraDB Vector Store with IBM watsonx Embeddings            │
└──────────────────────────────────────────────────────────────────────────┘
```

---

# SLIDE 5: IBM Cloud Platform Usage

## watsonx.ai Integration

### IBM Granite Model Configuration (from our LangFlow):

| Parameter | Value |
|-----------|-------|
| **Model** | ibm/granite-3-8b-instruct |
| **API Endpoint** | https://eu-gb.ml.cloud.ibm.com |
| **Max Tokens** | 1500 |
| **Temperature** | 0.21 (low for factual responses) |
| **Top P** | 0.9 |
| **Frequency Penalty** | 0.5 |
| **Presence Penalty** | 0.3 |

### System Message (actual from our flow):
```
You are an expert Bangalore Traffic Analysis AI assistant. 
You MUST follow these rules strictly:

1. ONLY respond to queries about Bangalore (Bengaluru), India traffic
2. REJECT any queries about other cities immediately with a polite message
3. Be concise and factual - no rambling or unnecessary elaboration
4. Use data from the provided context only - never invent statistics
5. Always mention data limitations and disclaimers when relevant
6. Respond in clear, structured markdown format
7. Activate only relevant analysis agents based on query type
8. Maintain professional but friendly tone
```

### IBM watsonx Embeddings:
- Used in **Embedding Model** components for vectorizing knowledge base
- Powers semantic search in AstraDB

---

# SLIDE 6: LangFlow Implementation

## Flow Components (from New Flow.json)

### Components Used:

| Component ID | Type | Purpose |
|--------------|------|---------|
| ChatInput-56yO0 | Chat Input | Receives operator queries |
| AstraDB-VCcYf | AstraDB | Ingests documents into vector store |
| AstraDB-A0R5g | AstraDB | Searches knowledge base |
| EmbeddingModel-vgkry | Embedding | Vectorizes documents for ingestion |
| EmbeddingModel-Spsnj | Embedding | Vectorizes queries for search |
| SplitText-z8cB4 | Split Text | Chunks documents for embedding |
| File-OIo6L | File Loader | Loads knowledge base documents |
| ParserComponent-oSlEl | Parser | Processes search results |
| Prompt Template-HTWIJ | Prompt | Contains 3-agent behavior logic |
| IBMwatsonxModel-HyB5s | IBM watsonx | Granite model for inference |
| ChatOutput-kPg0c | Chat Output | Returns response to user |

### Data Flow:
```
Document Ingestion:
File → SplitText → Embeddings → AstraDB (Store)

Query Processing:
Chat Input → AstraDB (Search) → Parser → Prompt Template → IBM Granite → Chat Output
     │                                          ▲
     └──────────────────────────────────────────┘
                    (Question)
```

---

# SLIDE 7: The 3-Agent System (via Prompt Engineering)

## How Query Routing Works

Our prompt template dynamically activates agent behaviors based on query type:

| Query Type | Agent 1 (Data) | Agent 2 (Causes) | Agent 3 (Explain) |
|------------|----------------|------------------|-------------------|
| "Which areas to avoid?" | ✅ Yes | ❌ No | ✅ Yes |
| "Why is X congested?" | ❌ No | ✅ Yes | ✅ Yes |
| "How does weather affect?" | ❌ No | ✅ Yes | ✅ Yes |
| "Traffic status in X" | ✅ Yes | ✅ Yes | ❌ No |
| "Best route from A to B" | ✅ Yes | ❌ No | ✅ Yes |

### Agent 1: Traffic Data Analysis
**Behavior:** Synthesizes traffic data into actionable summaries

**Outputs:**
- Traffic speed (km/h)
- Congestion level (Light/Moderate/Heavy/Severe)
- Road capacity utilization (%)
- Comparison to historical averages

---

### Agent 2: Congestion Cause Analysis
**Behavior:** Identifies WHY congestion is happening

**Correlation Factors (from knowledge base):**
- **Time of Day:** Morning peak (8:00-9:30 AM), Evening peak (6:00-7:30 PM)
- **Weather:** Rain reduces capacity 15-25%, Fog reduces 20-35%
- **Incidents:** 1 lane blocked = 30-75% capacity reduction
- **Volume:** Special events, holidays, end-of-month

**Outputs:**
- Primary cause with confidence percentage
- Contributing factors with impact levels
- Pattern type (Recurring vs Non-recurring)

---

### Agent 3: Explainable Insight Assistant
**Behavior:** Generates human-readable explanations

**Key Features:**
- Plain language summaries
- Confidence scores based on data availability
- Source citations from RAG knowledge base
- Actionable recommendations

---

# SLIDE 8: RAG Knowledge Base

## Knowledge Documents (from data/knowledge_base/)

### 1. traffic_congestion_classification.txt
**Content:**
- Congestion levels: Light (0-30%), Moderate (30-60%), Heavy (60-85%), Severe (85-100%)
- Travel Time Index (TTI) definitions
- Road capacity utilization guidelines
- Congestion duration patterns

### 2. weather_impact_guidelines.txt
**Content:**
- Clear weather: 0% speed reduction
- Light Rain: 10-15% speed reduction, 5-10% capacity reduction
- Heavy Rain: 25-40% speed reduction, 15-25% capacity reduction
- Fog: 30-50% speed reduction, 20-35% capacity reduction
- Monsoon season patterns (June-September)

### 3. incident_management_guidelines.txt
**Content:**
- Incident types: Accidents, Breakdowns, Roadwork, Events
- Clearance times: Minor (15-30 min), Moderate (30-60 min), Severe (1-3 hours)
- Capacity reduction formulas per blocked lane
- Incident severity classification (Level 1-4)

### 4. time_patterns_analysis.txt
**Content:**
- Morning Peak: 7:00-10:30 AM (peak intensity 8:00-9:30 AM)
- Evening Peak: 5:00-8:30 PM (peak intensity 6:00-7:30 PM)
- Weekday vs Weekend patterns
- Bangalore IT corridor shift timings

### 5. bangalore_urban_mobility.txt
**Content:**
- City profile: 13 million population, 10 million vehicles
- Area-specific characteristics (Indiranagar, Koramangala, Whitefield, etc.)
- Road hierarchy and major corridors
- Congestion drivers per area

---

# SLIDE 9: Traffic Data

## Dataset Statistics (from data/processed/dataset_statistics.json)

| Metric | Value |
|--------|-------|
| **Total Records** | 8,936 |
| **Date Range** | January 1, 2022 - August 9, 2024 |
| **Areas Covered** | 8 |
| **Roads Covered** | 16 |
| **Overall Avg Congestion** | 80.82% |

### Areas Covered:
1. Indiranagar (100 Feet Road, CMH Road)
2. Whitefield (Marathahalli Bridge, ITPL Main Road)
3. Koramangala
4. M.G. Road
5. Jayanagar
6. Hebbal
7. Yeshwanthpur
8. Electronic City

### Congestion Distribution:
| Level | Records | Percentage |
|-------|---------|------------|
| Severe | 5,110 | 57.2% |
| Heavy | 1,879 | 21.0% |
| Moderate | 1,609 | 18.0% |
| Light | 338 | 3.8% |

### Weather Distribution:
| Condition | Records |
|-----------|---------|
| Clear | 5,426 |
| Overcast | 1,296 |
| Fog | 959 |
| Rain | 827 |
| Windy | 428 |

### Example Area Data (Indiranagar):
- Total Records: 1,720
- Average Congestion: 87.64%
- Average Speed: 38.64 km/h
- Total Incidents: 3,057
- Severe Congestion Days: 1,167

---

# SLIDE 10: Demo Scenarios

## Test Query 1: Traffic Status

**User:** "What is the traffic situation in Koramangala?"

**Expected Response:**
```
## 🚦 TRAFFIC ANALYSIS (Agent 1)

| Area | Status | Speed | Utilization |
|------|--------|-------|-------------|
| Koramangala | Heavy | 35 km/h | 78% |

## 💡 EXPLANATION (Agent 3)

**Summary:** Koramangala is experiencing heavy traffic typical for 
this time of day due to IT office commute patterns and high 
commercial activity around Sony World Junction.

**Recommendation:** Consider using Inner Ring Road or 
HSR Layout as alternatives.

## 📈 CONFIDENCE: High
Reason: Area has comprehensive historical data

## ⚠️ DISCLAIMER
ℹ️ Based on historical data patterns (2022-2024), not real-time.
```

---

## Test Query 2: Cause Analysis

**User:** "Why is Silk Board always congested?"

**Expected Response:**
```
## 🔍 CONGESTION CAUSES (Agent 2)

**Primary Cause:** Junction bottleneck - Confidence: 92%

**Contributing Factors:**
1. IT corridor intersection → Impact: High
   (Electronic City, HSR, Koramangala traffic converges)
2. Limited alternate routes → Impact: High
3. Peak hour volume exceeding capacity → Impact: High
4. Signal timing constraints → Impact: Medium

**Pattern Type:** Recurring (daily weekday pattern)

## 💡 EXPLANATION (Agent 3)

**Summary:** Silk Board Junction is Bangalore's busiest intersection 
where multiple IT corridors meet. The junction handles traffic from 
Electronic City, Koramangala, and HSR Layout simultaneously, 
creating consistent bottlenecks during office hours.

## 📈 CONFIDENCE: High

## ⚠️ DISCLAIMER
Based on historical patterns (2022-2024).
```

---

## Test Query 3: Weather Impact

**User:** "How does rain affect traffic in Bangalore?"

**Expected Response:**
```
## 🔍 CONGESTION CAUSES (Agent 2)

**Weather Impact Analysis:**

| Condition | Speed Reduction | Capacity Reduction |
|-----------|-----------------|-------------------|
| Light Rain | 10-15% | 5-10% |
| Heavy Rain | 25-40% | 15-25% |

**Key Factors:**
1. First rain after dry spell → 20-30% incident increase
2. Waterlogging in low-lying areas
3. Reduced visibility → larger vehicle gaps
4. Monsoon season (June-Sept) → 30-40% higher incidents

## 💡 EXPLANATION (Agent 3)

**Summary:** Rain significantly impacts Bangalore traffic. Light 
rain reduces speeds by 10-15%, while heavy rain can reduce 
capacity by up to 25%. The "first rain effect" after dry spells 
is particularly dangerous due to oil and dust on roads.

## 📈 CONFIDENCE: High
Reason: Based on weather-traffic correlation data

## ⚠️ DISCLAIMER
🌧️ Weather patterns are historical averages (2022-2024).
```

---

## Test Query 4: Other City Rejection

**User:** "How is traffic in Chennai?"

**Expected Response:**
```
🚫 I specialize in Bangalore (Bengaluru) traffic analysis only.
I cannot provide information about Chennai traffic.

I cover these Bangalore areas:
Indiranagar, Whitefield, Koramangala, M.G. Road, Jayanagar, 
Hebbal, Yeshwanthpur, Electronic City

How can I help you with Bangalore traffic today?
```

---

# SLIDE 11: Societal Benefits

## Impact on Society

### For Traffic Operators:
| Benefit | Details |
|---------|---------|
| **Faster Decisions** | Instant analysis instead of manual cross-referencing |
| **Increased Trust** | Explainable AI = Confident action on recommendations |
| **Better Resource Allocation** | Know WHERE and WHY to deploy traffic police |

### For Citizens:
| Benefit | Details |
|---------|---------|
| **Reduced Commute Time** | Better traffic management = smoother flow |
| **Improved Safety** | Faster incident response through AI insights |
| **Reliable Journey Planning** | Operators can provide accurate advisories |

### For City Administration:
| Benefit | Details |
|---------|---------|
| **Data-Driven Infrastructure** | AI identifies chronic problem areas |
| **Pattern Recognition** | Understand recurring vs one-time issues |
| **Evidence-Based Budgeting** | Justify traffic investments with data |

### For Environment:
| Benefit | Details |
|---------|---------|
| **Lower Emissions** | Less time idling in traffic |
| **Fuel Savings** | Optimized routing reduces fuel consumption |

---

# SLIDE 12: Scalability & Innovation

## Why This Architecture Scales

### Current Implementation:
- 1 City (Bangalore)
- 8 Areas with detailed data
- 5 Knowledge documents
- Single model with 3-agent behaviors

### Scalable Design:
```
Current                          Future
───────                          ──────
1 City          ───────▶        Pan-India (100+ cities)
8 Areas         ───────▶        City-wide coverage
5 KB Documents  ───────▶        Dynamic knowledge updates
3 Agents        ───────▶        Extensible agent behaviors
```

### Innovation Highlights:

1. **Explainability-First Design**
   - Every response includes WHY, not just WHAT
   - Confidence scores build operator trust
   - Source citations prevent hallucinations

2. **Efficient Multi-Agent via Prompting**
   - Single model = Lower cost, faster response
   - Dynamic agent activation based on query
   - Industry-standard prompt engineering

3. **RAG-Powered Accuracy**
   - Responses grounded in real knowledge base
   - No invented statistics
   - Transparent data limitations

4. **City-Agnostic Architecture**
   - Same flow works for any city
   - Just update knowledge base and data
   - Modular component design

---

# SLIDE 13: Commercial Viability

## Business Model

### Target Market:
| Segment | Potential | Need |
|---------|-----------|------|
| **Traffic Control Centers** | 500+ in India | Real-time decision support |
| **Smart City Projects** | 100+ cities | AI-powered traffic management |
| **State Transport Departments** | 28 states + 8 UTs | Policy planning tools |
| **Municipal Corporations** | 4,000+ | Urban traffic management |

### Revenue Model (SaaS):

| Tier | Features | Price (Indicative) |
|------|----------|-------------------|
| **Starter** | Single area, 5 users | ₹25,000/month |
| **Professional** | Multi-area, 20 users, API access | ₹1,00,000/month |
| **Enterprise** | City-wide, unlimited users, custom training | Custom pricing |

### Competitive Advantage:
- **Only solution with built-in explainability**
- IBM Granite = Enterprise-grade, trusted AI
- Cloud-native = Pay-per-use, scalable
- LangFlow = Rapid customization without coding

---

# SLIDE 14: Future Scope

## Development Roadmap

### Phase 1: Current (MVP) ✅
- Single IBM Granite model with 3-agent prompt
- Bangalore coverage (8 areas)
- Historical data analysis (2022-2024)
- LangFlow + AstraDB RAG pipeline

### Phase 2: Q2 2026
- [ ] Real-time data integration (Google Maps API, traffic sensors)
- [ ] Predictive congestion alerts (30-60 min ahead)
- [ ] Mobile app for field operators
- [ ] Expand to 5 more Bangalore areas

### Phase 3: Q4 2026
- [ ] Multi-city expansion (Chennai, Hyderabad, Mumbai)
- [ ] Integration with traffic signal control systems
- [ ] Automated incident detection from CCTV feeds
- [ ] Fine-tuned Granite model for traffic domain

### Phase 4: 2027
- [ ] Pan-India coverage
- [ ] Autonomous traffic management recommendations
- [ ] Integration with emergency services (police, ambulance)
- [ ] Citizen-facing traffic advisory app

---

# SLIDE 15: Technology Summary

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **AI Model** | IBM Granite 3-8b-instruct | Core reasoning & generation |
| **AI Platform** | IBM watsonx.ai | Model hosting & inference |
| **Orchestration** | DataStax LangFlow | Visual flow building |
| **Vector Store** | AstraDB | RAG knowledge storage |
| **Embeddings** | IBM watsonx Embeddings | Text vectorization |
| **Data Processing** | Python (Pandas) | ETL pipeline |
| **Data Format** | JSON, CSV | Structured data storage |

### Key Technical Decisions:

| Decision | Rationale |
|----------|-----------|
| Single model with multi-agent prompt | Cost-effective, faster, coherent output |
| RAG over fine-tuning | No training needed, easy knowledge updates |
| LangFlow for orchestration | Visual, no-code, rapid iteration |
| AstraDB for vectors | Scalable, DataStax integration |

---

# SLIDE 16: Judging Criteria Alignment

## How We Meet Each Criterion

### 1. IBM Cloud Platform Usage (5 marks) ✅
- IBM Granite Model (ibm/granite-3-8b-instruct)
- watsonx.ai for model inference
- IBM watsonx Embeddings for vectorization
- Deployed on LangFlow (IBM partner)

### 2. Scalability & Innovativeness (5 marks) ✅
- Multi-agent behavior via single model (innovative)
- RAG architecture for extensibility
- City-agnostic design
- Modular component architecture

### 3. Societal Benefit (5 marks) ✅
- Reduces operator decision time
- Improves traffic management effectiveness
- Enhances public safety through better incident response
- Increases AI transparency and trust

### 4. Deployment Readiness (5 marks) ✅
- Working end-to-end demo on LangFlow
- Complete documentation
- Reproducible setup (flow JSON available)
- Graceful handling of out-of-scope queries

### 5. Commercial Viability (5 marks) ✅
- Clear value proposition (explainability)
- Target market identified (traffic control centers)
- SaaS pricing model
- Competitive advantage (only explainable traffic AI)

### 6. Future Scope (5 marks) ✅
- Phased roadmap through 2027
- Integration possibilities (Google Maps, CCTV, signals)
- Multi-city expansion plan
- AI model improvement path

---

# SLIDE 17: Conclusion

## Key Takeaways

### What We Built:
> An **Explainable AI system** that tells traffic operators not just WHAT is happening, but **WHY it's happening** and **WHAT to do about it**.

### Technical Innovation:
> **Single IBM Granite model** with intelligent prompt engineering that simulates **3 specialized agent behaviors** - proving that efficiency and capability can coexist.

### Real Impact:
> Making AI **transparent and trustworthy** for critical infrastructure decisions, enabling operators to act confidently on AI recommendations.

### Built With:
- 🔷 **IBM Granite** - Enterprise AI reasoning
- 🔷 **LangFlow** - Visual orchestration
- 🔷 **AstraDB** - Scalable vector storage
- 🔷 **watsonx.ai** - IBM Cloud AI platform

---

# SLIDE 18: Thank You

## Thank You!

### Team: [Your Team Name]

### Team Members:
- [Member 1 - Role]
- [Member 2 - Role]
- [Member 3 - Role]

### Contact:
- Email: [team@email.com]
- GitHub: [repository-url]

### Demo:
Available on DataStax LangFlow

---

# APPENDIX A: Prompt Template (Actual from Flow)

## Complete 3-Agent Prompt

```
You are a Bangalore Traffic AI System with 3 specialized agents.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 QUERY TYPE HANDLING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. GENERAL BANGALORE QUESTIONS (Not about traffic):
   → Reply briefly about city + offer traffic help

2. OTHER CITIES (Chennai, Mumbai, Texas, etc.):
   → Reject: "🚫 I specialize in Bangalore traffic only."

3. BANGALORE TRAFFIC QUESTIONS:
   → Proceed with full agent analysis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 BANGALORE AREAS I COVER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Indiranagar, Whitefield, Koramangala, M.G. Road, Jayanagar, 
Hebbal, Yeshwanthpur, Electronic City

+ All other Bangalore areas (general patterns)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 - QUERY TYPE DETECTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Query Type              | Agent 1 | Agent 2 | Agent 3 |
|-------------------------|---------|---------|---------|
| "Which areas to avoid?" | ✅ Yes  | ❌ No   | ✅ Yes  |
| "Why is X congested?"   | ❌ No   | ✅ Yes  | ✅ Yes  |
| "Traffic status in X"   | ✅ Yes  | ✅ Yes  | ❌ No   |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ LIMITATIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- DATA PERIOD: Historical data from 2022-2024
- NOT REAL-TIME: Cannot access live traffic
- COVERAGE: Bangalore metropolitan area only
- ESTIMATES: Numbers are averages, actual may vary

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER QUESTION:
{question}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPONSE FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚦 TRAFFIC ANALYSIS (Agent 1)
[Only if activated]

## 🔍 CONGESTION CAUSES (Agent 2)
[Only if activated]

## 💡 EXPLANATION (Agent 3)
[Summary + Recommendation]

## 📈 CONFIDENCE: [High/Medium/Low]

## ⚠️ DISCLAIMER
[Appropriate disclaimer based on query type]
```

---

# APPENDIX B: LangFlow Component Details

## Component Configuration

### IBM watsonx Model (IBMwatsonxModel-HyB5s)
```
Model: ibm/granite-3-8b-instruct
Endpoint: https://eu-gb.ml.cloud.ibm.com
Max Tokens: 1500
Temperature: 0.21
Top P: 0.9
Frequency Penalty: 0.5
Presence Penalty: 0.3
Seed: 8
```

### AstraDB Vector Store
```
Collection: traffic_knowledge
Embedding: IBM watsonx Embeddings
Search: Semantic similarity
```

### Data Flow Connections:
```
1. Chat Input → AstraDB Search (query)
2. Chat Input → Prompt Template (question)
3. AstraDB Search → Parser
4. Parser → Prompt Template (context)
5. Prompt Template → IBM Granite
6. IBM Granite → Chat Output
```

---

# APPENDIX C: Screenshots to Include

1. **LangFlow Canvas** - Full flow view showing all components connected
2. **IBM watsonx Component** - Configuration panel showing Granite model settings
3. **Prompt Template** - Showing the 3-agent behavior configuration
4. **AstraDB Component** - Vector store configuration
5. **Chat Interface** - Sample query and response demonstration

---

# APPENDIX D: Presentation Timing Guide

## For 10-Minute Presentation:

| Slide | Duration | Key Points |
|-------|----------|------------|
| Title | 0:30 | Team intro |
| Problem | 1:00 | Why operators need explainability |
| Solution | 1:00 | Single model, 3-agent concept |
| Architecture | 1:00 | LangFlow flow overview |
| IBM Cloud | 0:45 | Granite model, watsonx.ai |
| 3 Agents | 1:00 | How agent routing works |
| Demo | 2:00 | Live queries (2-3 examples) |
| Benefits | 0:30 | Societal impact |
| Future | 0:30 | Roadmap |
| Conclusion | 0:45 | Key takeaways |
| Q&A | 1:00+ | Answer questions |

**Total: ~10 minutes + Q&A**

---

# APPENDIX E: Design Recommendations

## Color Scheme:
- **Primary:** IBM Blue (#0043CE)
- **Accent:** Traffic Green (#00B050), Amber (#FFC000), Red (#FF0000)
- **Background:** White or Light Gray

## Icons to Use:
- 🚦 Traffic signals
- 🚗 Vehicles
- 🌧️ Weather
- 📊 Data/Analytics
- 🤖 AI/Robot
- 💡 Insights
- ⚠️ Warnings

## Fonts:
- Headings: IBM Plex Sans Bold (or similar sans-serif)
- Body: IBM Plex Sans Regular

---

*Document prepared for IBM Hackathon 2026*
*Last Updated: January 28, 2026*
*Based on actual project files and LangFlow configuration*
