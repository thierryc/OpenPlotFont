"""Native adapter doubles: offline checks, not evidence of Glyphs execution."""
import copy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as Obj
from openplotfont import ValidationError
from openplotfont.glyphs_hershey import populate_hershey
from openplotfont.glyphs_export import export_font
from openplotfont.comparison import compare_fonts
from test_openplotfont import ROOT, example
from test_glyphs_adapter import GlyphList


class Layers(list):
    def __setitem__(self, key, value):
        if isinstance(key, str):
            value.layerId = key
            for i, layer in enumerate(self):
                if layer.layerId == key:
                    return super().__setitem__(i, value)
            self.append(value)
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key):
        return next((x for x in self if x.layerId == key), None) if isinstance(key, str) else super().__getitem__(key)


class Glyph:
    def __init__(self, name):
        self.name, self.userData, self.layers = name, {}, Layers()
        self.rightKerningGroup = self.leftKerningGroup = None


class Layer:
    def __init__(self):
        self.shapes, self.components, self.anchors, self.hints = [], [], [], []
        self.temporarilyDisableRounding = False

    @property
    def paths(self):
        return self.shapes

    def setTemporarilyDisableRounding_(self, value):
        self.temporarilyDisableRounding = value

    def copyDecomposedLayer(self):
        return copy.deepcopy(self)


def fixture(path):
    return Obj(filepath=str(path), glyphs=GlyphList(), masters=[Obj(id='master')], userData={},
               features=[], kerningForPair=lambda *args: None)


def populate(font, path, layer_type=Layer):
    return populate_hershey(font, ROOT/'vendor/hershey/rowmans.jhf', path, glyph_type=Glyph,
                             layer_type=layer_type, path_type=lambda: Obj(nodes=[]),
                             node_type=lambda pt, type: Obj(position=Obj(x=pt[0], y=pt[1]), type=type), line_type='line')


class NativeImportTests(unittest.TestCase):
    def test_all_source_geometry_survives_population_export(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'font.glyphs'
            font = fixture(path)
            reference = populate(font, path)
            self.assertTrue(compare_fonts(reference, export_font(font, 'master', {'line':'line'})))
            self.assertEqual(len(font.glyphs), 97)
            for glyph in font.glyphs:
                self.assertFalse(glyph.layers['master'].temporarilyDisableRounding)
            with self.assertRaisesRegex(ValidationError, 'empty font'):
                populate(font, path)

    def test_blank_native_template_and_truthy_empty_proxies(self):
        class Proxy(list):
            def __bool__(self):
                return True
        font = fixture('/project/font.glyphspackage')
        glyph = Glyph('A')
        layer = Layer()
        layer.shapes = Proxy()
        layer.anchors = Proxy()
        layer.hasBackground = lambda: False
        layer.layerId = 'master'
        glyph.layers.append(layer)
        font.glyphs.append(glyph)
        reference = populate(font, '/project/font.glyphspackage')
        self.assertTrue(compare_fonts(reference, export_font(font, 'master', {'line':'line'})))
        self.assertEqual(len(font.glyphs), 97)
        self.assertEqual(len(font.glyphs['A'].layers), 1)

    def test_nonempty_template_is_preserved(self):
        font = fixture('/project/font.glyphspackage')
        glyph = Glyph('A')
        layer = Layer()
        layer.shapes.append(Obj(nodes=[]))
        glyph.layers.append(layer)
        font.glyphs.append(glyph)
        with self.assertRaisesRegex(ValidationError, 'existing artwork'):
            populate(font, '/project/font.glyphspackage')
        self.assertEqual(font.glyphs[0].name, 'A')
        self.assertEqual(len(layer.shapes), 1)

    def test_reject_unrelated_document_without_changes(self):
        font = fixture('/some/other/font.glyphs')
        with self.assertRaisesRegex(ValidationError, 'exact saved'):
            populate(font, '/project/font.glyphs')
        self.assertEqual(len(font.glyphs), 0)
        self.assertEqual(font.userData, {})

    def test_missing_precision_api_stops_before_font_changes(self):
        font = fixture('/project/font.glyphs')
        with self.assertRaisesRegex(ValidationError, 'precision API'):
            populate(font, '/project/font.glyphs', layer_type=lambda: Obj())
        self.assertEqual(len(font.glyphs), 0)
        self.assertEqual(font.userData, {})


class ComparisonTests(unittest.TestCase):
    def test_defaults_and_export_diagnostics_allowed(self):
        source = example()
        actual = copy.deepcopy(source)
        actual.setdefault('metadata', {})['glyphsMasterId'] = 'master'
        actual['metadata']['exportWarnings'] = []
        self.assertTrue(compare_fonts(source, actual))

    def test_geometry_spacing_order_mapping_and_metadata_changes_detected(self):
        for mutate in (
            lambda f: f['glyphs'][2]['strokes'][0]['commands'][1].__setitem__(1, 333),
            lambda f: f['glyphs'][2].__setitem__('advanceWidth', 999),
            lambda f: f['glyphs'][2]['strokes'].reverse(),
            lambda f: f['glyphs'][2].__setitem__('unicodes', ['0042']),
            lambda f: f.setdefault('metadata', {}).__setitem__('license', 'changed'),
        ):
            actual = example()
            mutate(actual)
            with self.assertRaises(ValidationError):
                compare_fonts(example(), actual)
