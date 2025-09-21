import requests
from ...config.settings import URLSCAN_KEY

def urlscan(url: str):
    """Check URL using URLScan.io API"""
    endpoint = "https://urlscan.io/api/v1/scan/"
    headers = {"API-Key": URLSCAN_KEY, "Content-Type": "application/json"}
    payload = {"url": url, "visibility": "private"}

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code != 200:
        return {"status": "error", "details": response.text}

    data = response.json()
    return {"status": "submitted", "details": data}
