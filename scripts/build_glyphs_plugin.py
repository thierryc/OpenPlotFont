"""Build the self-contained Glyphs 4 exporter from current repository sources."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(destination):
    destination = Path(destination)
    # Preserve existing builds; choose a fresh output directory per revision.
    shutil.copytree(ROOT / 'plugins/PlotFont.glyphsFileFormat', destination,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    resources = destination / 'Contents/Resources'
    package = resources / '_plotfont_glyphs4'
    package.mkdir()
    (package / '__init__.py').write_text('"""Private PlotFont exporter runtime."""\n')
    for name in ('glyphs_plugin', 'glyphs_export', 'validation', 'storage'):
        shutil.copy2(ROOT / 'plotfont' / (name + '.py'), package)
    shutil.copy2(ROOT / 'LICENSE', resources / 'PlotFont-LICENSE.txt')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path,
                        default=ROOT / 'output/build/PlotFont.glyphsFileFormat')
    args = parser.parse_args()
    print(build(args.destination))
