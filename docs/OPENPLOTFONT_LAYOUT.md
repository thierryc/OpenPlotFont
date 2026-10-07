# OpenType layout — draft 0.3

OpenPlotFont 0.3 adds an optional, self-contained `layout` object. The glyph drawings,
metrics, anchors, connections and explicit kerning retain their 0.2 meanings.
The implemented profile is `opentype-static-v1`: a compiled static OpenType font
selects and positions glyphs; OpenPlotFont supplies their actual stroke/fill geometry.
It supports GSUB substitutions, GPOS positioning and GDEF lookup behavior through
HarfBuzz, rather than defining a second feature-rule language.

## Container and authority

| Field in `layout` | Meaning |
| --- | --- |
| `profile` | Required exact string `opentype-static-v1` |
| `font` | Required `encoding: "base64"`, canonical base64 `data`, lowercase hex `sha256` of decoded bytes |
| `glyphOrder` | Required array: index is the compiled glyph ID; value is an OpenPlotFont glyph name |
| `features` | Required feature manifest: each record has `tag`, optional `label`, optional `recommendedValue` |
| `systems` | Required manifest of GSUB/GPOS script/language assignments and required features |
| `source` | Optional preserved authoring source and its integrity/binding digests |

See [the original layout fixture](../examples/layout-demo.opf.json) and
[0.3 schema](../schemas/openplotfont-0.3.schema.json) for a complete example. Its
embedded font has empty preview outlines intentionally: only OpenPlotFont drawings
are rendered. The embedded font is not an automatically generated design preview.

The binary is the execution authority. The manifest describes its coverage;
it does not replace lookup order, contextual matching or attachment rules.
`systems` records contain `table` (`GSUB` or `GPOS`), four-character OpenType
`script` and `language` tags (`dflt` for a default language system), a sorted
`features` array and nullable `requiredFeature`. The validator derives these
records from the compiled tables and requires an exact match.

`glyphOrder` must cover every drawing exactly once. Glyph ID zero maps to
`missingGlyph`. Count, units per em, Unicode cmap and all horizontal advances
must match. The map is explicit because compiled production names can differ
from source names. Obtain it from the compiler/export process; matching names,
counts and metrics alone cannot establish the identity of unencoded alternates.
Do not guess an order or infer it from the OpenPlotFont glyph collection.

The payload accepts one plain static TTF or CFF-based OTF sfnt, up to 8 MiB and
128 tables. Collections, WOFF, variable fonts, AAT layout and Unicode variation
selector mappings are outside this profile. Directory ranges, duplicates,
overlaps, required tables, feature references and mappings are validated.
This validation is not a general-purpose font security sanitizer. Consumers
must use maintained font parsers and their own resource limits.

## Features and authoring source

Ligatures (`liga`, `dlig`), alternates (`salt`, `ss01`…), contextual substitutions
(`calt`), localized forms (`locl`) and numeral choices (`tnum`…) are useful when
the corresponding drawings exist. Mark-to-base, mark-to-ligature, mark-to-mark
and cursive attachment are positioning rules. These are preserved in the
compiled tables, not reconstructed from anchor names. The profile does not
restrict execution to this illustrative list of feature tags.

There is no universal font-owned on/off default for every OpenType feature.
HarfBuzz applies its script/shaper defaults. A `recommendedValue` is an optional
application preference applied on top; an explicit caller choice takes priority.
Values are unsigned 32-bit integers, supporting indexed alternates as well as
0/1 toggles. Tags absent from the manifest are rejected by the reference API.
Required language-system features remain subject to OpenType shaping semantics;
a zero preference is not a promise that a mandatory rule can be disabled.

`source.format` is `fea` (string) or `glyphs-feature-source-v1` (object with
ordered `prefixes`, `classes`, `features`). Each Glyphs block stores `name`,
`code`, `notes`, `automatic` and `disabled`. Automatic flags and disabled code
are preserved for editing; they are not executable replacements for compilation.
Source content is limited to 1 MiB in its canonical representation.

`source.sha256` hashes UTF-8 JSON of `content`, using sorted keys, no extra
whitespace, literal Unicode and no nonfinite numbers. `compiledSha256` equals
the payload digest. These detect inconsistent edits and bind the two records;
they do not prove that the source compiles to that binary or authenticate its
author. Recompile after editing rules. Unresolved Glyphs automatic features,
classes, prefixes, custom parameters or instance overrides must be resolved in
the source-bound compilation workflow before attaching the resulting font.

## Explicit layout modes

`simple` retains scalar lookup, missing-glyph fallback, advances and explicit
OpenPlotFont kerning. It executes no OpenType rules. `opentype` requires the payload
and dependencies and fails clearly when unavailable; it never silently falls
back to simple mode. The CLI defaults to simple mode for compatibility.

In OpenType mode, shape first, then draw the returned glyph IDs at their
positions. **Do not apply OpenPlotFont pair kerning or advances again.** The
compiled font already supplies advances and positioning. Translate every
geometry and anchor point by that glyph's returned origin, then apply physical
scaling and destination-axis conversion once.

`shape_text` processes one horizontal run with explicit `ltr`/`rtl` direction,
ISO 15924 script (e.g. `Latn`) and language identifier (e.g. `en`, `tr`). These
API values differ from OpenType manifest tags such as `latn` and `TRK `.
Defaults are Latin/English/left-to-right, not automatic script detection.
The caller must segment mixed scripts and bidirectional text, resolve tabs,
choose fallback fonts and arrange runs. The renderer splits lines and applies
the same run settings to each. Vertical text, variation coordinates,
multi-font fallback, bidi segmentation and per-range feature settings are
not implemented. HarfBuzz may perform its normal internal normalization;
the API preserves the original input text and reports clusters into that text.

The run JSON contains selected `name`, `glyphId`, `cluster`, `x`, `y`,
`xAdvance`, `yAdvance`, `xOffset`, `yOffset`, plus total advances. `x`/`y`
already include offsets and are in upward-Y font units. Clusters are zero-based
UTF-8 byte offsets, using HarfBuzz monotone-character clustering; they are not
character indices and need not increase in RTL output. A ligature can consume
several characters, and marks can share a cluster. Do not assume one-to-one
correspondence. Preserve returned glyph order and each glyph's operation order.

Cursive attachment changes placement. It does not authorize connecting paths,
reversing strokes or inserting segments. The reference renderer rejects
`--join` with OpenType mode until a cluster-aware drawing schedule is defined.
Independent paths, fills, holes, closure and curves remain unchanged. Tool
coverage, pen width, compensation and machine settings remain downstream.

For reproducibility save original text, explicit run properties, feature
preferences, resolved glyph run, HarfBuzz version and payload digest. Also pin
the complete OpenPlotFont file digest: changing drawings while retaining the
layout binary changes the result. The run JSON is diagnostic output, not a
new persistent document-format standard. Plot-It's storage policy remains an
open question in its separate project.

## Tools and verification

Install optional dependencies with `python3 -m pip install '.[shaping]'`.
FontTools validates/attaches compiled layout; uharfbuzz executes it. Geometry-only
0.3 and legacy 0.2 workflows use the standard library. Validation of a 0.3 file
containing layout requires FontTools even when selecting simple rendering.

```sh
python3 -m openplotfont shape examples/layout-demo.opf.json fi -o output/run.json
python3 -m openplotfont render examples/layout-demo.opf.json 'fi AA' --layout opentype -o output/layout.svg
python3 -m openplotfont render examples/layout-demo.opf.json A --layout opentype --feature ss01=1 -o output/alternate.svg
python3 -m openplotfont attach-layout output/geometry.opf.json output/matching.otf --fea output/features.fea -o output/shaped.opf.json
```

`attach-layout --glyph-order mapping.json` accepts an explicit array in compiled
GID order when production names differ. It validates before atomic publication
and refuses overwriting existing files. Glyphs export integration is described
in [the script workflow](GLYPHS_EXPORT_SCRIPT.md).

The original MIT fixture checks ligature enable/disable, stylistic and indexed
alternates, contextual matching with ignored marks, Turkish localization,
tabular digits, base/ligature/mark attachment, cursive offsets, kerning exactly
once, RTL order, missing glyphs and UTF-8 clusters. Corruption, unsupported
profiles, incompatible metrics/mappings and dependency failures are tested.
This is bounded feature evidence, not certification of every script or font.

References: [OpenType feature syntax](https://adobe-type-tools.github.io/afdko/OpenTypeFeatureFileSpecification.html),
[GPOS](https://learn.microsoft.com/en-us/typography/opentype/spec/gpos),
[GDEF](https://learn.microsoft.com/en-us/typography/opentype/spec/gdef), and
[HarfBuzz shaping](https://harfbuzz.github.io/shaping-and-shape-plans.html).
