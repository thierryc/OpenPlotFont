"""Explicit layout modes and positioned glyph runs in font units."""
import re
from .validation import validate, ValidationError, require


def checked_text(text):
    require(isinstance(text,str) and len(text) <= 100000, 'text', 'expected string of at most 100000 scalars')
    require(not any(0xD800 <= ord(c) <= 0xDFFF for c in text), 'text', 'surrogates are not Unicode scalars')
    require(not any(c in text for c in '\r\n\t'), 'text', 'shape one run; split lines and resolve tabs first')


def shape_text(font, text, *, direction='ltr', script='Latn', language='en', features=None):
    """Shape one horizontal run. Clusters are UTF-8 byte offsets into its input."""
    validate(font)
    checked_text(text)
    require('layout' in font, 'layout', 'font has no OpenType layout payload; choose simple mode explicitly')
    require(direction in ('ltr','rtl'), 'direction', 'only horizontal ltr/rtl runs are supported')
    require(isinstance(script,str) and re.fullmatch(r'[A-Za-z]{4}',script), 'script', 'expected ISO 15924 tag, e.g. Latn')
    require(isinstance(language,str) and re.fullmatch(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*',language),
            'language', 'expected language identifier, e.g. en or tr')
    entries = {entry['tag']:entry for entry in font['layout']['features']}
    require(features is None or isinstance(features,dict), 'features', 'expected feature value object')
    settings = {tag:e['recommendedValue'] for tag,e in entries.items() if 'recommendedValue' in e}
    for tag,value in (features or {}).items():
        require(tag in entries and type(value) is int and 0 <= value <= 0xFFFFFFFF,
                'features', f'unknown feature or invalid value: {tag}')
        settings[tag] = value
    try:
        import uharfbuzz as hb
    except ImportError as error:
        raise ValidationError('OpenType shaping needs uharfbuzz; install openplotfont[shaping]') from error
    from .layout import decode_payload
    face = hb.Face(decode_payload(font['layout']))
    native = hb.Font(face)
    hb.ot_font_set_funcs(native)
    native.scale = (font['unitsPerEm'],font['unitsPerEm'])
    buffer = hb.Buffer()
    buffer.add_utf8(text.encode('utf-8'))
    buffer.direction, buffer.script, buffer.language = direction, script, language
    buffer.cluster_level = hb.BufferClusterLevel.MONOTONE_CHARACTERS
    try:
        hb.shape(native, buffer, settings, shapers=['ot'])
    except Exception as error:
        raise ValidationError(f'OpenType shaping failed: {error}') from error
    order = font['layout']['glyphOrder']
    infos, positions = buffer.glyph_infos or [], buffer.glyph_positions or []
    require(len(infos) <= 100000, 'layout', 'shaped run exceeds 100000 glyphs')
    x = y = 0
    glyphs = []
    for info,pos in zip(infos,positions):
        require(0 <= info.codepoint < len(order), 'layout', 'shaper returned unmapped glyph ID')
        glyphs.append({'name':order[info.codepoint], 'glyphId':info.codepoint, 'cluster':info.cluster,
                       'x':x+pos.x_offset, 'y':y+pos.y_offset,
                       'xAdvance':pos.x_advance,'yAdvance':pos.y_advance,
                       'xOffset':pos.x_offset,'yOffset':pos.y_offset})
        x += pos.x_advance
        y += pos.y_advance
    return {'mode':'opentype','text':text,'direction':direction,'script':script,'language':language,
            'features':settings,'clusterEncoding':'utf-8-bytes',
            'engine':{'name':'HarfBuzz','version':hb.version_string()},
            'layoutSha256':font['layout']['font']['sha256'], 'glyphs':glyphs,'xAdvance':x,'yAdvance':y}


def simple_run(font, text):
    checked_text(text)
    mapping = {int(u,16):g for g in font['glyphs'] for u in g['unicodes']}
    drawings = {g['name']:g for g in font['glyphs']}
    kerning = {(p['left'],p['right']):p['value'] for p in font.get('kerning',[])}
    x = cluster = 0
    previous = None
    items = []
    for scalar in text:
        glyph = mapping.get(ord(scalar),drawings[font['missingGlyph']])
        if previous:
            x += kerning.get((previous,glyph['name']),0)
        items.append({'name':glyph['name'],'cluster':cluster,'x':x,'y':0,
                      'joinable':ord(scalar) in mapping and scalar!=' '})
        x += glyph['advanceWidth']
        cluster += len(scalar.encode('utf-8'))
        previous = glyph['name']
    return {'mode':'simple','glyphs':items,'xAdvance':x,'yAdvance':0}
