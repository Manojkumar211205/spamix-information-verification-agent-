import requests
from ...config.settings import VIRUSTOTAL_KEY

def virustotal(url: str):
    """Check URL using VirusTotal API"""
    endpoint = "https://www.virustotal.com/api/v3/urls"
    # URLs must be sent as form-data
    response = requests.post(
        endpoint,
        headers={"x-apikey": VIRUSTOTAL_KEY},
        data={"url": url},
    )

    if response.status_code != 200:
        return {"status": "error", "details": response.text}

    data = response.json()
    analysis_id = data["data"]["id"]

    # Fetch analysis result
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    result = requests.get(analysis_url, headers={"x-apikey": VIRUSTOTAL_KEY}).json()

    stats = result["data"]["attributes"]["stats"]
    malicious = stats.get("malicious", 0)

    return {"status": "malicious" if malicious > 0 else "safe", "details": stats}
