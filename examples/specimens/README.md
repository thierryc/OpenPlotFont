# Reference specimens

- [Hershey Roman Simplex](hershey-roman-simplex.svg): rendered from the native Glyphs JSON export, cap height 8 mm. Required Hershey redistribution terms are embedded in SVG metadata and retained in the repository's upstream notice.
- [Hershey Roman Duplex](hershey-roman-duplex.svg): independent multiple-stroke lettering, cap height 8 mm.
- [Hershey Roman Triplex](hershey-roman-triplex.svg): additional parallel strokes, cap height 8 mm.
- [Hershey Script Simplex](hershey-script-simplex.svg): original handwriting strokes and descenders, cap height 8 mm, with no inferred joins.
- [Connected script](script-joined.svg): opt-in joining of declared coincident endpoints, cap height 12 mm.
- [Mixed geometry](mixed.svg): independent centerline and compound fill with a hole, cap height 12 mm. The fill is an area preview, not a machine coverage trajectory.
- [Native OpenType layout](layout-demo-native.svg): ligature selection, contextual alternate and mark attachment from the native Glyphs 0.3 export, cap height 12 mm.
- [Cursive positioning](layout-demo-cursive.svg): portable 0.3 fixture with `curs=1`, preserving two independent pen paths at their shaped origins, cap height 12 mm.

Each Hershey specimen embeds the complete upstream redistribution terms in SVG metadata. The SVG renderer preserves lines/curves and uses separate path elements for independent strokes. macOS Quick Look and a separate JavaScript font consumer were used to review interchange. Source/export semantic comparisons and saved-source tests establish geometry correspondence; no hardware operation or production Plot-It integration is claimed.

The new layout specimens are original MIT fixtures. Automated analytic checks
verify their feature selections and positions; the JavaScript checker covers
simple mode only. See [layout qualification](../../fonts/layout-demo/README.md)
for the native compiler's omitted Latin cursive rule and the portable fixture
that tests it.
