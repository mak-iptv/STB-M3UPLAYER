import requests

def fetch_channels(portal, mac):
    portal = portal.rstrip('/')
    headers = {"Cookie": f"mac={mac}"}

    # 1️⃣ Handshake
    r = requests.get(f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml", headers=headers, timeout=10)
    js = r.json()
    token = js["js"]["token"]

    headers["Authorization"] = f"Bearer {token}"

    # 2️⃣ Merr kanalet
    r2 = requests.get(f"{portal}/stalker_portal.php?action=get_live_streams&mac={mac}", headers=headers, timeout=10)
    channels_json = r2.json()

    channels = []
    for c in channels_json.get("js", {}).get("data", []):
        channels.append({
            "name": c["name"],
            "url": f"{portal}/play/live.php?mac={mac}&stream={c['stream_id']}&extension=m3u8&play_token={c['play_token']}",
            "category": c.get("tv_genre", "Other")
        })
    return {"success": True, "channels": channels}
