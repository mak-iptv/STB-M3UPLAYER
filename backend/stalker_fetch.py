import requests

def fetch_channels(portal: str, mac: str):
    """
    Merr kanalet nga Stalker Portal dhe kthen listën me URL për player.
    """
    portal = portal.rstrip('/')
    try:
        # 1️⃣ Handshake për token
        hs_resp = requests.get(
            f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml",
            headers={"Cookie": f"mac={mac}"}, timeout=10
        ).json()

        token = hs_resp["js"]["token"]

        # 2️⃣ Merr kanalet live
        ch_resp = requests.get(
            f"{portal}/stalker_portal.php?mac={mac}&action=get_live_streams",
            headers={"Cookie": f"mac={mac}"}, timeout=10
        ).json()

        channels = []
        for c in ch_resp["js"]["data"]:
            url = (
                f"{portal}/play/live.php?"
                f"mac={mac}&"
                f"stream={c['id']}&"
                f"extension=m3u8&"
                f"play_token={token}"
            )
            channels.append({
                "name": c["name"],
                "url": url,
                "category": c.get("tv_genre_id", "Other")
            })
        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
