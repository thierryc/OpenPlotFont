# Selected-master export script

Target: Glyphs 4+. [Export OpenPlotFont.py](../scripts/Export%20OpenPlotFont.py) is an implemented workspace script, with its adapter in [glyphs_export.py](../openplotfont/glyphs_export.py). It has been executed on a font copy in Glyphs 4.1 build 4107 through MCP. Native source/export and saved-source reopen comparisons passed; SDK-shaped doubles add portable regression coverage. A [geometry export plugin](GLYPHS_EXPORT_PLUGIN.md) is also implemented; app-loader/menu qualification remains pending. A general OpenPlotFont importer is not included.

The current format is **0.3**. Use plugin 0.1.1 for geometry-only 0.3 exports.
This script produces 0.3 when matching compiled layout bytes are supplied;
its geometry-only default remains legacy 0.2 for the existing qualification and
reproduction workflow. Do not equate a 0.3 version field with compiled shaping.

## Qualification and setup

Keep this repository intact: the script imports its sibling `openplotfont` package. Add the script to the Glyphs Scripts menu using a symlink that resolves to this repository script, or run it in the Glyphs scripting environment with its actual file path. Do not copy it alone. Open a project-owned font, select one master, and set the following font user data (using Glyphs' Python scripting environment):

```python
font.userData["org.openplotfont.font"] = {
    "id": "org.example.my-openplotfont.regular",
    "destination": "/absolute/existing/directory/MyFont.opf.json",
    "styleName": "Regular",
    "missingGlyph": ".notdef",
    "lineGap": 200,
    "metadata": {"license": "Your font's actual license"},
}
```

`id` must be nonempty. `destination` must be an absolute, new `.opf` or `.opf.json` path, with an existing parent directory. The script refuses overwrites. Family name, units per em, metrics, widths, and all Unicode assignments come from the selected master/font. Include an exported fallback glyph. The script reads source geometry and decomposes copied layers; it does not save or mutate the font. User-data setup is an authoring change; save your project source separately.

## Drawing annotations

Without annotations, each path becomes an independent `stroke` in source path order, including closed centerline loops. Closure does not imply filling. For mixed shapes, annotate the glyph:

```python
glyph.userData["org.openplotfont.glyph"] = {
    "operations": [
        {"kind": "stroke", "pathIndex": 0},
        {"kind": "fill", "pathIndices": [1, 2], "fillRule": "evenodd"},
    ]
}
```

Indices refer to the selected master layer's paths. An explicit plan must reference every path exactly once; its array order becomes drawing order. Filled contours must be closed. Group outer boundaries and holes together. The exporter rejects annotated component layers because safe reference remapping has not been implemented. Keep intent consistent across masters or prepare a dedicated static authoring source.

For a connectable open handwriting body, add `connections` inside `org.openplotfont.glyph`:

```python
{"connections": {
    "entry": {"strokeIndex": 0, "endpoint": "start"},
    "exit": {"strokeIndex": 0, "endpoint": "end"},
}}
```

This example assumes a single open stroke. Entry must reference the first operation's start and exit the last operation's end; both must be open strokes. Endpoint user data is optional. No anchor name or proximity implies a join. Layer anchors and JSON-compatible glyph/anchor user data are preserved. Binary or unsupported editor objects produce errors.

## Supported export and limits

- One exact selected master; components decomposed on copies after cycle/missing-reference checks. Hints/corner components and unresolved shapes are rejected.
- Lines, cubic curves, and quadratic curves including implied intermediate points. An explicit on-curve start is required; paths beginning off-curve are rejected rather than silently rotated.
- Fractional coordinates and advances retained; no physical scaling, flattening, stroke expansion, or fill trajectory generation.
- Group kerning resolved into glyph pairs, with stored glyph exceptions preceding class values. Native group kerning and explicit zero exceptions passed qualification.
- All enabled glyphs and the fallback exported. Geometry-only 0.2 export warns about active OpenType features. Supplying compiled layout bytes produces 0.3 and preserves feature source, manifest and compiled rules as described below.
- Semantic validation and UTF-8 encoding complete before publication. A same-directory temporary file is flushed and atomically linked to the new destination; failures remove staging files. Existing files and symlinks are preserved. Filesystems must support hard links; otherwise publication fails clearly. Atomic publication was exercised by the native export script.

## API evidence and acceptance

API choices were checked against the official [Glyphs SDK Python documentation](https://docu.glyphsapp.com/) and SDK revision `0f5422db727b78cb42abfb386f33ae0b382b0c4d`, particularly `GSLayer.copyDecomposedLayer`, `GSNode.type`, `GSGlyph.unicodes`, user data, anchors, and `GSFont.kerningForPair`. Node types use imported SDK constants.

Initial qualification used Glyphs 4.1 build 4107 and native-script support. The additional [Hershey faces](../fonts/README.md) were created, populated, saved, reopened, and exported through MCP in Glyphs 4.1.1 build 4108. MCP beta.10 build 52 advertises `create_document` and `document.create.v1`; it can open a new blank font without an existing document. Save that new source to its project path before running the guarded importer. Native script execution still requires a saved document binding.

The [qualification script](../scripts/Qualify%20Native%20OpenPlotFont.py) checks cubic and implied quadratic curves, fill holes, anchors, user data, endpoints, fractional spacing, group kerning, and zero exceptions on an invisible copy. [Native-exported fixtures](../tests/fixtures/native-qualification.opf.json) and [the report](../tests/fixtures/native-qualification-report.json) preserve the result. Each additional Hershey package passed exact saved-source checks, native reopening, and the actual export entry point on a copy. CI tests the saved artifacts; CI does not run Glyphs. Later Glyphs versions require their own qualification.

## Compare a source reference and export

```sh
python3 -m openplotfont compare fonts/hershey-roman-simplex/HersheyRomanSimplex.opf.json output/native.opf.json
```

The comparison validates both files, then checks identity, metrics, mappings, every operation and coordinate, advances, kerning, anchors, connections, user data, and provenance. Glyph collection order has no drawing semantics and is compared by name; operation, contour, command, and mapping order remain significant. Omitted stroke kinds and empty optional glyph metadata are normalized. Only `glyphsMasterId` and `exportWarnings` diagnostics are excluded. Numeric comparison uses absolute tolerance `1e-9` font units. A mismatch reports its JSON path.

`main(font=None, destination=None, master_id=None)` allows MCP qualification on a copy with an explicit exact master. The menu action still defaults to the current font, selected master, and user-data destination. Qualification writes only new files under `output/`; choose new filenames or move prior local outputs before rerunning. It does not publish files or save the source.

## Optional 0.3 layout export

`main` also accepts keyword arguments `layout_bytes`, `glyph_order` and
`feature_settings`. The adapter binds a **previously compiled matching static
font**, validates its metrics, mappings and manifest, and preserves ordered
Glyphs classes, prefixes and feature blocks (code, notes, automatic/disabled
flags). Install FontTools in the Glyphs Python environment for this path.
The menu action by itself still exports geometry-only 0.2; it does not compile
features, generate automatic code or interpolate an instance.

```python
from pathlib import Path
main(font=font.copy(), destination="/absolute/new/MyFont.opf.json",
     master_id=font.masters[0].id,
     layout_bytes=Path("/absolute/matching-static.otf").read_bytes(),
     feature_settings={"ss01": {"recommendedValue": 0}})
```

Compile/export the same saved source and exact static instance using Glyphs or
the typed Glyphs MCP `font_export` job. Disable production names when possible;
otherwise provide `glyph_order` from the compiler's exact GID mapping. Do not
guess the order from source glyph collection order. Verify source identity and
source-to-export correspondence, including unencoded glyphs. Select an instance
whose resolved geometry/metrics match the master; instance overrides can make
it incompatible even when the family name matches. Automatic classes/features
and instance-level feature replacements must be resolved by that compilation
workflow. A preserved code snapshot alone is not proof of the compiled rules.
The adapter rejects mismatched units, advances, mappings and glyph counts; it
cannot detect every stale feature edit solely from geometric agreement.

Read [the layout profile](OPENPLOTFONT_LAYOUT.md) for execution authority,
dependencies, integrity digests and shaping limitations. Compiled outlines
never replace the open OpenPlotFont paths or prescribe a pen width.

The actual 0.3 script passed native qualification on the [layout demo](../fonts/layout-demo/README.md)
in Glyphs 4.1.1 build 4108, preserving all drawings, anchors, mappings and feature
source. Feature flags use the documented `active` property. The native compiler
omits its Latin `curs` block: active authored tags absent from the payload are
reported in `exportWarnings`. This diagnostic does not prove complete rule
fidelity for tags that remain; review compiled behavior before redistribution.
