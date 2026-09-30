"""Portable regression checks on artifacts actually generated inside Glyphs 4."""
import unittest
from plotfont import load
from plotfont.comparison import compare_fonts
from plotfont.hershey import FACES
from test_plotfont import ROOT


class NativeExportArtifactTests(unittest.TestCase):
    def test_hershey_native_export_matches_pinned_preparation(self):
        for face, settings in FACES.items():
            with self.subTest(face=face):
                expected = load(ROOT/'fonts'/('hershey-'+face)/(settings['family'].replace(' ', '')+'.plotfont.json'))
                actual = load(ROOT/'examples'/('hershey-'+face+'.plotfont.json'))
                self.assertTrue(compare_fonts(expected, actual))
                self.assertEqual(actual['metadata']['exportWarnings'], [])

    def test_native_curves_fills_and_metadata(self):
        font = load(ROOT/'tests/fixtures/native-qualification.plotfont.json')
        glyph = next(g for g in font['glyphs'] if g['name']=='plotfont.qualify')
        self.assertEqual(glyph['advanceWidth'],321.125)
        self.assertEqual(glyph['strokes'][0]['commands'][1],['C',12.75,20.125,32.5,20.625,50.125,0])
        self.assertEqual(glyph['strokes'][1]['fillRule'],'evenodd')
        self.assertEqual(len(glyph['strokes'][1]['contours']),2)
        self.assertEqual(glyph['strokes'][2]['commands'],[
            ['M',90.125,0],['Q',100.25,20.5,110.5,20.5],['Q',120.75,20.5,130.125,0]])
        self.assertEqual(glyph['anchors'][0]['userData'],{'role':'alignment'})
        self.assertEqual(glyph['connections']['entry']['userData'],{'tag':'first'})
        self.assertEqual(glyph['connections']['exit']['strokeIndex'],2)
        self.assertIs(glyph['userData']['org.plotfont.test']['enabled'],True)

    def test_native_group_kerning_and_zero_exception(self):
        font = load(ROOT/'tests/fixtures/native-qualification.plotfont.json')
        self.assertIn({'left':'A','right':'W','value':-12.5},font['kerning'])
        self.assertFalse(any(p['left']=='A' and p['right']=='V' for p in font['kerning']))
