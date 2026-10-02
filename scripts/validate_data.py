"""Validate every collection; explicitly quarantine the known damaged archive."""
import json
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


def main():
    failures = 0
    html = (ROOT / 'index.html').read_text()
    registered = set(re.findall(r"file: '([^']+\.json)'", html))
    files = {p.name for p in ROOT.glob('*.json')}
    for missing in sorted(registered ^ files):
        print('ERROR: collection registration mismatch:', missing); failures += 1
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
