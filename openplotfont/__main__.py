"""Validate, render, shape, compare, attach layout, or import OpenPlotFont data."""

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
    render.add_argument('--profiles',choices=('appearance','centerline'),default='appearance')
    render.add_argument('--writing-mask',action='store_true')
    render.add_argument('--speed',type=float,default=20,help='Demonstration centerline speed in mm/s')
    render.add_argument('--pen-lift',type=float,default=0.15,help='Demonstration pen-up interval in seconds')
    fallback = sub.add_parser('centerlines',help='Explicitly remove pen profiles and export 0.3 centerlines')
    fallback.add_argument('font')
    fallback.add_argument('-o','--output',required=True)
    fallback.add_argument('--force',action='store_true')
    render.add_argument("--join", action="store_true")
    render.add_argument("--force", action="store_true")
    render.add_argument("--layout", choices=('simple','opentype'), default='simple')
    render.add_argument("--direction", choices=('ltr','rtl'), default='ltr')
    render.add_argument("--script", default='Latn')
    render.add_argument("--language", default='en')
    render.add_argument("--feature", action='append', default=[], metavar='TAG=VALUE')
    shape = sub.add_parser('shape', help='Shape one horizontal text run to JSON')
    shape.add_argument('font')
    shape.add_argument('text')
    shape.add_argument('-o','--output',required=True)
    shape.add_argument('--direction',choices=('ltr','rtl'),default='ltr')
    shape.add_argument('--script',default='Latn')
    shape.add_argument('--language',default='en')
    shape.add_argument('--feature',action='append',default=[],metavar='TAG=VALUE')
    shape.add_argument('--force',action='store_true')
    attach = sub.add_parser('attach-layout',help='Bind a verified compiled static OTF/TTF to OpenPlotFont geometry')
    attach.add_argument('font')
    attach.add_argument('opentype')
    attach.add_argument('--glyph-order',help='JSON array mapping each compiled glyph ID to a drawing name')
    attach.add_argument('--fea',help='Optional self-contained feature source, retained for authoring')
    attach.add_argument('-o','--output',required=True)
    attach.add_argument('--force',action='store_true')
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
                print(f"{path}: valid OpenPlotFont {font['version']} ({len(font['glyphs'])} glyphs)")
        elif args.command == "compare":
            compare_fonts(load(args.reference), load(args.export))
            print("Source and export semantics match.")
        elif args.command == "render":
            settings = parse_features(args.feature)
            write_output(args.output, render_svg(load(args.font), args.text, args.cap_height, join=args.join,
                         layout_mode=args.layout,direction=args.direction,script=args.script,
                         language=args.language,features=settings or None,profile_mode=args.profiles,writing_mask=args.writing_mask,speed_mm_s=args.speed,pen_lift_s=args.pen_lift), force=args.force, create_parents=True)
        elif args.command == 'centerlines':
            from .profiles import centerlines
            result = centerlines(load(args.font))
            write_font(args.output,result,force=args.force,create_parents=True)
            for warning in result.get('metadata',{}).get('exportWarnings',[]):
                print(warning)
        elif args.command == 'shape':
            from .shaping import shape_text
            run = shape_text(load(args.font),args.text,direction=args.direction,script=args.script,
                             language=args.language,features=parse_features(args.feature))
            write_output(args.output,json.dumps(run,indent=2)+'\n',force=args.force,create_parents=True)
        elif args.command == 'attach-layout':
            from .layout import attach_layout
            result = attach_layout(load(args.font),Path(args.opentype).read_bytes(),
                                   glyph_order=json.loads(Path(args.glyph_order).read_text()) if args.glyph_order else None,
                                   source=Path(args.fea).read_text() if args.fea else None)
            write_font(args.output,result,force=args.force,create_parents=True)
        else:
            write_font(args.output, import_hershey(args.source, args.face), force=args.force, create_parents=True)
    except (ValidationError, OSError, UnicodeError, json.JSONDecodeError) as error:
        parser.exit(1, f"openplotfont: {error}\n")


def parse_features(values):
    settings = {}
    for value in values:
        try:
            tag, number = value.split('=',1)
            if len(tag)!=4 or tag in settings or not number.isdecimal():
                raise ValueError()
            settings[tag] = int(number)
        except ValueError as error:
            raise ValidationError('features: expected unique TAG=unsigned-integer settings') from error
    return settings


if __name__ == "__main__":
    main()
