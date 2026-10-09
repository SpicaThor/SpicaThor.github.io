# SpicaThor.github.io

Static pages for my apps (privacy policies, support pages) and the site's `app-ads.txt`, served with
GitHub Pages at https://spicathor.github.io/

Until 2026-09-27 this repo was `static-pages`, a project site at `/static-pages/`. The pages kept their
paths under `static-pages/` because the apps and their App Store listings link to them there: don't move
them (GitHub Pages can't redirect).

| Path | What |
|---|---|
| `index.html` | The site's front page: the apps and links to their pages |
| `app-ads.txt` | Authorized ad sellers for the apps (AdMob). Found through each App Store listing's Marketing URL, whose host is this site |
| `static-pages/generator/support-<lang>.html` | Generator (iOS) support |
| `static-pages/generator/privacy-<lang>.html` | Generator (iOS) privacy policy |
| `static-pages/generator/privacy-android-<lang>.html` | Generator for Android privacy policy (linked from the Android app, AdMob and Google Play) |
| `tools/generator/` | What builds the Generator pages: `build.py`, the templates, `style.css` and `text/<lang>.json` |

`<lang>` is each of Generator's 14 languages: en, ru, uk, he, ar, es, pt, fr, de, it, pl, tr, id, hi. The apps
link to the policy in the language they're shown in, so every language the apps get needs pages here first.

Each page is a single self-contained HTML file with no scripts, external fonts or trackers.

## Generator pages are generated

Don't edit them by hand. Change the template (`tools/generator/support.html`, `privacy.html`, `style.css`) or
the text (`tools/generator/text/<lang>.json`, one table per language, with `_ios` / `_android` variants where
the platforms differ), then run `python3 tools/generator/build.py`. It checks that every table has every key
with the same tags and links as English, writes all pages (each with a script-free language dropdown,
`<details>`) and updates the front page's language links.
English and Russian are the originals; the other 12 were machine-translated (2026-10-09) and say that the
English version prevails. Hebrew and Arabic pages are right to left.
