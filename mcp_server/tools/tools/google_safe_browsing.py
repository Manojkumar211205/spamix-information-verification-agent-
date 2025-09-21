import requests
from config.settings import GOOGLE_SAFE_BROWSING_KEY

def google_safe_browsing(url: str):
    """Check URL using Google Safe Browsing API"""
    endpoint = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {
        "client": {"clientId": "url-safety-agent", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }
    response = requests.post(endpoint, params={"key": GOOGLE_SAFE_BROWSING_KEY}, json=payload)
    result = response.json()

    if "matches" in result:
        return {"status": "malicious", "details": result}
    return {"status": "safe", "details": "no threats detected"}
