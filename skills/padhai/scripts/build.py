#!/usr/bin/env python3
"""
Padhai build: turn a unit folder into one print-ready HTML file and a PDF.

    python build.py <unit_dir> [--math auto|node|cdn] [--html-only] [--no-inline]

The unit folder holds:
    config.json        subject, unit, syllabus, optional details (see SKILL.md)
    NN_*.html          answer parts in Padhai markup, built in file-name order
    fig/*.svg          figures made with fig_lib.py

Output (inside the unit folder):
    <output>.html      self-contained: CSS, fonts and figures inlined
    <output>.pdf       when a Chromium-family browser (Chrome, Edge, Chromium, Brave) is found

Requires: Python 3.8+, beautifulsoup4.
Optional: Node.js + `npm install katex` (offline maths), pypdf (page count).
Without Node, maths is rendered by KaTeX from a CDN at print time (needs internet).
Without a browser, open the HTML file and use Print -> Save as PDF.
"""
import argparse, base64, glob, html, json, os, platform, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ASSETS = SKILL / "assets"
KATEX_CDN = os.environ.get("PADHAI_KATEX_URL", "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist")

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Padhai needs beautifulsoup4. Install it with:  pip install beautifulsoup4")


def die(msg):
    sys.exit("BUILD FAILED: " + msg)


# --------------------------------------------------------------------------- config
def load_config(d):
    p = d / "config.json"
    if not p.exists():
        die(f"{p} not found. Copy assets/config.example.json into the unit folder and fill it in.")
    cfg = json.loads(p.read_text(encoding="utf8"))
    for k in ("subject", "unit", "syllabus"):
        if not cfg.get(k):
            die(f'config.json is missing "{k}".')
    cfg.setdefault("pyq_label", "PYQ")
    cfg.setdefault("doc_title", f"Master Solution — {cfg['unit']}")
    cfg.setdefault("details", [])
    slug = re.sub(r"[^A-Za-z0-9]+", "_", f"{cfg['subject']} {cfg['unit']}").strip("_")
    cfg.setdefault("output", slug + "_Notes")
    return cfg


# --------------------------------------------------------------------------- maths
def have_node():
    return shutil.which("node") is not None


def render_math_node(raw):
    with tempfile.TemporaryDirectory() as t:
        a, b = Path(t, "in.html"), Path(t, "out.html")
        a.write_text(raw, encoding="utf8")
        r = subprocess.run(["node", str(HERE / "render_math.js"), str(a), str(b)],
                           capture_output=True, text=True)
        if r.returncode == 3:
            return None, None
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            die("a formula failed to render (see MATH ERROR above). Fix the LaTeX and rebuild.")
        kdir = ""
        for line in r.stdout.splitlines():
            if line.startswith("KATEX_DIR="):
                kdir = line.split("=", 1)[1].strip()
        return b.read_text(encoding="utf8"), kdir


def katex_css_inline(kdir):
    css = Path(kdir, "dist", "katex.min.css").read_text(encoding="utf8")
    fonts = Path(kdir, "dist")

    def sub(m):
        f = fonts / m.group(1)
        data = base64.b64encode(f.read_bytes()).decode()
        return f'src:url(data:font/woff2;base64,{data}) format("woff2")'

    return re.sub(r'src:url\((fonts/[^)]+?\.woff2)\) format\("woff2"\)(?:,url\([^)]+\) format\("[^"]+"\))*', sub, css)


CDN_HEAD = f"""
<link rel="stylesheet" href="{KATEX_CDN}/katex.min.css">
<script defer src="{KATEX_CDN}/katex.min.js"></script>
<script defer src="{KATEX_CDN}/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}});"></script>
"""


# --------------------------------------------------------------------------- transform
def frag(s):
    return BeautifulSoup(s, "html.parser")


def esc(s):
    return html.escape(str(s), quote=False)


def marks_text(m):
    m = str(m).strip()
    if not m:
        return ""
    return m if m.upper().endswith("M") or "mark" in m.lower() else m + "M"


def asked_list(q):
    a = (q.get("data-asked") or "").strip()
    if not a or a.lower() == "expected":
        return []
    return [x.strip() for x in a.split(",") if x.strip()]


def header_html(cfg, nq):
    det = [(k, v) for k, v in cfg["details"] if str(v).strip()]
    det.append(("Total Questions", nq))
    rows = [f'<tr><th colspan="6">{esc(cfg["doc_title"]).upper()}</th></tr>']
    first = [("Subject", cfg["subject"])] + det[:1]
    rest = det[1:]
    chunks = [first] + [rest[i:i + 3] for i in range(0, len(rest), 3)]
    for ch in chunks:
        span = 6 // len(ch)
        rows.append("<tr>" + "".join(f'<td colspan="{span}">{esc(k)}: {esc(v)}</td>' for k, v in ch) + "</tr>")
    syl = "".join(f"<p><b>{esc(k)}:</b> {esc(v)}</p>" for k, v in cfg["syllabus"])
    rows.append(f'<tr><td colspan="6" class="syl">{syl}</td></tr>')
    return '<table class="mh">' + "".join(rows) + "</table>"


REPO = "github.com/KrishnaNaicker/padhai"


def notice_html():
    """First-page notice: these notes are free, with a QR code to the repo. Always included."""
    qr = base64.b64encode((ASSETS / "qr.svg").read_bytes()).decode()
    return (
        '<table class="notice"><tr>'
        f'<td class="qr"><img src="data:image/svg+xml;base64,{qr}" alt="QR code: {REPO}"></td>'
        '<td><b>Free notes. Not for sale.</b> These notes were made with <b>Padhai</b>, a free and open-source tool '
        f'that writes exam notes for any syllabus. Get it at <b>{REPO}</b> (scan the code). '
        'If you paid for this PDF, you were scammed. Please share Padhai so no student has to pay for notes.</td>'
        '</tr></table>')


def transform(body_html, cfg):
    soup = BeautifulSoup(body_html, "html.parser")
    label = cfg["pyq_label"]

    # number parts and questions
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pi, qn = 0, 0
    index_rows = []
    for el in soup.find_all(["div"], class_=["part", "q"]):
        cls = el.get("class") or []
        if "part" in cls:
            title = el.get("data-title", "").strip()
            sub = el.get("data-sub", "").strip()
            if "rev" in cls:
                head = title.upper() or "RAPID REVISION SHEET"
                index_rows.append(("part", "Last pages"))
                index_rows.append(("rev", title or "Rapid Revision Sheet", sub))
            else:
                head = f"PART {letters[pi]} — {title.upper()}"
                index_rows.append(("part", f"Part {letters[pi]} · {title}"))
                pi += 1
            el.replace_with(frag(f'<div class="partbar"><b>{esc(head)}</b>' + (f"<span>{esc(sub)}</span>" if sub else "") + "</div>"))
        else:
            qn += 1
            n = el.get("data-n") or f"Q{qn}"
            qt = el.find("div", class_="qt")
            ans = el.find("div", class_="ans")
            if qt is None or ans is None:
                die(f'question {n} needs <div class="qt"> and <div class="ans"> inside it.')
            marks = marks_text(el.get("data-marks", ""))
            asked = asked_list(el)
            ak = f"[{label}: " + ", ".join(asked) + "]" if asked else "[Expected]"
            idx_q = el.get("data-index") or qt.get_text(" ", strip=True)
            index_rows.append(("q", n, idx_q, marks, (f"{label}: " + ", ".join(asked)) if asked else "Expected"))
            mk = f' <span class="mk">[{esc(marks)}]</span>' if marks else ""
            box = frag(
                '<table class="qbox"><colgroup><col style="width:48px"><col></colgroup>'
                '<thead><tr class="cp"><td></td><td></td></tr></thead>'
                '<tfoot><tr class="cp"><td></td><td></td></tr></tfoot><tbody>'
                f'<tr class="qrow"><td class="qn">{esc(n)}</td><td class="qt">{qt.decode_contents()}{mk} <span class="ak">{esc(ak)}</span></td></tr>'
                '<tr class="arow"><td class="an">Ans.</td><td class="ac"></td></tr></tbody></table>')
            ac = box.select_one(".ac")
            for ch in list(ans.contents):
                ac.append(ch.extract())
            el.replace_with(box)

    if qn == 0:
        die('no questions found. Each question must be <div class="q" data-marks="..."> with .qt and .ans inside.')

    # index
    idx = ""
    for r in index_rows:
        if r[0] == "part":
            idx += f'<tr><td colspan="4" class="ip">{esc(r[1])}</td></tr>'
        elif r[0] == "rev":
            idx += f'<tr><td class="c">★</td><td>{esc(r[1])}' + (f": {esc(r[2])}" if r[2] else "") + '</td><td class="c"></td><td class="c"></td></tr>'
        else:
            idx += f'<tr><td class="c">{esc(r[1])}</td><td>{esc(r[2])}</td><td class="c">{esc(r[3])}</td><td class="c">{esc(r[4])}</td></tr>'
    npyq = sum(1 for r in index_rows if r[0] == "q" and r[4] != "Expected")
    note = '<table class="t note"><tr><th colspan="2">How to use these notes</th></tr>'
    if npyq:
        note += (f'<tr><td style="width:24%">{esc(label)}: date</td><td>Asked in previous papers. Learn these first. '
                 'A question listing more than one date has come more than once.</td></tr>')
    note += ('<tr><td style="width:24%">Expected</td><td>Syllabus topics not asked yet. Each answer is written so it also '
             'works for a reworded question.</td></tr>'
             '<tr><td>Long answers</td><td>Definition → explanation → diagram → example → advantages / limitations → '
             'applications → conclusion.</td></tr></table>')
    index = ('<table class="t idx"><thead><tr><th style="width:7%">Q. No.</th><th>Question</th>'
             '<th style="width:9%">Marks</th><th style="width:21%">Asked in</th></tr></thead>'
             f"<tbody>{idx}</tbody></table>")
    cover = frag(header_html(cfg, qn) + notice_html() + index + note)
    first = soup.find(True)
    if first is not None:
        first.insert_before(cover)
    else:
        soup.append(cover)

    # stack two-column blocks that start with headings
    for t in soup.select("div.two"):
        kids = [c for c in t.children if getattr(c, "name", None)]
        firsts = [next((x for x in k.children if getattr(x, "name", None)), None) for k in kids]
        if len(kids) == 2 and all(f is not None and f.name in ("h4", "h5") for f in firsts):
            t["class"] = ["stack"]
    for t in soup.select(".rev div.two"):
        t["class"] = ["stack"]

    # Sr. No. column for comparison tables
    keys = {"basis", "feature", "parameter", "aspect", "point", "criterion", "criteria", "property", "point of difference"}
    for tb in soup.select("table.t"):
        rows = tb.find_all("tr")
        if not rows:
            continue
        ths = rows[0].find_all("th")
        if ths and (ths[0].get_text(strip=True).lower() in keys or "sr" in (tb.get("class") or [])) and \
                ths[0].get_text(strip=True) != "Sr. No.":
            th = soup.new_tag("th"); th.string = "Sr. No."; th["class"] = ["sr"]; rows[0].insert(0, th)
            for i, r in enumerate(rows[1:], 1):
                td = soup.new_tag("td"); td.string = str(i); td["class"] = ["sr"]; r.insert(0, td)
            tb["class"] = (tb.get("class") or []) + ["cmp"]

    # long tables may break across pages, but rows never split
    for tb in soup.select("table.t"):
        if "idx" in (tb.get("class") or []):
            continue
        rows = tb.find_all("tr")
        if len(rows) > 7 and rows[0].find("th") and not tb.find("thead"):
            th = soup.new_tag("thead"); tbody = soup.new_tag("tbody")
            first_row = rows[0].extract(); th.append(first_row)
            for r in rows[1:]:
                tbody.append(r.extract())
            tb.append(th); tb.append(tbody)
            tb["class"] = (tb.get("class") or []) + ["long"]

    return soup, qn, npyq


def inline_images(soup, d):
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith(("data:", "http")):
            continue
        p = (d / src)
        if not p.exists():
            die(f"figure not found: {src}")
        mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(p.suffix.lower(), "application/octet-stream")
        img["src"] = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


# --------------------------------------------------------------------------- pdf
def find_browser():
    env = os.environ.get("PADHAI_BROWSER") or os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "microsoft-edge", "microsoft-edge-stable", "msedge", "brave-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    cands = []
    if platform.system() == "Darwin":
        cands = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                 "/Applications/Chromium.app/Contents/MacOS/Chromium",
                 "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"]
    elif platform.system() == "Windows":
        for base in (os.environ.get("PROGRAMFILES", r"C:\Program Files"),
                     os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
                     os.environ.get("LOCALAPPDATA", "")):
            cands += [rf"{base}\Google\Chrome\Application\chrome.exe",
                      rf"{base}\Microsoft\Edge\Application\msedge.exe",
                      rf"{base}\BraveSoftware\Brave-Browser\Application\brave.exe"]
    for c in cands:
        if c and Path(c).exists():
            return c
    return None


def print_pdf(browser, html_path, pdf_path, cdn):
    args = [browser, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}"]
    if platform.system() == "Linux" and hasattr(os, "geteuid") and os.geteuid() == 0:
        args.append("--no-sandbox")
    if cdn:
        args.append("--virtual-time-budget=20000")
    args.append(html_path.as_uri())
    subprocess.run(args, capture_output=True, text=True, timeout=240)
    return pdf_path.exists() and pdf_path.stat().st_size > 1000


def tag_pdf(pdf, cfg):
    """Write ownership tags into the PDF metadata (needs pypdf)."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return False
    w = PdfWriter(clone_from=str(pdf))
    w.add_metadata({
        "/Title": f"{cfg['subject']} – {cfg['unit']} – Notes",
        "/Author": f"Made with Padhai ({REPO})",
        "/Subject": f"Free exam notes made with Padhai, {REPO}. Not for sale.",
        "/Keywords": "Padhai, free exam notes, not for sale, open source, " + REPO,
        "/Creator": f"Padhai ({REPO})",
    })
    with open(pdf, "wb") as fh:
        w.write(fh)
    return True


def page_count(pdf):
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf)).pages)
    except Exception:
        try:
            return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
        except Exception:
            return "?"


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Build Padhai notes for one unit.")
    ap.add_argument("unit_dir")
    ap.add_argument("--math", choices=["auto", "node", "cdn"], default="auto")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--no-inline", action="store_true", help="link figures instead of embedding them")
    a = ap.parse_args()

    d = Path(a.unit_dir).resolve()
    cfg = load_config(d)
    parts = sorted(p for p in d.iterdir() if re.match(r"^\d\d_.*\.html$", p.name))
    if not parts:
        die("no part files found. Name them 01_partA.html, 02_partB.html, ...")
    body = "\n".join(p.read_text(encoding="utf8") for p in parts)

    mode, katex_css = None, ""
    if a.math in ("auto", "node") and have_node():
        out, kdir = render_math_node(body)
        if out is not None:
            body, mode = out, "node"
            if kdir:
                katex_css = katex_css_inline(kdir)
    if mode is None:
        if a.math == "node":
            die("--math node requested but Node.js/katex is not available (npm install katex).")
        mode = "cdn"

    soup, nq, npyq = transform(body, cfg)
    if not a.no_inline:
        inline_images(soup, d)

    css = (ASSETS / "style.css").read_text(encoding="utf8")
    css = css.replace("{{SUBJECT}}", cfg["subject"].replace('"', "'")).replace("{{UNIT}}", cfg["unit"].replace('"', "'"))
    head = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<title>{esc(cfg["subject"])} – {esc(cfg["unit"])} – Notes</title>'
            f'<meta name="author" content="Made with Padhai ({REPO})"><meta name="description" content="Free exam notes made with Padhai. Not for sale.">'
            + (f"<style>{katex_css}</style>" if katex_css else (CDN_HEAD if mode == "cdn" else ""))
            + f"<style>{css}</style></head><body>")
    out_html = d / (cfg["output"] + ".html")
    out_html.write_text(head + str(soup) + "</body></html>", encoding="utf8")
    print(f"questions: {nq} ({npyq} PYQ, {nq - npyq} Expected) · maths: {mode}")
    print(f"html: {out_html}")

    if a.html_only:
        return
    browser = find_browser()
    if not browser:
        print("pdf: no Chrome/Edge/Chromium found. Open the HTML file in a browser -> Print -> "
              "Save as PDF (paper A4, margins Default, tick 'Background graphics').")
        return
    pdf = d / (cfg["output"] + ".pdf")
    if pdf.exists():
        pdf.unlink()
    if print_pdf(browser, out_html, pdf, mode == "cdn"):
        tagged = tag_pdf(pdf, cfg)
        print(f"pdf: {pdf}  ({page_count(pdf)} pages)" + ("" if tagged else "  [pip install pypdf to add PDF tags]"))
    else:
        print("pdf: the browser did not produce a PDF. Open the HTML file and use Print -> Save as PDF.")


if __name__ == "__main__":
    main()
