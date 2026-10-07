# Editing in Glyphs and exporting OpenPlotFont

Target: Glyphs **4 and later**. A selected-master Python export script and [geometry export plugin](GLYPHS_EXPORT_PLUGIN.md) are included, with offline adapter tests. Native execution, source reopening, and Hershey source-to-export comparison passed in Glyphs 4.1. The plugin's class/action passed direct MCP qualification in 4.1.1 and installation was verified; startup and visible export-tab qualification remain pending. The format stores one resolved static font per file; resolved instance export is a later task. See [script setup and annotations](GLYPHS_EXPORT_SCRIPT.md).

For new geometry exports, use the **v0.3-only plugin** (plugin release 0.1.1).
For optional compiled OpenType layout, use the source-bound scripted workflow.
The tool versions and output versions are separate:

| Export route | OpenPlotFont output | OpenType layout |
| --- | --- | --- |
| Glyphs 4 plugin 0.1.1 | 0.3 only | Geometry only; active feature warnings retained |
| Export script with matching compiled font | 0.3 | Validated compiled layout and authoring source |
| Export script without compiled font | Legacy 0.2 | Geometry only |
| Pinned Hershey data preparation | Legacy 0.2 | Geometry only; retained for reproduction and compatibility |

## Design the source in Glyphs

Keep the editable `.glyphs` or `.glyphspackage` source. Glyphs supports open paths, node and handle editing, metrics, and Unicode assignments. Draw the trajectories you want the pen to follow; use separate paths when the pen must lift. Keep loops closed only when the design requires them. Set consistent baseline, cap height, advances, and spacing. These editing capabilities are documented in the [official Glyphs Handbook](https://handbook.glyphsapp.com/en/single-page/).

Start with a small specimen: `A`, `O`, a curved glyph, a descender, space, and `.notdef`. Review it as stroke geometry, since a filled font preview does not show the intended pen trajectories reliably.

For mixed glyphs, author centerlines and filled boundaries as distinct intended operations. Keep the connectable handwriting body open. A closed path may be a centerline loop or a fill boundary: mark its intent explicitly rather than classifying every closed path as filled. Group the outer boundary and holes of each filled region into one compound fill operation. Filled parts may retain regular outline-font geometry; do not infer a centerline from them. The draft annotation convention is documented in [the script instructions](GLYPHS_EXPORT_SCRIPT.md); its native round trip passed qualification.

Do not expand the centerlines into thick outlines before OpenPlotFont export. Conventional outline-font export can give application-dependent results for open contours. Read geometry directly from the editable source rather than using an OTF/TTF round trip to preserve pen paths. The [Glyphs discussion on unclosed outlines](https://forum.glyphsapp.com/t/export-a-singleline-font-with-unclosed-outlines/24814) explains that open/closed behavior depends on the application interpreting compiled outlines.

## Export contract

The script implements the selected-master portion of this contract; native acceptance checks passed for the Hershey source and dedicated fixtures:

1. Select one master or resolved static instance explicitly. Do not export every master layer as another stroke.
2. Work on a copy of the layer. Resolve components and their transforms; fail on unresolved references, cycles, or unsupported shapes.
3. Resolve advances and metrics into numbers. Include exported glyphs, their names, all Unicode mappings, and a fallback glyph. Preserve unencoded glyphs when referenced by the exported font.
4. Translate each authored centerline path into one stroke and each authored filled region into a fill operation containing its closed contours and explicit fill rule. Preserve start points, direction, open/closed state, holes, and operation order. Map line segments to `L`, quadratic segments to `Q`, and cubic segments to `C` using their actual control points. Handle implied points explicitly.
5. Preserve source coordinates: upward Y, baseline at zero. Do not rescale or flatten curves at this stage.
6. Resolve kerning groups and exceptions into effective glyph pairs. For geometry-only export, including the v0.3 plugin, report uncompiled shaping features and unsupported source objects instead of silently omitting them. To include optional v0.3 layout, attach a matching compiled static font and preserve authoring feature source through [the implemented layout export](GLYPHS_EXPORT_SCRIPT.md#optional-03-layout-export).
7. Validate the complete file, report diagnostics with glyph and path names, and write `.opf.json` deterministically.
8. Render a specimen to SVG for comparison with the source before publishing an export.

The exporter should also preserve the author's path order as the `strokes` array and carry supported glyph user data, named anchors, and explicit entry/exit endpoint annotations. The Glyphs user-data convention is specified in the script instructions and tested with adapter doubles; native anchors, endpoint metadata, and JSON-compatible user data passed qualification. Do not infer joining intent from nearby points or anchor names. When resolving components or changing path indices, remap endpoint references and validate them against the final exported geometry; report references that no longer identify permitted endpoints.

The script can be inspected and installed for qualification, but this project has executed it on a copy in Glyphs 4.1. Glyphs API usage was checked against the official SDK documentation; portable tests complement the recorded native qualification. The official [export documentation](https://handbook.glyphsapp.com/export/) describes existing export options; it does not establish native OpenPlotFont support.

## Converting an OpenPlotFont to a drawing

Choose text and cap height in millimetres, map scalars to glyphs, apply advances and kerning, then transform every stroke into document space. Keep the original text and font identity with the editable document. Handle line breaks using the font metrics. Calculate actual stroke bounds, including overhangs.

Transform filled-region contours along with the strokes. For a geometry/preview output, preserve their area and fill rule. For machine-ready output, generate fill trajectories only after physical sizing, using the destination's pen/cutter width, coverage strategy, stepover, and compensation. Preserve holes and flag features the selected tool cannot reproduce. Fill generation belongs to the plotter/CAM application; a device controller need not provide that feature itself.

The resulting geometry can be exported for several destinations:

| Output | Intended use | Conversion requirements |
| --- | --- | --- |
| SVG | Vector editors and plotter applications | Explicit mm page dimensions; independent centerlines use `fill="none"`; preserve compound fills for preview or generate separate fill trajectories for plotting |
| DXF | CAD drawing exchange | Preserve centerlines and explicitly supported regions/holes, or export generated fill paths; document units, axes, and unsupported area semantics |
| HPGL | Compatible plotters | Map to device units; emit separate pen-up travel and pen-down drawing; use a device profile |
| G-code | A specific CNC or pen controller | Explicit units, coordinate mode, tool-up/down actions, feeds, and travel behavior from a controller profile |

The reference SVG renderer is implemented; DXF, HPGL, and G-code converters are planned. Selecting a format does not make all machines compatible. DXF is a geometry handoff to CAD/CAM; engraving depth and machining strategy belong in CAM or a machine profile. G-code and HPGL are drawing/job outputs, not equivalent font containers.

For SVG, serialize each stroke independently:

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     width="30mm" height="20mm" viewBox="0 0 30 20">
  <g fill="none" stroke="#000" stroke-width="0.3"
     stroke-linecap="round" stroke-linejoin="round">
    <path d="M 5 15 L 10 1 L 15 15"/>
    <path d="M 7 9.4 L 13 9.4"/>
  </g>
</svg>
```

The crossbar is a separate path and needs separate pen travel. Use `Z` only when `closed` is true. SVG stroke width is a visual preview attribute; it does not change the tool's physical width.

A preview SVG can instead display a fill operation as a compound path with an explicit `fill-rule` and no boundary stroke. A visible SVG fill is not proof of machine coverage. For a plot-ready SVG, replace that region with the destination-generated fill trajectories, one separate path element per independent pen-down trajectory. If fill generation is unavailable, report the limitation rather than exporting only the outlines as an equivalent result.

If a destination accepts only polylines, flatten curves after physical scaling with a documented maximum error in millimetres. Retain stroke endpoints and closure. A sample spacing alone is not an error bound, particularly around tight curves.

## Review before exporting

Compare glyph count, mappings, advances, metrics, strokes, endpoints, and closures with the source. Confirm curves survive the font export. Check the drawing at a known cap height and verify that travel between strokes is pen-up. A converter must not join disconnected paths or reverse them without an explicit optimization setting.

For mixed glyphs, also compare operation kinds, grouped contours, fill rules, and holes. Check generated fill coverage with the selected physical tool size; raw font boundary contours must not be sent directly as fill toolpaths.

For script lettering, review entry and exit points in a multi-glyph specimen after spacing and scaling. Join only with an explicit consumer setting and retain unrelated pen-up boundaries. Verify that user data and anchors survive export even when the drawing consumer does not use them.

Reopening `.opf.json` directly in Glyphs would require a future importer. Keep the Glyphs source as the authoring file; do not promise a lossless round trip for masters, components, hints, features, or editor metadata absent from this draft.

## Remaining export questions

- How should a resolved static instance be selected and exported without changing the source?
- How should annotated components remap path references? The current adapter rejects them rather than guessing.
- Should export also generate a companion OpenType font? See the [preview questions in the README](../README.md#reflection-a-companion-font-for-design-previews).
- Which drawing interchange formats and CAD versions should verify compatibility? Device profiles and machine output belong to consuming applications.
