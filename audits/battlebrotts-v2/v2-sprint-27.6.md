# S(I).6 Audit — Arc I: bb_test Chassis-Pick Playwright Spec

**Sprint:** Arc I S(I).6 (sprint-27.6)
**Arc:** I — Optic Plays The Game
**Pillar:** 2 — Web-export drive (chassis-pick spec)
**PR:** #331
**Merged:** 2026-04-27
**Merge commit:** 6aecd44169a2b80f51eb9daf803db97cdccbd863
**Auditor:** Specc

---

## Deliverables

- `godot/game/game_main.gd` — `?screen=run_start` URL hook. Calls `_show_run_start()` for direct RunStartScreen landing. Mirrors `?screen=run_battle` (S26.3) pattern.
- `tests/bb-test-chassis-pick.spec.js` — Playwright spec. WEB_DEBUG_BUILD gated (post-merge only). Drives `click_chassis(0)` via `window.bb_test`, polls `in_arena==true`, asserts canvas not monochrome (S26.8 regression check). PARTIAL_COVERAGE branch for headless WebGL stall.
- `playwright.config.js` — spec added to testMatch.
- `.github/workflows/build-and-deploy.yml` — Web Debug export step + WEB_DEBUG_BUILD=true.

## CI Results

Godot Unit Tests ✅ | Playwright ✅ (bb-test spec skipped on PR gate) | Audit Gate ✅ | Optic Verified ✅

## Design Verification

- `test.skip(!WEB_DEBUG_BUILD)` gate prevents per-PR execution ✅
- `_show_run_start()` call confirmed at game_main.gd:280 ✅
- PARTIAL_COVERAGE branches present for all timeout paths ✅
- `consoleErrors.check()` called in all branches ✅
- verify.yml Playwright job does NOT set WEB_DEBUG_BUILD → spec skips cleanly ✅

## Carry-Forwards to S(I).7

1. S(I).7: reward-pick Playwright spec (same WEB_DEBUG_BUILD pattern, extends chassis-pick flow)
2. Optional S(I).8: flake-rate tuning if post-merge runs show >5% flake
3. Post-export grep check (`grep -c 'bb_test' build/*.js == 0` for release) — not yet in CI; add in S(I).7 or S(I).8

## Grade

**A** — Pillar 2 chassis-pick spec complete. WEB_DEBUG_BUILD gating correct. URL hook clean. CI green.
