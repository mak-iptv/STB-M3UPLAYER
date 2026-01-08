from flask import Flask, request, jsonify, send_from_directory
from stalker_fetch import get_channels
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal", "").rstrip('/')
    mac = request.args.get("mac", "")

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    try:
        channels = get_channels(portal, mac)
        return jsonify({"success": True, "channels": channels})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
