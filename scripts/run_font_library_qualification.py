"""Qualify generated packages with the installed public Glyphs CLI, in two runs."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--glyphs-command', default=shutil.which('glyphs'))
    parser.add_argument('--app', default='/Applications/Glyphs 4.app')
    parser.add_argument('--destination', type=Path, default=ROOT / 'output/font-library/native')
    args = parser.parse_args()
    if not args.glyphs_command:
        raise SystemExit('Specify the installed public CLI with --glyphs-command')
    rows = json.loads((ROOT / 'output/font-library/fonts/catalog.json').read_text())['fonts']
    for phase in ['save', 'reopen']:
        command = [args.glyphs_command, 'run', '--app', args.app, '--plugins', '', str(ROOT / 'scripts/qualify_font_library.py')]
        for row in rows:
            path = ROOT / row['package'] if phase == 'save' else args.destination.resolve() / (row['id'] + '.glyphspackage')
            command += ['-i', str(path)]
        command += ['--', '--phase', phase, '--destination', str(args.destination.resolve())]
        subprocess.run(command, check=True, cwd=ROOT)


if __name__ == '__main__': main()
