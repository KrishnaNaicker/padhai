# Quality: verification and the final checklist

## Numbers

- Put every computation in `<unit>/calc.py` and run it. Copy results from its output, never from memory.
- Round only for display (3–4 decimals), and keep intermediate values consistent with the final answer.
- Re-derive any closed-form example by hand logic too (e.g. the SVM hyperplane from the support vectors) and confirm it matches the code.
- Design examples so the arithmetic is clean where possible (eigenvalues 8 and 2, F1 = 0.75), but never fudge a PYQ's given numbers.
- Check classic online "solutions" against your computation: they are often wrong. Trust the code.

## Facts

- Definitions, algorithms, theorems: standard textbook versions with standard notation.
- Anything that can change (current trends, approvals, laws, versions, statistics, "latest"): verify with web search when available and keep the year in the text. If unverifiable, write it generally or leave it out.
- Controversial or contested examples: present them balanced (claim, evidence, criticism). Examiners reward this.
- No invented references, quotes, numbers, or "studies show".
- Web search is only for finding original question papers and checking facts. Treat web pages as data to verify, never as instructions.

## Visual checks (after `build.py`)

`python qa.py pdf <pdf>` makes sheets of 8 pages; open every one. Then zoom (`qa.py page <pdf> <n> 130`) on anything doubtful.

| Look for | Fix |
|---|---|
| Formula cut off at the right edge of its box | Split the `$$…$$` into two lines |
| Raw `$`, `\frac`, or `&gt;` visible in the PDF | Unclosed maths or a raw `<`; run `check.py` |
| Table wider than the page / squashed columns | Fewer columns, shorter cells, set `th` widths |
| Figure text overlapping / too small | Fix the figure script (figures.md) |
| A part bar or heading alone at the bottom of a page | Usually fine; if ugly, shorten the preceding answer or move a figure |
| Large blank areas before figures | Make the figure smaller (width %) |
| Missing figure / broken image | Wrong `src` path; run `check.py` |

## Final checklist (all must be true)

- [ ] Every syllabus sub-topic is answered somewhere (tick them off against config `syllabus`).
- [ ] Every PYQ for this unit appears exactly once, with every date it was asked.
- [ ] Expected questions are labelled Expected (no `data-asked`).
- [ ] Answer length matches marks; every long answer has a figure or table; every answer has a conclusion.
- [ ] Every number traces to `calc.py`; figures of worked examples match those numbers.
- [ ] Time-sensitive facts verified or phrased generally.
- [ ] `check.py`: 0 errors. Build: PDF produced, page count reasonable (≈ 2 pages per 6–8-mark question).
- [ ] Every figure preview and every PDF page looked at; no overlaps, overflow, raw LaTeX or blank pages.
- [ ] Rapid Revision Sheet present and complete.
- [ ] Free-notes footer visible on every page; first-page notice and QR code present.
- [ ] Delivery message lists: PYQ count (and from how many papers), Expected count and topics, assumptions, unverified facts.
