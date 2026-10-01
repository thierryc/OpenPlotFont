# PlotFont website

Plain HTML, CSS and JavaScript, following the [beztrace](https://thierryc.github.io/beztrace/) stack and visual language, with the large specimens and spare navigation of [ap.cx](https://ap.cx/). No framework, package manager, analytics, external fonts, or browser dependencies.

Build with Python 3.10 or later from the repository root:

```sh
python3 scripts/build_website.py
python3 scripts/verify_website.py
python3 -m http.server 8080 --directory output/website
```

Open `http://localhost:8080`. Build output and plugin staging remain under `output/`. Builds preserve existing output; choose `--destination output/website-next` for another build, and pass that same destination to the verifier. `index.html` is a template; the build renders the complete catalog into HTML. Search and collection filtering are optional enhancements: every font, credit and download is available without JavaScript.

## Catalog snapshot

`catalog.json` and `assets/catalog/` are the reviewed publication snapshot of 87 qualified local preparations as of 2026-10-01. The snapshot includes complete individual font bundles and specimen SVGs with embedded notices. The ZIPs include original font source, full license notices, attribution, PlotFont JSON, native Glyphs packages/exports, and review specimens. They retain upstream licenses; the repository's MIT license does not replace them. Asset digests bind the listing to its reviewed files.

The 87 local font-library packages passed source-to-native save/reopen comparison in Glyphs 4.1.1 (4108), with tolerance 0.000501 font units for native rounding. This is font preparation qualification, not hardware testing. Some Hershey source adaptations overlap in design. Fourteen non-Latin/symbol JHF sources retain temporary private-use mappings. See each ZIP's README and source credits for the full conversion and coverage notes.

To refresh, first fetch, prepare, qualify and package the library using its authoring workflow. Then run `python3 scripts/prepare_website_catalog.py`. Review `output/website-catalog/`, including credits and licenses, before copying its `catalog.json` and `assets/catalog/` into `site/`. GitHub Actions deploys the reviewed snapshot; it does not rerun native Glyphs qualification on Linux.

The Glyphs plugin ZIP is built from the current tracked exporter sources during each site build. Its version comes from the plugin plist; the ZIP retains the SDK and project licenses and the loader's executable permission. The page discloses pending startup/menu qualification. No source font is opened or modified by a website build.

## GitHub Pages

[pages.yml](../.github/workflows/pages.yml) builds, verifies and deploys `output/website` on relevant changes to `main`, or through workflow dispatch. In the repository's **Settings → Pages**, set **Source → GitHub Actions**. The project URL is `https://thierryc.github.io/PlotFont/`; all local asset links are relative so the project subpath works.
