import os
import requests
import json
from datetime import datetime
import pytz
from tqdm import tqdm

# --- Config ---
PORTAL_URL = os.environ.get("PORTAL_URL", "http://your.stalker.portal")
MAC = os.environ.get("MAC", "00:1A:79:XX:XX:XX")
OUTPUT_FILE = "frontend/channels.json"

def fetch_channels():
    """
    Fetch live channels from Stalker Portal using MAC address.
    """
    url = f"{PORTAL_URL}/stalker_portal.php?mac={MAC}&action=get_live_streams"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()  # Assuming JSON response
        return data
    except Exception as e:
        print(f"[ERROR] Failed to fetch channels: {e}")
        return []

if __name__ == "__main__":
    channels = fetch_channels()
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)
    print(f"[{datetime.now()}] Channels saved: {len(channels)}")
