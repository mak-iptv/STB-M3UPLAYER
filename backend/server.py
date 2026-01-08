import os
from flask import Flask, send_from_directory, jsonify, request
import requests


# Absolute path për frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')


app = Flask(__name__, static_folder=FRONTEND_DIR)


@app.route('/')
def index():
return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
return send_from_directory(app.static_folder, path)


@app.route('/fetch_channels')
def fetch_channels():
portal = request.args.get('portal')
mac = request.args.get('mac')
if not portal or not mac:
return jsonify({'success': False, 'error': 'Portal URL or MAC missing'})
try:
r = requests.get(f'{portal}/stalker_portal.php?mac={mac}&action=get_live_streams', timeout=10)
channels = r.json()
return jsonify({'success': True, 'channels': channels})
except Exception as e:
return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
