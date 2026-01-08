from flask import Flask, send_from_directory
from stalker_fetch import app as stalker_app

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Frontend index.html
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Integron API nga stalker_fetch.py
app.register_blueprint(stalker_app, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
