"""Draft 0.3 embedded static OpenType data; outlines never replace PlotFont geometry."""
import base64
import binascii
import copy
import hashlib
import io
import json
import re
import struct

from .validation import ValidationError, require, object_at, array_at, text

MAX_SFNT = 8 * 1024 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode('utf-8')


def fonttools():
    try:
        from fontTools.ttLib import TTFont
    except ImportError as error:
        raise ValidationError('OpenType layout validation needs fontTools; install plotfont[shaping]') from error
    return TTFont


def read_sfnt(raw):
    require(isinstance(raw, bytes) and 12 <= len(raw) <= MAX_SFNT, '$.layout.font', 'expected 12 bytes–8 MiB sfnt')
    require(raw[:4] in (b'\x00\x01\x00\x00', b'OTTO'), '$.layout.font', 'expected static TTF/OTF sfnt, not a collection or web font')
    count = struct.unpack_from('>H', raw, 4)[0]
    require(1 <= count <= 128 and 12 + count * 16 <= len(raw), '$.layout.font', 'invalid sfnt directory')
    seen, regions = set(), []
    for i in range(count):
        tag, checksum, offset, length = struct.unpack_from('>4sIII', raw, 12 + 16*i)
        require(tag not in seen, '$.layout.font', 'duplicate sfnt table')
        seen.add(tag)
        require(offset >= 12 + count*16 and offset + length <= len(raw), '$.layout.font', 'table outside sfnt')
        if length:
            require(all(offset+length <= start or offset >= end for start,end in regions),
                    '$.layout.font', 'overlapping sfnt tables')
            regions.append((offset, offset+length))
    try:
        ot = fonttools()(io.BytesIO(raw), lazy=False, recalcTimestamp=False)
        required = {'head', 'hhea', 'maxp', 'hmtx', 'cmap'}
        require(required <= set(ot.keys()), '$.layout.font', 'missing required font/metric tables')
        require(('glyf' in ot and 'loca' in ot) or 'CFF ' in ot, '$.layout.font', 'missing static outline tables')
        require(not set(ot.keys()) & {'fvar','gvar','HVAR','VVAR','MVAR','avar','morx','mort','kerx'},
                '$.layout.font', 'variable and AAT fonts are outside the static OpenType profile')
        for tag in required | ({'GSUB','GPOS','GDEF'} & set(ot.keys())):
            ot[tag]  # Force parsing before accepting a payload.
        return ot
    except ValidationError:
        raise
    except Exception as error:
        raise ValidationError(f'$.layout.font: malformed OpenType data: {error}') from error


def manifest(ot):
    """Expose coverage without inventing application defaults or lookup ordering."""
    features, systems = set(), []
    for tag in ('GSUB', 'GPOS'):
        if tag not in ot:
            continue
        table = ot[tag].table
        records = table.FeatureList.FeatureRecord if table.FeatureList else []
        lookups = table.LookupList.Lookup if table.LookupList else []
        for record in records:
            require(all(0 <= index < len(lookups) for index in record.Feature.LookupListIndex),
                    '$.layout.font', 'invalid feature lookup reference')
            features.add(str(record.FeatureTag))
        for script in table.ScriptList.ScriptRecord if table.ScriptList else []:
            languages = ([('dflt', script.Script.DefaultLangSys)] if script.Script.DefaultLangSys else [])
            languages += [(r.LangSysTag, r.LangSys) for r in script.Script.LangSysRecord]
            for language, system in languages:
                indices = list(system.FeatureIndex)
                required = system.ReqFeatureIndex
                if required != 0xFFFF:
                    indices.append(required)
                require(all(0 <= i < len(records) for i in indices), '$.layout.font', 'invalid language feature reference')
                systems.append({'table': tag, 'script': str(script.ScriptTag), 'language': str(language),
                                'features': sorted({str(records[i].FeatureTag) for i in indices}),
                                'requiredFeature': str(records[required].FeatureTag) if required != 0xFFFF else None})
    return sorted(features), sorted(systems, key=lambda s: (s['table'],s['script'],s['language']))


def decode_payload(layout):
    container = object_at(layout.get('font'), '$.layout.font')
    require(container.get('encoding') == 'base64', '$.layout.font.encoding', 'expected base64')
    encoded = container.get('data')
    require(isinstance(encoded, str) and len(encoded) <= 4*((MAX_SFNT+2)//3), '$.layout.font.data', 'invalid or oversized payload')
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as error:
        raise ValidationError('$.layout.font.data: invalid base64') from error
    require(base64.b64encode(raw).decode('ascii') == encoded, '$.layout.font.data', 'noncanonical base64')
    require(container.get('sha256') == digest(raw), '$.layout.font.sha256', 'payload digest mismatch')
    return raw


def validate_layout(font):
    layout = object_at(font['layout'], '$.layout')
    require(layout.get('profile') == 'opentype-static-v1', '$.layout.profile', 'unsupported layout profile')
    order = array_at(layout.get('glyphOrder'), '$.layout.glyphOrder')
    require(all(isinstance(n,str) and n for n in order) and 1 <= len(order) <= 65535,
            '$.layout.glyphOrder', 'invalid glyph ID mapping')
    require(len(order) == len(set(order)), '$.layout.glyphOrder', 'duplicate glyph ID mapping')
    drawings = {g['name']:g for g in font['glyphs']}
    require(set(order) == set(drawings), '$.layout.glyphOrder', 'glyph mapping must cover every drawing exactly once')
    require(order[0] == font['missingGlyph'], '$.layout.glyphOrder[0]', 'glyph zero must map to missingGlyph')
    raw = decode_payload(layout)
    ot = read_sfnt(raw)
    try:
        native = ot.getGlyphOrder()
        require(len(native) == len(order), '$.layout.glyphOrder', 'glyph count differs from payload')
        require(ot['head'].unitsPerEm == font['unitsPerEm'], '$.layout.font', 'unitsPerEm mismatch')
        for gid, name in enumerate(order):
            width = ot['hmtx'].metrics[native[gid]][0]
            require(width == drawings[name]['advanceWidth'], '$.layout.font', f'advance mismatch for {name}')
        expected = {int(u,16):g['name'] for g in font['glyphs'] for u in g['unicodes']}
        cmap = ot.getBestCmap() or {}
        actual = {u:order[ot.getGlyphID(n)] for u,n in cmap.items()}
        require(actual == expected, '$.layout.font', 'Unicode cmap mismatch')
        # All Unicode cmap subtables must agree; UVS mappings need a separate contract.
        for table in ot['cmap'].tables:
            if table.isUnicode():
                require(table.format != 14, '$.layout.font', 'variation-selector cmap is not supported in this profile')
                require(all(u in expected and order[ot.getGlyphID(n)] == expected[u] for u,n in table.cmap.items()),
                        '$.layout.font', 'conflicting Unicode cmap subtables')
        tags, systems = manifest(ot)
        entries = array_at(layout.get('features'), '$.layout.features')
        seen = []
        for entry in entries:
            object_at(entry, '$.layout.features[]')
            tag = entry.get('tag')
            require(isinstance(tag,str) and re.fullmatch(r'[ -~]{4}',tag), '$.layout.features', 'invalid feature tag')
            seen.append(tag)
            if 'label' in entry:
                text(entry['label'], '$.layout.features.label')
            if 'recommendedValue' in entry:
                require(type(entry['recommendedValue']) is int and 0 <= entry['recommendedValue'] <= 0xFFFFFFFF,
                        '$.layout.features.recommendedValue', 'expected unsigned integer')
        require(sorted(seen) == tags, '$.layout.features', 'feature manifest differs from compiled payload')
        require(layout.get('systems') == systems, '$.layout.systems', 'script/language manifest differs from compiled payload')
        if 'source' in layout:
            source = object_at(layout['source'], '$.layout.source')
            require(source.get('format') in ('fea','glyphs-feature-source-v1'), '$.layout.source.format', 'unsupported authoring source')
            content = source.get('content')
            require(isinstance(content,str) if source['format']=='fea' else isinstance(content,dict),
                    '$.layout.source.content', 'invalid authoring source content')
            if source['format'] == 'glyphs-feature-source-v1':
                for group in ('prefixes','classes','features'):
                    for block in array_at(content.get(group),'$.layout.source.content.'+group):
                        object_at(block,'$.layout.source.content.block')
                        text(block.get('name'),'$.layout.source.content.block.name')
                        require(isinstance(block.get('code'),str) and isinstance(block.get('notes'),str),
                                '$.layout.source.content.block','code and notes must be strings')
                        require(type(block.get('automatic')) is bool and type(block.get('disabled')) is bool,
                                '$.layout.source.content.block','automatic/disabled must be booleans')
            require(len(canonical_bytes(content)) <= 1024*1024, '$.layout.source', 'source exceeds 1 MiB')
            require(source.get('sha256') == digest(canonical_bytes(content)), '$.layout.source.sha256', 'source digest mismatch; rebuild layout')
            require(source.get('compiledSha256') == digest(raw), '$.layout.source.compiledSha256', 'source/payload binding mismatch')
        return raw
    except ValidationError:
        raise
    except Exception as error:
        raise ValidationError(f'$.layout: malformed OpenType mapping or manifest: {error}') from error
    finally:
        ot.close()


def attach_layout(font, raw, *, glyph_order=None, source=None, source_format='fea', feature_settings=None):
    """Bind an already compiled static font to drawings. Never guess renamed glyph IDs."""
    from .validation import validate
    validate(font)
    require(glyph_order is None or isinstance(glyph_order,(list,tuple)), '$.layout.glyphOrder', 'expected glyph ID array')
    ot = read_sfnt(raw)
    try:
        tags, systems = manifest(ot)
        order = list(ot.getGlyphOrder()) if glyph_order is None else list(glyph_order)
    finally:
        ot.close()
    feature_settings = {} if feature_settings is None else feature_settings
    require(isinstance(feature_settings,dict) and set(feature_settings) <= set(tags), '$.layout.features', 'settings reference absent features')
    require(all(isinstance(value,dict) and not set(value)-{'label','recommendedValue'}
                for value in feature_settings.values()), '$.layout.features', 'settings must contain label/recommendedValue objects')
    result = copy.deepcopy(font)
    result['version'] = '0.3'
    layout = {'profile':'opentype-static-v1', 'font':{'encoding':'base64', 'sha256':digest(raw),
              'data':base64.b64encode(raw).decode('ascii')}, 'glyphOrder':order,
              'features':[{'tag':tag, **feature_settings.get(tag,{})} for tag in tags], 'systems':systems}
    if source is not None:
        layout['source'] = {'format':source_format, 'content':copy.deepcopy(source),
                            'sha256':digest(canonical_bytes(source)), 'compiledSha256':digest(raw)}
    result['layout'] = layout
    return validate(result)
