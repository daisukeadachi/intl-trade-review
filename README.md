# intl-trade-review

Spaced-repetition review pages for **International Trade (HA), Aarhus University**.

Review prompts are maintained as platform-neutral YAML (`prompts/`) and compiled
into embeddable HTML pages (`docs/`). See issue #1 for the design rationale
(prompts as the asset, platforms as replaceable outlets).

## Layout

```
prompts/   lectureN_*.yaml — Q&A prompts per lecture (the asset; Markdown + $LaTeX$)
scripts/   build_pages.py — YAML -> docs/*.html (self-hosted outlet, current)
           build_orbit_pages.py — Orbit outlet (kept in case upstream revives; issue #2)
docs/      generated review pages (GitHub Pages root)
  assets/  review.js (FSRS scheduling + localStorage), review.css
  assets/vendor/ts-fsrs.mjs — vendored ts-fsrs 5.4.1 (no runtime deps)
```

## Build

```sh
pip install pyyaml
python3 scripts/build_pages.py
```

## How the self-hosted outlet works

- Each review page embeds its prompts as JSON; `assets/review.js` runs the
  review session: recall -> reveal -> self-grade (Again/Hard/Good/Easy).
- Scheduling uses the FSRS algorithm (same family as modern Anki) via the
  vendored `ts-fsrs`; each card's state lives in the student's own
  `localStorage`. No server, no accounts, nothing leaves the device.
- Cards graded *Again* return within the session; when nothing is due the page
  shows the next due date (students are nudged to revisit via scheduled LMS
  announcements).
- Debug helpers: `?autotest` (self-check), `?card=N` (jump to prompt N),
  `&reveal` (auto-reveal).
- KaTeX is loaded from jsdelivr (pinned 0.16.11); vendor it too if CDN
  independence is wanted.

## Status

- Lecture 2 (Ricardian model): 12 prompts, page generated and verified.
- The Orbit outlet is non-functional upstream (`api.withorbit.com` TLS cert
  lapsed ~May 2026, see issue #2); the self-hosted outlet above replaces it.
