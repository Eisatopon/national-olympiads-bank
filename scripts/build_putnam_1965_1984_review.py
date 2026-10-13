"""Reproduce the manually reviewed historical statements from pinned input files."""
import hashlib
import json
from pathlib import Path
from putnam_historical_corrections import prepare, native, NOTES

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    'research/putnam/Putnam-1950-1974-raw-review.json': '4077713018839eb4cf1bb489ff8abac08ff684239246a36fa646e83d9bf198e7',
    'undergraduate/Putnam-1975-1979-raw-review.json': 'b82b7149e3ae8141d80ca7db16b6579383119050a705f0d3e88141d64a8763a0',
    'undergraduate/Putnam-1980-1984-raw-review.json': 'e45813fc03e79c94eb7ecea871faa1da74ce11d6d495353cc99f19cd9abfc48a',
}
BOOK = "https://www.scribd.com/document/629286756/Putnam-1965-1984"
START_PAGES = dict(zip(range(1965, 1985), [15,17,19,21,23,25,27,29,31,34,37,39,41,43,45,47,49,51,53,55]))
FIGURES = {
    (1973, 'A1'): ('1973-A1', 'Two configurations of triangle ABC with points X, Y and Z on its sides.', 31, [75,365,850,610], 2),
    (1974, 'A2'): ('1974-A2', 'A vertical circle, starting point A, stopping point B and path of descent.', 34, [190,380,465,585], 1),
    (1974, 'A5'): ('1974-A5', 'A parabola rolling around a fixed parabola, with its moving focus indicated.', 35, [235,105,705,283], 1),
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def build():
    years = []
    for filename, expected in INPUTS.items():
        raw = (ROOT / filename).read_bytes()
        if digest(raw) != expected:
            raise ValueError(f'{filename}: input changed; fresh source review required')
        data = json.loads(raw)
        for year in data['years']:
            y = year['year']
            if not 1965 <= y <= 1984:
                continue
            result = {'year': y, 'problems': []}
            for original in year['problems']:
                label = original['number']
                key = (y, label)
                text = prepare(y, label, original['problem'])
                p = {
                    'number': label,
                    'problem': text,
                    'statement_format': 'english_text_latex',
                    'statement_verified': True,
                    'text_transcription_verified': True,
                    'statement_sha256': digest(text.encode()),
                    'transcription_input': filename,
                    'transcription_input_problem_sha256': digest(original['problem'].encode()),
                    'transcription_corrected': text != native(original['problem']),
                    'review_flags': [],
                    'topics': original.get('topics', []),
                    'problem_dna': original.get('problem_dna', []),
                }
                if y < 1980 or key == (1982, 'B5'):
                    page = START_PAGES[y]
                    pages = [page, page + 1]
                    if y in (1973, 1974):
                        pages.append(page + 2)
                    if key == (1982, 'B5'):
                        pages = [52]
                    p.update({
                        'verification_source': BOOK,
                        'source_url': BOOK,
                        'verification_source_viewer_pages': pages,
                        'verification_source_printed_pages': [n - 12 for n in pages],
                        'source_reference': 'G. L. Alexanderson, L. F. Klosinski and L. C. Larson, The William Lowell Putnam Mathematical Competition: Problems and Solutions, 1965–1984, MAA (1985).',
                        'verification_method': 'AI-assisted visual comparison with printed MAA compilation pages in the public image viewer; native English prose and LaTeX; only statements and diagrams imported.',
                        'verified_on': '2026-10-13',
                        'source_contains_solutions': True,
                    })
                else:
                    if not original.get('statement_verified'):
                        raise ValueError(f'{y}/{label}: no existing source verification')
                    source = original['verification_source']
                    p.update({
                        'verification_source': source,
                        'source_url': source,
                        'verification_page': 1 if label.startswith('A') else 2,
                        'verification_method': original['verification_method'] + '; existing source review retained; math delimiters normalized to dollar syntax.',
                        'verified_on': '2026-10-12',
                        'source_contains_solutions': False,
                    })
                if key == (1965, 'A3'):
                    p['additional_verification_source'] = 'https://assets.cambridge.org/97808838/54631/excerpt/9780883854631_excerpt.pdf'
                    p['additional_verification_page'] = 2
                if key in NOTES:
                    p['source_issue_note'] = NOTES[key]
                if key in FIGURES:
                    name, alt, page, box, count = FIGURES[key]
                    filename = f'research/putnam/figures/{name}.png'
                    p['figures'] = [{'src': filename, 'alt': alt, 'sha256': digest((ROOT / filename).read_bytes()), 'source_url': BOOK, 'source_viewer_page': page, 'source_printed_page': page - 12, 'source_crop_pixels': box, 'diagram_count': count, 'content': 'diagram_only'}]
                result['problems'].append(p)
            assert [p['number'] for p in result['problems']] == [f'{s}{n}' for s in 'AB' for n in range(1,7)]
            years.append(result)
    assert [y['year'] for y in years] == list(range(1965,1985))
    output = {
        'competition': 'William Lowell Putnam Mathematical Competition',
        'first_year': 1965, 'last_year': 1984, 'problem_count': 240,
        'status': 'SOURCE_REVIEWED_RESEARCH_CHECKPOINT',
        'publication_eligible': False,
        'publication_note': 'Held outside the public bank until the full historical 1938–1984 series is source-verified. This checkpoint does not certify 1938–1964 or 1985–2025.',
        'solutions_imported': False,
        'classification_status': 'pending',
        'source_input_sha256': INPUTS,
        'statement_format': 'english_text_latex',
        'native_text_count': 240, 'figure_asset_count': 3, 'diagram_count': 4,
        'source_issue_count': len(NOTES), 'years': years,
    }
    path = ROOT / 'research/putnam/Putnam-1965-1984-verified-review.json'
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(f'Wrote {path.relative_to(ROOT)}: 240 source-reviewed statements, 4 diagrams in 3 assets.')

if __name__ == '__main__':
    build()
