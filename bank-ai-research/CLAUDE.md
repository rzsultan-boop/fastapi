# CLAUDE.md — Bank AI-Adoption / LinkedIn Project

This project is **business-development research**, not software. Goal: help a startup engage Israeli
banks on **AI adoption** — (a) map the right people to talk to, and (b) build a concrete **commercial
loan-origination use case** at Bank Leumi (departments, process, systems) for demos/intros.

**It has nothing to do with FastAPI** — it lived in a `fastapi` repo only because that was the cloud
container's checkout. It belongs in the user's local **LinkedIn project** folder.

## Read first
- `SESSION-HANDOFF.md` — full memory of the prior session: what was done, all findings, open items,
  how the research was run, and the user's working preferences. **Start here.**
- `SUMMARY.md` — consolidated findings (people · departments · loan process · systems).
- `LEUMI-loan-origination-usecase.md` — deep detail + §5b systems table.
- `loan-flow.png/.svg` + `make_flow.py` — the flow diagram (regenerate: `python3 make_flow.py` then
  screenshot the HTML with headless Chromium).
- `RESEARCH-CHECKPOINT.md` — provenance + workflow run IDs.

## User's working preferences (honor these)
- **Systems > personnel names** — getting the systems right matters most (that's the wedge).
- **Little fluff** — readability over decoration; honest `[CONFIRMED]` vs `[TEMPLATE]` vs `[NOT FOUND]` tags.
- **Search Hebrew-first**, cross-check English/LinkedIn.
- **Save frequently** — commit + push after each meaningful step (the env was ephemeral).
- Diagrams: colorblind-safe (Okabe-Ito), redundant encoding (glyph + line-style + label, not hue alone).
