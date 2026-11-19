"""
Padhai figure helpers. Import from a figure script that runs inside the unit folder:

    import sys; sys.path.insert(0, "<path to padhai>/scripts")
    from fig_lib import *

    f, ax = canvas(7, 3)                     # blank diagram area, 0..7 by 0..3, axes hidden
    flow(ax, [1, 3.5, 6], 1.5, ["Input", "Model", "Output"], [BLU, YEL, GRN])
    save(f, "pipeline")                      # -> fig/pipeline.svg and fig/_preview/pipeline.png

Rules (see references/figures.md):
  * Serif text, colours only inside figures, white/transparent background.
  * Text is converted to outlines in the SVG, so it looks identical on every computer.
  * After saving, LOOK at fig/_preview/*.png (python qa.py figs) and fix every overlap.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Ellipse, Polygon  # noqa: F401

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.fonttype": "path",
})

# Series colours for plots, and soft fills for boxes.
C = ["#2b6cb0", "#d97706", "#059669", "#9333ea", "#dc2626"]
NAVY = "#1e2a4a"; GREY = "#9aa3b5"; LG = "#eef2f7"
YEL = "#fde68a"; BLU = "#dbeafe"; GRN = "#d1fae5"; PNK = "#fee2e2"; PUR = "#e9d5ff"; ORG = "#fed7aa"

FIG_DIR = "fig"


def canvas(w, h, scale=1.0):
    """A blank drawing area w x h data units (axes hidden). Returns (figure, axes)."""
    f, ax = plt.subplots(figsize=(w * scale, h * scale))
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    return f, ax


def save(f, name, preview=True):
    """Write fig/<name>.svg (for the notes) and fig/_preview/<name>.png (for checking)."""
    os.makedirs(FIG_DIR, exist_ok=True)
    f.savefig(f"{FIG_DIR}/{name}.svg", bbox_inches="tight", transparent=True)
    if preview:
        os.makedirs(f"{FIG_DIR}/_preview", exist_ok=True)
        f.savefig(f"{FIG_DIR}/_preview/{name}.png", bbox_inches="tight", dpi=110, facecolor="white")
    plt.close(f)


def box(ax, x, y, w, h, t, fc="white", ec=NAVY, tc=NAVY, fs=8.6, bold=False):
    """Rounded box centred at (x, y) with text. Make w wide enough for the text (check the preview)."""
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.2, zorder=2))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", zorder=3)


def arr(ax, a, b, c=NAVY, rad=0, lw=1.1, style="-|>"):
    """Arrow from point a to point b. rad bends it (e.g. 0.3)."""
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=10, color=c, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", zorder=1))


def flow(ax, xs, y, labels, fcs, w=1.8, h=1.0, fs=8.2):
    """A left-to-right chain of boxes joined by arrows."""
    for x, l, fc in zip(xs, labels, fcs):
        box(ax, x, y, w, h, l, fc=fc, fs=fs)
    for i in range(len(xs) - 1):
        arr(ax, (xs[i] + w / 2, y), (xs[i + 1] - w / 2, y))


def vflow(ax, x, ys, labels, fcs, w=2.6, h=0.8, fs=8.2):
    """A top-to-bottom chain of boxes joined by arrows (ys from top to bottom)."""
    for y, l, fc in zip(ys, labels, fcs):
        box(ax, x, y, w, h, l, fc=fc, fs=fs)
    for i in range(len(ys) - 1):
        arr(ax, (x, ys[i] - h / 2), (x, ys[i + 1] + h / 2))


def node(ax, x, y, t, r=0.4, fc=YEL, fs=9, ec=NAVY):
    """Circular node (graphs, trees, networks)."""
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=1.3, zorder=3))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, zorder=4, fontweight="bold")


def edge(ax, p, q, r1=0.4, r2=0.4, c=NAVY, rad=0, lw=1.2, head=True, label=None, fs=8):
    """Edge between two nodes that stops at their borders. Optional label at the midpoint."""
    p = np.array(p, float); q = np.array(q, float); d = (q - p) / np.linalg.norm(q - p)
    a = tuple(p + d * r1); b = tuple(q - d * r2)
    if head:
        arr(ax, a, b, c=c, rad=rad, lw=lw)
    else:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=c, lw=lw, zorder=1)
    if label is not None:
        m = (np.array(a) + np.array(b)) / 2
        ax.text(m[0], m[1], label, fontsize=fs, ha="center", va="center", zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.6))


def inhibit(ax, p, q, r1=0.4, r2=0.4, c="#dc2626", lw=1.6):
    """Blunt-ended line (inhibition / blocking)."""
    p = np.array(p, float); q = np.array(q, float); d = (q - p) / np.linalg.norm(q - p)
    a = p + d * r1; b = q - d * r2
    ax.plot([a[0], b[0]], [a[1], b[1]], color=c, lw=lw, zorder=1)
    perp = np.array([-d[1], d[0]]) * 0.18
    ax.plot([b[0] - perp[0], b[0] + perp[0]], [b[1] - perp[1], b[1] + perp[1]], color=c, lw=2.2, zorder=2)


def label(ax, x, y, t, fs=8.5, ha="center", color="black", **kw):
    """Text with a white backing so lines behind it never cut through the letters."""
    ax.text(x, y, t, fontsize=fs, ha=ha, va="center", color=color, zorder=6,
            bbox=dict(fc="white", ec="none", pad=0.8), **kw)
