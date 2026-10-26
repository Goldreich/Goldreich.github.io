# Or Goldreich — Research & Projects

Academic website hosted on GitHub Pages. The five pages, portrait, downloadable CV and interactive Knesset forecast chart are preserved. No server or ChatGPT sign-in is required.

## Edit online

Open a file in GitHub, select the pencil icon, make your changes and commit to `main`. The publishing workflow rebuilds and deploys the website automatically.

- `content.json`: biography, profile links and publications.
- `build.py`: Projects and CV page text and page layouts.
- `public/styles.css`: visual styling.
- `public/assets/or-goldreich.jpg`: homepage photo.
- `public/assets/or-goldreich-cv.pdf`: downloadable CV; replace it by uploading a new PDF through GitHub.

Publication author names use comma separators. Submitted papers omit venues and unavailable manuscripts have no links. The site removes Oxford commas during the HTML build.

The previous custom `/admin` editor requires a server and is not part of this GitHub Pages version. GitHub's browser editor provides online editing and commit history instead.

## Hosting setup

Repository: `Goldreich/Goldreich.github.io`. The website is published at `https://goldreich.github.io` once GitHub Pages is enabled with GitHub Actions as its publishing source. The included `.github/workflows/pages.yml` builds and publishes `public/` on each push to `main`.

## Local build

Run `python3 build.py`, then serve `public/` with any static web server. The HTML build uses only Python's standard library. The optional `build_cv.py` uses ReportLab; install that separately if regenerating the bundled PDF locally.

## Forecast provenance

The Knesset page contains a frozen forecast from 24 October 2026, drawn from commit `00a0988471e51f7d89cc7aeb0e42cfa57b2d3713` of https://github.com/Goldreich/26th-knesset-prediction. It links to the project's live dashboard and source repository.
