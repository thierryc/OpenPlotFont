"""Build reviewed sources into OpenPlotFont 0.3, format-4 Glyphs packages and SVGs.

Fetch first with fetch_font_library.py. Existing output is never overwritten.
Optional build dependencies: FontTools and openstep-plist.
"""
import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from openplotfont.comparison import compare_fonts
from openplotfont.glyphs_package import write_package, read_package
from openplotfont.hershey import parse_jhf, ASCII_NAMES, FACES, import_hershey
from openplotfont.render import render_svg
from openplotfont.stroke_import import import_svg, import_lff, fallback, font_record

SOURCES = ROOT / 'output/font-library/sources'


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def metadata(path, manifests, license_name, notice, repository):
    source = manifests[str(path.relative_to(ROOT))]
    if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
        raise ValueError('Source digest differs from the reviewed lock')
    return {'source': repository, 'sourceFile': str(path.relative_to(SOURCES)),
            'sourceRevision': source['revision'], 'sourceUrl': source['url'],
            'sourceSha256': source['sha256'], 'license': license_name,
            'attribution': notice, 'conversion': 'OpenPlotFont format conversion; source drawing order and pen lifts retained'}


def hershey(path, manifests):
    stem = path.stem
    names = {'futural': 'Futural', 'futuram': 'Futuram', 'timesr': 'Roman Complex', 'timesi': 'Roman Italic',
             'timesrb': 'Roman Bold', 'timesib': 'Roman Bold Italic', 'scriptc': 'Script Complex',
             'scripts': 'Script Simplex', 'rowmans': 'Roman Simplex', 'rowmand': 'Roman Duplex', 'rowmant': 'Roman Triplex'}
    family = 'Hershey ' + names.get(stem, stem.replace('_', ' ').title())
    notice = 'Glyph data: Dr. A. V. Hershey; JHF representation: James Hurt, Cognition, Inc. See HERSHEY-NOTICE.txt for the complete required acknowledgments and use restriction.'
    meta = metadata(path, manifests, 'Hershey permissive terms; not MIT', notice, 'https://github.com/kamalmostafa/hershey-fonts')
    meta['authorLinks'] = ['https://github.com/kamalmostafa/hershey-fonts']
    latin = stem in {'futural', 'futuram', 'timesr', 'timesi', 'timesrb', 'timesib', 'scriptc', 'scripts',
                     'rowmans', 'rowmand', 'rowmant', 'cursive', 'gothgbt', 'gothiceng', 'gothgrt', 'gothicger', 'gothitt', 'gothicita'}
    records = parse_jhf(path.read_text(encoding='ascii'))
    baseline, cap = 9, 21
    if latin:
        h = records[ord('H') - 32]
        ys = [y for s in h['strokes'] for _, y in s]
        baseline, cap = max(ys), max(ys) - min(ys)
    all_y = [(baseline - y) * 50 for r in records for s in r['strokes'] for _, y in s]
    glyphs = [fallback(1470)]
    for row, record in enumerate(records):
        code = row + 32 if latin and row < 95 else (0xE000 + row if not latin else None)
        glyphs.append({'name': ASCII_NAMES[code] if code in ASCII_NAMES else f'hershey.{row:03d}.{record["sourceId"]}',
                       'unicodes': [f'{code:04X}'] if code is not None else [],
                       'advanceWidth': (record['right'] - record['left']) * 50,
                       'strokes': [{'closed': False, 'commands': [['M' if i == 0 else 'L', (x - record['left']) * 50,
                                   (baseline - y) * 50] for i, (x, y) in enumerate(s)]} for s in record['strokes']],
                       'userData': {'org.openplotfont.hershey': {'row': row, 'sourceId': record['sourceId']}}})
    if not latin:
        glyphs.append({'name': 'space', 'unicodes': ['0020'], 'advanceWidth': 500, 'strokes': []})
    meta.update(mapping=('Rows 0–94 -> printable ASCII; final row retained unencoded' if latin else
                         'Explicit temporary private-use mapping: U+E000+source row. Standard Greek/Cyrillic/Japanese/symbol Unicode mapping is NOT qualified.'),
                coordinateTransform={'sourceBaselineY': baseline, 'scale': 50, 'yAxis': 'up'})
    return font_record('hershey-' + stem, family, 1470,
                       {'ascender': max(max(all_y), cap * 50), 'descender': min(0, min(all_y)),
                        'capHeight': cap * 50, 'xHeight': cap * 25, 'lineGap': 210}, glyphs, meta)


def glyph_atlas(font):
    """Show every source glyph, including unencoded and PUA drawings."""
    count = len(font['glyphs']); cols = 10; rows = (count + cols - 1) // cols
    cell = 22; scale = 8 / font['metrics']['capHeight']
    pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols*cell}mm" height="{rows*cell}mm" viewBox="0 0 {cols*cell} {rows*cell}">',
              '<rect width="100%" height="100%" fill="white"/>']
    for index, glyph in enumerate(font['glyphs']):
        x, y = index % cols * cell + 3, index // cols * cell + 12
        pieces.append(f'<text x="{x}" y="{y+8}" font-size="1.5">{escape(glyph["name"])}</text>')
        for op in glyph['strokes']:
            if op.get('kind', 'stroke') != 'stroke':
                raise ValueError('Stroke atlas cannot silently discard fills')
            d = []
            for c in op['commands']:
                vals = [(x + c[i]*scale, y - c[i+1]*scale) for i in range(1, len(c), 2)]
                d.append(c[0]+' '+ ' '.join(f'{a:.12g} {b:.12g}' for a,b in vals))
            if op['closed']: d.append('Z')
            pieces.append(f'<path d="{" ".join(d)}" fill="none" stroke="black" stroke-width="0.2" stroke-linecap="round"/>')
    return '\n'.join(pieces) + '\n</svg>\n'


def svg_notices(svg, font):
    notices = font['metadata']['attribution'] + '\n\n' + '\n\n'.join(n['text'] for n in font['metadata']['licenseNotices'])
    end = svg.index('>', svg.index('<svg')) + 1
    return svg[:end] + '\n<metadata>' + escape(notices) + '</metadata>' + svg[end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', type=Path, default=ROOT / 'output/font-library/fonts')
    parser.add_argument('--only-source', nargs='*')
    args = parser.parse_args()
    destination = args.destination.resolve()
    if destination.exists():
        raise SystemExit('Choose a new build destination; output is never overwritten')
    manifests = {x['path']: x for x in json.loads((SOURCES.parent / 'sources.json').read_text())}
    fonts, deferred = [], [{'source': 'https://github.com/cmiscm/leonsans', 'reason': 'Reviewed JS renderer uses filled circles for dots, alongside strokes. A pure-stroke conversion would change drawing intent; mixed-fill extraction is not implemented.'}]
    def build(path, font, notices, author_links=None):
        family = font['familyName']
        key = slug(family)
        folder = destination / key
        folder.mkdir(parents=True)
        font['metadata']['authorLinks'] = author_links or font['metadata'].get('authorLinks', [])
        notice_names = [('UPSTREAM-README.md' if Path(n).name == 'README.md' else Path(n).name) for n in notices]
        font['metadata']['licenseFiles'] = notice_names
        font['metadata']['licenseNotices'] = [{'filename': name, 'text': Path(n).read_text(encoding='utf-8-sig')} for n, name in zip(notices, notice_names)]
        font['metadata']['sourceIntentReview'] = 'Upstream explicitly identifies this source as stroke geometry; centerlines imported without outline recovery'
        for n, name in zip(notices, notice_names):
            shutil.copyfile(n, folder / name)
            if name == 'hershey-fonts.notes': shutil.copyfile(n, folder / 'HERSHEY-NOTICE.txt')
        shutil.copyfile(path, folder / ('SOURCE' + path.suffix))
        jsonpath = folder / (key + '.opf.json')
        jsonpath.write_text(json.dumps(font, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
        (folder / 'ATTRIBUTION.txt').write_text('OpenPlotFont conversion of ' + family + '\n\n' +
            font['metadata']['attribution'] + '\n\nOriginal source: ' + font['metadata']['sourceUrl'] +
            '\nSource revision: ' + font['metadata']['sourceRevision'] + '\nSource SHA-256: ' +
            font['metadata']['sourceSha256'] + '\n\nLicense: ' + font['metadata']['license'] +
            '\nRetain SOURCE and all license/notice files. Conversion does not relicense the font as project MIT.\n')
        package = folder / (key + '.glyphspackage')
        write_package(font, package)
        compare_fonts(font, read_package(package))
        mapped = [int(u, 16) for g in font['glyphs'] for u in g['unicodes']]
        text = 'Hamburgefontsiv 0123456789\nA O Q gjpq é Å @ & fi'
        if any(0xE000 <= u <= 0xF8FF for u in mapped):
            text = ''.join(chr(u) for u in mapped[:36])
        svg = folder / 'specimen.svg'
        svg.write_text(svg_notices(render_svg(font, text, cap_height_mm=8), font))
        (folder / 'glyph-atlas.svg').write_text(svg_notices(glyph_atlas(font), font))
        row = {'id': key, 'family': family, 'glyphs': len(font['glyphs']), 'unicodeMappings': len(mapped),
               'kerningPairs': len(font['kerning']), 'license': font['metadata']['license'],
               'source': font['metadata']['source'], 'sourceUrl': font['metadata']['sourceUrl'],
               'authorLinks': font['metadata']['authorLinks'], 'attribution': font['metadata']['attribution'],
               'openplotfont': str(jsonpath.relative_to(ROOT)), 'package': str(package.relative_to(ROOT)),
               'specimen': str(svg.relative_to(ROOT)), 'fontDigest': hashlib.sha256(jsonpath.read_bytes()).hexdigest(),
               'status': 'saved-package round trip passed; native qualification pending',
               'warnings': font['metadata'].get('importWarnings', [])}
        fonts.append(row)
        (folder / 'README.md').write_text(f'# {family}\n\nSource: [{font["metadata"]["source"]}]({font["metadata"]["source"]})\n\nLicense: {row["license"]}. Retain every accompanying notice and SOURCE file with redistribution.\n\n{row["attribution"]}\n\n' +
            '\n'.join(f'- [Author/source link]({url})' for url in row['authorLinks']) +
            f'\n\n{row["glyphs"]} glyphs; {row["unicodeMappings"]} scalar mappings; {row["kerningPairs"]} resolved kerning pairs.\n\n' +
            font['metadata'].get('mapping', '') + '\n\n' +
            'Independent strokes retain their order and pen lifts. No automatic script joining, stroke-width expansion, or device commands. This is geometry-only OpenPlotFont 0.3; retained unencoded alternates/ligatures have no automatic substitutions.\n')
    for path in sorted((SOURCES / 'hershey').glob('*.jhf')):
        if args.only_source and path.stem not in args.only_source: continue
        try: build(path, hershey(path, manifests), [SOURCES / 'hershey/hershey-fonts.notes'])
        except Exception as error: deferred.append({'source': str(path.relative_to(ROOT)), 'reason': str(error)})
    paths = sorted((SOURCES / 'oskay/fonts').rglob('*.svg')) + sorted((SOURCES / 'relief').glob('*.svg')) + sorted((SOURCES / 'norm').glob('*.svg')) + sorted((SOURCES / 'custom').glob('*.svg')) + sorted((SOURCES / 'cutlings').glob('*.svg')) + sorted((SOURCES / 'creative').glob('*.svg'))
    for path in paths:
        if args.only_source and path.stem not in args.only_source: continue
        if '_glyphTable' in path.name: continue
        try:
            root = ET.parse(path).getroot()
            face = root.find('.//{*}font-face')
            if face is None: raise ValueError('Not a reusable SVG font')
            family = 'PF ' + face.get('font-family', path.stem)
            notice = '\n'.join(''.join(m.itertext()).strip() for m in root.findall('.//{*}metadata'))
            if 'oskay' in path.parts:
                repository = 'https://gitlab.com/oskay/svg-fonts'
                notices = [SOURCES / 'oskay/fonts/EMS/OFL.txt'] if 'EMS' in path.parts else [SOURCES / 'hershey/hershey-fonts.notes']
                license_name = 'SIL OFL 1.1' if 'EMS' in path.parts else 'Hershey permissive terms; not MIT'
                source_font = re.search(r'Google font page:\s*(\S+)', notice)
                if source_font:
                    google_family = source_font[1].rsplit('/',1)[1].replace('+','').lower().replace('sourcesanspro','sourcesans3')
                    upstream_notice = SOURCES / 'google-notices' / (google_family + '.txt')
                    if upstream_notice.exists(): notices.append(upstream_notice)
                if path.name == 'EMSMistyNight.svg': notices.append(SOURCES / 'ancestor-notices/foglihten-OFL_License.txt')
                if path.name == 'EMSElfin.svg':
                    notices += [SOURCES / 'oskay/fonts/EMS/Elfin-ancestor-APACHE.txt', SOURCES / 'oskay/fonts/EMS/Elfin-ancestor-NOTICE.txt']
                    license_name += '; Apache 2.0 ancestor notice retained'
                if path.name == 'TwinSans.svg':
                    notices.append(SOURCES / 'oskay/fonts/EMS/OFL.txt')
                    license_name = 'SIL OFL 1.1; Hershey ancestor notice retained'
            elif 'relief' in path.parts:
                repository = 'https://github.com/isdat-type/Relief-SingleLine'; notices = [SOURCES / 'relief/OFL.txt', SOURCES / 'relief/AUTHORS.txt']; license_name = 'SIL OFL 1.1'
            elif 'norm' in path.parts:
                repository = 'https://github.com/octycs/norm-stroke'; notices = [SOURCES / 'norm/README.md']; license_name = 'CC0 1.0'
                notice += '\nNormStroke by octycs; based on Wikimedia ISO3098 Type B lettering. CC0 declaration retained.'
            elif 'custom' in path.parts:
                repository = 'https://github.com/Shriinivas/inkscapestrokefont'; notices = [SOURCES / 'custom/OFL.txt', SOURCES / 'custom/README.md']; license_name = 'SIL OFL 1.1'
                notices.append(SOURCES / ('ancestor-notices/pinyon-original-OFL.txt' if path.stem == 'Custom-Script' else 'ancestor-notices/square-grotesk-Copying.txt'))
                notice += '\nCustom stroke fonts by Shriinivas; derived from Square Grotesk and Pinyon Script as credited upstream. Font notice template has unfilled copyright fields; original declarations retained.'
            elif 'cutlings' in path.parts:
                repository = 'https://cutlings.datafil.no/stroke-fonts-singularis-dualis-pluralis/'; notices = [SOURCES / 'cutlings/readme.txt', SOURCES / 'oskay/fonts/EMS/OFL.txt']; license_name = 'SIL OFL 1.1'
                notice += '\nCutlings Singularis, Dualis and Pluralis by Ellen Wasbø; author credits and font license in readme.txt.'
            else:
                repository = 'https://www.eyesofpanda.com/project/dearplotter_font/'; notices = [SOURCES / 'oskay/fonts/EMS/OFL.txt']; license_name = 'SIL OFL 1.1 (font); CC BY-SA 4.0 generator/adaptation credits retained'
            links = re.findall(r'(?:Link:|Google font page:)\s*(https?://\S+)', notice)
            if path.name == 'TwinSans.svg': links.append('https://keithp.com/')
            if 'cutlings' in path.parts: links.append('https://cutlings.datafil.no/')
            if 'creative' in path.parts: links.append('https://www.eyesofpanda.com/')
            links += [repository]
            meta = metadata(path, manifests, license_name, notice, repository)
            font = import_svg(path, identity=slug(family), family=family, metadata=meta, stroke_source=True)
            build(path, font, notices, links)
        except Exception as error:
            deferred.append({'source': str(path.relative_to(ROOT)), 'reason': str(error)})
    for path in sorted((SOURCES / 'lff').glob('*.lff')):
        if args.only_source and path.stem not in args.only_source: continue
        try:
            if path.stem == 'kst32b':
                deferred.append({'source': str(path.relative_to(ROOT)), 'reason': 'Additional KST32B license terms need verification before redistribution.'}); continue
            family = 'PF CAD ' + path.stem
            license_name = 'SIL OFL 1.1' if 'opengost' in path.stem else 'GPL v2 or later'
            notice = '\n'.join(line for line in path.read_text().splitlines() if line.startswith('# Author:') or line.startswith('# License:'))
            meta = metadata(path, manifests, license_name, notice, 'https://github.com/LibreCAD/LibreCAD')
            licenses = [SOURCES / 'oskay/fonts/EMS/OFL.txt'] if 'opengost' in path.stem else [SOURCES / 'lff/GPL-2.0.txt']
            build(path, import_lff(path, identity=slug(family), family=family, metadata=meta), licenses, ['https://github.com/LibreCAD/LibreCAD'])
        except Exception as error: deferred.append({'source': str(path.relative_to(ROOT)), 'reason': str(error)})
    destination.mkdir(exist_ok=True)
    (destination / 'catalog.json').write_text(json.dumps({'fonts': fonts, 'deferred': deferred}, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(fonts)} converted; {len(deferred)} deferred/errors')
    for row in deferred: print(row['source'], row['reason'])


if __name__ == '__main__': main()
