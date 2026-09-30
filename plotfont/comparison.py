"""Compare source/export semantics, allowing only explicit diagnostic metadata."""

import math
from .validation import validate, ValidationError


def compare_fonts(expected, actual, *, tolerance=1e-9):
    validate(expected)
    validate(actual)
    if type(tolerance) not in (int, float) or not math.isfinite(tolerance) or tolerance < 0:
        raise ValidationError('comparison: tolerance must be finite and nonnegative')

    def canonical(font):
        result = {k: font[k] for k in ('format', 'version', 'id', 'familyName', 'styleName', 'unitsPerEm', 'metrics', 'missingGlyph')}
        result['kerning'] = font.get('kerning', [])
        result['glyphs'] = []
        for glyph in sorted(font['glyphs'], key=lambda g: g['name']):
            record = dict(glyph)
            record['strokes'] = [{**op, 'kind': op.get('kind', 'stroke')} for op in glyph['strokes']]
            for optional, default in (('anchors', []), ('userData', {}), ('connections', {})):
                record.setdefault(optional, default)
            result['glyphs'].append(record)
        result['metadata'] = {k: v for k, v in font.get('metadata', {}).items() if k not in ('glyphsMasterId', 'exportWarnings')}
        return result

    def check(a, b, path):
        if type(a) in (int, float) and type(b) in (int, float):
            if not math.isclose(a, b, rel_tol=0, abs_tol=tolerance):
                raise ValidationError(f'{path}: source/export mismatch: {a!r} != {b!r}')
        elif isinstance(a, dict) and isinstance(b, dict):
            if a.keys() != b.keys():
                raise ValidationError(f'{path}: source/export fields differ: {sorted(a.keys() ^ b.keys())}')
            for key in a:
                check(a[key], b[key], f'{path}.{key}')
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                raise ValidationError(f'{path}: source/export counts differ: {len(a)} != {len(b)}')
            for index, (left, right) in enumerate(zip(a, b)):
                check(left, right, f'{path}[{index}]')
        elif type(a) is not type(b) or a != b:
            raise ValidationError(f'{path}: source/export mismatch: {a!r} != {b!r}')
    check(canonical(expected), canonical(actual), '$')
    return True
