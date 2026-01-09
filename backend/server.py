from flask import Flask, request, jsonify, send_from_directory
from stalker_fetch import fetch_channels
import os

# Vendos rrugën absolute te frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
app = Flask(__name__, static_folder=frontend_path, static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/fetch_channels")
def fetch():
    portal = request.args.get("portal", "").strip()
    mac = request.args.get("mac", "").strip()

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    result = fetch_channels(portal, mac)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
