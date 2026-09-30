"""Check repository Markdown local links, anchors, and fenced JSON examples."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
for source in ROOT.rglob('*.md'):
    if any(part.startswith('.') for part in source.relative_to(ROOT).parts):
        continue
    content = source.read_text(encoding='utf-8')
    for block in re.findall(r'```json\s*\n(.*?)\n```', content, re.S):
        try:
            json.loads(block)
        except ValueError as error:
            errors.append(f'{source.relative_to(ROOT)}: invalid fenced JSON: {error}')
    for link in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', content):
        parsed = urlsplit(link.strip('<>'))
        if parsed.scheme or parsed.netloc:
            continue
        path = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
        if not path.exists():
            errors.append(f'{source.relative_to(ROOT)}: missing {link}')
        elif parsed.fragment and path.suffix == '.md':
            headings = re.findall(r'^#+\s+(.+)$', path.read_text(), re.M)
            anchors = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings}
            if unquote(parsed.fragment) not in anchors:
                errors.append(f'{source.relative_to(ROOT)}: missing anchor {link}')
if errors:
    raise SystemExit('\n'.join(errors))
print('Local documentation links and JSON blocks pass.')
