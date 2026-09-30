"""Structural and semantic validation with path-specific errors."""

import json
import math
import re
from pathlib import Path


class ValidationError(ValueError):
    pass


def require(condition, path, message):
    if not condition:
        raise ValidationError(f"{path}: {message}")


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def object_at(value, path):
    require(isinstance(value, dict), path, "expected object")
    return value


def array_at(value, path):
    require(isinstance(value, list), path, "expected array")
    return value


def text(value, path):
    require(isinstance(value, str) and bool(value), path, "expected nonempty string")


def json_value(value, path="$", depth=0):
    require(depth <= 64, path, "JSON nesting exceeds 64 levels")
    if isinstance(value, dict):
        for key, item in value.items():
            require(isinstance(key, str), path, "object keys must be strings")
            json_value(item, f"{path}.{key}", depth + 1)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            json_value(item, f"{path}[{i}]", depth + 1)
    else:
        require(value is None or type(value) in (str, bool) or number(value),
                path, "expected JSON value with finite numbers")


def path_record(record, path):
    object_at(record, path)
    require(type(record.get("closed")) is bool, path + ".closed", "expected boolean")
    commands = array_at(record.get("commands"), path + ".commands")
    require(2 <= len(commands) <= 100000, path, "expected 2–100000 commands")
    for i, command in enumerate(commands):
        at = f"{path}.commands[{i}]"
        array_at(command, at)
        require(bool(command) and isinstance(command[0], str), at, "expected command name")
        arity = {"M": 3, "L": 3, "Q": 5, "C": 7}.get(command[0])
        require(arity is not None, at, "unsupported command")
        require(len(command) == arity, at, "wrong command arity")
        require((command[0] == "M") == (i == 0), at, "M must occur exactly once, first")
        require(all(number(n) for n in command[1:]), at, "coordinates must be finite numbers")


def validate(font):
    """Return the original object unchanged or raise ValidationError."""
    object_at(font, "$")
    json_value(font)
    require(font.get("format") == "PlotFont", "$.format", "expected PlotFont")
    require(font.get("version") in ("0.2", "0.3"), "$.version", "unsupported version; expected 0.2 or 0.3")
    require("layout" not in font or font["version"] == "0.3", "$.layout", "layout requires version 0.3")
    for key in ("id", "familyName", "styleName", "missingGlyph"):
        text(font.get(key), "$." + key)
    upm = font.get("unitsPerEm")
    require(type(upm) is int and upm > 0, "$.unitsPerEm", "expected positive integer")
    metrics = object_at(font.get("metrics"), "$.metrics")
    for key in ("ascender", "descender", "capHeight", "xHeight", "lineGap"):
        require(number(metrics.get(key)), "$.metrics." + key, "expected finite number")
    require(metrics["ascender"] > 0 and metrics["capHeight"] > 0, "$.metrics", "ascender/capHeight must be positive")
    require(metrics["descender"] <= 0 and metrics["xHeight"] >= 0 and metrics["lineGap"] >= 0,
            "$.metrics", "invalid descender, xHeight, or lineGap")
    if "metadata" in font:
        object_at(font["metadata"], "$.metadata")
    glyphs = array_at(font.get("glyphs"), "$.glyphs")
    require(1 <= len(glyphs) <= 100000, "$.glyphs", "expected 1–100000 glyphs")
    names, scalars = set(), set()
    total_commands = 0
    for i, glyph in enumerate(glyphs):
        at = f"$.glyphs[{i}]"
        object_at(glyph, at)
        name = glyph.get("name")
        text(name, at + ".name")
        require(name not in names, at, "duplicate glyph name")
        names.add(name)
        for u in array_at(glyph.get("unicodes"), at + ".unicodes"):
            require(isinstance(u, str) and re.fullmatch(r"[0-9A-F]{4,6}", u), at, "invalid Unicode encoding")
            scalar = int(u, 16)
            require(scalar <= 0x10FFFF and not 0xD800 <= scalar <= 0xDFFF and u == f"{scalar:04X}",
                    at, "Unicode must be a canonical scalar value")
            require(scalar not in scalars, at, "duplicate Unicode mapping")
            scalars.add(scalar)
        require(number(glyph.get("advanceWidth")) and glyph["advanceWidth"] >= 0, at, "invalid advanceWidth")
        operations = array_at(glyph.get("strokes"), at + ".strokes")
        require(len(operations) <= 100000, at, "too many operations")
        for j, operation in enumerate(operations):
            op_at = f"{at}.strokes[{j}]"
            object_at(operation, op_at)
            kind = operation.get("kind", "stroke")
            require(kind in ("stroke", "fill"), op_at, "unsupported operation kind")
            if kind == "stroke":
                require("contours" not in operation and "fillRule" not in operation, op_at, "mixed stroke/fill fields")
                records = [operation]
            else:
                require("commands" not in operation and "closed" not in operation, op_at, "mixed stroke/fill fields")
                require(operation.get("fillRule") in ("evenodd", "nonzero"), op_at, "unsupported fill rule")
                records = array_at(operation.get("contours"), op_at + ".contours")
                require(1 <= len(records) <= 100000, op_at, "fill needs closed contours")
            for k, record in enumerate(records):
                record_at = op_at if kind == "stroke" else f"{op_at}.contours[{k}]"
                path_record(record, record_at)
                total_commands += len(record["commands"])
                require(total_commands <= 1000000, "$", "font exceeds one million commands")
                if kind == "fill":
                    require(record["closed"], record_at, "fill contour must be closed")
        for side, ref in object_at(glyph.get("connections", {}), at + ".connections").items():
            require(side in ("entry", "exit"), at, "unknown connection side")
            object_at(ref, at + ".connections." + side)
            index = ref.get("strokeIndex")
            require(type(index) is int and 0 <= index < len(operations), at, "invalid connection strokeIndex")
            require(index == (0 if side == "entry" else len(operations) - 1), at, "connection must reference first/last operation")
            require(ref.get("endpoint") == ("start" if side == "entry" else "end"), at, "invalid connection endpoint")
            op = operations[index]
            require(op.get("kind", "stroke") == "stroke" and not op["closed"], at, "connection requires open stroke")
            if "userData" in ref:
                object_at(ref["userData"], at + ".connections." + side + ".userData")
        anchors = array_at(glyph.get("anchors", []), at + ".anchors")
        anchor_names = set()
        for anchor in anchors:
            object_at(anchor, at + ".anchors")
            text(anchor.get("name"), at + ".anchors.name")
            require(anchor["name"] not in anchor_names, at, "duplicate anchor name")
            anchor_names.add(anchor["name"])
            require(number(anchor.get("x")) and number(anchor.get("y")), at, "invalid anchor coordinates")
            if "userData" in anchor:
                object_at(anchor["userData"], at + ".anchors.userData")
        if "userData" in glyph:
            object_at(glyph["userData"], at + ".userData")
    require(font["missingGlyph"] in names, "$.missingGlyph", "fallback glyph does not exist")
    pairs = set()
    for i, pair in enumerate(array_at(font.get("kerning", []), "$.kerning")):
        at = f"$.kerning[{i}]"
        object_at(pair, at)
        for key in ("left", "right"):
            text(pair.get(key), at + "." + key)
            require(pair[key] in names, at, "kerning references unknown glyph")
        identity = (pair["left"], pair["right"])
        require(identity not in pairs, at, "duplicate kerning pair")
        pairs.add(identity)
        require(number(pair.get("value")), at, "invalid kerning value")
    if "layout" in font:
        from .layout import validate_layout
        validate_layout(font)
    return font


def _pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "$", f"duplicate JSON property {key!r}")
        result[key] = value
    return result


def load(path):
    source = Path(path)
    require(source.stat().st_size <= 32 * 1024 * 1024, "$", "font exceeds 32 MiB")
    try:
        return validate(json.loads(source.read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                                   parse_constant=lambda value: require(False, "$", f"invalid number {value}")))
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise ValidationError(f"{source}: invalid UTF-8 JSON: {error}") from error
