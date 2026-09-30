"""Populate an explicitly bound empty project font; never create/save documents."""

from contextlib import ExitStack
from pathlib import Path

from .hershey import import_roman_simplex
from .validation import ValidationError


def populate_hershey(font, source, expected_destination, *, glyph_type, layer_type, path_type, node_type, line_type):
    actual = getattr(font, 'filepath', None)
    if not actual or Path(str(actual)).resolve() != Path(expected_destination).resolve():
        raise ValidationError('Hershey import: document must be the exact saved project destination')
    if len(font.masters) != 1:
        raise ValidationError('Hershey import: an empty font with exactly one master is required')
    placeholders = list(font.glyphs)
    for glyph in placeholders:
        if len(glyph.userData):
            raise ValidationError('Hershey import: empty font required; existing glyph metadata is never replaced')
        for layer in glyph.layers:
            background = getattr(layer, 'hasBackground', False)
            background = background() if callable(background) else background
            if (len(layer.shapes) or len(layer.anchors) or len(getattr(layer, 'hints', []))
                    or len(getattr(layer, 'guides', [])) or getattr(layer, 'backgroundImage', None)
                    or background):
                raise ValidationError('Hershey import: empty font required; existing artwork is never replaced')
    data = import_roman_simplex(source)
    master = font.masters[0]
    prepared = []
    # Build everything detached; reject missing precision support before changing font.
    with ExitStack() as restore:
        for record in data['glyphs']:
            glyph = glyph_type(record['name'])
            glyph.unicodes = list(record['unicodes'])
            glyph.export = True
            for key, value in record.get('userData', {}).items():
                glyph.userData[key] = value
            layer = layer_type()
            layer.layerId = master.id
            layer.associatedMasterId = master.id
            getter = getattr(layer, 'temporarilyDisableRounding', None)
            setter = getattr(layer, 'setTemporarilyDisableRounding_', None)
            if getter is None or not callable(setter):
                raise ValidationError('Hershey import: native fractional-coordinate precision API unavailable')
            prior = bool(getter() if callable(getter) else getter)
            restore.callback(setter, prior)
            setter(True)
            layer.width = record['advanceWidth']
            for operation in record['strokes']:
                path = path_type()
                path.closed = operation['closed']
                for command in operation['commands']:
                    path.nodes.append(node_type(tuple(command[1:]), type=line_type))
                layer.shapes.append(path)
            glyph.layers[master.id] = layer
            prepared.append(glyph)
        for placeholder in placeholders:
            del font.glyphs[placeholder.name]
        font.familyName = data['familyName']
        font.upm = data['unitsPerEm']
        master.name = data['styleName']
        for key in ('ascender', 'descender', 'capHeight', 'xHeight'):
            setattr(master, key, data['metrics'][key])
        font.userData['org.plotfont.font'] = {
            'id': data['id'], 'styleName': data['styleName'], 'missingGlyph': data['missingGlyph'],
            'lineGap': data['metrics']['lineGap'], 'metadata': data['metadata'],
        }
        for glyph in prepared:
            font.glyphs.append(glyph)
    return data
