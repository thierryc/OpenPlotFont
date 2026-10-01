# Stroke-font candidates for PlotFont

Research date: 2026-10-01. **Follow-up:** see the [converted library](FONT_LIBRARY.md) for the implemented SVG/LFF preparation, native qualification, current inclusion decisions and remaining coverage limits. The historical candidate inventory below records the state before that work. This is a candidate catalog, not a list of newly implemented imports. Priorities are recommendations. Font counts below distinguish source records from verified Unicode coverage.

The best next steps are to extend the pinned Hershey importer for a few distinct Latin faces, then add a reviewed SVG-font conversion route. SVG fonts unlock modern lettering and real curves. Relief's editable sources also make it a strong candidate for the existing Glyphs export workflow, subject to source and native compatibility qualification.

## Existing support and selection criteria

The [current catalog](../fonts/README.md) contains Roman Simplex, Roman Duplex, Roman Triplex, and Script Simplex. Each has 96 upstream records, 95 printable ASCII mappings, an unencoded final record, and an original `.notdef`. The [Hershey importer](../plotfont/hershey.py) explicitly supports only those four pinned faces; a JHF file being parseable does not make it a supported CLI import.

Prefer sources with explicit pen-up boundaries, reusable per-glyph geometry, spacing information, and a font-specific redistribution license. A centerline font can contain multiple strokes and closed centerline loops. Duplex, triplex, and decorative stroke fonts are eligible even when they use several trajectories to suggest weight.

Neither an ordinary thin outline font nor a font advertised as “monoline” necessarily contains centerlines. Do not recover skeletons from filled outlines or silently remove closing edges. Conversion must follow the [format geometry rules](PLOTFONT_FORMAT.md) and [authoring/export workflow](GLYPHS_AND_EXPORT.md).

## 1. More classic Hershey fonts: the smallest conversion gap

Source: [kamalmostafa/hershey-fonts, pinned revision](https://github.com/kamalmostafa/hershey-fonts/tree/1356bf2f83d380fcef68c887e88675eb9d445d86/hershey-fonts). This is the same revision already used by PlotFont. All 32 JHF files were read and passed the existing low-level `parse_jhf` parser during research. Four are already included, leaving **28 additional candidate files**, not necessarily 28 distinct designs.

The glyph data has the [Hershey permissive terms](../vendor/hershey/NOTICE.txt), separate from the upstream C library's GPL license. Retain the required acknowledgments and the restriction against conversion to the original NTIS distribution representation. PlotFont JSON is a different representation. Keep the complete notice with derivatives; do not relabel the geometry as project MIT.

| Candidate/design group | Exact source file(s) | Records per file | Recommendation and conversion work |
| --- | --- | ---: | --- |
| Futural, light sans | `futural.jhf` | 96 | First batch: useful sans alternative to Roman Simplex; review Latin mapping and metrics. |
| Futuram, medium sans | `futuram.jhf` | 96 | First batch: preserve its extra weight-building trajectories as strokes. |
| Roman Complex / Times Roman | `timesr.jhf` | 96 | First batch: serif variety between existing simplex and triplex choices. |
| Roman Italic / Times Italic | `timesi.jhf` | 96 | First batch: a distinct italic serif option. |
| Bold Roman / Times Roman Bold | `timesrb.jhf` | 96 | Later Latin batch: additional trajectories, not filled outlines. |
| Bold Italic / Times Bold Italic | `timesib.jhf` | 96 | Later Latin batch: preserve every trajectory and overhang. |
| Script Complex | `scriptc.jhf` | 96 | First batch: richer script than existing Script Simplex; no automatic joins. |
| Alternate cursive | `cursive.jhf` | 96 | Later Latin batch: compare against Script Simplex before deciding catalog identity. |
| English Gothic variants | `gothgbt.jhf`, `gothiceng.jhf` | 96 | Decorative batch: compare both variants rather than assuming equivalent aliases. |
| German Gothic variants | `gothgrt.jhf`, `gothicger.jhf` | 96 | Decorative batch: same variant review; more drawing operations than simple faces. |
| Italian Gothic variants | `gothitt.jhf`, `gothicita.jhf` | 96 | Decorative batch: retain original stroke scheduling. |
| Greek Simplex and alternative | `greeks.jhf`, `greek.jhf` | 96 | Multilingual batch: establish Greek Unicode mapping; compare variants. |
| Greek Complex and alternative | `greekc.jhf`, `timesg.jhf` | 96 | Multilingual batch: review glyph identities and differences. |
| Cyrillic variants | `cyrillic.jhf`, `cyrilc_1.jhf` | 96 | Multilingual batch: Unicode mapping is required, not ASCII row numbering. |
| Japanese repertoire | `japanese.jhf` | 193 | Specialist batch: inspect every character and map explicitly; not a modern comprehensive Japanese font. |
| Mathematical symbols | `mathlow.jhf`, `mathupp.jhf` | 96 | Specialist batch: establish semantic names and Unicode where appropriate. |
| General symbols | `symbolic.jhf` | 96 | Specialist batch: retain unmappable symbols unencoded. |
| Astrology symbols | `astrology.jhf` | 96 | Specialist batch: inspect symbol identities and spacing. |
| Weather symbols | `meteorology.jhf` | 96 | Specialist batch: useful scientific drawing repertoire; mapping review needed. |
| Music symbols | `music.jhf` | 96 | Specialist batch: a symbol collection, not a music-layout engine. |
| Plot markers | `markers.jhf` | 97 | Specialist batch: likely more useful as named glyphs than a text alphabet. |

These record totals were measured from the pinned files. They do not prove complete alphabets or Unicode coverage. The differently named Gothic, Greek, Cyrillic, and cursive variants should be compared visually and geometrically before assigning separate public family names.

JHF already encodes polylines, bearings, and pen lifts. A new face still needs a pinned digest, explicit character mapping, its own reviewed normalization and metrics, and fixtures. The current importer assumes 96 records and a particular baseline/cap-height transform; neither assumption should be applied to new repertoires without checking. Repeated first/last coordinates do not supply an explicit closure flag: preserve the trajectory without guessing closure.

## 2. Non-Hershey sources worth adding

| Candidate | Preferred source format | License evidence | Value and remaining work |
| --- | --- | --- | --- |
| [Relief SingleLine](https://github.com/isdat-type/Relief-SingleLine) | Skeletal `.glyphs` or UFO; alternatively `fonts/open_svg/ReliefSingleLineSVG-Regular.svg` | Project `OFL.txt`, SIL OFL 1.1 | Highest priority modern sans. Curves, kerning, and alternates; inspected SVG has 566 `<glyph>` elements. Review editable source in a copy and qualify export; SVG-only conversion needs an adapter. |
| [NormStroke](https://github.com/octycs/norm-stroke) | `font/NormStroke.svg`; open UFO also available | Author's README declares CC0 1.0 | Highest priority technical lettering based on ISO 3098 Type B. SVG has 324 glyph elements, matching the documented 323 characters plus space. Inspected UFO `A` has two explicitly open contours. Prefer SVG over its pseudoclosed TTF/OTF variants. |
| [EMS SVG collection](https://gitlab.com/oskay/svg-fonts/-/tree/master/fonts/EMS) | SVG 1.1 fonts | Per-file metadata declares SIL OFL; accompanying `OFL.txt` | High priority: 29 fonts/styles found, with handwriting, script, sans, and display options. Full list below. Review ancestry and geometry per face; two candidates need extra license/provenance work. |
| [Singularis, Dualis, Pluralis](https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/) | Author's SVG font downloads | Author explicitly offers them under SIL OFL | Useful family spanning one-, two-, and three-line construction. The author identifies SVGs as the real stroke versions. Inspect downloaded font data and notices before qualification; avoid substituting companion TTF geometry. |
| [Custom-Script, Custom-Square Normal, Custom-Square Italic](https://github.com/Shriinivas/inkscapestrokefont/tree/master/strokefontdata) | SVG fonts | Font metadata/README identify OFL and ancestry in Pinyon Script and Square Grotesk | Useful cursive and geometric alternatives. `Custom-Script.svg` has 98 glyph elements. Accompanying OFL contains placeholder copyright fields, so complete attribution/provenance needs review. Extension code is GPL; keep that separate from font terms. |
| [DearPlotter](https://www.eyesofpanda.com/project/dearplotter_font/) | Exported core-stroke JSON or SVG | Author specifies SIL OFL for generated fonts; generator uses CC BY-SA 4.0 | Good source of original customizable Latin stroke families with cubic curves. Export and retain the actual design/parameters; a seed alone does not reproduce interactive changes. Select core strokes, excluding tool-dependent outlines/hatches. Adapter not implemented. |
| [Leon Sans](https://github.com/cmiscm/leonsans) | JavaScript font definitions and path construction | Repository MIT license | Experimental geometric family authored in code. Requires extraction of a fixed static design, advances, and ordered paths; avoid bundling runtime animation or treating a visual line-width parameter as font geometry. |
| [LibreCAD OpenGOST A/B stroke adaptations](https://github.com/LibreCAD/LibreCAD/tree/master/librecad/support/fonts) | `lc_opengost-ar.lff`, `lc_opengost-br.lff` | Each inspected file header specifies SIL OFL 1.1 | Strong technical-lettering candidates for a future LFF route. Ordered polylines plus circular arc/bulge notation and character references; needs spacing and curve-conversion policy. |
| [LibreCAD ISO3098 regular/italic](https://github.com/LibreCAD/LibreCAD/tree/master/librecad/support/fonts) | `iso3098.lff`, `iso3098_i.lff` | Each inspected header specifies GPL v2 or later | Open-source technical fonts; preserve those font-specific terms. NormStroke is a simpler first source for comparable lettering under CC0. LFF conversion remains unimplemented. |

Counts of `<glyph>` elements are source inventory counts, not verified distinct scalar mappings. Relief includes unencoded/alternate drawings; Unicode, ligatures, and fallback need separate review. Its [source inventory](https://github.com/isdat-type/Relief-SingleLine/tree/01dfc5779ec1e9e4b288d96c6c96c23bfccbaf9d/sources) includes skeletal Glyphs and UFO files plus an ornament source. Review ornaments separately for drawing intent.

### EMS collection: individual candidates

Inspected source revision: `8c71f2d9e1a5292047bb88e5595a766241b82cc6`, [font directory](https://gitlab.com/oskay/svg-fonts/-/tree/8c71f2d9e1a5292047bb88e5595a766241b82cc6/fonts/EMS). Metadata identifies the upstream designs, Sheldon B. Michaels' derivatives for most faces, and SVG conversion by Windell H. Oskay. These are existing stroke-font derivatives; this proposal does not call for skeletonizing the original outline fonts.

| Candidate | Declared source design | Selection note |
| --- | --- | --- |
| EMS Readability | Source Sans Pro-Light | First SVG batch: everyday sans. |
| EMS Readability Italic | Source Sans Pro-Light | Useful matching italic. |
| EMS Allure | Allura | First SVG batch: flowing script. |
| EMS Tech | Architects Daughter | First SVG batch: informal technical hand. |
| EMS Nixish | Nixie One | First SVG batch: distinctive display lettering. |
| EMS Nixish Italic | Nixie One | Matching variant. |
| EMS Osmotron | Orbitron Regular | First SVG batch: geometric display. |
| EMS Bird | Bilbo | Additional script. |
| EMS Bird Swash Caps | Bilbo Swash Caps | Decorative capital variant. |
| EMS Brush | Alex Brush | Additional script. |
| EMS Capitol | Sacramento | Additional script. |
| EMS Casual Hand | Covered By Your Grace | Handwritten option. |
| EMS Decorous Script | Petit Formal Script | Formal script option. |
| EMS Delight | Delius | Informal option. |
| EMS Delight Swash Caps | Delius Swash Caps | Decorative capital variant. |
| EMS Elfin | Mountains of Christmas | Hold: file notes OFL versus Apache 2.0 license discrepancy. Resolve ancestry/notices first. |
| EMS Felix | Felipa | Additional calligraphic option. |
| EMS Herculean | Poiret One | Display option. |
| EMS Invite | Tangerine | Formal script option. |
| EMS League | League Script | Additional script. |
| EMS Little Princess | Princess Sofia | Decorative option. |
| EMS Misty Night | Foglihten No03 | Decorative option. |
| EMS Neato | Bad Script | Handwritten option. |
| EMS Pancakes | Short Stack | Informal option. |
| EMS Pepita | Pecita | Handwritten option. |
| EMS Qwandry | Qwigley | SVG metadata spells it “Qwandry”; filename is `EMSQwandry.svg`. |
| EMS Society | Mrs Saint Delafield | Formal script option. |
| EMS Swiss | Italianno | Additional script. |
| EMS SpaceRocks | Atari Asteroids font | Included in the converted library using the source SVG’s declared SIL OFL, with its original attribution retained. |

All inspected EMS files declare OFL in metadata. SpaceRocks contains 95 glyph elements; each of the other 28 contains 216. An older [hersheytextjs copy](https://github.com/techninja/hersheytextjs/tree/262f4782cd412ee539eb43d4d9d9b92562d7590b/svg_fonts) contains only nine EMS faces, with 187 glyph elements each. Prefer the larger original collection and pin the selected files rather than combining mirrors blindly.

Script styling does not authorize continuous pen-down text. Add connection declarations only after reviewing actual entry/exit endpoints and a joining policy.

## 3. Specialist and deferred sources

- **[KST32B in LibreCAD](https://github.com/LibreCAD/LibreCAD/blob/master/librecad/support/fonts/kst32b.lff):** promising Japanese and multilingual stroke repertoire. The inspected header says `GPL v2 or later, KST32B`. Resolve the additional KST32B terms and character mapping before adding; do not assume LibreCAD's application license answers every font question.
- **[LingDong's Chinese Hershey fonts](https://github.com/LingDong-/chinese-hershey-font):** Heiti/Kaiti list 20,975 characters each; Mingti lists 73,874. JHF-like text and normalized polyline JSON are available. These are algorithmically inferred skeletons from outline/raster fonts, so they fall outside this repository's current “do not infer centerlines” policy for a normal import batch. Treat as a separate research proposal requiring explicit scope review, visual/stroke-order review, and upstream font-license tracing. The converter's MIT license is insufficient evidence for every derived font.
- **[LibreCAD's remaining LFF library](https://github.com/LibreCAD/LibreCAD/tree/master/librecad/support/fonts):** Roman Complex/Complex Small, additional Greek, script, and symbol files could expand coverage. Inspect each file rather than importing the whole folder. Some are Hershey relatives; some contain outline-derived geometry. `unicode.lff` explicitly declares `GPL v2 or later + unknown`, so defer it.
- **[Golan Levin's single-line resource archive](https://github.com/golanlevin/p5-single-line-font-resources):** excellent discovery index for SVG, TTF, JSON, procedural fonts, vintage plotters, SHX, and CJK sources. Use original authors' repositories for redistribution decisions. ROM-extracted Apple/Commodore/Tektronix/game lettering and AutoCAD SHX archives need underlying font rights checked; extraction-code licenses alone do not settle them.
- **Conventional Hershey TTF/OTF reinterpretations:** useful for visual companions, but inspect whether they contain expanded outlines or forced closing edges. Prefer original JHF for authentic trajectories. Commercial single-line fonts, system stick fonts, and download-only “free” fonts are outside the open-source shortlist unless their font license explicitly permits conversion and redistribution.

## 4. Conversion routes and information to retain

These are proposed adapters, except for the existing four-face JHF preparation and Glyphs export routes.

| Source format | Route to PlotFont | Main review points |
| --- | --- | --- |
| JHF / Hershey text | Parse bearings and pen-up-separated polylines; normalize with a reviewed baseline and scale | JHF IDs are not Unicode. Do not reuse ASCII row mapping or metrics globally; preserve source trajectory order and repeated endpoints. |
| SVG 1.1 font | Read `<font-face>`, `<glyph>`, `<missing-glyph>`, advances, paths, and optional kerning | Font coordinates are Y-up, unlike ordinary SVG page coordinates. Split every `M` subpath into its own trajectory; preserve `Z` closure and explicit stroke/fill intent. |
| Skeletal UFO / GLIF | Read advances, Unicode, ordered contours, points, components, and kerning | An initial `move` point specifies an open contour. Resolve components with transforms and order intact; retain quadratic/cubic curves. Font-specific drawing intent still needs review. |
| Skeletal Glyphs | Qualify a copy through the existing selected-master export workflow | Check source format/app compatibility, contours, intent, metrics, and features. No native qualification of these candidate sources has been performed. |
| CAD LFF / CXF | Parse ordered lines/arcs and character references; reconstruct documented advances | Arcs need a reviewed representation policy; character references must be resolved without inventing connections. Do not replace spacing with bounds alone. |
| Procedural JS / stroke JSON | Extract one static design into glyph metrics and ordered `M/L/Q/C` paths | Pin design parameters and coordinate transforms. Preserve original curves and pen lifts; retain generator and font notices separately. |
| OpenType-SVG | Extract actual SVG glyph documents and align with OpenType glyph IDs/cmap/metrics | More complex than standalone SVG; ordinary outline tables may be only companions. Features require the separately validated PlotFont layout workflow. |
| TTF/OTF “single-line” | Use only a documented and verified source convention | Never remove all closing edges generically: real loops and pseudoclosed paths need different treatment. Prefer an open source version when available. |

See the authoritative [SVG font specification](https://www.w3.org/TR/SVG11/fonts.html) and [UFO GLIF specification](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/) for coordinate and contour semantics. SVG relative/shorthand commands need normalization. PlotFont supports `M`, `L`, `Q`, and `C`, not native circular/elliptical arcs. Circular arcs cannot be represented exactly by a finite set of ordinary polynomial Béziers: reject them until an explicit, documented approximation policy is agreed, or convert with an approved bound tied to the intended physical scale. Do not silently flatten source curves.

SVG glyphs may map to multi-character strings. PlotFont's scalar `unicodes` array cannot encode a ligature sequence: retain the glyph unencoded and supply supported layout rules where needed. Likewise, SVG kerning expressed through groups/ranges needs explicit resolution rather than omission. Keep geometry import distinct from optional compiled shaping; do not claim that importing an SVG brings across all OpenType behavior.

For each accepted face, retain source URL/revision, source-file digest, copyright/attribution, the complete font notice, character mapping, coordinate transform, and any acknowledged losses. New additions should use current draft 0.3. The retained four-face JHF preparation emits legacy 0.2; a validated version migration is documented in the [format specification](PLOTFONT_FORMAT.md#draft-compatibility).

## Recommended implementation batches

1. **Hershey diversity:** Futural, Futuram, Roman Complex (`timesr`), Roman Italic (`timesi`), Script Complex, and one reviewed English Gothic variant. No new geometry format parser is needed, but face configuration, metrics, mapping, and provenance qualification are.
2. **Modern curved fonts:** Relief SingleLine and NormStroke, followed by EMS Readability, Allure, Tech, Nixish, and Osmotron. A reusable SVG-font adapter offers the largest catalog gain; Relief's skeletal Glyphs source is an additional route to qualify.
3. **Coverage and technical lettering:** reviewed Greek/Cyrillic JHF mappings, Hershey symbols, OpenGOST LFF, then KST32B if its additional terms are resolved.
4. **Creative static designs:** Cutlings families, Custom-Square/Script after attribution review, DearPlotter core-stroke exports, and a static Leon Sans extraction.

Acceptance requires geometry/spacing comparison and a specimen containing separate strokes, loops, curves, descenders, space, missing characters, scaling, and axis conversion as applicable. Preserve fills or reject unsupported source intent; never plot only their boundaries. Generated preparations and research output belong in `output/`; add curated fonts/examples only after review. This research added no font data or importer implementation.
