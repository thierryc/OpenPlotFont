# MenuTitle: Prepare original OpenPlotFont Pen-profile demo
# Requires an explicitly bound new empty qualification font; does not save.
import json, math, objc
from pathlib import Path
from GlyphsApp import GSGlyph, GSPath, GSNode, GSComponent, LINE, CURVE, OFFCURVE
assert str(font.familyName)=='OpenPlotFont Original Pen Qualification'
assert len(font.glyphs)==0
PP=objc.lookUpClass('GSPenPoint')
def value(o,k):
 v=getattr(o,k);return v() if callable(v) else v
def record(pp):
 return {k:float(value(pp,k)) for k in ('t','width','height','angle','strokePosition','progressionIn','progressionOut')}
def geo(p):
 return {'closed':bool(p.closed),'nodes':[[float(n.position.x),float(n.position.y),str(n.type)] for n in p.nodes]}
report={'default':record(PP.alloc().init()),'fixtures':{}}
for name in ['.notdef','space','constant','linear','progression','ellipse','offset','cubic','loop','inherited']:
 g=GSGlyph(name);font.glyphs.append(g);l=g.layers[font.masters[0].id];l.width=650
 if name=='space':g.unicode='0020';continue
 p=GSPath();p.closed=name=='loop'
 specs=[(50.125,200.25,LINE),(550.125,200.25,LINE)]
 if name=='cubic':specs=[(50.125,200.25,LINE),(100,500,OFFCURVE),(450,-100,OFFCURVE),(550.125,200.25,CURVE)]
 if name=='loop':specs=[(50.125,100.25,LINE),(550.125,100.25,LINE),(550.125,500.25,LINE),(50.125,500.25,LINE)]
 for x,y,t in specs:p.nodes.append(GSNode((x,y),type=t))
 l.shapes.append(p)
 for k,v in {'fill':False,'strokeWidth':40.,'strokeHeight':40.,'strokeAngle':0.,'strokePos':0.,'lineJoin':1,'lineCapStart':1,'lineCapEnd':1}.items():p.attributes[k]=v
 if name not in ('.notdef','inherited'):
  start=PP.alloc().initWithT_width_height_position_angle_progIn_progOut_(0.,20. if name in ('linear','progression') else 40.,20. if name in ('linear','progression') else (20. if name=='ellipse' else 40.),.5 if name=='offset' else 0.,30. if name=='ellipse' else 0.,0.,.6 if name=='progression' else 0.)
  end=PP.alloc().initWithT_width_height_position_angle_progIn_progOut_(1.,80. if name in ('linear','progression') else 40.,80. if name in ('linear','progression') else (20. if name=='ellipse' else 40.),.5 if name=='offset' else 0.,30. if name=='ellipse' else 0.,.6 if name=='progression' else 0.,0.)
  p.nodes[-1].setAssociatedPenPoints_([start,end])
 if name=='inherited':
  pp=PP.alloc().init();pp.setT_(.37);p.nodes[-1].setAssociatedPenPoints_([pp])
 report['fixtures'][name]={'geometry':geo(p),'attributes':{str(k):str(p.attributes[k]) for k in p.attributes},'points':[{'node':i,**record(pp)} for i,n in enumerate(p.nodes) for pp in n.associatedPenPoints() or []],'expanded':[geo(q) for q in p.expandedStroke()]}
Path(params['destination']).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps({'fixtures':len(report['fixtures']),'default':report['default']}))

for name,code in zip(['constant','linear','progression','ellipse','offset','cubic','loop','inherited'],range(0x41,0x49)):
 font.glyphs[name].unicode=f'{code:04X}'
font.userData['org.openplotfont.font']={'id':'org.openplotfont.pen-profile-demo','metadata':{'author':'OpenPlotFont contributors','license':'MIT','description':'Original synthetic fixtures; no font reconstruction or upstream artwork.'}}
# An independent dot and body test the pen-up boundary.
g=GSGlyph('separate');g.unicode='0049';font.glyphs.append(g);l=g.layers[font.masters[0].id];l.width=400
for coordinates in [[(100.125,0.25),(100.125,350.25)],[(100.125,450.25),(100.125,465.25)]]:
 p=GSPath();p.closed=False
 for xy in coordinates:p.nodes.append(GSNode(xy,type=LINE))
 l.shapes.append(p)
 for k,v in {'fill':False,'strokeWidth':40.,'strokeHeight':40.,'lineJoin':1,'lineCapStart':1,'lineCapEnd':1}.items():p.attributes[k]=v
# A profile component is intentionally nonexporting, for rejection qualification.
g=GSGlyph('componentDiagnostic');g.export=False;font.glyphs.append(g)
g.layers[font.masters[0].id].shapes.append(GSComponent('constant'))
print('Assigned original demo mappings and added independent strokes plus nonexporting component diagnostic.')
