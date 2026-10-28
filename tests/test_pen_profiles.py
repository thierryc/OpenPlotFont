"""0.4 conformance: preservation, explicit fallback and operative profile errors."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from openplotfont import load, validate, render_svg, ValidationError
from openplotfont.profiles import CHANNELS, appearance_binding, centerlines, linear_values
from openplotfont.storage import write_font
from openplotfont.glyphs_export import export_font
from test_glyphs_adapter import font_fixture

ROOT = Path(__file__).resolve().parents[1]
NS = {'s':'http://www.w3.org/2000/svg'}


def fixture(native=False):
    font = load(ROOT/'examples/minimal.opf.json')
    font['version'] = '0.4'
    op = font['glyphs'][2]['strokes'][0]
    profile = {'version':'1','model':'linear-ellipse-v1',
               'defaults':dict(zip(CHANNELS,(40,30,0,0,0,0))),
               'points':[{'segment':0,'t':0.25,'values':{'width':20,'angle':None}},
                         {'segment':0,'t':0.75,'values':{'width':80,'angle':45}}],
               'style':{'capStart':'round','capEnd':'round','join':'round'}}
    op['penProfile'] = profile
    if native:
        profile['model'] = 'glyphs4-v1'
        profile['points'][0]['values']['progressionOut'] = 0.6
        profile['appearance'] = {'source':'Original test renderer','fillRule':'nonzero',
                                'bindingSha256':appearance_binding(op),
                                'contours':[{'closed':True,'commands':[['M',0,0],['L',100,0],['L',0,100]]}]}
    return font, op


class PenProfileTests(unittest.TestCase):
    def test_nullable_and_missing_channels_survive_storage(self):
        font,op = fixture(native=True)
        before = copy.deepcopy(font)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'font.opf.json'
            write_font(p,font)
            self.assertEqual(load(p),before)
        self.assertEqual(font,before)

    def test_old_versions_reject_profiles(self):
        for version in ('0.2','0.3'):
            font,_ = fixture();font['version']=version
            with self.assertRaisesRegex(ValidationError,'requires version 0.4'):validate(font)

    def test_profile_errors_are_actionable(self):
        edits = [lambda p:p.update(version='2'),lambda p:p.update(model='unknown'),
                 lambda p:p['defaults'].update(width=0),lambda p:p['defaults'].update(height=-1),
                 lambda p:p['defaults'].update(strokePosition=1.1),lambda p:p['defaults'].update(angle=None),
                 lambda p:p['points'][0].update(segment=999),lambda p:p['points'][0].update(t=-.1),
                 lambda p:p['points'][0].update(t=True),lambda p:p['points'].reverse(),
                 lambda p:p['points'].append(copy.deepcopy(p['points'][-1])),
                 lambda p:p['points'][0]['values'].update(pressure=1),
                 lambda p:p['points'][0]['values'].update(width=float('inf')),
                 lambda p:p['points'][0]['values'].update(progressionOut=.6)]
        for edit in edits:
            with self.subTest(edit=edits.index(edit)):
                font,op=fixture();edit(op['penProfile'])
                with self.assertRaises(ValidationError):validate(font)

    def test_binding_detects_edits_to_each_operative_field(self):
        edits=[lambda o:o['commands'][1].__setitem__(1,123),lambda o:o.update(closed=True),
               lambda o:o['penProfile']['defaults'].update(width=41),
               lambda o:o['penProfile']['points'][0]['values'].update(progressionOut=.7),
               lambda o:o['penProfile']['style'].update(capStart='butt')]
        for edit in edits:
            font,op=fixture(native=True);edit(op)
            with self.assertRaisesRegex(ValidationError,'stale appearance'):validate(font)

    def test_native_profile_needs_appearance(self):
        font,op=fixture(native=True);del op['penProfile']['appearance']
        with self.assertRaisesRegex(ValidationError,'requires a bound'):validate(font)

    def test_fill_profile_is_rejected(self):
        font,op=fixture();profile=op['penProfile']
        op.clear();op.update(kind='fill',fillRule='evenodd',contours=[{'closed':True,'commands':[['M',0,0],['L',10,10]]}],penProfile=profile)
        with self.assertRaisesRegex(ValidationError,'unsupported on fills'):validate(font)
        del op['penProfile'];op['contours'][0]['penProfile']=profile
        with self.assertRaisesRegex(ValidationError,'fill contours'):validate(font)

    def test_explicit_centerlines_keeps_all_other_font_semantics(self):
        font,_=fixture(native=True);before=copy.deepcopy(font)
        simple=centerlines(font)
        self.assertEqual(simple['version'],'0.3');self.assertEqual(font,before)
        expected=copy.deepcopy(before);expected['version']='0.3'
        del expected['glyphs'][2]['strokes'][0]['penProfile']
        expected['metadata']=simple['metadata']
        self.assertEqual(simple,expected)
        self.assertIn('removed 1',simple['metadata']['exportWarnings'][-1])

    def test_linear_channels_use_curve_parameter_and_inherited_defaults(self):
        _,op=fixture();p=op['penProfile']
        v=linear_values(p,0,.5)
        self.assertEqual(v['width'],50);self.assertEqual(v['height'],30);self.assertEqual(v['angle'],22.5)

    def test_native_appearance_renders_compound_contours_and_centerline_is_explicit(self):
        font,op=fixture(native=True)
        paths=ET.fromstring(render_svg(font,'A')).findall('s:path',NS)
        self.assertEqual(paths[0].get('fill-rule'),'nonzero')
        self.assertEqual(paths[0].get('d'),'M 0 0 L 1.71428571429 0 L 0 -1.71428571429 Z')
        paths=ET.fromstring(render_svg(font,'A',profile_mode='centerline')).findall('s:path',NS)
        self.assertEqual(paths[0].get('fill'),'none')
        self.assertEqual(paths[0].get('d').count('L'),2)

    def test_writing_masks_keep_independent_strokes_and_clock_order(self):
        font,_=fixture(native=True)
        root=ET.fromstring(render_svg(font,'AA',writing_mask=True))
        masks=root.findall('s:defs/s:mask',NS)
        self.assertEqual(len(masks),4)
        animations=root.findall('.//s:animate',NS)
        begins=[float(a.get('begin')[:-1]) for a in animations]
        self.assertEqual(begins[0],0);self.assertEqual(begins,sorted(set(begins)))
        self.assertIn('constant centerline speed',root.find('s:desc',NS).text)

    def test_join_rejects_unreviewed_profile_transitions(self):
        font,_=fixture()
        with self.assertRaisesRegex(ValidationError,'profile transition'):render_svg(font,'AA',join=True)

    def test_profile_cli_preserves_source_and_refuses_overwrite(self):
        font,_=fixture(native=True)
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'source.opf.json';target=Path(d)/'simple.opf.json';write_font(source,font)
            before=source.read_bytes()
            command=[sys.executable,'-m','openplotfont','centerlines',str(source),'-o',str(target)]
            result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr);self.assertIn('removed 1',result.stdout)
            self.assertNotEqual(subprocess.run(command,cwd=ROOT,capture_output=True).returncode,0)
            self.assertEqual(source.read_bytes(),before)

    def test_layout_does_not_downgrade_04(self):
        from openplotfont.layout import attach_layout
        old=load(ROOT/'examples/layout-demo.opf.json');old['version']='0.4'
        import base64
        new=attach_layout(old,base64.b64decode(old['layout']['font']['data']),glyph_order=old['layout']['glyphOrder'])
        self.assertEqual(new['version'],'0.4')
        self.assertEqual(new['glyphs'],old['glyphs'])

    def test_schema_agrees_with_semantic_validator(self):
        import jsonschema
        schema=json.loads((ROOT/'schemas/openplotfont-0.4.schema.json').read_text())
        for native in (False,True):
            font,_=fixture(native);validate(font);jsonschema.validate(font,schema)

    def test_legacy_export_cannot_silently_drop_profile(self):
        from types import SimpleNamespace as Obj
        font=font_fixture();p=font.glyphs[1].layers['master'].paths[0]
        p.attributes={'strokeWidth':40.}
        with self.assertRaisesRegex(ValidationError,'requires 0.4'):
            export_font(font,'master',{'line':'line'},output_version='0.3')
        simple=export_font(font,'master',{'line':'line'},centerlines_only=True)
        self.assertEqual(simple['version'],'0.3')
        self.assertIn('removed 3',simple['metadata']['exportWarnings'][-1])


class LayoutProjectionWarningTests(unittest.TestCase):
    def test_compiled_layout_projection_keeps_loss_warning(self):
        import io
        from fontTools.fontBuilder import FontBuilder
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
        font=font_fixture()
        for g in font.glyphs:
            g.layers['master'].width=650
        font.glyphs[1].layers['master'].paths[0].attributes={'strokeWidth':40.}
        order=['.notdef','A','V']
        fb=FontBuilder(1000,isTTF=True)
        fb.setupGlyphOrder(order);fb.setupCharacterMap({65:'A',86:'V'})
        fb.setupGlyf({name:TTGlyphPen(None).glyph() for name in order})
        fb.setupHorizontalMetrics({name:(650,0) for name in order})
        fb.setupHorizontalHeader(ascent=800,descent=-200)
        fb.setupNameTable({'familyName':'Original layout test','styleName':'Regular'})
        fb.setupOS2();fb.setupPost();fb.setupMaxp()
        stream=io.BytesIO();fb.save(stream)
        result=export_font(font,'master',{'line':'line'},centerlines_only=True,layout_bytes=stream.getvalue(),glyph_order=order)
        self.assertIn('layout',result)
        self.assertIn('removed 3',result['metadata']['exportWarnings'][-1])

    def test_writing_mask_rejects_joined_schedule(self):
        font,_=fixture()
        with self.assertRaisesRegex(ValidationError,'independent strokes'):
            render_svg(font,'AA',join=True,writing_mask=True)
