"""Prepare a reviewable website catalog snapshot from the qualified local library.

Writes to output/ by default. Copy a reviewed snapshot into site/ for publication.
Native Glyphs qualification and packaging must have already completed.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination):
    base = ROOT / 'output/font-library'
    library = json.loads((base / 'fonts/catalog.json').read_text())
    report = json.loads((base / 'mcp/qualification.json').read_text())
    passed = {row['id'] for row in report['fonts'] if row['status'] == 'pass'}
    if passed != {row['id'] for row in library['fonts']}:
        raise ValueError('Every font must pass native save/reopen qualification before publication.')
    destination.mkdir(parents=True, exist_ok=False)
    assets = destination / 'assets/catalog'
    assets.mkdir(parents=True)
    rows = []
    for source in library['fonts']:
        key = source['id']
        font = json.loads((ROOT / source['openplotfont']).read_text())
        mapped = [int(code, 16) for glyph in font['glyphs'] for code in glyph['unicodes']]
        group = ('EMS' if key.startswith('pf-ems-') else
                 'Hershey' if 'hershey' in key or key == 'pf-twin-sans' else
                 'Relief' if key.startswith('pf-relief-') else
                 'CAD' if key.startswith('pf-cad-') else 'Independent')
        row = {field: source[field] for field in
               ('id', 'family', 'glyphs', 'license', 'source', 'sourceUrl', 'authorLinks', 'attribution')}
        row['collection'] = group
        row['privateUseMappings'] = key.startswith('hershey-') and any(0xE000 <= value <= 0xF8FF for value in mapped)
        row['assets'] = {}
        for field, suffix in [('specimen', '.svg'), ('bundle', '.zip')]:
            target = assets / (key + suffix)
            shutil.copy2(ROOT / source[field], target)
            row['assets'][field] = {'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                                    'bytes': target.stat().st_size}
        rows.append(row)
    # A handful of different styles introduce the collection, then alphabetical.
    featured = ['pf-ems-brush', 'pf-relief-singleline-svg', 'hershey-script-simplex', 'pf-norm-stroke']
    rows.sort(key=lambda row: (featured.index(row['id']) if row['id'] in featured else len(featured), row['family']))
    snapshot = {'prepared': '2026-10-01', 'qualification': {
        'hostVersion': report['hostVersion'], 'hostBuild': report['hostBuild'],
        'fontCount': len(passed), 'comparisonToleranceFontUnitsAfterNativeSave': report['comparisonToleranceFontUnitsAfterNativeSave'],
    }, 'fonts': rows}
    (destination / 'catalog.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(rows)} qualified font snapshots; {destination}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / 'output/website-catalog')
    prepare(parser.parse_args().destination)
