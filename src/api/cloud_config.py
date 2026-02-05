"""
Cloud Deployment Configuration
==============================
Configuration for deploying the Traffic API to cloud platforms.

Supports: Railway, Render, Heroku, or any cloud platform.

Author: IBM Hackathon Team
"""

import os

# ==================== DEPLOYMENT CONFIGURATION ====================

# For local development
LOCAL_API_URL = "http://localhost:8001"

# For cloud deployment - Set this in your cloud platform's environment variables
# Example: https://traffic-api-production.up.railway.app
CLOUD_API_URL = os.getenv("CLOUD_API_URL", LOCAL_API_URL)

# Determine if running in cloud or local
IS_CLOUD = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER") or os.getenv("HEROKU_APP_NAME")

# Get the appropriate API URL
def get_api_base_url():
    """Returns the appropriate API base URL based on environment."""
    if IS_CLOUD:
        return CLOUD_API_URL
    return LOCAL_API_URL

# ==================== CORS CONFIGURATION ====================

# Allowed origins for CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "https://langflow.datastax.com",
    "https://*.langflow.astra.datastax.com",
    "https://astra.datastax.com",
    # Add your frontend URL when deployed
]

# If in cloud, allow all origins (for hackathon demo)
if IS_CLOUD:
    ALLOWED_ORIGINS = ["*"]

