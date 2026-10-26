const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('file://'+require('path').resolve('.')+'/'+(process.argv[2]||'Observatorio_MERPAZ.html'));await p.waitForTimeout(600);
await p.addStyleTag({content:`nav,.controls .seg,#copy,#wa,.weights,#wreset{display:none!important}
section.view{display:flex!important;break-before:page}section#v-variaciones{break-before:auto}
.ring .spin,.ring .spin2{animation:none}tr,.prof,.chart,.alert,.calc,.simres{break-inside:avoid}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact;background-image:none!important}*{clip-path:none!important;box-shadow:none!important}.read,.simres,.scen .base,tr.grp td{background:var(--soft)!important}
section.view::before{font:600 11px var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
#v-sdirm::before{content:"Pestaña SDIRM"}#v-recomendacion::before{content:"Pestaña Recomendación"}#v-mensaje::before{content:"Mensaje WhatsApp"}`});
await p.evaluate(()=>{document.querySelectorAll('section.view').forEach(s=>s.hidden=false);document.getElementById('v-sdirm').after(document.getElementById('v-recomendacion'));});
await p.emulateMedia({media:'screen'});
await p.pdf({path:(process.argv[3]||'Observatorio_MERPAZ.pdf'),format:'A4',landscape:true,printBackground:true,margin:{top:'0',bottom:'0',left:'0',right:'0'},scale:0.7});
await b.close();})();
