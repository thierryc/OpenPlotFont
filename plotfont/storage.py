"""Publish a complete validated font or drawing without exposing partial output."""
import json
import os
import tempfile
from pathlib import Path
from .validation import validate


def write_output(path, content, *, force=False, create_parents=False):
    destination = Path(path)
    encoded = content.encode('utf-8')  # Fail before touching the filesystem.
    if create_parents:
        destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.plotfont-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        if force:
            os.replace(temporary, destination)
        else:
            # An atomic same-filesystem link refuses existing destinations, including symlinks.
            os.link(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_font(path, font, *, force=False, create_parents=False):
    validate(font)
    content = json.dumps(font, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    write_output(path, content, force=force, create_parents=create_parents)
