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
    mapping = '<p class="mapping-note">Temporary private-use mappings · see the included glyph atlas.</p>' if font['privateUseMappings'] else ''
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
