import requests

def get_channels(portal, mac):
    headers = {"Cookie": f"mac={mac}", "User-Agent": "Mozilla/5.0"}

    # 1️⃣ Handshake për token
    hs = requests.get(f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml",
                      headers=headers, timeout=10)
    token_json = hs.json()
    token = token_json["js"]["token"]

    # 2️⃣ Merr kanalet live
    ch = requests.get(f"{portal}/stalker_portal.php",
                      params={"action": "get_live_streams", "mac": mac, "token": token},
                      headers=headers, timeout=10)
    channels_json = ch.json()

    # 3️⃣ Krijo URL për player
    channels = [
        {
            "name": c["name"],
            "url": f'{portal}/play/live.php?mac={mac}&stream={c["id"]}&extension=m3u8&play_token={token}',
            "category": c.get("category", "Other")
        } for c in channels_json
    ]
    return channels
