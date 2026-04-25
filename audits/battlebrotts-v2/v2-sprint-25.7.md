# S25.7 Audit — Battle-to-Battle Loop + HUD
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#306
**Merge commit:** 004295d8d0707d2b6f3a9d3ddb3b89eccbef3072
**Grade:** A

## PLAYTEST-READY: Full 15-battle run is playable end-to-end from this build.

## Summary
S25.7 wires the complete battle-to-battle loop: N-enemy spawning via compose_encounter() (bronze-0 stub gone), battle-15 boss path, RUN_COMPLETE victory screen, Continue Run in-session resume, HUD color escalation. All 5 Optic gates pass; 8/8 unit conditions pass.

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. Win -> reward -> N+1 with correct encounter | PASS | compose_encounter wired |
| 2. Loss (retries remain) -> retry, same archetype | PASS | |
| 3. Loss (retries=0) -> run-end fires | PASS | run_ended flag |
| 4. Run progress bar on reward pick | PASS | HUD bar + battle counter |
| 5. HUD visibility per matrix | PASS | BOSS_ARENA/RUN_COMPLETE gating |
| 6. Color shift: amber >=12, red at 14 | PASS | _color_for_battle() |
| 7. Battle 15 -> boss arena -> RUN_COMPLETE | PASS | battle_index >=14 routing |
| 8. test_run_loop.gd | PASS | 8/8 conditions |

## Deviations
- run_start_screen HUD gate skipped: battle_index always 0 at run-start — dead code, correctly omitted.
- return_to_menu_pressed signal name (vs spec return_to_menu) — functionally identical.
- has_active_run() uses current_battle_index (actual field).

## Playtest-ready: what a player can do
- Menu -> chassis pick -> 15 battles (S25.6 encounter engine, all 7 archetypes)
- HUD: white (1-11) -> amber (12-13) -> red (14) -> gold (15 boss)
- Battle 15 boss -> RUN_COMPLETE screen with summary -> return to menu
- Continue Run resumes correctly after mid-session quit
- Defeat (retry x3 then run-end) cleans up correctly

## Carry-forwards to S25.8
- S25.8 re-skins RunCompleteScreen + BROTT DOWN screen with full stat layout
- S25.8 updates first-run tooltips (two-click affordances, no BrottBrain copy)

## Arc F progress
S25.1 thru S25.7 complete (7/9) | S25.8 pending | S25.9 planned
