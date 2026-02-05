# 🚀 Deployment Guide - Traffic Analysis API

## Quick Deployment Options

### Option 1: Railway (Recommended - Free & Fast)

1. **Create Railway Account**: https://railway.app
2. **Connect GitHub** and push your code
3. **Create New Project** → Deploy from GitHub
4. **Add Environment Variables** in Railway Dashboard:
   ```
   TOMTOM_API_KEY=your-key
   OPENWEATHER_API_KEY=your-key
   ```
5. **Get your URL**: `https://your-app.up.railway.app`

### Option 2: Render (Free Tier Available)

1. **Create Render Account**: https://render.com
2. **New Web Service** → Connect GitHub
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn src.api.traffic_api:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variables**
6. **Get your URL**: `https://your-app.onrender.com`

### Option 3: Heroku

1. **Create Heroku Account**: https://heroku.com
2. **Install Heroku CLI**
3. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set TOMTOM_API_KEY=your-key
   heroku config:set OPENWEATHER_API_KEY=your-key
   git push heroku main
   ```
4. **Get your URL**: `https://your-app-name.herokuapp.com`

---

## LangFlow Configuration

Once deployed, use this URL in your LangFlow **API Request** component:

```
https://YOUR-DEPLOYED-URL/smart-traffic?query={user_question}
```

### In LangFlow:
1. Open your flow
2. Find the **API Request** component
3. Set **URL**: `https://YOUR-DEPLOYED-URL/smart-traffic`
4. Set **Method**: `GET`
5. Add **Query Parameter**: `query` → Connect to Chat Input

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/smart-traffic?query=...` | GET | **PRIMARY** - Extracts location from query automatically |
| `/traffic/{location}` | GET | Raw traffic data for location |
| `/analyze/{location}` | GET | Full XAI analysis |
| `/weather` | GET | Current weather |
| `/areas` | GET | List all available areas |
| `/api/status` | GET | Check all API configurations |

---

## Testing Your Deployment

After deploying, test these URLs:

1. **Health Check**: `https://YOUR-URL/`
2. **API Status**: `https://YOUR-URL/api/status`
3. **Smart Query**: `https://YOUR-URL/smart-traffic?query=How%20is%20traffic%20at%20Silk%20Board`
4. **Direct Location**: `https://YOUR-URL/analyze/Koramangala`

---

## Environment Variables Required

| Variable | Required | Description |
|----------|----------|-------------|
| `TOMTOM_API_KEY` | Yes | TomTom Traffic API key |
| `OPENWEATHER_API_KEY` | Yes | OpenWeatherMap API key |
| `LANGFLOW_API_KEY` | Optional | For calling LangFlow from API |
| `LANGFLOW_FLOW_ID` | Optional | Your LangFlow flow ID |

