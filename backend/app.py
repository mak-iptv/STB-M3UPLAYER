import os
from flask import Flask, request, jsonify, send_from_directory
from stalker_fetch import get_channels

# Absolute path e frontend folder
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app = Flask(__name__, static_folder=frontend_path, static_url_path="")

# Root → index.html
@app.route("/")
def index():
    return send_from_directory(frontend_path, "index.html")

# API → fetch channels
@app.route("/fetch_channels")
def fetch():
    portal = request.args.get("portal", "").strip()
    mac = request.args.get("mac", "").strip()

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    result = get_channels(portal, mac)
    return jsonify(result)

# ❌ Hiqni app.run për Vercel
# Vercel menaxhon serverin vetë
