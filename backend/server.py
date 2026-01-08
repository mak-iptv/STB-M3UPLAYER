import os
from flask import Flask, send_from_directory, jsonify, request
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal')
    mac = request.args.get('mac')

    if not portal or not mac:
        return jsonify({'success': False, 'error': 'Portal or MAC missing'})

    try:
        url = f"{portal}/stalker_portal.php?mac={mac}&action=get_live_streams"
        r = requests.get(url, timeout=10)
        data = r.json()
        return jsonify({'success': True, 'channels': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
