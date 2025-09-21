import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# -----------------------
# External API Keys
# -----------------------

# Google Safe Browsing API Key
GOOGLE_SAFE_BROWSING_KEY = os.getenv("GOOGLE_SAFE_BROWSING_KEY")

# VirusTotal API Key
VIRUSTOTAL_KEY = os.getenv("VIRUSTOTAL_KEY")

# URLScan.io API Key
URLSCAN_KEY = os.getenv("URLSCAN_KEY")

# Google Fact Check Tools API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini API Key for fact checking
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Tavily API Key for web search
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# -----------------------
# Reddit API Settings
# -----------------------

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_REFRESH_TOKEN = os.getenv("REDDIT_REFRESH_TOKEN")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "mcp-reddit-fact-checker")

# -----------------------
# LLM / Groq Settings
# -----------------------

# Groq API Key for LLaMA 3.3
LLM_API_KEY = os.getenv("GROQ_API_KEY")

# LLaMA model name
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

# Optional: max tokens for Groq completion
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 200))

