# Converted stroke-font library

Built and reviewed 2026-10-01. **87 fonts**: 32 JHF Hershey files, 12 Hershey-related SVGs, 29 EMS SVGs, Relief Regular and Ornament, NormStroke, three Custom fonts, three Cutlings fonts, one DearPlotter design, and four LibreCAD LFF fonts. These are 87 converted source files; some Hershey aliases and SVG adaptations overlap in design.

Every row has an OpenPlotFont 0.3 export and an editable format-4 Glyphs package. All packages were loaded, saved and reopened through the live Glyphs MCP server in Glyphs 4.1.1 (4108), then compared against their source conversions. Earlier CLI qualification is retained separately; the links below now point to the MCP-created copies. Coordinates in native saved packages are rounded to 0.001 font units; comparisons allow 0.000501 font units per numeric value. The primary OpenPlotFont JSON retains the higher precision source conversion. Local qualification report: `output/font-library/mcp/qualification.json`.

[Download individual fonts from the website](https://thierryc.github.io/OpenPlotFont/#fonts). The complete local archive is `output/font-library/OpenPlotFont-stroke-library.zip`. Each individual ZIP includes original source, full notices, attribution, Glyphs package, OpenPlotFont JSON, native JSON export, specimen and glyph atlas. Generated files are local, ignored by Git and reproducible using the scripts below.

## Drawing and machine interoperability

These are reviewed stroke sources, with independent pen-down trajectories, explicit closure, source path order/start points/direction, spaces, advances and supported kerning retained. Cubic and quadratic curves remain curves. SVG/LFF arcs become tangent-matched cubic segments of at most 5°; conservative error allowance is 1e-7 × maximum radius in source units. No outline skeletonization or stroke-width expansion is performed.

OpenPlotFont geometry is in font units with Y up. The specimens demonstrate physical sizing at an 8 mm cap height and convert to SVG page coordinates. CNC/plotter consumers must preserve each trajectory and lift the pen/tool between strokes, size geometry physically, and apply device motion settings outside the font. A closed stroke remains a trajectory, not a filled area. This repository supplies portable geometry and SVG review output; it does not generate G-code/HPGL or operate hardware. Machine compatibility has not been tested on hardware. See [consumer responsibilities](USING_OPENPLOTFONT.md).

**Coverage limits:** 14 non-Latin/symbol JHF sources use temporary U+E000 + source-row mappings, explicitly recorded in each font. Their geometry is usable through the glyph atlas/private-use mapping; standard Greek, Cyrillic, Japanese and symbol text mapping is not qualified. Original JHF records beyond printable ASCII are retained. SVG ligatures and unencoded alternates retain drawings and source metadata but have no automatic substitutions. Scripts preserve pen lifts and have no automatic joining. JHF x-height is estimated at half cap height, and non-Latin JHF baseline/cap metrics are estimates. LFF line metrics are explicit conversion estimates; origins and LibreCAD xMax + LetterSpacing advances are retained. Font bounds can exceed nominal cap/ascender metrics.

## Licensing and attribution

Conversions keep the upstream font licenses. Full available copyright/license notices are embedded in OpenPlotFont metadata and Glyphs font user data, copied beside the fonts, and embedded in specimen/atlas SVG metadata. Original sources retain their notices. Distribute the whole ZIP/folder; the project MIT license does not replace these font terms. PF prefixes distinguish converted SVG/CAD family names from their source font names.

- **Hershey:** Dr. A. V. Hershey; JHF representation by James Hurt, Cognition, Inc.; SVG adaptations retain their source credits. Complete acknowledgment/use restriction is included, including the prohibition on recreating the original NTIS representation.
- **OFL:** retain author/copyright notices and the full OFL; modified fonts remain OFL and honor reserved font names. Font software cannot be sold by itself. Each ZIP includes available ancestor notices. EMS Elfin retains both the stroke derivative’s OFL declaration and its Mountains of Christmas ancestor’s Apache 2.0 notice; this is not a claim that the ancestor was OFL.
- **CC0:** NormStroke retains octycs’ CC0 declaration and ISO3098/Wikimedia ancestry credits.
- **GPL v2 or later:** the two LibreCAD ISO3098 fonts include GPL text and the original LFF source. Keep source available with redistribution and retain author/license headers.
- **DearPlotter:** the font is OFL; Licia He’s generator and Golan Levin’s adaptation have CC BY-SA 4.0 credits in the retained source metadata. No generator code is included in the font bundle.

The supplied EMS and Custom OFL templates have unfilled copyright fields. Source metadata supplies the declared authors and ancestry; these are retained with available ancestor notices. The Custom font template also has unfilled copyright fields. Its explicit upstream font license declaration, Shriinivas’ attribution, Pinyon Script/Square Grotesk ancestry and complete upstream README are retained rather than inventing copyright ownership.

## Individual fonts

| Font / glyph count | License | Original repository / author links | Files |
| --- | --- | --- | --- |
| Hershey Astrology (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-astrology.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-astrology.svg) |
| Hershey Cursive (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cursive.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cursive.svg) |
| Hershey Cyrilc 1 (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cyrilc-1.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cyrilc-1.svg) |
| Hershey Cyrillic (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cyrillic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cyrillic.svg) |
| Hershey Futural (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-futural.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-futural.svg) |
| Hershey Futuram (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-futuram.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-futuram.svg) |
| Hershey Gothgbt (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothgbt.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothgbt.svg) |
| Hershey Gothgrt (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothgrt.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothgrt.svg) |
| Hershey Gothiceng (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothiceng.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothiceng.svg) |
| Hershey Gothicger (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothicger.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothicger.svg) |
| Hershey Gothicita (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothicita.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothicita.svg) |
| Hershey Gothitt (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothitt.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothitt.svg) |
| Hershey Greek (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greek.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greek.svg) |
| Hershey Greekc (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greekc.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greekc.svg) |
| Hershey Greeks (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greeks.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greeks.svg) |
| Hershey Japanese (195) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-japanese.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-japanese.svg) |
| Hershey Markers (99) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-markers.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-markers.svg) |
| Hershey Mathlow (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-mathlow.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-mathlow.svg) |
| Hershey Mathupp (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-mathupp.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-mathupp.svg) |
| Hershey Meteorology (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-meteorology.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-meteorology.svg) |
| Hershey Music (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-music.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-music.svg) |
| Hershey Roman Duplex (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-duplex.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-duplex.svg) |
| Hershey Roman Simplex (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-simplex.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-simplex.svg) |
| Hershey Roman Triplex (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-triplex.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-triplex.svg) |
| Hershey Script Complex (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-script-complex.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-script-complex.svg) |
| Hershey Script Simplex (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-script-simplex.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-script-simplex.svg) |
| Hershey Symbolic (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-symbolic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-symbolic.svg) |
| Hershey Timesg (98) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-timesg.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-timesg.svg) |
| Hershey Roman Italic (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-italic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-italic.svg) |
| Hershey Roman Bold Italic (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-bold-italic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-bold-italic.svg) |
| Hershey Roman Complex (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-complex.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-complex.svg) |
| Hershey Roman Bold (97) | Hershey permissive terms; not MIT | [repository](https://github.com/kamalmostafa/hershey-fonts) · [author/source 1](https://github.com/kamalmostafa/hershey-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-bold.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-bold.svg) |
| PF EMS Allure (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.typesetit.com) · [author/source 2](https://fonts.google.com/specimen/Allura) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-allure.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-allure.svg) |
| PF EMS Bird (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.typesetit.com) · [author/source 2](https://fonts.google.com/specimen/Bilbo) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-bird.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-bird.svg) |
| PF EMS Bird Swash Caps (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.typesetit.com) · [author/source 2](https://fonts.google.com/specimen/Bilbo+Swash+Caps) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-bird-swash-caps.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-bird-swash-caps.svg) |
| PF EMS Brush (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.typesetit.com) · [author/source 2](https://fonts.google.com/specimen/Alex+Brush) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-brush.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-brush.svg) |
| PF EMS Capitol (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.astigmatic.com) · [author/source 2](https://fonts.google.com/specimen/Sacramento) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-capitol.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-capitol.svg) |
| PF EMS Casual Hand (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.kimberlygeswein.com/) · [author/source 2](https://fonts.google.com/specimen/Covered+By+Your+Grace) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-casual-hand.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-casual-hand.svg) |
| PF EMS Decorous Script (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://fonts.google.com/specimen/Petit+Formal+Script) · [author/source 2](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-decorous-script.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-decorous-script.svg) |
| PF EMS Delight (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://fonts.google.com/specimen/Delius) · [author/source 2](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-delight.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-delight.svg) |
| PF EMS Delight Swash Caps (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://fonts.google.com/specimen/Delius+Swash+Caps) · [author/source 2](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-delight-swash-caps.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-delight-swash-caps.svg) |
| PF EMS Elfin (218) | SIL OFL 1.1; Apache 2.0 ancestor notice retained | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.tartworkshop.com) · [author/source 2](https://fonts.google.com/specimen/Mountains+of+Christmas) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-elfin.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-elfin.svg) |
| PF EMS Felix (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://twitter.com/fontstage) · [author/source 2](https://fonts.google.com/specimen/Felipa) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-felix.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-felix.svg) |
| PF EMS Herculean (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://www.myfonts.com/foundry/Denis_Masharov/) · [author/source 2](https://fonts.google.com/specimen/Poiret+One) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-herculean.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-herculean.svg) |
| PF EMS Invite (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://tosche.net/about) · [author/source 2](https://fonts.google.com/specimen/Tangerine) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-invite.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-invite.svg) |
| PF EMS League (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://www.theleagueofmoveabletype.com) · [author/source 2](https://fonts.google.com/specimen/League+Script) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-league.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-league.svg) |
| PF EMS Little Princess (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.tartworkshop.com) · [author/source 2](https://fonts.google.com/specimen/Princess+Sofia) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-little-princess.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-little-princess.svg) |
| PF EMS Misty Night (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.glukfonts.pl) · [author/source 2](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-misty-night.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-misty-night.svg) |
| PF EMS Neato (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://www.myfonts.com/foundry/Gaslight/) · [author/source 2](https://fonts.google.com/specimen/Bad+Script) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-neato.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-neato.svg) |
| PF EMS Nixish (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://jovanny.ru) · [author/source 2](https://fonts.google.com/specimen/Nixie+One) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-nixish.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-nixish.svg) |
| PF EMS Nixish Italic (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://jovanny.ru) · [author/source 2](https://fonts.google.com/specimen/Nixie+One) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-nixish-italic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-nixish-italic.svg) |
| PF EMS Osmotron (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://www.theleagueofmoveabletype.com) · [author/source 2](https://fonts.google.com/specimen/Orbitron) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-osmotron.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-osmotron.svg) |
| PF EMS Pancakes (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.typeco.com) · [author/source 2](https://fonts.google.com/specimen/Short+Stack) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-pancakes.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-pancakes.svg) |
| PF EMS Pepita (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://pecita.eu/police-en.php) · [author/source 2](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-pepita.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-pepita.svg) |
| PF EMS Qwandry (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.typesetit.com) · [author/source 2](https://fonts.google.com/specimen/Qwigley) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-qwandry.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-qwandry.svg) |
| PF EMS Readability (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.adobe.com) · [author/source 2](https://fonts.google.com/specimen/Source+Sans+Pro) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-readability.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-readability.svg) |
| PF EMS Readability Italic (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.adobe.com) · [author/source 2](https://fonts.google.com/specimen/Source+Sans+Pro) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-readability-italic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-readability-italic.svg) |
| PF EMS Society (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.sudtipos.com) · [author/source 2](https://fonts.google.com/specimen/Mrs+Saint+Delafield) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-society.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-society.svg) |
| PF EMS Swiss (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.typesetit.com) · [author/source 2](https://fonts.google.com/specimen/Italianno) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-swiss.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-swiss.svg) |
| PF EMS Tech (218) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](http://www.kimberlygeswein.com/) · [author/source 2](https://fonts.google.com/specimen/Architects+Daughter) · [author/source 3](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-tech.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-tech.svg) |
| PF Hershey Gothic English (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-english.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-english.svg) |
| PF Hershey Gothic German (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-german.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-german.svg) |
| PF Hershey Gothic Italian (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-italian.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-italian.svg) |
| PF Hershey Sans 1-stroke (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-sans-1-stroke.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-sans-1-stroke.svg) |
| PF Hershey Sans medium (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-sans-medium.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-sans-medium.svg) |
| PF Hershey Script 1-stroke (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-script-1-stroke.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-script-1-stroke.svg) |
| PF Hershey Script medium (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-script-medium.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-script-medium.svg) |
| PF Hershey Serif bold (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-bold.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-bold.svg) |
| PF Hershey Serif bold italic (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-bold-italic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-bold-italic.svg) |
| PF Hershey Serif medium (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-medium.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-medium.svg) |
| PF Hershey Serif medium italic (218) | Hershey permissive terms; not MIT | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-medium-italic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-medium-italic.svg) |
| PF Twin Sans (264) | SIL OFL 1.1; Hershey ancestor notice retained | [repository](https://gitlab.com/oskay/svg-fonts) · [author/source 1](https://keithp.com/) · [author/source 2](https://gitlab.com/oskay/svg-fonts) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-twin-sans.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-twin-sans.svg) |
| PF Relief SingleLine Ornament (171) | SIL OFL 1.1 | [repository](https://github.com/isdat-type/Relief-SingleLine) · [author/source 1](https://github.com/isdat-type/Relief-SingleLine) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-relief-singleline-ornament.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-relief-singleline-ornament.svg) |
| PF Relief SingleLine SVG (568) | SIL OFL 1.1 | [repository](https://github.com/isdat-type/Relief-SingleLine) · [author/source 1](https://github.com/isdat-type/Relief-SingleLine) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-relief-singleline-svg.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-relief-singleline-svg.svg) |
| PF Norm Stroke (326) | CC0 1.0 | [repository](https://github.com/octycs/norm-stroke) · [author/source 1](https://github.com/octycs/norm-stroke) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-norm-stroke.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-norm-stroke.svg) |
| PF Custom-Script (100) | SIL OFL 1.1 | [repository](https://github.com/Shriinivas/inkscapestrokefont) · [author/source 1](https://github.com/Shriinivas/inkscapestrokefont) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-script.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-script.svg) |
| PF Custom-Square Italic (100) | SIL OFL 1.1 | [repository](https://github.com/Shriinivas/inkscapestrokefont) · [author/source 1](https://github.com/Shriinivas/inkscapestrokefont) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-square-italic.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-square-italic.svg) |
| PF Custom-Square Normal (100) | SIL OFL 1.1 | [repository](https://github.com/Shriinivas/inkscapestrokefont) · [author/source 1](https://github.com/Shriinivas/inkscapestrokefont) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-square-normal.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-square-normal.svg) |
| PF CutlingsDualis (98) | SIL OFL 1.1 | [repository](https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/) · [author/source 1](http://cutlings.wasbo.net/) · [author/source 2](https://cutlings.datafil.no/) · [author/source 3](https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingsdualis.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingsdualis.svg) |
| PF CutlingsPluralis (98) | SIL OFL 1.1 | [repository](https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/) · [author/source 1](http://cutlings.wasbo.net/) · [author/source 2](https://cutlings.datafil.no/) · [author/source 3](https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingspluralis.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingspluralis.svg) |
| PF CutlingsSingularis (98) | SIL OFL 1.1 | [repository](https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/) · [author/source 1](http://cutlings.wasbo.net/) · [author/source 2](https://cutlings.datafil.no/) · [author/source 3](https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingssingularis.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingssingularis.svg) |
| PF DearPlotter (97) | SIL OFL 1.1 (font); CC BY-SA 4.0 generator/adaptation credits retained | [repository](https://www.eyesofpanda.com/project/dearplotter_font/) · [author/source 1](https://www.eyesofpanda.com/) · [author/source 2](https://www.eyesofpanda.com/project/dearplotter_font/) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-dearplotter.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-dearplotter.svg) |
| PF CAD iso3098 (321) | GPL v2 or later | [repository](https://github.com/LibreCAD/LibreCAD) · [author/source 1](https://github.com/LibreCAD/LibreCAD) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-iso3098.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-iso3098.svg) |
| PF CAD iso3098_i (321) | GPL v2 or later | [repository](https://github.com/LibreCAD/LibreCAD) · [author/source 1](https://github.com/LibreCAD/LibreCAD) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-iso3098-i.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-iso3098-i.svg) |
| PF CAD lc_opengost-ar (678) | SIL OFL 1.1 | [repository](https://github.com/LibreCAD/LibreCAD) · [author/source 1](https://github.com/LibreCAD/LibreCAD) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-lc-opengost-ar.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-lc-opengost-ar.svg) |
| PF CAD lc_opengost-br (678) | SIL OFL 1.1 | [repository](https://github.com/LibreCAD/LibreCAD) · [author/source 1](https://github.com/LibreCAD/LibreCAD) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-lc-opengost-br.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-lc-opengost-br.svg) |
| PF EMS SpaceRocks (97) | SIL OFL 1.1 | [repository](https://gitlab.com/oskay/svg-fonts) · [SVG conversion author](https://www.evilmadscientist.com/) | [ZIP (Glyphs and OpenPlotFont)](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-spacerocks.zip) · [preview](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-spacerocks.svg) |

## Deferred or excluded

- `https://github.com/cmiscm/leonsans` — Reviewed JS renderer uses filled circles for dots, alongside strokes. A pure-stroke conversion would change drawing intent; mixed-fill extraction is not implemented.
- `output/font-library/sources/lff/kst32b.lff` — Additional KST32B license terms need verification before redistribution.

LingDong’s outline-derived skeleton collection, fonts with unknown rights, ROM/SHX extracts and the unreviewed remainder of the LibreCAD library remain outside this batch. Ordinary Google Fonts outline files are not converted into centerlines: the imported EMS files are existing stroke derivatives from Oskay’s repository.

## Reproduce

Install the optional build dependencies with `python3 -m pip install ".[library]"`. Then run:

```sh
python3 scripts/fetch_font_library.py
python3 scripts/build_font_library.py
# Perform native qualification and packaging through Glyphs MCP as described below.
```

The digest lock pins every downloaded source and required notice. Existing changed source files fail SHA-256 validation. Builds refuse an existing destination; use a new build directory or preserve/remove your previous generated output first. Qualification uses the standard `fonts/` catalog; a custom build destination needs its catalog copied into that location before qualification. Use the Glyphs MCP server for native loading, saving, reopening, export and packaging. Submit [qualify_font_library_mcp.py](../scripts/qualify_font_library_mcp.py) through `start_edit_workflow` with kind=`python_script`, entrypoint=`script`, targets=`[]`, and params containing `root` (absolute repository path) and `sourceForRecord` (the exact script source). Bind a separate saved verification document, then execute its offered Run action. The script refuses an existing MCP report and promotes catalog/bundle links only after all 87 comparisons pass. Preserve the previous generated output before rebuilding. Historical CLI verification remains recorded separately. No font binaries are installed and no original source is modified.

## Per-font source credits

### Hershey Astrology

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-astrology.zip)

### Hershey Cursive

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cursive.zip)

### Hershey Cyrilc 1

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cyrilc-1.zip)

### Hershey Cyrillic

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-cyrillic.zip)

### Hershey Futural

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-futural.zip)

### Hershey Futuram

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-futuram.zip)

### Hershey Gothgbt

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothgbt.zip)

### Hershey Gothgrt

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothgrt.zip)

### Hershey Gothiceng

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothiceng.zip)

### Hershey Gothicger

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothicger.zip)

### Hershey Gothicita

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothicita.zip)

### Hershey Gothitt

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-gothitt.zip)

### Hershey Greek

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greek.zip)

### Hershey Greekc

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greekc.zip)

### Hershey Greeks

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-greeks.zip)

### Hershey Japanese

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-japanese.zip)

### Hershey Markers

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-markers.zip)

### Hershey Mathlow

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-mathlow.zip)

### Hershey Mathupp

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-mathupp.zip)

### Hershey Meteorology

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-meteorology.zip)

### Hershey Music

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-music.zip)

### Hershey Roman Duplex

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-duplex.zip)

### Hershey Roman Simplex

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-simplex.zip)

### Hershey Roman Triplex

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-triplex.zip)

### Hershey Script Complex

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-script-complex.zip)

### Hershey Script Simplex

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-script-simplex.zip)

### Hershey Symbolic

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-symbolic.zip)

### Hershey Timesg

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-timesg.zip)

### Hershey Roman Italic

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-italic.zip)

### Hershey Roman Bold Italic

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-bold-italic.zip)

### Hershey Roman Complex

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-complex.zip)

### Hershey Roman Bold

Source credits retained verbatim:

```text
Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/hershey-roman-bold.zip)

### PF EMS Allure

Source credits retained verbatim:

```text
Font name:               EMS Allure
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Allura
Designer:                Rob Leuschke, TypeSETit
Link:                    http://www.typesetit.com
Google font page:        https://fonts.google.com/specimen/Allura
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-allure.zip)

### PF EMS Bird

Source credits retained verbatim:

```text
Font name:               EMS Bird
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Bilbo
Designer:                Rob Leuschke, TypeSETit
Link:                    http://www.typesetit.com
Google font page:        https://fonts.google.com/specimen/Bilbo
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-bird.zip)

### PF EMS Bird Swash Caps

Source credits retained verbatim:

```text
Font name:               EMS Bird Swash Caps
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Bilbo Swash Caps
Designer:                Rob Leuschke, TypeSETit
Link:                    http://www.typesetit.com
Google font page:        https://fonts.google.com/specimen/Bilbo+Swash+Caps
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-bird-swash-caps.zip)

### PF EMS Brush

Source credits retained verbatim:

```text
Font name:               EMS Brush
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Alex Brush
Designer:                Rob Leuschke, TypeSETit
Link:                    http://www.typesetit.com
Google font page:        https://fonts.google.com/specimen/Alex+Brush
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-brush.zip)

### PF EMS Capitol

Source credits retained verbatim:

```text
Font name:               EMS Capitol
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Sacramento
Designer:                Brian J. Bonislawsky, Astigmatic One Eye Typographic Institute
Link:                    http://www.astigmatic.com
Google font page:        https://fonts.google.com/specimen/Sacramento
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-capitol.zip)

### PF EMS Casual Hand

Source credits retained verbatim:

```text
Font name:               EMS Casual Hand
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Covered By Your Grace
Designer:                Kimberly Geswein, Kimberly Geswein Fonts
Link:                    http://www.kimberlygeswein.com/
Google font page:        https://fonts.google.com/specimen/Covered+By+Your+Grace
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-casual-hand.zip)

### PF EMS Decorous Script

Source credits retained verbatim:

```text
Font name:               EMS Decorous Script
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Petit Formal Script
Designer:                Impallari Type
Google font page:        https://fonts.google.com/specimen/Petit+Formal+Script
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-decorous-script.zip)

### PF EMS Delight

Source credits retained verbatim:

```text
Font name:               EMS Delight
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Delius
Designer:                Natalia Raices
Google font page:        https://fonts.google.com/specimen/Delius
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-delight.zip)

### PF EMS Delight Swash Caps

Source credits retained verbatim:

```text
Font name:               EMS Delight Swash Caps
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Delius Swash Caps
Designer:                Natalia Raices
Google font page:        https://fonts.google.com/specimen/Delius+Swash+Caps
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-delight-swash-caps.zip)

### PF EMS Elfin

Source credits retained verbatim:

```text
Font name:               EMS Elfin
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Mountains of Christmas
Designer:                Crystal Kluge, Tart Workshop
Link:                    http://www.tartworkshop.com
Google font page:        https://fonts.google.com/specimen/Mountains+of+Christmas
Note:                    SIL OFL per metadata; Google cites Apache License, version 2.0
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-elfin.zip)

### PF EMS Felix

Source credits retained verbatim:

```text
Font name:               EMS Felix
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Felipa
Designer:                Fontstage
Link:                    https://twitter.com/fontstage
Google font page:        https://fonts.google.com/specimen/Felipa
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-felix.zip)

### PF EMS Herculean

Source credits retained verbatim:

```text
Font name:               EMS Herculean
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Poiret One
Designer:                Denis Masharov
Link:                    https://www.myfonts.com/foundry/Denis_Masharov/
Google font page:        https://fonts.google.com/specimen/Poiret+One
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-herculean.zip)

### PF EMS Invite

Source credits retained verbatim:

```text
Font name:               EMS Invite
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Tangerine
Designer:                Toshi Omagari
Link:                    http://tosche.net/about
Google font page:        https://fonts.google.com/specimen/Tangerine
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-invite.zip)

### PF EMS League

Source credits retained verbatim:

```text
Font name:               EMS League
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         League Script
Designer:                Haley Fiege, the League of Moveable Type
Link:                    https://www.theleagueofmoveabletype.com
Google font page:        https://fonts.google.com/specimen/League+Script
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-league.zip)

### PF EMS Little Princess

Source credits retained verbatim:

```text
Font name:               EMS Little Princess
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Princess Sofia
Designer:                Crystal Kluge, Tart Workshop
Link:                    http://www.tartworkshop.com
Google font page:        https://fonts.google.com/specimen/Princess+Sofia
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-little-princess.zip)

### PF EMS Misty Night

Source credits retained verbatim:

```text
Font name:               EMS Misty Night
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Foglihten No03
Designer:                Grzegorz L, GLUK fonts
Link:                    http://www.glukfonts.pl
FontSquirrel page:       https://www.fontsquirrel.com/fonts/foglihten
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-misty-night.zip)

### PF EMS Neato

Source credits retained verbatim:

```text
Font name:               EMS Neato
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Bad Script
Designer:                Roman Shchyukin, Gaslight
Link:                    https://www.myfonts.com/foundry/Gaslight/
Google font page:        https://fonts.google.com/specimen/Bad+Script
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-neato.zip)

### PF EMS Nixish

Source credits retained verbatim:

```text
Font name:               EMS Nixish
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Nixie One
Designer:                Jovanny Lemonad
Link:                    http://jovanny.ru
Google font page:        https://fonts.google.com/specimen/Nixie+One
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-nixish.zip)

### PF EMS Nixish Italic

Source credits retained verbatim:

```text
Font name:               EMS Nixish Italic
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Nixie One
Designer:                Jovanny Lemonad
Link:                    http://jovanny.ru
Google font page:        https://fonts.google.com/specimen/Nixie+One
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-nixish-italic.zip)

### PF EMS Osmotron

Source credits retained verbatim:

```text
Font name:               EMS Osmotron
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Orbitron (Regular)
Designer:                Matt McInerney, the League of Moveable Type
Link:                    https://www.theleagueofmoveabletype.com
Google font page:        https://fonts.google.com/specimen/Orbitron
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-osmotron.zip)

### PF EMS Pancakes

Source credits retained verbatim:

```text
Font name:               EMS Pancakes
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Short Stack
Designer:                James Grieshaber, Typeco
Link:                    http://www.typeco.com
Google font page:        https://fonts.google.com/specimen/Short+Stack
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-pancakes.zip)

### PF EMS Pepita

Source credits retained verbatim:

```text
Font name:               EMS Pepita
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Pecita
Designer:                Philippe Cochy
Link:                    http://pecita.eu/police-en.php
FontSquirrel page:       https://www.fontsquirrel.com/fonts/Pecita
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-pepita.zip)

### PF EMS Qwandry

Source credits retained verbatim:

```text
Font name:               EMS Qwandry
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Qwigley
Designer:                Rob Leuschke, TypeSETit
Link:                    http://www.typesetit.com
Google font page:        https://fonts.google.com/specimen/Qwigley
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-qwandry.zip)

### PF EMS Readability

Source credits retained verbatim:

```text
Font name:               EMS Readability
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Source Sans Pro-Light
Designer:                Paul D. Hunt, Adobe
Link:                    http://www.adobe.com
Google font page:        https://fonts.google.com/specimen/Source+Sans+Pro
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-readability.zip)

### PF EMS Readability Italic

Source credits retained verbatim:

```text
Font name:               EMS Readability Italic
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Source Sans Pro-Light
Designer:                Paul D. Hunt, Adobe
Link:                    http://www.adobe.com
Google font page:        https://fonts.google.com/specimen/Source+Sans+Pro
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-readability-italic.zip)

### PF EMS Society

Source credits retained verbatim:

```text
Font name:               EMS Society
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Mrs Saint Delafield
Designer:                Alejandro Paul, Sudtipos
Link:                    http://www.sudtipos.com
Google font page:        https://fonts.google.com/specimen/Mrs+Saint+Delafield
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-society.zip)

### PF EMS Swiss

Source credits retained verbatim:

```text
Font name:               EMS Swiss
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Italianno
Designer:                Rob Leuschke, TypeSETit
Link:                    http://www.typesetit.com
Google font page:        https://fonts.google.com/specimen/Italianno
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-swiss.zip)

### PF EMS Tech

Source credits retained verbatim:

```text
Font name:               EMS Tech
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Sheldon B. Michaels
SVG font conversion by:  Windell H. Oskay
A derivative of:         Architects Daughter
Designer:                Kimberly Geswein, Kimberly Geswein Fonts
Link:                    http://www.kimberlygeswein.com/
Google font page:        https://fonts.google.com/specimen/Architects+Daughter
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-tech.zip)

### PF Hershey Gothic English

Source credits retained verbatim:

```text
Font name: Hershey Gothic English

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-english.zip)

### PF Hershey Gothic German

Source credits retained verbatim:

```text
Font name: Hershey Gothic German

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-german.zip)

### PF Hershey Gothic Italian

Source credits retained verbatim:

```text
Font name: Hershey Gothic Italian

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-gothic-italian.zip)

### PF Hershey Sans 1-stroke

Source credits retained verbatim:

```text
Font name: Hershey Sans 1-stroke

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-sans-1-stroke.zip)

### PF Hershey Sans medium

Source credits retained verbatim:

```text
Font name: Hershey Sans medium

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-sans-medium.zip)

### PF Hershey Script 1-stroke

Source credits retained verbatim:

```text
Font name: Hershey Script 1-stroke

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-script-1-stroke.zip)

### PF Hershey Script medium

Source credits retained verbatim:

```text
Font name: Hershey Script medium

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-script-medium.zip)

### PF Hershey Serif bold

Source credits retained verbatim:

```text
Font name: Hershey Serif bold

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-bold.zip)

### PF Hershey Serif bold italic

Source credits retained verbatim:

```text
Font name: Hershey Serif bold italic

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-bold-italic.zip)

### PF Hershey Serif medium

Source credits retained verbatim:

```text
Font name: Hershey Serif medium

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-medium.zip)

### PF Hershey Serif medium italic

Source credits retained verbatim:

```text
Font name: Hershey Serif medium italic

Originally prepared in 2011 and converted to SVG fonts
in 2019 by Windell H. Oskay, www.evilmadscientist.com

Contents adapted from emergent.unpythonic.net/software/hershey
 by way of "Hershey Fonts in SVG" by Marty McGuire
 http://www.thingiverse.com/thing:6168

-------------------------------------------------------------------
The Hershey Fonts are a set of vector fonts with a liberal license.

USE RESTRICTION:
    This distribution of the Hershey Fonts may be used by anyone for
    any purpose, commercial or otherwise, providing that:
        1. The following acknowledgements must be distributed with
            the font data:
            - The Hershey Fonts were originally created by Dr.
                A. V. Hershey while working at the U. S.
                National Bureau of Standards.
            - The format of the Font data in this distribution
                was originally created by
                    James Hurt
                    Cognition, Inc.
                    900 Technology Park Drive
                    Billerica, MA 01821
                    (mit-eddie!ci-dandelion!hurt)
        2. The font data in this distribution may be converted into
            any other format *EXCEPT* the format distributed by
            the U.S. NTIS where each point is described
            in eight bytes as "xxx yyy:", where xxx and yyy are
            the coordinate values as ASCII numbers.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-hershey-serif-medium-italic.zip)

### PF Twin Sans

Source credits retained verbatim:

```text
Font name:       Twin Sans
License:         SIL Open Font License http://scripts.sil.org/OFL
Created by:      Keith Packard
A derivative of: Hershey Sans

Prepared in 2023 and converted to SVG fonts
in 2023 by Keith Packard, www.keithp.com
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-twin-sans.zip)

### PF Relief SingleLine Ornament

Source credits retained verbatim:

```text
Created by FontForge 20201107 at Thu May 26 19:50:12 2022
 By Tanguy Vanlaeys
Copyright 2021 The Relief SingleLine Project Authors (https://github.com/isdat-type/Relief-SingleLine)
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-relief-singleline-ornament.zip)

### PF Relief SingleLine SVG

Source credits retained verbatim:

```text
Created by FontForge 20201107 at Fri Feb 14 11:47:47 2025
 By Tanguy Vanlaeys
Copyright 2021 The Relief SingleLine Project Authors (https://github.com/isdat-type/Relief-SingleLine)
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-relief-singleline-svg.zip)

### PF Norm Stroke

Source credits retained verbatim:

```text
Font name:               Norm Stroke
License:                 This work is marked with CC0 1.0. To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/
A derivative of:         https://commons.wikimedia.org/wiki/File:ISO3098.svg
Version:                 1.0
NormStroke by octycs; based on Wikimedia ISO3098 Type B lettering. CC0 declaration retained.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-norm-stroke.zip)

### PF Custom-Script

Source credits retained verbatim:

```text
Open Font License
Custom stroke fonts by Shriinivas; derived from Square Grotesk and Pinyon Script as credited upstream. Font notice template has unfilled copyright fields; original declarations retained.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-script.zip)

### PF Custom-Square Italic

Source credits retained verbatim:

```text
Open Font License
Custom stroke fonts by Shriinivas; derived from Square Grotesk and Pinyon Script as credited upstream. Font notice template has unfilled copyright fields; original declarations retained.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-square-italic.zip)

### PF Custom-Square Normal

Source credits retained verbatim:

```text
Open Font License
Custom stroke fonts by Shriinivas; derived from Square Grotesk and Pinyon Script as credited upstream. Font notice template has unfilled copyright fields; original declarations retained.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-custom-square-normal.zip)

### PF CutlingsDualis

Source credits retained verbatim:

```text
Font name:               Cutlings Dualis
License:                 SIL Open Font License http://scripts.sil.org/OFL
Designed by:             Ellen Wasbo
Link:                    http://cutlings.wasbo.net/
Cutlings Singularis, Dualis and Pluralis by Ellen Wasbø; author credits and font license in readme.txt.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingsdualis.zip)

### PF CutlingsPluralis

Source credits retained verbatim:

```text
Font name:               Cutlings Pluralis
License:                 SIL Open Font License http://scripts.sil.org/OFL
Designed by:             Ellen Wasbo
Link:                    http://cutlings.wasbo.net/
Cutlings Singularis, Dualis and Pluralis by Ellen Wasbø; author credits and font license in readme.txt.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingspluralis.zip)

### PF CutlingsSingularis

Source credits retained verbatim:

```text
Font name:               Cutlings Singularis
License:                 SIL Open Font License http://scripts.sil.org/OFL
Designed by:             Ellen Wasbo
Link:                    http://cutlings.wasbo.net/
Cutlings Singularis, Dualis and Pluralis by Ellen Wasbø; author credits and font license in readme.txt.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cutlingssingularis.zip)

### PF DearPlotter

Source credits retained verbatim:

```text
Font name: DearPlotter
Format: SVG 1.1 single-line font
Converted to SVG 1.1 Font format from the p5.js DearPlotter font archive.

Source: licia_he_font/sketch.js and licia_he_font/fontData.js
Original font: DearPlotter Font Generator, created by Licia He in 2026.
DearPlotter was commissioned by The Processing Foundation and the Tezos Foundation.
The p5.js and SVG adaptation is by Golan Levin, 2026.

Licensing notes from the repository README:
The DearPlotter Font Generator is licensed under Creative Commons Attribution-ShareAlike 4.0 International.
Fonts created with it are licensed under the SIL Open Font License.

Reference:
https://www.eyesofpanda.com/project/dearplotter_font/

This conversion preserves DearPlotter's cubic Bezier stroke geometry using SVG C commands.
It includes printable ASCII glyphs present in the source data, plus a space glyph.
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-dearplotter.zip)

### PF CAD iso3098

Source credits retained verbatim:

```text
# Author:            AZO <typesylph@gmail.com> (convert)
# Author:            User:K7 (ISO3098.svg, Wikimedia Commons)
# License:           GPL v2 or later
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-iso3098.zip)

### PF CAD iso3098_i

Source credits retained verbatim:

```text
# Author:            AZO <typesylph@gmail.com> (convert)
# Author:            User:K7 (ISO3098.svg, Wikimedia Commons)
# License:           GPL v2 or later
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-iso3098-i.zip)

### PF CAD lc_opengost-ar

Source credits retained verbatim:

```text
# Author:            stranger573 <stranger573@mail.ru>
# License:           SIL OPEN FONT LICENSE Version 1.1
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-lc-opengost-ar.zip)

### PF CAD lc_opengost-br

Source credits retained verbatim:

```text
# Author:            stranger573 <stranger573@mail.ru>
# License:           SIL OPEN FONT LICENSE Version 1.1
```

[Complete notices and source](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-cad-lc-opengost-br.zip)


### PF EMS SpaceRocks

Source credits retained verbatim:

```text
Font name:               EMS SpaceRocks
License:                 SIL Open Font License http://scripts.sil.org/OFL
Created by:              Trammell Hudson
SVG font conversion by:  Trammell Hudson
A derivative of:         Atari Asteroids font
Designer:                Ed Logg
Link:                    https://trmm.net/Asteroids_font
```

[Complete source and notices](https://thierryc.github.io/OpenPlotFont/assets/catalog/pf-ems-spacerocks.zip)
