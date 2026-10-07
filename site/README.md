# OpenPlotFont website

Plain HTML, CSS and JavaScript, following the [beztrace](https://thierryc.github.io/beztrace/) stack and visual language, with the large specimens and spare navigation of [ap.cx](https://ap.cx/). No framework, bundler, analytics, or runtime CDN requests.

The website uses the visitor's system font by default, including the animated footer. Code samples use the system monospace font stack. Catalog specimens preserve the font geometry they demonstrate.

## Official ap.cx footer

The animated footer uses the vanilla `mountMarquee` API of the official [@ap.cx/gl-marquee](https://www.npmjs.com/package/@ap.cx/gl-marquee) **0.1.0** package. Its unmodified browser modules are self-hosted under `vendor/gl-marquee/`; `SOURCE.json` records the npm tarball integrity and per-file SHA-256 digests. The package's MIT license is retained. The package has no runtime dependencies, so website builds still use Python alone.

`footer.js` mounts the package in `footer-banner` mode with the ap.cx message and inherits the website's system font. No custom web font is loaded. The marquee respects reduced motion, provides a Play/Pause button, and releases its renderer when the footer leaves view. The package handles resizing, hidden-document pauses, WebGL context restoration, and a Canvas 2D fallback when WebGL2 is unavailable. Brand and copyright text remain ordinary accessible HTML.

To update the package, run `npm pack @ap.cx/gl-marquee@VERSION --ignore-scripts --pack-destination output`, verify the official npm integrity, and replace only the published `dist/index.js`, `dist/mount.js`, `dist/renderer.js`, `package.json` and `LICENSE`. Update `SOURCE.json` and this version note, then build and verify the site. No npm lifecycle scripts or application framework are required.

Build with Python 3.10 or later from the repository root:

```sh
python3 scripts/build_website.py
python3 scripts/verify_website.py
python3 -m http.server 8080 --directory output/website
```

Open `http://localhost:8080`. Build output and plugin staging remain under `output/`. Builds preserve existing output; choose `--destination output/website-next` for another build, and pass that same destination to the verifier. `index.html` is a template; the build renders the complete catalog into HTML. Search and collection filtering are optional enhancements: every font, credit and download is available without JavaScript.

## Catalog snapshot

`catalog.json` and `assets/catalog/` are the reviewed publication snapshot of 87 qualified local preparations as of 2026-10-01. The snapshot includes complete individual font bundles and specimen SVGs with embedded notices. The ZIPs include original font source, full license notices, attribution, OpenPlotFont JSON, native Glyphs packages/exports, and review specimens. They retain upstream licenses; the repository's MIT license does not replace them. Asset digests bind the listing to its reviewed files. The 2026-10-07 naming migration updates project metadata, JSON filenames and catalog digests; it preserves drawings and upstream source/license files and does not claim a new native qualification of all 87 packages.

The pre-rename 87 local font-library packages passed source-to-native save/reopen comparison in Glyphs 4.1.1 (4108), with tolerance 0.000501 font units for native rounding. This is font preparation qualification, not hardware testing. Some Hershey source adaptations overlap in design. Fourteen non-Latin/symbol JHF sources retain temporary private-use mappings. See each ZIP's README and source credits for the full conversion and coverage notes.

Cards with private-use mappings explain this conversion limitation: the numbered JHF drawings have not yet been assigned reviewed standard Unicode characters. Each source row uses U+E000 plus its zero-based row index as a placeholder. Users can select drawings by glyph name using the included atlas, or look up their private-use codes in the OpenPlotFont JSON. These assignments are specific to each font and are not interchangeable character meanings.

To refresh, first fetch, prepare, qualify and package the library using its authoring workflow. Then run `python3 scripts/prepare_website_catalog.py`. Review `output/website-catalog/`, including credits and licenses, before copying its `catalog.json` and `assets/catalog/` into `site/`. GitHub Actions deploys the reviewed snapshot; it does not rerun native Glyphs qualification on Linux.

The Glyphs plugin ZIP is built from the current tracked exporter sources during each site build. Its version comes from the plugin plist; the ZIP retains the SDK and project licenses and the loader's executable permission. The page discloses pending startup/menu qualification. No source font is opened or modified by a website build.

## GitHub Pages

[pages.yml](../.github/workflows/pages.yml) builds, verifies and deploys `output/website` on relevant changes to `main`, or through workflow dispatch. In the repository's **Settings → Pages**, set **Source → GitHub Actions** and leave **Custom domain** unset for now. The canonical website URL is `https://thierryc.github.io/OpenPlotFont/`. Relative asset links work under this project path and in local previews. Publishing the renamed content requires committing and deploying the changes; a repository rename alone does not update deployed assets.

When DNS is ready, configure **Custom domain → openplotfont.litsquare.com**, then add a `CNAME` record named `openplotfont` pointing to `thierryc.github.io` at the DNS provider for `litsquare.com`. Update the canonical URL, repository homepage and maintained website links to the new domain, then enable **Enforce HTTPS** once the certificate is available. Actions deployments do not require a repository `CNAME` file. See [GitHub's custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).
