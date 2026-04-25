# S25.4 Audit — Multi-target AI Priority + 7-Archetype Encounter Data
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#303
**Merge commit:** 02bf4c26af9ffdbab3fae9145f9d148de4d4f883
**Grade:** A

## Summary
S25.4 extends the S25.3 baseline AI to multi-target priority selection (melee-adjacent > equidistant-lowest-HP > nearest) and authors the full 7-archetype encounter data pool in opponent_loadouts.gd. combat_sim gains an enemies context population pass + guard preventing brain-chosen targets from being clobbered. All 5 Optic gates pass; combat_batch win-rates unchanged from S25.3 baseline (expected: multi-target logic inert in 1v1 simulation).

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. Nearest in 1v3 | ✅ PASS | cascade confirmed |
| 2. Equidistant picks lower-HP | ✅ PASS | 1px epsilon tie-break |
| 3. Melee-range priority | ✅ PASS | 48px threshold, 2 test variants |
| 4. Click-override beats melee | ✅ PASS | _override_target_id short-circuit unchanged |
| 5. Counter-Build selector | ✅ PASS | modules≥3 first, then weapon type |
| 6. 7 archetype records | ✅ PASS | all IDs locked and present |
| 7. test_multi_target_ai.gd | ✅ PASS | 10/10 conditions |
| 8. combat_batch ±15% regression | ✅ PASS | Scout 54.0%, Brawler 44.2%, Fortress 49.8% |

## Deviations / Notes
- T3 split into T3a + T3b for stronger coverage → 10 conditions (spec: 9). No issue.
- T4 click-override tests movement_override == "target_override" (correct brain-layer contract).
- combat_batch unchanged because multi-target paths are inert in 1v1 batch. Forward-compat gate only.

## Carry-forwards to S25.5
- S25.5 builds reward pick screen + run flow; needs RunState.equipped_* mutation methods
- S25.6 completes archetype_for() rotation + anti-repeat + run guarantees
- Boss loadout placeholder; S25.9 tunes IRONCLAD PRIME AI behavior

## Arc F progress
S25.1 ✅ | S25.2 ✅ | S25.3 ✅ | S25.4 ✅ | S25.5 ⏳ | S25.6–S25.9 📋
