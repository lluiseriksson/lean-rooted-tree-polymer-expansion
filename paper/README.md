# Manuscript package

- `main.tex` / `main.pdf`: submission manuscript.
- `references.bib`: machine-readable bibliography retained for venue conversion; the PDF uses an embedded bibliography so it builds without BibTeX.
- `graphical-abstract.tex` / `graphical-abstract-final.pdf`: optional visual abstract.
- `cover-letter.md`: venue-neutral cover letter.
- `arxiv-abstract.txt`: plain-text abstract for arXiv.
- `highlights.txt`: journal-style highlights.
- `submission-metadata.yaml`: proposed metadata and classifications.

Build with:

```bash
make -C paper clean all
```
