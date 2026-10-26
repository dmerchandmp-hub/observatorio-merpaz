# Uso: python3 reporte_pdf.py <datos.json> <salida.pdf>
import json,sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
D=json.load(open(sys.argv[1],encoding='utf8'))
INK=colors.HexColor('#0b1622');CY=colors.HexColor('#0e7490');MU=colors.HexColor('#5b6b75');RL=colors.HexColor('#c9d6dd');UP=colors.HexColor('#15803d');DN=colors.HexColor('#be123c');WA=colors.HexColor('#b45309')
st=lambda n,**k:ParagraphStyle(n,fontName=k.pop('f','Helvetica'),**k)
H1=st('h1',f='Helvetica-Bold',fontSize=18,leading=22,textColor=INK);EY=st('ey',f='Helvetica-Bold',fontSize=7.5,leading=10,textColor=CY)
H2=st('h2',f='Helvetica-Bold',fontSize=11.5,leading=15,textColor=INK,spaceBefore=8,spaceAfter=4);B=st('b',fontSize=8.6,leading=11.5,textColor=INK)
S=st('s',fontSize=7.4,leading=9.5,textColor=MU);C=st('c',fontSize=7.8,leading=10,textColor=INK);CB=st('cb',f='Helvetica-Bold',fontSize=7.8,leading=10,textColor=INK)
def P(t,s=C):return Paragraph(str(t).replace('&','&amp;').replace('<','&lt;'),s)
def tbl(rows,w,head=True):
    t=Table(rows,colWidths=w,repeatRows=1 if head else 0)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,RL),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f1f5') if head else colors.white),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)]));return t
def col(a):
    a=a.lower()
    return UP if a.startswith(('comprar','incrementar')) else DN if a.startswith('evitar') else WA if a.startswith('subponderar') else MU
def hdr(c,d):
    c.saveState();c.setFillColor(INK);c.rect(0,A4[1]-14*mm,A4[0],14*mm,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#22d3ee'));c.setLineWidth(1.2);c.rect(12*mm,A4[1]-11.5*mm,9*mm,9*mm)
    c.setFillColor(colors.HexColor('#22d3ee'));c.setFont('Helvetica-Bold',10);c.drawCentredString(16.5*mm,A4[1]-8.3*mm,'MP')
    c.setFillColor(colors.white);c.setFont('Helvetica-Bold',9);c.drawString(24*mm,A4[1]-8.3*mm,'MERPAZ CONSULTORES  ·  OBSERVATORIO DE INVERSIÓN')
    c.setFont('Helvetica',7.5);c.drawRightString(A4[0]-12*mm,A4[1]-8.3*mm,'Cierre '+D['corte'])
    c.setFillColor(MU);c.setFont('Helvetica',6.5);c.drawString(12*mm,8*mm,'Información referencial elaborada con datos públicos. No constituye asesoría financiera.');c.drawRightString(A4[0]-12*mm,8*mm,'Pág. %d'%d.page);c.restoreState()
doc=SimpleDocTemplate(sys.argv[2],pagesize=A4,leftMargin=12*mm,rightMargin=12*mm,topMargin=19*mm,bottomMargin=14*mm,title='Observatorio de Inversión MERPAZ '+D['corte'],author='MERPAZ Consultores')
E=[P('REPORTE DIARIO',EY),P('Observatorio de Inversión',H1),P('Cierre de mercado '+D['corte']+' · generado '+D['generado'],S),Spacer(1,5)]
k=D['kpis'];kr=[[P(x[0],S) for x in k],[P(x[1],st('kv',f='Helvetica-Bold',fontSize=12,leading=14,textColor=CY)) for x in k],[P(x[2] if len(x)>2 else '',S) for x in k]]
A=D['alerta'];acol=UP if A['nivel']=='fuerte' else WA
ab=[[Paragraph(A['tit'].upper(),st('at',f='Helvetica-Bold',fontSize=11,leading=14,textColor=acol))]]+[[Paragraph('<b><font color="%s">%s:</font></b> <b>%s</b>. %s <font color="#5b6b75">(%s)</font>'%('#be123c' if i['c']=='down' else '#15803d',i['k'],i['t'].replace('&','&amp;'),i['d'].replace('&','&amp;'),i['perf']),C)] for i in A['items']]
at=Table(ab,colWidths=[186*mm]);at.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.4,acol),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fffbeb')),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
E+=[at,Spacer(1,5)]
E+= [tbl(kr,[31*mm]*len(k),head=False),Spacer(1,4),P('Lectura del día',H2),P(D['contexto'],B)]
E+=[P('SDIRM · Sistema de Detección de Ineficiencias y Riesgos de Mercado',H2)]
rows=[[P('Activo',CB),P('Modelo',CB),P('Puntaje',CB),P('Señal',CB),P('Hipótesis',CB)]]+[[P(r[0],CB),P(r[1],S),P(r[2].split('\n')[-1]),P(r[3]),P(r[4],S)] for r in D['rank']]
E+=[tbl(rows,[34*mm,26*mm,14*mm,20*mm,92*mm])]
E+=[P('Monitor de ventas forzadas',H2),tbl([[P('Valor',CB),P('Indicador',CB),P('Lectura',CB),P('Estado',CB)]]+[[P(a[0]),P(a[1],CB),P(a[2],S),P(a[3])] for a in D['alerts']],[22*mm,38*mm,108*mm,18*mm])]
if D.get('empresas'):
    er=[[P('Empresa',CB),P('Sector',CB),P('ISR',CB),P('Veredicto',CB),P('Dividendo',CB),P('Riesgo principal',CB)]]
    for x in D['empresas']:
        vc=UP if x['isr']>=70 else WA if x['isr']>=55 else DN
        er.append([P(x['n'],CB),P(x['sec']+' · '+x['pais'],S),P(str(x['isr'])),Paragraph(x['ver'],st('v'+x['t'],f='Helvetica-Bold',fontSize=7.6,leading=10,textColor=vc)),P((('%.2f'%x['div']).replace('.',',')+'%') if x['div'] else 'No paga',S),P(x['riesgo'],S)])
    E.append(KeepTogether([P('Empresas sólidas y rentables · Índice ISR MERPAZ',H2),tbl(er,[36*mm,30*mm,10*mm,28*mm,19*mm,63*mm])]))
for kname,t in [('conservador','Conservador'),('moderado','Moderado'),('agresivo','Agresivo')]:
    pf=D['perfiles'][kname];blk=[P('Recomendación · perfil '+t,H2),P(pf['desc'],B),Spacer(1,3)]
    blk.append(tbl([[P(x[0],S) for x in pf['sim']],[P(x[1],st('g',f='Helvetica-Bold',fontSize=11,leading=13,textColor=UP if x[1].startswith('+') else DN)) for x in pf['sim']],[P(x[2] if len(x)>2 else '',S) for x in pf['sim']]],[62*mm]*len(pf['sim']),head=False))
    rr=[[P('Acción',CB),P('Activo',CB),P('SDIRM',CB),P('Motivo',CB)]]
    for r in pf['recos']: rr.append([Paragraph(r[0],st('a'+r[0],f='Helvetica-Bold',fontSize=7.6,leading=10,textColor=col(r[0]))),P(r[1],CB),P(r[2]),P(r[3],S)])
    blk+=[Spacer(1,3),tbl(rr,[30*mm,44*mm,13*mm,99*mm])];E.append(KeepTogether(blk))
E+=[Spacer(1,6),P('Simulación con USD 10.000, escenario base y rango pesimista a optimista. Tablero interactivo y calculadora: archivo Observatorio_MERPAZ.html (se abre en cualquier navegador).',S)]
doc.build(E,onFirstPage=hdr,onLaterPages=hdr)
