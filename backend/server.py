from flask import Flask, request, jsonify, send_from_directory
from stalker_api import get_channels
import os

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal", "").strip()
    mac = request.args.get("mac", "").strip()

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal ose MAC mungon"})

    return jsonify(get_channels(portal, mac))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
