from flask import Flask, jsonify, request, send_from_directory
from stalker_fetch import get_channels
import os

app = Flask(__name__, static_folder="../frontend")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal', '').strip()
    mac = request.args.get('mac', '').strip()
    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal and MAC required"})

    result = get_channels(portal, mac)
    return jsonify(result)

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
