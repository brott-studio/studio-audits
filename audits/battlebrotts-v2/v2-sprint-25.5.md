# S25.5 Audit — Reward Pick Screen + Run Flow
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#304
**Merge commit:** 547d4724d9199f5137819c784831c09c3956b100
**Grade:** A

## Summary
S25.5 builds the post-battle reward pick screen, retry prompt, run HUD bar, and wires the complete win->reward->next-battle / loss->retry-or-end flow. The game is now playable as a run: pick a chassis, fight battles, collect rewards, use retries. All 5 Optic gates pass; 6/6 unit conditions pass.

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. Post-win reward pick shows 3 deduped items | PASS | dedup via equipped_* check |
| 2. Pick updates RunState + HUD reflects | PASS | run_state_changed signal propagates |
| 3. Post-loss retry prompt, Retry Battle resets arena | PASS | post-decrement seed formula |
| 4. After retry win, reward pick appears | PASS | flow wired |
| 5. Retry counter decrements, Accept Loss only at 0 | PASS | use_retry() guard |
| 6. HUD amber at battle 12, red at battle 14 | PASS | idx >= 11/13 thresholds |
| 7. Full 16-item pool from battle 1 | PASS | FULL_ITEM_POOL confirmed 16 entries |
| 8. test_reward_pick.gd passes CI | PASS | 6/6 conditions |

## Deviations / Notes
- One Boltz iteration: result_screen.gd missing DEPRECATED header; Riv applied fix (58c8882), re-reviewed cleanly.
- advance_battle() in GameFlow delegates to advance_battle_index() so run_state_changed fires and battles_won increments.
- .uid files for 3 prior-sprint test files included (missing from prior commits, belong with .gd files).

## Carry-forwards to S25.6
- archetype_for() stub returns "standard_duel" always; S25.6 builds full encounter generator
- _advance_to_next_battle() uses stub archetype; S25.6 replaces with generator output
- Duplicate fallback (eligible pool < 3) is defensive; unreachable in 15-battle run

## Arc F progress
S25.1 | S25.2 | S25.3 | S25.4 | S25.5 - all complete | S25.6 pending | S25.7-S25.9 planned
