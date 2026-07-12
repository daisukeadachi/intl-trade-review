# intl-trade-review

Spaced-repetition review pages for **International Trade (HA), Aarhus University**.

Review prompts are maintained as platform-neutral YAML (`prompts/`) and compiled
into embeddable HTML pages (`docs/`). See issue #1 for the design rationale
(prompts as the asset, platforms as replaceable outlets).

## Layout

```
prompts/   lectureN_*.yaml  — Q&A prompts per lecture (the asset; Markdown + $LaTeX$)
scripts/   build_orbit_pages.py — YAML -> docs/*.html generator (Orbit outlet)
docs/      generated review pages (GitHub Pages root)
```

## Build

```sh
pip install pyyaml
python3 scripts/build_orbit_pages.py
```

## Status

- Lecture 2 (Ricardian model): 12 prompts, page generated.
- **The Orbit outlet is currently non-functional upstream**: the TLS certificate
  for `api.withorbit.com` lapsed (~May 2026), so sign-in, progress saving, and
  email reviews fail. See issue #2. The YAML asset is unaffected; an alternative
  outlet (ts-fsrs + localStorage self-hosted component) is planned in issue #1.
