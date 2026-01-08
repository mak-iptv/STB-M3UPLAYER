import requests

def get_channels(portal: str, mac: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 1️⃣ Handshake
        hs = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()
        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # 2️⃣ Get channels
        ch = requests.get(
            f"{portal}/portal.php",
            params={"type":"itv","action":"get_all_channels","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "cmd": c["cmd"],
                "category": c.get("tv_genre_id", "Other"),
                "url": f'{portal}/portal.php?type=itv&action=create_link&cmd={c["cmd"]}'
            } for c in ch["js"]["data"]
        ]
        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
