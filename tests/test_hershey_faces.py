"""Pinned extra faces: complete repertoire, exact strokes, identity and native guards."""
import hashlib
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from openplotfont import ValidationError, load
from openplotfont.comparison import compare_fonts
from openplotfont.glyphs_export import export_font
from openplotfont.glyphs_hershey import populate_hershey
from openplotfont.hershey import FACES, import_hershey, parse_jhf
from test_hershey_native_adapter import Glyph, Layer, fixture
from test_glyphs_adapter import Obj
from test_openplotfont import ROOT


class HersheyFaceTests(unittest.TestCase):
    def test_every_pinned_point_stroke_mapping_and_advance(self):
        for face, settings in FACES.items():
            with self.subTest(face=face):
                source = ROOT / 'vendor/hershey' / settings['file']
                raw = source.read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), settings['sha256'])
                records = parse_jhf(raw.decode('ascii'))
                font = import_hershey(source, face)
                stored = ROOT / 'fonts' / ('hershey-' + face) / (settings['family'].replace(' ', '') + '.opf.json')
                self.assertEqual(font, load(stored))
                self.assertEqual(len(font['glyphs']), 97)
                self.assertEqual(sum(len(g['unicodes']) for g in font['glyphs']), 95)
                self.assertEqual(font['glyphs'][-1]['unicodes'], [])
                self.assertEqual(font['metadata']['sourceSha256'], settings['sha256'])
                for row, (record, glyph) in enumerate(zip(records, font['glyphs'][1:])):
                    self.assertEqual(glyph['advanceWidth'], (record['right'] - record['left']) * 50)
                    self.assertEqual(glyph['userData']['org.openplotfont.hershey'], {'row': row, 'sourceId': record['sourceId']})
                    self.assertEqual(len(glyph['strokes']), len(record['strokes']))
                    self.assertNotIn('connections', glyph)
                    for points, stroke in zip(record['strokes'], glyph['strokes']):
                        self.assertFalse(stroke['closed'])
                        self.assertEqual(stroke['commands'], [
                            ['M' if i == 0 else 'L', (x-record['left'])*50, (9-y)*50]
                            for i, (x, y) in enumerate(points)])

    def test_wrong_face_changed_bytes_and_unsupported_face_rejected(self):
        for face, settings in FACES.items():
            with tempfile.TemporaryDirectory() as directory:
                source = ROOT / 'vendor/hershey' / settings['file']
                wrong = 'roman-duplex' if face == 'roman-simplex' else 'roman-simplex'
                with self.assertRaisesRegex(ValidationError, 'pinned'):
                    import_hershey(source, wrong)
                changed = Path(directory) / settings['file']
                changed.write_bytes(source.read_bytes() + b'\n')
                with self.assertRaisesRegex(ValidationError, 'pinned'):
                    import_hershey(changed, face)
        with self.assertRaisesRegex(ValidationError, 'Unsupported Hershey face'):
            import_hershey(ROOT/'vendor/hershey/rowmans.jhf', 'unknown')

    def test_all_faces_population_and_export_preserve_semantics(self):
        for face, settings in FACES.items():
            with self.subTest(face=face):
                destination = '/project/' + settings['family'].replace(' ', '') + '.glyphspackage'
                font = fixture(destination)
                reference = populate_hershey(
                    font, ROOT/'vendor/hershey'/settings['file'], destination, face=face,
                    glyph_type=Glyph, layer_type=Layer, path_type=lambda: Obj(nodes=[]),
                    node_type=lambda pt, type: Obj(position=Obj(x=pt[0], y=pt[1]), type=type), line_type='line')
                self.assertTrue(compare_fonts(reference, export_font(font, 'master', {'line': 'line'})))
                with self.assertRaisesRegex(ValidationError, 'existing'):
                    populate_hershey(font, ROOT/'vendor/hershey'/settings['file'], destination, face=face,
                                     glyph_type=Glyph, layer_type=Layer, path_type=None, node_type=None, line_type='line')

    def test_cli_selects_face_and_rejects_mislabeled_input_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            for face, settings in FACES.items():
                destination = Path(directory)/(face+'.opf.json')
                result = subprocess.run([sys.executable, '-m', 'openplotfont', 'import-hershey',
                                         str(ROOT/'vendor/hershey'/settings['file']), '--face', face,
                                         '-o', str(destination)], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(load(destination)['familyName'], settings['family'])
            failed = Path(directory)/'wrong.opf.json'
            result = subprocess.run([sys.executable, '-m', 'openplotfont', 'import-hershey',
                                     str(ROOT/'vendor/hershey/scripts.jhf'), '-o', str(failed)],
                                    cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('pinned', result.stderr)
            self.assertFalse(failed.exists())

    def test_script_metrics_include_descenders_and_no_invented_joins(self):
        font = import_hershey(ROOT/'vendor/hershey/scripts.jhf', 'script-simplex')
        self.assertEqual(font['metrics']['xHeight'], 450)
        self.assertEqual(font['metrics']['descender'], -600)
        g = next(g for g in font['glyphs'] if g['name'] == 'g')
        self.assertEqual(min(cmd[2] for s in g['strokes'] for cmd in s['commands']), -600)
        self.assertTrue(all('connections' not in g for g in font['glyphs']))

    def test_standalone_specimens_preserve_full_upstream_notice(self):
        notice = (ROOT/'vendor/hershey/NOTICE.txt').read_text()
        for face in FACES:
            with self.subTest(face=face):
                tree = ET.fromstring((ROOT/'examples/specimens'/('hershey-'+face+'.svg')).read_text())
                metadata = tree.find('{http://www.w3.org/2000/svg}metadata')
                self.assertIsNotNone(metadata)
                self.assertEqual(metadata.text, notice)
