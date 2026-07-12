#!/usr/bin/env python3
"""Generate Orbit-embedded review pages from prompts/*.yaml into docs/.

Usage:  python3 scripts/build_orbit_pages.py
Deps:   pip install pyyaml
"""

import html
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
OUT_DIR = ROOT / "docs"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script type="module" src="https://js.withorbit.com/orbit-web-component.js"></script>
<style>
  body {{ font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
         max-width: 720px; margin: 2rem auto; padding: 0 1rem; line-height: 1.55;
         color: #1a1a1a; }}
  h1 {{ font-size: 1.5rem; }}
  .howto {{ background: #f5f5f5; border-radius: 8px; padding: 0.9rem 1.1rem;
            font-size: 0.92rem; }}
  footer {{ margin-top: 2.5rem; font-size: 0.85rem; color: #777; }}
  a {{ color: #0b62a4; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p class="howto">
  <strong>How to use this page:</strong> work through the cards below — try to
  recall the answer <em>before</em> revealing it. If you sign in when prompted,
  Orbit will re-send you these questions by email over the following weeks,
  spacing the repetitions so the ideas stick. Signing in is optional and not
  monitored or graded.
</p>
{reviewarea}
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
<style>
  body {{ font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
         max-width: 720px; margin: 2rem auto; padding: 0 1rem; line-height: 1.55; }}
  a {{ color: #0b62a4; }}
</style>
</head>
<body>
<h1>International Trade — Review pages</h1>
<p>Spaced-repetition review prompts for each lecture.</p>
<ul>
{items}
</ul>
</body>
</html>
"""


def esc(s: str) -> str:
    """Escape a prompt string for use inside an HTML attribute."""
    return html.escape(str(s).strip(), quote=True)


def build_page(spec: dict) -> str:
    lines = [f'<orbit-reviewarea color="{esc(spec.get("color", "blue"))}">']
    for p in spec["prompts"]:
        lines.append(f'  <orbit-prompt\n    question="{esc(p["q"])}"\n    answer="{esc(p["a"])}"\n  ></orbit-prompt>')
    lines.append("</orbit-reviewarea>")
    return PAGE_TEMPLATE.format(title=esc(spec["title"]), reviewarea="\n".join(lines))


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
