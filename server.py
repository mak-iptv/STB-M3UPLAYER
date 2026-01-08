from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal').rstrip('/')
    mac = request.args.get('mac')

    if not portal or not mac:
        return jsonify({"success": False, "error": "Missing portal or MAC"})

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 1️⃣ HANDSHAKE
        hs = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # 2️⃣ GET CHANNELS
        ch = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={
                "type":"itv",
                "action":"get_all_channels",
                "JsHttpRequest":"1-xml"
            },
            headers=headers,
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/stalker_portal/server/load.php?type=itv&action=create_link&cmd={c["cmd"]}',
                "category": c.get("tv_genre_id","Other")
            }
            for c in ch["js"]["data"]
        ]

        return jsonify({"success": True, "channels": channels})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
