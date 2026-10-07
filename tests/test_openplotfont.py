import copy
import json
import math
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from openplotfont import load, validate, render_svg, ValidationError
from openplotfont.hershey import import_roman_simplex, parse_jhf
from openplotfont.glyphs_export import node_commands, operations_from_paths, export_font

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://www.w3.org/2000/svg"}


def example(name="minimal"):
    return load(ROOT / "examples" / (name + ".opf.json"))


class ValidationTests(unittest.TestCase):
    def test_examples(self):
        for path in (ROOT / "examples").glob("*.json"):
            self.assertIsInstance(load(path), dict)

    def test_semantic_failures(self):
        mutations = [
            ("expected OpenPlotFont", lambda f: f.update(format="OpenPlotFont"[4:])),
            ("version", lambda f: f.update(version="0.1")),
            ("fallback", lambda f: f.update(missingGlyph="absent")),
            ("Unicode", lambda f: f["glyphs"][2].update(unicodes=["D800"])),
            ("Unicode", lambda f: f["glyphs"][2].update(unicodes=["000041"])),
            ("duplicate", lambda f: f["glyphs"][2].update(unicodes=["0020"])),
            ("finite", lambda f: f["glyphs"][2].update(advanceWidth=float("inf"))),
            ("arity", lambda f: f["glyphs"][2]["strokes"][0]["commands"].append(["L",1])),
            ("M must", lambda f: f["glyphs"][2]["strokes"][0]["commands"].append(["M",1,2])),
            ("connection", lambda f: f["glyphs"][2].update(connections={"entry":{"strokeIndex":9,"endpoint":"start"}})),
            ("kerning", lambda f: f.update(kerning=[{"left":"absent","right":"A","value":-20}])),
            ("object", lambda f: f["glyphs"][2].update(userData=[])),
            ("duplicate anchor", lambda f: f["glyphs"][2].update(anchors=[{"name":"top","x":0,"y":1}]*2)),
            ("kind", lambda f: f["glyphs"][2]["strokes"][0].update(kind="unknown")),
            ("integer", lambda f: f.update(unitsPerEm=True)),
        ]
        for message, mutate in mutations:
            with self.subTest(message=message):
                f = example()
                mutate(f)
                with self.assertRaisesRegex(ValidationError, message):
                    validate(f)

    def test_fill_constraints_and_connection(self):
        font = example("mixed")
        font["glyphs"][2]["strokes"][1]["contours"][0]["closed"] = False
        with self.assertRaisesRegex(ValidationError, "closed"):
            validate(font)
        font = example("mixed")
        font["glyphs"][2]["connections"] = {"exit":{"strokeIndex":1,"endpoint":"end"}}
        with self.assertRaisesRegex(ValidationError, "open stroke"):
            validate(font)

    def test_duplicate_json_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "bad.json"
            for content in ('{"version":"0.2","version":"0.1"}', '{"x": NaN}', '{"x": 1e999}'):
                p.write_text(content)
                with self.assertRaises(ValidationError):
                    load(p)

    def test_unknown_metadata_preserved(self):
        f = example()
        f["extension"] = {"editor": [True, None, 0.125]}
        before = copy.deepcopy(f)
        self.assertIs(validate(f), f)
        self.assertEqual(f, before)


class RenderTests(unittest.TestCase):
    def paths(self, font, text, **options):
        return ET.fromstring(render_svg(font, text, **options)).findall("s:path", NS)

    def test_stroke_boundaries_scaling_and_axis(self):
        paths = self.paths(example(), "A", cap_height_mm=14)
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0].get("d"), "M 1 0 L 6 -14 L 11 0")
        self.assertEqual(paths[1].get("d"), "M 3 -5.6 L 9 -5.6")

    def test_closed_fallback(self):
        paths = self.paths(example(), "☃")
        self.assertEqual(len(paths), 1)
        self.assertTrue(paths[0].get("d").endswith("Z"))
        self.assertEqual(paths[0].get("fill"), "none")

    def test_space_kerning_and_multiline(self):
        font = example()
        font["kerning"] = [{"left":"A","right":"A","value":-50}]
        paths = self.paths(font, "AA", cap_height_mm=700)
        self.assertTrue(paths[2].get("d").startswith("M 650 0"))
        paths = self.paths(font, "A A\nA", cap_height_mm=700)
        self.assertEqual(len(paths), 6)
        self.assertTrue(paths[2].get("d").startswith("M 1050 0"))
        self.assertTrue(paths[4].get("d").startswith("M 50 1200"))

    def test_curves_and_optional_join(self):
        font = example("script")
        self.assertEqual(len(self.paths(font, "un")), 2)
        joined = self.paths(font, "un", join=True)
        self.assertEqual(len(joined), 1)
        self.assertEqual(joined[0].get("d").count("M"), 1)
        self.assertIn("C", joined[0].get("d"))
        self.assertEqual(len(self.paths(font, "u n", join=True)), 2)
        self.assertEqual(len(self.paths(font, "u\nn", join=True)), 2)
        font["glyphs"][2]["advanceWidth"] += 5
        with self.assertRaisesRegex(ValidationError, "connector policy"):
            render_svg(font, "un", join=True)

    def test_quadratic_and_fill_holes(self):
        font = example("mixed")
        font["glyphs"][2]["strokes"][0]["commands"][1] = ["Q",100,200,200,450]
        paths = self.paths(font, "i")
        self.assertIn("Q", paths[0].get("d"))
        self.assertEqual(paths[1].get("fill-rule"), "evenodd")
        self.assertEqual(paths[1].get("stroke"), "none")
        self.assertEqual(paths[1].get("d").count("M"), 2)
        self.assertEqual(paths[1].get("d").count("Z"), 2)

    def test_bounds_include_overhangs_and_control_hulls(self):
        font = example()
        font["glyphs"][2]["strokes"][0]["commands"] = [["M",-300,-500],["C",-1000,3000,2000,3000,500,-500]]
        tree = ET.fromstring(render_svg(font,"A",cap_height_mm=700))
        x,y,w,h = map(float,tree.get("viewBox").split())
        self.assertLess(x,-1000)
        self.assertLess(y,-3000)
        self.assertGreater(x+w,2000)
        self.assertGreater(y+h,500)

    def test_invalid_size_tabs_and_empty_text(self):
        for value in (0,-1,float("nan")):
            with self.assertRaises(ValidationError):
                render_svg(example(), "A", value)
        with self.assertRaisesRegex(ValidationError,"tabs"):
            render_svg(example(), "A\tA")
        self.assertEqual(len(self.paths(example(), "")), 0)


class HersheyTests(unittest.TestCase):
    def test_full_repertoire_and_exact_geometry(self):
        source = ROOT / "vendor/hershey/rowmans.jhf"
        font = import_roman_simplex(source)
        stored = load(ROOT / "fonts/hershey-roman-simplex/HersheyRomanSimplex.opf.json")
        self.assertEqual(font, stored)
        records = parse_jhf(source.read_text())
        self.assertEqual(len(font["glyphs"]), 97)
        self.assertEqual(sum(len(g["unicodes"]) for g in font["glyphs"]), 95)
        self.assertEqual(font["glyphs"][-1]["unicodes"], [])
        scale = 50
        for record, glyph in zip(records,font["glyphs"][1:]):
            self.assertAlmostEqual(glyph["advanceWidth"] / scale,record["right"]-record["left"])
            for stroke, op in zip(record["strokes"],glyph["strokes"]):
                self.assertFalse(op["closed"])
                for point, cmd in zip(stroke,op["commands"]):
                    self.assertAlmostEqual(cmd[1]/scale+record["left"],point[0])
                    self.assertAlmostEqual(9-cmd[2]/scale,point[1])

    def test_malformed_source(self):
        with self.assertRaisesRegex(ValidationError,"count"):
            parse_jhf("  699  2JZ")


class ExportGeometryTests(unittest.TestCase):
    def test_fractional_cubic_closed_segment(self):
        cmds = node_commands([('curve',0.125,0),('line',1.5,2),('offcurve',2,3),('offcurve',-2,3)], True)
        self.assertEqual(cmds[-1], ['C',2,3,-2,3,0.125,0])

    def test_implied_quadratics(self):
        cmds = node_commands([('line',0,0),('offcurve',10,20),('offcurve',30,20),('qcurve',40,0)],False)
        self.assertEqual(cmds,[['M',0,0],['Q',10,20,20,20],['Q',30,20,40,0]])

    def test_no_implicit_reordering_or_invalid_controls(self):
        for nodes in ([('offcurve',0,0),('line',1,1)], [('line',0,0),('curve',1,1)]):
            with self.assertRaises(ValidationError):
                node_commands(nodes,False)

    def test_annotation_grouping_and_coverage(self):
        paths = [op for op in example()["glyphs"][2]["strokes"]]
        operations = operations_from_paths(paths,[{"kind":"stroke","pathIndex":1},{"kind":"stroke","pathIndex":0}])
        self.assertEqual(operations[0]["commands"],paths[1]["commands"])
        with self.assertRaisesRegex(ValidationError,"every path"):
            operations_from_paths(paths,[{"kind":"stroke","pathIndex":0}])
        with self.assertRaisesRegex(ValidationError,"duplicate"):
            operations_from_paths(paths,[{"kind":"fill","pathIndices":[0,0],"fillRule":"evenodd"}])


class SchemaTests(unittest.TestCase):
    def test_schema_and_examples(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("Install requirements-dev.txt to verify the JSON Schema")
        schemas = {version:json.loads((ROOT/'schemas'/f'openplotfont-{version}.schema.json').read_text())
                   for version in ('0.2','0.3')}
        for schema in schemas.values():
            jsonschema.Draft202012Validator.check_schema(schema)
        for path in list((ROOT / "examples").glob("*.json")) + list((ROOT / "fonts").rglob("*.json")):
            value = json.loads(path.read_text())
            jsonschema.validate(value,schemas[value['version']])
        font = example()
        font["glyphs"][2]["strokes"][0]["commands"].append(["M",1,2])
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(font,schemas['0.2'])


if __name__ == "__main__":
    unittest.main()
