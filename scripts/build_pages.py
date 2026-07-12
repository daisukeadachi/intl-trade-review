#!/usr/bin/env python3
"""Generate self-hosted spaced-repetition review pages from prompts/*.yaml.

Outlet: own web component (docs/assets/review.js, FSRS via vendored ts-fsrs,
progress in the student's localStorage). No server, no accounts.

Usage:  python3 scripts/build_pages.py
Deps:   pip install pyyaml
"""

import html
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
OUT_DIR = ROOT / "docs"

KATEX_VER = "0.16.11"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@{katex}/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@{katex}/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@{katex}/dist/contrib/auto-render.min.js"></script>
<link rel="stylesheet" href="assets/review.css">
</head>
<body>
<h1>{title}</h1>
<p class="howto">
  <strong>How to use this page:</strong> try to recall each answer
  <em>before</em> revealing it, then grade yourself honestly. Your progress is
  saved in this browser only (nothing is uploaded, monitored, or graded), and
  the page schedules each card&rsquo;s return with spaced repetition &mdash;
  revisit every few days and the cards you struggle with will come back sooner.
</p>
<div id="review-root"></div>
<script type="application/json" id="deck-data">{deck_json}</script>
<script type="module" src="assets/review.js"></script>
<footer>International Trade &middot; Aarhus University &middot;
<a href="index.html">All review pages</a></footer>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>International Trade — Review pages</title>
<link rel="stylesheet" href="assets/review.css">
</head>
<body>
<h1>International Trade — Review pages</h1>
<p>Spaced-repetition review prompts for each lecture. Your progress is saved
in your own browser; nothing is uploaded or graded.</p>
<ul>
{items}
</ul>
</body>
</html>
"""


def build_page(spec: dict) -> str:
    deck = {
        "lecture": spec["lecture"],
        "prompts": [{"q": p["q"], "a": p["a"]} for p in spec["prompts"]],
    }
    # </script> inside JSON would terminate the data block early.
    deck_json = json.dumps(deck, ensure_ascii=False).replace("</", "<\\/")
    return PAGE_TEMPLATE.format(
        title=html.escape(spec["title"]), deck_json=deck_json, katex=KATEX_VER
    )


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    entries = []
    for f in sorted(PROMPTS_DIR.glob("*.yaml")):
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        out_name = f"lecture{spec['lecture']}.html"
        (OUT_DIR / out_name).write_text(build_page(spec), encoding="utf-8")
        entries.append((spec["lecture"], spec["title"], out_name, len(spec["prompts"])))
        print(f"{f.name} -> docs/{out_name} ({len(spec['prompts'])} prompts)")
    items = "\n".join(
        f'  <li><a href="{name}">{html.escape(title)}</a> ({n} prompts)</li>'
        for _, title, name, n in sorted(entries)
    )
    (OUT_DIR / "index.html").write_text(INDEX_TEMPLATE.format(items=items), encoding="utf-8")
    print(f"docs/index.html ({len(entries)} lectures)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
