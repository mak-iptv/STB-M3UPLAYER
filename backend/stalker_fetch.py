import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal").rstrip("/")
    mac = request.args.get("mac")

    try:
        # HANDSHAKE
        resp = requests.get(
            f"{portal}/portal.php?type=stb&action=handshake&JsHttpRequest=1-xml",
            headers={"Cookie": f"mac={mac}"}, timeout=10
        )
        token = resp.json()["js"]["token"]

        # Këtu mund të mbledhim kanalet
        # Për shembull:
        channels = [
            {
                "name": "Channel 1",
                "url": f"{portal}/play/live.php?mac={mac}&stream=156653&extension=m3u8&play_token={token}"
            }
        ]
        return jsonify({"success": True, "channels": channels})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
