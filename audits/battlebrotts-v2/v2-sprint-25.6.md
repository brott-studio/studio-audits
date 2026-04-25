# S25.6 Audit — Encounter Generator + Distribution
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#305
**Merge commit:** e39ac1e749d4ad8c6dbd27ed876896f2f8ac8ca6
**Grade:** A

## Summary
S25.6 replaces the standard_duel stub with a full encounter generator: pre-rolled 15-slot run schedule with probability-weighted draws, no-repeat rule, guarantee seeds (small_swarm/counter_build_elite/miniboss_escorts ≥1 per run), boss-lock at battle 15, and large_swarm tier-adaptive HP. 1000-run simulation passes with 0 no-repeat violations and guarantee budget well under 1% failure rate.

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. No consecutive repeat (1000 runs) | PASS | 0 violations |
| 2. Run guarantee (small_swarm/counter_build_elite/miniboss_escorts) | PASS | Under 10/1000 failure budget |
| 3. Battle 15 always boss | PASS | 100/100 seeds |
| 4. difficulty_for_battle() tier mapping | PASS | Exact [1,1,1,2,2,2,2,3,3,3,3,4,4,4,5] |
| 5. compose_encounter() HP correct by tier | PASS | |
| 6. Large Swarm tier-adaptive HP | PASS | {1:0.2, 2:0.4, 3:0.7, 4:0.9} |
| 7. Counter-Build Elite selector | PASS | Covered by S25.4 |
| 8. test_encounter_generator.gd | PASS | 5/5 conditions headless |

## Deviations / Notes
- difficulty_for_battle() rename correct — GDScript overload conflict with legacy difficulty_for(league, index).
- T2 excludes miniboss_escorts from weighted draw; appears via slot-5 guarantee only. Intentional.
- encounter_schedule cached on run_state, reset on new run.

## Carry-forwards to S25.7
- S25.7 wires full battle-to-battle loop; archetype_for() output feeds into actual N-bot spawning via compose_encounter()
- Boss at battle 15 is still a stub encounter; S25.9 tunes boss AI

## Arc F progress
S25.1 thru S25.6 all complete | S25.7 pending | S25.8-S25.9 planned
