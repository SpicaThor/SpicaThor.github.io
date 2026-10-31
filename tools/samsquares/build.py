#!/usr/bin/env python3
"""Writes Samsquares' support and privacy pages (English only) from one template per page and the
text table text/en.json, and checks the front page links to them.

    python3 tools/samsquares/build.py

Edit the templates or the table, never the generated pages. A simpler copy of tools/horoscope/build.py
(one language, so no language menu). [[key]] is replaced by the table entry; {privacy_subject} and
{support_subject} by the URL-encoded mail subjects.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).parent
SITE = HERE.parents[1]
OUT = SITE / "static-pages/samsquares"
PAGES = ["support", "privacy"]

STYLE = (HERE / "style.css").read_text().rstrip("\n")
TABLE = json.loads((HERE / "text/en.json").read_text())


def page(name):
    html = (HERE / f"{name}.html").read_text()
    missing = sorted(set(re.findall(r"\[\[(\w+)\]\]", html)) - set(TABLE) - {"style"})
    if missing:
        sys.exit(f"{name}.html: no text for {missing}")
    html = re.sub(r"\[\[(\w+)\]\]", lambda m: STYLE if m[1] == "style" else TABLE[m[1]], html)
    tokens = {"privacy_subject": quote(TABLE["privacy_subject"]), "support_subject": quote(TABLE["support_subject"])}
    return re.sub(r"\{(privacy_subject|support_subject)\}", lambda m: tokens[m[1]], html)


OUT.mkdir(parents=True, exist_ok=True)
for name in PAGES:
    (OUT / f"{name}-en.html").write_text(page(name))

index = (SITE / "index.html").read_text()
for name in PAGES:
    if f'href="static-pages/samsquares/{name}-en.html"' not in index:
        sys.exit(f"index.html has no link to static-pages/samsquares/{name}-en.html")
print(f"wrote {len(PAGES)} pages")
