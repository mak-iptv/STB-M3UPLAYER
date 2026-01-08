from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal').rstrip('/')
    mac = request.args.get('mac')
    if not portal or not mac:
        return jsonify({"success": False, "error": "Missing portal or MAC"})

    headers = {"Cookie": f"mac={mac}"}
    try:
        # 1️⃣ Handshake
        hs = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        token = hs["js"]["token"]

        # 2️⃣ Merr kanalet
        ch = requests.get(
            f"{portal}/portal.php",
            params={"type":"itv","action":"get_all_channels","JsHttpRequest":"1-xml","token":token},
            headers=headers,
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/portal.php?type=itv&action=create_link&cmd={c["cmd"]}',
                "category": c.get("tv_genre_id","Other")
            }
            for c in ch["js"]["data"]
        ]
        return jsonify({"success": True, "channels": channels})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
