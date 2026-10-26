# Uso: python3 correo_html.py <datos.json> <salida.html>  -> cuerpo HTML del correo diario
import json,sys,html
D=json.load(open(sys.argv[1],encoding='utf8'));e=html.escape
c=lambda a:'#15803d' if a.lower().startswith(('comprar','incrementar')) else '#be123c' if a.lower().startswith('evitar') else '#b45309' if a.lower().startswith('subponderar') else '#5b6b75'
def alerta():
    A=D['alerta'];col='#15803d' if A['nivel']=='fuerte' else '#b45309'
    li=''.join(f'<li style="margin:4px 0"><b style="color:{"#be123c" if i["c"]=="down" else "#15803d"}">{e(i["k"])}:</b> <b>{e(i["t"])}</b>. {e(i["d"])} <span style="color:#5b6b75">({e(i["perf"])})</span></li>' for i in A['items'])
    return f'<div style="border:2px solid {col};background:#fffbeb;padding:12px 14px;margin:12px 0"><div style="font:bold 15px Arial;color:{col};text-transform:uppercase">{e(A["tit"])}</div><ul style="margin:8px 0 0;padding-left:18px;font-size:13px">{li}</ul></div>'
td='style="padding:6px 8px;border-bottom:1px solid #dbe4e9;font:13px Arial,sans-serif;color:#0b1622;vertical-align:top"'
h=f'''<div style="max-width:680px;margin:0 auto;font:14px Arial,sans-serif;color:#0b1622">
<div style="background:#0b1622;color:#fff;padding:14px 18px"><span style="border:2px solid #22d3ee;color:#22d3ee;font-weight:bold;padding:1px 6px">MP</span>&nbsp; <b>MERPAZ Consultores</b> · Observatorio de Inversión<br><span style="color:#9fc3d1;font-size:12px">Cierre de mercado {e(D['corte'])}</span></div>
'''+alerta()+'''<table style="border-collapse:collapse;width:100%;margin:12px 0">'''+''.join(f'<tr><td {td}>{e(k[0])}</td><td {td} align="right"><b>{e(k[1])}</b></td><td {td} align="right">{e(k[2] if len(k)>2 else "")}</td></tr>' for k in D['kpis'])+f'''</table>
<p style="line-height:1.5">{e(D['contexto'])}</p>
<h3 style="font:bold 15px Arial;margin:16px 0 6px">SDIRM: ranking del día</h3><table style="border-collapse:collapse;width:100%">'''+''.join(f'<tr><td {td}><b>{e(r[0])}</b></td><td {td} align="right">{e(r[2].split(chr(10))[-1])}</td><td {td}>{e(r[3])}</td></tr>' for r in D['rank'])+'</table>'
if D.get('empresas'):
    h+='<h3 style="font:bold 15px Arial;margin:16px 0 6px">Empresas sólidas y rentables (ISR MERPAZ)</h3><table style="border-collapse:collapse;width:100%">'+''.join(f'<tr><td {td}><b>{e(x["n"])}</b><br><span style="color:#5b6b75;font-size:12px">{e(x["sec"])} · {e(x["pais"])}</span></td><td {td} align="right">{x["isr"]}/100</td><td {td} style="color:{"#15803d" if x["isr"]>=70 else "#b45309" if x["isr"]>=55 else "#be123c"}"><b>{e(x["ver"])}</b></td><td {td}>{(str(x["div"]).replace(".",",")+"%") if x["div"] else "sin dividendo"}</td></tr>' for x in D['empresas'])+'</table>'
for k,t in [('conservador','Conservador'),('moderado','Moderado'),('agresivo','Agresivo')]:
    p=D['perfiles'][k]
    h+=f'<h3 style="font:bold 15px Arial;margin:16px 0 4px">Perfil {t}</h3><p style="margin:0 0 6px;color:#5b6b75;font-size:13px">{e(p["desc"])}</p><p style="margin:0 0 6px">'+' &nbsp;|&nbsp; '.join(f'{e(s[0].capitalize())}: <b>{e(s[1])}</b>' for s in p['sim'])+'</p><table style="border-collapse:collapse;width:100%">'+''.join(f'<tr><td {td} style="color:{c(r[0])}"><b style="color:{c(r[0])}">{e(r[0])}</b></td><td {td}>{e(r[1])}</td></tr>' for r in p['recos'][1:])+'</table>'
h+='<p style="color:#5b6b75;font-size:12px;margin-top:18px">Adjunto: reporte en PDF. El tablero interactivo con la calculadora está en OneDrive\\APP\\Observatorio MERPAZ (Observatorio_MERPAZ.html, se abre en cualquier navegador). Información referencial elaborada con datos públicos; no constituye asesoría financiera.</p></div>'
open(sys.argv[2],'w',encoding='utf8').write(h)
