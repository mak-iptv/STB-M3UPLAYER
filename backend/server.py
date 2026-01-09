from flask import Flask, request, jsonify, send_from_directory, Response
import requests
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# -----------------------------------------
# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# -----------------------------------------
# Fetch channels from Stalker portal
@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal", "").strip()
    mac = request.args.get("mac", "").strip()

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    try:
        # Handshake
        hs = requests.get(
            f"{portal}/portal.php",
            params={"type": "stb", "action": "handshake", "JsHttpRequest": "1-xml"},
            headers={"Cookie": f"mac={mac}"},
            timeout=10
        ).json()

        token = hs["js"]["token"]

        # Get live streams
        ch = requests.get(
            f"{portal}/stalker_portal.php",
            params={"action": "get_live_streams", "mac": mac},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "url": f"{portal}/play/live.php?mac={mac}&stream={c['id']}&extension=m3u8&play_token={c['play_token']}",
                "category": c.get("tv_genre_id", "Other")
            }
            for c in ch["js"]["data"]
        ]

        return jsonify({"success": True, "channels": channels})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# -----------------------------------------
# Proxy for streaming (CORS fix)
@app.route("/proxy_stream")
def proxy_stream():
    url = request.args.get("url")
    if not url:
        return "No url provided", 400

    headers = {"User-Agent": "Mozilla/5.0"}  # STB-like UA
    r = requests.get(url, stream=True, headers=headers)
    return Response(r.iter_content(chunk_size=1024), content_type=r.headers.get("Content-Type"))

# -----------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
