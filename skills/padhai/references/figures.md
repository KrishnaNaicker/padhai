# Figures that look hand-made by a topper, not by a robot

## When to draw

A long answer (≥ 5 marks) about any of these needs a figure: architecture, process / workflow / pipeline, cycle, hierarchy or types, network / graph / tree, geometric idea (hyperplane, margin, clusters, decision boundary), curve or trend, data distribution, before/after comparison, a worked example's data (scatter of points, a matrix heat-map).

Never draw a figure that only repeats a table. Never use photos or copyrighted images.

## How

```python
# fig_unit.py, run from inside the unit folder:  python fig_unit.py
import sys; sys.path.insert(0, "<skill>/scripts")
from fig_lib import *

f, ax = canvas(8, 3)                                          # diagram area 8 x 3 units
flow(ax, [1.2, 4, 6.8], 1.5, ["Raw data", "Clean +\nscale", "Train model"], [BLU, YEL, GRN], w=2.0)
save(f, "pipeline")                                           # fig/pipeline.svg + fig/_preview/pipeline.png
```

Helpers: `canvas`, `box`, `arr`, `flow`, `vflow`, `node`, `edge(label=…)`, `inhibit`, `label` (text on a white patch). Plots: normal matplotlib (`plt.subplots`), colours from `C[0..4]`, then `save`.

Style (already set by fig_lib): serif text, text converted to outlines (identical on every computer), transparent background, no top/right spines.

## Rules

1. **Size**: `figsize` about (4–5, 3) for one plot, (7, 2.6–3.2) for two panels or a wide flow. Font 8–10 pt. Never shrink text below 7.5 pt to make it fit: widen the figure instead.
2. **Colour only inside figures**, muted: `C` for series, `BLU YEL GRN PNK PUR ORG LG` for box fills. Same meaning, same colour, across the unit.
3. **Distinguish classes by marker shape as well as colour** (o, ^, s) so the figure survives black-and-white printing.
4. **Label everything** that the answer refers to: axes with units, boundaries, regions, support vectors, K circles.
5. **No overlaps**: text must not touch lines, markers, other text or the figure edge. Use `label()` (white backing) for text that sits on lines, and leader arrows (`ax.annotate`) for crowded points.
6. **Worked-example figures must match the computed numbers exactly** (same points, same boundary, same result).
7. Prefer two simple panels to one crowded panel.

## Look at every figure (mandatory)

```bash
python <skill>/scripts/qa.py figs <unit>      # -> <unit>/qa/figs_0.png, figs_1.png ...
```
Open each sheet image. For each figure ask: Is any text overlapping or clipped? Does an arrow cross text? Is anything too small to read when printed? Does it show what the caption claims? Fix → re-run the script → look again. Expect 2–3 rounds; that is normal.
