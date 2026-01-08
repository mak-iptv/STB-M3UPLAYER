from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/fetch_channels")
def fetch_channels():
    portal = request.args.get("portal").rstrip('/')
    mac = request.args.get("mac")
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"{portal}/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }
    
    try:
        # 1️⃣ Handshake
        hs = requests.get(
            f"{portal}/portal.php",
            params={"type":"stb","action":"handshake","token":"","prehash":"0","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()
        
        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"
        
        # 2️⃣ Get channels
        ch = requests.get(
            f"{portal}/portal.php",
            params={"type":"itv","action":"get_all_channels","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()
        
        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/portal.php?type=itv&action=create_link&cmd={c["cmd"]}',
                "category": c.get("tv_genre_id","Other")
            }
            for c in ch["js"]["data"]
        ]
        
        return jsonify({"success": True, "channels": channels})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
