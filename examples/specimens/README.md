# Reference specimens

- [Hershey Roman Simplex](hershey-roman-simplex.svg): rendered from the native Glyphs JSON export, cap height 8 mm. Required Hershey redistribution terms are embedded in SVG metadata and retained in the repository's upstream notice.
- [Connected script](script-joined.svg): opt-in joining of declared coincident endpoints, cap height 12 mm.
- [Mixed geometry](mixed.svg): independent centerline and compound fill with a hole, cap height 12 mm. The fill is an area preview, not a machine coverage trajectory.

The SVG renderer preserves lines/curves and uses separate path elements for independent strokes. macOS Quick Look and a separate JavaScript font consumer were used to review interchange. Source/export semantic comparisons and saved-source tests establish geometry correspondence; no hardware operation or production Plot-It integration is claimed.
