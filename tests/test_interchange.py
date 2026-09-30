"""Compare produced SVG with a separate JS font consumer and analytic fixtures."""
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from plotfont import load, render_svg
from plotfont.hershey import FACES
from test_plotfont import ROOT, example, NS


@unittest.skipUnless(shutil.which('node'), 'Independent interchange check requires Node.js (provided in CI)')
class IndependentInterchangeTests(unittest.TestCase):
    def check(self, font_path, text, *, altered=None):
        with tempfile.TemporaryDirectory() as directory:
            svg = render_svg(load(font_path), text, 8)
            if altered:
                svg = altered(svg)
            path = Path(directory)/'drawing.svg'
            path.write_text(svg)
            return subprocess.run(['node', str(ROOT/'scripts/verify_svg.mjs'), str(font_path), str(path), text, '8'],
                                  capture_output=True, text=True)

    def test_full_hershey_repertoire_and_line_metrics(self):
        text = ''.join(chr(u) for u in range(32, 127))+'\nHello! ☃'
        result = self.check(ROOT/'fonts/hershey-roman-simplex/HersheyRomanSimplex.plotfont.json', text)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_native_export_render_matches_source_reference(self):
        text = ''.join(chr(u) for u in range(32,127))+'\nHershey 0123456789 ☃'
        for face, settings in FACES.items():
            with self.subTest(face=face):
                source = load(ROOT/'fonts'/('hershey-'+face)/(settings['family'].replace(' ', '')+'.plotfont.json'))
                native_path = ROOT/'examples'/('hershey-'+face+'.plotfont.json')
                self.assertEqual(render_svg(source,text,8),render_svg(load(native_path),text,8))
                result = self.check(native_path,text)
                self.assertEqual(result.returncode,0,result.stderr)

    def test_curves_fills_holes_and_independent_script_paths(self):
        for name, text in [('mixed', 'i i'), ('script', 'un\nun'), ('minimal', 'AA ☃')]:
            result = self.check(ROOT/'examples'/f'{name}.plotfont.json', text)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_curated_additional_hershey_specimens(self):
        text = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789 !?.,:;+-*/()\n'
                'The quick brown fox jumps over the lazy dog.')
        for face in ('roman-duplex', 'roman-triplex', 'script-simplex'):
            with self.subTest(face=face):
                result = subprocess.run([
                    'node', str(ROOT/'scripts/verify_svg.mjs'),
                    str(ROOT/'examples'/('hershey-'+face+'.plotfont.json')),
                    str(ROOT/'examples/specimens'/('hershey-'+face+'.svg')), text, '8'],
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_checker_detects_geometry_and_fill_corruption(self):
        for mutate in (lambda s: s.replace('fill-rule="evenodd"', 'fill-rule="nonzero"'),
                       lambda s: s.replace(' d="M ', ' d="L ', 1)):
            result = self.check(ROOT/'examples/mixed.plotfont.json', 'i', altered=mutate)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('mismatch', result.stderr)


class PreviewBoundsTests(unittest.TestCase):
    def test_round_caps_and_joins_make_half_width_padding_sufficient(self):
        tree = ET.fromstring(render_svg(example(), 'A', cap_height_mm=14, margin_mm=0, stroke_width_mm=2))
        for path in tree.findall('s:path', NS):
            self.assertEqual(path.get('stroke-linecap'), 'round')
            self.assertEqual(path.get('stroke-linejoin'), 'round')
        x, y, w, h = map(float, tree.get('viewBox').split())
        self.assertLessEqual(x, 0)
        self.assertGreaterEqual(x+w, 12)
        self.assertLessEqual(y, -15)
        self.assertGreaterEqual(y+h, 1)
