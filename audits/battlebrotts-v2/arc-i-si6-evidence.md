# Arc I S(I).6 — Optic Evidence

**Sprint:** Arc I S(I).6 (sprint-27.6)
**PR:** #331
**Merged:** 2026-04-27
**Merge commit:** 6aecd44169a2b80f51eb9daf803db97cdccbd863

## Deliverables

- [x] `godot/game/game_main.gd` — `?screen=run_start` URL hook added
- [x] `tests/bb-test-chassis-pick.spec.js` — Playwright spec, WEB_DEBUG_BUILD gated
- [x] `playwright.config.js` — spec in testMatch
- [x] `.github/workflows/build-and-deploy.yml` — Web Debug export + WEB_DEBUG_BUILD=true

## CI: all green (Playwright skips bb-test spec on PR gate — WEB_DEBUG_BUILD not set in verify.yml)

## Architecture

WEB_DEBUG_BUILD=true set only in build-and-deploy.yml (post-merge). Per-PR gate correctly skips spec. PARTIAL_COVERAGE branch handles headless WebGL stalls.
