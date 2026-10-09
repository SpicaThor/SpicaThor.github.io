#!/usr/bin/env python3
"""Writes Generator's support and privacy pages in every language from one template per page and
one text table per language (text/<code>.json), and the language links on the front page.

    python3 tools/generator/build.py

Edit the template or the tables, never the generated pages. A table entry ending in _ios or _android
is used on that platform's page instead of the plain one. Template lines starting with @ios,
@android or @translated appear only on those pages. Text can hold these tokens:
{privacy_href} (this platform's policy), {ios_privacy_href}, {english_href}, {languages}, {hl}.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).parent
SITE = HERE.parents[1]
OUT = SITE / "static-pages/generator"

# Page order in the language menu: English and Russian first, then the rest.
LANGUAGES = ["en", "ru", "uk", "he", "ar", "es", "pt", "fr", "de", "it", "pl", "tr", "id", "hi"]
RIGHT_TO_LEFT = {"he", "ar"}
PAGES = {  # file prefix -> (template, platform)
    "support": ("support.html", "ios"),
    "privacy": ("privacy.html", "ios"),
    "privacy-android": ("privacy.html", "android"),
}

STYLE = (HERE / "style.css").read_text().rstrip("\n")
GLOBE = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8">'
         '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9'
         'c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>')
CHEVRON = ('<svg class="chevron" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
           'stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>')
TABLES = {code: json.loads((HERE / f"text/{code}.json").read_text()) for code in LANGUAGES}


def french(text):
    # No-break spaces before French double punctuation and inside guillemets, as in the apps.
    text = re.sub(r" ([:;!?])", "\u202f\\1", text)
    return text.replace("« ", "«\u00a0").replace(" »", "\u00a0»")


TABLES["fr"] = {key: french(text) for key, text in TABLES["fr"].items()}
REQUIRED = set(TABLES["en"])


def value(table, key, platform):
    for name in (f"{key}_{platform}", key):
        if name in table:
            return table[name]
    raise KeyError(key)


def page(prefix, code):
    template, platform = PAGES[prefix]
    table = TABLES[code]
    privacy = "privacy" if platform == "ios" else "privacy-android"
    # The language menu: a <details> dropdown, so the pages need no script.
    items = "\n".join(
        f'            <li><a href="{prefix}-{c}.html" hreflang="{c}" lang="{c}"'
        + (' aria-current="page"' if c == code else "") + f'>{TABLES[c]["name"]}</a></li>'
        for c in LANGUAGES)
    nav = f"""      <nav class="lang" aria-label="{table['language']}">
        <details>
          <summary>{GLOBE}<span>{table['name']}</span>{CHEVRON}</summary>
          <ul>
{items}
          </ul>
        </details>
      </nav>"""
    alternates = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{prefix}-{c}.html">' for c in LANGUAGES)
    tokens = {
        "privacy_href": f"{privacy}-{code}.html",
        "ios_privacy_href": f"privacy-{code}.html",
        "english_href": f"{prefix}-en.html",
        # Each name isolated, so Hebrew and Arabic names next to each other keep their order.
        "languages": ("، " if code == "ar" else ", ").join(f'<bdi lang="{c}">{TABLES[c]["name"]}</bdi>' for c in LANGUAGES),
        "hl": "" if code == "en" else f"?hl={code}",
        "apple_privacy": table.get("apple_privacy", "https://www.apple.com/legal/privacy/"),
        "privacy_subject": quote(table["privacy_subject"]),
        "support_subject": quote(table["support_subject"]),
    }
    lines = []
    for line in (HERE / template).read_text().splitlines():
        match = re.match(r"@(\w+)(.*)", line)
        if match:
            condition, line = match.groups()
            if condition in ("ios", "android") and condition != platform:
                continue
            if condition == "translated" and code == "en":
                continue
        lines.append(line)
    html = "\n".join(lines) + "\n"
    fixed = {"code": code, "dir": ' dir="rtl"' if code in RIGHT_TO_LEFT else "", "style": STYLE, "nav": nav,
             "alternates": alternates}
    html = re.sub(r"\[\[(\w+)\]\]", lambda m: fixed[m[1]] if m[1] in fixed else value(table, m[1], platform), html)
    return re.sub(r"\{(\w+)\}", lambda m: tokens[m[1]], html)


def check():
    errors = []
    for code, table in TABLES.items():
        missing = REQUIRED - set(table)
        extra = set(table) - REQUIRED - {"apple_privacy"}
        if missing or extra:
            errors.append(f"{code}: missing {sorted(missing)}, extra {sorted(extra)}")
        for key, text in table.items():
            english = TABLES["en"].get(key, "")
            for pattern in (r"<[a-z]+", r"\{\w+\}", r'href="[^"]*"'):
                if sorted(re.findall(pattern, text)) != sorted(re.findall(pattern, english)):
                    errors.append(f"{code}.{key}: {pattern} differs from English")
    if errors:
        sys.exit("\n".join(errors))


def front_page():
    index = SITE / "index.html"
    html = index.read_text()
    for prefix in PAGES:
        links = " · ".join(
            f'<a href="static-pages/generator/{prefix}-{c}.html"'
            + ("" if c == "en" else f' hreflang="{c}" lang="{c}"') + f'>{TABLES[c]["name"]}</a>'
            for c in LANGUAGES)
        html, count = re.subn(rf'(<dd>)<a href="static-pages/generator/{prefix}-en\.html".*?(</dd>)',
                              lambda m: m[1] + links + m[2], html)
        assert count == 1, prefix
    index.write_text(html)


check()
for prefix in PAGES:
    for code in LANGUAGES:
        (OUT / f"{prefix}-{code}.html").write_text(page(prefix, code))
front_page()
print(f"wrote {len(PAGES) * len(LANGUAGES)} pages")
