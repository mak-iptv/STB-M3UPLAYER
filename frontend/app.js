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
    const url = document.getElementById("portalUrl").value.trim();
    const mac = document.getElementById("macAddr").value.trim();
    if (!url || !mac) return alert("Enter Portal URL & MAC");

    fetch(`/api/fetch_channels?portal=${encodeURIComponent(url)}&mac=${encodeURIComponent(mac)}`)
    .then(res => res.json())
    .then(data => {
        if(data.success){
            channels = data.channels;
            render();
            showCategories();
            alert("Channels loaded successfully!");
        } else {
            alert("Failed: " + data.error);
        }
    }).catch(err => alert("Error fetching channels"));
}

function render(list = channels){
    const grid = document.getElementById("grid");
    grid.innerHTML = "";
    list.filter(c => c.name.toLowerCase().includes(search.value.toLowerCase()))
        .forEach(c=>{
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `<div class="star" onclick="fav(event,'${c.name}')">${favorites.includes(c.name)?"⭐":"☆"}</div>
                              <div>${c.name}</div>`;
            card.onclick = ()=>play(c);
            grid.appendChild(card);
        });
}

function play(c){
    if(Hls.isSupported()){
        const hls = new Hls();
        hls.loadSource(c.url);
        hls.attachMedia(player);
    } else {
        player.src = c.url;
    }
    addHistory(c.name);
}

function addHistory(name){
    history.unshift(name);
    history = [...new Set(history)].slice(0,10);
    localStorage.setItem("hist", JSON.stringify(history));
    updateHistory();
}

function fav(e,name){
    e.stopPropagation();
    favorites.includes(name) ? favorites=favorites.filter(f=>f!=name) : favorites.push(name);
    localStorage.setItem("fav", JSON.stringify(favorites));
    updateFav();
    render();
}

function updateFav(){
    favList.innerHTML="";
    favorites.forEach(f=>{
        const div=document.createElement("div");
        div.innerText=f;
        div.onclick=()=>{const c=channels.find(ch=>ch.name===f); if(c) play(c);};
        favList.appendChild(div);
    });
}

function updateHistory(){
    histList.innerHTML="";
    history.forEach(h=>{
        const div=document.createElement("div");
        div.innerText=h;
        div.onclick=()=>{const c=channels.find(ch=>ch.name===h); if(c) play(c);};
        histList.appendChild(div);
    });
}

function showCategories(){
    cats.innerHTML="";
    const unique = [...new Set(channels.map(c=>c.category))];
    unique.forEach(cat=>{
        const div=document.createElement("div");
        div.innerText=cat;
        div.onclick=()=>render(channels.filter(c=>c.category===cat));
        cats.appendChild(div);
    });
}

updateFav();
updateHistory();
