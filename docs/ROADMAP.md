# PlotFont milestones

The format is draft `0.2`; file names end in `.plotfont.json`. Glyphs 4 and later is the authoring target. Plot-It is an independent concept-testing application with its own roadmap.

| Milestone | Deliverables and acceptance | Current evidence / remaining work |
| --- | --- | --- |
| M1 — Foundation | Required metadata, compatibility rules, MIT for original works, separate imported-font terms, clean public foundation | Complete: documentation and examples validated and published at [thierryc/PlotFont](https://github.com/thierryc/PlotFont), with a clean initial public history. |
| M2 — Format validation | Schema and semantic checks for ordered strokes, curves, fills/holes, mappings, spacing, anchors, JSON user data, and endpoints | Implemented. Fixtures cover malformed geometry, versions, and invalid references. Physical tool settings remain outside font data. |
| M3 — Native Hershey port | Roman Simplex in a new local Glyphs source; exact upstream revision, attribution, mappings, stroke order, direction, and spacing | Complete: native Glyphs 4.1 source populated and saved through MCP; 97 glyphs / 95 mappings, 1,117 points. Native comparison and exact saved-package tests pass. Integral normalization avoids native coordinate serialization loss. |
| M4 — Glyphs export | Script exporting one selected master or resolved static instance, validated before saving; compare source/export | Selected-master script, atomic validated publication, and source/export comparator implemented and tested offline. Native Hershey comparison passed; generated export and broader native curve/metadata fixtures are next. Resolved instance interpolation and plug-in packaging are deferred. |
| M5 — Interchange | Reference SVG, physical scaling, axis conversion, independent strokes, fallback, loops, joins, mixed fills, consumer checklist | Renderer and fixtures implemented; SVG interpreted by macOS Quick Look. A separate JavaScript consumer verifies generated geometry and deliberate corruption in CI. Native Glyphs specimen comparison and independent font-aware consumer validation remain pending. |

## Next acceptance steps

1. Create and save an empty project font manually, or expose a Glyphs MCP new-font creation capability. Computer Use access was denied; the existing MCP interface requires a saved document. Do not use unrelated documents as import targets.
2. Populate all 96 upstream records plus an original fallback, preserving fractional coordinates and advances. Save the editable source under `fonts/hershey-roman-simplex/`.
3. Verify that the source opens in Glyphs 4. Compare every source path/node, mapping, and advance against the pinned dataset.
4. Run the export script on that source. Compare every exported operation, curve, anchor, endpoint annotation, and user-data record; test group kerning and exception precedence natively.
5. Compare SVG specimens with the native source and validate the JSON with an independently developed font-aware consumer before a stable format release.

## Retained questions

- Should export automatically create an OpenType companion for design previews?
- Which OpenType features, substitutions, ligatures, and shaping behaviors make sense?
- How should Plot-It save font references and preserve reproducible text layout?
- Which CAD versions and machine profiles should future converters target?

These questions do not block format validation, the first font port, or selected-master export. Hardware operation and filled-region coverage generation are outside this repository's initial milestones.
