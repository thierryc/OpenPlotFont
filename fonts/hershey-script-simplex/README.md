# Hershey Script Simplex

[HersheyScriptSimplex.opf.json](HersheyScriptSimplex.opf.json) is a reproducible preparation from pinned upstream JHF data, separately from the [native Glyphs export](../../examples/hershey-script-simplex.opf.json). The [editable source](HersheyScriptSimplex.glyphspackage/fontinfo.plist) was created, populated, and saved through Glyphs MCP in Glyphs 4.1.1 build 4108. Each of its 97 glyphs and 2,130 points passed source/export comparison. See the [specimen](../../examples/specimens/hershey-script-simplex.svg).

## Source and licensing

Upstream: [kamalmostafa/hershey-fonts](https://github.com/kamalmostafa/hershey-fonts/tree/1356bf2f83d380fcef68c887e88675eb9d445d86), revision `1356bf2f83d380fcef68c887e88675eb9d445d86`, file `hershey-fonts/scripts.jhf`. SHA-256: `6b391b2ea3a0771cf18caff0ed111db3d05681fa586d423a740cc0b2b155a873`. The importer refuses modified bytes or a different face's source. Retain [the full upstream notice](../../vendor/hershey/NOTICE.txt) with the data and derivatives. Hershey geometry is not relicensed as MIT; the original fallback and project code use MIT. No upstream C implementation is included.

## Mapping, drawing order, and spacing

All 96 source records are preserved. Rows 0–94 map sequentially to printable ASCII U+0020–U+007E; row 95 remains unencoded. The original unencoded `.notdef` adds one glyph, producing 97 glyphs and 95 mappings. Glyph user data retains the upstream row and source ID. Conventional Glyphs ASCII names are mapping choices; native collection order may differ while each glyph's path and point order remain unchanged.

Each pen-down run is an independent open stroke. Coincident endpoints do not imply closure or filling. Baseline source Y = 9, cap top Y = −12, scale = 50 font units per JHF coordinate:

```text
x_font = (x_source − left_bearing) × 50
y_font = (9 − y_source) × 50
advanceWidth = (right_bearing − left_bearing) × 50
```

Cap height 1050, UPM 1470, ascender 1260, line gap 210. Script x-height is 450 and descender −600, following the lowercase body and deeper descenders. No entry/exit annotations or joins are inferred; the source often contains multiple strokes per letter. Use the dedicated connected-script example to test explicit joining. These line metrics are preparation choices, not supplied upstream metrics. Integral coordinates preserve every point exactly through native saving. No kerning is invented.

## Reproduce and edit

```sh
python3 -m openplotfont import-hershey vendor/hershey/scripts.jhf --face script-simplex -o output/HersheyScriptSimplex.opf.json
python3 -m openplotfont compare fonts/hershey-script-simplex/HersheyScriptSimplex.opf.json examples/hershey-script-simplex.opf.json
```

Open the native package to edit. [Import Hershey Font.py](../../scripts/Import%20Hershey%20Font.py) populates only an empty single-master source at the exact documented project path and rejects existing artwork or glyph metadata. [Export OpenPlotFont.py](../../scripts/Export%20OpenPlotFont.py) exports one selected master; choose a new absolute JSON destination and export from a copy. Source creation and saving are separate MCP operations.

Regression tests inspect every saved node, mapping, advance, metric, and source identifier, compare preparation with native export, and check SVG interpretation using an independent JavaScript consumer. These retained preparation/native-example files use legacy draft `0.2`. The current format is draft `0.3`; [plugin 0.1.1](../../docs/GLYPHS_EXPORT_PLUGIN.md) exports geometry-only 0.3 from the editable source. No hardware compatibility is claimed.
