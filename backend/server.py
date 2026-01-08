import os
import requests
from flask import Flask, send_from_directory, jsonify, request

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)


# =========================
# STALKER HEADERS (MAG)
# =========================
def stalker_headers(mac, token=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "application/json",
        "Referer": "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/Tirane"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


# =========================
# FRONTEND
# =========================
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


# =========================
# FETCH CHANNELS (STALKER)
# =========================
@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal")
    mac = request.args.get("mac")

    if not portal or not mac:
        return jsonify({"success": False, "error": "Portal URL or MAC missing"})

    try:
        # Normalize portal URL
        portal = portal.rstrip("/")

        # 1️⃣ HANDSHAKE → TOKEN
        hs_url = f"{portal}/portal.php?action=handshake&type=stb&token="
        hs_res = requests.get(
            hs_url,
            headers=stalker_headers(mac),
            timeout=10
        )
        hs_res.raise_for_status()
        token = hs_res.json()["js"]["token"]

        # 2️⃣ GET CHANNELS
        ch_url = f"{portal}/portal.php?type=itv&action=get_all_channels"
        ch_res = requests.get(
            ch_url,
            headers=stalker_headers(mac, token),
            timeout=15
        )
        ch_res.raise_for_status()

        channels = ch_res.json()["js"]["data"]

        return jsonify({
            "success": True,
            "channels": channels
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
