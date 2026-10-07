"""OpenType semantics, corruption rejection and explicit compatibility boundaries."""
import base64
import copy
import io
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from openplotfont import load, validate, shape_text, render_svg, ValidationError
from openplotfont.layout import attach_layout, decode_payload, digest
from openplotfont.comparison import compare_fonts
from openplotfont.glyphs_export import feature_source
from test_openplotfont import ROOT, example, NS


def fixture():
    return load(ROOT/'examples/layout-demo.opf.json')


class LayoutValidationTests(unittest.TestCase):
    def test_rebuilt_original_fixture_has_equivalent_layout(self):
        build = runpy.run_path(str(ROOT/'scripts/build_layout_fixture.py'))
        raw = build['compile_fixture'](build['geometry'](),build['feature_text']())
        rebuilt = attach_layout(build['geometry'](),raw,
                                feature_settings={tag:{'recommendedValue':0} for tag in ('ss01','salt','tnum','curs')})
        for text,features in [('fi',{}),('AA',{}),('A',{'ss01':1}),('A\u0301\u0307',{}),('un',{'curs':1})]:
            self.assertEqual(shape_text(rebuilt,text,features=features)['glyphs'],
                             shape_text(fixture(),text,features=features)['glyphs'])
        self.assertEqual(fixture()['layout']['source']['content'],(ROOT/'tests/fixtures/layout-demo.fea').read_text())

    def test_version_compatibility_and_explicit_modes(self):
        original = example()
        changed = copy.deepcopy(original)
        changed['version'] = '0.3'
        self.assertEqual(render_svg(original,'A'),render_svg(changed,'A'))
        changed['layout'] = fixture()['layout']
        changed['version'] = '0.2'
        with self.assertRaisesRegex(ValidationError,'requires version 0.3'):
            validate(changed)
        with self.assertRaisesRegex(ValidationError,'no OpenType'):
            shape_text(original,'A')
        with self.assertRaisesRegex(ValidationError,'require OpenType'):
            render_svg(fixture(),'A',features={'ss01':1})
        with self.assertRaisesRegex(ValidationError,'joining requires'):
            render_svg(fixture(),'un',layout_mode='opentype',join=True)

    def test_manifest_mapping_and_digest_corruption(self):
        mutations = [
            ('profile',lambda f:f['layout'].update(profile='unknown')),
            ('base64',lambda f:f['layout']['font'].update(data='!')),
            ('digest',lambda f:f['layout']['font'].update(sha256='0'*64)),
            ('glyph mapping',lambda f:f['layout']['glyphOrder'].__setitem__(3,'absent')),
            ('duplicate',lambda f:f['layout']['glyphOrder'].__setitem__(3,'A')),
            ('glyph zero',lambda f:f['layout']['glyphOrder'].reverse()),
            ('advance',lambda f:f['glyphs'][2].update(advanceWidth=601)),
            ('Unicode cmap',lambda f:f['glyphs'][2].update(unicodes=['0042'])),
            ('feature manifest',lambda f:f['layout']['features'].pop()),
            ('script/language',lambda f:f['layout']['systems'].pop()),
            ('source digest',lambda f:f['layout']['source'].update(content='changed')),
            ('binding',lambda f:f['layout']['source'].update(compiledSha256='0'*64)),
        ]
        for message,change in mutations:
            with self.subTest(message=message):
                font = fixture()
                change(font)
                with self.assertRaisesRegex(ValidationError,message):
                    validate(font)

    def test_broken_sfnt_rejected_even_with_new_digest(self):
        for raw in (b'garbage header here',decode_payload(fixture()['layout'])[:100]):
            font = fixture()
            font['layout']['font'].update(data=base64.b64encode(raw).decode(),sha256=digest(raw))
            with self.assertRaisesRegex(ValidationError,'sfnt'):
                validate(font)

    def test_incompatible_binary_rejected_and_no_source_mutation(self):
        from fontTools.ttLib import TTFont
        source = fixture()
        before = copy.deepcopy(source)
        for mutate in (lambda t:setattr(t['head'],'unitsPerEm',2000),
                       lambda t:t['hmtx'].metrics.__setitem__('A',(601,0))):
            font = TTFont(io.BytesIO(decode_payload(source['layout'])),recalcTimestamp=False)
            mutate(font)
            stream = io.BytesIO()
            font.save(stream)
            geometry = copy.deepcopy(source)
            del geometry['layout']
            with self.assertRaises(ValidationError):
                attach_layout(geometry,stream.getvalue())
        self.assertEqual(source,before)

    def test_optional_dependencies_have_actionable_errors(self):
        with patch.dict(sys.modules,{'fontTools.ttLib':None}):
            self.assertIsInstance(validate(example()),dict)
            with self.assertRaisesRegex(ValidationError,'fontTools'):
                validate(fixture())
        font = fixture()
        with patch.dict(sys.modules,{'uharfbuzz':None}):
            self.assertIn('<svg',render_svg(example(),'A'))
            with self.assertRaisesRegex(ValidationError,'uharfbuzz'):
                shape_text(font,'fi')

    def test_comparison_checks_layout_not_only_geometry(self):
        changed = fixture()
        entry = next(e for e in changed['layout']['features'] if e['tag']=='ss01')
        entry['recommendedValue'] = 1
        with self.assertRaisesRegex(ValidationError,'source/export'):
            compare_fonts(fixture(),changed)

    def test_attachment_rejects_invalid_mapping_and_settings(self):
        font = fixture()
        raw = decode_payload(font['layout'])
        for settings in ([], {'liga':1}, {'liga':{'tag':'xxxx'}}, {'xxxx':{}}):
            with self.subTest(settings=settings),self.assertRaises(ValidationError):
                attach_layout(font,raw,feature_settings=settings)
        with self.assertRaisesRegex(ValidationError,'glyph ID array'):
            attach_layout(font,raw,glyph_order=42)

    def test_authoring_flags_use_documented_active_property(self):
        from types import SimpleNamespace
        block = SimpleNamespace(name='liga',code='sub f i by f_i;',active=True,
                                automatic=False,notes='Original rule',disabled=lambda:False)
        font = SimpleNamespace(features=[block],featurePrefixes=[],classes=[])
        self.assertFalse(feature_source(font)['features'][0]['disabled'])
        block.active = False
        self.assertTrue(feature_source(font)['features'][0]['disabled'])


class ShapingTests(unittest.TestCase):
    def names(self,text,**settings):
        return [g['name'] for g in shape_text(fixture(),text,**settings)['glyphs']]

    def test_ligatures_alternates_numerals_and_language(self):
        self.assertEqual(self.names('fi'),['f_i'])
        self.assertEqual(self.names('fi',features={'liga':0}),['f','i'])
        self.assertEqual(self.names('A'),['A'])
        self.assertEqual(self.names('A',features={'ss01':1}),['A.alt'])
        self.assertEqual(self.names('A',features={'salt':1}),['A.alt'])
        self.assertEqual(self.names('00',features={'tnum':1}),['zero.tnum']*2)
        self.assertEqual(self.names('i',language='en'),['i'])
        self.assertEqual(self.names('i',language='tr'),['i.trk'])
        self.assertEqual(self.names('i',language='tr',features={'locl':0}),['i'])

    def test_context_and_gdef_ignore_marks(self):
        self.assertEqual(self.names('AA'),['A','A.alt'])
        self.assertEqual(self.names('AA',features={'calt':0}),['A','A'])
        self.assertEqual(self.names('A\u0301A'),['A','acutecomb','A.alt'])

    def test_base_ligature_and_mark_attachment_positions(self):
        for text,position in [('A\u0301',(300,700)),('fi\u0301',(700,700))]:
            run = shape_text(fixture(),text)
            mark = run['glyphs'][-1]
            self.assertEqual((mark['x'],mark['y']),position)
            self.assertEqual(mark['xAdvance'],0)
        run = shape_text(fixture(),'A\u0301\u0307')
        self.assertEqual((run['glyphs'][-1]['x'],run['glyphs'][-1]['y']),(300,850))
        self.assertEqual([g['cluster'] for g in run['glyphs']],[0,1,3])
        self.assertEqual(run['clusterEncoding'],'utf-8-bytes')

    def test_cursive_positioning_preserves_pen_lifts(self):
        run = shape_text(fixture(),'un',features={'curs':1})
        self.assertEqual((run['glyphs'][1]['x'],run['glyphs'][1]['y']),(400,100))
        tree = ET.fromstring(render_svg(fixture(),'un',layout_mode='opentype',features={'curs':1},cap_height_mm=700))
        paths = tree.findall('s:path',NS)
        self.assertEqual(len(paths),2)
        self.assertTrue(paths[1].get('d').startswith('M 400 -100'))

    def test_kerning_applied_once_and_optional_feature_switch(self):
        run = shape_text(fixture(),'AA',features={'calt':0})
        self.assertEqual(run['glyphs'][1]['x'],520)
        tree = ET.fromstring(render_svg(fixture(),'AA',layout_mode='opentype',features={'calt':0},cap_height_mm=700))
        self.assertTrue(tree.findall('s:path',NS)[1].get('d').startswith('M 570 0'))
        off = shape_text(fixture(),'AA',features={'calt':0,'kern':0})
        self.assertEqual(off['glyphs'][1]['x'],600)

    def test_shaped_svg_preserves_curves_and_y_axis_multiline(self):
        font = fixture()
        glyph = next(g for g in font['glyphs'] if g['name']=='f_i')
        glyph['strokes'][0]['commands'] = [['M',100,0],['C',100,500,300,700,500,0]]
        tree = ET.fromstring(render_svg(font,'fi\nA\u0301',layout_mode='opentype',cap_height_mm=700))
        paths = tree.findall('s:path',NS)
        self.assertEqual(paths[0].get('data-glyph'),'f_i')
        self.assertIn('C 100 -500 300 -700 500 0',paths[0].get('d'))
        self.assertTrue(paths[-1].get('d').startswith('M 300 500'))

    def test_shaped_alternate_preserves_mixed_operations_and_holes(self):
        font = fixture()
        alternate = next(g for g in font['glyphs'] if g['name']=='A.alt')
        mixed = next(g for g in example('mixed')['glyphs']
                     if any(o.get('kind')=='fill' for o in g['strokes']))
        alternate['strokes'] = copy.deepcopy(mixed['strokes'])
        tree = ET.fromstring(render_svg(font,'A',layout_mode='opentype',features={'ss01':1}))
        paths = tree.findall('s:path',NS)
        self.assertEqual(len(paths),len(mixed['strokes']))
        self.assertTrue(all(p.get('data-glyph')=='A.alt' for p in paths))
        self.assertEqual(paths[0].get('fill'),'none')
        self.assertEqual(paths[1].get('fill-rule'),'evenodd')
        self.assertEqual(paths[1].get('d').count('M '),2)
        self.assertEqual(paths[1].get('d').count('Z'),2)

    def test_missing_empty_rtl_and_invalid_requests(self):
        self.assertEqual(self.names('☃'),['.notdef'])
        self.assertEqual(shape_text(fixture(),'')['glyphs'],[])
        self.assertEqual(self.names('f i',direction='rtl',features={'liga':0}),['i','space','f'])
        for kwargs in ({'direction':'ttb'},{'script':'bad'},{'language':'bad language'},
                       {'features':{'xxxx':1}},{'features':{'liga':-1}},{'features':{'liga':True}}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValidationError):
                shape_text(fixture(),'fi',**kwargs)
        for text in ('fi\nfi','\t','\ud800'):
            with self.assertRaises(ValidationError):
                shape_text(fixture(),text)

    def test_output_matches_independent_harfbuzz_buffer(self):
        import uharfbuzz as hb
        font = fixture()
        raw = decode_payload(font['layout'])
        hbfont = hb.Font(hb.Face(raw))
        hb.ot_font_set_funcs(hbfont)
        hbfont.scale = (1000,1000)
        for text in ('fi','A\u0301\u0307','AA','un'):
            buffer = hb.Buffer()
            buffer.add_utf8(text.encode())
            buffer.direction,buffer.script,buffer.language = 'ltr','Latn','en'
            buffer.cluster_level = hb.BufferClusterLevel.MONOTONE_CHARACTERS
            hb.shape(hbfont,buffer,{'ss01':0,'salt':0,'tnum':0,'curs':0},shapers=['ot'])
            run = shape_text(font,text)
            self.assertEqual([g['glyphId'] for g in run['glyphs']],[g.codepoint for g in buffer.glyph_infos])
            self.assertEqual([(g['xAdvance'],g['yAdvance'],g['xOffset'],g['yOffset']) for g in run['glyphs']],
                             [(g.x_advance,g.y_advance,g.x_offset,g.y_offset) for g in buffer.glyph_positions])


class LayoutCLITests(unittest.TestCase):
    def cli(self,*args):
        return subprocess.run([sys.executable,'-m','openplotfont',*map(str,args)],cwd=ROOT,capture_output=True,text=True)

    def test_shape_render_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)/'run.json'
            source = ROOT/'examples/layout-demo.opf.json'
            r = self.cli('shape',source,'A','--feature','ss01=1','-o',out)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(json.loads(out.read_text())['glyphs'][0]['name'],'A.alt')
            before = out.read_bytes()
            self.assertNotEqual(self.cli('shape',source,'fi','-o',out).returncode,0)
            self.assertEqual(out.read_bytes(),before)
            r = self.cli('render',source,'fi','--layout','opentype','-o',Path(directory)/'shaped.svg')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('data-glyph="f_i"',(Path(directory)/'shaped.svg').read_text())
            r = self.cli('shape',source,'fi','--feature','liga=no','-o',Path(directory)/'bad.json')
            self.assertNotEqual(r.returncode,0)
            self.assertFalse((Path(directory)/'bad.json').exists())

    def test_attach_validates_before_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            font = fixture()
            raw = decode_payload(font.pop('layout'))
            (root/'geometry.json').write_text(json.dumps(font))
            (root/'font.ttf').write_bytes(raw)
            (root/'order.json').write_text('42')
            args = ('attach-layout',root/'geometry.json',root/'font.ttf')
            r = self.cli(*args,'--glyph-order',root/'order.json','-o',root/'bad.json')
            self.assertNotEqual(r.returncode,0)
            self.assertNotIn('Traceback',r.stderr)
            self.assertFalse((root/'bad.json').exists())
            r = self.cli(*args,'--fea',ROOT/'tests/fixtures/layout-demo.fea','-o',root/'good.json')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(load(root/'good.json')['layout']['source']['format'],'fea')
            original = (root/'good.json').read_bytes()
            self.assertNotEqual(self.cli(*args,'-o',root/'good.json').returncode,0)
            self.assertEqual((root/'good.json').read_bytes(),original)


class NativeLayoutTests(unittest.TestCase):
    def test_native_feature_source_and_compiled_receipt(self):
        font = load(ROOT/'examples/layout-demo-native.opf.json')
        report = json.loads((ROOT/'tests/fixtures/native-layout-report.json').read_text())
        self.assertEqual(font['layout']['font']['sha256'],report['compiledSha256'])
        build = runpy.run_path(str(ROOT/'scripts/build_layout_fixture.py'))
        blocks = font['layout']['source']['content']
        self.assertEqual([(b['name'],b['code']) for b in blocks['features']],list(build['FEATURES'].items()))
        self.assertEqual(blocks['prefixes'][0]['code'],build['PREFIX'])
        self.assertTrue(all(not b['disabled'] and not b['automatic'] for b in blocks['features']))
        self.assertEqual(font['metadata']['exportWarnings'],['Active source features absent from compiled layout: curs'])
        with self.assertRaisesRegex(ValidationError,'unknown feature'):
            shape_text(font,'un',features={'curs':1})

    def test_native_and_portable_shaping_agree_where_compiled(self):
        font = load(ROOT/'examples/layout-demo-native.opf.json')
        for text,settings in [('fi',{}),('AA',{'features':{'calt':0}}),('AA',{}),
                              ('A',{'features':{'ss01':1}}),('00',{'features':{'tnum':1}}),
                              ('A\u0301\u0307',{}),('fi\u0301',{}),('i',{'language':'tr'})]:
            with self.subTest(text=text,settings=settings):
                actual = shape_text(font,text,**settings)['glyphs']
                expected = shape_text(fixture(),text,**settings)['glyphs']
                keys = ('name','x','y','xAdvance','yAdvance','xOffset','yOffset')
                # Native compilers can assign different GIDs and cluster merging.
                self.assertEqual([[g[k] for k in keys] for g in actual],
                                 [[g[k] for k in keys] for g in expected])

    def test_saved_native_source_preserves_drawings_mappings_and_rules(self):
        from openstep_plist import loads
        package = ROOT/'fonts/layout-demo/OpenPlotFontLayoutDemo.glyphspackage'
        info = loads((package/'fontinfo.plist').read_text())
        exported = load(ROOT/'examples/layout-demo-native.opf.json')
        expected = {g['name']:g for g in fixture()['glyphs']}
        files = list((package/'glyphs').glob('*.glyph'))
        self.assertEqual(len(files),len(expected))
        for path in files:
            glyph = loads(path.read_text())
            record = expected[glyph['glyphname']]
            codes = glyph.get('unicode',[])
            codes = codes if isinstance(codes,list) else [codes]
            self.assertEqual([f'{int(u):04X}' for u in codes],record['unicodes'])
            layer = glyph['layers'][0]
            self.assertEqual(float(layer['width']),record['advanceWidth'])
            self.assertEqual(len(layer.get('shapes',[])),len(record['strokes']))
            for shape,operation in zip(layer.get('shapes',[]),record['strokes']):
                self.assertEqual(bool(int(shape['closed'])),operation['closed'])
                self.assertEqual([[float(n[0]),float(n[1])] for n in shape['nodes']],
                                 [c[1:] for c in operation['commands']])
            anchors = [{'name':a['name'],'x':float(a.get('pos',[0,0])[0]),
                        'y':float(a.get('pos',[0,0])[1])} for a in layer.get('anchors',[])]
            self.assertEqual(anchors,record.get('anchors',[]))
        blocks = exported['layout']['source']['content']['features']
        for block,saved in zip(blocks,info['features']):
            self.assertEqual(saved['tag'],block['name'])
            self.assertEqual((package/'features'/saved['file']).read_text().strip(),block['code'].strip())
