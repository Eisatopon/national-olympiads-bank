"""Generate an auditable progress inventory; checks must match current statements."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def inventory(root=ROOT):
    metadata = json.loads((root / 'metadata/collections.json').read_text())['collections']
    rows = []
    for filename, entry in sorted(metadata.items()):
        data = json.loads((root / filename).read_text())
        if isinstance(data['years'], list):
            statements = [p['problem'] for b in data['years'] for p in b['problems']]
            years = sorted({b['year'] for b in data['years']})
        else:
            statements = [p['statement'] for b in data['data'].values() for cs in b['problems'].values() for ps in cs.values() for p in ps]
            years = sorted(int(y) for y in data['data'])
        checked = len(entry.get('statement_checks', {}))
        state = 'quarantined' if entry['verification_status'] == 'quarantined' else ('stored_statements_checked' if checked == len(statements) else 'pending')
        rows.append({'file':filename,'total_records':len(statements),'source_checked_records':checked,'remaining_records':len(statements)-checked,'status':state,'years':years,'research_links_recorded':bool(entry['source_links'])})
    return rows

def render(rows):
    total = sum(r['total_records'] for r in rows); checked = sum(r['source_checked_records'] for r in rows)
    out = ['# Source verification progress', '', f'Inventory: {total} records; {checked} source-checked; {total-checked} remaining.', '',
           'Counts describe stored records, not certified unique mathematical problems. China includes damaged records and remains quarantined. Complete stored-statement checks do not certify historical archive coverage. Review method is AI-assisted visual and textual source comparison, not independent solution verification.', '',
           '| Collection | Stored records | Source checked | Remaining | State |', '|---|---:|---:|---:|---|']
    out += [f"| {r['file']} | {r['total_records']} | {r['source_checked_records']} | {r['remaining_records']} | {r['status']} |" for r in rows]
    out += ['', '## Review order', '', '1. Complete USA TST: done for all 85 stored statements.', '2. Australia AMO: done for all 40 stored statements, including the 2020 problem 7 figure.', '3. New Zealand NZMO Round Two: done for all 40 stored statements. Canada CMO remains pending.', '4. European finals and TSTs, then remaining Asian and American collections.', '5. Repair the quarantined China archive only from reliable original papers; missing papers remain explicitly pending.', '', 'Research links are leads, not evidence that the corresponding statements have already been checked. For every review, retain source URL, page, original problem number, PDF checksum, exact reviewed text, statement checksum and review date. Do not add checks from automated extraction alone.', '']
    return '\n'.join(out)

if __name__ == '__main__':
    destination = ROOT / 'docs/verification-progress.md'
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(render(inventory()))
    print(destination)
