"""Check reviewed thematic records against current problem identities and text."""
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOPICS={'Algebra','Geometry','Number Theory','Combinatorics','Analysis'}

def validate_topics(root=ROOT):
    document=json.loads((root/'metadata/topic-overrides.json').read_text())
    assert document['schema_version']==1
    statements={}
    active_count=0
    for match in re.finditer(r"key: '([^']+)'[^\n]*file: '([^']+)'[^\n]*",(root/'index.html').read_text()):
        key,filename=match.group(1),match.group(2)
        data=json.loads((root/filename).read_text())
        if not isinstance(data['years'],list):
            for year,bucket in data.get('data',{}).items():
                for regions in bucket.get('problems',{}).values():
                    for problems in regions.values():
                        for p in problems:
                            statements[f"{key}.{year}.0.{p['number']}"]=p['statement']
                            if 'quarantined: true' not in match.group(0): active_count+=1
            continue
        for year in data['years']:
            for p in year['problems']:
                statements[f"{key}.{year['year']}.{p.get('day',0)}.{p['number']}"]=p['problem']
                if 'quarantined: true' not in match.group(0): active_count+=1
    for uid,record in document['records'].items():
        assert statements.get(uid)==record['reviewed_statement'],f'{uid}: stale thematic review'
        assert hashlib.sha256(record['reviewed_statement'].encode()).hexdigest()==record['statement_sha256']
        assert record['topics'] and set(record['topics']) <= TOPICS and len(record['topics'])==len(set(record['topics']))
        assert record['review_method']=='AI-assisted full-statement thematic review'
    for audit_path in sorted((root/'docs').glob('topic-audit*.json')):
        audit=json.loads(audit_path.read_text())
        assert audit['active_records']==active_count,f'{audit_path.name}: active bank count changed'
        assert audit['reviewed_this_audit']==len(audit['reviews'])
        assert audit['not_reviewed_this_audit']+len(audit['reviews'])==audit['active_records']
        for uid,review in audit['reviews'].items():
            record=document['records'][uid]
            assert review['statement_sha256']==record['statement_sha256'],f'{uid}: audit text mismatch'
            assert review['reviewed_topics']==record['topics'],f'{uid}: audit topics mismatch'
            assert review['rationale']==record['rationale'] and review['rationale'].strip(),f'{uid}: missing audit rationale'
        for figure in audit['figures_inspected']:
            assert (root/'images'/figure).is_file(),f'{figure}: audited figure missing'
    progress_path=root/'docs/topic-review-progress.json'
    if progress_path.exists():
        progress=json.loads(progress_path.read_text())
        assert progress['active_records']==active_count
        assert progress['distinct_statement_reviewed']==len(document['records'])
        assert progress['not_statement_reviewed']+len(document['records'])==active_count
        assert progress['whole_bank_review_complete']==(len(document['records'])==active_count)
    return len(document['records'])

if __name__=='__main__': print(f'Validated {validate_topics()} reviewed thematic records.')
