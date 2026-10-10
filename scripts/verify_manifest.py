#!/usr/bin/env python3
"""Check all listed package file identities. No network access or source archive."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'MANIFEST.json').read_text(encoding='utf-8'))
errors = []
for row in manifest['files']:
    path = ROOT / row['path']
    if not path.exists():
        errors.append(row['path'] + ': missing')
    elif hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
        errors.append(row['path'] + ': changed')
if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: ' + str(len(manifest['files'])) + ' listed package files match their SHA-256 hashes.')
