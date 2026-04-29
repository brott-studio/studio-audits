# v2-sprint-28.7 — Arc K.2: Combat Sim Timer Sweep

**Date:** 2026-04-29
**Sprint:** 28.7
**Arc:** K.2 — Headless sim timer race + ARENA screen state fix
**Status:** ✅ CLOSED
**PRs:** #340 (K.2 timer sweep), #341 (K.2b ARENA screen state fix)
**Issue:** #314

---

## Summary

Arc K.2 diagnosed and fixed the root cause of the 8/20 parse errors in the combat sim, which had persisted through K.1.

### Diagnosis vs Hypothesis

**Original hypothesis (K.2 scope):** K.1 only patched 1 of 3 `create_timer` call sites. Sites 2 (`_on_match_end` line 816) and 3 (`_on_brott_death` line 1244) were unpatched. Additionally, K.1's headless path had no `else`-branch (no `await` at all), potentially breaking the frame boundary `_show_reward_pick` depends on.

**Actual root cause (discovered during K.2):** `_start_roguelike_match()` only set `current_screen = ARENA` when called from `RUN_START` (battle 0). Battles 2+ are entered from `REWARD_PICK` or `RETRY_PROMPT` — neither path updated `current_screen` to `ARENA`. AutoDriver then saw `SCREEN_REWARD_PICK` while battle 1 was running, found 0 reward buttons (old screen queue_freed), and failed after 5 retries.

The `create_timer` patches (K.1, K.2) were correct improvements for a different issue vector (wall-clock timer races in headless), but the 8/20 parse errors were caused entirely by the screen-state bug.

### Fixes Landed

**PR #340 — K.2 timer sweep:**
- Added `else: await get_tree().process_frame` to all 3 `create_timer` call sites in `game_main.gd`
- Ensures 1-frame settle time in headless, no wall-clock race

**PR #341 — K.2b ARENA screen state fix (root cause):**
- Changed `if current_screen == RUN_START: current_screen = ARENA` to unconditional
- Carve-out: `BOSS_ARENA` preserved (set by `_show_boss_arena()` before calling `_start_roguelike_match`)

### Sim Results

**Post-merge sim run #25126311384 (2026-04-29T18:21):**

| Chassis | Run Win % | Battle Win % | Median Battles Won |
|---|---|---|---|
| BRAWLER | 0.0% | 25.0% | 0.0 |
| FORTRESS | 0.0% | 45.5% | 1.0 |
| SCOUT | 0.0% | 68.8% | 2.0 |
| **ALL** | 0.0% | 48.7% | 1.0 |

- **Parse errors: 0/20 ✅** (was 8-9/20)
- Schema skips: 0, Missing fields: 0
- CI Verify: ✅ (Godot Unit Tests + AutoDriver headless flow tests pass)
- Playwright Smoke Tests: ✅

### Remaining Work on #314

The ≥30% run win-rate gate for #314 is not met (0% all chassis). This is a **balance issue** (T1 encounters are too hard for fresh chassis with no items/armor) — separate from the parse error bug. #314 remains open pending T1 balance work.

---

## DoD Gate Status

| Gate | Status |
|---|---|
| 0/20 parse errors | ✅ |
| AutoDriver 4 flows green | ✅ |
| Scout/Brawler/Fortress ≥30% WR | ❌ (balance, separate arc) |
| #314 closes | ❌ (blocked on balance, not parse errors) |

**Arc K.2 scope (parse errors + CI):** ✅ Complete
**Carry-forward:** T1 balance arc (run win-rate improvement for Brawler particularly)
