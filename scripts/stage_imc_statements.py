#!/usr/bin/env python3
"""Stage actual IMC statement HTML, never solutions, for independent PDF review."""
import argparse
import json
import pathlib
import re
from bs4 import BeautifulSoup, NavigableString, Tag

TITLE = re.compile(r"IMC\s+(\d{4})\s*[·–-]\s*Day\s+([12])\s*[·–-]\s*P(\d+)")
EXPECTED = {
    **{y: 12 for y in range(1994, 2009)},
    **{y: 10 for y in range(2009, 2020)},
    **{y: 8 for y in range(2020, 2023)},
    **{y: 10 for y in range(2023, 2027)},
}
assert sum(EXPECTED.values()) == 354

def render(node):
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag) or node.name in ('script', 'style', 'noscript'):
        return ''
    if 'katex' in node.get('class', []) or node.name == 'math':
        annotation = node.select_one('annotation[encoding="application/x-tex"]')
        return ('$' + annotation.get_text(strip=True) + '$') if annotation and annotation.get_text(strip=True) else '[MATH_REQUIRES_REVIEW]'
    if node.name == 'img':
        return '[FIGURE_REQUIRES_REVIEW]'
    if node.name == 'br':
        return '\n'
    if node.name in ('p', 'li'):
        return ''.join(map(render, node.children)).strip() + '\n\n'
    return ''.join(map(render, node.children))

def extract(html, year, day, local_number):
    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.find('h1')
    match = TITLE.search(heading.get_text(' ', strip=True)) if heading else None
    annual_number = local_number + (EXPECTED[year] // 2 if day == 2 else 0)
    if not match or tuple(map(int, match.groups())) != (year, day, annual_number):
        raise ValueError('Problem heading identity mismatch')
    statement = soup.select_one('div.card.statement')
    if not statement or statement.find('details', class_='solution'):
        raise ValueError('Missing isolated statement container')
    text = re.sub(r'[ \t]+', ' ', render(statement))
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    if len(text) < 30:
        raise ValueError('Missing or suspiciously short statement')
    latex = [a.get_text(strip=True) for a in statement.select('annotation[encoding="application/x-tex"]')]
    flags = ['requires_original_imc_pdf_fidelity_review']
    if '[MATH_REQUIRES_REVIEW]' in text: flags.append('missing_latex_annotation')
    if '[FIGURE_REQUIRES_REVIEW]' in text: flags.append('figure_requires_review')
    return {'statement_candidate': text, 'latex_annotations': latex, 'review_flags': flags}

def stage(manifest, archive):
    records, errors = [], []
    for item in manifest['sources']:
        if item.get('source') != 'studolymp_problem': continue
        year, day, local = item['year'], item['day'], item['number']
        try:
            body = extract((archive / item['path']).read_text(encoding='utf-8'), year, day, local)
        except (OSError, ValueError, UnicodeError) as exc:
            body = {'statement_candidate': '', 'latex_annotations': [], 'review_flags': ['extraction_failed']}
            errors.append({'year': year, 'day': day, 'local_number': local, 'error': str(exc)})
        records.append({'year': year, 'day': day,
                        'number': local + (EXPECTED[year] // 2 if day == 2 else 0),
                        'day_local_number': local, **body,
                        'source_url': item['resolved_url'], 'source_sha256': item['sha256'],
                        'statement_verified': False, 'publication_eligible': False})
    records.sort(key=lambda x: (x['year'], x['number']))
    years = manifest['years_requested']
    expected = sum(EXPECTED[y] for y in years)
    if len(records) != expected: errors.append({'error': 'Wrong total source problem count', 'actual': len(records), 'expected': expected})
    for year in years:
        numbers = sorted(r['number'] for r in records if r['year'] == year)
        if numbers != list(range(1, EXPECTED[year] + 1)):
            errors.append({'year': year, 'error': 'Incomplete annual numbering'})
    return {'competition': 'IMC', 'status': 'UNVERIFIED_REVIEW_ONLY',
            'expected': expected, 'extracted': len(records),
            'nonempty_candidates': sum(bool(r['statement_candidate']) for r in records),
            'candidates_with_latex': sum(bool(r['latex_annotations']) for r in records),
            'candidates': records, 'errors': errors,
            'publication_note': 'Check all mathematical statements against original IMC PDFs before public release.'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--archive', required=True, type=pathlib.Path)
    p.add_argument('--output', required=True, type=pathlib.Path)
    a = p.parse_args()
    manifest = json.loads((a.archive / 'manifest.json').read_text(encoding='utf-8'))
    out = stage(manifest, a.archive)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"IMC {out['extracted']}/{out['expected']}; nonempty={out['nonempty_candidates']}; latex={out['candidates_with_latex']}; errors={len(out['errors'])}")
    if out['errors']:
        for err in out['errors'][:15]: print('ERROR', err)
        raise SystemExit('Incomplete IMC extraction')

if __name__ == '__main__':
    main()
