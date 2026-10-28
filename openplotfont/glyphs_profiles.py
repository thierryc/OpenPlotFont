"""Glyphs 4 Pen-point capture; never mutate or expand the authoring source."""
import math
import sys
from .validation import ValidationError
from .profiles import CHANNELS, appearance_binding


def native_value(obj, name, default=None):
    value = getattr(obj, name, default)
    return value() if callable(value) else value


def pen_points(node):
    return list(native_value(node, 'associatedPenPoints', []) or [])


def has_profile(path):
    attrs = getattr(path, 'attributes', {}) or {}
    return attrs.get('strokeWidth') is not None or any(pen_points(n) for n in path.nodes)


def precise_position(node):
    return native_value(node, 'positionPrecise', node.position)


def native_path(path, node_types, *, appearance=False):
    from .glyphs_export import node_commands
    nodes = []
    for node in path.nodes:
        kind = next((k for k,v in node_types.items() if node.type == v), None)
        if kind is None:
            raise ValidationError('profile: unsupported native node type')
        pos = precise_position(node)
        nodes.append((kind, float(pos.x), float(pos.y)))
    if appearance and nodes and nodes[0][0] == 'offcurve':
        first = next((i for i,n in enumerate(nodes) if n[0] != 'offcurve'), None)
        if first is None:
            raise ValidationError('profile: appearance has no explicit oncurve')
        nodes = nodes[first:]+nodes[:first]
    return {'closed':bool(path.closed), 'commands':node_commands(nodes, bool(path.closed))}


def capture_profile(path, operation, node_types, *, source_identity='Glyphs 4'):
    """Retain nullable native channels and exact native-expanded appearance.

    Native controls use the ending oncurve node plus local t. Implied quadratic
    conversion and component profile transforms are deliberately rejected until
    their value remapping is qualified.
    """
    attrs = getattr(path, 'attributes', {}) or {}
    width = attrs.get('strokeWidth')
    if width is None or not math.isfinite(float(width)) or float(width) <= 0:
        raise ValidationError('penProfile: set an explicit positive path strokeWidth before exporting Pen points')
    width = float(width)
    defaults = {'width':width, 'height':float(attrs.get('strokeHeight',width)),
                'angle':float(attrs.get('strokeAngle',0)), 'strokePosition':float(attrs.get('strokePos',0)),
                'progressionIn':0., 'progressionOut':0.}
    caps = {0:'butt',1:'round',2:'square'}
    joins = {0:'miter',1:'round',2:'bevel'}
    try:
        style = {'capStart':caps[int(attrs.get('lineCapStart',0))],
                 'capEnd':caps[int(attrs.get('lineCapEnd',0))], 'join':joins[int(attrs.get('lineJoin',0))]}
    except KeyError as e:
        raise ValidationError('penProfile: unsupported native cap/join; Round Full and custom joins need qualification') from e
    end_nodes = []
    for index,node in enumerate(path.nodes):
        kind = next((k for k,v in node_types.items() if node.type == v), None)
        if kind == 'qcurve' and any(pen_points(n) for n in path.nodes):
            raise ValidationError('penProfile: quadratic/implied-point mapping is not qualified; use explicit cubic authoring')
        if index and kind != 'offcurve':
            end_nodes.append(index)
    if path.closed:
        end_nodes.append(0)
    mapping = {node:segment for segment,node in enumerate(end_nodes)}
    points = []
    for index,node in enumerate(path.nodes):
        for pp in pen_points(node):
            if index not in mapping:
                raise ValidationError('penProfile: point is not attached to a qualified ending oncurve node')
            values = {}
            for key in CHANNELS:
                value = float(native_value(pp,key))
                if value == sys.float_info.max:
                    values[key] = None
                elif not math.isfinite(value):
                    raise ValidationError('penProfile: nonfinite native channel '+key)
                else:
                    values[key] = value
            points.append({'segment':mapping[index], 't':float(native_value(pp,'t')), 'values':values})
    points.sort(key=lambda p:(p['segment'],p['t']))
    profile = {'version':'1', 'model':'glyphs4-v1', 'defaults':defaults, 'points':points, 'style':style}
    operation['penProfile'] = profile
    expanded = native_value(path, 'expandedStroke')
    if expanded is None:
        raise ValidationError('penProfile: native expandedStroke is required for a faithful appearance reference')
    profile['appearance'] = {'source':source_identity, 'bindingSha256':appearance_binding(operation),
                             'fillRule':'nonzero', 'contours':[native_path(p,node_types,appearance=True) for p in expanded]}
    return profile
