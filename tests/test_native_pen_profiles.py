"""Independent comparison with original raw records captured after native reopen."""
import json
import math
import sys
import unittest
from openplotfont import load, render_svg
from openplotfont.profiles import CHANNELS, centerlines
from test_openplotfont import ROOT


def nodes_from_commands(path):
    commands=path['commands'];closed=path['closed']
    first_type='curve' if closed and commands[-1][0]=='C' and commands[-1][-2:]==commands[0][-2:] else 'line'
    result=[[*commands[0][1:],first_type]]
    for command in commands[1:]:
        if command[0]=='L':result.append([*command[1:],'line'])
        elif command[0]=='C':result.extend([[*command[1:3],'offcurve'],[*command[3:5],'offcurve'],[*command[5:],'curve']])
        else:raise AssertionError('Original native fixture contains unsupported command')
    if closed and result[-1][:2]==result[0][:2]:result.pop()
    return result


class NativeProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.font=load(ROOT/'examples/pen-profile-demo.opf.json')
        cls.raw=json.loads((ROOT/'tests/fixtures/pen-profile-native-records.json').read_text())

    def test_every_native_path_and_channel_matches_independent_raw_readback(self):
        for g in self.font['glyphs']:
            raw=self.raw[g['name']]
            self.assertEqual(g['advanceWidth'],raw['width'])
            self.assertEqual(len(g['strokes']),len(raw['paths']))
            for op,path in zip(g['strokes'],raw['paths']):
                self.assertEqual(op['closed'],path['closed'])
                self.assertEqual(nodes_from_commands(op),path['nodes'])
                ends=[i for i,n in enumerate(path['nodes']) if i and n[2]!='offcurve']+([0] if path['closed'] else [])
                expected=[]
                for point in path['points']:
                    values={k:None if point[k]==sys.float_info.max else point[k] for k in CHANNELS}
                    expected.append({'segment':ends.index(point['node']),'t':point['t'],'values':values})
                expected.sort(key=lambda p:(p['segment'],p['t']))
                self.assertEqual(op['penProfile']['points'],expected)
                contours=op['penProfile']['appearance']['contours']
                self.assertEqual(len(contours),len(path['expanded']))
                for contour,expanded in zip(contours,path['expanded']):
                    nodes=expanded['nodes'];first=next(i for i,n in enumerate(nodes) if n[2]!='offcurve')
                    self.assertEqual(nodes_from_commands(contour),nodes[first:]+nodes[:first])

    def test_public_centerline_pair_is_the_exact_explicit_projection(self):
        self.assertEqual(centerlines(self.font),load(ROOT/'examples/pen-profile-centerlines.opf.json'))

    def test_each_native_reference_renders_at_three_physical_scales(self):
        import xml.etree.ElementTree as ET
        for cap in (6,12,24):
            root=ET.fromstring(render_svg(self.font,'ABCDEFGHI',cap_height_mm=cap))
            paths=root.findall('{http://www.w3.org/2000/svg}path')
            self.assertEqual(len(paths),10) # Nine glyphs, I has body plus dot.
            self.assertTrue(all(p.get('fill-rule')=='nonzero' for p in paths))
            self.assertEqual(sum(p.get('d').count('M ') for p in paths),11) # Closed loop has inner/outer contours.

    def test_zero_length_native_seam_retains_its_control_address(self):
        op=next(g for g in self.font['glyphs'] if g['name']=='seam')['strokes'][0]
        self.assertEqual(op['commands'][-1],['L',*op['commands'][0][1:]])
        self.assertEqual(op['commands'][-2][-2:],op['commands'][0][1:])
        self.assertTrue(any(p['segment']==2 and p['t']==1 for p in op['penProfile']['points']))
