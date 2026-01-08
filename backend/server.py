from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal', '').rstrip('/')
    mac = request.args.get('mac', '').strip()

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC is missing"})

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 1️⃣ HANDSHAKE
        try:
            hs_resp = requests.get(
                f"{portal}/stalker_portal/server/load.php",
                params={"type":"stb", "action":"handshake", "JsHttpRequest":"1-xml"},
                headers=headers,
                timeout=10
            )
            hs = hs_resp.json()
        except ValueError:
            return jsonify({"success": False, "error": "Portal did not return JSON (handshake failed)"})

        token = hs.get("js", {}).get("token")
        if not token:
            return jsonify({"success": False, "error": "Handshake failed, no token received"})
        headers["Authorization"] = f"Bearer {token}"

        # 2️⃣ GET CHANNELS
        try:
            ch_resp = requests.get(
                f"{portal}/stalker_portal/server/load.php",
                params={"type":"itv", "action":"get_all_channels", "JsHttpRequest":"1-xml"},
                headers=headers,
                timeout=10
            )
            ch = ch_resp.json()
        except ValueError:
            return jsonify({"success": False, "error": "Portal did not return JSON (channels fetch failed)"})

        channels = [
            {
                "name": c.get("name", "Unnamed"),
                "url": f'{portal}/stalker_portal/server/load.php?type=itv&action=create_link&cmd={c.get("cmd")}',
                "category": c.get("tv_genre_id","Other")
            }
            for c in ch.get("js", {}).get("data", [])
        ]

        return jsonify({"success": True, "channels": channels})

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Request failed: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
