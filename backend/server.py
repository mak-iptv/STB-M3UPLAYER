from flask import Flask, jsonify, request, send_from_directory
from stalker_fetch import get_channels  # ✅ versioni i saktë
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/fetch_channels")
def fetch_channels_route():
    portal = request.args.get("portal", "").rstrip("/")
    mac = request.args.get("mac", "")

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    try:
        channels = get_channels(portal, mac)  # ✅ funksioni i saktë
        return jsonify({"success": True, "channels": channels})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
