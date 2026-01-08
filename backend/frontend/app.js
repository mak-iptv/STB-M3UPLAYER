let channels = [];
let favorites = JSON.parse(localStorage.getItem("fav") || "[]");
let history = JSON.parse(localStorage.getItem("hist") || "[]");

const player = document.getElementById("player");
const search = document.getElementById("search");
const cats = document.getElementById("cats");
const favList = document.getElementById("favList");
const histList = document.getElementById("histList");

search.oninput = () => render();

function fetchChannels() {
    const url = document.getElementById("portalUrl").value;
    const mac = document.getElementById("macAddr").value;
    if (!url || !mac) return alert("Enter Portal URL & MAC");

   @app.route('/fetch_channels')
def fetch_channels():
    portal = request.args.get('portal').rstrip('/')
    mac = request.args.get('mac')

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C)",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Accept": "*/*",
        "Referer": portal + "/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=Europe/London"
    }

    try:
        # 1️⃣ HANDSHAKE
        hs = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={"type":"stb","action":"handshake","JsHttpRequest":"1-xml"},
            headers=headers,
            timeout=10
        ).json()

        token = hs["js"]["token"]
        headers["Authorization"] = f"Bearer {token}"

        # 2️⃣ GET CHANNELS
        ch = requests.get(
            f"{portal}/stalker_portal/server/load.php",
            params={
                "type":"itv",
                "action":"get_all_channels",
                "JsHttpRequest":"1-xml"
            },
            headers=headers,
            timeout=10
        ).json()

        channels = [
            {
                "name": c["name"],
                "url": f'{portal}/stalker_portal/server/load.php?type=itv&action=create_link&cmd={c["cmd"]}',
                "category": c.get("tv_genre_id","Other")
            }
            for c in ch["js"]["data"]
        ]

        return jsonify({"success": True, "channels": channels})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


function render(list = channels) {
    const grid = document.getElementById("grid");
    grid.innerHTML = "";
    list.filter(c => c.name?.toLowerCase().includes(search.value.toLowerCase()))
    .forEach(c => {
        const d = document.createElement("div");
        d.className = "card";
        d.innerText = c.name;
        d.onclick = () => play(c);
        grid.appendChild(d);
    });
}

function play(c) {
    if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(c.url);
        hls.attachMedia(player);
    } else player.src = c.url;
}
