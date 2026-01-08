from flask import Flask, request, jsonify, send_from_directory
from stalker_fetch import get_channels
import os

app = Flask(__name__, static_folder="../frontend")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# ✅ Route për skedarët statikë
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/fetch_channels')
def fetch_channels_route():
    portal = request.args.get("portal")
    mac = request.args.get("mac")
    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL and MAC required"})
    return jsonify(get_channels(portal, mac))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
