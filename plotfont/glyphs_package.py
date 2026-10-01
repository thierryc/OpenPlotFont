"""Write explicit Glyphs format-4 packages without mutating an open font."""
import copy
from pathlib import Path
import uuid

from .glyphs_export import node_commands
from .validation import validate


def path_nodes(operation):
    nodes = []
    kinds = {'M': 'l', 'L': 'l', 'Q': 'q', 'C': 'c'}
    for c in operation['commands']:
        if c[0] == 'C':
            nodes.extend([[c[1], c[2], 'o'], [c[3], c[4], 'o']])
        elif c[0] == 'Q':
            nodes.append([c[1], c[2], 'o'])
        nodes.append([c[-2], c[-1], kinds[c[0]]])
    return nodes


def write_package(font, destination):
    from openstep_plist import dumps
    validate(font)
    path = Path(destination)
    if path.exists():
        raise FileExistsError(path)
    if path.suffix != '.glyphspackage':
        raise ValueError('Expected .glyphspackage destination')
    master = str(uuid.uuid5(uuid.NAMESPACE_URL, font['id'])).upper()
    info = {'.appVersion': '4108', '.formatVersion': 4, 'unitsPerEm': font['unitsPerEm'],
            'versionMajor': 1, 'versionMinor': 0,
            'fontMaster': [{'id': master, 'name': font['styleName'], 'metricValues':
                           [{'pos': font['metrics'][k]} for k in ['ascender', 'capHeight', 'xHeight']] +
                           [{'pos': 0}, {'pos': font['metrics']['descender']}, {'pos': 0}]}],
            'metrics': [{'type': k} for k in ['ascender', 'cap height', 'x-height', 'baseline', 'descender', 'italic angle']],
            'properties': [{'key': 'familyNames', 'values': [{'language': 'dflt', 'value': font['familyName']}]}],
            'settings': {'disablesNiceNames': True, 'gridSubDivision': 1000000},
            'userData': {'org.plotfont.font': {'id': font['id'], 'styleName': font['styleName'],
                         'missingGlyph': font['missingGlyph'], 'lineGap': font['metrics']['lineGap'],
                         'metadata': font.get('metadata', {})}}}
    def save(file, obj):
        file.write_text(dumps(obj, unicode_escape=False, float_precision=15, indent=None,
                              single_line_tuples=True) + '\n', encoding='utf-8')
    (path / 'glyphs').mkdir(parents=True)
    save(path / 'fontinfo.plist', info)
    save(path / 'order.plist', [g['name'] for g in font['glyphs']])
    for index, glyph in enumerate(font['glyphs']):
        shapes, plan = [], []
        for operation in glyph['strokes']:
            if operation.get('kind', 'stroke') != 'stroke':
                raise ValueError('Catalog package writer only accepts reviewed stroke fonts')
            plan.append({'kind': 'stroke', 'pathIndex': len(shapes)})
            shapes.append({'closed': int(operation['closed']), 'nodes': path_nodes(operation)})
        data = copy.deepcopy(glyph.get('userData', {}))
        record = {'glyphname': glyph['name'], 'layers': [{'layerId': master,
                  'width': glyph['advanceWidth'], 'shapes': shapes}], 'userData': data}
        if len(glyph['unicodes']) == 1:
            record['unicode'] = int(glyph['unicodes'][0], 16)
        elif glyph['unicodes']:
            record['unicode'] = [int(u, 16) for u in glyph['unicodes']]
        save(path / 'glyphs' / f'{index:05d}.glyph', record)
    if font.get('kerning'):
        pairs = {}
        for pair in font['kerning']:
            pairs.setdefault(pair['left'], {})[pair['right']] = pair['value']
        save(path / 'kerning.plist', {'kerningLTR': {master: pairs}})


def read_package(path):
    """Independent saved-file round trip, including precision and drawing order."""
    from openstep_plist import loads
    path = Path(path)
    info = loads((path / 'fontinfo.plist').read_text(), use_numbers=True)
    order = loads((path / 'order.plist').read_text(), use_numbers=True)
    master = info['fontMaster'][0]
    meta = info['userData']['org.plotfont.font']
    glyphs = {}
    types = {'l': 'line', 'c': 'curve', 'q': 'qcurve', 'o': 'offcurve'}
    for file in (path / 'glyphs').glob('*.glyph'):
        record = loads(file.read_text(), use_numbers=True)
        layer = record['layers'][0]
        codes = record.get('unicode', [])
        if not isinstance(codes, list):
            codes = [codes]
        g = {'name': record['glyphname'], 'unicodes': [f'{int(c):04X}' for c in codes],
             'advanceWidth': float(layer['width']), 'strokes': []}
        for shape in layer.get('shapes', []):
            closed = bool(int(shape['closed']))
            nodes = [(types[n[2]], float(n[0]), float(n[1])) for n in shape['nodes']]
            g['strokes'].append({'closed': closed, 'commands': node_commands(nodes, closed)})
        if record.get('userData'):
            g['userData'] = record['userData']
        glyphs[g['name']] = g
    kernfile = path / 'kerning.plist'
    pairs = loads(kernfile.read_text(), use_numbers=True)['kerningLTR'][master['id']] if kernfile.exists() else {}
    return validate({'format': 'PlotFont', 'version': '0.3', 'id': meta['id'],
                     'familyName': info['properties'][0]['values'][0]['value'], 'styleName': meta['styleName'],
                     'unitsPerEm': int(info['unitsPerEm']), 'metrics':
                     {k: float(master['metricValues'][i].get('pos', 0)) for i, k in
                      [(0, 'ascender'), (1, 'capHeight'), (2, 'xHeight'), (4, 'descender')]} | {'lineGap': meta['lineGap']},
                     'missingGlyph': meta['missingGlyph'], 'glyphs': [glyphs[n] for n in order],
                     'kerning': [{'left': l, 'right': r, 'value': float(v)} for l, rs in pairs.items() for r, v in rs.items()],
                     'metadata': meta['metadata']})
