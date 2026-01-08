let channels = [];
let favorites = JSON.parse(localStorage.getItem("fav")||"[]");
let history = JSON.parse(localStorage.getItem("hist")||"[]");

const player = document.getElementById("player");
const grid = document.getElementById("grid");
const cats = document.getElementById("cats");
const favList = document.getElementById("favList");
const histList = document.getElementById("histList");
const search = document.getElementById("search");

fetch("channels.json")
  .then(r=>r.json())
  .then(data=>{ channels=data; render(); showCategories(); })
  .catch(e=>console.warn("Failed to load channels.json", e));

function render(list=channels){
  grid.innerHTML="";
  list.filter(c=>c.name.toLowerCase().includes(search.value.toLowerCase()))
      .forEach(c=>{
    let d = document.createElement("div");
    d.className="card";
    d.innerHTML=`<div class="star" onclick="fav(event,'${c.name}')">${favorites.includes(c.name)?'⭐':'☆'}</div>
                 <img src="${c.logo||''}">
                 <div>${c.name}</div>`;
    d.onclick=()=>play(c);
    grid.appendChild(d);
  });
  updateFav(); updateHistory();
}

function showCategories(){
  const unique=[...new Set(channels.map(c=>c.cat))];
  cats.innerHTML="";
  unique.forEach(cat=>{
    let d=document.createElement("div");
    d.innerText=cat;
    d.onclick=()=>render(channels.filter(c=>c.cat===cat));
    cats.appendChild(d);
  });
}

function play(c){
  let url = c.url;
  if(Hls.isSupported()){
    let hls = new Hls();
    hls.loadSource(url);
    hls.attachMedia(player);
  } else player.src=url;
  addHistory(c.name);
}

function fav(e,name){e.stopPropagation();
  favorites.includes(name)?favorites=favorites.filter(f=>f!=name):favorites.push(name);
  localStorage.setItem("fav",JSON.stringify(favorites));
  render();
}
function addHistory(name){history.unshift(name);history=[...new Set(history)].slice(0,10);
  localStorage.setItem("hist",JSON.stringify(history)); updateHistory();
}
function updateFav(){favList.innerHTML="";favorites.forEach(f=>{let div=document.createElement("div");div.innerText=f;div.onclick=()=>{let c=channels.find(ch=>ch.name===f);if(c)play(c);};favList.appendChild(div);});}
function updateHistory(){histList.innerHTML="";history.forEach(h=>{let div=document.createElement("div");div.innerText=h;div.onclick=()=>{let c=channels.find(ch=>ch.name===h);if(c)play(c);};histList.appendChild(div);});}

search.oninput=()=>render();
