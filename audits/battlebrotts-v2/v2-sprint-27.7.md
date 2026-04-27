# S(I).7 Audit — Arc I: bb_test Reward-Pick Playwright Spec

**Sprint:** Arc I S(I).7 (sprint-27.7)
**Arc:** I — Optic Plays The Game
**Pillar:** 2 — Web-export drive (reward-pick spec)
**PR:** #332
**Merged:** 2026-04-27T22:16:58Z
**Merge commit:** 6ec48c2b4f1301c0c5d1d189fcbb3ba78e467ead
**Auditor:** Specc

---

## Deliverables

- `tests/bb-test-reward-pick.spec.js` — WEB_DEBUG_BUILD gated. Drives: run_start→click_chassis(0)→in_arena→force_battle_end(0)→REWARD_PICK(8)→click_reward(0)→in_arena(2). Asserts battles_won>=1, canvas not monochrome. PARTIAL_COVERAGE branches at all timeouts.
- `playwright.config.js` — spec in testMatch.
- `.github/workflows/build-and-deploy.yml` — `grep -q "bb_test" build/index.js` check; exit 1 if found (bridge-leak gate). Positioned after release export, before debug export.

## CI: all green. Playwright skips bb-test spec on PR gate (WEB_DEBUG_BUILD not in verify.yml).

## Design Verification

- REWARD_PICK_TIMEOUT_MS=10000: accounts for 1s Godot create_timer + scene transition ✅
- `force_battle_end(0)`: synchronous bridge call, timer fires in Godot engine time ✅
- Production grep check: `build/index.js` only (debug build intentionally excluded) ✅
- PARTIAL_COVERAGE branches at every polling step ✅
- `consoleErrors.check()` in all branches ✅

## Grade

**A** — Pillar 2 complete (S(I).6 chassis-pick + S(I).7 reward-pick). Production leak gate live.
