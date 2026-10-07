# MenuTitle: Export OpenPlotFont
# encoding: utf-8

__doc__ = 'Export one selected master as validated OpenPlotFont JSON without modifying source geometry'

import json
import sys
from pathlib import Path

from GlyphsApp import Glyphs, LINE, CURVE, QCURVE, OFFCURVE

# Run this workspace script in Glyphs 4. Keep its sibling package in place.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openplotfont.glyphs_export import export_font
from openplotfont.storage import write_font


def main(font=None, destination=None, master_id=None, *, layout_bytes=None, glyph_order=None, feature_settings=None):
    font = Glyphs.font if font is None else font
    if font is None:
        raise RuntimeError("Open a font in Glyphs before running this script.")
    if int(Glyphs.versionNumber) < 4:
        raise RuntimeError("OpenPlotFont export requires Glyphs 4 or later.")
    settings = font.userData.get("org.openplotfont.font", {})
    destination = settings.get("destination") if destination is None else destination
    if not destination or not Path(destination).is_absolute() or not str(destination).endswith((".opf", ".opf.json")):
        raise RuntimeError("Set org.openplotfont.font.destination to a new absolute .opf or .opf.json path.")
    selected = (next((m for m in font.masters if m.id == master_id), None)
                if master_id is not None else font.selectedFontMaster)
    if selected is None:
        raise RuntimeError("Select a master before exporting.")
    data = export_font(font, selected.id, {"line": LINE, "curve": CURVE, "qcurve": QCURVE, "offcurve": OFFCURVE},
                       layout_bytes=layout_bytes,glyph_order=glyph_order,feature_settings=feature_settings)
    for warning in data["metadata"]["exportWarnings"]:
        print("OpenPlotFont warning:", warning)
    # Existing output is deliberately preserved; change destination for another export.
    write_font(destination, data)
    print("Exported", len(data["glyphs"]), "glyphs to", destination)


if __name__ == "__main__":
    main()
