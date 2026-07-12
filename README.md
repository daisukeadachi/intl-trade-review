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
           extract_pptx.py — slide text extraction, for drafting prompts
docs/      generated review pages (GitHub Pages root)
  all.html — pooled "review everything due" session across all lectures
  assets/  review.js (FSRS scheduling + localStorage), review.css
  assets/vendor/ts-fsrs.mjs — vendored ts-fsrs 5.4.1 (no runtime deps)
```

## Prompt schema (v1)

A prompt is either a fixed card or a variant card (issue #3, extension 2):

```yaml
prompts:
  - q: "Define *comparative advantage*."          # fixed card
    a: "..."
  - type: calculation                              # variant card: one FSRS
    skill: "Determine comparative advantage from MPLs"   # card per skill,
    variants:                                      # random variant per review
      - {q: "...", a: "..."}
      - {q: "...", a: "..."}
```

Variant cards schedule by *skill* (the FSRS state is shared by all variants),
so each return of the card shows a fresh set of numbers — students practice
the procedure instead of memorizing one answer. `type` is optional metadata
(definition / notation / why / calculation / discrimination).

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
- `docs/all.html` pools the due cards of every lecture into one session
  (issue #3, extension 4). Card ids are identical across pages, so progress
  made on a lecture page counts on the pooled page and vice versa.
- Debug helpers: `?autotest` (self-check), `?card=N` (jump to prompt N),
  `&reveal` (auto-reveal).
- KaTeX is loaded from jsdelivr (pinned 0.16.11); vendor it too if CDN
  independence is wanted.

## Status

- Lecture 2 (Ricardian model): 12 prompts (2 of them variant cards with 3
  variants each), page generated and verified.
- Pooled review page (`all.html`) generated and verified; linked from the index.
- The Orbit outlet is non-functional upstream (`api.withorbit.com` TLS cert
  lapsed ~May 2026, see issue #2); the self-hosted outlet above replaces it.
