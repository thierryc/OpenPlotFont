"""Parse the pinned James Hurt JHF representation; preserve every source record."""

import hashlib
from pathlib import Path

from .validation import ValidationError, validate

REVISION = "1356bf2f83d380fcef68c887e88675eb9d445d86"
SOURCE_SHA256 = "8718fb129c0f6bce89c84fe41bc467e39534d215a6f7c3220cc5789a8a7d8618"
SOURCE = "https://github.com/kamalmostafa/hershey-fonts"

# Each supported face has independently pinned bytes and explicit mapping/metrics.
# Other Hershey repertoires must not inherit the printable-ASCII mapping silently.
FACES = {
    "roman-simplex": {"file": "rowmans.jhf", "family": "Hershey Roman Simplex",
                      "sha256": SOURCE_SHA256, "xHeight": 700, "descender": -420},
    "roman-duplex": {"file": "rowmand.jhf", "family": "Hershey Roman Duplex",
                     "sha256": "c56497b162a3831f0da2e189ada4a7335ce81b1c3c1cf380b2ced04287313d2e",
                     "xHeight": 700, "descender": -420},
    "roman-triplex": {"file": "rowmant.jhf", "family": "Hershey Roman Triplex",
                      "sha256": "703d6a641334bce32ae8347900b6ec743d4672f898266796853f26f53918b52a",
                      "xHeight": 700, "descender": -420},
    "script-simplex": {"file": "scripts.jhf", "family": "Hershey Script Simplex",
                       "sha256": "6b391b2ea3a0771cf18caff0ed111db3d05681fa586d423a740cc0b2b155a873",
                       "xHeight": 450, "descender": -600},
}


ASCII_NAMES = dict(zip(range(32, 65), (
    'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright '
    'asterisk plus comma hyphen period slash zero one two three four five six seven eight nine '
    'colon semicolon less equal greater question at').split()))
ASCII_NAMES.update({91:'bracketleft',92:'backslash',93:'bracketright',94:'asciicircum',95:'underscore',96:'grave',
                    123:'braceleft',124:'bar',125:'braceright',126:'asciitilde'})
ASCII_NAMES.update({u: chr(u) for u in (*range(65,91), *range(97,123))})

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
    """Retained compatibility entry point for the first face."""
    return import_hershey(path, "roman-simplex")


def import_hershey(path, face="roman-simplex"):
    if face not in FACES:
        raise ValidationError(f"Unsupported Hershey face: {face}")
    settings = FACES[face]
    label = settings["family"].removeprefix("Hershey ")
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != settings["sha256"]:
        raise ValidationError(f"{label} source differs from the pinned upstream data; provenance would be incorrect")
    records = parse_jhf(raw.decode("ascii"))
    if len(records) != 96:
        raise ValidationError(f"{label} source must contain all 96 records")
    # Source capitals run y=-12..9. Baseline 9; exactly 50 font units per coordinate; native saves stay integral.
    scale = 50
    glyphs = [{"name": ".notdef", "unicodes": [], "advanceWidth": 600,
               "strokes": [{"closed": True, "commands": [["M", 50, 0], ["L", 50, 1000], ["L", 550, 1000], ["L", 550, 0]]}]}]
    for row, record in enumerate(records):
        code = row + 32
        glyphs.append({
            "name": ASCII_NAMES[code] if code <= 126 else "hershey.extra.95",
            "unicodes": [f"{code:04X}"] if code <= 126 else [],
            "advanceWidth": (record["right"] - record["left"]) * scale,
            "strokes": [{"closed": False, "commands": [
                ["M" if i == 0 else "L", (x - record["left"]) * scale, (9 - y) * scale]
                for i, (x, y) in enumerate(stroke)]} for stroke in record["strokes"]],
            "userData": {"org.openplotfont.hershey": {"row": row, "sourceId": record["sourceId"]}},
        })
    return validate({
        "format": "OpenPlotFont", "version": "0.2", "id": f"hershey-{face}-regular",
        "familyName": settings["family"], "styleName": "Regular", "unitsPerEm": 1470,
        "metrics": {"ascender": 1260, "descender": settings["descender"], "capHeight": 1050,
                    "xHeight": settings["xHeight"], "lineGap": 210},
        "missingGlyph": ".notdef", "glyphs": glyphs, "kerning": [],
        "metadata": {"source": SOURCE, "sourceRevision": REVISION,
                     "sourceFile": "hershey-fonts/" + settings["file"], "sourceSha256": hashlib.sha256(raw).hexdigest(),
                     "license": "Hershey permissive terms; see vendor/hershey/NOTICE.txt; not MIT",
                     "attribution": "Hershey glyphs: Dr. A. V. Hershey; JHF data representation: James Hurt, Cognition, Inc.",
                     "mapping": "Rows 0–94 map to U+0020–U+007E; row 95 retained unencoded; .notdef is original OpenPlotFont artwork.",
                     "coordinateTransform": {"sourceBaselineY": 9, "sourceCapTopY": -12, "scale": scale}},
    })
