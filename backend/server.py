from flask import Flask, request, jsonify, send_from_directory
from stalker_fetch import fetch_channels  # ndryshova nga get_channels në fetch_channels
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/fetch_channels")
def fetch_channels_route():  # emri i ruteve mund të jetë ndryshe nga funksioni real
    portal = request.args.get("portal", "").strip()
    mac = request.args.get("mac", "").strip()

    if not portal or not mac:
        return jsonify({
            "success": False,
            "error": "Portal URL or MAC missing"
        })

    try:
        result = fetch_channels(portal, mac)  # thërret funksionin e saktë
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
