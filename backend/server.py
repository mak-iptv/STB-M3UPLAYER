import os
from flask import Flask, send_from_directory, jsonify, request
import requests

# Vendos folderin frontend si static folder
app = Flask(__name__, static_folder="../frontend")

# Route kryesore për index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Route për CSS/JS
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# Route për fetch kanalet nga Stalker portal
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
    port = int(os.environ.get('PORT', 5000))  # Render cakton port nga environment
    app.run(host='0.0.0.0', port=port)
