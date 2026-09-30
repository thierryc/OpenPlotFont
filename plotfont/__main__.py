"""python -m plotfont validate|render|import-hershey"""

import argparse
import json
from pathlib import Path

from . import load, render_svg, ValidationError
from .hershey import FACES, import_hershey
from .storage import write_output, write_font
from .comparison import compare_fonts



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("fonts", nargs="+")
    compare = sub.add_parser("compare")
    compare.add_argument("reference")
    compare.add_argument("export")
    render = sub.add_parser("render")
    render.add_argument("font")
    render.add_argument("text")
    render.add_argument("-o", "--output", required=True)
    render.add_argument("--cap-height", type=float, default=12)
    render.add_argument("--join", action="store_true")
    render.add_argument("--force", action="store_true")
    convert = sub.add_parser("import-hershey")
    convert.add_argument("source")
    convert.add_argument("--face", choices=tuple(FACES), default="roman-simplex")
    convert.add_argument("-o", "--output", required=True)
    convert.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            for path in args.fonts:
                font = load(path)
                print(f"{path}: valid PlotFont 0.2 ({len(font['glyphs'])} glyphs)")
        elif args.command == "compare":
            compare_fonts(load(args.reference), load(args.export))
            print("Source and export semantics match.")
        elif args.command == "render":
            write_output(args.output, render_svg(load(args.font), args.text, args.cap_height, join=args.join), force=args.force, create_parents=True)
        else:
            write_font(args.output, import_hershey(args.source, args.face), force=args.force, create_parents=True)
    except (ValidationError, OSError, UnicodeError) as error:
        parser.exit(1, f"plotfont: {error}\n")


if __name__ == "__main__":
    main()
