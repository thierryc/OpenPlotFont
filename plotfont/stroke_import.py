"""Explicit stroke-font adapters. Requires optional FontTools for SVG geometry.

These functions do not infer drawing intent from arbitrary outline fonts.
Callers must review and explicitly declare their source to be a stroke font.
"""
import hashlib
import math
import re
from pathlib import Path
import xml.etree.ElementTree as ET

from .validation import ValidationError, validate


def fallback(upm):
    return {'name': '.notdef', 'unicodes': [], 'advanceWidth': upm * .6,
            'strokes': [{'closed': True, 'commands': [
                ['M', upm * .1, 0], ['L', upm * .1, upm * .7],
                ['L', upm * .5, upm * .7], ['L', upm * .5, 0]]}]}


def font_record(identity, family, upm, metrics, glyphs, metadata, kerning=None):
    return validate({'format': 'PlotFont', 'version': '0.3', 'id': identity,
                     'familyName': family, 'styleName': 'Regular', 'unitsPerEm': upm,
                     'metrics': metrics, 'missingGlyph': '.notdef', 'glyphs': glyphs,
                     'kerning': kerning or [], 'metadata': metadata})


class StrokePen:
    def __init__(self):
        self.strokes = []
        self.commands = None
        self.non_drawing_moves = []

    def moveTo(self, point):
        if self.commands is not None:
            self.endPath()
        self.commands = [['M', *point]]

    def lineTo(self, point):
        self.commands.append(['L', *point])

    def curveTo(self, *points):
        if len(points) != 3:
            raise ValidationError('SVG: unsupported cubic segment')
        self.commands.append(['C', *(n for p in points for n in p)])

    def qCurveTo(self, *points):
        if len(points) != 2 or points[-1] is None:
            raise ValidationError('SVG: unsupported quadratic segment')
        self.commands.append(['Q', *(n for p in points for n in p)])

    def finish(self, closed):
        if self.commands is None:
            raise ValidationError('SVG: path end without move')
        if len(self.commands) < 2:
            self.non_drawing_moves.append({'closure': 'closed' if closed else 'open', 'commands': self.commands})
            self.commands = None
            return
        self.strokes.append({'closed': closed, 'commands': self.commands})
        self.commands = None

    def closePath(self):
        self.finish(True)

    def endPath(self):
        self.finish(False)


def arc_cubics(center, rx, ry, angle, start, sweep, endpoint):
    """Tangent-matched cubic arcs, at most 5 degrees per segment.

    Conservative geometric error allowance: 1e-7 * max(rx, ry) source units.
    This preserves curves, not flattened polylines. See library documentation.
    """
    count = max(1, math.ceil(abs(sweep) / math.radians(5)))
    ca, sa = math.cos(angle), math.sin(angle)
    def transform(x, y):
        return (center[0] + ca * rx * x - sa * ry * y,
                center[1] + sa * rx * x + ca * ry * y)
    for i in range(count):
        a, b = start + sweep * i / count, start + sweep * (i + 1) / count
        t = 4 / 3 * math.tan((b - a) / 4)
        p1 = transform(math.cos(a) - t * math.sin(a), math.sin(a) + t * math.cos(a))
        p2 = transform(math.cos(b) + t * math.sin(b), math.sin(b) - t * math.cos(b))
        end = endpoint if i == count - 1 else transform(math.cos(b), math.sin(b))
        yield ['C', *p1, *p2, *end]


def svg_paths(data, non_drawing_moves=None):
    from fontTools.svgLib.path import parse_path
    from fontTools.svgLib.path.arc import EllipticalArc
    class PreciseArc(EllipticalArc):
        def draw(self, pen):
            if not self._parametrize():
                if not self.rx or not self.ry:
                    pen.lineTo((self.target_point.real, self.target_point.imag))
                return
            # FontTools parametrizes in scaled, rotated unit-circle coordinates.
            ca, sa = math.cos(self.angle), math.sin(self.angle)
            cx, cy = self.center_point.real * self.rx, self.center_point.imag * self.ry
            center = (ca * cx - sa * cy, sa * cx + ca * cy)
            for command in arc_cubics(center, self.rx, self.ry, self.angle,
                                      self.theta1, self.theta_arc,
                                      (self.target_point.real, self.target_point.imag)):
                pen.curveTo(tuple(command[1:3]), tuple(command[3:5]), tuple(command[5:7]))
    pen = StrokePen()
    if data.strip():
        parse_path(data, pen, arc_class=PreciseArc)
    if non_drawing_moves is not None:
        non_drawing_moves.extend(pen.non_drawing_moves)
    return pen.strokes


def import_svg(path, *, identity, family, metadata, stroke_source=False):
    if not stroke_source:
        raise ValidationError('SVG: explicit reviewed stroke-source declaration required')
    raw = Path(path).read_bytes()
    if len(raw) > 20_000_000:
        raise ValidationError('SVG: source exceeds size limit')
    root = ET.fromstring(raw)
    fonts = root.findall('.//{*}font')
    if len(fonts) != 1:
        raise ValidationError('SVG: expected one reusable font, not a composed drawing')
    font = fonts[0]
    face = font.find('{*}font-face')
    if face is None:
        raise ValidationError('SVG: missing font-face metrics')
    if any(font.get(k, '0') != '0' for k in ('horiz-origin-x', 'horiz-origin-y')):
        raise ValidationError('SVG: nonzero font origin unsupported')
    for node in root.iter():
        if 'transform' in node.attrib:
            raise ValidationError('SVG: transforms require explicit coordinate conversion; unsupported')
        if node.tag.split('}')[-1] in ('use', 'script', 'image', 'filter'):
            raise ValidationError('SVG: external or executable geometry unsupported')
    upm = int(float(face.get('units-per-em', '1000')))
    if upm <= 0 or upm != float(face.get('units-per-em', '1000')):
        raise ValidationError('SVG: integer units-per-em required')
    metrics = {'ascender': float(face.get('ascent', upm * .8)),
               'descender': -abs(float(face.get('descent', upm * .2))),
               'capHeight': float(face.get('cap-height', upm * .7)),
               'xHeight': float(face.get('x-height', upm * .5)), 'lineGap': 0}
    glyphs, used_names, encoded = [], set(), set()
    warnings = []
    elements = [(font.find('{*}missing-glyph'), True)] + [(g, False) for g in font.findall('{*}glyph')]
    for index, (element, missing) in enumerate(elements):
        if element is None:
            continue
        if list(element):
            raise ValidationError('SVG: nested glyph geometry unsupported; nothing was dropped')
        if any(k in element.attrib for k in ('transform', 'vert-adv-y')):
            raise ValidationError('SVG: glyph transform/vertical layout unsupported')
        text = element.get('unicode', '')
        maps = [f'{ord(text):04X}'] if len(text) == 1 and ord(text) not in encoded and not missing else []
        name = '.notdef' if missing else element.get('glyph-name') or (f'uni{ord(text):04X}' if len(text) == 1 else f'source.{index:04d}')
        if name != '.notdef' and (not re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]*', name)):
            name = f'uni{ord(text):04X}' if len(text) == 1 else f'source.{index:04d}'
        if name in used_names:
            name += f'.source{index}'
        used_names.add(name)
        if maps:
            encoded.add(ord(text))
        elif text:
            warnings.append(f'{name}: source Unicode sequence/alternate retained unencoded: {text!r}')
        non_drawing = []
        strokes = svg_paths(element.get('d', ''), non_drawing)
        glyph = {'name': name, 'unicodes': maps,
                 'advanceWidth': float(element.get('horiz-adv-x', font.get('horiz-adv-x', upm))),
                 'strokes': strokes,
                 'userData': {'org.plotfont.source': {'record': index, 'unicodeText': text,
                                                     'glyphName': element.get('glyph-name', '')}}}
        glyphs.append(glyph)
        if non_drawing:
            glyph['userData']['org.plotfont.source']['nonDrawingMoves'] = non_drawing
            warnings.append(f'{name}: isolated pen-up moves have no ink; retained in source userData, not converted to drawing strokes')
    missing_record = next((g for g in glyphs if g['name'] == '.notdef'), None)
    if missing_record is not None and not missing_record['strokes']:
        missing_record['name'] = 'source.notdef'
        used_names.remove('.notdef')
        warnings.append('Empty source missing-glyph retained as source.notdef; original PlotFont fallback added')
    if '.notdef' not in used_names:
        glyphs.insert(0, fallback(upm))
    # Missing drawings stay missing; do not invent replacements for empty glyphs.
    kern = {}
    source_names = {g['userData']['org.plotfont.source']['glyphName']: g['name'] for g in glyphs if 'userData' in g}
    def selectors(node, side):
        found = set()
        for name in node.get('g' + side, '').split(','):
            if name:
                if name not in source_names:
                    raise ValidationError('SVG: unresolved kerning glyph ' + name)
                found.add(source_names[name])
        for item in node.get('u' + side, '').split(','):
            if not item:
                continue
            if item.startswith('U+'):
                token = item[2:]
                if '?' in token:
                    lo, hi = int(token.replace('?', '0'), 16), int(token.replace('?', 'F'), 16)
                elif '-' in token:
                    lo, hi = (int(x, 16) for x in token.split('-'))
                else:
                    lo = hi = int(token, 16)
                found.update(g['name'] for g in glyphs if any(lo <= int(u, 16) <= hi for u in g['unicodes']))
            else:
                found.update(g['name'] for g in glyphs if g.get('userData', {}).get('org.plotfont.source', {}).get('unicodeText') == item)
        return found
    for node in font.findall('{*}hkern'):
        for left in selectors(node, '1'):
            for right in selectors(node, '2'):
                kern.setdefault((left, right), -float(node.get('k', '0')))
    if font.findall('{*}vkern'):
        raise ValidationError('SVG: vertical kerning unsupported')
    meta = dict(metadata, sourceSha256=hashlib.sha256(raw).hexdigest(), sourceCoordinateSystem='font units, Y up',
                sourceMetrics=dict(face.attrib), importWarnings=warnings,
                arcConversion='Circular/elliptical arcs: cubic segments <=5 degrees; conservative error <=1e-7*max(radius) source units; no flattening',
                drawingIntent='Reviewed upstream stroke-font data; explicit centerline import')
    return font_record(identity, family, upm, metrics, glyphs, meta,
                       [{'left': l, 'right': r, 'value': v} for (l, r), v in sorted(kern.items()) if v])


def import_lff(path, *, identity, family, metadata):
    """Reviewed LFF stroke fonts; retain polylines, references, and bulge arcs."""
    raw = Path(path).read_bytes()
    fields, records, code = {}, {}, None
    for line in raw.decode('utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            if ':' in line:
                key, value = line[1:].split(':', 1)
                fields.setdefault(key.strip(), value.strip())
            continue
        if line.startswith('['):
            code = int(line[1:line.index(']')], 16)
            if code in records:
                raise ValidationError('LFF: duplicate glyph code')
            records[code] = []
        elif code is None:
            raise ValidationError('LFF: geometry before glyph')
        else:
            records[code].append(line)
    scale = 100
    def resolve(code, chain=()):
        if code in chain or len(chain) > 32:
            raise ValidationError('LFF: recursive character reference')
        if code not in records:
            raise ValidationError('LFF: missing character reference')
        strokes = []
        for line in records[code]:
            if line.startswith('C'):
                strokes.extend(resolve(int(line[1:], 16), (*chain, code)))
                continue
            points = []
            for token in line.split(';'):
                values = token.split(',')
                if len(values) not in (2, 3) or (len(values) == 3 and not values[2].startswith('A')):
                    raise ValidationError('LFF: unsupported vertex ' + token)
                points.append((float(values[0]), float(values[1]), float(values[2][1:]) if len(values) == 3 else 0))
            if len(points) < 2:
                raise ValidationError('LFF: isolated vertex')
            commands = [['M', points[0][0] * scale, points[0][1] * scale]]
            for a, b in zip(points, points[1:]):
                bulge = b[2]
                if bulge == 0:
                    commands.append(['L', b[0] * scale, b[1] * scale])
                    continue
                dx, dy = b[0] - a[0], b[1] - a[1]
                if not math.hypot(dx, dy):
                    raise ValidationError('LFF: degenerate arc')
                offset = (1 - bulge * bulge) / (4 * bulge)
                center = ((a[0] + b[0]) / 2 - dy * offset, (a[1] + b[1]) / 2 + dx * offset)
                radius = math.dist(center, a[:2])
                for c in arc_cubics(tuple(x * scale for x in center), radius * scale, radius * scale, 0,
                                    math.atan2(a[1] - center[1], a[0] - center[0]), 4 * math.atan(bulge),
                                    (b[0] * scale, b[1] * scale)):
                    commands.append(c)
            strokes.append({'closed': False, 'commands': commands})
        return strokes
    glyphs = [fallback(1000)]
    for code in records:
        strokes = resolve(code)
        from fontTools.pens.boundsPen import BoundsPen
        bounds_pen = BoundsPen(None)
        for stroke in strokes:
            for c in stroke['commands']:
                if c[0] == 'M': bounds_pen.moveTo(tuple(c[1:]))
                elif c[0] == 'L': bounds_pen.lineTo(tuple(c[1:]))
                elif c[0] == 'C': bounds_pen.curveTo(tuple(c[1:3]), tuple(c[3:5]), tuple(c[5:7]))
            bounds_pen.endPath()
        right = bounds_pen.bounds[2] if bounds_pen.bounds else 0
        advance = (float(fields.get('WordSpacing', '6.75')) * scale if code == 32 else
                   max(0, right + float(fields.get('LetterSpacing', '0')) * scale))
        glyphs.append({'name': f'uni{code:04X}', 'unicodes': [f'{code:04X}'], 'advanceWidth': advance,
                       'strokes': strokes, 'userData': {'org.plotfont.source': {'codepoint': code}}})
    if 32 not in records:
        glyphs.append({'name': 'space', 'unicodes': ['0020'], 'advanceWidth': float(fields.get('WordSpacing', '6.75')) * scale, 'strokes': []})
    return font_record(identity, family, 1000, {'ascender': 1500, 'descender': -500, 'capHeight': 900,
                       'xHeight': 600, 'lineGap': 0}, glyphs,
                       dict(metadata, sourceSha256=hashlib.sha256(raw).hexdigest(), sourceHeader=fields,
                            coordinateTransform={'scale': scale, 'yAxis': 'up'},
                            spacingPolicy='LibreCAD RS_Text: actual geometric xMax plus LetterSpacing; WordSpacing for space; origins retained',
                            arcConversion='LFF bulge=tan(sweep/4); cubic segments <=5 degrees; error allowance 1e-7*radius source units',
                            metricsPolicy='Explicit catalog normalization: capHeight 9 LFF units, upm 10; adjust physical size using reviewed specimen'))
