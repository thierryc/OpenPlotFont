"""Fetch digest-locked source fonts and notices into output/.

No upstream code is executed. Archive members are extracted by basename only
from the locked author download. Reviewed notices keep their exact text in the
lock file; their URL identifies the license/ancestor being acknowledged.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'scripts/font_library_sources.json'


def main():
    records = json.loads(LOCK.read_text())
    errors = []
    def fetch(record):
        path = ROOT / record['path']
        try:
            if path.exists():
                data = path.read_bytes()
            elif 'sourceText' in record:
                data = record['sourceText'].encode('utf-8')
            else:
                data = urllib.request.urlopen(record['url'], timeout=60).read()
            if hashlib.sha256(data).hexdigest() != record['sha256']:
                raise ValueError('SHA-256 mismatch; refusing changed source')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        except Exception as error:
            return {'path': record['path'], 'error': str(error)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        errors += [e for e in pool.map(fetch, [r for r in records if 'archiveMember' not in r]) if e]
    archive_path = ROOT / 'output/font-library/sources/cutlings/download.zip'
    if archive_path.exists():
        with zipfile.ZipFile(archive_path) as archive:
            for record in records:
                if 'archiveMember' not in record: continue
                try:
                    data = archive.read(record['archiveMember'])
                    if hashlib.sha256(data).hexdigest() != record['sha256']:
                        raise ValueError('Archive member digest mismatch')
                    path = ROOT / record['path']
                    path.write_bytes(data)
                except Exception as error:
                    errors.append({'path': record['path'], 'error': str(error)})
    destination = ROOT / 'output/font-library'
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'sources.json').write_text(json.dumps([{k:v for k,v in r.items() if k != 'sourceText'} for r in records], indent=2)+'\n')
    (destination / 'fetch-errors.json').write_text(json.dumps(errors, indent=2)+'\n')
    print(f'{len(records)} locked records; {len(errors)} errors')
    if errors: raise SystemExit(1)


if __name__ == '__main__': main()
