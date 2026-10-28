# Pen profiles — draft 0.4

OpenPlotFont 0.4 adds an optional `penProfile` to each independent `stroke`
operation. Its version is `"1"`. Profiles cannot be attached to fills or fill
contours. The centerline remains the editable drawing trajectory; appearance
contours are reference ink, never additional drawing operations or CNC paths.

The [0.4 schema](../schemas/openplotfont-0.4.schema.json), semantic validator,
Glyphs exporter and reference renderer implement this contract. Existing 0.2
and 0.3 files retain their meanings. A 0.3 reader must reject 0.4; merely changing
a version field does not make a profiled font compatible.

## Locations and authored channels

`points` is an ordered array of `{segment, t, values}` objects. `segment` is a
zero-based drawing-segment index: the first command after `M` is segment zero.
An implicit straight closing edge, when the final command does not end at `M`,
is the final segment. A curved closing edge remains an explicit command.
`t` is the local Bézier parameter in [0,1], **not an arc-distance fraction**.
There is no path rotation, reversal, resampling or knot insertion during capture.
Points must be unique and sorted by `(segment,t)`. Adjacent segments may retain
separate endpoint events. Open endpoints do not wrap. Closed seams preserve
the source events without inventing closure or averaging their values.

`defaults` contains six resolved finite values. Each point's `values` may contain
any of those channels. A missing property means no authored assignment; `null`
preserves an explicitly inherited/unset native property. Both resolve through
the path default when evaluating the portable linear model, but remain distinct
for editing and interchange. Zero is an authored value, not an unset marker.

| Channel | Units and meaning |
| --- | --- |
| `width` | Positive footprint diameter in font units, normal to travel at angle zero |
| `height` | Positive footprint diameter in font units, along travel at angle zero |
| `angle` | Unwrapped degrees counterclockwise relative to the local tangent; zero retains the width-normal orientation |
| `strokePosition` | Dimensionless placement in [-1,1]; positive moves the footprint right of travel by half the width times this value |
| `progressionIn`, `progressionOut` | Native authored interpolation controls; preserved without normalization in the Glyphs model; zero in the linear model |

`style` contains `capStart`, `capEnd` (`butt`, `round`, `square`) and `join`
(`miter`, `round`, `bevel`). These describe visual stroke construction, not
machine travel. Native Round Full and custom joins require separate qualification
and are rejected by this exporter.

## Two explicit interpolation models

### linear-ellipse-v1

This independent portable model interpolates each resolved channel linearly in
`segment + t`, holds the first/last control outside their range, and uses defaults
when there are no points. Angles interpolate as stored unwrapped values; there
is no shortest-angle guess. Progression must be zero. This model must not be
used to relabel native Glyphs controls as though their interpolation were linear.

The reference renderer samples oriented elliptical footprints with round caps
and joins. Its control-polygon step is at most 2 font units, with 48 vertices
per ellipse and a 10,000-sample limit. This is an approximate preview, not a
physical machining-error guarantee. Other cap/join previews fail explicitly.

### glyphs4-v1

This is a source-preserving dialect for Glyphs 4 Pen points. It retains every
native channel, including nonzero progression, node/interior locations and
resolved path defaults. Native progression is nonlinear and is **not** defined
as a generic easing ratio or as linear interpolation. A consumer must implement
that dialect or explicitly select its own approximation; it must never silently
claim native-equivalent pressure or appearance from linear width interpolation.

To make appearance portable without depending on Glyphs' interpolation engine,
this model requires an `appearance` reference. It stores closed native-expanded
contours, a `nonzero` compound fill rule, renderer `source`, and `bindingSha256`.
The exact reference is used by the SVG renderer. It does not replace the
centerline/profile and must not be plotted as boundary rails or treated as
physical depth. Editing controls requires regenerating the appearance in its
source renderer; this release does not provide a generic native-profile editor
or a source-independent evaluator of Glyphs progression.

The binding is SHA-256 of UTF-8 JSON containing `closed`, `commands`, and
`penProfile` without `appearance`, with sorted object keys, no whitespace,
literal Unicode and finite JSON numbers. It detects stale geometry/profile
bindings; it does not authenticate a producer or prove that the reference is
correct. Appearance contours themselves remain validated geometry. Consumers
must retain these authoring/reference distinctions.

## Native export and limitations

Glyphs 4.2 build 4202 qualification confirms that native Pen points belong to
the ending on-curve node, and `t` is local to that segment. An open start uses
`t=0` on the first segment's ending node. The native unset width/height/angle
sentinel is converted to `null`, never serialized as an enormous dimension.
Saved source may omit an explicit zero angle and reopen it as inherited; export
preserves the **saved** state rather than inventing a pre-save explicit flag.

The exporter reads precise coordinates, copies/decomposes layers, and obtains
appearance from the copied native path. It does not save or edit the source.
Pen-point mappings through quadratic/implied-point conversion, off-curve-owned
controls, open first-node controls, and profile-bearing components/transforms
are rejected with diagnostics. Prepare and verify a separate decomposed cubic
authoring copy when necessary. Geometry-only component decomposition remains
available, including the explicit centerline fallback. These limits prevent
unqualified profile remapping; they do not silently drop source data.

Original synthetic examples and their editable source are in
[the profile demo](../fonts/pen-profile-demo/README.md). Native class/action
qualification is distinct from installed plugin startup/menu qualification.

## Constant-width output and writing masks

`python3 -m openplotfont centerlines input.opf.json -o simple.opf.json` makes an
explicit 0.3 copy without profiles or appearance references. It preserves every
XY command, stroke boundary/order, start, closure, mapping, advance, anchor,
kerning pair and optional compiled layout. The result records loss of variation.
It is suitable for a conventional pen plotter; its physical pen determines ink
weight. A preview can also select `render --profiles centerline` explicitly.

`render --writing-mask` creates per-stroke SVG masks and ordered SMIL playback.
The default demonstration speed is 20 mm/s with 0.15-second pen-up intervals;
`--speed` and `--pen-lift` change those preview settings. Closed loops trace once;
separate strokes remain separate. The timing is invented for demonstration,
not inferred handwriting or motion instructions. Broad centerline masks can
reveal nearby parts of the same stroke early, especially at self-intersections.
Fills and joined profiles require a separate scheduling policy and fail clearly.

Physical pressure, CNC depth, tool calibration, clearance, feed rates and video
production belong to consuming applications. This release preserves their input
data; it does not implement hardware mappings or plot-it profile rendering.

Native API references: [GSPenPoint](https://docu.glyphsapp.com/Core/GlyphsCore/GSPenPoint/),
[GSPath](https://docu.glyphsapp.com/Core/GlyphsCore/GSPath/), and the
[Strokes handbook](https://handbook.glyphsapp.com/strokes/).
