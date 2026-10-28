# Glyphs 4 export plugin 0.2.0

The updated plugin offers **Flexible strokes — 0.4** by default and an explicit
**Centerlines only — 0.3** option that removes variation with a warning. Both
preserve ordered editable centerline geometry. The plugin exports a copied,
explicitly selected master and refuses existing output files. It does not compile
OpenType features; the [scripted workflow](GLYPHS_EXPORT_SCRIPT.md) can attach
matching compiled layout. See [Pen profiles](PEN_POINTS.md) for the implemented
models and unsupported native mappings.

## Build and install

Build with `python3 scripts/build_glyphs_plugin.py`, then install the complete
`output/build/OpenPlotFont.glyphsFileFormat` bundle through Glyphs 4. The website
and GitHub release provide the same self-contained bundle as a ZIP. The SDK
loader and its Apache notice are retained; the OpenPlotFont runtime is MIT.

## Verification and limits

The 0.2.0 built principal class, native settings view, mode selector and both
export actions are qualified in Glyphs 4.2 build 4202 using the original
[Pen-profile demo](../fonts/pen-profile-demo/README.md). Its saved/reopened
centerlines, raw channels and native appearance are compared independently.
Portable tests cover version selection, overwrite refusal, source preservation,
master selection, profile errors and active-feature diagnostics.

This release's class is `OpenPlotFontExporter020` and its bundled runtime uses
`_openplotfont_glyphs4_v020`, preventing an older loaded exporter package from
being mistaken for the tested revision. Installation and cold startup/visible
Export-menu loading of this version remain unqualified. Native class/action
execution is not a claim of installation or startup testing. A restart is normally
needed after installation; preserve unrelated work before restarting Glyphs.

Earlier 0.1.x plugin/export evidence is historical. It qualified geometry rather
than flexible-stroke preservation. The new download must be tested in the target
Glyphs build before depending on behavior outside this release's fixtures.
