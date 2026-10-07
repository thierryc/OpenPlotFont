import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from openplotfont import ValidationError, load
from openplotfont.storage import write_font, write_output
from test_openplotfont import example


class StorageTests(unittest.TestCase):
    def test_valid_font_roundtrip_and_preserve_existing_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'font.opf.json'
            write_font(path, example())
            self.assertEqual(load(path), example())
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                write_font(path, example('script'))
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(len(list(Path(directory).iterdir())), 1)

    def test_failed_validation_and_encoding_leave_no_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'bad.opf.json'
            with self.assertRaises(ValidationError):
                write_font(path, {'version':'99'})
            with self.assertRaises(UnicodeError):
                write_output(path, '\ud800')
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_publication_failure_cleans_staging_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'font.opf.json'
            with patch('openplotfont.storage.os.link', side_effect=OSError('simulated filesystem failure')):
                with self.assertRaises(OSError):
                    write_font(path, example())
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_force_replaces_output_and_preserves_symlink_target(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)/'original.txt'
            path = Path(directory)/'drawing.svg'
            target.write_text('original')
            path.symlink_to(target)
            with self.assertRaises(FileExistsError):
                write_output(path, 'new')
            write_output(path, 'new', force=True)
            self.assertEqual(target.read_text(), 'original')
            self.assertEqual(path.read_text(), 'new')
            self.assertFalse(path.is_symlink())
