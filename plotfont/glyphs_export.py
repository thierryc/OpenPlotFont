"""Glyphs 4 selected-master adapter. Native execution is separately qualified."""

import json
from .validation import validate, ValidationError


def plain(value):
    """Convert property-list containers; reject non-JSON binary/editor objects."""
    if value is None:
        return None
    for kind in (str, bool, int, float):
        if isinstance(value, kind):
            return kind(value)
    if hasattr(value, "keys"):
        if not all(isinstance(k, str) for k in value.keys()):
            raise ValidationError("Glyphs user data: expected string keys")
        return {k: plain(value[k]) for k in value.keys()}
    if isinstance(value, (bytes, bytearray)):
        raise ValidationError("Glyphs user data: binary values cannot be exported as JSON")
    if hasattr(value, "__iter__"):
        return [plain(item) for item in value]
    raise ValidationError(f"Glyphs user data: unsupported {type(value).__name__}")


def node_commands(nodes, closed):
    """Nodes are (kind, x, y); implied quadratic midpoints are explicit."""
    if not nodes or nodes[0][0] == "offcurve":
        raise ValidationError("path: explicit on-curve start node required; start order is not rotated automatically")
    commands = [["M", *nodes[0][1:]]]
    controls = []
    remaining = list(nodes[1:]) + ([nodes[0]] if closed else [])
    for i, (kind, x, y) in enumerate(remaining):
        if kind == "offcurve":
            controls.append((x, y))
        elif kind == "line":
            if controls:
                raise ValidationError("path: off-curve controls before line node")
            if not (closed and i == len(remaining) - 1):
                commands.append(["L", x, y])
        elif kind == "curve":
            if len(controls) != 2:
                raise ValidationError("path: cubic segment requires two controls")
            commands.append(["C", *controls[0], *controls[1], x, y])
            controls = []
        elif kind == "qcurve":
            if not controls:
                raise ValidationError("path: quadratic segment requires controls")
            for a, b in zip(controls, controls[1:]):
                commands.append(["Q", *a, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2])
            commands.append(["Q", *controls[-1], x, y])
            controls = []
        else:
            raise ValidationError(f"path: unsupported node type {kind}")
    if controls:
        raise ValidationError("path: dangling off-curve nodes")
    if len(commands) < 2:
        raise ValidationError("path: no drawable segment")
    return commands


def operations_from_paths(paths, plan=None):
    """A plan assigns every path exactly once; closure never implies fill."""
    if plan is None:
        return [{"kind": "stroke", **path} for path in paths]
    result, used = [], set()
    if not isinstance(plan, list):
        raise ValidationError("org.plotfont.glyph.operations must be an array")
    for item in plan:
        if not isinstance(item, dict) or item.get("kind") not in ("stroke", "fill"):
            raise ValidationError("invalid Glyphs drawing-operation annotation")
        indices = [item.get("pathIndex")] if item["kind"] == "stroke" else item.get("pathIndices")
        if not isinstance(indices, list) or not indices:
            raise ValidationError("operation must reference paths")
        for index in indices:
            if type(index) is not int or not 0 <= index < len(paths) or index in used:
                raise ValidationError(f"invalid or duplicate annotated path index {index!r} ({type(index).__name__}), path count {len(paths)}")
            used.add(index)
        if item["kind"] == "stroke":
            result.append({"kind": "stroke", **paths[indices[0]]})
        else:
            result.append({"kind": "fill", "fillRule": item.get("fillRule"), "contours": [paths[i] for i in indices]})
    if len(used) != len(paths):
        raise ValidationError("operation annotations must cover every path exactly once")
    return result


def export_font(font, master_id, node_types):
    """Export one exact master; never save or edit the source font."""
    master = next((m for m in font.masters if m.id == master_id), None)
    if master is None:
        raise ValidationError("Glyphs export: selected master does not exist")
    meta = plain(font.userData.get("org.plotfont.font", {}))
    if not isinstance(meta, dict):
        raise ValidationError("org.plotfont.font must be an object")
    exported = [g for g in font.glyphs if g.export or g.name == meta.get("missingGlyph", ".notdef")]

    def check_components(glyph, chain):
        if glyph.name in chain:
            raise ValidationError("component cycle: " + " → ".join((*chain, glyph.name)))
        if len(chain) >= 64:
            raise ValidationError("component nesting exceeds 64 levels")
        layer = glyph.layers[master_id]
        if layer is None:
            raise ValidationError(f"{glyph.name}: missing master layer")
        for component in layer.components:
            child = font.glyphs[component.componentName]
            if child is None:
                raise ValidationError(f"{glyph.name}: unresolved component {component.componentName}")
            check_components(child, (*chain, glyph.name))

    glyphs = []
    for glyph in exported:
        check_components(glyph, ())
        original = glyph.layers[master_id]
        data = plain(glyph.userData)
        annotations = data.get("org.plotfont.glyph", {})
        if not isinstance(annotations, dict):
            raise ValidationError(f"{glyph.name}: org.plotfont.glyph must be an object")
        if original.components and annotations:
            raise ValidationError(f"{glyph.name}: resolve annotated components in the authoring source before export")
        layer = original.copyDecomposedLayer()
        if layer.components or len(layer.shapes) != len(layer.paths):
            raise ValidationError(f"{glyph.name}: unsupported or unresolved shapes")
        if getattr(layer, "hints", []):
            raise ValidationError(f"{glyph.name}: hints/corner components require explicit resolution")
        paths = []
        for path_index, path in enumerate(layer.paths):
            nodes = []
            for node in path.nodes:
                kind = next((name for name, constant in node_types.items() if node.type == constant), None)
                if kind is None:
                    raise ValidationError(f"{glyph.name} path {path_index}: unsupported native node type")
                nodes.append((kind, float(node.position.x), float(node.position.y)))
            paths.append({"closed": bool(path.closed), "commands": node_commands(nodes, bool(path.closed))})
        record = {"name": glyph.name, "unicodes": [f"{int(u, 16):04X}" for u in (glyph.unicodes or [])],
                  "advanceWidth": float(layer.width), "strokes": operations_from_paths(paths, annotations.get("operations"))}
        if data:
            record["userData"] = data
        if "connections" in annotations:
            record["connections"] = annotations["connections"]
        anchors = []
        for anchor in layer.anchors:
            entry = {"name": anchor.name, "x": float(anchor.position.x), "y": float(anchor.position.y)}
            user_data = plain(anchor.userData)
            if user_data:
                entry["userData"] = user_data
            anchors.append(entry)
        if anchors:
            record["anchors"] = anchors
        glyphs.append(record)

    # Resolve class pairs explicitly: glyph/glyph, glyph/class, class/glyph, class/class.
    pairs = []
    for left in exported:
        for right in exported:
            left_class = "@MMK_L_" + left.rightKerningGroup if left.rightKerningGroup else None
            right_class = "@MMK_R_" + right.leftKerningGroup if right.leftKerningGroup else None
            candidates = [(left.name, right.name), (left.name, right_class), (left_class, right.name), (left_class, right_class)]
            for lkey, rkey in candidates:
                if lkey is None or rkey is None:
                    continue
                value = font.kerningForPair(master_id, lkey, rkey)
                if value is not None:
                    if value != 0:
                        pairs.append({"left": left.name, "right": right.name, "value": float(value)})
                    break
    active_features = [feature.name for feature in font.features if not feature.disabled]
    result = {"format": "PlotFont", "version": "0.2", "id": meta.get("id", ""),
              "familyName": font.familyName, "styleName": meta.get("styleName", master.name),
              "unitsPerEm": int(font.upm), "metrics": {
                  "ascender": float(master.ascender), "descender": float(master.descender),
                  "capHeight": float(master.capHeight), "xHeight": float(master.xHeight), "lineGap": meta.get("lineGap", 0)},
              "missingGlyph": meta.get("missingGlyph", ".notdef"), "glyphs": glyphs, "kerning": pairs,
              "metadata": meta.get("metadata", {})}
    if not isinstance(result["metadata"], dict):
        raise ValidationError("org.plotfont.font.metadata must be an object")
    # Copy before adding export diagnostics; never mutate font.userData.
    result = json.loads(json.dumps(result, allow_nan=False))
    result["metadata"]["glyphsMasterId"] = str(master_id)
    result["metadata"]["exportWarnings"] = (["OpenType features not executed: " + ", ".join(active_features)] if active_features else [])
    return validate(result)
