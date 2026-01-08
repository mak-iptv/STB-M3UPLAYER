import requests

def get_channels(portal: str, mac: str):
    """Fetch channels from the Stalker portal using working portal URL and MAC."""
    portal = portal.rstrip('/')
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 1️⃣ Handshake
        hs_resp = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb", "action":"handshake", "JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        token = hs_resp["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # 2️⃣ Get channels
        ch_resp = requests.get(
            f"{portal}/stalker_portal.php",
            params={"type":"itv", "action":"get_all_channels", "JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/play/live.php?mac={mac}&stream={c["cmd"]}&extension=m3u8&play_token={token}',
                "category": c.get("tv_genre_id","Other")
            }
            for c in ch_resp["js"]["data"]
        ]

        return {"success": True, "channels": channels}
    except Exception as e:
        return {"success": False, "error": str(e)}
