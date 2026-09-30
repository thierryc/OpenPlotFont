"""Regression checks on the Glyphs-4-native saved source, not a constructed file."""
import unittest
from pathlib import Path
from plotfont.hershey import FACES, import_hershey
from test_plotfont import ROOT


class SavedGlyphsTests(unittest.TestCase):
    def test_native_saved_source_preserves_entire_repertoire_exactly(self):
        for face, settings in FACES.items():
            with self.subTest(face=face):
                self.check_saved_source(face, settings)

    def check_saved_source(self, face, settings):
        try:
            from openstep_plist import loads
        except ImportError:
            self.skipTest('Install requirements-dev.txt to inspect the native saved source')
        package = ROOT/'fonts'/('hershey-'+face)/(settings['family'].replace(' ', '')+'.glyphspackage')
        info = loads((package/'fontinfo.plist').read_text())
        reference = import_hershey(ROOT/'vendor/hershey'/settings['file'], face)
        self.assertEqual(int(info['unitsPerEm']), reference['unitsPerEm'])
        self.assertEqual(info['properties'][0]['values'][0]['value'], reference['familyName'])
        master = info['fontMaster'][0]
        self.assertEqual(master['name'], 'Regular')
        metrics = dict(zip((m['type'] for m in info['metrics']), master['metricValues']))
        for native, expected in [('ascender','ascender'),('cap height','capHeight'),('x-height','xHeight'),('descender','descender')]:
            self.assertEqual(float(metrics[native]['pos']), reference['metrics'][expected])
        expected = {g['name']:g for g in reference['glyphs']}
        files = list((package/'glyphs').glob('*.glyph'))
        self.assertEqual(len(files), 97)
        observed = set()
        for path in files:
            glyph = loads(path.read_text())
            record = expected[glyph['glyphname']]
            observed.add(glyph['glyphname'])
            mappings = [f"{int(glyph['unicode']):04X}"] if 'unicode' in glyph else []
            self.assertEqual(mappings, record['unicodes'])
            self.assertEqual(len(glyph['layers']), 1)
            layer = glyph['layers'][0]
            self.assertEqual(layer['layerId'], master['id'])
            self.assertEqual(float(layer['width']), record['advanceWidth'])
            paths = layer.get('shapes', [])
            self.assertEqual(len(paths), len(record['strokes']))
            for shape, operation in zip(paths, record['strokes']):
                self.assertEqual(bool(int(shape['closed'])), operation['closed'])
                self.assertEqual(len(shape['nodes']), len(operation['commands']))
                for node, command in zip(shape['nodes'], operation['commands']):
                    self.assertEqual(node[2], 'l')
                    self.assertEqual([float(node[0]),float(node[1])], command[1:])
            if glyph['glyphname'] != '.notdef':
                stored = glyph['userData']['org.plotfont.hershey']
                source = record['userData']['org.plotfont.hershey']
                self.assertEqual(int(stored['row']), source['row'])
                self.assertEqual(int(stored['sourceId']), source['sourceId'])
        self.assertEqual(observed, set(expected))
