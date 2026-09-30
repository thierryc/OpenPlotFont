# Using PlotFont in other software

PlotFont is a proposed font-data interchange format. An application can consume its JSON directly or receive a drawing generated from it. The contracts below define consumer responsibilities. This repository includes a Python reader, semantic validator, and reference SVG renderer; machine preparation belongs downstream.

## Load, lay out, and render

```text
Load and validate .plotfont.json
  → map text to glyphs using the supported layout profile
  → apply advances, kerning, and line metrics
  → scale geometry and anchors into document coordinates
  → optionally assemble declared script connections
  → preserve filled regions or generate fill paths using destination tool settings
  → render or export the drawing
```

Reject unsupported versions and drawing operations before rendering. Preserve operation order, open paths, explicit closure, curves, compound fill contours, and holes. Do not infer joining or filling from visual proximity or closure alone. Consumer-specific optimization must be explicit.

For an initial drawing interchange route, use SVG with physical dimensions in millimetres. Keep each independent pen-down trajectory in a separate path element. A consumer must split SVG subpaths at pen-up boundaries rather than sampling disconnected subpaths as one continuous trajectory. Preview fills preserve region geometry and fill rules; a machine-ready drawing requires actual fill trajectories generated using the selected tool after sizing.

Native JSON loading can retain reusable glyph geometry and editable text. Generic drawing import does not guarantee recovery of the original copy, glyph choices, or font identity. Drawing conversion is described in [the export workflow](GLYPHS_AND_EXPORT.md).

## Reproducible text and saved documents

Applications should retain original text, the exact font identity and file version or digest, physical text size, placement, and selected layout/joining settings. Embed font data where permitted or use a resolvable reference with a documented missing-font policy. Changing the copy must use the selected font and supported features consistently. Preserve anchors and user data when rewriting font data.

Open design questions:

- Should documents embed the font JSON, reference an external file, or support both?
- How should applications detect a changed or unavailable font and let users preserve or regenerate existing geometry?
- Which resolved glyph choices and feature settings need saving when advanced shaping is introduced?
- How should fallback fonts, licensing restrictions, and font revisions affect reproducible layout?

## Reference renderer

Use `python3 -m plotfont render FONT.plotfont.json "Text" -o output/text.svg --cap-height 8`. The SVG uses physical millimetre dimensions and flips upward font Y into downward SVG Y. Bounds include curve control-point hulls, overhangs, and the preview stroke width. Text uses simple left-to-right Unicode scalar lookup, numeric kerning, fallback glyphs, and line metrics. Tabs are rejected. It does not execute OpenType features.

Each independent stroke receives a separate path. Closed centerlines receive `Z`; fills receive a compound path with their fill rule and no boundary stroke. `--join` merges only declared, coincident adjacent endpoints and rejects gaps requiring a connector policy. Preview width is visual only.

The final [SVG specimens](../examples/specimens/README.md) were interpreted independently by macOS Quick Look. A separate Node.js font consumer checks the native-exported JSON against SVG geometry. This verifies reference interchange; production application integration and machine operation need their own tests.

## Consumer verification

Use the [minimal](../examples/minimal.plotfont.json), [script](../examples/script.plotfont.json), and [mixed](../examples/mixed.plotfont.json) examples to check:

- Independent strokes remain separate, and closed centerline loops are traced once.
- Scaling and Y-axis conversion preserve requested physical size and all curve control points.
- Spaces advance without drawing; unsupported characters use the declared fallback glyph.
- Script connections apply only when enabled and declared; spaces and line breaks interrupt the chain.
- Filled regions retain holes and operation order; unsupported fills produce an actionable error.
- Save/reload preserves font identity, copy, layout settings, anchors, and user data. This is a downstream application requirement; the renderer produces a drawing, not an editable text project.

Plot-It is a possible concept-testing application in a separate repository. Its integration, interface, machine support, and development roadmap belong to that project. Compatibility must be established through testing rather than assumed from this specification.

## Independent interchange checks

[verify_svg.mjs](../scripts/verify_svg.mjs) is a separate Node.js implementation of scalar mapping, fallback, kerning, line metrics, physical scaling, operation ordering, and contour serialization expectations. It reads JSON directly and does not import the Python implementation. Tests compare all printable Hershey glyphs, mixed fills/holes, curves, spaces, fallback, and multiple lines against the produced SVG, and deliberately corrupt geometry/fill rules to verify failures. This is cross-implementation test evidence within this repository, not certification of a third-party font-aware application.

```sh
node scripts/verify_svg.mjs fonts/hershey-roman-simplex/HersheyRomanSimplex.plotfont.json output/specimen.svg "Hello PlotFont!" 8
```

Use the same text and cap height as the Python render command. The checker checks default independent strokes; opt-in joined output has separate Python tests. Node.js is a development/test dependency only; normal library and CLI use remains standard-library Python. CI installs Node.js explicitly so these checks cannot silently skip there.

Centerline previews use round caps and joins. This makes half the preview width a sufficient padding around the geometry/control-point hull, avoiding unbounded miter extensions at sharp corners. Fills retain area and rule, with no generated tool coverage paths.
