"""Exercise the actual menu entry point with a supplied SDK-shaped font."""
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch
from test_openplotfont import ROOT
from test_glyphs_adapter import font_fixture
from openplotfont import load


class ExportScriptTests(unittest.TestCase):
    def test_selected_master_entrypoint_and_no_overwrite(self):
        api = ModuleType('GlyphsApp')
        api.Glyphs = SimpleNamespace(font=None,versionNumber=4.1)
        for name in ('LINE','CURVE','QCURVE','OFFCURVE'):
            setattr(api,name,name.lower())
        with patch.dict(sys.modules,{'GlyphsApp':api}):
            namespace = runpy.run_path(str(ROOT/'scripts/Export OpenPlotFont.py'))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'actual-script.opf.json'
            namespace['main'](font_fixture(),str(path),'master')
            self.assertEqual(load(path)['familyName'],'Adapter Fixture')
            original=path.read_bytes()
            with self.assertRaises(FileExistsError):
                namespace['main'](font_fixture(),str(path),'master')
            self.assertEqual(path.read_bytes(),original)

    def test_absent_master_fails_before_writing(self):
        api = ModuleType('GlyphsApp')
        api.Glyphs = SimpleNamespace(font=None,versionNumber=4.1)
        for name in ('LINE','CURVE','QCURVE','OFFCURVE'): setattr(api,name,name.lower())
        with patch.dict(sys.modules,{'GlyphsApp':api}):
            namespace=runpy.run_path(str(ROOT/'scripts/Export OpenPlotFont.py'))
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'absent.opf.json'
            with self.assertRaisesRegex(RuntimeError,'Select a master'):
                namespace['main'](font_fixture(),str(path),'missing')
            self.assertFalse(path.exists())

    def test_short_extension(self):
        api = ModuleType('GlyphsApp')
        api.Glyphs = SimpleNamespace(font=None, versionNumber=4.1)
        for name in ('LINE', 'CURVE', 'QCURVE', 'OFFCURVE'):
            setattr(api, name, name.lower())
        with patch.dict(sys.modules, {'GlyphsApp': api}):
            namespace = runpy.run_path(str(ROOT/'scripts/Export OpenPlotFont.py'))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'actual-script.opf'
            namespace['main'](font_fixture(), str(path), 'master')
            self.assertEqual(load(path)['format'], 'OpenPlotFont')
