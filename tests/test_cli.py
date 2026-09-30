import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from plotfont import ValidationError, render_svg
from plotfont.hershey import import_roman_simplex
from test_plotfont import ROOT, example


class CLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-m', 'plotfont', *map(str, args)], cwd=ROOT, capture_output=True, text=True)

    def test_preserve_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'specimen.svg'
            output.write_text('existing drawing')
            result = self.run_cli('render', ROOT/'examples/minimal.plotfont.json', 'A', '-o', output)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(output.read_text(), 'existing drawing')
            result = self.run_cli('render', ROOT/'examples/minimal.plotfont.json', 'A', '-o', output, '--force')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('<svg', output.read_text())

    def test_invalid_font_reports_error_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'bad.plotfont.json'
            output = Path(directory)/'bad.svg'
            source.write_text('{"format":"PlotFont","version":"99"}')
            result = self.run_cli('render', source, 'A', '-o', output)
            self.assertEqual(result.returncode, 1)
            self.assertIn('version', result.stderr)
            self.assertFalse(output.exists())

    def test_changed_upstream_cannot_claim_pinned_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'changed.jhf'
            source.write_bytes((ROOT/'vendor/hershey/rowmans.jhf').read_bytes()+b'\n')
            with self.assertRaisesRegex(ValidationError, 'pinned'):
                import_roman_simplex(source)

    def test_invalid_xml_characters_rejected(self):
        for text in ('A\x00', 'A\ud800'):
            with self.assertRaisesRegex(ValidationError, 'XML'):
                render_svg(example(), text)
        font = example()
        font['glyphs'][2]['name'] = 'A\x01'
        with self.assertRaisesRegex(ValidationError, 'XML'):
            render_svg(font, 'A')
