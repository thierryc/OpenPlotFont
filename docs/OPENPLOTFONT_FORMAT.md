# OpenPlotFont format — draft 0.3

Status: draft specification, implemented for validation and reference rendering; subject to review before stable release.

Version **0.3** is the current draft and the Glyphs plugin's only output version.
It supports geometry-only fonts and fonts with optional compiled OpenType
`layout`. Version 0.2 remains accepted by the reader for existing fonts and
compatibility fixtures. The geometry rules below apply to both versions unless
an explicit version restriction is stated.

## What an OpenPlotFont describes

An OpenPlotFont contains named glyphs, Unicode mappings, font metrics, advances, and ordered drawing operations. A glyph may combine centerline strokes and filled regions. For example, `A` can use one open stroke for its two diagonals and a second stroke for the crossbar; another design could add a filled decoration. A consumer raises the pen between independent stroke trajectories.

“Single-line” means centerline geometry. It does not mean one continuous stroke per character. A connectable handwriting body uses an open stroke. A centerline loop such as `O` may remain closed and be traced once. A closed contour describing a filled shape instead defines an area that the destination software converts into toolpaths. **Closure and drawing intent are separate properties.**

The format represents reusable font geometry. A composed SVG or DXF represents a particular drawing. A machine file represents movement for a particular controller and tool setup.

## Container

The supported extensions are `.opf` and `.opf.json`, with `.opf.json` as the default export suffix. Both contain the same UTF-8 JSON object. Reject duplicate JSON property names rather than allowing parser-dependent interpretations. No executable code, external geometry references, or embedded device commands are allowed.

The 2026-10-07 project rename is an incompatible identity change within the unreleased drafts: `format` must be `OpenPlotFont`, Python imports and the CLI use `openplotfont`, and authoring metadata uses `org.openplotfont`. Pre-rename format identifiers and metadata keys have no compatibility aliases. Draft versions `0.2` and `0.3` describe the same geometry/layout capabilities as before; a supported version alone does not make an old identifier valid. Existing authoring settings must be migrated explicitly before export.

The retained 0.2 [minimal example](../examples/minimal.opf.json) illustrates the geometry shared with 0.3; its glyphs are illustrative drawings, not a complete font. The [native layout demo](../examples/layout-demo-native.opf.json) is a complete 0.3 conformance fixture with optional compiled layout.

| Field | Type | Meaning |
| --- | --- | --- |
| `format` | string | Must equal `OpenPlotFont` |
| `version` | string | Current draft: `0.3`; legacy `0.2` is also accepted by the reader |
| `id` | string | Stable font identifier within a consumer's catalog |
| `familyName` | string | Display family name |
| `styleName` | string | Display style name |
| `unitsPerEm` | positive integer | Font coordinate scale |
| `metrics` | object | `ascender`, `descender`, `capHeight`, `xHeight`, `lineGap` |
| `missingGlyph` | string | Name of an existing fallback glyph |
| `glyphs` | array | Collection of unique glyph records; collection order is for editing, not drawing |
| `kerning` | array, optional | Explicit glyph-name pairs and adjustments |
| `metadata` | object, optional | Author, provenance, copyright, license, source details |
| `layout` | object, optional in 0.3 only | Self-contained compiled static OpenType layout; see [layout specification](OPENPLOTFONT_LAYOUT.md) |

All table fields are required except those marked optional. Identification strings must be nonempty; glyph names and Unicode mappings must be unique. Provenance and license details are strongly recommended for redistribution but are not required by the draft schema.

Consumers must reject unsupported versions with a clear error. Unknown fields may be ignored, but must never change geometry or text layout. A future editing tool should preserve unknown fields when rewriting a file. The font identifier is not a content hash: projects should also pin the exact font version or file digest for reproducible rendering.

## Coordinates and metrics

- All geometry, advances, and kerning use font units.
- X increases rightward; Y increases upward.
- The baseline is `y = 0`; the glyph origin is `x = 0`.
- `ascender` is positive; `descender` is zero or negative.
- `capHeight` is positive; `xHeight` and `lineGap` are nonnegative.
- Line advance is `ascender - descender + lineGap` and must be positive.
- Coordinates may be negative or extend beyond metrics and advances. Consumers calculate actual geometry bounds and must not crop overhangs or descenders to the em box.

For a requested cap height `H` millimetres:

```text
scale = H / metrics.capHeight
x_mm = originX_mm + x_font × scale
y_mm = baselineY_mm - y_font × scale    # downward-Y page such as SVG
```

Every point and curve control point receives the same transformation. For an upward-Y CAD drawing, use addition on Y instead. Scaling by `unitsPerEm` specifies em size, which is a different operation from scaling by cap height.

## Glyph records

Each glyph is a self-contained description of its identity, spacing, ordered drawing operations, and optional authoring and connection information. The first four fields are required; the remaining fields are optional:

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string | Unique stable name, such as `A`, `space`, or `.notdef` |
| `unicodes` | array of strings | Unicode scalar values in uppercase hexadecimal, such as `0041` |
| `advanceWidth` | nonnegative number | Horizontal advance in font units |
| `strokes` | array | Ordered drawing operations: centerline strokes and/or filled regions |
| `connections` | object, optional | Explicit `entry` and/or `exit` endpoint references for script joining |
| `anchors` | array, optional | Named points for attachment, alignment, or authoring |
| `userData` | object, optional | Application-specific JSON data retained with this glyph |

Unicode strings use 4–6 digits with no `U+` prefix and the shortest length of at least four digits. They must describe scalar values from `0000` through `10FFFF`, excluding `D800`–`DFFF`. Each scalar maps to at most one glyph; multiple scalars may map to one glyph. `unicodes: []` is valid for unencoded glyphs.

The `simple` consumer profile uses left-to-right scalar lookup. Draft 0.3 additionally defines optional [OpenType layout](OPENPLOTFONT_LAYOUT.md) for ligatures, alternates, contextual substitutions and mark/cursive positioning. Simple mode executes none of these rules. Mixed-script/bidirectional run segmentation and variable fonts remain outside the reference implementation. Consumers must document any normalization or case substitution they apply; case substitution is not an implicit format behavior.

An unsupported scalar uses `missingGlyph`. Space is a real encoded glyph with an advance and no strokes. A consumer handles line breaks outside glyph lookup. Tabs need an explicit consumer policy.

## Drawing intent: strokes and filled shapes

Each item in `strokes` has a `kind`: `stroke` or `fill`. Omission means `stroke`, retaining the compact existing stroke representation. The array name is retained from draft 0.1; it now contains drawing operations, not exclusively ready-to-draw trajectories. Unknown kinds are errors and must never be ignored.

| Operation | Stored geometry | Destination behavior |
| --- | --- | --- |
| `stroke`, open | One path with `closed: false` | Trace its centerline; eligible for declared script connections |
| `stroke`, closed | One path with `closed: true` | Trace the loop once; do not fill it |
| `fill` | One region containing closed boundary contours and a fill rule | Generate toolpaths to cover or machine the region after physical sizing |

Use `kind: "fill"` to express the visible area of regular outline lettering or a filled part within a stroke glyph. Never guess this intent from closure, direction, thickness, or user data. The font records the desired geometry and whether to trace or fill it, not a tool-specific approximation.

A stroke operation has `closed` and `commands`, with optional explicit `kind: "stroke"`. A fill operation has required `kind: "fill"`, `fillRule`, and `contours`. It has no operation-level `closed` or `commands`; each contour supplies those fields. Do not mix the two record structures.

## Filled regions and holes

`fillRule` must be `evenodd` or `nonzero`. A fill operation's nonempty `contours` array describes a single compound region, including any holes. Each contour uses the same absolute commands as a stroke and must have `closed: true`. The fill rule determines interior membership across all its contours: `evenodd` uses crossing parity; `nonzero` uses signed winding. For `nonzero`, preserve contour direction and the relationship between outer boundaries and holes. Contour-array order is stored geometry order, not a toolpath schedule.

```json
{
  "kind": "fill",
  "fillRule": "evenodd",
  "contours": [
    {"closed": true, "commands": [["M", 100, 550], ["L", 300, 550], ["L", 300, 750], ["L", 100, 750]]},
    {"closed": true, "commands": [["M", 160, 610], ["L", 240, 610], ["L", 240, 690], ["L", 160, 690]]}
  ]
}
```

This example is a filled square with a square hole. Store its contours together: separate fill operations would lose the shared hole relationship. Consumers supporting only centerlines must reject fill operations with an actionable message, not trace just their boundaries, silently omit them, or treat their contours as ready-to-plot strokes.

The font does not store hatch spacing, tool diameter, stepover, offsets, fill angles, machining depth, or precomputed fill trajectories. After laying out and sizing the glyph, the plotter/CAM software uses the actual pen or cutter and its own fill strategy to generate potentially many independent paths. It preserves holes, applies tool compensation where appropriate, and reports features that the selected tool cannot reproduce. It must not silently bridge a hole or replace a filled area with its outline.

See [mixed.opf.json](../examples/mixed.opf.json) for an illustrative glyph containing an open line and a filled dot with a hole. This is format data only; fill-path generation is not implemented.

## Stroke records and commands

Each stroke contains `closed` (boolean) and `commands` (array). Commands are absolute coordinates in glyph space:

| Command | Array | Meaning |
| --- | --- | --- |
| Move | `["M", x, y]` | Starting point, reached with pen raised |
| Line | `["L", x, y]` | Draw to endpoint |
| Quadratic | `["Q", cx, cy, x, y]` | Draw quadratic Bézier segment |
| Cubic | `["C", c1x, c1y, c2x, c2y, x, y]` | Draw cubic Bézier segment |

Every stroke or fill contour starts with exactly one `M` and contains at least one drawing command. A later `M` is invalid: start a new stroke or contour instead. All numbers must be finite. Relative coordinates, SVG shorthand, arcs, and a `Z` command are outside draft 0.3 and its legacy 0.2 geometry model.

`closed: false` means stop at the final endpoint and raise the pen by default. The explicit script-joining mode described below may continue from a declared exit into the next glyph's declared entry. `closed: true` adds a straight segment back to the initial point if needed, then raises the pen. A curved closing segment must be encoded explicitly as `Q` or `C` ending at the initial point. Never add closure because two endpoints look close. An open stroke may intentionally return to its start; its open status still remains explicit.

Array order defines operation order; command order defines stroke direction. Optimization happens only with an explicit consumer setting. A centerline dot may use a small drawable segment or loop; an area-shaped dot may use a fill operation. A stationary pen dwell is not part of this version.

Example `A`:

```json
{
  "name": "A",
  "unicodes": ["0041"],
  "advanceWidth": 650,
  "strokes": [
    {"closed": false, "commands": [["M", 50, 0], ["L", 300, 700], ["L", 550, 0]]},
    {"closed": false, "commands": [["M", 150, 280], ["L", 450, 280]]}
  ]
}
```

The move between the diagonals and the crossbar is a pen-up travel move.

## Drawing order and glyph endpoints

The `strokes` array is the drawing schedule: process operation `0`, then `1`, and so on. A stroke produces its declared trajectory; a fill produces a block of toolpaths chosen by the destination software. Complete that fill block before the next operation in preserve-order mode. Commands inside each stroke define its direction. No separate `pathOrder` field is needed. A consumer must not sort operations, rotate a centerline loop's start, or reverse a stroke without an explicit user setting. Fill-path ordering is a consumer choice within its operation.

For a glyph containing only stroke operations, the first drawing point is the `M` point of its first stroke. The last drawing point is the final command's endpoint of its last open stroke, or the starting point of its last closed stroke after closure. A space has neither point. These points are derived from geometry rather than duplicated as coordinates that could become stale. For glyphs beginning or ending with a fill, the corresponding actual drawing endpoint depends on generated toolpaths and is not a font-level endpoint.

Drawing endpoints are not automatically script connection points. The first path might be a dot, or the last path might be a crossbar. An author declares connection intent using `connections`; proximity alone is insufficient.

## Entry and exit points for script lettering

`connections.entry` identifies the point that may connect to the **previous glyph's exit**. `connections.exit` identifies the point that may connect to the **next glyph's entry**. Each reference contains a zero-based `strokeIndex`, an `endpoint` (`start` or `end`), and optional `userData`. Its coordinates come from the referenced stroke, in font units:

```json
{
  "connections": {
    "entry": {"strokeIndex": 0, "endpoint": "start"},
    "exit": {"strokeIndex": 0, "endpoint": "end"}
  },
  "userData": {
    "org.openplotfont.authoring": {"note": "Continuous script body; joins at baseline shoulder."}
  }
}
```

In draft 0.3 and legacy 0.2, `strokeIndex` indexes the ordered operations in `strokes`. Entry must reference the start of the first operation and exit the end of the last operation; both referenced operations must be open `stroke` records, never fills or fill contours. Either connection may be omitted, preventing joining on that side. This restriction preserves drawing order. A glyph with later dots, crossbars, or fills cannot declare an exit on an earlier body stroke in this draft; designing deferred finishing operations needs a future explicit scheduling model.

Connections are optional drawing information, not machine commands or OpenType cursive positioning rules. The 0.3 renderer rejects joining in OpenType mode until a cluster-aware drawing schedule is defined. The default renderer draws all strokes independently. A consumer with a user-enabled script-joining mode may join only adjacent, explicitly mapped glyphs on the same text line, with a declared exit on the left and entry on the right. Spaces, line breaks, and substituted missing glyphs break the chain.

First apply advances, kerning, placement, and scaling. Then evaluate both endpoints in document space. A basic joining mode may keep the pen down only when the endpoints coincide within a documented numeric tolerance; that tolerance must not authorize a visible connecting segment. A nonzero gap requires an explicit connector policy and preview, such as a straight line or a separately designed curve. The file does not prescribe such a connector or authorize snapping, changing spacing, moving points, or guessing tangents.

An approved join becomes a continuous trajectory in the generated drawing, with no pen-up travel across the join. Other strokes remain separate. A consumer that does not support joining must still render the original glyph strokes correctly. Joining and trajectory optimization must not conflict: preserve the assembled script chain's direction and sequence unless the user explicitly permits changing them.

See [script.opf.json](../examples/script.opf.json) for two illustrative curved glyphs whose exit and following entry coincide at their normal advances. The reference renderer implements opt-in joining for coincident declared endpoints; nonzero gaps require a connector policy and are rejected.

## Named points and user data

`anchors` stores optional named points independently of pen-path endpoints:

```json
{
  "anchors": [
    {"name": "top", "x": 250, "y": 550, "userData": {"org.openplotfont.authoring": {"role": "alignment"}}}
  ]
}
```

Each anchor has a unique nonempty `name`, finite `x` and `y` coordinates in font units, and optional `userData`. Transform anchors with glyph geometry. They do not draw anything, create joins, or define mark positioning by themselves. Entry/exit references remain tied to actual stroke endpoints; an arbitrary anchor is not a replacement for a drawable endpoint.

Glyph, anchor, and connection-point `userData` are JSON objects whose values may be any JSON value. Use namespaced keys, such as `org.openplotfont.authoring`, to avoid collisions. Store notes, tags, source point identifiers, or editor settings here. Preserve these objects when importing, editing, and exporting; consumers may ignore unfamiliar keys. User data must never override standard geometry, order, spacing, or connection semantics, contain executable instructions, or control a machine. Geometry-affecting features need defined versioned fields rather than private user-data conventions.

These optional metadata fields are supported by the validator and reference renderer. The Glyphs adapter preserves them in native Glyphs 4.1 qualification and portable regression tests.

## Spacing and kerning

In simple mode, place a glyph at the current horizontal origin, advance by `advanceWidth`, then apply any pair adjustment before the next glyph. In OpenType mode, use the shaped advances and offsets; never apply these pair adjustments again. Kerning records have `left`, `right`, and `value`; names must exist in the glyph collection and pairs must be unique. Negative values reduce the gap. Missing pairs contribute zero.

```json
{"left": "A", "right": "V", "value": -50}
```

Group kerning and metrics expressions from Glyphs are resolved into numeric glyph-pair values before export. Draft 0.3 carries resolved geometry and spacing for one static font, not Glyphs components or expressions. Optional compiled layout supplies shaping in OpenType mode.

## Validation before use

The semantic validator checks the version, required fields and types, metric constraints, unique names and Unicode mappings, fallback existence, operation kinds and record structures, command names and arities, numeric values, stroke structure, and kerning references. Fill operations require supported fill rules and nonempty closed contours. It also checks connection indices and endpoint restrictions (including rejection of fills), unique anchor names and finite coordinates, and JSON-object user data. A glyph without strokes cannot declare connections. Consumers should bound file size, operation, contour and command counts, and metadata depth before rendering.

Preserve coincident endpoints and path boundaries during conversion. Reject unsupported source objects with an actionable message instead of silently dropping them. The current [0.3 schema](../schemas/openplotfont-0.3.schema.json) and legacy [0.2 schema](../schemas/openplotfont-0.2.schema.json) validate structure; [semantic validation](../openplotfont/validation.py) additionally checks geometry, canonical Unicode scalars, and cross-references.

## Information outside the format

Paper size, physical text size, origin, color/tool assignment, tool diameter, pen pressure, feed rate, acceleration, Z depth, servo settings, device units, and return-to-origin policy belong to the document, exporter, CAM setup, or machine profile.

Optional metadata can record authorship and provenance. A metadata license string is not a substitute for permission to redistribute the source font. Original project works use MIT; imported fonts retain their upstream terms. See [licensing](../README.md#licensing).

## Draft compatibility

Draft `0.2` supersedes unreleased draft `0.1` to introduce mixed stroke/fill operations. Existing stroke-only records are unchanged and may be migrated by validating them and updating the file version; no geometry conversion is needed. Fill records introduce new semantics, so a `0.1`-only reader must reject `0.2`. A `0.2` reader without fill support must reject fonts containing fill operations. Never use unknown-field tolerance to discard drawing intent. No released standard or implemented reader is changed by this revision.

Draft `0.3` retains all 0.2 geometry and adds optional `layout`. A 0.2-only consumer must reject version 0.3, even if it could otherwise ignore fields. Geometry-only 0.2 files need no migration. A 0.3 file without layout behaves like 0.2. Unknown layout profiles are errors, and an unsupported OpenType renderer must report the limitation rather than silently substitute simple rendering.

To migrate valid geometry-only data to 0.3, change `version` to `"0.3"` and
validate against the 0.3 schema and semantic validator. Coordinates, drawing
intent, order, metrics and metadata require no conversion. This migration does
not add shaping: compiled layout must be attached through the separately
validated layout workflow. The retained 0.2 examples remain unchanged so
compatibility coverage is reproducible.

## Questions before format release

- Decide whether provenance fields beyond the currently required identity fields should become mandatory. The supported extensions are `.opf` and `.opf.json`; this implementation accepts versions `0.2` and `0.3` and rejects other versions.
- Decide which shaping requirements belong in the initial release; Hershey Roman Simplex is the first repertoire; see the [OpenType questions in the README](../README.md#opentype-features-and-remaining-questions).
- Confirm the entry/exit restrictions and whether deferred finishing operations need a later scheduling model.
- Review the implemented schema and semantic checks with independent font-aware consumers before declaring a stable release.
