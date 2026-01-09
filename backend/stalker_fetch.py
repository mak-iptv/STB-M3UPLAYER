import requests

def get_channels(portal, mac):
    try:
        portal = portal.rstrip("/")

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
        }

        # HANDSHAKE
        hs = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # GET CHANNELS
        ch = requests.get(
            f"{portal}/portal.php",
            params={"type":"itv","action":"get_all_channels","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        channels = []

        for c in ch["js"]["data"]:
            link = requests.get(
                f"{portal}/portal.php",
                params={
                    "type":"itv",
                    "action":"create_link",
                    "cmd": c["cmd"],
                    "JsHttpRequest":"1-xml"
                },
                headers=headers,
                timeout=10
            ).json()

            stream = link["js"]["cmd"].replace("ffmpeg ", "")

            channels.append({
                "name": c["name"],
                "url": stream,
                "category": c.get("tv_genre_id","Other")
            })

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}
