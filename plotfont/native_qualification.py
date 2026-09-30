"""Execute in Glyphs 4 against the project font; fixtures use an invisible copy."""
from contextlib import ExitStack
from pathlib import Path
from .hershey import import_roman_simplex
from .glyphs_export import export_font
from .comparison import compare_fonts
from .storage import write_font, write_output
import json


def qualify_native(font, root):
    from GlyphsApp import GSFont, GSGlyph, GSLayer, GSPath, GSNode, GSAnchor, LINE, CURVE, QCURVE, OFFCURVE
    root = Path(root)
    source = root/'fonts/hershey-roman-simplex/HersheyRomanSimplex.glyphspackage'
    if str(font.filepath) != str(source):
        raise RuntimeError('Qualification requires the exact saved project font')
    types = {'line':LINE, 'curve':CURVE, 'qcurve':QCURVE, 'offcurve':OFFCURVE}
    reference = import_roman_simplex(root/'vendor/hershey/rowmans.jhf')
    result = export_font(font, font.masters[0].id, types)
    compare_fonts(reference, result)
    reopened = GSFont(str(source))
    compare_fonts(reference, export_font(reopened, reopened.masters[0].id, types))

    fixture = font.copy()
    master = fixture.masters[0]
    glyph = GSGlyph('plotfont.qualify')
    glyph.export = True
    glyph.unicodes = []
    fixture.glyphs.append(glyph)
    layer = GSLayer()
    layer.associatedMasterId = master.id
    getter = layer.temporarilyDisableRounding
    prior = bool(getter() if callable(getter) else getter)
    with ExitStack() as restore:
        restore.callback(layer.setTemporarilyDisableRounding_, prior)
        layer.setTemporarilyDisableRounding_(True)
        def path(nodes, closed):
            p = GSPath()
            p.closed = closed
            for x,y,kind in nodes:
                p.nodes.append(GSNode((x,y), type=kind))
            layer.shapes.append(p)
        path([(0.125,0,LINE),(12.75,20.125,OFFCURVE),(32.5,20.625,OFFCURVE),(50.125,0,CURVE)],False)
        path([(60,0,LINE),(80,0,LINE),(80,20,LINE),(60,20,LINE)],True)
        path([(65,5,LINE),(75,5,LINE),(75,15,LINE),(65,15,LINE)],True)
        path([(90.125,0,LINE),(100.25,20.5,OFFCURVE),(120.75,20.5,OFFCURVE),(130.125,0,QCURVE)],False)
        layer.width = 321.125
        anchor = GSAnchor()
        anchor.name = 'top'
        anchor.position = (42.5,93.75)
        anchor.userData['role'] = 'alignment'
        layer.anchors.append(anchor)
        glyph.layers[master.id] = layer
    glyph.userData['org.plotfont.glyph'] = {
        'operations':[{'kind':'stroke','pathIndex':0},{'kind':'fill','pathIndices':[1,2],'fillRule':'evenodd'},
                      {'kind':'stroke','pathIndex':3}],
        'connections':{'entry':{'strokeIndex':0,'endpoint':'start','userData':{'tag':'first'}},
                       'exit':{'strokeIndex':2,'endpoint':'end','userData':{'tag':'last'}}}}
    glyph.userData['org.plotfont.test'] = {'enabled':True,'fraction':0.125}
    fixture.glyphs['A'].rightKerningGroup = 'plotfont.test.left'
    fixture.glyphs['V'].leftKerningGroup = 'plotfont.test.right'
    fixture.glyphs['W'].leftKerningGroup = 'plotfont.test.right'
    fixture.setKerningForPair(master.id,'@MMK_L_plotfont.test.left','@MMK_R_plotfont.test.right',-12.5)
    fixture.setKerningForPair(master.id,'A','V',0)
    tested = export_font(fixture, master.id, types)
    record = next(g for g in tested['glyphs'] if g['name']=='plotfont.qualify')
    assert record['advanceWidth']==321.125
    assert record['strokes'][0]['commands']==[['M',0.125,0],['C',12.75,20.125,32.5,20.625,50.125,0]]
    assert record['strokes'][1]['kind']=='fill' and len(record['strokes'][1]['contours'])==2
    assert record['strokes'][2]['commands']==[['M',90.125,0],['Q',100.25,20.5,110.5,20.5],['Q',120.75,20.5,130.125,0]]
    assert record['anchors']==[{'name':'top','x':42.5,'y':93.75,'userData':{'role':'alignment'}}]
    assert record['connections']==glyph.userData['org.plotfont.glyph']['connections']
    assert record['userData']['org.plotfont.test']=={'enabled':True,'fraction':0.125}
    assert {'left':'A','right':'W','value':-12.5} in tested['kerning']
    assert not any(p['left']=='A' and p['right']=='V' for p in tested['kerning'])
    compare_fonts(reference, export_font(font, font.masters[0].id, types))
    write_font(root/'output/HersheyRomanSimplex.plotfont.json', result)
    write_font(root/'output/native-qualification-fixture.plotfont.json', tested)
    report={'glyphs':len(result['glyphs']),'mappings':sum(len(g['unicodes']) for g in result['glyphs']),
            'reopenedSourceVerified':True,'sourceUnchangedVerified':True,
            'checks':['cubic','implied-quadratic','fill-holes','anchors','user-data','connections',
                      'fractional-spacing','group-kerning','zero-exception']}
    write_output(root/'output/native-qualification.json',json.dumps(report,indent=2)+'\n')
    return report
