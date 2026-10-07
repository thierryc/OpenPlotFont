# OpenPlotFont layout demo

This original MIT conformance font is an authoring/test fixture, not a finished
typeface. [The editable Glyphs 4 source](OpenPlotFontLayoutDemo.glyphspackage/fontinfo.plist)
contains 14 glyphs and 10 manual feature blocks. It was created, populated,
verified and saved through Glyphs MCP in Glyphs 4.1.1 build 4108.

[The portable example](../../examples/layout-demo.opf.json) uses a static
TTF compiled with FontTools from [explicit FEA](../../tests/fixtures/layout-demo.fea).
It verifies ligatures, alternates, contextual substitutions, Turkish localized
forms, numeral widths, mark/base/ligature/mark attachment and cursive placement.
Its empty binary outlines are intentional; render the OpenPlotFont geometry.

The native workflow exports the exact Regular instance using Glyphs MCP's
typed static `font_export`, with production names, autohinting and overlap
removal disabled, then supplies those bytes to the actual OpenPlotFont export
script on a source copy. Native and portable compilers can assign different
glyph IDs; each payload carries its own explicit mapping.

[The retained native JSON](../../examples/layout-demo-native.opf.json) and
[verification report](../../tests/fixtures/native-layout-report.json) record
this completed workflow.

Glyphs adds U+00A0 to `space`, so the authoring source and portable fixture
declare that mapping explicitly. Its native compiler omits this fixture's
Latin `curs` feature. The native export preserves its authored source and
reports the omitted tag in `exportWarnings`; requesting `curs` from that
payload fails clearly. The portable fixture includes and tests the rule.
No general Glyphs cursive-export compatibility is claimed.

The source has manual `kern` code, not a native Glyphs pair dictionary. Its
simple-mode export therefore has no pair adjustment; OpenType mode applies
the compiled adjustment. The portable fixture also has the explicit pair,
testing that OpenType rendering never applies it a second time.

Rebuilding the portable fixture with `python3 scripts/build_layout_fixture.py`
does not change the native source. `scripts/Prepare Layout Demo.py` populates
only an empty, saved font at this exact project path and never overwrites an
existing font. Native artifacts are qualified locally; CI inspects retained
files without launching Glyphs.
