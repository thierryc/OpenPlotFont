"""Parse the pinned James Hurt JHF representation; preserve every source record."""

import hashlib
from pathlib import Path

from .validation import ValidationError, validate

REVISION = "1356bf2f83d380fcef68c887e88675eb9d445d86"
SOURCE_SHA256 = "8718fb129c0f6bce89c84fe41bc467e39534d215a6f7c3220cc5789a8a7d8618"
SOURCE = "https://github.com/kamalmostafa/hershey-fonts"


def parse_jhf(source):
    records = []
    for row, line in enumerate(source.splitlines()):
        try:
            identity, count = int(line[:5]), int(line[5:8])
        except ValueError as error:
            raise ValidationError(f"JHF row {row + 1}: invalid header") from error
        data = line[8:]
        if len(data) != count * 2 or count < 1:
            raise ValidationError(f"JHF row {row + 1}: coordinate count mismatch")
        left, right = (ord(c) - ord("R") for c in data[:2])
        strokes, current = [], []
        for i in range(2, len(data), 2):
            pair = data[i:i + 2]
            if pair == " R":
                if current:
                    strokes.append(current)
                current = []
            else:
                current.append([ord(pair[0]) - ord("R"), ord(pair[1]) - ord("R")])
        if current:
            strokes.append(current)
        if right < left or any(len(s) < 2 for s in strokes):
            raise ValidationError(f"JHF row {row + 1}: invalid advance or stationary stroke")
        records.append({"sourceId": identity, "left": left, "right": right, "strokes": strokes})
    return records


def import_roman_simplex(path):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValidationError("Roman Simplex source differs from the pinned upstream data; provenance would be incorrect")
    records = parse_jhf(raw.decode("ascii"))
    if len(records) != 96:
        raise ValidationError("Roman Simplex source must contain all 96 records")
    # Source capitals run y=-12..9. Baseline 9; exactly 1000/21 font units per coordinate.
    scale = 1000 / 21
    glyphs = [{"name": ".notdef", "unicodes": [], "advanceWidth": 600,
               "strokes": [{"closed": True, "commands": [["M", 50, 0], ["L", 50, 1000], ["L", 550, 1000], ["L", 550, 0]]}]}]
    for row, record in enumerate(records):
        code = row + 32
        glyphs.append({
            "name": "space" if code == 32 else (f"uni{code:04X}" if code <= 126 else "hershey.extra.95"),
            "unicodes": [f"{code:04X}"] if code <= 126 else [],
            "advanceWidth": (record["right"] - record["left"]) * scale,
            "strokes": [{"closed": False, "commands": [
                ["M" if i == 0 else "L", (x - record["left"]) * scale, (9 - y) * scale]
                for i, (x, y) in enumerate(stroke)]} for stroke in record["strokes"]],
            "userData": {"org.plotfont.hershey": {"row": row, "sourceId": record["sourceId"]}},
        })
    return validate({
        "format": "PlotFont", "version": "0.2", "id": "hershey-roman-simplex-regular",
        "familyName": "Hershey Roman Simplex", "styleName": "Regular", "unitsPerEm": 1400,
        "metrics": {"ascender": 1200, "descender": -400, "capHeight": 1000, "xHeight": 14 * scale, "lineGap": 200},
        "missingGlyph": ".notdef", "glyphs": glyphs, "kerning": [],
        "metadata": {"source": SOURCE, "sourceRevision": REVISION,
                     "sourceFile": "hershey-fonts/rowmans.jhf", "sourceSha256": hashlib.sha256(raw).hexdigest(),
                     "license": "Hershey permissive terms; see vendor/hershey/NOTICE.txt; not MIT",
                     "attribution": "Hershey glyphs: Dr. A. V. Hershey; JHF data representation: James Hurt, Cognition, Inc.",
                     "mapping": "Rows 0–94 map to U+0020–U+007E; row 95 retained unencoded; .notdef is original PlotFont artwork.",
                     "coordinateTransform": {"sourceBaselineY": 9, "sourceCapTopY": -12, "scale": scale}},
    })
