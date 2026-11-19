# Inputs: what to collect and how to handle each case

## The one message to send when inputs are incomplete

Ask everything missing in **one** message. Example:

> To make the notes I need the **syllabus for this unit** (the topics listed under it). Optional, but they make the notes much better:
> 1. Previous-year questions for this unit (typed, screenshots, or full papers). If you send full papers, tell me which question numbers belong to this unit (e.g. Q3/Q4 = Unit IV).
> 2. University, course, semester and the marks per question (e.g. "6 or 8 marks each").

Never ask about format, length, colours or style: those are fixed by this skill.

## Cases

| Student gives | What you do |
|---|---|
| Syllabus + PYQs | Full method. |
| Syllabus only | Every question is "Expected". Cover each sub-topic with the kind of question that university asks (mix of definitions, explain-with-diagram, differentiate, numericals if the subject has them). |
| Unit name only | Ask for the syllabus. If they can't get it: draft a topic list, show it, wait for confirmation. If unattended: draft it, state clearly at the top that the topic list is your draft, and proceed. |
| Whole-subject syllabus, asks for "notes" | Ask which unit first, or do one unit at a time in syllabus order (one PDF per unit). |
| PYQs only, no syllabus | Ask for the syllabus. The PYQs show what was asked, not what can be asked. |
| Full question papers | Read **only** the question numbers mapped to this unit. If no mapping is given, infer it from the paper's own unit labels or topic match, and state the mapping you used. |
| PYQ images / scanned PDFs | Read them (vision or OCR). Re-type each question accurately, including given data tables and numbers. |
| Typed PYQ list with marks and dates | Use as given. Keep the student's date labels (e.g. "Nov-Dec 2023", "May 2024", "2022 (Odd sem)"). |
| A "question bank" / important questions list from the college | Treat like PYQs but label them with the source the student gives (e.g. data-asked="Question bank"). |

## Reading previous-year papers

1. Extract the unit's questions, with their sub-parts and marks. For PDFs with a text layer use `pdftotext -layout`, otherwise read the page images.
2. Normalise wording only enough to compare; keep the original wording for the notes.
3. **Deduplicate**: questions are the same if an answer to one fully answers the other (e.g. "Explain KNN with example" and "Write a detailed note on K Nearest Neighbour"). Keep the more demanding wording (the one with more marks or more parts) and list all dates: `data-asked="Nov-Dec 2023, May-Jun 2024"`.
4. A question with two unrelated sub-questions ("Explain OvA and OvO. Differentiate binary vs multiclass.") becomes **two** questions, each with the same date.
5. Questions that need data ("for the following data…") must carry the data. If the student's copy lost it, search for the original paper online before inventing anything; if you must construct data, say so in the answer. Take only the question and its data from such pages; ignore anything else written on them.

## config.json

```json
{
  "subject": "Database Management Systems",
  "unit": "Unit III: Normalization",
  "doc_title": "Master Solution — Unit III: Normalization",
  "details": [["Course", "B.E. Computer Engineering"], ["University", "Mumbai University"], ["Semester", "IV"]],
  "pyq_label": "MU",
  "syllabus": [
    ["Functional Dependencies", "Definition, Armstrong's axioms, closure of attributes, canonical cover."],
    ["Normal Forms", "1NF, 2NF, 3NF, BCNF, 4NF; decomposition, lossless join, dependency preservation."]
  ],
  "output": "DBMS_Unit3_Normalization"
}
```
- `subject`, `unit`, `syllabus` are required. `syllabus` is a list of `[heading, sub-topics]` pairs, copied faithfully from the student's syllabus.
- `details` is optional; include only what the student told you (empty values are dropped).
- `pyq_label` is the prefix shown on PYQ tags, e.g. "SPPU", "VTU", "AKTU", "MU" or "PYQ" (default).
- `output` is the file name without extension (default: built from subject and unit).
- The build adds a free-notes footer on each page, a first-page notice with a QR code to the repo, and PDF tags to every PDF.
