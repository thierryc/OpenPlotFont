# PlotFont milestones

Geometry-only fonts retain draft `0.2`; optional OpenType layout uses draft `0.3`. file names end in `.plotfont.json`. Glyphs 4 and later is the authoring target. Plot-It is an independent concept-testing application with its own roadmap.

| Milestone | Deliverables and acceptance | Current evidence / remaining work |
| --- | --- | --- |
| M1 — Foundation | Required metadata, compatibility rules, MIT for original works, separate imported-font terms, clean public foundation | Complete: documentation and examples validated and published at [thierryc/PlotFont](https://github.com/thierryc/PlotFont), with a clean initial public history. |
| M2 — Format validation | Schema and semantic checks for ordered strokes, curves, fills/holes, mappings, spacing, anchors, JSON user data, and endpoints | Implemented. Fixtures cover malformed geometry, versions, and invalid references. Physical tool settings remain outside font data. |
| M3 — Native Hershey port | Roman Simplex in a new local Glyphs source; exact upstream revision, attribution, mappings, stroke order, direction, and spacing | Complete: native Glyphs 4.1 source populated and saved through MCP; 97 glyphs / 95 mappings, 1,117 points. Native comparison and exact saved-package tests pass. Integral normalization avoids native coordinate serialization loss. |
| M4 — Glyphs export | Script exporting one selected master or resolved static instance, validated before saving; compare source/export | Complete for one selected master: actual script executed on a copy in Glyphs 4.1; native source reopening, comparison, curve/fill/metadata fixtures and kerning exceptions passed. Native JSON export retained as a conformance example. A [selected-master plugin](GLYPHS_EXPORT_PLUGIN.md) is packaged, its class/action tested through MCP in 4.1.1, and installation verified; startup/menu qualification remains pending. Instance interpolation remains deferred. |
| M5 — Interchange | Reference SVG, physical scaling, axis conversion, independent strokes, fallback, loops, joins, mixed fills, consumer checklist | Complete for reference interchange: native-export rendering equals the source reference, independent JavaScript consumption passes, and final specimens render in macOS Quick Look. Curves, joins, fill holes, scaling, fallback and bounds are covered by tests. Production consumer integrations and hardware profiles remain separate work. |

## Completed acceptance evidence

- Native authoring source: `fonts/hershey-roman-simplex/HersheyRomanSimplex.glyphspackage`, populated and saved through MCP in Glyphs 4.1 build 4107.
- Reopened native source and actual export-script entry point compared against all 97 glyphs / 95 mappings and the pinned upstream dataset.
- Native cubic/quadratic curves, compound fills, holes, anchors, user data, connection references, fractional widths, group kerning and zero exceptions qualified on a disposable copy. Fixtures and a compact report are retained under `tests/fixtures/`.
- Saved-source tests verify exact integral Hershey geometry; SVG tests verify correspondence between native export and source, with a separate Node.js consumer and macOS Quick Look review.
- [Curated specimens](../examples/specimens/README.md) provide reviewable interchange results.

All five initial milestones are complete within their documented scope. The format remains an unreleased draft; this is not a stable format release or certification of a machine workflow. Native qualification covers Glyphs 4.1 and the additional-font workflow in 4.1.1; later versions require qualification. Portable CI verifies fixtures and tools, rather than launching Glyphs.

## Additional Hershey faces

Roman Duplex, Roman Triplex, and Script Simplex extend the [font catalog](../fonts/README.md). Each source was created with MCP `create_document`, populated, saved, reopened, and exported through the real export script on a copy in Glyphs 4.1.1 build 4108. Each face has 97 glyphs / 95 mappings; saved point counts including the original fallback are 2,236, 3,269, and 2,130 respectively. Individually pinned source digests and full upstream terms accompany the ports. Tests cover every source point and saved node, native-export semantics, separate strokes, face selection, modified-data rejection, Script descenders, and independent SVG consumption. No joining annotations or kerning are invented.

## M6 — Self-contained OpenType layout

Implemented in draft 0.3: optional compiled static OpenType payload with exact glyph-ID mapping, feature/script/language manifest and preserved authoring source; FontTools validation; HarfBuzz shaping and positioned-run JSON; SVG rendering with shaped advances/offsets; optional Glyphs adapter attachment. Existing 0.2 exports remain usable. Original fixtures and tests cover substitutions, contextual rules, localized forms, marks, ligature attachment, cursive positioning, RTL runs, digest/mapping errors and kerning exactly once. See [the layout specification](PLOTFONT_LAYOUT.md).

Automatic instance resolution, automatic compilation from the menu, multi-run bidi segmentation, automatic fallback and shaped pen-path joining are deferred. Companion preview-font generation remains separate.

M6 is complete within this scope. The [native layout demo](../fonts/layout-demo/README.md) was created and saved in Glyphs 4.1.1 through MCP, exported through a source-bound typed static job and converted by the actual 0.3 export-script entry point on a copy. Its ligatures, alternates, localized forms, contextual substitutions, numeral widths, marks and kerning match the portable fixture. The native compiler omits this demo's Latin `curs` block; its code is preserved, the omission is warned, and requesting that feature fails. The portable compiler includes and tests cursive placement. Native receipt and verification samples are retained in [the qualification report](../tests/fixtures/native-layout-report.json).

## Retained questions

- Should export automatically create an OpenType companion for design previews?
- Which per-family feature preferences, fallback and mixed-script policies should consumers adopt?
- How should Plot-It save font references and preserve reproducible text layout?
- Which CAD versions and machine profiles should future converters target?

These questions do not block format validation, the first font port, or selected-master export. Hardware operation and filled-region coverage generation are outside this repository's initial milestones.
