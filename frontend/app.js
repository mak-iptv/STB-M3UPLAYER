
function load(){
 fetch(`/fetch_channels?portal=${portal.value}&mac=${mac.value}`)
 .then(r=>r.json()).then(d=>{
  list.innerHTML='';
  d.channels.forEach(c=>{
   let li=document.createElement('li');
   li.innerText=c.name;
   li.onclick=()=>{
    if(Hls.isSupported()){let h=new Hls();h.loadSource(c.url);h.attachMedia(v);}
    else v.src=c.url;
   };
   list.appendChild(li);
  })
 })
}
