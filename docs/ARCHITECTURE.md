# System Architecture

## Document Information
| Field | Value |
|-------|-------|
| Project | Agentic AI System for Explainable Traffic Congestion Analysis |
| Version | 1.0 |
| Last Updated | January 27, 2026 |

---

## 1. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              USER LAYER                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    Traffic Operator Dashboard                            │ │
│  │            (Web Interface / Chat Interface)                              │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATION LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                         LANGFLOW ENGINE                                  │ │
│  │                                                                          │ │
│  │   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐               │ │
│  │   │    Input     │──▶│   Router     │──▶│   Output     │               │ │
│  │   │   Parser     │   │   Agent      │   │  Formatter   │               │ │
│  │   └──────────────┘   └──────────────┘   └──────────────┘               │ │
│  │                             │                                            │ │
│  │         ┌───────────────────┼───────────────────┐                       │ │
│  │         ▼                   ▼                   ▼                       │ │
│  │   ┌───────────┐      ┌───────────┐      ┌───────────┐                  │ │
│  │   │  Traffic  │      │ Congestion│      │Explainable│                  │ │
│  │   │   Data    │      │   Cause   │      │  Insight  │                  │ │
│  │   │  Agent    │      │   Agent   │      │ Assistant │                  │ │
│  │   └───────────┘      └───────────┘      └───────────┘                  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           AI/ML LAYER                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    IBM watsonx.ai Studio                                 │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                     IBM GRANITE MODEL                              │ │ │
│  │  │                                                                    │ │ │
│  │  │   • Natural Language Understanding                                 │ │ │
│  │  │   • Reasoning & Analysis                                           │ │ │
│  │  │   • Text Generation                                                │ │ │
│  │  │   • Summarization                                                  │ │ │
│  │  └────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         KNOWLEDGE LAYER                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    RAG (Retrieval Augmented Generation)                  │ │
│  │                                                                          │ │
│  │   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐       │ │
│  │   │    Vector      │    │    Document    │    │   Retrieval    │       │ │
│  │   │    Store       │◀──│    Embeddings  │    │    Engine      │       │ │
│  │   └────────────────┘    └────────────────┘    └────────────────┘       │ │
│  │                                                                          │ │
│  │   Knowledge Base:                                                        │ │
│  │   • Traffic Engineering Standards                                        │ │
│  │   • Urban Mobility Frameworks                                            │ │
│  │   • Congestion Management Guidelines                                     │ │
│  │   • Case Studies & Best Practices                                        │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │
│  │  Traffic      │  │   Weather     │  │   Incident    │  │  Historical   │ │
│  │  Sensors      │  │   Data API    │  │   Reports     │  │   Archives    │ │
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘ │
│                                                                               │
│                    ┌─────────────────────────────────────┐                   │
│                    │    IBM Cloud Object Storage         │                   │
│                    └─────────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Agent Architecture

### 2.1 Traffic Data Analysis Agent

```
┌─────────────────────────────────────────────────────────────────┐
│                 TRAFFIC DATA ANALYSIS AGENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INPUT                                                           │
│  ├── Traffic sensor data (volume, speed, occupancy)             │
│  ├── GPS/probe data                                              │
│  └── Historical baseline data                                    │
│                                                                  │
│  PROCESSING                                                      │
│  ├── Data normalization & validation                            │
│  ├── Multi-source fusion                                         │
│  ├── Pattern detection                                           │
│  └── Statistical analysis                                        │
│                                                                  │
│  OUTPUT                                                          │
│  ├── Traffic summary report                                      │
│  ├── Congestion level indicators                                 │
│  ├── Anomaly flags                                               │
│  └── Trend metrics                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Congestion Cause Analysis Agent

```
┌─────────────────────────────────────────────────────────────────┐
│              CONGESTION CAUSE ANALYSIS AGENT                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INPUT                                                           │
│  ├── Traffic summary (from Agent 1)                             │
│  ├── Weather conditions                                          │
│  ├── Incident reports                                            │
│  └── Time/date context                                           │
│                                                                  │
│  ANALYSIS DIMENSIONS                                             │
│  ├── Temporal: Time-of-day, day-of-week, seasonality            │
│  ├── Weather: Rain, fog, snow, temperature extremes             │
│  ├── Incidents: Accidents, construction, events                 │
│  └── Demand: Volume spikes, special events, holidays            │
│                                                                  │
│  OUTPUT                                                          │
│  ├── Primary cause identification                                │
│  ├── Contributing factors list                                   │
│  ├── Confidence scores                                           │
│  └── Historical pattern matches                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Explainable Insight Assistant

```
┌─────────────────────────────────────────────────────────────────┐
│               EXPLAINABLE INSIGHT ASSISTANT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INPUT                                                           │
│  ├── Cause analysis results (from Agent 2)                      │
│  ├── Operator query/question                                     │
│  └── RAG context (retrieved documents)                          │
│                                                                  │
│  GENERATION COMPONENTS                                           │
│  ├── Explanation Builder                                         │
│  │   ├── Cause narrative                                         │
│  │   ├── Evidence synthesis                                      │
│  │   └── Confidence framing                                      │
│  ├── Citation Engine                                             │
│  │   └── Source attribution                                      │
│  └── Recommendation Engine                                       │
│      └── Actionable suggestions                                  │
│                                                                  │
│  OUTPUT                                                          │
│  ├── Human-readable explanation                                  │
│  ├── Supporting evidence with citations                         │
│  ├── Confidence level                                            │
│  └── Recommended actions (optional)                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. LangFlow Workflow Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LANGFLOW WORKFLOW                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [User Input]                                                                │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────┐                                                            │
│  │   Prompt    │  "Why is there congestion on Highway 101?"                 │
│  │   Input     │                                                            │
│  └──────┬──────┘                                                            │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────┐     ┌──────────────┐                                       │
│  │   Intent    │────▶│   Context    │  Determine what data is needed       │
│  │   Analyzer  │     │   Gatherer   │                                       │
│  └─────────────┘     └──────┬───────┘                                       │
│                             │                                                │
│         ┌───────────────────┼───────────────────┐                           │
│         ▼                   ▼                   ▼                           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   │
│  │  Traffic    │     │  Weather    │     │  Incident   │                   │
│  │  Data Tool  │     │  Data Tool  │     │  Data Tool  │                   │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘                   │
│         │                   │                   │                           │
│         └───────────────────┼───────────────────┘                           │
│                             ▼                                                │
│                      ┌─────────────┐                                        │
│                      │   Traffic   │  Synthesize traffic state             │
│                      │   Analyst   │                                        │
│                      └──────┬──────┘                                        │
│                             │                                                │
│                             ▼                                                │
│                      ┌─────────────┐                                        │
│                      │  Cause      │  Correlate factors                    │
│                      │  Analyzer   │                                        │
│                      └──────┬──────┘                                        │
│                             │                                                │
│                             ▼                                                │
│                      ┌─────────────┐     ┌──────────────┐                  │
│                      │  RAG        │◀───▶│  Vector DB   │                  │
│                      │  Retriever  │     │  (Knowledge) │                  │
│                      └──────┬──────┘     └──────────────┘                  │
│                             │                                                │
│                             ▼                                                │
│                      ┌─────────────┐                                        │
│                      │ Explanation │  Generate human-readable output       │
│                      │  Generator  │                                        │
│                      └──────┬──────┘                                        │
│                             │                                                │
│                             ▼                                                │
│                      ┌─────────────┐                                        │
│                      │  Response   │  Format final response                │
│                      │  Formatter  │                                        │
│                      └──────┬──────┘                                        │
│                             │                                                │
│                             ▼                                                │
│                       [User Output]                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW                                          │
└─────────────────────────────────────────────────────────────────────────────┘

                    INGESTION              PROCESSING            OUTPUT
                    ─────────              ──────────            ──────

Traffic Sensors ──┐
                  │    ┌──────────────┐    ┌──────────────┐
Weather APIs ─────┼───▶│    Data      │───▶│   Traffic    │
                  │    │  Ingestion   │    │   Analysis   │
Incident Feed ────┤    │   Layer      │    │    Agent     │
                  │    └──────────────┘    └──────┬───────┘
Historical DB ────┘                               │
                                                  │
                                                  ▼
                                         ┌──────────────┐
                                         │  Congestion  │
                                         │    Cause     │
                                         │   Analysis   │
                                         └──────┬───────┘
                                                │
                    ┌───────────────────────────┤
                    │                           │
                    ▼                           ▼
           ┌──────────────┐            ┌──────────────┐
           │     RAG      │            │  Explanation │
           │  Knowledge   │───────────▶│   Engine     │
           │    Base      │            │              │
           └──────────────┘            └──────┬───────┘
                                              │
                                              ▼
                                      ┌──────────────┐
                                      │    User      │
                                      │  Interface   │
                                      └──────────────┘
```

---

## 5. IBM Cloud Service Mapping

| Component | IBM Cloud Service | Purpose |
|-----------|-------------------|---------|
| AI Model | watsonx.ai (Granite) | Core LLM for reasoning and generation |
| Orchestration | LangFlow on IBM Cloud | Agent workflow management |
| Vector Store | watsonx.ai Embeddings | RAG document embeddings |
| Data Storage | IBM Cloud Object Storage | Traffic data and documents |
| Compute | IBM Cloud Kubernetes / Code Engine | Application hosting |
| API Gateway | IBM API Connect (optional) | API management |

---

## 6. Sequence Diagram - User Query Flow

```
User          LangFlow        TrafficAgent    CauseAgent    InsightAgent    RAG           Granite
 │               │                 │              │              │           │               │
 │  Query        │                 │              │              │           │               │
 │──────────────▶│                 │              │              │           │               │
 │               │  Get Traffic    │              │              │           │               │
 │               │────────────────▶│              │              │           │               │
 │               │                 │  Analyze     │              │           │               │
 │               │                 │─────────────────────────────────────────────────────────▶│
 │               │                 │              │              │           │    Summary    │
 │               │                 │◀─────────────────────────────────────────────────────────│
 │               │  Traffic Summary│              │              │           │               │
 │               │◀────────────────│              │              │           │               │
 │               │                 │              │              │           │               │
 │               │  Analyze Causes │              │              │           │               │
 │               │────────────────────────────────▶│              │           │               │
 │               │                 │              │  Correlate   │           │               │
 │               │                 │              │─────────────────────────────────────────▶│
 │               │                 │              │              │           │    Causes    │
 │               │                 │              │◀─────────────────────────────────────────│
 │               │  Cause Analysis │              │              │           │               │
 │               │◀────────────────────────────────│              │           │               │
 │               │                 │              │              │           │               │
 │               │  Retrieve Context              │              │           │               │
 │               │───────────────────────────────────────────────────────────▶│               │
 │               │                 │              │              │  Context  │               │
 │               │◀───────────────────────────────────────────────────────────│               │
 │               │                 │              │              │           │               │
 │               │  Generate Explanation          │              │           │               │
 │               │────────────────────────────────────────────────▶│           │               │
 │               │                 │              │              │  Explain  │               │
 │               │                 │              │              │──────────────────────────▶│
 │               │                 │              │              │           │  Explanation │
 │               │                 │              │              │◀──────────────────────────│
 │               │  Final Response │              │              │           │               │
 │               │◀────────────────────────────────────────────────│           │               │
 │  Explanation  │                 │              │              │           │               │
 │◀──────────────│                 │              │              │           │               │
 │               │                 │              │              │           │               │
```

---

## 7. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         IBM CLOUD DEPLOYMENT                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│    ┌─────────────────────────────────────────────────────────────────────┐  │
│    │                        IBM Cloud Region                              │  │
│    │                                                                      │  │
│    │   ┌─────────────────┐         ┌─────────────────┐                   │  │
│    │   │   Code Engine   │         │  watsonx.ai     │                   │  │
│    │   │   / Kubernetes  │◀───────▶│  Runtime        │                   │  │
│    │   │                 │         │                 │                   │  │
│    │   │  ┌───────────┐  │         │  ┌───────────┐  │                   │  │
│    │   │  │ LangFlow  │  │         │  │  Granite  │  │                   │  │
│    │   │  │   App     │  │         │  │  Model    │  │                   │  │
│    │   │  └───────────┘  │         │  └───────────┘  │                   │  │
│    │   └─────────────────┘         └─────────────────┘                   │  │
│    │            │                           │                             │  │
│    │            │                           │                             │  │
│    │            ▼                           ▼                             │  │
│    │   ┌─────────────────────────────────────────────┐                   │  │
│    │   │           IBM Cloud Object Storage          │                   │  │
│    │   │                                             │                   │  │
│    │   │   ┌──────────┐   ┌──────────┐   ┌────────┐ │                   │  │
│    │   │   │ Traffic  │   │Knowledge │   │  Logs  │ │                   │  │
│    │   │   │  Data    │   │  Base    │   │        │ │                   │  │
│    │   │   └──────────┘   └──────────┘   └────────┘ │                   │  │
│    │   └─────────────────────────────────────────────┘                   │  │
│    │                                                                      │  │
│    └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-27 | Team | Initial architecture |
