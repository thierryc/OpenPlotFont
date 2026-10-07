from pathlib import Path
import json, sys, hashlib
from GlyphsApp import GSFont, Glyphs, LINE, CURVE, QCURVE, OFFCURVE
root = Path(params["root"])
sys.path.insert(0, str(root))
from openplotfont.glyphs_export import export_font
from openplotfont.comparison import compare_fonts
from openplotfont.validation import validate
catalog_path = root / "output/font-library/fonts/catalog.json"
catalog = json.loads(catalog_path.read_text())
dest = root / "output/font-library/mcp"
dest.mkdir(exist_ok=True)
report_path = dest / "qualification.json"
if report_path.exists():
    raise RuntimeError("MCP output already exists; reconcile the existing report instead of replaying")
(dest / "MCP-QUALIFICATION.py").write_text(params["sourceForRecord"])
types = {"line": LINE, "curve": CURVE, "qcurve": QCURVE, "offcurve": OFFCURVE}

class CachedGlyph:
    def __init__(self, native):
        self.native = native
        self.name = str(native.name)
        self.export = bool(native.export)
        self.rightKerningGroup = native.rightKerningGroup
        self.leftKerningGroup = native.leftKerningGroup
        if self.rightKerningGroup or self.leftKerningGroup:
            raise RuntimeError("This explicit-pair catalog verifier rejects class kerning")
    def __getattr__(self, key):
        return getattr(self.native, key)

class NativeReadProxy:
    # The catalog stores explicit glyph pairs only. Read the complete live native
    # table once, rather than issuing n-squared Objective-C pair queries.
    def __init__(self, native):
        self.native = native
        self.glyphs = [CachedGlyph(g) for g in native.glyphs]
        names = {str(g.id): str(g.name) for g in native.glyphs}
        names.update({str(g.name): str(g.name) for g in native.glyphs})
        self.pairs = {}
        master = str(native.masters[0].id)
        table = native.kerning or {}
        for left, rights in (table.get(master, {}) or {}).items():
            if str(left) not in names:
                raise RuntimeError("Unresolved native kerning left key: " + str(left))
            for right, value in rights.items():
                if str(right) not in names:
                    raise RuntimeError("Unresolved native kerning right key: " + str(right))
                self.pairs[(names[str(left)], names[str(right)])] = float(value)
    def __getattr__(self, key):
        return getattr(self.native, key)
    def kerningForPair(self, master, left, right):
        if str(master) != str(self.native.masters[0].id):
            raise RuntimeError("Unexpected master")
        return self.pairs.get((left, right))

report = {"transport": "Glyphs MCP server script.native.v1, live native bridge",
          "hostVersion": str(Glyphs.versionString), "hostBuild": str(Glyphs.buildNumber),
          "comparisonToleranceFontUnitsAfterNativeSave": 0.000501, "fonts": []}
def checkpoint():
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

for row in catalog["fonts"]:
    try:
        expected = json.loads((root / row["openplotfont"]).read_text())
        native = GSFont(str(root / row["package"]))
        actual = export_font(NativeReadProxy(native), native.masters[0].id, types)
        actual["version"] = "0.3"
        compare_fonts(expected, actual, tolerance=1e-8)
        package = dest / (row["id"] + ".glyphspackage")
        if package.exists():
            raise RuntimeError("MCP destination exists")
        native.save(str(package))
        reopened = GSFont(str(package))
        exported = export_font(NativeReadProxy(reopened), reopened.masters[0].id, types)
        exported["version"] = "0.3"
        compare_fonts(expected, exported, tolerance=0.000501)
        validate(exported)
        json_path = dest / (row["id"] + ".opf.json")
        json_path.write_text(json.dumps(exported, ensure_ascii=False, indent=2) + "\n")
        report["fonts"].append({"id": row["id"], "status": "pass", "glyphs": len(exported["glyphs"]),
            "kerningPairs": len(exported["kerning"]), "package": str(package.relative_to(root)),
            "openplotfont": str(json_path.relative_to(root)),
            "openplotfontSha256": hashlib.sha256(json_path.read_bytes()).hexdigest()})
    except Exception as error:
        report["fonts"].append({"id": row["id"], "status": "failed", "error": str(error)})
    checkpoint()

passed = sum(r["status"] == "pass" for r in report["fonts"])
report["passed"] = passed
report["total"] = len(catalog["fonts"])
checkpoint()
print(json.dumps({"passed": passed, "total": report["total"],
                 "failures": [r for r in report["fonts"] if r["status"] != "pass"]}))
if passed != report["total"]:
    raise RuntimeError("MCP qualification incomplete; inspect qualification.json")

# Promote only after the complete live-MCP batch has passed.
for row, verified in zip(catalog["fonts"], report["fonts"]):
    row["previousCliPackage"] = row.get("nativePackage")
    row["previousCliExport"] = row.get("nativeExport")
    row["nativePackage"] = verified["package"]
    row["nativeExport"] = verified["openplotfont"]
    row["qualificationTransport"] = report["transport"]
    row["status"] = "MCP native save/reopen geometry comparison passed"
catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")

# Refresh catalog links and bundles through this same MCP script, without CLI.
import zipfile
document_path = root / "docs/FONT_LIBRARY.md"
document = document_path.read_text()
old = "All packages were loaded, saved by Glyphs 4.1.1 (4108), reopened in a separate public CLI process, and compared against their source conversions."
new = "All packages were loaded, saved and reopened through the live Glyphs MCP server in Glyphs 4.1.1 (4108), then compared against their source conversions. Earlier CLI qualification is retained separately; the links below now point to the MCP-created copies."
document = document.replace(old, new)
document = document.replace("../output/font-library/native/qualification-reopen.json", "../output/font-library/mcp/qualification.json")
for row in catalog["fonts"]:
    for suffix in [".glyphspackage", ".opf.json"]:
        document = document.replace("../output/font-library/native/" + row["id"] + suffix,
                                    "../output/font-library/mcp/" + row["id"] + suffix)
from scripts.package_font_library import publication_document
document_path.write_text(publication_document(document))
(root / "output/font-library/FONT_LIBRARY.md").write_text(document.replace("../output/font-library/", "").replace("(USING_OPENPLOTFONT.md)", "(../../docs/USING_OPENPLOTFONT.md)"))

full_zip = root / "output/font-library/OpenPlotFont-stroke-library.zip"
with zipfile.ZipFile(full_zip, "w", zipfile.ZIP_DEFLATED) as aggregate:
    for row in catalog["fonts"]:
        key = row["id"]
        folder = (root / row["openplotfont"]).parent
        package = root / row["nativePackage"]
        entries = [(p, key + "/" + str(p.relative_to(folder))) for p in sorted(folder.rglob("*"))
                   if p.is_file() and ".glyphspackage" not in str(p.relative_to(folder))]
        entries += [(p, key + "/" + key + ".glyphspackage/" + str(p.relative_to(package)))
                    for p in sorted(package.rglob("*")) if p.is_file()]
        entries.append((root / row["nativeExport"], key + "/native-export.opf.json"))
        with zipfile.ZipFile(root / row["bundle"], "w", zipfile.ZIP_DEFLATED) as individual:
            for source, target in entries:
                individual.write(source, target)
                aggregate.write(source, target)
    archive_doc = document.replace("[Download the complete library](../output/font-library/OpenPlotFont-stroke-library.zip).", "This archive contains the complete library.").replace("[consumer responsibilities](USING_OPENPLOTFONT.md)", "the consumer responsibilities described above").replace("../output/font-library/mcp/qualification.json", "qualification-mcp.json")
    for row in catalog["fonts"]:
        key = row["id"]
        archive_doc = archive_doc.replace("../" + row["nativePackage"], key + "/" + key + ".glyphspackage").replace("../" + row["nativeExport"], key + "/native-export.opf.json").replace("../" + row["bundle"], key + "/README.md").replace("../output/font-library/fonts/" + key + "/", key + "/")
    aggregate.writestr("FONT_LIBRARY.md", archive_doc)
    aggregate.write(report_path, "qualification-mcp.json")
print("MCP packages, catalog and bundles updated; all 87 fonts verified.")
