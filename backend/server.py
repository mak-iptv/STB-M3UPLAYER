from flask import Flask, request, jsonify, send_from_directory
from stalker_fetch import fetch_channels

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_channels')
def get_channels():
    portal = request.args.get('portal')
    mac = request.args.get('mac')
    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL and MAC required"})

    result = fetch_channels(portal, mac)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
