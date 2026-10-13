"""Build the slim metadata files that index.html downloads.

The audit files in metadata/ keep a full copy of every reviewed statement
(reviewed_statement + statement_sha256) so that validators can prove that a
review still matches the published text.  The browser does not need those
copies: it only needs to know whether the statement it is showing is the one
that was reviewed.  For that a short fingerprint is enough.

Fingerprint: 32-bit FNV-1a over the UTF-16 code units of the statement,
written as 8 lowercase hex digits.  index.html computes the same value with
textHash().  A changed statement therefore loses its reviewed topics / checked
badge immediately, exactly as before.

Usage:
    python scripts/build_runtime_metadata.py          # (re)write metadata/runtime/*
    python scripts/build_runtime_metadata.py --check  # fail if they are stale (CI)

metadata/runtime/manifest.json holds the problem count per year of every
collection file; index.html draws the grid and the totals from it and
downloads a collection only when its problems are needed.

The statement checks (most of the data) are written per collection to
metadata/runtime/checks/<collection file>, and index.html downloads them
together with the collection, so the first page load stays small.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'metadata' / 'runtime'

# Fields of a statement check that index.html actually reads.
CHECK_FIELDS = ('status', 'checked_at', 'source_url', 'source_page', 'source_problem_number',
                'source_pages', 'printed_source_pages', 'source_download_url', 'source_download_kind', 'source_format',
                'source_contains_solutions', 'transcription_source_url', 'source_variant_note', 'original_wording_verified', 'verification_basis', 'verification_tex_mirror', 'verification_pdf_source')


def text_hash(text: str) -> str:
    h = 0x811C9DC5
    data = text.encode('utf-16-le')
    for i in range(0, len(data), 2):
        h ^= data[i] | (data[i + 1] << 8)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f'{h:08x}'


def load(name):
    path = ROOT / 'metadata' / name
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else None


def build_topics():
    records = dict((load('topic-overrides.json') or {}).get('records', {}))
    records.update((load('topic-overrides-final575.json') or {}).get('records', {}))
    out = {}
    for uid in sorted(records):
        rec = records[uid]
        if 'reviewed_statement' not in rec or not rec.get('topics'):
            continue
        out[uid] = [rec['topics'], text_hash(rec['reviewed_statement'])]
    return {'schema_version': 1, 'hash': 'fnv1a32-utf16', 'records': out}


def checks_path(file):
    return f'checks/{file}'


def build_collections():
    src = dict(load('collections.json')['collections'])
    src.update((load('smmc-statement-checks.json') or {}).get('collections', {}))
    src.update((load('vjimc-statement-checks.json') or {}).get('collections', {}))
    src.update((load('putnam-statement-checks.json') or {}).get('collections', {}))
    out, check_files = {}, {}
    for file in sorted(src):
        meta = src[file]
        slim = {}
        if meta.get('verification_notes'):
            slim['verification_notes'] = meta['verification_notes']
        if meta.get('missing_problem_numbers'):
            slim['missing_problem_numbers'] = meta['missing_problem_numbers']
        links = [{'url': l['url']} for l in meta.get('source_links') or [] if l.get('url')]
        if links:
            slim['source_links'] = links
        checks = {}
        for uid, c in (meta.get('statement_checks') or {}).items():
            if 'reviewed_statement' not in c:
                continue
            item = {k: c[k] for k in CHECK_FIELDS if k in c}
            item['h'] = text_hash(c['reviewed_statement'])
            checks[uid] = item
        if checks:
            slim['statement_checks_file'] = checks_path(file)
            check_files[checks_path(file)] = {'schema_version': 1, 'hash': 'fnv1a32-utf16', 'statement_checks': checks}
        notes = {}
        for uid, n in (meta.get('statement_notes') or {}).items():
            if 'reviewed_statement' not in n or not n.get('text'):
                continue
            notes[uid] = {'text': n['text'], 'h': text_hash(n['reviewed_statement'])}
        if notes:
            slim['statement_notes'] = notes
        out[file] = slim
    return {'schema_version': 1, 'hash': 'fnv1a32-utf16', 'collections': out}, check_files


def build_manifest():
    """Problem counts per year for every collection file.

    The grid and the totals are drawn from this small file, so the browser
    only downloads a collection when its problems are actually shown.
    The counts must equal what index.html derives from the full file
    (normalizeYears / normalizeUsa)."""
    out = {}
    for path in sorted([*ROOT.glob('*-problems.json'), ROOT / 'undergraduate/Vojtech-Jarnik-problems.json', ROOT / 'undergraduate/Simon-Marais-problems.json', ROOT / 'undergraduate/Putnam-problems.json', ROOT / 'undergraduate/IMC-1994-2026-review.json', ROOT / 'undergraduate/SEEMOUS-2007-2010-problems.json']):
        raw = json.loads(path.read_text(encoding='utf-8'))
        years = {}
        if isinstance(raw.get('data'), dict):  # older USA TSTST schema
            for yr, v in raw['data'].items():
                n = sum(len(lst or []) for by_region in (v.get('problems') or {}).values()
                        for lst in by_region.values())
                if n:
                    years[str(int(yr))] = years.get(str(int(yr)), 0) + n
        else:
            for y in raw.get('years') or []:
                n = len(y.get('problems') or [])
                if n:
                    years[str(y['year'])] = years.get(str(y['year']), 0) + n
        out[str(path.relative_to(ROOT))] = {'total': sum(years.values()), 'years': years}
    return {'schema_version': 1, 'files': out}


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'), sort_keys=False) + '\n'


def main():
    collections, check_files = build_collections()
    files = {'topics.json': dump(build_topics()), 'collections.json': dump(collections),
             'manifest.json': dump(build_manifest())}
    files.update({name: dump(body) for name, body in check_files.items()})
    # Check files of collections that no longer have checks must not linger.
    orphans = [str(p.relative_to(OUT)) for p in (OUT / 'checks').rglob('*.json')
               if str(p.relative_to(OUT)) not in files] if (OUT / 'checks').exists() else []
    if '--check' in sys.argv:
        stale = [n for n, body in files.items()
                 if not (OUT / n).exists() or (OUT / n).read_text(encoding='utf-8') != body] + orphans
        if stale:
            print('Stale runtime metadata: ' + ', '.join(stale) +
                  '. Run: python scripts/build_runtime_metadata.py')
            sys.exit(1)
        print('Runtime metadata is up to date.')
        return
    OUT.mkdir(parents=True, exist_ok=True)
    for name in orphans:
        (OUT / name).unlink()
        print(f'Removed metadata/runtime/{name}')
    for name, body in files.items():
        (OUT / name).parent.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text(body, encoding='utf-8')
    print(f'Wrote {len(files)} files in metadata/runtime/ (collections.json: {len(files["collections.json"].encode()):,} bytes, '
          f'{len(check_files)} statement-check files: {sum(len(files[n].encode()) for n in check_files):,} bytes)')


if __name__ == '__main__':
    main()
