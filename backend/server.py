from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal")
    mac = request.args.get("mac")
    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    try:
        r = requests.get(f"{portal}/stalker_portal.php?mac={mac}&action=get_live_streams", timeout=10)
        channels = r.json()  # ose parse sipas formatit te portalit
        return jsonify({"success": True, "channels": channels})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
