import requests

def get_channels(portal: str, mac: str):
    portal = portal.strip().rstrip("/")
    mac = mac.strip()

    headers = {
        "Cookie": f"mac={mac}"
    }

    try:
        # HANDSHAKE
        hs = requests.get(
            f"{portal}/portal.php",
            params={
                "type": "stb",
                "action": "handshake",
                "JsHttpRequest": "1-xml"
            },
            headers=headers,
            timeout=10
        )
        hs.raise_for_status()
        token = hs.json()["js"]["token"]

        # GET CHANNELS
        ch = requests.get(
            f"{portal}/stalker_portal.php",
            params={
                "action": "get_live_streams",
                "mac": mac
            },
            headers=headers,
            timeout=10
        )
        ch.raise_for_status()
        data = ch.json()["js"]["data"]

        channels = []
        for c in data:
            stream_id = c.get("id") or c.get("num")
            channels.append({
                "name": c["name"],
                "url": (
                    f"{portal}/play/live.php"
                    f"?mac={mac}"
                    f"&stream={stream_id}"
                    f"&extension=m3u8"
                    f"&play_token={token}"
                ),
                "category": c.get("tv_genre_id", "Other")
            })

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
