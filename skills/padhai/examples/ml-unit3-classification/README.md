# Example unit: Machine Learning, Unit III Classification (SPPU, 2019 pattern)

A complete, real Padhai unit: 15 questions (13 previous-year questions from 3 papers, deduplicated, plus 2 Expected), 14 figures, worked numericals and a revision sheet.

| File | What it is |
|---|---|
| `config.json` | Subject, unit, syllabus, header details |
| `01_partA.html` … `06_rev.html` | The answers, in Padhai markup |
| `calc.py` | Every number in the notes, computed |
| `figs/k1.py`, `figs/k2.py` | Figure scripts (write `fig/*.svg`) |

Rebuild it (from this folder):

```bash
python figs/k1.py && python figs/k2.py
python ../../scripts/check.py .
python ../../scripts/build.py .
```
