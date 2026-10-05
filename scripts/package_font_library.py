"""Create the review catalog and distributable bundles after native qualification."""
from html import escape
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'output/font-library'


def publication_document(document):
    """Link repository readers to published bundles instead of ignored output."""
    website = 'https://plotfont.litsquare.com/'
    document = re.sub(r'\[Qualification report\]\((\.\./output/[^)]+)\)',
                      lambda match: 'Local qualification report: `' + match[1][3:] + '`', document)
    document = document.replace(
        '[Download the complete library](../output/font-library/PlotFont-stroke-library.zip).',
        f'[Download individual fonts from the website]({website}#fonts). '
        'The complete local archive is `output/font-library/PlotFont-stroke-library.zip`.')
    document = re.sub(
        r'\[ZIP\]\(\.\./output/font-library/bundles/([^/)]+)\.zip\) · '
        r'\[Glyphs\]\([^)]+\) · \[PlotFont\]\([^)]+\) · \[preview\]\([^)]+\)',
        lambda match: f'[ZIP (Glyphs and PlotFont)]({website}assets/catalog/{match[1]}.zip) · '
                      f'[preview]({website}assets/catalog/{match[1]}.svg)', document)
    document = re.sub(r'\]\(\.\./output/font-library/fonts/([^/]+)/README\.md\)',
                      lambda match: f']({website}assets/catalog/{match[1]}.zip)', document)
    return '\n'.join(line.rstrip() for line in document.splitlines()) + '\n'


def main():
    catalog = json.loads((BASE / 'fonts/catalog.json').read_text())
    report_file = BASE / 'mcp/qualification.json' if (BASE / 'mcp/qualification.json').exists() else BASE / 'native/qualification-reopen.json'
    report = json.loads(report_file.read_text())
    qualified = {r['id']: r for r in report['fonts'] if r['status'] == 'pass'}
    if len(qualified) != len(catalog['fonts']):
        raise SystemExit('Every catalog font must pass native reopen qualification first')
    bundles = BASE / 'bundles'; bundles.mkdir(exist_ok=True)
    lines = ['# Converted stroke-font library', '',
        'Built and reviewed 2026-10-01. **87 fonts**: 32 JHF Hershey files, 12 Hershey-related SVGs, 29 EMS SVGs, Relief Regular and Ornament, NormStroke, three Custom fonts, three Cutlings fonts, one DearPlotter design, and four LibreCAD LFF fonts. These are 87 converted source files; some Hershey aliases and SVG adaptations overlap in design.', '',
        'Every row has a PlotFont 0.3 export and an editable format-4 Glyphs package. All packages were loaded, saved and reopened through the live Glyphs MCP server in Glyphs 4.1.1 (4108), then compared against their source conversions. Coordinates in native saved packages are rounded to 0.001 font units; comparisons allow 0.000501 font units per numeric value. The primary PlotFont JSON retains the higher precision source conversion. [Qualification report](../output/font-library/mcp/qualification.json).', '',
        '[Download the complete library](../output/font-library/PlotFont-stroke-library.zip). Each individual ZIP includes original source, full notices, attribution, Glyphs package, PlotFont JSON, native JSON export, specimen and glyph atlas. Generated files are local, ignored by Git and reproducible using the scripts below.', '',
        '## Drawing and machine interoperability', '',
        'These are reviewed stroke sources, with independent pen-down trajectories, explicit closure, source path order/start points/direction, spaces, advances and supported kerning retained. Cubic and quadratic curves remain curves. SVG/LFF arcs become tangent-matched cubic segments of at most 5°; conservative error allowance is 1e-7 × maximum radius in source units. No outline skeletonization or stroke-width expansion is performed.', '',
        'PlotFont geometry is in font units with Y up. The specimens demonstrate physical sizing at an 8 mm cap height and convert to SVG page coordinates. CNC/plotter consumers must preserve each trajectory and lift the pen/tool between strokes, size geometry physically, and apply device motion settings outside the font. A closed stroke remains a trajectory, not a filled area. This repository supplies portable geometry and SVG review output; it does not generate G-code/HPGL or operate hardware. Machine compatibility has not been tested on hardware. See [consumer responsibilities](USING_PLOTFONT.md).', '',
        '**Coverage limits:** 14 non-Latin/symbol JHF sources use temporary U+E000 + source-row mappings, explicitly recorded in each font. Their geometry is usable through the glyph atlas/private-use mapping; standard Greek, Cyrillic, Japanese and symbol text mapping is not qualified. Original JHF records beyond printable ASCII are retained. SVG ligatures and unencoded alternates retain drawings and source metadata but have no automatic substitutions. Scripts preserve pen lifts and have no automatic joining. JHF x-height is estimated at half cap height, and non-Latin JHF baseline/cap metrics are estimates. LFF line metrics are explicit conversion estimates; origins and LibreCAD xMax + LetterSpacing advances are retained. Font bounds can exceed nominal cap/ascender metrics.', '',
        '## Licensing and attribution', '',
        'Conversions keep the upstream font licenses. Full available copyright/license notices are embedded in PlotFont metadata and Glyphs font user data, copied beside the fonts, and embedded in specimen/atlas SVG metadata. Original sources retain their notices. Distribute the whole ZIP/folder; the project MIT license does not replace these font terms. PF prefixes distinguish converted SVG/CAD family names from their source font names.', '',
        '- **Hershey:** Dr. A. V. Hershey; JHF representation by James Hurt, Cognition, Inc.; SVG adaptations retain their source credits. Complete acknowledgment/use restriction is included, including the prohibition on recreating the original NTIS representation.',
        '- **OFL:** retain author/copyright notices and the full OFL; modified fonts remain OFL and honor reserved font names. Font software cannot be sold by itself. Each ZIP includes available ancestor notices. EMS Elfin retains both the stroke derivative’s OFL declaration and its Mountains of Christmas ancestor’s Apache 2.0 notice; this is not a claim that the ancestor was OFL.',
        '- **CC0:** NormStroke retains octycs’ CC0 declaration and ISO3098/Wikimedia ancestry credits.',
        '- **GPL v2 or later:** the two LibreCAD ISO3098 fonts include GPL text and the original LFF source. Keep source available with redistribution and retain author/license headers.',
        '- **DearPlotter:** the font is OFL; Licia He’s generator and Golan Levin’s adaptation have CC BY-SA 4.0 credits in the retained source metadata. No generator code is included in the font bundle.', '',
        'The supplied EMS and Custom OFL templates have unfilled copyright fields. Source metadata supplies the declared authors and ancestry; these are retained with available ancestor notices. The Custom font template also has unfilled copyright fields. Its explicit upstream font license declaration, Shriinivas’ attribution, Pinyon Script/Square Grotesk ancestry and complete upstream README are retained rather than inventing copyright ownership.', '',
        '## Individual fonts', '',
        '| Font / glyph count | License | Original repository / author links | Files |',
        '| --- | --- | --- | --- |']
    full_zip = BASE / 'PlotFont-stroke-library.zip'
    credits = []
    with zipfile.ZipFile(full_zip, 'w', zipfile.ZIP_DEFLATED) as aggregate:
        for row in catalog['fonts']:
            key = row['id']; folder = ROOT / row['plotfont']; folder = folder.parent
            native = ROOT / qualified[key]['package']; native_json = ROOT / qualified[key]['plotfont']
            entries = [(p, f'{key}/{p.relative_to(folder)}') for p in sorted(folder.rglob('*')) if p.is_file() and '.glyphspackage' not in str(p.relative_to(folder))]
            entries += [(p, f'{key}/{key}.glyphspackage/{p.relative_to(native)}') for p in sorted(native.rglob('*')) if p.is_file()]
            entries.append((native_json, f'{key}/native-export.plotfont.json'))
            bundle = bundles / (key + '.zip')
            with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as individual:
                for source, target in entries:
                    individual.write(source, target); aggregate.write(source, target)
            author_links = ' · '.join(f'[author/source {i+1}]({u})' for i,u in enumerate(dict.fromkeys(row['authorLinks'])))
            lines.append(f'| {row["family"]} ({row["glyphs"]}) | {row["license"]} | [repository]({row["source"]}) · {author_links} | [ZIP](../{bundle.relative_to(ROOT)}) · [Glyphs](../{native.relative_to(ROOT)}) · [PlotFont](../{row["plotfont"]}) · [preview](../{row["specimen"]}) |')
            credits += [f'### {row["family"]}', '', 'Source credits retained verbatim:', '', '```text', row['attribution'].strip(), '```', '', f'[Complete notices and source]({"../"+str(folder.relative_to(ROOT))+"/README.md"})', '']
            row['nativePackage'] = str(native.relative_to(ROOT)); row['nativeExport'] = str(native_json.relative_to(ROOT)); row['bundle'] = str(bundle.relative_to(ROOT)); row['status'] = 'native saved/reopened geometry comparison passed'
    lines += ['', '## Deferred or excluded', '']
    for row in catalog['deferred']:
        lines.append(f'- `{row["source"]}` — {row["reason"]}')
    lines += ['', 'LingDong’s outline-derived skeleton collection, fonts with unknown rights, ROM/SHX extracts and the unreviewed remainder of the LibreCAD library remain outside this batch. Ordinary Google Fonts outline files are not converted into centerlines: the imported EMS files are existing stroke derivatives from Oskay’s repository.', '',
        '## Reproduce', '',
        'Install the optional build dependencies with `python3 -m pip install ".[library]"`. Then run:', '', '```sh',
        'python3 scripts/fetch_font_library.py', 'python3 scripts/build_font_library.py',
        'python3 scripts/run_font_library_qualification.py --glyphs-command /path/to/glyphs --app "/Applications/Glyphs 4.app"',
        'python3 scripts/package_font_library.py', '```', '',
        'The digest lock pins every downloaded source and required notice. Existing changed source files fail SHA-256 validation. Builds refuse an existing destination; use a new build directory or preserve/remove your previous generated output first. Qualification uses the standard `fonts/` catalog; a custom build destination needs its catalog copied into that location before qualification. The public Glyphs CLI loads inputs with `-i`; the qualifier does not attach to GUI documents. No font binaries are installed and no original source is modified.', '',
        '## Per-font source credits', ''] + credits
    document = '\n'.join(lines)+'\n'
    (ROOT / 'docs/FONT_LIBRARY.md').write_text(publication_document(document))
    (BASE / 'FONT_LIBRARY.md').write_text(document.replace('../output/font-library/', '').replace('(USING_PLOTFONT.md)', '(../../docs/USING_PLOTFONT.md)'))
    archive_document = document.replace('[Download the complete library](../output/font-library/PlotFont-stroke-library.zip).', 'This archive contains the complete library.').replace('[consumer responsibilities](USING_PLOTFONT.md)', 'the consumer responsibilities described above').replace('../output/font-library/mcp/qualification.json', 'qualification-reopen.json')
    for row in catalog['fonts']:
        key = row['id']
        archive_document = archive_document.replace('../' + row['nativePackage'], key + '/' + key + '.glyphspackage').replace('../' + row['nativeExport'], key + '/native-export.plotfont.json').replace('../' + row['bundle'], key + '/README.md').replace('../output/font-library/fonts/' + key + '/', key + '/')
    with zipfile.ZipFile(full_zip, 'a', zipfile.ZIP_DEFLATED) as aggregate:
        aggregate.writestr('FONT_LIBRARY.md', archive_document)
        aggregate.write(report_file, 'qualification-reopen.json')
    (BASE / 'fonts/catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(qualified)} bundled fonts; {full_zip}')


if __name__ == '__main__': main()
