// Uso: node extraer.js <Observatorio_MERPAZ.html> <salida.json>
const { chromium } = require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const [,,html,outp]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('file://'+path.resolve(html)+'#recomendacion');await p.waitForTimeout(500);
const R={};
R.corte=await p.$eval('#corte',e=>e.textContent);R.generado=await p.$eval('#gen',e=>e.textContent);
R.contexto=await p.$eval('#contexto',e=>e.textContent);
R.kpis=await p.$$eval('#summary>div',d=>d.map(x=>[...x.children].map(c=>c.textContent.trim())));
R.ecuador=await p.$$eval('#tabla tr',t=>t.map(r=>[...r.cells].map(c=>c.innerText.replace(/\s+/g,' ').trim())).filter(r=>r.length>3));
R.rank=await p.$$eval('#rank tr',t=>t.map(r=>[r.cells[0].innerText,r.cells[1].innerText,r.cells[3].innerText.trim(),r.cells[4].innerText,r.cells[2].innerText]));
R.alerts=await p.$$eval('.alert',a=>a.map(x=>[x.children[0].innerText,x.children[1].querySelector('strong').innerText,x.children[1].querySelector('p').innerText,x.children[2].innerText]));
R.alerta=await p.evaluate(()=>alertaInv());
R.empresas=await p.evaluate(()=>window.empresasTop?window.empresasTop():[]);
R.perfiles={};
for(const k of ['conservador','moderado','agresivo']){await p.click(`#segPerfil button[data-p=${k}]`);
 R.perfiles[k]={sim:await p.$$eval('#simRes .horiz>div',d=>d.map(x=>[...x.children].map(c=>c.innerText.trim()))),
  desc:await p.$eval('#simRes .lead',e=>e.innerText),
  recos:await p.$$eval('#recoRows tr',t=>t.map(r=>[...r.cells].map(c=>c.innerText.replace(/\s+/g,' ').trim())))};}
fs.writeFileSync(outp,JSON.stringify(R,null,1));await b.close();})();
