# MenuTitle: Export PlotFont
# encoding: utf-8

__doc__ = 'Export one selected master as validated PlotFont JSON without modifying source geometry'

import json
import sys
from pathlib import Path

from GlyphsApp import Glyphs, LINE, CURVE, QCURVE, OFFCURVE

# Run this workspace script in Glyphs 4. Keep its sibling package in place.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plotfont.glyphs_export import export_font


def main():
    font = Glyphs.font
    if font is None:
        raise RuntimeError("Open a font in Glyphs before running this script.")
    if int(Glyphs.versionNumber) < 4:
        raise RuntimeError("PlotFont export requires Glyphs 4 or later.")
    settings = font.userData.get("org.plotfont.font", {})
    destination = settings.get("destination")
    if not destination or not Path(destination).is_absolute() or not str(destination).endswith(".plotfont.json"):
        raise RuntimeError("Set org.plotfont.font.destination to a new absolute .plotfont.json path.")
    selected = font.selectedFontMaster
    if selected is None:
        raise RuntimeError("Select a master before exporting.")
    data = export_font(font, selected.id, {"line": LINE, "curve": CURVE, "qcurve": QCURVE, "offcurve": OFFCURVE})
    for warning in data["metadata"]["exportWarnings"]:
        print("PlotFont warning:", warning)
    # Existing output is deliberately preserved; change destination for another export.
    encoded = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    with Path(destination).open("x", encoding="utf-8") as stream:
        stream.write(encoded)
    print("Exported", len(data["glyphs"]), "glyphs to", destination)


if __name__ == "__main__":
    main()
