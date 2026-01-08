from flask import Flask, request, jsonify, send_from_directory, Response
from stalker_fetch import get_channels
import requests

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal').rstrip('/')
    mac = request.args.get('mac')
    if not portal or not mac:
        return jsonify({"success": False, "error": "Missing portal or MAC"})
    return jsonify(get_channels(portal, mac))

@app.route('/play')
def play_channel():
    url = request.args.get('url')
    if not url:
        return "Missing URL", 400
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, stream=True)
    return Response(r.iter_content(chunk_size=1024),
                    content_type=r.headers.get('Content-Type', 'application/octet-stream'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
