
from flask import Flask, request, jsonify, send_from_directory
from backend.stalker_api import get_channels
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal","").strip()
    mac = request.args.get("mac","").strip()
    return jsonify(get_channels(portal, mac))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
