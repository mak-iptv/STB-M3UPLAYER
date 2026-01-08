import requests

def handshake(portal: str, mac: str) -> str:
    """
    Kryen handshake me portalin Stalker dhe kthen tokenin
    """
    headers = {"Cookie": f"mac={mac}"}
    url = portal.rstrip('/') + "/portal.php"
    params = {"type": "stb", "action": "handshake", "JsHttpRequest": "1-xml"}

    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()  # hedh exception nëse nuk funksionon
    data = resp.json()
    return data["js"]["token"]

def get_channels(portal: str, mac: str) -> list:
    """
    Merr të gjitha kanalet nga portal Stalker
    """
    token = handshake(portal, mac)
    headers = {"Cookie": f"mac={mac}"}
    url = portal.rstrip('/') + "/portal.php"
    params = {
        "type": "itv",
        "action": "get_all_channels",
        "JsHttpRequest": "1-xml",
        "token": token
    }

    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    channels = [
        {
            "name": c["name"],
            "url": f'{portal}/portal.php?type=itv&action=create_link&cmd={c["cmd"]}',
            "category": c.get("tv_genre_id", "Other")
        }
        for c in data["js"]["data"]
    ]
    return channels
