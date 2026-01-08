import requests

def get_channels(portal, mac):
    portal = portal.rstrip("/")
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": f"{portal}/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # HANDSHAKE
        hs = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # GET CHANNELS
        ch = requests.get(
            f"{portal}/stalker_portal.php",
            params={"action":"get_live_streams","mac":mac},
            headers=headers,
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/play/live.php?mac={mac}&stream={c["id"]}&extension=m3u8&play_token={token}',
                "category": c.get("tv_genre_id","Other")
            } for c in ch["js"]["data"]
        ]

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
