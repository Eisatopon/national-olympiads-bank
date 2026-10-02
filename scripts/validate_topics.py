"""Check reviewed thematic records against current problem identities and text."""
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOPICS={'Algebra','Geometry','Number Theory','Combinatorics'}

def validate_topics(root=ROOT):
    document=json.loads((root/'metadata/topic-overrides.json').read_text())
    assert document['schema_version']==1
    statements={}
    for key,filename in re.findall(r"key: '([^']+)'[^\n]*file: '([^']+)'",(root/'index.html').read_text()):
        data=json.loads((root/filename).read_text())
        if not isinstance(data['years'],list): continue
        for year in data['years']:
            for p in year['problems']:
                statements[f"{key}.{year['year']}.{p.get('day',0)}.{p['number']}"]=p['problem']
    for uid,record in document['records'].items():
        assert statements.get(uid)==record['reviewed_statement'],f'{uid}: stale thematic review'
        assert hashlib.sha256(record['reviewed_statement'].encode()).hexdigest()==record['statement_sha256']
        assert record['topics'] and set(record['topics']) <= TOPICS and len(record['topics'])==len(set(record['topics']))
        assert record['review_method']=='AI-assisted full-statement thematic review'
    return len(document['records'])

if __name__=='__main__': print(f'Validated {validate_topics()} reviewed thematic records.')
