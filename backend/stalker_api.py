import requests

def fetch_channels(portal: str, mac: str):
    portal = portal.rstrip('/')
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"mac={mac}"
    }

    try:
        # Handshake për të marrë token
        hs_resp = requests.get(f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml", headers=headers, timeout=10)
        hs_resp.raise_for_status()
        hs_json = hs_resp.json()
        token = hs_json["js"]["token"]

        # Për test: krijojmë disa kanale shembull
        channels = [
            {
                "name": f"Channel {i}",
                "url": f"{portal}/play/live.php?mac={mac}&stream={i}&extension=m3u8&play_token={token}",
                "category": "TV"
            } for i in range(1, 6)
        ]

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": f"Failed to fetch channels: {e}", "text": hs_resp.text if 'hs_resp' in locals() else ""}
