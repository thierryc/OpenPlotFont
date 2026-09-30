"""SDK-shaped doubles verify adapter logic; these are not native runtime tests."""

import copy
import unittest
from types import SimpleNamespace as Obj

from plotfont.glyphs_export import export_font, plain
from plotfont import ValidationError


class GlyphList(list):
    def __delitem__(self, key):
        if isinstance(key, str):
            self.remove(self[key])
        else:
            super().__delitem__(key)

    def __getitem__(self, key):
        if isinstance(key, str):
            return next((g for g in self if g.name == key), None)
        return super().__getitem__(key)


class Layer:
    def __init__(self, paths):
        self.paths = paths
        self.shapes = paths
        self.width = 650.125
        self.components = []
        self.anchors = [Obj(name='top', position=Obj(x=300.5,y=800.25),userData={'role':'alignment'})]
        self.hints = []

    def copyDecomposedLayer(self):
        return copy.deepcopy(self)


def font_fixture():
    def path(points,closed=False):
        return Obj(closed=closed,nodes=[Obj(type='line',position=Obj(x=x,y=y)) for x,y in points])
    paths = [path([(50.125,0),(300,700),(550,0)]),path([(150,280),(450,280)])]
    glyphs = GlyphList()
    for name, unicodes in [('.notdef',[]),('A',['0041']),('V',['0056'])]:
        glyphs.append(Obj(name=name,unicodes=unicodes,export=True,layers={'master':Layer(paths)},
                          userData={'note':'keep'},rightKerningGroup='A',leftKerningGroup='V'))
    font = Obj(familyName='Adapter Fixture',upm=1000,userData={'org.plotfont.font':{'id':'adapter-fixture'}},glyphs=glyphs,
               masters=[Obj(id='master',name='Regular',ascender=800,descender=-200,capHeight=700,xHeight=500)],features=[])
    font.kerningForPair = lambda master,left,right: {('A','V'):0,('@MMK_L_A','@MMK_R_V'):-25}.get((left,right))
    return font


class AdapterTests(unittest.TestCase):
    def test_complete_export_preserves_source_and_zero_exception(self):
        font = font_fixture()
        source = copy.deepcopy(font.glyphs[1].layers['master'].__dict__)
        result = export_font(font,'master',{'line':'line'})
        glyph = result['glyphs'][1]
        self.assertEqual(glyph['advanceWidth'],650.125)
        self.assertEqual(glyph['strokes'][0]['commands'][0],['M',50.125,0.0])
        self.assertEqual(glyph['userData'],{'note':'keep'})
        self.assertEqual(glyph['anchors'][0]['userData'],{'role':'alignment'})
        self.assertNotIn({'left':'A','right':'V','value':-25},result['kerning'])
        self.assertIn({'left':'V','right':'A','value':-25},result['kerning'])
        self.assertEqual(font.glyphs[1].layers['master'].width,source['width'])
        self.assertEqual(font.glyphs[1].layers['master'].paths[0].nodes[0].position.x,50.125)
        self.assertNotIn('glyphsMasterId',font.userData['org.plotfont.font'])

    def test_filled_group_and_connections(self):
        font = font_fixture()
        glyph = font.glyphs[1]
        for path in glyph.layers['master'].paths:
            path.closed = True
        glyph.userData['org.plotfont.glyph'] = {'operations':[{'kind':'fill','pathIndices':[0,1],'fillRule':'evenodd'}]}
        result = export_font(font,'master',{'line':'line'})
        self.assertEqual(len(result['glyphs'][1]['strokes']),1)
        self.assertEqual(len(result['glyphs'][1]['strokes'][0]['contours']),2)

    def test_component_cycle_and_missing_master(self):
        font = font_fixture()
        font.glyphs[1].layers['master'].components = [Obj(componentName='A')]
        with self.assertRaisesRegex(ValidationError,'component cycle'):
            export_font(font,'master',{'line':'line'})
        with self.assertRaisesRegex(ValidationError,'master does not exist'):
            export_font(font,'missing',{'line':'line'})

    def test_invalid_font_metadata_and_feature_warnings(self):
        font = font_fixture()
        font.userData['org.plotfont.font']['metadata'] = []
        with self.assertRaisesRegex(ValidationError, 'metadata must be an object'):
            export_font(font, 'master', {'line':'line'})
        font = font_fixture()
        font.features = [Obj(name='liga', active=True), Obj(name='dlig', active=False)]
        result = export_font(font, 'master', {'line':'line'})
        self.assertEqual(result['metadata']['exportWarnings'], ['OpenType features not executed: liga'])

    def test_native_none_unicode_is_unencoded(self):
        font = font_fixture()
        font.glyphs[0].unicodes = None
        self.assertEqual(export_font(font, 'master', {'line':'line'})['glyphs'][0]['unicodes'], [])

    def test_native_string_master_id_is_normalized(self):
        class NativeString(str):
            pass
        font = font_fixture()
        font.masters[0].id = NativeString('master')
        result = export_font(font, font.masters[0].id, {'line':'line'})
        self.assertIs(type(result['metadata']['glyphsMasterId']), str)

    def test_binary_userdata_is_actionable(self):
        with self.assertRaisesRegex(ValidationError,'binary'):
            plain({'image':b'cannot serialize'})


if __name__ == '__main__':
    unittest.main()
