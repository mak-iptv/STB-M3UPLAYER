import requests

def get_channels(portal: str, mac: str):
    portal = portal.rstrip('/')
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 🔹 HANDSHAKE
        resp = requests.get(
            f"{portal}/portal.php",
            params={"type": "stb", "action": "handshake", "JsHttpRequest": "1-xml"},
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        token = data["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # 🔹 GET CHANNELS
        ch_resp = requests.get(
            f"{portal}/server/load.php",
            params={"type": "itv", "action": "get_all_channels", "JsHttpRequest": "1-xml"},
            headers=headers,
            timeout=10
        )
        ch_resp.raise_for_status()
        ch_data = ch_resp.json()["js"]["data"]

        channels = [
            {
                "name": c["name"],
                "category": c.get("tv_genre_id", "Other"),
                "url": f"{portal}/play/live.php?mac={mac}&stream={c['cmd']}&extension=m3u8&play_token={token}"
            }
            for c in ch_data
        ]

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": f"Failed to fetch channels: {str(e)}"}
