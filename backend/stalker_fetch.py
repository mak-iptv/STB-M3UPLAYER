import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_channels(portal: str, mac: str):
    portal = portal.strip().rstrip('/')
    mac = mac.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": f"{portal}/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 1️⃣ Handshake
        hs_resp = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb", "action":"handshake", "JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        )
        hs_resp.raise_for_status()
        hs_json = hs_resp.json()
        token = hs_json["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # 2️⃣ Merr kanalet
        ch_resp = requests.get(
            f"{portal}/server/load.php",
            params={"type":"itv", "action":"get_all_channels", "JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        )
        ch_resp.raise_for_status()
        ch_json = ch_resp.json()

        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/play/live.php?mac={mac}&stream={c["cmd"]}&extension=m3u8&play_token={token}',
                "category": c.get("tv_genre_id", "Other")
            }
            for c in ch_json["js"]["data"]
        ]

        return {"success": True, "channels": channels}

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.route("/fetch_channels")
def fetch_channels_route():
    portal = request.args.get("portal")
    mac = request.args.get("mac")
    if not portal or not mac:
        return jsonify({"success": False, "error": "Missing portal or MAC"}), 400

    result = get_channels(portal, mac)
    return jsonify(result)
