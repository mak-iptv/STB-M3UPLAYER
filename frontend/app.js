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

   fetch(`/fetch_channels?portal=${encodeURIComponent(url)}&mac=${encodeURIComponent(mac)}`)
  .then(res => res.json())
  .then(data => {
      if(data.success){
          channels = data.channels;
          render();
          showCategories();
      } else {
          alert("Failed: " + data.error);
      }
  });

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
    } else {
        player.src = c.url;
    }
}
