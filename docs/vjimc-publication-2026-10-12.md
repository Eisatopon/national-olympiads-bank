# VJIMC publication: 1991–2026

33 held editions, 65 category papers, **261 original statements**, without solutions.

The original-papers collection succeeded in GitHub Actions run 38274003460.
Source PDF bytes were preserved in artifact 11758317060, along with their SHA-256
hashes. The organizer's HTTPS chain was not accepted by the runner; this transport
exception remains explicitly recorded in each publication record. Statement
images were rendered from the returned organizer PDF bytes, never generated or
reconstructed from OCR.

Each published statement has a lossless 3x PNG crop, an exact source URL, PDF page,
PDF hash, crop coordinates, image dimensions and image hash. All 261 saved crop
bodies were compared pixel-for-pixel to their original PDF render. The full crop
set was visually inspected for content and clipping. The two 2026 geometry
illustrations are contained in their original statement images.

`statement_verified` applies to the **original statement image**. The extracted
PDF text provides keyword search and preliminary automatic topic classification;
it is explicitly not a certified mathematical or LaTeX transcription. The UI,
print sheets and related-problem cards show the original image, and the AI prompt
uses the image URL instead of the potentially damaged extraction. If ChatGPT
cannot load that image, its prompt asks the user to upload it before solving.

Category I/II remain distinct in IDs and in visible category filters. Paper IDs
are stored as `paper_id`, not fabricated calendar days. Problem 4-M and 4-I are
separate alternatives in each category in 1997 and 1998; treating them as a single
problem number gave the earlier count of 257. The actual published total is 261.
The official 1991 archive contains Category I only. Category I in 1995 has three
problems, and both categories in 1996 have three. No placeholder editions are
created for 2020, 2021 or 2023.

Publication was explicitly authorized by the project owner on 12 October 2026;
the owner previously reported oral permission to republish the contest problems.

Rebuild from the extracted source artifact with:

```sh
python scripts/build_vjimc_publication.py --sources /path/to/extracted-artifact
node tests/test_vjimc_publication.cjs
```

Runtime tests cover completeness, variant identity, image integrity, loader IDs,
category labels, category-safe AI handoff and image renderer path validation.
