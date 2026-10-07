"""Run with public Glyphs CLI -i for each package, in catalog order.

First --phase save loads prepared packages; a separate --phase reopen process
loads saved native copies. Glyphs native saves quantize coordinates to 0.001 FU;
reopened comparison allows 0.000501 FU per numeric value.

Loads only generated packages; saves new native copies and exports. Never uses
or changes a GUI document. GUI bridge qualification is a separate operation.
"""
import argparse
import json
from pathlib import Path
import sys

from GlyphsApp import Glyphs, LINE, CURVE, QCURVE, OFFCURVE

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from openplotfont.glyphs_export import export_font
from openplotfont.comparison import compare_fonts
from openplotfont.validation import validate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', nargs='*')
    parser.add_argument('--phase', choices=['save', 'reopen'], required=True)
    parser.add_argument('--destination', type=Path, default=ROOT / 'output/font-library/native')
    args = parser.parse_args()
    destination = args.destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((ROOT / 'output/font-library/fonts/catalog.json').read_text())
    reports = []
    node_types = {'line': LINE, 'curve': CURVE, 'qcurve': QCURVE, 'offcurve': OFFCURVE}
    rows = [r for r in catalog['fonts'] if not args.only or r['id'] in args.only]
    loaded = list(Glyphs.fonts)
    if len(loaded) != len(rows):
        raise ValueError('Pass each selected package with CLI -i, in catalog order')
    for row, font in zip(rows, loaded):
        if args.only and row['id'] not in args.only:
            continue
        try:
            native_path = destination / (row['id'] + '.glyphspackage')
            json_path = destination / (row['id'] + '.opf.json')
            if args.phase == 'save' and (native_path.exists() or json_path.exists()):
                raise FileExistsError('Qualification destination exists; use a new directory')
            expected = json.loads((ROOT / row['openplotfont']).read_text())
            if font.familyName != row['family']:
                raise ValueError('CLI input order/family mismatch')
            actual = export_font(font, font.masters[0].id, node_types)
            actual['version'] = '0.3'
            validate(actual)
            tolerance = 1e-8 if args.phase == 'save' else 0.000501
            compare_fonts(expected, actual, tolerance=tolerance)
            if args.phase == 'save':
                font.save(str(native_path))
            json_path.write_text(json.dumps(actual, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
            reports.append({'id': row['id'], 'status': 'pass', 'glyphs': len(actual['glyphs']),
                            'kerningPairs': len(actual['kerning']), 'package': str(native_path.relative_to(ROOT)),
                            'openplotfont': str(json_path.relative_to(ROOT)),
                            'maximumComparisonToleranceFontUnits': tolerance})
        except Exception as error:
            reports.append({'id': row['id'], 'status': 'failed', 'error': str(error)})
        (destination / ('qualification-' + args.phase + '.json')).write_text(json.dumps({'host': 'Glyphs CLI with /Applications/Glyphs 4.app',
            'phase': args.phase, 'version': str(Glyphs.versionString), 'build': str(Glyphs.buildNumber), 'fonts': reports}, indent=2)+'\n')
        print(row['id'], reports[-1]['status'], reports[-1].get('error', ''), flush=True)
    if any(r['status'] != 'pass' for r in reports):
        raise SystemExit(1)


if __name__ == '__main__': main()
