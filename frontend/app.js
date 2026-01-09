let channels = [];

const player = document.getElementById("player");
const search = document.getElementById("search");
const cats = document.getElementById("cats");

function fetchChannels() {
    const portal = portalUrl.value;
    const mac = macAddr.value;

    fetch(`/fetch_channels?portal=${encodeURIComponent(portal)}&mac=${encodeURIComponent(mac)}`)
    .then(r => r.json())
    .then(d => {
        if (!d.success) return alert(d.error);
        channels = d.channels;
        render(channels);
        showCategories();
    });
}

function render(list) {
    grid.innerHTML = "";
    list
      .filter(c => c.name.toLowerCase().includes(search.value.toLowerCase()))
      .forEach(c => {
        const d = document.createElement("div");
        d.className = "card";
        d.innerText = c.name;
        d.onclick = () => play(c.url);
        grid.appendChild(d);
      });
}

function play(url) {
    if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(url);
        hls.attachMedia(player);
    } else {
        player.src = url;
    }
}

function showCategories() {
    cats.innerHTML = "";
    [...new Set(channels.map(c => c.category))].forEach(cat => {
        const d = document.createElement("div");
        d.innerText = cat;
        d.onclick = () => render(channels.filter(c => c.category === cat));
        cats.appendChild(d);
    });
}

search.oninput = () => render(channels);
