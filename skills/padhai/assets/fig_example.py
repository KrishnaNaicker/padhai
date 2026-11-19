# Example figure script for part_template.html (a Gantt chart). Run from inside the unit folder.
import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))   # adjust to <skill>/scripts
from fig_lib import *

f, ax = canvas(9, 1.6)
segs = [("P1", 0, 5, BLU), ("P2", 5, 8, YEL), ("P3", 8, 16, GRN), ("P4", 16, 22, PNK)]
s = 8 / 22
for name, a, b, fc in segs:
    box(ax, 0.5 + s * (a + b) / 2, 1.0, s * (b - a), 0.6, name, fc=fc, fs=9, bold=True)
for t in [0, 5, 8, 16, 22]:
    ax.text(0.5 + s * t, 0.45, str(t), ha="center", fontsize=8.5)
save(f, "gantt")
