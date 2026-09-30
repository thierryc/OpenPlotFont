# MenuTitle: Import Hershey Font
# encoding: utf-8

"""Populate only a saved, empty project source for an explicitly pinned face."""
import sys
from pathlib import Path
from GlyphsApp import Glyphs, GSGlyph, GSLayer, GSPath, GSNode, LINE, CURVE, QCURVE, OFFCURVE

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from plotfont.hershey import FACES
from plotfont.glyphs_hershey import populate_hershey
from plotfont.glyphs_export import export_font
from plotfont.comparison import compare_fonts


def main(font=None):
    font = Glyphs.font if font is None else font
    if int(Glyphs.versionNumber) < 4 or font is None:
        raise RuntimeError('Open a saved blank project font in Glyphs 4 or later.')
    destination = Path(str(font.filepath)).resolve() if font.filepath else None
    for face, settings in FACES.items():
        stem = ROOT / 'fonts' / ('hershey-' + face) / settings['family'].replace(' ', '')
        if destination in [stem.with_suffix(ext).resolve() for ext in ('.glyphs', '.glyphspackage')]:
            break
    else:
        raise RuntimeError('Open a saved source at one of the documented Hershey project paths.')
    reference = populate_hershey(
        font, ROOT / 'vendor/hershey' / settings['file'], destination, face=face,
        glyph_type=GSGlyph, layer_type=GSLayer, path_type=GSPath, node_type=GSNode, line_type=LINE)
    actual = export_font(font, font.masters[0].id,
                         {'line': LINE, 'curve': CURVE, 'qcurve': QCURVE, 'offcurve': OFFCURVE})
    compare_fonts(reference, actual)
    print('Verified', reference['familyName'], len(reference['glyphs']), 'glyphs against pinned upstream data.')
    return reference


if __name__ == '__main__':
    main()
