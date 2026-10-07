"""Geometry and saved-package checks for reviewed stroke font conversion."""
import json
import math
from pathlib import Path
import tempfile
import unittest

from openplotfont.comparison import compare_fonts
from openplotfont.glyphs_package import write_package, read_package
from openplotfont.stroke_import import import_svg, import_lff, svg_paths, arc_cubics
from openplotfont.validation import ValidationError


SVG = '''<svg xmlns="http://www.w3.org/2000/svg"><defs><font horiz-adv-x="600">
<font-face units-per-em="1000" ascent="800" descent="200" cap-height="700" x-height="500"/>
<missing-glyph/><glyph glyph-name="space" unicode=" " horiz-adv-x="250"/>
<glyph glyph-name="A" unicode="A" d="M0 0l300 700 300 -700M120 250h360"/>
<glyph glyph-name="O" unicode="O" d="M100 0Q0 100 100 200C200 200 200 0 100 0z"/>
<glyph glyph-name="g" unicode="g" d="M0.125 -130.25c100 0 100 200 0 200"/>
<glyph glyph-name="fi" unicode="fi" d="M0 0v700M200 0v500"/>
<hkern g1="A" g2="O" k="30"/></font></defs></svg>'''


class StrokeImportTests(unittest.TestCase):
    def test_paths_spacing_closure_curves_and_package_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.svg'; path.write_text(SVG)
            with self.assertRaises(ValidationError):
                import_svg(path, identity='test', family='Test', metadata={})
            font = import_svg(path, identity='test', family='Test', metadata={}, stroke_source=True)
            glyphs = {g['name']: g for g in font['glyphs']}
            self.assertEqual(len(glyphs['A']['strokes']), 2)
            self.assertFalse(glyphs['A']['strokes'][0]['closed'])
            self.assertTrue(glyphs['O']['strokes'][0]['closed'])
            self.assertEqual(glyphs['g']['strokes'][0]['commands'][0], ['M', .125, -130.25])
            self.assertEqual(glyphs['space']['advanceWidth'], 250)
            self.assertEqual(glyphs['space']['strokes'], [])
            self.assertEqual(glyphs['fi']['unicodes'], [])
            self.assertEqual(font['metrics']['descender'], -200)
            self.assertEqual(font['kerning'], [{'left': 'A', 'right': 'O', 'value': -30}])
            self.assertTrue(glyphs['.notdef']['strokes'])
            self.assertEqual(glyphs['source.notdef']['strokes'], [])
            package = Path(folder) / 'Test.glyphspackage'; write_package(font, package)
            compare_fonts(font, read_package(package))
            with self.assertRaises(FileExistsError): write_package(font, package)

    def test_arc_error_and_direction(self):
        for sweep in [math.pi, -math.pi, 2*math.pi]:
            commands = list(arc_cubics((0, 0), 100, 100, 0, 0, sweep,
                                     (100*math.cos(sweep), 100*math.sin(sweep))))
            current = (100, 0)
            for c in commands:
                points = [current, tuple(c[1:3]), tuple(c[3:5]), tuple(c[5:7])]
                for i in range(101):
                    t = i/100
                    x,y = [sum(w*p[axis] for w,p in zip([(1-t)**3,3*t*(1-t)**2,3*t*t*(1-t),t**3],points)) for axis in [0,1]]
                    self.assertLessEqual(abs(math.hypot(x,y)-100), 100*1e-7)
                current = points[-1]
            self.assertAlmostEqual(current[0], 100*math.cos(sweep))
            self.assertGreater(commands[0][2]*sweep, 0)

    def test_svg_arc_normalization_and_penup_only_metadata(self):
        strokes = svg_paths('M100 0A100 100 0 0 1 0 100M0 0l0 1')
        self.assertEqual(len(strokes), 2)
        self.assertEqual(strokes[0]['commands'][-1][-2:], [0, 100])
        self.assertEqual(len(strokes[0]['commands']), 19)
        moves = []
        self.assertEqual(svg_paths('M10 20z', moves), [])
        self.assertEqual(moves[0]['commands'], [['M', 10, 20]])

    def test_lff_references_curves_spacing_and_cycles(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.lff'
            path.write_text('# LetterSpacing: 2\n# WordSpacing: 5\n[0041]\n2,0;4,0,A1\n[0042]\nC0041\n1,0;1,5\n')
            font = import_lff(path, identity='lff', family='LFF', metadata={})
            a,b = font['glyphs'][1:3]
            self.assertEqual(len(b['strokes']), 2)
            self.assertEqual(a['strokes'][0], b['strokes'][0])
            self.assertEqual(a['advanceWidth'], 600)
            self.assertEqual(a['strokes'][0]['commands'][0], ['M', 200, 0])
            self.assertEqual(a['strokes'][0]['commands'][-1][-2:], [400, 0])
            path.write_text('[0041]\nC0041\n')
            with self.assertRaises(ValidationError): import_lff(path, identity='bad', family='Bad', metadata={})

    def test_unsafe_source_names_keep_mapping_and_attribution(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'names.svg'
            path.write_text(SVG.replace('glyph-name="A" unicode="A"', 'glyph-name="_" unicode="A"').replace('g1="A"', 'g1="_"'))
            font = import_svg(path, identity='names', family='Names', metadata={}, stroke_source=True)
            a = next(g for g in font['glyphs'] if g['unicodes'] == ['0041'])
            self.assertEqual(a['name'], 'uni0041')
            self.assertEqual(a['userData']['org.openplotfont.source']['glyphName'], '_')
            self.assertEqual(font['kerning'][0]['left'], 'uni0041')

    def test_unsupported_geometry_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'bad.svg'
            path.write_text(SVG.replace('<missing-glyph/>', '<missing-glyph><path d="M0 0L1 1"/></missing-glyph>'))
            with self.assertRaises(ValidationError): import_svg(path, identity='bad', family='Bad', metadata={}, stroke_source=True)
            path.write_text(SVG.replace('<defs>', '<defs transform=\"translate(10,20)\">'))
            with self.assertRaises(ValidationError): import_svg(path, identity='bad', family='Bad', metadata={}, stroke_source=True)


if __name__ == '__main__': unittest.main()
