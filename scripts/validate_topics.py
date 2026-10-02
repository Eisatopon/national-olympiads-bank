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
    audit_path=root/'docs/topic-audit-2026-10-02.json'
    if audit_path.exists():
        audit=json.loads(audit_path.read_text())
        assert audit['reviewed_this_audit']==len(audit['reviews'])
        assert audit['not_reviewed_this_audit']+len(audit['reviews'])==audit['active_records']
        for uid,review in audit['reviews'].items():
            record=document['records'][uid]
            assert review['statement_sha256']==record['statement_sha256'],f'{uid}: audit text mismatch'
            assert review['reviewed_topics']==record['topics'],f'{uid}: audit topics mismatch'
            assert review['rationale']==record['rationale'] and review['rationale'].strip(),f'{uid}: missing audit rationale'
        for figure in audit['figures_inspected']:
            assert (root/'images'/figure).is_file(),f'{figure}: audited figure missing'
    return len(document['records'])

if __name__=='__main__': print(f'Validated {validate_topics()} reviewed thematic records.')
