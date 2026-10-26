# Uso: python3 app_pwa.py <contenido_artifact.html> <carpeta_salida> [version]
# Genera la app instalable (PWA) OBSERVATORIO_APP: index.html, manifest.webmanifest, sw.js
import sys,os,datetime,json
src,out=sys.argv[1],sys.argv[2]; ver=sys.argv[3] if len(sys.argv)>3 else datetime.datetime.now().strftime('%Y%m%d-%H%M')
os.makedirs(out,exist_ok=True)
body=open(src,encoding='utf8').read()
head=f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#060b12">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Observatorio">
<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="icon" href="icon-192.png">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}
#appbar{{position:fixed;left:0;right:0;bottom:0;z-index:20;display:flex;justify-content:center;gap:10px;align-items:center;padding:8px max(16px,env(safe-area-inset-left,0px)) calc(8px + env(safe-area-inset-bottom,0px));background:#0b1622;border-top:1px solid #15405a;font:600 11px "JetBrains Mono",ui-monospace,monospace;letter-spacing:.08em;color:#7fa3b5;text-transform:uppercase}}
#appbar button{{all:unset;cursor:pointer;color:#060b12;background:#22d3ee;padding:5px 10px}}</style>
</head><body>'''
tail=f'''<div id="appbar" hidden><span id="appmsg"></span><button id="appupd" hidden>Actualizar</button></div>
<script>
(function(){{var bar=document.getElementById('appbar'),msg=document.getElementById('appmsg'),up=document.getElementById('appupd');
function show(t,b){{msg.textContent=t;bar.hidden=false;up.hidden=!b;}}
if(!('serviceWorker' in navigator)){{return;}}
navigator.serviceWorker.register('sw.js').then(function(reg){{
  navigator.serviceWorker.ready.then(function(){{show('Lista para usar sin conexión · versión {ver}');setTimeout(function(){{bar.hidden=true}},5000);}});
  reg.addEventListener('updatefound',function(){{var w=reg.installing;w&&w.addEventListener('statechange',function(){{if(w.state==='installed'&&navigator.serviceWorker.controller){{show('Nueva versión disponible',true);up.onclick=function(){{w.postMessage('skip');}};}}}});}});
  reg.update();
}}).catch(function(){{}});
navigator.serviceWorker.addEventListener('controllerchange',function(){{location.reload();}});
window.addEventListener('offline',function(){{show('Sin conexión · mostrando el último reporte guardado');}});
window.addEventListener('online',function(){{bar.hidden=true;}});
}})();
</script></body></html>'''
open(os.path.join(out,'index.html'),'w',encoding='utf8').write(head+body+tail)
man={"name":"Observatorio de Inversión MERPAZ","short_name":"Observatorio","description":"Variaciones de mercado, SDIRM y recomendaciones de inversión diarias de MERPAZ Consultores","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#060b12","theme_color":"#060b12","lang":"es","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]}
open(os.path.join(out,'manifest.webmanifest'),'w',encoding='utf8').write(json.dumps(man,ensure_ascii=False))
sw=f"""const CACHE='observatorio-merpaz-{ver}';
const FILES=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./apple-touch-icon.png'];
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener('message',e=>{{if(e.data==='skip')self.skipWaiting()}});
self.addEventListener('fetch',e=>{{if(e.request.method!=='GET')return;const u=new URL(e.request.url);
 if(e.request.mode==='navigate'||u.pathname.endsWith('/index.html')){{e.respondWith(fetch(e.request).then(res=>{{const cp=res.clone();caches.open(CACHE).then(c=>c.put('./index.html',cp));return res}}).catch(()=>caches.match('./index.html')));return}}
 e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request).then(res=>{{if(res.ok||res.type==='opaque'){{const cp=res.clone();caches.open(CACHE).then(c=>c.put(e.request,cp))}}return res}})))}});
"""
open(os.path.join(out,'sw.js'),'w',encoding='utf8').write(sw)
print('OK',out,ver)
