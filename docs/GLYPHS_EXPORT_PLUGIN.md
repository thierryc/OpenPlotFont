# PlotFont export plugin for Glyphs 4

Version 0.1.1 implements a selected-master, geometry-only draft 0.3 exporter.
The plugin uses the same adapter and atomic no-overwrite writer as the
[export script](GLYPHS_EXPORT_SCRIPT.md). It provides a master chooser in the
export settings and a native save dialog. It does not require a destination or
font identifier to be entered in user data first.

Every export declares `version: "0.3"`; there is no 0.2 output option. Draft
0.3 permits geometry-only fonts with no `layout` object. This changes the
plugin's output version from 0.1.0 without changing drawings or inventing
compiled features. Consumers that accept only 0.2 must update to accept 0.3.

## Build and install

From this repository, using Python 3.10 or later:

```sh
python3 scripts/build_glyphs_plugin.py
```

The self-contained bundle is written to `output/build/PlotFont.glyphsFileFormat`,
separate from the current font exports.
Existing builds are preserved; choose a new destination for another revision:

```sh
python3 scripts/build_glyphs_plugin.py --destination output/build/revision-2/PlotFont.glyphsFileFormat
```

The bundle includes the current exporter, validator and writer in a private
Python package, the project license, and the official SDK loader and attribution.
No repository checkout is needed after installation. The source bundle under
`plugins/` is a build input; install the complete generated bundle from `output/`.

Drag the built bundle onto **Glyphs 4** and accept its installation prompt.
Restart Glyphs to load the plugin, after protecting any unsaved work. The
[official handbook](https://handbook.glyphsapp.com/plugins/) documents plugin
installation and loading at launch.

## Export

1. Open your `.glyphs` or `.glyphspackage` authoring source in Glyphs 4.
2. Choose **File → Export**, then **PlotFont**.
3. Choose one exact master from the popup and proceed to the save dialog.
4. Choose a new absolute filename ending in `.plotfont.json`.

All enabled glyphs and the fallback are exported. Existing files and symlinks
are preserved, even if the native save dialog offers replacement. An Export All
destination directory is supported; programmatic export uses the bound popup
selection or the supplied font's selected master. An unbound multi-master copy
requires binding and an explicit popup choice.

The plugin exports an invisible font copy, retains font units, open paths,
explicit closure, curves, start points and stroke order, and does not save the
source. Unsupported geometry or invalid metadata produces an export error.
Stroke/fill annotations, anchors, connections, kerning and user data follow the
[adapter's documented rules](GLYPHS_EXPORT_SCRIPT.md#supported-export-and-limits).
Keep a valid exported `.notdef`, or configure another `missingGlyph`.

Existing `org.plotfont.font` settings are honored, including `id`, `styleName`,
`missingGlyph`, `lineGap` and provenance metadata. Its `destination` is ignored
in favor of the save dialog. When `id` is absent, a deterministic UUID-based
identifier is derived from family and master names on the copy only. Renaming
either changes this default identifier; set an explicit `id` for a stable
catalog identity across renames. Family/master names are not a global uniqueness
guarantee. Default line gap is zero; no license or provenance is invented.

## Verification and limits

The SDK scaffold validator checks the bundle suffix, Python syntax, plist,
principal class, loader fingerprint and attribution. Eight plugin regression
tests cover built-runtime correspondence, master choice/rebinding, source
preservation, automatic identifiers, cancellation, invalid metadata, existing
files/symlinks, directory export and feature warnings.

The 0.1.0 plugin class and settings view were instantiated through Glyphs MCP
in Glyphs **4.1.1 build 4108**. Its actual export action produced all 97 Script
Simplex glyphs; the result matched the reference's geometry, metrics, mappings,
metadata and kerning. Native existing-file protection and export without font
settings passed; original font user data remained unchanged. Invisible font
copies are supported without accessing a nonexistent document.

Version 0.1.0 was installed through Glyphs 4's native installer using Copy.
All 13 installed payload files matched the native-tested build. This is direct
native class/action qualification plus verified installation. Loading at
application startup, the visible File → Export tab, save-dialog interaction,
and native multi-master popup behavior remain unverified until restart.
Current build and qualification evidence live under `output/build/` and
`output/qualification/`; superseded generated revisions are removed during cleanup.
MCP script execution marks its bound document dirty; no source Save was performed.

The 0.1.1 build passes the SDK scaffold validator and plugin regression tests,
including 0.3 output with and without active feature warnings. The native
installer replaced 0.1.0 with 0.1.1; all 13 installed files match the new build.
Its changed
revision still requires native startup/menu qualification after restart.

This plugin exports draft **0.3 only** and reports active OpenType features as
warnings. It does not compile or attach optional layout, interpolate instances,
generate a companion OTF, import PlotFont, flatten/expand strokes, or produce
device/fill toolpaths. Use the script's explicit matching compiled-font path
for [optional 0.3 layout](GLYPHS_EXPORT_SCRIPT.md#optional-03-layout-export).
Later Glyphs versions require native qualification.

Implementation follows the official SDK File Format template and
`FileFormatPlugin.setFont_`, `export(font)` and `export(font, destination)`
callbacks at SDK revision `0f5422db727b78cb42abfb386f33ae0b382b0c4d`.
The loader and sample resources retain their Apache attribution; original
PlotFont code uses the repository's existing MIT license.
