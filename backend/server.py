from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal', '').rstrip('/')
    mac = request.args.get('mac', '')
    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; Linux)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # Handshake
        hs = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers, timeout=10
        ).json()
        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # Channels
        ch = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={"type":"itv","action":"get_all_channels","JsHttpRequest":"1-xml"},
            headers=headers, timeout=10
        ).json()

        channels = [
            {"name": c["name"],
             "url": f'{portal}/stalker_portal/server/load.php?type=itv&action=create_link&cmd={c["cmd"]}',
             "category": c.get("tv_genre_id","Other")}
            for c in ch["js"]["data"]
        ]
        return jsonify({"success": True, "channels": channels})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/m3u')
def m3u():
    portal = request.args.get('portal', '').rstrip('/')
    mac = request.args.get('mac', '')
    if not portal or not mac:
        return "# ERROR: Portal URL or MAC missing", 400

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; Linux)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # Handshake
        hs = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers, timeout=10
        ).json()
        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # Channels
        ch = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={"type":"itv","action":"get_all_channels","JsHttpRequest":"1-xml"},
            headers=headers, timeout=10
        ).json()

        m3u = "#EXTM3U\n"
        for c in ch["js"]["data"]:
            stream = f'{portal}/stalker_portal/server/load.php?type=itv&action=create_link&cmd={c["cmd"]}'
            m3u += f'#EXTINF:-1,{c["name"]}\n{stream}\n'

        return m3u, 200, {"Content-Type": "audio/x-mpegurl"}

    except Exception as e:
        return f"# ERROR: {str(e)}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
