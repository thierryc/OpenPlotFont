# Original Pen-profile demo

This MIT-licensed synthetic fixture is original OpenPlotFont test artwork,
created in Glyphs 4.2 build 4202. It contains no traced font or third-party design.
The native source includes nine encoded demonstrations A–I, space, `.notdef`,
and a nonexporting component diagnostic. The export has eleven glyph records
and eleven independent profiled strokes; I has a separate short mark.

[Editable native source](PenProfileDemo.glyphspackage),
[0.4 export](../../examples/pen-profile-demo.opf.json),
[explicit 0.3 centerline projection](../../examples/pen-profile-centerlines.opf.json).

The demonstrations cover constant/variable width, native progression,
noncircular/oriented footprints, placement, a cubic trajectory, a closed loop,
inherited values and independent strokes. The native source was saved through
Glyphs MCP and read independently into a detached native font. Exact raw
readback and native-expanded contours are retained in the portable
[verification fixture](../../tests/fixtures/pen-profile-native-records.json).
Tests compare native and exported nodes, starts, direction, closure, segment
mappings, every raw channel, inherited defaults, advances and expanded geometry.

The updated plugin's native settings view and both actions were executed on
this saved/reopened fixture. This is class/action qualification, not installation
or cold-start/menu qualification. Profile-bearing components are rejected;
explicit centerline output can decompose their geometry. Source font data was
preserved during export. No hardware was operated.

These are conformance drawings, not an approved handwriting family. See
[the profile specification](../../docs/PEN_POINTS.md) for interpolation models,
appearance binding, unsupported mappings and writing-mask limitations.
