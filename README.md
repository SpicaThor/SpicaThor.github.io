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
| `static-pages/generator/support-en.html`, `support-ru.html` | Generator (iOS) support, English and Russian |
| `static-pages/generator/privacy-en.html`, `privacy-ru.html` | Generator (iOS) privacy policy, English and Russian |
| `static-pages/generator/privacy-android-en.html`, `privacy-android-ru.html` | Generator for Android privacy policy, English and Russian (linked from the Android app, AdMob and Google Play) |

Each page is a single self-contained HTML file with no scripts, external fonts or trackers.
