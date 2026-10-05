# PlotFont

PlotFont v0.3 is a draft portable font format for pen plotters and CAD/CAM workflows. A glyph can mix centerline strokes and filled shapes. It records drawing intent and order; the destination software generates fill paths using the actual tool size. OpenType layout is optional: a v0.3 font may contain geometry alone or include compiled text-layout rules.

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

- [Project website](https://plotfont.litsquare.com/): introduction, attributed font catalog, and Glyphs exporter installation. See [website maintenance](site/README.md) for the static GitHub Pages workflow.
- [Format specification](docs/PLOTFONT_FORMAT.md): purpose, draft JSON structure, units, strokes, curves, spacing, and validation rules.
- [OpenType layout](docs/PLOTFONT_LAYOUT.md): self-contained feature rules, glyph-ID mappings, HarfBuzz positioning and explicit layout modes.
- [Layout demo](examples/layout-demo.plotfont.json): original fixture for substitutions, marks, language rules and cursive positioning.
- [Glyphs and export workflow](docs/GLYPHS_AND_EXPORT.md): how to design open paths, prepare an exporter, and produce drawing formats.
- [Stroke-font candidates](docs/STROKE_FONT_CANDIDATES.md): researched Hershey, SVG, UFO, CAD, and procedural font sources, with licenses and proposed conversion priorities.
- [Outline-to-stroke research study](docs/OUTLINE_TO_STROKE_STUDY.md): mathematical methods, font-specific and 2026 research, Glyphs review, and possible future width profiles; no converter or format extension implemented.
- [Converted stroke-font library](docs/FONT_LIBRARY.md): 87 local PlotFont/Glyphs preparations, per-font licenses, authors, previews and downloadable bundles.
- [Glyphs 4 export plugin](docs/GLYPHS_EXPORT_PLUGIN.md): build a self-contained selected-master exporter with a master chooser and save dialog; native class/action tested and installation verified, startup/menu qualification pending.
- [Using PlotFont in other software](docs/USING_PLOTFONT.md): consumer responsibilities, geometry interchange, and reproducible text layout.
- [Minimal font example](examples/minimal.plotfont.json): an illustrative `A`, space, and fallback glyph.
- [Script font example](examples/script.plotfont.json): ordered curves, entry/exit points, anchors, and glyph user data for optional letter connections.
- [Mixed glyph example](examples/mixed.plotfont.json): an open line combined with a filled region containing a hole.
- [Agent instructions](AGENTS.md): project scope and contribution rules for coding assistants.

## Project status

Confirmed requirements: `.plotfont.json`, Glyphs **4 and later**, and Hershey Roman Simplex as the first repertoire. The five initial milestones and optional layout milestone are complete within the [documented scope](docs/ROADMAP.md). The current format is unreleased draft **0.3**. Existing 0.2 fonts remain supported for compatibility; new plugin exports use 0.3 only.

Implemented here: JSON Schema, semantic validation, a source-pinned Hershey data import, an SVG reference renderer, a selected-master Glyphs export script, and a v0.3-only Glyphs 4 export plugin. Guarded native import, atomic publication, source/export comparison, and independent JavaScript SVG interchange checks are included. Four [Hershey faces](fonts/README.md) have editable `.glyphspackage` sources and native JSON exports: Roman Simplex, Roman Duplex, Roman Triplex, and Script Simplex. Native source reopening, the actual export-script entry point, and curve/metadata/kerning qualification passed. The additional faces were created, populated, saved, and verified through Glyphs MCP in Glyphs 4.1.1. MCP builds advertising `create_document` and `document.create.v1` can create blank fonts directly; population uses a saved document binding.

Review the [SVG specimens](examples/specimens/README.md). See the [milestone plan and completion evidence](docs/ROADMAP.md), [Hershey provenance](fonts/hershey-roman-simplex/README.md), [v0.3 JSON Schema](schemas/plotfont-0.3.schema.json), and [export plugin instructions](docs/GLYPHS_EXPORT_PLUGIN.md). The [script workflow](docs/GLYPHS_EXPORT_SCRIPT.md) adds optional compiled layout.

Draft 0.3 adds self-contained OpenType feature data, HarfBuzz shaping, positioned-run JSON and shaped SVG rendering. The [original layout demo](fonts/layout-demo/README.md) includes an editable Glyphs source, portable compiled fixture and [native export](examples/layout-demo-native.plotfont.json). The native compiler omits this demo's Latin `curs` rule; its export preserves the source and reports that limitation. Cursive positioning is covered by the portable fixture.

The original local font exports in `output/` use draft 0.3: Roman Simplex,
Roman Duplex, Roman Triplex, Script Simplex, and the PlotFont layout demo.
The Hershey files preserve the retained native examples with their format
version migrated to 0.3; the layout demo retains its compiled layout payload.
`HERSHEY-NOTICE.txt` accompanies the exported Hershey data. Superseded generated
font exports have been removed. Plugin builds live in `output/build/` and current
qualification reports in `output/qualification/`. These generated files are
ignored by Git; curated examples and compatibility fixtures remain tracked.
The Glyphs plugin exports geometry-only 0.3; the scripted compiled-layout
workflow adds optional OpenType layout. The 0.2 schemas, examples and Hershey preparations remain
supported compatibility material.

The additional [stroke-font library](docs/FONT_LIBRARY.md) is generated under `output/font-library/`. Its SVG-font and LFF adapters preserve reviewed stroke geometry and license notices. Non-Latin JHF sources have explicitly temporary private-use mappings; see the catalog for coverage and deferred sources. The optional `library` dependencies support this preparation workflow.

## Run locally

Python 3.10 or later. Geometry-only tools use the standard library; OpenType validation and shaping use optional FontTools and uharfbuzz dependencies. Run from this repository:

```sh
python3 -m pip install '.[shaping]'
python3 -m plotfont render examples/layout-demo.plotfont.json 'fi AA' --layout opentype -o output/layout.svg
python3 -m plotfont shape examples/layout-demo.plotfont.json fi -o output/run.json
python3 -m plotfont validate examples/*.plotfont.json fonts/hershey-*/*.plotfont.json
python3 -m plotfont render fonts/hershey-roman-simplex/HersheyRomanSimplex.plotfont.json "Hello PlotFont!" -o output/specimen.svg --cap-height 8
python3 -m plotfont render examples/script.plotfont.json un -o output/joined.svg --join
python3 -m plotfont import-hershey vendor/hershey/scripts.jhf --face script-simplex -o output/HersheyScriptSimplex.plotfont.json
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
```

Render sizes are in millimetres. Existing output is preserved unless the CLI receives `--force`. Fills are SVG areas for review, not generated machining trajectories. Joining is opt-in and currently requires declared endpoints to coincide; it does not invent connecting geometry. The guarded Hershey importer populates empty project sources; a general PlotFont JSON importer into Glyphs, mixed-script/bidirectional segmentation, automatic font fallback, instance interpolation, DXF/HPGL/G-code converters, and device control are not implemented.

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

## OpenType features and remaining questions

Draft 0.3 preserves compiled static OpenType rules and optional authoring source inside the JSON. [The layout profile](docs/PLOTFONT_LAYOUT.md) implements substitutions, language assignments, mark attachment and cursive placement with HarfBuzz. It selects the matching PlotFont drawings; independent strokes and fill intent remain intact. Named anchors alone do not define attachment rules, and cursive placement does not authorize a pen-down connection.

Remaining questions:

- Which feature preferences should particular font families recommend?
- How should consumers segment mixed scripts and bidirectional text and choose fallback fonts?
- How should shaped glyph clusters interact with continuous script drawing and deferred dots/crossbars?
- How should Plot-It save text, feature choices, font identity and resolved runs reproducibly?
- Should a companion preview font be exported automatically, and how should its stroke width be chosen?
