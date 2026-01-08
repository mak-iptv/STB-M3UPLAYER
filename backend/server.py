from flask import Flask, send_from_directory
import os

# Root folder frontend
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(__name__, static_folder=FRONTEND_FOLDER)

@app.route("/")
def index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/channels.json")
def channels():
    return send_from_directory(FRONTEND_FOLDER, "channels.json")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
