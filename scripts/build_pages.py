#!/usr/bin/env python3
"""Generate self-hosted spaced-repetition review pages from prompts/*.yaml.

Outlet: own web component (docs/assets/review.js, FSRS via vendored ts-fsrs,
progress in the student's localStorage). No server, no accounts.

Prompt schema (v1, see issues #1 and #3):
  lecture: lecture number
  title:   lecture title shown on the review page
  color:   accent color (kept for the Orbit outlet; unused here)
  prompts: list of either
    {q, a [, type]}                    - a fixed card
    {skill, variants: [{q, a}, ...] [, type]}
                                       - one FSRS card per *skill*; a random
                                         variant is shown at each review
  Markdown and $...$ / $$...$$ LaTeX are supported in q/a.

Besides one page per lecture, a pooled page (docs/all.html) is generated that
reviews everything due across all lectures. Card scheduling state is shared
with the per-lecture pages (same localStorage ids).

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
<p class="pooled-link"><a href="all.html"><strong>Review everything due</strong></a>
&mdash; one session pooling the due cards from every lecture. Use this as the
course progresses (and before the exam); the per-lecture pages below are for
first-time review of a single lecture.</p>
<p>A session takes about <strong>five minutes</strong>: at most 12 cards per
visit, hardest-to-remember first, with a few new cards mixed in. Anything left
over stays scheduled for next time (you can always keep going if you want).</p>
<ul>
{items}
</ul>
</body>
</html>
"""


def normalize_prompts(spec: dict, fname: str) -> list:
    """Validate and normalize a lecture's prompt list (schema v1)."""
    out = []
    for i, p in enumerate(spec["prompts"]):
        where = f"{fname} prompt {i}"
        if "variants" in p:
            if "skill" not in p or not p["variants"]:
                raise ValueError(f"{where}: variants require a non-empty 'skill'")
            for j, v in enumerate(p["variants"]):
                if "q" not in v or "a" not in v:
                    raise ValueError(f"{where} variant {j}: needs both 'q' and 'a'")
            entry = {"skill": p["skill"],
                     "variants": [{"q": v["q"], "a": v["a"]} for v in p["variants"]]}
        elif "q" in p and "a" in p:
            entry = {"q": p["q"], "a": p["a"]}
        else:
            raise ValueError(f"{where}: needs either q/a or skill/variants")
        if "type" in p:
            entry["type"] = p["type"]
        out.append(entry)
    return out


def render_page(title: str, deck: dict) -> str:
    # </script> inside JSON would terminate the data block early.
    deck_json = json.dumps(deck, ensure_ascii=False).replace("</", "<\\/")
    return PAGE_TEMPLATE.format(
        title=html.escape(title), deck_json=deck_json, katex=KATEX_VER
    )


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    entries = []
    lectures = []
    for f in sorted(PROMPTS_DIR.glob("*.yaml")):
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        prompts = normalize_prompts(spec, f.name)
        out_name = f"lecture{spec['lecture']}.html"
        deck = {"lecture": spec["lecture"], "prompts": prompts}
        (OUT_DIR / out_name).write_text(
            render_page(spec["title"], deck), encoding="utf-8"
        )
        entries.append((spec["lecture"], spec["title"], out_name, len(prompts)))
        lectures.append(deck)
        print(f"{f.name} -> docs/{out_name} ({len(prompts)} prompts)")

    # Pooled cross-lecture page: same card ids as the per-lecture pages, so
    # scheduling state is shared through localStorage (issue #3, extension 4).
    pooled = {"pooled": True, "lectures": lectures}
    (OUT_DIR / "all.html").write_text(
        render_page("Review everything due — all lectures", pooled),
        encoding="utf-8",
    )
    n_all = sum(len(d["prompts"]) for d in lectures)
    print(f"docs/all.html ({n_all} prompts across {len(lectures)} lectures)")

    items = "\n".join(
        f'  <li><a href="{name}">{html.escape(title)}</a> ({n} prompts)</li>'
        for _, title, name, n in sorted(entries)
    )
    (OUT_DIR / "index.html").write_text(INDEX_TEMPLATE.format(items=items), encoding="utf-8")
    print(f"docs/index.html ({len(entries)} lectures)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
