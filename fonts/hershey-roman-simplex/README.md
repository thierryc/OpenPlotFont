# Hershey Roman Simplex preparation

[HersheyRomanSimplex.plotfont.json](HersheyRomanSimplex.plotfont.json) is a reproducible JSON preparation from pinned upstream stroke data. It is **not a Glyphs-generated export**. The editable [Glyphs package](HersheyRomanSimplex.glyphspackage/fontinfo.plist) was populated and saved through Glyphs MCP in Glyphs 4.1 build 4107. All 97 glyphs passed native source/export comparison and saved-file geometry tests.

## Source, mapping, and rights

Upstream: [kamalmostafa/hershey-fonts](https://github.com/kamalmostafa/hershey-fonts/tree/1356bf2f83d380fcef68c887e88675eb9d445d86), revision `1356bf2f83d380fcef68c887e88675eb9d445d86`, file `hershey-fonts/rowmans.jhf`. The source, original notice, and revision are retained in [vendor/hershey](../../vendor/hershey/README.md). Export metadata records a source SHA-256 and upstream revision.

Rows 0–94 map sequentially to ASCII U+0020 through U+007E, preserving the source's complete printable ASCII repertoire. Row 95 (source ID 718, a circle) remains unencoded: this project does not assume an extra Unicode mapping from its appearance. Each glyph carries the original row and source ID in user data. An original unencoded `.notdef` is added separately, producing 97 glyphs with 95 Unicode mappings. Its rectangle is a traced centerline, not a fill.

Hershey geometry retains the upstream acknowledgment and redistribution terms, including derivatives and generated exports. It is not MIT. The newly authored fallback and conversion code use project MIT. Retain [NOTICE.txt](../../vendor/hershey/NOTICE.txt) with redistribution.

## Geometry and spacing

JHF stores a five-character identifier, three-character pair count, a left/right bearing pair, and coordinate pairs measured relative to ASCII `R`. The pair ` R` lifts the pen. Every source run becomes a distinct open stroke; even coincident endpoints remain open unless the source explicitly defines closure. Point order and direction are unchanged.

The normalization uses scale `50`, source baseline Y = 9, and cap top Y = −12:

```text
x_font = (x_source − left_bearing) × scale
y_font = (9 − y_source) × scale
advanceWidth = (right_bearing − left_bearing) × scale
```

Upward Y, baseline zero, cap height 1050, units per em 1470. All Hershey positions and advances are integral with this scale. Selected line metrics are ascender 1260, descender −420, x-height `14 × scale`, and line gap 210; they are preparation choices, not upstream font metrics. No kerning or invented joining annotations are added.

## Reproduce and verify

```sh
python3 -m plotfont import-hershey vendor/hershey/rowmans.jhf -o output/HersheyRomanSimplex.plotfont.json
python3 -m plotfont validate output/HersheyRomanSimplex.plotfont.json
```

Tests compare every prepared path, point, advance, source identifier, and mapping with the pinned data. Reference specimens cover uppercase/lowercase, punctuation, and numerals. macOS Quick Look interpreted the SVG successfully. Native population and source-to-export comparison passed. Saved-package tests check every node, path, mapping, advance, metric, and source record.

## Prepared native import

[Import Hershey Roman Simplex.py](../../scripts/Import%20Hershey%20Roman%20Simplex.py) populates only an empty, single-master font already saved at this directory's `HersheyRomanSimplex.glyphs` or `HersheyRomanSimplex.glyphspackage` path. Verified blank template glyphs may be replaced; existing artwork and glyph metadata are rejected. It rejects any other document and refuses to overwrite glyphs. It restores the native layer rounding flags after retaining fractional geometry, then compares the exported result against every pinned source record. It neither creates nor saves a document. The same adapter was qualified through native MCP scripts. Regression tests additionally use SDK-shaped doubles.

Glyph names use the conventional ASCII names used by Glyphs (`A`, `a`, `zero`, `exclam`, etc.). These names are project mapping choices; upstream JHF supplies numeric identifiers rather than glyph names. Native font collection order may differ from source row order; `org.plotfont.hershey.row` retains the exact source row. Drawing order remains each glyph's path order. Both `.glyphs` and `.glyphspackage` authoring sources are supported.

## Native storage precision

Glyphs 4.1 saves coordinates with three decimal places. The initial `1000 / 21` normalization introduced up to `0.0004762` font-unit error on save. The first unreleased asset now uses 50 units per JHF coordinate and cap height 1050, preserving the same physical Hershey proportions while saving every point exactly. This changes the asset's font-unit scale, not draft format `0.2`. Use a file digest for reproducible font references. Arbitrary fractional authoring remains subject to the editor's native save precision; the exporter preserves the in-memory values it receives.
