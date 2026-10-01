"""Shared export action for the Glyphs 4 plugin; no UI or source mutation."""
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from .glyphs_export import export_font, plain
from .storage import write_font
from .validation import ValidationError


def export_to_path(font, master_id, destination, node_types):
    destination = Path(destination)
    if not destination.is_absolute() or not str(destination).endswith('.plotfont.json'):
        raise ValidationError('Choose an absolute destination ending in .plotfont.json.')
    master = next((m for m in font.masters if m.id == master_id), None)
    if master is None:
        raise ValidationError('Choose an existing master; instance interpolation is not supported.')
    # All defaults and decomposition apply to an invisible copy only.
    copied = font.copy()
    settings = plain(copied.userData.get('org.plotfont.font', {}))
    if not isinstance(settings, dict):
        raise ValidationError('org.plotfont.font must be an object.')
    if 'id' not in settings:
        identity = str(font.familyName) + '\n' + str(master.name)
        settings['id'] = 'org.plotfont.' + str(uuid5(NAMESPACE_URL, identity))
    copied.userData['org.plotfont.font'] = settings
    data = export_font(copied, master_id, node_types)
    write_font(destination, data)
    return data
