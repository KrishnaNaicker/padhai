# Padhai markup: the complete reference

Write **content only**. The build turns this markup into the finished layout: header table, free-notes notice with QR code, question index, bordered Q/Ans boxes with `[6M] [PYQ: date]` tags, "PART A — …" bars, "Step N:" numbering, Sr. No. columns, page headers ("Subject · Page N · Unit") and the black/grey/white theme.

Files: `01_partA.html`, `02_partB.html`, … (any name after the two-digit number). They are joined in order. No `<html>`, `<head>` or `<body>`: just the elements below. `assets/part_template.html` shows every element in use; the example unit shows a full real unit.

## Structure

```html
<div class="part" data-title="Binary Classification and its Evaluation"
     data-sub="Linear model · Confusion matrix · Accuracy · Precision · Recall"></div>

<div class="q" data-marks="12" data-asked="Nov-Dec 2024, May-Jun 2023">
  <div class="qt">Write formulas for accuracy, precision, recall and F1-score. Calculate them for the given confusion matrix.</div>
  <div class="ans">
    ... answer elements ...
  </div>
</div>

<div class="part rev" data-title="Rapid Revision Sheet" data-sub="Read the night before the exam"></div>
<div class="rev"> ... </div>
```

| Attribute | Meaning |
|---|---|
| `data-marks` | `"6"`, `"6–8"`, `"12"`. Shown as `[6M]`. Required. |
| `data-asked` | Comma-separated exam dates for a PYQ. Omit (or `"Expected"`) for Expected questions. |
| `data-index` | Optional shorter wording for the index (long PYQs with data). |
| `data-n` | Optional custom number (default Q1, Q2, … in order). |

Parts are lettered A, B, C … automatically. Questions are numbered Q1, Q2 … automatically.

## Answer elements

```html
<h4>Definition</h4>                     <!-- section heading; the build adds the colon -->
<h5>Sub-heading</h5>

<div class="def"><b>Term</b> is ... (2–3 sentences, keywords bold)</div>

<p>Normal paragraph.</p>
<ul><li><b>Point:</b> explanation.</li></ul>

<ol class="steps">                       <!-- renders "Step 1:", "Step 2:" ... -->
  <li><b>Choose K</b>, the number of neighbours.</li>
</ol>

<div class="formula"><span class="lbl">Euclidean distance</span>
$$d=\sqrt{\sum_i (x_i-y_i)^2}$$
<div class="where"><b>x, y</b> = feature vectors, <b>i</b> = feature index.</div></div>

<div class="tip">If the paper prints the matrix the other way round, precision and recall swap.</div>
<div class="hook"><b>Precision looks at the Predicted column; Recall at the Real row.</b></div>
<div class="concl">One or two sentences restating the core idea.</div>   <!-- every answer -->
```

### Tables

```html
<table class="t">
<tr><th style="width:22%">Basis</th><th>Binary Classification</th><th>Multiclass Classification</th></tr>
<tr><td>Number of classes</td><td>Exactly 2</td><td>3 or more</td></tr>
</table>
```
- First row is `<th>` headers. Every table needs `class="t"`.
- First header **"Basis"** (or Feature, Parameter, Aspect, Point, Criterion, Property) → a "Sr. No." column is added automatically. Add class `sr` to force it on any table.
- `class="t num"` centres every cell (numerical tables). `<td class="hl">` highlights a key cell (e.g. TP, the chosen neighbours, the final answer).
- `<p class="cap">Table caption</p>` under a table if needed.
- Tables longer than 7 rows may break across pages; rows never split.
- Keep tables to ≤ 5 columns so text stays readable.

### Figures

```html
<figure><img src="fig/knn.svg" style="width:56%"><figcaption>Fig. 3.7 · The same point gets a different class for K = 3 and K = 7</figcaption></figure>
```
- Number figures `Fig. <unit>.<n>` in order of appearance, unique in the unit.
- Width: 50–65 % for single plots/diagrams, 85–95 % for wide two-panel figures.

### Two columns, code, small text

```html
<div class="two"><div> left column </div><div> right column </div></div>
<pre class="code">for i in range(n):
    print(i)</pre>
<code>inline_code()</code>   <span class="sm">smaller note text</span>
```

### Simple HTML diagrams (no image needed)

```html
<div class="flow"><span class="n">Data</span><span class="ar">→</span><span class="n">Model</span>
  <span class="ar">→</span><span class="n e">Prediction</span></div>

<div class="tree"><div class="root">Classification</div>
  <div class="kids"><div class="kid"><b>Binary</b><i>2 classes</i></div> ... 4 kids (use class "kids c3" for 3)</div></div>
```

### Revision sheet

```html
<div class="part rev" data-title="Rapid Revision Sheet" data-sub="Read the night before the exam"></div>
<div class="rev">
<div class="two">
  <div><div class="box"><h5>Core formulas</h5><ul><li>...</li></ul></div></div>
  <div><div class="box"><h5>One-liners examiners love</h5><ul><li>...</li></ul></div></div>
</div>
<div class="box"><h5>If they ask X → make sure you write Y</h5>
  <table class="t"><tr><th>Question says</th><th>Must include</th></tr> ... </table></div>
<div class="box"><h5>Numerical answers to re-check</h5> <table class="t num"> ... </table></div>
</div>
```

## Maths (KaTeX)

- Inline `$...$`, display `$$...$$`. Standard LaTeX maths: `\frac`, `\sqrt`, `\sum`, `\lVert w\rVert`, `\operatorname{sign}`, `\begin{cases}…\end{cases}`, `\underbrace`, `\text{...}`.
- Write `<` and `>` inside maths as `\lt` and `\gt` (or `&lt;` `&gt;`); a raw `<` breaks the HTML.
- A literal dollar sign in text is `\$` (or write "USD"). An odd number of `$` on a line is a lint error.
- One display formula should fit one line (≈ 100 characters of LaTeX). Split longer ones into several `$$…$$` lines.
- Prefer Unicode for simple symbols in prose and tables (x₁, σ², ≤, →, ×) and LaTeX for real formulas.

## Do not

- Add colours, fonts, emojis, icons or inline styles beyond `width` on images and table headers.
- Write `<table>` without `class="t"`, or end `<h4>`/`<h5>` text with ":".
- Put a question's marks/date in the question text: they come from the attributes.
- Number steps or figures in a way that skips or repeats.
- Edit the free-notes footer, first-page notice or PDF tags: the build adds them as part of the standard output.
