# PlotFont

PlotFont is a proposed portable font format for pen plotters and CAD/CAM workflows. A glyph can mix centerline strokes and filled shapes. It records drawing intent and order; the destination software generates fill paths using the actual tool size.

The intended workflow is:

```text
Glyphs source (.glyphs / .glyphspackage)
  → PlotFont (.plotfont.json)
  → text layout and physical sizing
  → SVG / DXF / HPGL / machine-specific G-code
  → plotter or CAD/CAM software
```

This project defines the PlotFont format and the workflow for editing fonts in Glyphs, exporting and saving them as JSON, and using that data in other software. Consumer applications handle text layout, drawing preparation, and machine output. Plot-It is a separate repository with its own development roadmap; it can serve as a test application for the format.

## Start here

- [Format specification](docs/PLOTFONT_FORMAT.md): purpose, draft JSON structure, units, strokes, curves, spacing, and validation rules.
- [Glyphs and export workflow](docs/GLYPHS_AND_EXPORT.md): how to design open paths, prepare an exporter, and produce drawing formats.
- [Using PlotFont in other software](docs/USING_PLOTFONT.md): consumer responsibilities, geometry interchange, and reproducible text layout.
- [Minimal font example](examples/minimal.plotfont.json): an illustrative `A`, space, and fallback glyph.
- [Script font example](examples/script.plotfont.json): ordered curves, entry/exit points, anchors, and glyph user data for optional letter connections.
- [Mixed glyph example](examples/mixed.plotfont.json): an open line combined with a filled region containing a hole.
- [Agent instructions](AGENTS.md): project scope and contribution rules for coding assistants.

## Project status

Confirmed requirements: `.plotfont.json`, draft version `0.2`, Glyphs **4 and later**, and Hershey Roman Simplex as the first repertoire. The five initial milestones are complete within the [documented scope](docs/ROADMAP.md). The format remains an unreleased draft.

Implemented here: JSON Schema, semantic validation, a source-pinned Hershey data import, an SVG reference renderer, and a selected-master Glyphs export script. Guarded native import, atomic publication, source/export comparison, and independent JavaScript SVG interchange checks are included. The native Hershey `.glyphspackage` source has been populated, verified, and saved through Glyphs MCP in Glyphs 4.1. Native source reopening, the actual export-script entry point, and curve/metadata/kerning qualification passed. The [native export](examples/hershey-roman-simplex.plotfont.json) is a curated conformance artifact. Standalone document creation still requires Glyphs because MCP scripts need an existing document binding.

Review the [SVG specimens](examples/specimens/README.md). See the [milestone plan and completion evidence](docs/ROADMAP.md), [Hershey provenance](fonts/hershey-roman-simplex/README.md), [JSON Schema](schemas/plotfont-0.2.schema.json), and [export script instructions](docs/GLYPHS_EXPORT_SCRIPT.md).

## Run locally

Python 3.10 or later; the library and CLI use only the standard library. Run from this repository:

```sh
python3 -m plotfont validate examples/*.plotfont.json fonts/hershey-roman-simplex/*.plotfont.json
python3 -m plotfont render fonts/hershey-roman-simplex/HersheyRomanSimplex.plotfont.json "Hello PlotFont!" -o output/specimen.svg --cap-height 8
python3 -m plotfont render examples/script.plotfont.json un -o output/joined.svg --join
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
```

Render sizes are in millimetres. Existing output is preserved unless the CLI receives `--force`. Fills are SVG areas for review, not generated machining trajectories. Joining is opt-in and currently requires declared endpoints to coincide; it does not invent connecting geometry. General shaping, instance interpolation, an importer into Glyphs, DXF/HPGL/G-code converters, and device control are not implemented.

## Licensing

Original code, documentation, and original examples use [MIT](LICENSE). Imported Hershey glyph data has its own permissive redistribution terms and required acknowledgments: retain [the upstream notice](vendor/hershey/NOTICE.txt) with derivatives. The Hershey geometry and its generated font are not relicensed as MIT. The upstream GPL C implementation is not included.

## Reflection: a companion font for design previews

How can we create a companion font for previewing and laying out PlotFont text in regular design software such as Adobe Illustrator, Affinity Designer, Figma, and Sketch? Should exporting a PlotFont automatically produce an OpenType companion font at the same time?

Questions to explore before choosing an export strategy:

- How should centerline strokes appear in the companion: should export expand them into visible outlines using a configurable preview width, while retaining filled shapes as areas?
- How can both exports share glyph names, Unicode mappings, advances, and kerning so preview layout matches PlotFont layout?
- How should optional script connections appear, and what differences between preview shaping and plotted lettering need to be disclosed?
- Should companion export be automatic, optional, or a separate action, and which OpenType representation works consistently across the target applications?

The companion would be a visual layout aid. Its preview stroke width would not define the physical pen or cutter size; PlotFont geometry and destination tool settings would remain the source for machine output. Companion-font export and compatibility with these applications are open research questions, not implemented features.

## Open question: OpenType features and text shaping

Which OpenType features make sense for PlotFont and its companion font, which should be optional, and which should remain unsupported? How should glyph substitutions, special ligatures, and other typographic elements be represented so design previews and plotted output agree?

Questions to investigate:

- Which substitutions should we support: standard, discretionary, and contextual ligatures; contextual alternates; stylistic sets; localized forms; or alternate numeral styles? Which are useful for the first font repertoire, and which add complexity without a clear plotting use case?
- How should unencoded alternate and ligature glyphs be selected? Should PlotFont carry feature rules, reference a companion OpenType font for shaping, or accept a resolved glyph sequence from a shaping engine?
- How should kerning, cursive attachment, and mark positioning interact with advances, named anchors, and script entry/exit points? How do we distinguish typographic placement from an intentional pen-down connection?
- How should special ligatures preserve drawing order, independent strokes, and filled regions? How should a saved project retain the original text, selected features, and resulting glyph choices so editing remains reproducible?
- How should fallback to another font work for missing characters or scripts, including matching size and baseline and preserving the identity of the font used for each glyph? This is separate from substituting one glyph for another within a font.
- Which features require shaping behavior beyond the current simple left-to-right scalar lookup, and how should consumers report unsupported rules rather than silently produce different lettering?
- Should preview-only features be allowed, or must every enabled companion-font feature have an equivalent PlotFont rendering path?

Feature support, shaping-engine integration, and fallback policy remain open design questions. The current draft stores resolved static glyph geometry, simple mappings, and numeric kerning; it does not implement OpenType feature execution.
