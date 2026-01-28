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
├── data/              # Traffic datasets
├── Frontend/          # Web interface
│   ├── index.html
│   ├── app.js
│   └── config.example.js
├── langflow/          # Langflow agent definitions
├── docs/              # Documentation
└── README.md
```

## 🎯 Features
- Multi-agent AI system
- Natural language queries
- Markdown-formatted responses
- Responsive design

## 📝 License

MIT License

## 👥 Team

IBM Hackathon 2026
```
