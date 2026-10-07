# MenuTitle: Prepare OpenPlotFont Layout Demo
# encoding: utf-8
"""Populate only the saved empty layout-demo project font. Never save or compile."""
import runpy
import sys
from pathlib import Path
from GlyphsApp import Glyphs, GSGlyph, GSLayer, GSNode, GSPath, GSAnchor, GSFeature, GSFeaturePrefix, LINE

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from openplotfont.glyphs_export import export_font
from openplotfont.comparison import compare_fonts


def main(font=None):
    font = Glyphs.font if font is None else font
    destination = ROOT/'fonts/layout-demo/OpenPlotFontLayoutDemo.glyphspackage'
    if font is None or str(font.filepath) != str(destination) or len(font.glyphs) or len(font.masters)!=1:
        raise RuntimeError('Requires the saved empty single-master layout-demo project font')
    if len(font.features) or len(font.classes) or len(font.featurePrefixes):
        raise RuntimeError('Existing feature blocks are never replaced')
    fixture = runpy.run_path(str(ROOT/'scripts/build_layout_fixture.py'))
    data = fixture['geometry']()
    master = font.masters[0]
    font.familyName = data['familyName']
    font.upm = data['unitsPerEm']
    master.name = 'Regular'
    for key in ('ascender','descender','capHeight','xHeight'):
        setattr(master,key,data['metrics'][key])
    font.userData['org.openplotfont.font'] = {key:data[key] for key in ('id','styleName','missingGlyph','metadata')}
    font.userData['org.openplotfont.font']['lineGap'] = data['metrics']['lineGap']
    for record in data['glyphs']:
        glyph = GSGlyph(record['name'])
        glyph.unicodes = record['unicodes']
        glyph.export = True
        if record['name'].endswith('comb'):
            glyph.category = 'Mark'
            glyph.subCategory = 'Nonspacing'
        font.glyphs.append(glyph)
        layer = GSLayer()
        layer.associatedMasterId = master.id
        layer.width = record['advanceWidth']
        for operation in record['strokes']:
            path = GSPath()
            path.closed = operation['closed']
            for command in operation['commands']:
                path.nodes.append(GSNode(tuple(command[1:]),type=LINE))
            layer.shapes.append(path)
        for point in record.get('anchors',[]):
            anchor = GSAnchor()
            anchor.name = point['name']
            anchor.position = (point['x'],point['y'])
            layer.anchors.append(anchor)
        glyph.layers[master.id] = layer
    prefix = GSFeaturePrefix('OpenPlotFontLanguagesAndMarks',fixture['PREFIX'])
    prefix.automatic = False
    font.featurePrefixes.append(prefix)
    for tag,code in fixture['FEATURES'].items():
        feature = GSFeature(tag,code)
        feature.automatic = False
        font.features.append(feature)
    # Manual kern feature is compiled layout data, not a native kerning pair.
    data['kerning'] = []
    data['version'] = '0.2'
    exported = export_font(font,master.id,{'line':LINE})
    compare_fonts(data,exported)
    print('Prepared and verified',len(data['glyphs']),'glyphs and',len(font.features),'manual features. Save separately.')


if __name__ == '__main__':
    main()
