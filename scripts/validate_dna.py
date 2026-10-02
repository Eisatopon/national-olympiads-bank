"""Reject stale or undocumented technique sequences before publication."""
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def validate_dna(root=ROOT):
    data = json.loads((root / 'metadata/problem-dna.json').read_text())
    assert data['schema_version'] == 1
    records = {}
    for key, filename in re.findall(r"key: '([^']+)'[^\n]*file: '([^']+)'", (root / 'index.html').read_text()):
        collection = json.loads((root / filename).read_text())
        if not isinstance(collection['years'], list):
            continue
        for year in collection['years']:
            for problem in year['problems']:
                uid = f"{key}.{year['year']}.{problem.get('day',0)}.{problem['number']}"
                records[uid] = problem['problem']
    for uid, record in data['records'].items():
        assert records.get(uid) == record['reviewed_statement'], f'{uid}: stale DNA statement'
        assert hashlib.sha256(record['reviewed_statement'].encode()).hexdigest() == record['statement_sha256'], f'{uid}: DNA checksum'
        assert record['techniques'] and len(set(record['techniques'])) == len(record['techniques'])
        assert all(t in data['techniques'] for t in record['techniques']), f'{uid}: unknown technique'
        assert type(record['practice_level']) is int and 1 <= record['practice_level'] <= 3
        assert record['review_method'] == 'AI-assisted mathematical derivation'
        assert len(record['solution_review']) >= 80
        assert record['concepts'] and all(isinstance(x,str) for x in record['concepts'])
    return len(data['records'])

if __name__ == '__main__':
    print(f'Validated {validate_dna()} reviewed Problem DNA records.')
