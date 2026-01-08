# backend/stalker_fetch.py
import requests
import re

def get_channels(portal: str, mac: str):
    """
    Merr kanalet nga portal Stalker dhe kthen listë me link HLS për player.
    portal: URL e portalit pa / në fund (p.sh. http://IP:PORT/c)
    mac: MAC i set-top-box
    """
    if not portal.endswith("/c"):
        portal = portal.rstrip("/") + "/c"

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": portal + "/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    # 1️⃣ Handshake për të marrë token
    handshake_url = f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml"
    resp = requests.get(handshake_url, headers=headers, timeout=10)
    try:
        token = resp.json()["js"]["token"]
    except Exception:
        raise Exception(f"Handshake failed, response: {resp.text}")

    # 2️⃣ Merr listën e kanaleve
    channel_url = f"{portal}/stalker_portal.php"
    params = {
        "type": "itv",
        "action": "get_all_channels",
        "JsHttpRequest": "1-xml"
    }
    headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(channel_url, headers=headers, params=params, timeout=10)

    try:
        data = resp.json()["js"]["data"]
    except Exception:
        raise Exception(f"Failed to get channels, response: {resp.text}")

    # 3️⃣ Krijo listën me link HLS
    channels = []
    for ch in data:
        stream_id = ch.get("id") or ch.get("num") or ch.get("cmd")
        if not stream_id:
            continue
        # link HLS për player
        url = f"{portal}/play/live.php?mac={mac}&stream={stream_id}&extension=m3u8&play_token={token}"
        channels.append({
            "name": ch.get("name", "Unknown"),
            "url": url,
            "category": ch.get("tv_genre_id", "Other")
        })

    return channels
