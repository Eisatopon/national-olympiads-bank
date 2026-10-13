"""Check retained official PDF hashes and the two diagram crops.

Usage: python scripts/verify_vjimc_sources.py --pdf-dir /path/to/vjimc-pdfs
The source archive is read-only. This never regenerates statements from PDF text.
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf-dir', required=True, type=Path)
    args = parser.parse_args()
    # Rendering dependencies are needed only for this offline source-byte audit.
    import fitz
    from PIL import Image
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / 'undergraduate/Vojtech-Jarnik-problems.json').read_text())
    docs, crop_count = {}, 0
    for year in data['years']:
        for p in year['problems']:
            filename = p['source_url'].rsplit('/', 1)[1]
            if filename not in docs:
                path = args.pdf_dir / filename
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != p['source_document_sha256']:
                    raise ValueError(f'Changed official PDF: {filename}')
                docs[filename] = (fitz.open(path), actual)
            doc, actual = docs[filename]
            if actual != p['source_document_sha256']:
                raise ValueError(f'Conflicting PDF hash: {filename}')
            page = doc[p['verification_page'] - 1]
            if p.get('figure_asset'):
                rect = fitz.Rect(p['figure_crop_points'])
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect)
                original = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
                saved = Image.open(root / p['figure_asset']).convert('RGB')
                if saved.size != original.size or saved.tobytes() != original.tobytes():
                    raise ValueError(f'Changed diagram: {p["figure_asset"]}')
                crop_count += 1
    print(f'Official PDF bytes verified: {len(docs)}; diagram crops matched pixel-for-pixel: {crop_count}.')


if __name__ == '__main__':
    main()
