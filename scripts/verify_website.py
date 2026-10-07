"""Verify the deployable static site, attributed font payloads, and plugin ZIP."""
import argparse
import hashlib
import json
import plistlib
import re
import stat
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.cards = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for name in ('href', 'src'):
            if name in attrs:
                self.links.append(attrs[name])
        if tag == 'article' and 'font-card' in attrs.get('class', '').split():
            self.cards.append(attrs['id'])


def verify(destination):
    destination = destination.resolve()
    page = Page()
    document = (destination / 'index.html').read_text()
    page.feed(document)
    assert not re.search(r'\{\{\w+\}\}', document), 'Unrendered template token'
    assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML id'
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            assert url.scheme in ('http', 'https'), f'Unexpected link scheme: {link}'
            continue
        assert not url.path.startswith('/'), f'Root-relative link breaks project Pages: {link}'
        if url.path:
            target = (destination / unquote(url.path)).resolve()
            assert target.is_relative_to(destination) and target.is_file(), f'Missing local link: {link}'
        elif url.fragment:
            assert unquote(url.fragment) in page.ids, f'Missing anchor: {link}'
    catalog = json.loads((destination / 'catalog.json').read_text())
    # Verify the official published runtime, including its transitive browser
    # imports, instead of accepting a similarly named local reimplementation.
    vendor = destination / 'vendor/gl-marquee'
    source = json.loads((vendor / 'SOURCE.json').read_text())
    package = json.loads((vendor / 'package.json').read_text())
    assert package['name'] == source['package'] == '@ap.cx/gl-marquee'
    assert package['version'] == source['version'] == '0.1.0'
    for filename, digest in source['files'].items():
        asset = vendor / filename
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == digest, f'Changed official marquee file: {filename}'
        if asset.suffix == '.js':
            for imported in re.findall(r'from\s+[\'"]([^\'"]+)[\'"]', asset.read_text()):
                assert imported.startswith('./') and (asset.parent / imported).is_file(), f'Missing browser module: {imported}'
    font_source = json.loads((destination / 'assets/fonts/SOURCE.json').read_text())
    font = destination / 'assets/fonts/SquareBotSans-Regular.woff2'
    assert hashlib.sha256(font.read_bytes()).hexdigest() == font_source['sha256'], 'Changed footer font'
    assert 'SIL OPEN FONT LICENSE Version 1.1' in (font.parent / 'OFL.txt').read_text()
    assert set(page.cards) == {font['id'] for font in catalog['fonts']}, 'Catalog/HTML mismatch'
    assert len(page.cards) == catalog['qualification']['fontCount'], 'Qualification count mismatch'
    for font in catalog['fonts']:
        key = font['id']
        assert font['license'] and font['attribution'] and font['authorLinks'], f'Missing credits: {key}'
        for kind, suffix in [('specimen', '.svg'), ('bundle', '.zip')]:
            path = destination / f'assets/catalog/{key}{suffix}'
            assert hashlib.sha256(path.read_bytes()).hexdigest() == font['assets'][kind]['sha256'], f'Changed asset: {key}{suffix}'
        svg = ElementTree.parse(destination / f'assets/catalog/{key}.svg')
        assert svg.find('{http://www.w3.org/2000/svg}metadata') is not None, f'Missing SVG notices: {key}'
        with zipfile.ZipFile(destination / f'assets/catalog/{key}.zip') as archive:
            assert archive.testzip() is None, f'Corrupt ZIP: {key}'
            names = archive.namelist()
            assert any(name.endswith('/README.md') for name in names), f'Missing font credits: {key}'
            assert any(name.startswith(f'{key}/SOURCE.') for name in names), f'Missing original source: {key}'
            assert any('.glyphspackage/fontinfo.plist' in name for name in names), f'Missing Glyphs source: {key}'
            original = json.loads(archive.read(f'{key}/{key}.opf.json'))
            assert original['metadata'].get('licenseNotices'), f'Missing font license notices: {key}'
            assert len(original['glyphs']) == font['glyphs'], f'Glyph count mismatch: {key}'
    info = plistlib.loads((ROOT / 'plugins/OpenPlotFont.glyphsFileFormat/Contents/Info.plist').read_bytes())
    version = info['CFBundleShortVersionString']
    with zipfile.ZipFile(destination / f'downloads/OpenPlotFont-Glyphs-{version}.zip') as archive:
        prefix = 'OpenPlotFont.glyphsFileFormat/Contents/'
        assert archive.testzip() is None, 'Corrupt plugin ZIP'
        for module in ('glyphs_plugin', 'glyphs_export', 'validation', 'storage'):
            assert archive.read(prefix + f'Resources/_openplotfont_glyphs4/{module}.py') == (ROOT / f'openplotfont/{module}.py').read_bytes(), f'Stale plugin {module}'
        assert archive.read(prefix + 'Resources/OpenPlotFont-LICENSE.txt') == (ROOT / 'LICENSE').read_bytes()
        assert archive.read(prefix + 'Resources/GlyphsSDK-LICENSE.txt')
        loader = archive.getinfo(prefix + 'MacOS/plugin')
        assert stat.S_IMODE(loader.external_attr >> 16) & stat.S_IXUSR, 'Plugin loader is not executable'
    print(f'Website verified: {len(page.cards)} fonts, credits, source/license bundles, relative links and plugin {version}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / 'output/website')
    verify(parser.parse_args().destination)
