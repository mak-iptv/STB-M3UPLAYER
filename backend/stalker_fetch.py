import requests

def fetch_channels(portal, mac):
    try:
        portal = portal.rstrip("/")

        # Handshake
        resp = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers={"Cookie": f"mac={mac}"}, timeout=10
        ).json()
        token = resp["js"]["token"]

        # Merr kanalet
        channels_resp = requests.get(
            f"{portal}/stalker_portal.php",
            params={"action":"get_live_streams", "mac": mac},
            headers={"Authorization": f"Bearer {token}"}, timeout=10
        ).json()

        channels = []
        for c in channels_resp.get("js", {}).get("data", []):
            channels.append({
                "name": c["name"],
                "url": f"{portal}/play/live.php?mac={mac}&stream={c['id']}&extension=m3u8&play_token={c['play_token']}",
                "category": c.get("tv_genre_id", "Other")
            })

        return {"success": True, "channels": channels}
    except Exception as e:
        return {"success": False, "error": str(e)}
