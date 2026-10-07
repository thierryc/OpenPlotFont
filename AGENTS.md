# Instructions for agents working on OpenPlotFont

## Purpose

Define a portable JSON font format supporting centerline strokes and filled regions, and its Glyphs editing, export, and saving workflow. Start from the documentation in `docs/` and the draft examples in `examples/`. Consumer applications are separate projects with their own roadmaps; do not turn this repository into a plotter application or device-driver project.

## Source of truth

- Read `README.md`, `docs/OPENPLOTFONT_FORMAT.md`, and the relevant workflow document before changing the format or integrations.
- Preserve the distinction between confirmed user requirements, draft design decisions, and implemented behavior. Never present a proposed importer or exporter as available.
- Keep project documentation focused on the specification, authoring workflow, examples, and open design questions. Do not add conversation-recovery documents, chat identifiers, or local implementation audits of other projects.
- Keep format versions, examples, schemas, and implementations consistent. Record incompatible changes explicitly.

## Geometry rules

- Preserve open paths, explicit closure, stroke order, start points, and direction.
- Each stroke is an independent pen-down trajectory. Never connect separate strokes with a drawing move.
- Script connections are an explicit exception only in a user-enabled joining mode, using declared glyph entry/exit endpoints and a reviewed connector policy. Preserve all other pen-up boundaries and drawing order.
- Store font geometry in font units with an upward Y axis. Convert to millimetres and the destination axis convention at the drawing/export boundary.
- Preserve curves until an output needs flattening; flatten with a documented physical error tolerance.
- Do not infer centerlines from filled outline fonts, expand stroke widths, close open paths, or reorder artwork silently.
- Keep pen widths, feeds, acceleration, Z motion, servo commands, and device calibration outside the font data.
- Preserve explicit stroke/fill intent, compound region contours, fill rules, and holes. Closure alone does not imply filling. Generate fill toolpaths in destination software after physical sizing using actual tool settings; reject unsupported fills rather than silently plotting only their boundaries.

## Implementation and verification

- Keep dependencies small and justified. Do not add an app framework or build system to this format/tooling repository without a concrete implementation need.
- Add meaningful fixtures when implementing geometry: separate strokes, explicit loops, curves, spaces, missing glyphs, scaling, axis conversion, and unsupported versions.
- Validate touched JSON and documentation links. Documentation-only changes do not require an application test suite.
- Keep Glyphs source files separate from generated exports. Export from copies without mutating the user's original font.
- Read related repositories when needed, but make changes here unless the user authorizes work elsewhere.
- Verify Glyphs API and exporter behavior against official documentation and the target app version before coding or promising support.
- Report what changed, what was verified, and any remaining compatibility gaps.

## Scope and collaboration

Use ordinary independent work by default. Do not publish, push, choose a license, or operate hardware as a side effect of editing this repository. Keep generated local output in `output/`; retain curated examples in `examples/`.
