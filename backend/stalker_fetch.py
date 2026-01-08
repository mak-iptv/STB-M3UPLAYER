import requests

def get_channels(portal, mac):
    portal = portal.strip().rstrip('/')
    mac = mac.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # Handshake
        hs_resp = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb", "action":"handshake", "JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        )
        hs = hs_resp.json()
        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # Get channels
        ch_resp = requests.get(
            f"{portal}/stalker_portal.php",
            params={"type":"itv", "action":"get_all_channels", "JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        )
        ch = ch_resp.json()
        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/play/live.php?mac={mac}&stream={c["id"]}&extension=m3u8&play_token={token}',
                "category": c.get("tv_genre_id","Other")
            } for c in ch["js"]["data"]
        ]
        return {"success": True, "channels": channels}

    except ValueError:
        return {"success": False, "error": "Portal did not return JSON (handshake failed)"}
    except Exception as e:
        return {"success": False, "error": str(e)}
