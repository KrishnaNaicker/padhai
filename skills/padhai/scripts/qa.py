#!/usr/bin/env python3
"""
Padhai visual QA: make contact sheets you can LOOK at, so overlaps and layout bugs are caught.

    python qa.py figs <unit_dir>               # tiles fig/_preview/*.png -> <unit_dir>/qa/figs_N.png
    python qa.py pdf  <file.pdf>               # 8 pages per sheet         -> qa/pages_N.png next to the PDF
    python qa.py page <file.pdf> <n> [zoom]    # one page at higher zoom   -> qa/page_<n>.png

Needs Pillow. For PDFs it uses PyMuPDF (pip install pymupdf) or, if absent, poppler's pdftoppm.
"""
import glob, os, shutil, subprocess, sys, tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("pip install pillow")


def pdf_pages(pdf, dpi, first=None, last=None):
    """Return a list of PIL images for the PDF pages."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf)
        rng = range((first or 1) - 1, (last or len(doc)))
        out = []
        for i in rng:
            pix = doc[i].get_pixmap(dpi=dpi)
            out.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        return out
    except ImportError:
        if not shutil.which("pdftoppm"):
            sys.exit("Install PyMuPDF (pip install pymupdf) or poppler (pdftoppm) to render PDF pages.")
        t = tempfile.mkdtemp()
        cmd = ["pdftoppm", "-r", str(dpi), "-png"]
        if first:
            cmd += ["-f", str(first), "-l", str(last or first)]
        subprocess.run(cmd + [pdf, f"{t}/p"], check=True)
        return [Image.open(f).convert("RGB") for f in sorted(glob.glob(f"{t}/p-*.png"))]


def tile(images, cols, out):
    w = max(i.width for i in images); h = max(i.height for i in images)
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), "white")
    for k, im in enumerate(images):
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    sheet.save(out)
    print(out)


def figs(unit):
    prev = sorted(glob.glob(os.path.join(unit, "fig", "_preview", "*.png")))
    if not prev:
        sys.exit("no previews in fig/_preview (save figures with fig_lib.save)")
    qa = Path(unit, "qa"); qa.mkdir(exist_ok=True)
    ims = [Image.open(p).convert("RGB") for p in prev]
    # 4 figures per sheet, stacked in 2 columns, each scaled to a common width
    W = 900
    ims = [i.resize((W, int(i.height * W / i.width))) for i in ims]
    for s in range(0, len(ims), 4):
        chunk = ims[s:s + 4]
        cols = [chunk[0::2], chunk[1::2]]
        H = max(sum(i.height + 12 for i in c) for c in cols if c)
        sheet = Image.new("RGB", (W * 2 + 24, H), "white")
        for c, col in enumerate(cols):
            y = 0
            for im in col:
                sheet.paste(im, (c * (W + 24), y)); y += im.height + 12
        out = qa / f"figs_{s // 4}.png"; sheet.save(out); print(out, " <- ", ", ".join(Path(p).stem for p in prev[s:s + 4]))


def pdf(path):
    qa = Path(path).parent / "qa"; qa.mkdir(exist_ok=True)
    pages = pdf_pages(path, 55)
    for s in range(0, len(pages), 8):
        tile(pages[s:s + 8], 4, qa / f"pages_{s // 8}.png")
    print(f"{len(pages)} pages")


def page(path, n, zoom=130):
    qa = Path(path).parent / "qa"; qa.mkdir(exist_ok=True)
    im = pdf_pages(path, int(zoom), int(n), int(n))[0]
    out = qa / f"page_{n}.png"; im.save(out); print(out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "figs":
        figs(sys.argv[2])
    elif cmd == "pdf":
        pdf(sys.argv[2])
    elif cmd == "page":
        page(sys.argv[2], sys.argv[3], *(sys.argv[4:5]))
    else:
        sys.exit(__doc__)
