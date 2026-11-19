# Writing answers that score full marks

The reader is a student revising the night before. The marker is a university examiner skimming 60 scripts. Both reward the same thing: **clear structure, correct keywords, a diagram, an example, and nothing vague.**

## 1. Choosing and phrasing questions

- PYQs keep their original wording (fix obvious typos only).
- Expected questions use the examiner's verbs: *Explain … with a neat diagram*, *Differentiate between … and …*, *Write a short note on …*, *What is …? Explain its types*, *Solve / Apply … for the given data*, *Explain the working of …*, *List and explain the applications of …*.
- Marks for Expected questions follow the paper's pattern (if the paper has 6- and 8-mark sub-questions, use 6 or 8).
- One question per concept cluster. Do not create five tiny questions where the exam would ask one big one; do not cram two unrelated topics into one.
- Numerical-heavy subjects: at least one Expected numerical per numerical-capable topic, with clean numbers.

## 2. Length follows marks

| Marks | Target (in the PDF) | Typical structure |
|---|---|---|
| 1–2 | 3–6 lines | definition + one example or formula |
| 3–4 | ½–¾ page | definition, 4–6 points, small table or diagram |
| 5–6 | 1–1½ pages | full anatomy below, one figure or table |
| 8–9 | ≈ 2 pages | full anatomy, figure **and** table, worked example |
| 10–12+ | 2–3 pages | numericals: every step shown; theory: two figures, two tables |

## 3. Answer anatomy (long answers)

1. **Definition / Introduction**: 2–3 crisp sentences with the bolded keywords. Use `<div class="def">`.
2. **Explanation in points**: numbered "Step N:" lists for processes/algorithms (`ol.steps`), bullets for properties/features.
3. **Formula** (if any) in a formula box with a "where" line explaining every symbol.
4. **Diagram** with a numbered caption ("Fig. 3.4 · …").
5. **Example**: small, concrete, worked.
6. **Table**: types, comparison, or summary.
7. **Advantages / limitations**, or **applications**, as the question demands.
8. **Conclusion**: one or two sentences that restate the core idea. Every answer has one.

Not every answer needs all eight. Match the question: "List the applications" is mostly item 7; "Explain with a diagram" must have item 4.

## 4. Patterns by question type

**Differentiate / Compare** — two one-line definitions, then a table whose first column header is **"Basis"** (the build adds the Sr. No. column), 7–10 rows: definition, purpose, working, structure, complexity, advantages, disadvantages, example, applications, … Add a diagram if one makes the difference visible. End with a conclusion.

**Numerical** — 
1. *Given* (restate data as a table).
2. *Formula* (formula box).
3. *Step-by-step* computation, one step per line, substitution visible, intermediate values to 3–4 decimals.
4. *Result* table.
5. *Interpretation* (what the number means).
6. Optional "check" (alternative method, or sensitivity: other K, other threshold).
Ambiguous data → solve the likely reading, give the other in an Exam Tip.

**Algorithm / Working** — idea → Step N list → diagram or flow → worked trace on a small example → complexity → pros/cons.

**Short note** — definition, 5–8 key points, one small figure or table, applications, conclusion.

**Types / Classification** — definition, a tree or table of types, each type with definition + example.

**Case study / "give an example of …"** — pick a real, verifiable example, structured as: problem → approach → how it works → outcome → limitations/controversy. Prefer balanced facts over hype.

**Ethics / trends / essay-type** — structure them anyway: numbered points each with a bold title and one explanatory sentence, plus a table.

## 5. Style

- Simple, exam-register English. Short sentences. No filler ("In today's world…", "plays a vital role").
- **Bold** the keywords a marker scans for (2–5 per paragraph, not whole sentences).
- Use the real technical terms and standard notation of the subject.
- Do not refer to "the notes", "this PDF" or "as an AI".
- Exam Tip: a specific, actionable scoring tip (what examiners look for, a common mistake, how to handle a variant). Memory Hook: a mnemonic or one-line contrast. Use each at most once per question, only when it adds value.
- Cross-references are fine ("see Q7", "Fig. 3.5").

## 6. Rapid Revision Sheet (last part)

Mark the part with `<div class="part rev" ...>` and wrap the content in `<div class="rev">`:
1. **Core formulas**: every formula in the unit, one line each.
2. **One-liners examiners love**: 10–14 crisp facts/contrasts.
3. **If they ask X → make sure you write Y**: a table mapping each question type in this unit to the must-include elements.
4. **Numerical answers to re-check**: every final number in the notes (for numerical subjects); otherwise **Key terms** with one-line definitions.
