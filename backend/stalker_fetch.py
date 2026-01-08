import requests

def get_channels(portal: str, mac: str):
    """
    Merr kanalet nga portal STB.
    portal: URL e portalit, p.sh. http://23232.top:80/c
    mac: MAC adresë, p.sh. 00:1A:79:9D:8C:B3
    """
    portal = portal.strip().rstrip('/')  # heq hapësirat dhe "/"
    mac = mac.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # Handshake
        hs = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # Merr kanalet
        ch = requests.get(
            f"{portal}/portal.php",
            params={"type":"itv","action":"get_all_channels","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "url": f"{portal}/play/live.php?mac={mac}&stream={c['id']}&extension=m3u8&play_token={c.get('play_token','')}",
                "category": c.get("tv_genre_id","Other")
            }
            for c in ch["js"]["data"]
        ]

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
