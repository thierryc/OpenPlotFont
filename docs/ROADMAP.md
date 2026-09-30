# PlotFont milestones

The format is draft `0.2`; file names end in `.plotfont.json`. Glyphs 4 and later is the authoring target. Plot-It is an independent concept-testing application with its own roadmap.

| Milestone | Deliverables and acceptance | Current evidence / remaining work |
| --- | --- | --- |
| M1 — Foundation | Required metadata, compatibility rules, MIT for original works, separate imported-font terms, clean public foundation | Complete: documentation and examples validated and published at [thierryc/PlotFont](https://github.com/thierryc/PlotFont), with a clean initial public history. |
| M2 — Format validation | Schema and semantic checks for ordered strokes, curves, fills/holes, mappings, spacing, anchors, JSON user data, and endpoints | Implemented. Fixtures cover malformed geometry, versions, and invalid references. Physical tool settings remain outside font data. |
| M3 — Native Hershey port | Roman Simplex in a new local Glyphs source; exact upstream revision, attribution, mappings, stroke order, direction, and spacing | Complete: native Glyphs 4.1 source populated and saved through MCP; 97 glyphs / 95 mappings, 1,117 points. Native comparison and exact saved-package tests pass. Integral normalization avoids native coordinate serialization loss. |
| M4 — Glyphs export | Script exporting one selected master or resolved static instance, validated before saving; compare source/export | Complete for one selected master: actual script executed on a copy in Glyphs 4.1; native source reopening, comparison, curve/fill/metadata fixtures and kerning exceptions passed. Native JSON export retained as a conformance example. Instance interpolation and plug-in packaging remain deferred. |
| M5 — Interchange | Reference SVG, physical scaling, axis conversion, independent strokes, fallback, loops, joins, mixed fills, consumer checklist | Complete for reference interchange: native-export rendering equals the source reference, independent JavaScript consumption passes, and final specimens render in macOS Quick Look. Curves, joins, fill holes, scaling, fallback and bounds are covered by tests. Production consumer integrations and hardware profiles remain separate work. |

## Completed acceptance evidence

- Native authoring source: `fonts/hershey-roman-simplex/HersheyRomanSimplex.glyphspackage`, populated and saved through MCP in Glyphs 4.1 build 4107.
- Reopened native source and actual export-script entry point compared against all 97 glyphs / 95 mappings and the pinned upstream dataset.
- Native cubic/quadratic curves, compound fills, holes, anchors, user data, connection references, fractional widths, group kerning and zero exceptions qualified on a disposable copy. Fixtures and a compact report are retained under `tests/fixtures/`.
- Saved-source tests verify exact integral Hershey geometry; SVG tests verify correspondence between native export and source, with a separate Node.js consumer and macOS Quick Look review.
- [Curated specimens](../examples/specimens/README.md) provide reviewable interchange results.

All five initial milestones are complete within their documented scope. The format remains draft `0.2`; this is not a stable format release or certification of a machine workflow. Native qualification covers Glyphs 4.1 and the additional-font workflow in 4.1.1; later versions require qualification. Portable CI verifies fixtures and tools, rather than launching Glyphs.

## Additional Hershey faces

Roman Duplex, Roman Triplex, and Script Simplex extend the [font catalog](../fonts/README.md). Each source was created with MCP `create_document`, populated, saved, reopened, and exported through the real export script on a copy in Glyphs 4.1.1 build 4108. Each face has 97 glyphs / 95 mappings; saved point counts including the original fallback are 2,236, 3,269, and 2,130 respectively. Individually pinned source digests and full upstream terms accompany the ports. Tests cover every source point and saved node, native-export semantics, separate strokes, face selection, modified-data rejection, Script descenders, and independent SVG consumption. No joining annotations or kerning are invented.

## Retained questions

- Should export automatically create an OpenType companion for design previews?
- Which OpenType features, substitutions, ligatures, and shaping behaviors make sense?
- How should Plot-It save font references and preserve reproducible text layout?
- Which CAD versions and machine profiles should future converters target?

These questions do not block format validation, the first font port, or selected-master export. Hardware operation and filled-region coverage generation are outside this repository's initial milestones.
