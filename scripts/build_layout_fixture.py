"""Reproducible original OpenType/PlotFont shaping fixture (not a native Glyphs export)."""
import io
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from plotfont.layout import attach_layout
from plotfont.storage import write_font, write_output


PREFIX = '''languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem latn TRK;
markClass acutecomb <anchor 0 0> @TOP;
markClass dotcomb <anchor 0 0> @TOP;
'''
FEATURES = {
    'liga':'sub f i by f_i;',
    'ss01':'sub A by A.alt;',
    'salt':'sub A from [A.alt];',
    'calt':"lookupflag IgnoreMarks; sub A A' by A.alt;",
    'tnum':'sub zero by zero.tnum;',
    'locl':'script latn; language TRK; sub i by i.trk;',
    'kern':'pos A A -80;',
    'mark':'''pos base A <anchor 300 700> mark @TOP;
pos ligature f_i <anchor 250 700> mark @TOP ligComponent <anchor 700 700> mark @TOP;''',
    'mkmk':'pos mark acutecomb <anchor 0 150> mark @TOP;',
    'curs':'pos cursive u <anchor 0 0> <anchor 400 100>; pos cursive n <anchor 0 0> <anchor 400 0>;',
}


def geometry():
    def glyph(name, code, width, points, *, anchors=None):
        return {'name':name,'unicodes':[] if code is None else [f'{code:04X}'],'advanceWidth':width,
                'strokes':[] if not points else [{'closed':False,'commands':[
                    ['M' if i==0 else 'L',x,y] for i,(x,y) in enumerate(points)]}],
                **({'anchors':anchors} if anchors else {})}
    return {'format':'PlotFont','version':'0.3','id':'org.plotfont.layout-demo.regular',
            'familyName':'PlotFont Layout Demo','styleName':'Regular','unitsPerEm':1000,
            'metrics':{'ascender':800,'descender':-200,'capHeight':700,'xHeight':500,'lineGap':200},
            'missingGlyph':'.notdef','kerning':[{'left':'A','right':'A','value':-80}],
            'metadata':{'license':'MIT','author':'Thierry Charbonnel',
                        'purpose':'Original conformance fixture; strokes are intentionally simple.'},
            'glyphs':[
                glyph('.notdef',None,600,[(50,0),(50,700),(550,700),(550,0),(50,0)]),
                {**glyph('space',32,300,[]),'unicodes':['0020','00A0']},
                glyph('A',65,600,[(50,0),(300,700),(550,0)],anchors=[{'name':'top','x':300,'y':700}]),
                glyph('A.alt',None,600,[(50,0),(300,600),(550,0)]),
                glyph('f',102,400,[(100,0),(100,500),(300,700)]),
                glyph('i',105,250,[(100,0),(100,500)]),
                glyph('f_i',None,600,[(100,0),(100,500),(300,700),(500,500),(500,0)]),
                glyph('i.trk',None,250,[(100,0),(100,450)]),
                glyph('zero',48,450,[(50,0),(50,700),(400,700),(400,0),(50,0)]),
                glyph('zero.tnum',None,600,[(100,0),(100,700),(500,700),(500,0),(100,0)]),
                glyph('acutecomb',0x301,0,[(0,0),(100,100)],anchors=[{'name':'_top','x':0,'y':0},{'name':'top','x':0,'y':150}]),
                glyph('dotcomb',0x307,0,[(-20,0),(20,0)],anchors=[{'name':'_top','x':0,'y':0}]),
                glyph('u',117,500,[(0,0),(0,-100),(400,100)]),
                glyph('n',110,500,[(0,0),(200,400),(400,0)]),
            ]}


def feature_text():
    return PREFIX + '\n'.join(f'feature {tag} {{\n{code}\n}} {tag};' for tag,code in FEATURES.items()) + '\n'


def compile_fixture(data, source):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    builder = FontBuilder(data['unitsPerEm'],isTTF=True)
    order = [g['name'] for g in data['glyphs']]
    builder.setupGlyphOrder(order)
    builder.setupCharacterMap({int(u,16):g['name'] for g in data['glyphs'] for u in g['unicodes']})
    # Empty outlines deliberately prevent this shaping payload becoming plotting artwork.
    builder.setupGlyf({name:TTGlyphPen(None).glyph() for name in order})
    builder.setupHorizontalMetrics({g['name']:(g['advanceWidth'],0) for g in data['glyphs']})
    builder.setupHorizontalHeader(ascent=800,descent=-200)
    builder.setupNameTable({'familyName':data['familyName'],'styleName':'Regular',
                           'uniqueFontIdentifier':data['id'],'fullName':data['familyName'],
                           'psName':'PlotFontLayoutDemo-Regular','version':'Version 0.003',
                           'copyright':'Copyright Thierry Charbonnel. MIT.'})
    builder.setupOS2(sTypoAscender=800,sTypoDescender=-200,usWinAscent=800,usWinDescent=200)
    builder.setupPost()
    builder.setupMaxp()
    builder.font['head'].created = builder.font['head'].modified = 3800000000
    builder.font.recalcTimestamp = False
    addOpenTypeFeaturesFromString(builder.font,source)
    stream = io.BytesIO()
    builder.font.save(stream)
    return stream.getvalue()


def build():
    data = geometry()
    source = feature_text()
    raw = compile_fixture(data,source)
    settings = {'ss01':{'label':'Lower apex capitals','recommendedValue':0},
                'salt':{'recommendedValue':0}, 'tnum':{'recommendedValue':0},
                'curs':{'recommendedValue':0}}
    font = attach_layout(data,raw,source=source,feature_settings=settings)
    write_font(ROOT/'examples/layout-demo.plotfont.json',font,force=True)
    write_output(ROOT/'tests/fixtures/layout-demo.fea',source,force=True)
    return font


if __name__ == '__main__':
    font = build()
    print('Built original layout fixture:',len(font['glyphs']),'glyphs')
