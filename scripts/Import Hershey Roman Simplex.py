# MenuTitle: Import Hershey Roman Simplex
# encoding: utf-8

__doc__ = 'Populate only the saved empty project font with pinned Hershey Roman Simplex data'

import sys
from pathlib import Path
from GlyphsApp import Glyphs, GSGlyph, GSLayer, GSPath, GSNode, LINE, CURVE, QCURVE, OFFCURVE

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from plotfont.glyphs_hershey import populate_hershey
from plotfont.glyphs_export import export_font
from plotfont.comparison import compare_fonts


def main():
    if int(Glyphs.versionNumber) < 4 or Glyphs.font is None:
        raise RuntimeError('Open the saved blank project font in Glyphs 4 or later.')
    font = Glyphs.font
    destinations = [ROOT / ('fonts/hershey-roman-simplex/HersheyRomanSimplex' + extension)
                    for extension in ('.glyphs', '.glyphspackage')]
    destination = next((p for p in destinations if str(p) == str(font.filepath)), None)
    if destination is None:
        raise RuntimeError('Open the saved Hershey Roman Simplex project source.')
    reference = populate_hershey(font, ROOT / 'vendor/hershey/rowmans.jhf', destination,
                                 glyph_type=GSGlyph, layer_type=GSLayer, path_type=GSPath,
                                 node_type=GSNode, line_type=LINE)
    exported = export_font(font, font.masters[0].id,
                           {'line': LINE, 'curve': CURVE, 'qcurve': QCURVE, 'offcurve': OFFCURVE})
    compare_fonts(reference, exported)
    print('Verified all', len(reference['glyphs']), 'glyphs against the pinned source. Save the project font separately.')


if __name__ == '__main__':
    main()
