# Hershey font catalog

The four faces below preserve pinned upstream JHF trajectories and spacing. Each contains 96 upstream records plus an original `.notdef`: 97 glyphs and 95 printable ASCII mappings. Row 95 remains unencoded. Drawing order, pen-up boundaries, direction, and open endpoints are preserved.

| Face | Editable source and provenance | Native JSON export | Specimen |
| --- | --- | --- | --- |
| Roman Simplex | [Source notes](hershey-roman-simplex/README.md) | [JSON](../examples/hershey-roman-simplex.plotfont.json) | [SVG](../examples/specimens/hershey-roman-simplex.svg) |
| Roman Duplex | [Source notes](hershey-roman-duplex/README.md) | [JSON](../examples/hershey-roman-duplex.plotfont.json) | [SVG](../examples/specimens/hershey-roman-duplex.svg) |
| Roman Triplex | [Source notes](hershey-roman-triplex/README.md) | [JSON](../examples/hershey-roman-triplex.plotfont.json) | [SVG](../examples/specimens/hershey-roman-triplex.svg) |
| Script Simplex | [Source notes](hershey-script-simplex/README.md) | [JSON](../examples/hershey-script-simplex.plotfont.json) | [SVG](../examples/specimens/hershey-script-simplex.svg) |

Editable native sources and reproducible preparations live in each face's directory. Curated exports under `examples/` were generated in Glyphs from copies and compared against the preparations. Separate saved-package tests inspect every stored node, metric, advance, Unicode assignment, and source identifier. Native reopening and the actual export-script entry point also passed.

Roman Simplex was populated and saved in Glyphs 4.1 build 4107. Roman Duplex, Roman Triplex, and Script Simplex were created using MCP `create_document`, then populated and saved in Glyphs 4.1.1 build 4108. Creation requires both the advertised tool and `document.create.v1`. Population uses [Import Hershey Font.py](../scripts/Import%20Hershey%20Font.py) against a saved empty source at its exact project path; existing artwork is rejected. Native exports use [Export PlotFont.py](../scripts/Export%20PlotFont.py) on copies.

Use `python3 -m plotfont import-hershey SOURCE --face FACE -o output/NAME.plotfont.json` for reproducible preparation. Supported face names are `roman-simplex` (default), `roman-duplex`, `roman-triplex`, and `script-simplex`. Each has an independently pinned digest; selecting the wrong face or modifying the bytes fails rather than mislabeling provenance. The four retained preparations and their historical native examples remain draft `0.2` for reproducibility and compatibility. The current format is `0.3`; plugin 0.1.1 exports these editable sources as geometry-only 0.3. Optional layout requires the matching compiled-font workflow described in [the export documentation](../docs/GLYPHS_AND_EXPORT.md).

No font gets invented kerning or script-connection annotations. Script Simplex retains its original multiple strokes and pen lifts. Roman Duplex and Triplex use additional trajectories to suggest heavier forms; these strokes do not become fills. Tool width and physical sizing remain consumer settings.

Retain [the Hershey upstream notice](../vendor/hershey/NOTICE.txt) with data and derivatives. Hershey glyph geometry is not MIT; original project code and fallback artwork use project MIT.
