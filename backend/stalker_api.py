
import requests

def get_channels(portal, mac):
    try:
        portal = portal.rstrip("/")
        r = requests.get(f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml",
                         headers={"Cookie": f"mac={mac}"})
        token = r.json()["js"]["token"]

        headers = {"Cookie": f"mac={mac}", "Authorization": f"Bearer {token}"}
        ch = requests.get(f"{portal}/portal.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml",
                          headers=headers).json()

        channels = []
        for c in ch["js"]["data"]:
            channels.append({
                "name": c["name"],
                "url": f"{portal}/play/live.php?mac={mac}&stream={c['id']}&extension=m3u8"
            })
        return {"success": True, "channels": channels}
    except Exception as e:
        return {"success": False, "error": str(e)}
