# Hershey Roman Simplex preparation

[HersheyRomanSimplex.plotfont.json](HersheyRomanSimplex.plotfont.json) is a reproducible JSON preparation from pinned upstream stroke data. It is **not a Glyphs-generated export**. The editable `.glyphs` port remains pending a new-font capability in Glyphs MCP; no native source file is included yet.

## Source, mapping, and rights

Upstream: [kamalmostafa/hershey-fonts](https://github.com/kamalmostafa/hershey-fonts/tree/1356bf2f83d380fcef68c887e88675eb9d445d86), revision `1356bf2f83d380fcef68c887e88675eb9d445d86`, file `hershey-fonts/rowmans.jhf`. The source, original notice, and revision are retained in [vendor/hershey](../../vendor/hershey/README.md). Export metadata records a source SHA-256 and upstream revision.

Rows 0–94 map sequentially to ASCII U+0020 through U+007E, preserving the source's complete printable ASCII repertoire. Row 95 (source ID 718, a circle) remains unencoded: this project does not assume an extra Unicode mapping from its appearance. Each glyph carries the original row and source ID in user data. An original unencoded `.notdef` is added separately, producing 97 glyphs with 95 Unicode mappings. Its rectangle is a traced centerline, not a fill.

Hershey geometry retains the upstream acknowledgment and redistribution terms, including derivatives and generated exports. It is not MIT. The newly authored fallback and conversion code use project MIT. Retain [NOTICE.txt](../../vendor/hershey/NOTICE.txt) with redistribution.

## Geometry and spacing

JHF stores a five-character identifier, three-character pair count, a left/right bearing pair, and coordinate pairs measured relative to ASCII `R`. The pair ` R` lifts the pen. Every source run becomes a distinct open stroke; even coincident endpoints remain open unless the source explicitly defines closure. Point order and direction are unchanged.

The normalization uses scale `1000 / 21`, source baseline Y = 9, and cap top Y = −12:

```text
x_font = (x_source − left_bearing) × scale
y_font = (9 − y_source) × scale
advanceWidth = (right_bearing − left_bearing) × scale
```

Upward Y, baseline zero, cap height 1000, units per em 1400. Fractional positions and advances are preserved. Selected line metrics are ascender 1200, descender −400, x-height `14 × scale`, and line gap 200; they are preparation choices, not upstream font metrics. No kerning or invented joining annotations are added.

## Reproduce and verify

```sh
python3 -m plotfont import-hershey vendor/hershey/rowmans.jhf -o output/HersheyRomanSimplex.plotfont.json
python3 -m plotfont validate output/HersheyRomanSimplex.plotfont.json
```

Tests compare every prepared path, point, advance, source identifier, and mapping with the pinned data. Reference specimens cover uppercase/lowercase, punctuation, and numerals. macOS Quick Look interpreted the SVG successfully. Native Glyphs creation, reopen verification, and source-to-export comparisons are the remaining acceptance work.

## Prepared native import

[Import Hershey Roman Simplex.py](../../scripts/Import%20Hershey%20Roman%20Simplex.py) populates only an empty, single-master font already saved at this directory's `HersheyRomanSimplex.glyphs` path. It rejects any other document and refuses to overwrite glyphs. It restores the native layer rounding flags after retaining fractional geometry, then compares the exported result against every pinned source record. It neither creates nor saves a document. Native execution is pending; tests use SDK-shaped doubles.
