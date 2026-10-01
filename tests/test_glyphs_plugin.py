"""Exercise the built plugin action; doubles do not establish native UI support."""
import copy
import importlib.util
import plistlib
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

from test_glyphs_adapter import font_fixture
from test_plotfont import ROOT
from plotfont import load


class Widget:
    def __init__(self, *args, **kwargs):
        self._nsObject = self
        self.value = 0
    def addAutoPosSizeRules(self, *args): pass
    def setItems(self, items): self.items = items
    def set(self, value): self.value = value
    def get(self): return self.value


class PluginBase:
    def setFont_(self, font): self._font = font
    def font(self): return getattr(self, '_font', None)


class GlyphsPluginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        spec = importlib.util.spec_from_file_location('build_glyphs_plugin', ROOT/'scripts/build_glyphs_plugin.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        cls.bundle = builder.build(Path(cls.temp.name)/'PlotFont.glyphsFileFormat')
        api = ModuleType('GlyphsApp')
        cls.host = SimpleNamespace(versionNumber=4.1)
        api.Glyphs = cls.host
        api.GetSaveFile = lambda *args: None
        for name in ('LINE', 'CURVE', 'QCURVE', 'OFFCURVE'):
            setattr(api, name, name.lower())
        plugins = ModuleType('GlyphsApp.plugins')
        plugins.FileFormatPlugin = PluginBase
        objc = ModuleType('objc')
        objc.python_method = lambda method: method
        objc.super = super
        vanilla = ModuleType('vanilla')
        for name in ('Window', 'TextBox', 'Group', 'PopUpButton'):
            setattr(vanilla, name, Widget)
        with patch.dict(sys.modules, {'GlyphsApp': api, 'GlyphsApp.plugins': plugins,
                                     'objc': objc, 'vanilla': vanilla}):
            cls.namespace = runpy.run_path(str(cls.bundle/'Contents/Resources/plugin.py'))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
        for key in list(sys.modules):
            if key == '_plotfont_glyphs4' or key.startswith('_plotfont_glyphs4.'):
                sys.modules.pop(key)

    def setUp(self):
        self.host.versionNumber = 4.1
        self.plugin = self.namespace['PlotFontExporter']()
        self.plugin.settings()
        self.font = font_fixture()
        self.font.selectedFontMaster = self.font.masters[0]
        self.font.copy = lambda: copy.deepcopy(self.font)
        self.plugin.setFont_(self.font)
        self.output = tempfile.TemporaryDirectory()
        self.addCleanup(self.output.cleanup)
        self.path = Path(self.output.name)/'export.plotfont.json'

    def test_export_matches_adapter_and_preserves_source(self):
        before = copy.deepcopy(self.font.userData)
        success, message = self.plugin.export(self.font, str(self.path))
        self.assertTrue(success, message)
        data = load(self.path)
        self.assertEqual(data['version'], '0.3')
        self.assertNotIn('layout', data)
        self.assertEqual(data['id'], 'adapter-fixture')
        self.assertEqual(data['glyphs'][1]['strokes'][0]['commands'][0], ['M', 50.125, 0.0])
        self.assertEqual(len(data['glyphs'][1]['strokes']), 2)
        self.assertEqual(self.font.userData, before)
        self.assertEqual(self.plugin.exportPath, str(self.path))

    def test_new_font_needs_no_destination_or_id_metadata(self):
        self.font.userData = {}
        self.assertTrue(self.plugin.export(self.font, str(self.path))[0])
        first = load(self.path)['id']
        other = self.path.with_name('second.plotfont.json')
        self.assertTrue(self.plugin.export(self.font, str(other))[0])
        self.assertEqual(load(other)['id'], first)
        self.assertEqual(self.font.userData, {})

    def test_existing_file_and_symlink_preserved(self):
        self.path.write_text('keep')
        success, message = self.plugin.export(self.font, str(self.path))
        self.assertFalse(success)
        self.assertIn('already exists', message)
        self.assertEqual(self.path.read_text(), 'keep')
        link = self.path.with_name('link.plotfont.json')
        link.symlink_to(self.path)
        self.assertFalse(self.plugin.export(self.font, str(link))[0])
        self.assertTrue(link.is_symlink())
        self.assertEqual(self.path.read_text(), 'keep')

    def test_cancel_and_validation_failures_write_nothing(self):
        self.assertFalse(self.plugin.export(self.font)[0])
        self.assertFalse(self.plugin.export(self.font, str(self.path.with_name('invalid.json')))[0])
        del self.font.glyphs['.notdef']
        success, message = self.plugin.export(self.font, str(self.path))
        self.assertFalse(success)
        self.assertIn('missingGlyph', message)
        self.assertFalse(self.path.exists())

    def test_master_chooser_and_rebinding(self):
        second = copy.deepcopy(self.font.masters[0])
        second.id, second.name, second.capHeight = 'second', 'Tall', 900
        self.font.masters.append(second)
        for glyph in self.font.glyphs:
            glyph.layers['second'] = copy.deepcopy(glyph.layers['master'])
        self.plugin.setFont_(self.font)
        self.plugin.w.group.master.set(1)
        self.assertTrue(self.plugin.export(self.font, str(self.path))[0])
        self.assertEqual(load(self.path)['metrics']['capHeight'], 900)
        other = font_fixture()
        other.selectedFontMaster = other.masters[0]
        self.plugin.setFont_(other)
        self.assertEqual(self.plugin.chosen_master(other), 'master')
        self.assertEqual(self.plugin.w.group.master.items, ['Regular'])

        # Native copies have no document; selectedFontMaster is unavailable.
        class DetachedFont:
            parent = None
            masters = other.masters
            @property
            def selectedFontMaster(self):
                raise AssertionError('A detached copy has no selected master')
        detached = DetachedFont()
        self.plugin.setFont_(detached)
        self.assertEqual(self.plugin.chosen_master(detached), 'master')

    def test_removed_master_and_glyphs3_rejected(self):
        self.font.masters.clear()
        self.assertFalse(self.plugin.export(self.font, str(self.path))[0])
        self.host.versionNumber = 3
        self.assertIn('Glyphs 4', self.plugin.export(self.font, str(self.path))[1])
        self.assertFalse(self.path.exists())

    def test_export_all_directory_and_feature_warning(self):
        self.font.features = [SimpleNamespace(name='liga', active=True)]
        success, message = self.plugin.export(self.font, self.output.name)
        self.assertTrue(success, message)
        self.assertIn('OpenType features not executed: liga', message)
        self.assertEqual(load(self.plugin.exportPath)['version'], '0.3')
        self.assertNotIn('layout', load(self.plugin.exportPath))

    def test_bundle_is_self_contained_and_export_only(self):
        info = plistlib.loads((self.bundle/'Contents/Info.plist').read_bytes())
        self.assertNotIn('CFBundleDocumentTypes', info)
        self.assertEqual(info['NSPrincipalClass'], 'PlotFontExporter')
        self.assertEqual(info['CFBundleShortVersionString'], '0.1.1')
        package = self.bundle/'Contents/Resources/_plotfont_glyphs4'
        for name in ('glyphs_plugin', 'glyphs_export', 'validation', 'storage'):
            self.assertEqual((package/(name+'.py')).read_bytes(), (ROOT/'plotfont'/(name+'.py')).read_bytes())
