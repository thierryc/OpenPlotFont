"""Reference SVG preview. Filled areas are retained, never converted to toolpaths."""

import math
from html import escape

from .validation import validate, number, ValidationError


def render_svg(font, text, cap_height_mm=12, *, join=False, margin_mm=2, stroke_width_mm=0.3):
    validate(font)
    for label, value in (("cap height", cap_height_mm), ("margin", margin_mm), ("preview width", stroke_width_mm)):
        if not number(value) or value < 0 or (label != "margin" and value == 0):
            raise ValidationError(f"{label}: invalid physical size")
    if not isinstance(text, str) or len(text) > 100000:
        raise ValidationError("text: expected string of at most 100000 scalars")
    if "\t" in text:
        raise ValidationError("text: tabs require an explicit layout policy")
    def xml_text(value):
        if any(not (ord(c) in (9, 10, 13) or 0x20 <= ord(c) <= 0xD7FF
                       or 0xE000 <= ord(c) <= 0xFFFD or 0x10000 <= ord(c) <= 0x10FFFF) for c in value):
            raise ValidationError("SVG: text or glyph name contains an invalid XML character")
    xml_text(text)
    for glyph in font["glyphs"]:
        xml_text(glyph["name"])
    scale = cap_height_mm / font["metrics"]["capHeight"]
    glyphs = {g["name"]: g for g in font["glyphs"]}
    mapping = {int(u, 16): g for g in font["glyphs"] for u in g["unicodes"]}
    kerning = {(p["left"], p["right"]): p["value"] for p in font.get("kerning", [])}
    line_height = font["metrics"]["ascender"] - font["metrics"]["descender"] + font["metrics"]["lineGap"]
    rows = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    drawings = []
    bounds_x = [0]
    bounds_y = [-font["metrics"]["ascender"] * scale,
                ((len(rows) - 1) * line_height - font["metrics"]["descender"]) * scale]
    total_commands = 0

    def transform(commands, x, baseline):
        result = []
        for command in commands:
            values = []
            for i in range(1, len(command), 2):
                px, py = (x + command[i]) * scale, (baseline - command[i + 1]) * scale
                if not math.isfinite(px) or not math.isfinite(py):
                    raise ValidationError("layout: coordinate overflow")
                bounds_x.append(px)
                bounds_y.append(py)
                values.extend((px, py))
            result.append([command[0], *values])
        return result

    for row, line in enumerate(rows):
        x = 0
        previous = None
        previous_mapped = False
        for scalar in line:
            mapped = ord(scalar) in mapping
            glyph = mapping.get(ord(scalar), glyphs[font["missingGlyph"]])
            if previous:
                x += kerning.get((previous["name"], glyph["name"]), 0)
            for index, operation in enumerate(glyph["strokes"]):
                kind = operation.get("kind", "stroke")
                records = [operation] if kind == "stroke" else operation["contours"]
                total_commands += sum(len(r["commands"]) for r in records)
                if total_commands > 1000000:
                    raise ValidationError("layout: drawing exceeds one million commands")
                paths = [(transform(r["commands"], x, row * line_height), r["closed"]) for r in records]
                can_join = (join and kind == "stroke" and index == 0 and previous and mapped and previous_mapped
                            and scalar != " " and previous["name"] != "space"
                            and "exit" in previous.get("connections", {})
                            and "entry" in glyph.get("connections", {})
                            and drawings and drawings[-1]["kind"] == "stroke")
                if can_join:
                    last = drawings[-1]["paths"][-1][0][-1][-2:]
                    first = paths[0][0][0][-2:]
                    if math.dist(last, first) > 1e-9:
                        raise ValidationError(f"join {previous['name']} → {glyph['name']}: endpoints differ; connector policy required")
                    drawings[-1]["paths"][-1][0].extend(paths[0][0][1:])
                else:
                    drawings.append({"kind": kind, "paths": paths, "fillRule": operation.get("fillRule"), "glyph": glyph["name"]})
            x += glyph["advanceWidth"]
            bounds_x.append(x * scale)
            previous = glyph
            previous_mapped = mapped and scalar != " "
    # Control-point hulls conservatively bound Bézier curves without flattening.
    pad = margin_mm + stroke_width_mm / 2
    left, top = min(bounds_x) - pad, min(bounds_y) - pad
    width, height = max(bounds_x) - left + pad, max(bounds_y) - top + pad
    if not all(math.isfinite(v) for v in (left, top, width, height)):
        raise ValidationError("layout: document size overflow")

    def fmt(n):
        return format(n, ".12g")

    elements = []
    for drawing in drawings:
        pieces = []
        for commands, closed in drawing["paths"]:
            pieces.extend(c[0] + " " + " ".join(fmt(v) for v in c[1:]) for c in commands)
            if closed:
                pieces.append("Z")
        attributes = (f'fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round" stroke-width="{fmt(stroke_width_mm)}"'
                      if drawing["kind"] == "stroke"
                      else f'fill="black" stroke="none" fill-rule="{drawing["fillRule"]}"')
        elements.append(f'  <path data-glyph="{escape(drawing["glyph"], quote=True)}" {attributes} d="{" ".join(pieces)}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(width)}mm" height="{fmt(height)}mm" '
            f'viewBox="{fmt(left)} {fmt(top)} {fmt(width)} {fmt(height)}">\n'
            f'  <title>{escape(text)}</title>\n' + "\n".join(elements) + "\n</svg>\n")
