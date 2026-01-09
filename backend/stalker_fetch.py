import requests

def fetch_channels(portal, mac):
    portal = portal.rstrip("/")
    headers = {"Cookie": f"mac={mac}"}

    # 1️⃣ Handshake
    hs = requests.get(f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml", headers=headers, timeout=10).json()
    token = hs["js"]["token"]

    # 2️⃣ Merr kanalet
    ch = requests.get(
        f"{portal}/stalker_portal.php?action=get_live_streams&mac={mac}",
        headers=headers,
        timeout=10
    ).json()

    channels = [
        {
            "name": c["name"],
            "url": f'{portal}/play/live.php?mac={mac}&stream={c["id"]}&extension=m3u8&play_token={token}',
            "category": c.get("tv_genre_id", "Other")
        }
        for c in ch["js"]["data"]
    ]

    return {"success": True, "channels": channels}
