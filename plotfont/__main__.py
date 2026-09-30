"""python -m plotfont validate|render|import-hershey"""

import argparse
import json
from pathlib import Path

from . import load, render_svg, ValidationError
from .hershey import import_roman_simplex


def write(path, content, force=False):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w" if force else "x", encoding="utf-8") as stream:
        stream.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("fonts", nargs="+")
    render = sub.add_parser("render")
    render.add_argument("font")
    render.add_argument("text")
    render.add_argument("-o", "--output", required=True)
    render.add_argument("--cap-height", type=float, default=12)
    render.add_argument("--join", action="store_true")
    render.add_argument("--force", action="store_true")
    convert = sub.add_parser("import-hershey")
    convert.add_argument("source")
    convert.add_argument("-o", "--output", required=True)
    convert.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            for path in args.fonts:
                font = load(path)
                print(f"{path}: valid PlotFont 0.2 ({len(font['glyphs'])} glyphs)")
        elif args.command == "render":
            write(args.output, render_svg(load(args.font), args.text, args.cap_height, join=args.join), args.force)
        else:
            write(args.output, json.dumps(import_roman_simplex(args.source), indent=2, ensure_ascii=False, allow_nan=False) + "\n", args.force)
    except (ValidationError, OSError) as error:
        parser.exit(1, f"plotfont: {error}\n")


if __name__ == "__main__":
    main()
