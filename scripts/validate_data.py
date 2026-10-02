"""Validate every collection; explicitly quarantine the known damaged archive."""
import json
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUARANTINED = {'China-olympiad-problems.json'}
KNOWN_GAPS = {('Argentina-level3-problems.json', 1994): [2, 3, 4, 5, 6],
              ('Argentina-level3-problems.json', 1996): [2, 3, 4, 5, 6],
              ('Argentina-level3-problems.json', 2007): [1, 2, 3, 5, 6],
              ('Argentina-level3-problems.json', 2008): [2, 3, 4, 5, 6],
              ('Argentina-level3-problems.json', 2010): [1, 2, 3, 4, 6]}


def validate(data, filename, root=ROOT):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    if not isinstance(data, dict):
        return ['root must be an object']
    require(isinstance(data.get('competition'), str) and bool(data.get('competition')), 'competition is required')
    years = data.get('years')
    legacy = filename == 'Usa-tstst-problems.json'
    if legacy:
        if not isinstance(data.get('data'), dict):
            return errors + ['legacy data must be an object']
        blocks = []
        for year, entry in data['data'].items():
            try:
                number = int(year)
                problems = [p for countries in entry['problems'].values() for ps in countries.values() for p in ps]
                blocks.append({'year': number, 'problems': problems})
            except (ValueError, TypeError, KeyError, AttributeError):
                return errors + ['invalid legacy year block']
    else:
        if not isinstance(years, list):
            return errors + ['years must be an array']
        blocks = years
    seen_years, seen_ids = set(), set()
    year_order = []
    for block in blocks:
        if not isinstance(block, dict) or type(block.get('year')) is not int:
            errors.append('year must be an integer'); continue
        year = block['year']; year_order.append(year)
        require(year not in seen_years, f'{year}: duplicate year'); seen_years.add(year)
        problems = block.get('problems')
        if not isinstance(problems, list) or not problems:
            errors.append(f'{year}: problems must be a nonempty array'); continue
        numbers = []
        for p in problems:
            if not isinstance(p, dict):
                errors.append(f'{year}: problem must be an object'); continue
            n = p.get('number'); day = p.get('day', 0)
            require((isinstance(n, str) and n.isdigit()) if legacy else type(n) is int and n > 0, f'{year}: invalid number')
            require(type(day) is int and day >= 0 and ('day' not in p or day > 0), f'{year}/{n}: invalid day')
            numbers.append(int(n) if legacy and isinstance(n, str) and n.isdigit() else n)
            uid = (year, str(day), str(n))
            require(uid not in seen_ids, f'{year}/{n}: duplicate identifier'); seen_ids.add(uid)
            text = p.get('statement' if legacy else 'problem')
            if not isinstance(text, str) or not text.strip():
                errors.append(f'{year}/{n}: empty statement'); continue
            require(text.count('$') % 2 == 0, f'{year}/{n}: unmatched dollar delimiter')
            require(not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', text), f'{year}/{n}: control character')
            for image in re.findall(r'https?://\S+?images/([^\s]+)', text):
                require((root / 'images' / image).is_file(), f'{year}/{n}: missing image {image}')
        expected = KNOWN_GAPS.get((filename, year), list(range(1, len(problems) + 1)))
        require(numbers == expected, f'{year}: unexpected numbering {numbers}')
    if not legacy:
        require(year_order == sorted(year_order), 'years must be ascending')
    return errors


def validate_statement_checks(entry, data, country_key):
    records = {f"{country_key}.{b['year']}.{p.get('day', 0)}.{p['number']}": p['problem']
               for b in data['years'] for p in b['problems']}
    errors = []
    for uid, check in entry.get('statement_checks', {}).items():
        text = records.get(uid)
        if text is None or text != check.get('reviewed_statement'):
            errors.append(f'{uid}: checked statement changed or missing'); continue
        if hashlib.sha256(text.encode()).hexdigest() != check.get('statement_sha256'):
            errors.append(f'{uid}: statement checksum mismatch')
        image_paths = set(re.findall(r'images/[A-Za-z0-9_.-]+', text))
        figure_checks = check.get('figure_checks', [])
        if image_paths != {f.get('path') for f in figure_checks}:
            errors.append(f'{uid}: missing or unexpected reviewed figure')
        for figure in figure_checks:
            path = figure.get('path', '')
            if not re.fullmatch(r'images/[A-Za-z0-9_.-]+', path):
                errors.append(f'{uid}: invalid reviewed figure path'); continue
            image = ROOT / path
            if not image.is_file() or hashlib.sha256(image.read_bytes()).hexdigest() != figure.get('sha256'):
                errors.append(f'{uid}: reviewed figure changed or missing')
        if (check.get('status') != 'statement_checked_against_source'
                or not re.fullmatch(r'https?://[^\s{}<>]+', check.get('source_url', ''))
                or type(check.get('source_page')) is not int or check['source_page'] < 1
                or type(check.get('source_problem_number')) is not int or check['source_problem_number'] < 1
                or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', check.get('checked_at', ''))
                or not re.fullmatch(r'[0-9a-f]{64}', check.get('source_document_sha256', ''))
                or check.get('review_method') != 'AI-assisted visual and textual comparison'
                or not check.get('scope')):
            errors.append(f'{uid}: incomplete source-check evidence')
    return errors


def main():
    failures = 0
    html = (ROOT / 'index.html').read_text()
    registered = set(re.findall(r"file: '([^']+\.json)'", html))
    files = {p.name for p in ROOT.glob('*.json')}
    for missing in sorted(registered ^ files):
        print('ERROR: collection registration mismatch:', missing); failures += 1
    try:
        metadata = json.loads((ROOT / 'metadata/collections.json').read_text())
        collections = metadata['collections']
        assert metadata['schema_version'] == 1 and set(collections) == files
        for name, entry in collections.items():
            assert entry['verification_status'] == ('quarantined' if name in QUARANTINED else 'not_verified_against_source')
            if entry.get('statement_checks'):
                country_key = next(re.search(r"key: '([^']+)'", line).group(1)
                                   for line in html.splitlines() if "file: '" + name + "'" in line)
                data = json.loads((ROOT / name).read_text())
                for error in validate_statement_checks(entry, data, country_key):
                    print('ERROR:', error); failures += 1
            for link in entry['source_links']:
                assert re.fullmatch(r'https?://[^\s{}<>]+', link['url'])
                assert link['verification'] == 'unverified'
            if name == 'Argentina-level3-problems.json':
                data = json.loads((ROOT / name).read_text())
                for year, missing in entry['missing_problem_numbers'].items():
                    nums = {p['number'] for b in data['years'] if b['year'] == int(year) for p in b['problems']}
                    assert not nums.intersection(missing)
    except (ValueError, OSError, KeyError, TypeError, AssertionError):
        print('ERROR: missing or invalid collection provenance metadata'); failures += 1
    for path in sorted(ROOT.glob('*.json')):
        try:
            data = json.loads(path.read_text())
        except (ValueError, OSError) as exc:
            print('ERROR:', path.name, exc); failures += 1; continue
        errors = validate(data, path.name)
        if path.name in QUARANTINED:
            entry = next((line for line in html.splitlines() if "file: '" + path.name + "'" in line), '')
            if 'quarantined: true' not in entry:
                print('ERROR: damaged archive must remain quarantined'); failures += 1
            print(f'QUARANTINED: {path.name}: {len(errors)} validation findings')
        elif errors:
            failures += len(errors)
            for error in errors:
                print('ERROR:', path.name, error)
    print(f'Checked {len(files)} collections; {failures} blocking errors; known Argentina gaps preserved.')
    return int(bool(failures))

if __name__ == '__main__':
    raise SystemExit(main())
