from flask import Flask, request, jsonify, send_from_directory
from stalker_fetch import get_channels

app = Flask(__name__, static_folder="../frontend")

@app.route('/fetch_channels')
def fetch_channels_route():
    portal = request.args.get('portal', '')
    mac = request.args.get('mac', '')
    return jsonify(get_channels(portal, mac))

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
