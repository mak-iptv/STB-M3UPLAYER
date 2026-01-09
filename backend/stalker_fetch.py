import requests

def fetch_channels(portal: str, mac: str):
    """
    Merr kanalet nga Stalker portal.
    portal: URL e portalit (shembull: http://IP:PORT/c/)
    mac: MAC i pajisjes
    """
    portal = portal.rstrip('/')  # heq / në fund
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 1️⃣ HANDSHAKE
        hs_resp = requests.get(
            f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml",
            headers=headers,
            timeout=10
        )
        try:
            hs = hs_resp.json()
        except ValueError:
            return {"success": False, "error": "Handshake failed: invalid JSON", "text": hs_resp.text}

        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # 2️⃣ GET LIVE STREAMS
        ch_resp = requests.get(
            f"{portal}/stalker_portal.php",
            params={"action":"get_live_streams", "mac": mac},
            headers=headers,
            timeout=10
        )
        try:
            ch_data = ch_resp.json()
        except ValueError:
            return {"success": False, "error": "Failed to fetch channels: invalid JSON", "text": ch_resp.text}

        channels = []
        for c in ch_data:
            stream = c.get("id") or c.get("cmd")
            play_token = c.get("play_token") or token
            url = f"{portal}/play/live.php?mac={mac}&stream={stream}&extension=m3u8&play_token={play_token}"
            channels.append({
                "name": c.get("name", "Unknown"),
                "url": url,
                "category": c.get("category", "Other")
            })

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
