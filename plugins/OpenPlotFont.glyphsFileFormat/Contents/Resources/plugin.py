# encoding: utf-8
"""OpenPlotFont geometry export for Glyphs 4, using the official SDK loader."""
import importlib.util
import sys
from pathlib import Path

import objc
from GlyphsApp import Glyphs, GetSaveFile, LINE, CURVE, QCURVE, OFFCURVE
from GlyphsApp.plugins import FileFormatPlugin
from vanilla import Window, TextBox, PopUpButton, Group

# A private package prevents another plugin's `openplotfont` module from taking over.
# Build with scripts/build_glyphs_plugin.py before installing this bundle.
_PACKAGE = '_openplotfont_glyphs4'
_RUNTIME = Path(__file__).resolve().parent / _PACKAGE
if _PACKAGE not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        _PACKAGE, _RUNTIME / '__init__.py', submodule_search_locations=[str(_RUNTIME)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[_PACKAGE] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(_PACKAGE, None)
        raise
from _openplotfont_glyphs4.glyphs_plugin import export_to_path

NODE_TYPES = {'line': LINE, 'curve': CURVE, 'qcurve': QCURVE, 'offcurve': OFFCURVE}


class OpenPlotFontExporter(FileFormatPlugin):
    @objc.python_method
    def settings(self):
        self.name = 'OpenPlotFont'
        self.icon = 'ExportIcon'
        self.toolbarPosition = 100
        self._master_ids = []
        self.exportPath = None
        self.w = Window((420, 180))
        self.w.group = Group('auto')
        self.w.group.heading = TextBox('auto', 'Export one master as OpenPlotFont (.opf.json)')
        self.w.group.masterLabel = TextBox('auto', 'Master')
        self.w.group.master = PopUpButton('auto', [])
        self.w.group.scope = TextBox('auto', 'OpenPlotFont v0.3 geometry. OpenType features are not compiled.')
        self.w.group.safety = TextBox('auto', 'Exports a copy. Choose a new filename; existing files are preserved.')
        self.w.group.addAutoPosSizeRules([
            'H:|-[heading]-|', 'H:|-[masterLabel]-[master(>=200)]-|',
            'H:|-[scope]-|', 'H:|-[safety]-|',
            'V:|-[heading(20@999)]-[master(26@999)]-[scope(40@999)]-[safety(40@999)]-|',
            'V:|-[heading]-[masterLabel(26@999)]',
        ], {})
        self.dialog = self.w.group._nsObject

    def setFont_(self, font):
        objc.super(OpenPlotFontExporter, self).setFont_(font)
        self._master_ids = [m.id for m in font.masters] if font is not None else []
        self.w.group.master.setItems([m.name for m in font.masters] if font is not None else [])
        # GSFont.selectedFontMaster delegates to its document. Invisible copies
        # have no document, so leave the popup at its first master in that case.
        selected = font.selectedFontMaster if font is not None and getattr(font, 'parent', None) is not None else None
        if selected is not None and selected.id in self._master_ids:
            self.w.group.master.set(self._master_ids.index(selected.id))

    @objc.python_method
    def chosen_master(self, font):
        # The native dialog is bound to a particular font. Never reuse its choice
        # for an unrelated programmatic export.
        if font == self.font() and self._master_ids:
            index = self.w.group.master.get()
            if index is not None and 0 <= index < len(self._master_ids):
                return self._master_ids[index]
        selected = font.selectedFontMaster if getattr(font, 'parent', None) is not None else None
        if selected is None and len(font.masters) == 1:
            return font.masters[0].id
        if selected is None:
            raise ValueError('Select a master before exporting OpenPlotFont.')
        return selected.id

    @objc.python_method
    def export(self, font, destination=None):
        self.exportPath = None
        try:
            if int(Glyphs.versionNumber) < 4:
                raise ValueError('OpenPlotFont export requires Glyphs 4 or later.')
            master_id = self.chosen_master(font)
            master = next((m for m in font.masters if m.id == master_id), None)
            if master is None:
                raise ValueError('The chosen master no longer exists. Reopen the export dialog.')
            filename = f'{font.familyName}-{master.name}.opf.json'
            # Avoid treating family/master names as path components.
            filename = filename.replace('/', '-').replace(':', '-')
            if destination is None:
                destination = GetSaveFile('Export OpenPlotFont — choose a new filename', filename, ['json', 'opf'])
                if not destination:
                    return False, 'OpenPlotFont export cancelled. No file was written.'
            path = Path(destination)
            if path.is_dir():
                path = path / filename
            data = export_to_path(font, master_id, path, NODE_TYPES)
            self.exportPath = str(path)
            warnings = data['metadata']['exportWarnings']
            message = f'Exported {len(data["glyphs"])} glyphs to {path.name}.'
            if warnings:
                message += '\n' + '\n'.join(warnings)
            return True, message
        except FileExistsError:
            return False, 'Destination already exists. Choose a new filename; the existing file was preserved.'
        except Exception as error:
            return False, f'OpenPlotFont export failed: {error}'

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged (SDK resource lookup)."""
        return __file__
