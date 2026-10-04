"""Generate source-review progress from current, valid evidence, never from leads."""
import hashlib
import json
import re
from pathlib import Path
if __package__:
    from .validate_data import validate_statement_checks
else:
    from validate_data import validate_statement_checks
ROOT = Path(__file__).resolve().parents[1]

def inventory(root=ROOT):
    metadata = json.loads((root / 'metadata/collections.json').read_text())['collections']
    html = (root / 'index.html').read_text()
    keys = {m.group(2): m.group(1) for m in re.finditer(r"key: '([^']+)'[^\n]*file: '([^']+)'", html)}
    rows = []
    for filename, entry in sorted(metadata.items()):
        data = json.loads((root / filename).read_text())
        if isinstance(data['years'], list):
            statements = [p for b in data['years'] for p in b['problems']]
            years = sorted({b['year'] for b in data['years']})
            errors = validate_statement_checks(entry, data, keys[filename])
            if errors:
                raise ValueError('; '.join(errors))
        else:
            statements = [p for b in data['data'].values() for cs in b['problems'].values() for ps in cs.values() for p in ps]
            years = sorted(int(y) for y in data['data'])
            if entry.get('statement_checks'):
                raise ValueError('Legacy source evidence must be supported before counting it')
        checked = len(entry.get('statement_checks', {}))
        solutions = sum(any(k in p and p[k] for k in ('solution', 'solutions', 'official_solution', 'answer')) for p in statements)
        state = 'quarantined' if entry['verification_status'] == 'quarantined' else ('stored_statements_checked' if checked == len(statements) else 'pending')
        rows.append({'file':filename,'total_records':len(statements),'source_checked_records':checked,'remaining_records':len(statements)-checked,'status':state,'years':years,'research_links_recorded':bool(entry['source_links']),'stored_solution_records':solutions})
    return rows

def render(rows):
    total = sum(r['total_records'] for r in rows); checked = sum(r['source_checked_records'] for r in rows)
    active = [r for r in rows if r['status'] != 'quarantined']
    active_total = sum(r['total_records'] for r in active); active_checked = sum(r['source_checked_records'] for r in active)
    out = ['# Source verification progress', '', f'Inventory: {total} stored records; {checked} source-checked; {total-checked} remaining (including quarantine).', '',
           f'Active bank: {active_total} records; {active_checked} source-checked; {active_total-active_checked} remaining. Whole-bank source verification is **not complete**.', '',
           f'Stored solution records: {sum(r["stored_solution_records"] for r in rows)}. No stored solution has been independently verified. Source fidelity, mathematical correctness and thematic classification are separate review stages.', '',
           'Counts describe stored records, not certified unique mathematical problems. China active data contains only reconstructed 2003–2006 papers; damaged historical data is retained outside the active collections. Complete stored-statement checks do not certify historical archive coverage. Review method is AI-assisted visual and textual source comparison, not independent solution verification.', '',
           '| Collection | Stored records | Source checked | Remaining | State |', '|---|---:|---:|---:|---|']
    out += [f"| {r['file']} | {r['total_records']} | {r['source_checked_records']} | {r['remaining_records']} | {r['status']} |" for r in rows]
    out += ['', '## Evidence and outstanding work', '',
            'USA TST (85), Australia AMO (40), and New Zealand NZMO Round Two (40) have recorded source checks for every stored statement. Canada has 100 recorded checks: 1969, 1970 and 2011–2026. Its other 223 stored statements remain pending.', '',
            'The Canadian review found a missing nonzero-denominator condition in the original CMO 1969 problem 1, recorded as a separate editorial note. The CMO 2019 problem 3 figure has been replaced with a faithful crop of the official paper, including all six original counter positions.', '',
            'Independent reasoning for CMO 1969 is recorded in mathematical-checks-2026-10-03.json: nine claims checked and one source domain gap. This is not mathematical certification of the other problems.', '',
            'Research links and retrieved PDFs are leads, not evidence that their statements or solutions have already been checked. For every source review, retain source URL, page, original problem number, PDF checksum, exact reviewed text, statement checksum and review date. Do not add checks from automated extraction alone.', '']
    return '\n'.join(out)

if __name__ == '__main__':
    destination = ROOT / 'docs/verification-progress.md'
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(render(inventory()))
    print(destination)
