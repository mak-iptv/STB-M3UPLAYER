import requests

def get_channels(portal: str, mac: str):
    """
    Marrim token nga handshake dhe ndërtojmë listën e kanaleve
    """
    portal = portal.rstrip('/')  # heq hapësirat dhe / në fund

    headers = {
        "Cookie": f"mac={mac}"
    }

    try:
        # 1️⃣ Handshake për token
        hs_resp = requests.get(
            f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml",
            headers=headers,
            timeout=10
        ).json()

        token = hs_resp["js"]["token"]

        # 2️⃣ Merr kanalet
        ch_resp = requests.get(
            f"{portal}/stalker_portal.php?action=get_live_streams&mac={mac}",
            headers=headers,
            timeout=10
        ).json()

        channels = []
        for c in ch_resp["js"]["data"]:
            stream_id = c.get("num") or c.get("cmd")  # siguro ID e stream
            channels.append({
                "name": c["name"],
                "url": f"{portal}/play/live.php?mac={mac}&stream={stream_id}&extension=m3u8&play_token={token}",
                "category": c.get("tv_genre_id", "Other")
            })

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
