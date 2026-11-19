#!/usr/bin/env python3
"""
Padhai lint: catch structural mistakes before building.

    python check.py <unit_dir>

Errors (exit 1) must be fixed. Warnings are worth a look.
"""
import json, re, sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip install beautifulsoup4")

d = Path(sys.argv[1]).resolve()
errors, warns = [], []
E = errors.append
W = warns.append

cfgp = d / "config.json"
if not cfgp.exists():
    E("config.json missing")
    cfg = {}
else:
    try:
        cfg = json.loads(cfgp.read_text(encoding="utf8"))
    except Exception as e:
        E(f"config.json is not valid JSON: {e}")
        cfg = {}
for k in ("subject", "unit", "syllabus"):
    if cfg and not cfg.get(k):
        E(f'config.json: "{k}" is missing')
if cfg.get("syllabus") and not all(isinstance(x, list) and len(x) == 2 for x in cfg["syllabus"]):
    E('config.json: "syllabus" must be a list of ["Topic heading", "sub-topics text"] pairs')

parts = sorted(p for p in d.iterdir() if re.match(r"^\d\d_.*\.html$", p.name))
if not parts:
    E("no NN_*.html part files")

figs_seen, qcount, pyq, has_rev = [], 0, 0, False
for p in parts:
    src = p.read_text(encoding="utf8")
    soup = BeautifulSoup(src, "html.parser")
    if soup.select("div.part.rev") or soup.select("div.rev"):
        has_rev = True
    for q in soup.select("div.q"):
        qcount += 1
        tag = f"{p.name} Q{qcount}"
        if not q.get("data-marks"):
            E(f"{tag}: data-marks missing")
        if not q.find("div", class_="qt"):
            E(f'{tag}: <div class="qt"> missing')
        ans = q.find("div", class_="ans")
        if not ans:
            E(f'{tag}: <div class="ans"> missing')
            continue
        if (q.get("data-asked") or "").strip() and q["data-asked"].strip().lower() != "expected":
            pyq += 1
        if not ans.find(class_="concl"):
            W(f'{tag}: no <div class="concl"> conclusion')
        try:
            m = float(re.findall(r"\d+(?:\.\d+)?", q.get("data-marks", "0"))[-1])
        except IndexError:
            m = 0
        words = len(ans.get_text(" ", strip=True).split())
        if m >= 6 and words < 220:
            W(f"{tag}: only {words} words for {q.get('data-marks')} marks (a 6-mark answer is usually 350+ words)")
        if m >= 5 and not ans.find(["table", "figure"]):
            W(f"{tag}: {q.get('data-marks')} marks but no table or figure")

    # maths sanity
    text = re.sub(r"<(pre|code)\b[\s\S]*?</\1>", "", src)
    text = text.replace("\\$", "")
    for m in re.finditer(r"\$\$([\s\S]+?)\$\$", text):
        if len(m.group(0)) > 170:
            W(f"{p.name}: long display formula ({len(m.group(0))} chars) may overflow the page; split it: {m.group(0)[:70]}...")
    single = re.sub(r"\$\$[\s\S]+?\$\$", "", text)
    for ln, line in enumerate(single.splitlines(), 1):
        if line.count("$") % 2:
            E(f"{p.name}:{ln}: odd number of $ on this line (unclosed maths, or a literal $ that should be written as \\$)")

    for img in soup.find_all("img"):
        src_ = img.get("src", "")
        if not src_.startswith(("data:", "http")) and not (d / src_).exists():
            E(f"{p.name}: figure file not found: {src_}")
    for fc in soup.find_all("figcaption"):
        m = re.match(r"\s*Fig\.\s*([\w.]+)", fc.get_text())
        if not m:
            W(f'{p.name}: figcaption should start with "Fig. <unit>.<n>": {fc.get_text()[:50]}')
        else:
            figs_seen.append(m.group(1))
    for h in soup.find_all(["h4", "h5"]):
        if h.get_text(strip=True).endswith(":"):
            W(f'{p.name}: heading "{h.get_text(strip=True)}" ends with ":" (the stylesheet adds one)')
    for t in soup.find_all("table"):
        if "t" not in (t.get("class") or []):
            W(f'{p.name}: table without class="t" will not get the notes table style')

dups = {f for f in figs_seen if figs_seen.count(f) > 1}
if dups:
    E(f"duplicate figure numbers: {sorted(dups)}")
if qcount == 0:
    E("no questions found")
if not has_rev:
    W('no Rapid Revision Sheet (<div class="part rev"> + <div class="rev">)')

print(f"checked {len(parts)} parts: {qcount} questions ({pyq} PYQ, {qcount - pyq} Expected), {len(figs_seen)} figures")
for w in warns:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
