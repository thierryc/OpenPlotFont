"""Assemble the static Pages site and self-contained Glyphs plugin with stdlib only."""
import argparse
import html
import json
import plistlib
import shutil
import zipfile
from pathlib import Path

from build_glyphs_plugin import build as build_plugin

ROOT = Path(__file__).resolve().parents[1]


def font_card(font):
    escape = html.escape
    key = escape(font['id'], quote=True)
    searchable = escape(' '.join(str(font[field]) for field in
        ('family', 'collection', 'license', 'attribution')).lower(), quote=True)
    links = ''.join(f'<a href="{escape(url, quote=True)}">Author/source {i + 1} ↗</a>'
                    for i, url in enumerate(font['authorLinks']))
    mapping = '''<p class="mapping-note">Unicode mapping pending · choose glyphs from the included atlas.</p>
    <details class="mapping-explanation"><summary>Why are these mappings temporary?</summary>
      <p>The original JHF file stores numbered drawings, without Unicode character labels. This conversion has not yet verified the character represented by each source row. It assigns placeholder codes in source order: U+E000 for the first drawing, U+E001 for the next, and so on.</p>
      <p>These codes are in the <a href="https://www.unicode.org/faq/private_use.html">Unicode Private Use Area</a>, where character meanings are defined by individual fonts. The same code can select a different drawing in another font. The stroke geometry is preserved, but ordinary typed text will not select these drawings through their standard Unicode characters.</p>
      <p>Open glyph-atlas.svg from the ZIP to choose a drawing, then select its named glyph in Glyphs or use its private-use code from the included PlotFont JSON. &ldquo;Temporary&rdquo; describes this conversion: each drawing needs a reviewed character assignment before standard text mapping can replace these placeholders.</p>
    </details>''' if font['privateUseMappings'] else ''
    return f'''<article class="font-card" id="{key}" data-collection="{escape(font['collection'])}" data-search="{searchable}">
  <div class="font-specimen"><img src="assets/catalog/{key}.svg" alt="Stroke specimen for {escape(font['family'], quote=True)}" loading="lazy" width="600" height="150"></div>
  <div class="font-info">
    <div class="font-topline"><h3>{escape(font['family'])}</h3><span>{font['glyphs']} glyphs</span></div>
    <p class="font-license">{escape(font['license'])}</p>
    <div class="font-links"><a href="assets/catalog/{key}.zip" download>Download ZIP ↓</a><a href="{escape(font['source'], quote=True)}">Original repository ↗</a></div>
    {mapping}
    <details class="font-credits"><summary>Attribution & source</summary><pre>{escape(font['attribution'].strip())}</pre><div class="author-links">{links}<a href="{escape(font['sourceUrl'], quote=True)}">Pinned source ↗</a></div><p class="small-copy">Complete license notices and original source accompany this font in its ZIP.</p></details>
  </div>
</article>'''


def build(destination):
    destination = Path(destination).resolve()
    # A build never deletes or replaces another output.
    shutil.copytree(ROOT / 'site', destination)
    catalog = json.loads((destination / 'catalog.json').read_text())
    info = plistlib.loads((ROOT / 'plugins/PlotFont.glyphsFileFormat/Contents/Info.plist').read_bytes())
    version = info['CFBundleShortVersionString']
    template = (destination / 'index.html').read_text()
    for token, value in {
        '{{FONT_COUNT}}': str(len(catalog['fonts'])),
        '{{PLUGIN_VERSION}}': version,
        '{{CATALOG}}': '\n'.join(font_card(font) for font in catalog['fonts']),
    }.items():
        template = template.replace(token, value)
    (destination / 'index.html').write_text(template, encoding='utf-8')
    (destination / 'README.md').unlink()
    (destination / '.nojekyll').touch()
    downloads = destination / 'downloads'
    downloads.mkdir()
    # Build beside the site, so the unpacked executable isn't part of Pages.
    bundle = build_plugin(destination.parent / (destination.name + '-plugin') / 'PlotFont.glyphsFileFormat')
    with zipfile.ZipFile(downloads / f'PlotFont-Glyphs-{version}.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(bundle.rglob('*')):
            if path.is_file():
                info = zipfile.ZipInfo.from_file(path, str(path.relative_to(bundle.parent)))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
    print(f'{len(catalog["fonts"])} fonts; Glyphs plugin {version}; {destination}')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / 'output/website')
    build(parser.parse_args().destination)
