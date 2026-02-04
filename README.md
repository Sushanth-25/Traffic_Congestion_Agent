# Agentic AI System for Explainable Traffic Congestion Analysis

## 🚦 Overview

An explainable AI-powered traffic congestion analysis system built using **IBM Granite Model** and **LangFlow**. This system enhances transparency, trust, and usability of AI-driven traffic insights by providing human-readable explanations for congestion causes and patterns.

## 🎯 Problem Statement

Traffic operators often receive congestion alerts without sufficient explanation of underlying causes. This limits trust and effective decision-making. Our solution provides an explainable AI system that:
- Detects congestion patterns
- Explains contributing factors
- Provides interpretable insights derived from traffic data

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                                │
│                    (Traffic Operator Dashboard)                      │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     LANGFLOW ORCHESTRATION                           │
│                    (IBM Granite Model Core)                          │
└─────────────────────────────────────────────────────────────────────┘
           │                       │                       │
           ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  Traffic Data   │   │ Congestion Cause│   │   Explainable   │
│ Analysis Agent  │   │  Analysis Agent │   │ Insight Assistant│
└─────────────────┘   └─────────────────┘   └─────────────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     RAG KNOWLEDGE BASE                               │
│     (Traffic Engineering Literature & Urban Mobility Frameworks)     │
└─────────────────────────────────────────────────────────────────────┘
```

## 🤖 AI Agents

| Agent | Purpose |
|-------|---------|
| **Traffic Data Analysis Agent** | Synthesizes traffic data from multiple sources into comprehensive summaries |
| **Congestion Cause Analysis Agent** | Correlates congestion patterns with time-of-day, incidents, weather, and volume changes |
| **Explainable Insight Assistant** | Generates human-readable explanations for congestion causes and trends |

## 🛠️ Tech Stack

- **AI Model**: IBM Granite (via watsonx.ai)
- **Orchestration**: LangFlow
- **RAG**: Traffic engineering literature & urban mobility frameworks
- **Cloud Platform**: IBM Cloud
# Traffic AI Assistant - IBM Hackathon

An intelligent traffic congestion analysis system built with IBM watsonx.ai and Langflow.

## 🏗️ Architecture

This project consists of:
- **Frontend**: Interactive web interface for user queries
- **Langflow**: AI agent workflow for traffic analysis
- **Data**: Traffic datasets and knowledge base

## 🚀 Setup Instructions

### Prerequisites
- IBM Cloud account
- Langflow instance on DataStax Astra
- Modern web browser

### Frontend Configuration

1. Navigate to the `Frontend` directory
2. Copy `config.example.js` to `config.js`:
   ```bash
   cp Frontend/config.example.js Frontend/config.js
   ```

3. Edit `Frontend/config.js` with your credentials:
   - `apiUrl`: Your Langflow API endpoint
   - `flowId`: Your flow ID from Langflow
   - `applicationToken`: Generate from Langflow Settings → API Keys
   - `organizationId`: Your DataStax organization ID

### Running the Application

1. Start a local server:
   ```bash
   python -m http.server 8000
   ```

2. Open your browser to `http://localhost:8000`

3. Start chatting with the Traffic AI Assistant!

## 📁 Project Structure

```
IBM_Hackathon/
├── docs/
│   ├── REQUIREMENTS.md          # Detailed requirements
│   ├── OBJECTIVES.md            # Project objectives & success criteria
│   ├── ARCHITECTURE.md          # System architecture details
│   └── API_REFERENCE.md         # API documentation
├── src/
│   ├── agents/                  # AI Agent implementations
│   ├── rag/                     # RAG pipeline components
│   ├── data/                    # Data processing modules
│   └── utils/                   # Utility functions
├── langflow/
│   └── flows/                   # LangFlow flow definitions
├── data/
│   ├── raw/                     # Raw traffic data
│   ├── processed/               # Processed datasets
│   └── knowledge_base/          # RAG documents
├── tests/                       # Test cases
├── deployment/                  # Deployment configurations
├── presentation/                # PPT and demo materials
└── README.md
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd IBM_Hackathon

# Install dependencies
pip install -r requirements.txt

# Set up IBM Cloud credentials
cp .env.example .env
# Edit .env with your IBM Cloud API keys

# Run the application
python src/main.py
```

## 📖 Documentation

- [Requirements](docs/REQUIREMENTS.md)
- [Objectives](docs/OBJECTIVES.md)
- [Architecture](docs/ARCHITECTURE.md)

## 👥 Team

- Team Member 1 (Team Lead)
- Team Member 2 
- Team Member 3

## 📄 License

This project is developed for IBM Hackathon 2026.
