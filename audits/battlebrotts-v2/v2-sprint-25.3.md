# S25.3 Audit — Hardcoded Baseline AI (single-target)
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#302
**Merge commit:** b9910b970679cfeab90ca550af870a80d109beff
**Grade:** A

## Summary
S25.3 replaces the card-driven BrottBrain with a hardcoded rule chain (advance/kite-hysteresis/module-autofire) while preserving public API and save-compat. combat_sim gains move_to_override and target_override consumers completing the click-control integration from S25.2. All 6 Optic gates pass; combat_batch 600-match clean run establishes the S25.3 win-rate baseline.

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. Advance/engage | ✅ PASS | empty movement_override, stance=default |
| 2. Kite hysteresis | ✅ PASS | drop ≤30%, recover ≥40% |
| 3. Repair Nanites auto-fire | ✅ PASS | HP<40% |
| 4. EMP Charge auto-fire | ✅ PASS | enemy has active module |
| 5. Afterburner auto-fire | ✅ PASS | while kiting |
| 6. Public API unchanged | ✅ PASS | all 5 properties/methods present |
| 7. move_to_override consumer | ✅ PASS | 24px arrive+clear |
| 8. target_override consumer | ✅ PASS | sets b.target, death-side cleanup |
| 9. combat_batch clean run | ✅ PASS | 600 matches, no crash/NaN |
| 10. test_baseline_ai.gd | ✅ PASS | 9/9 conditions |

## Deviations / Notes
- EMP module name corrected to "EMP Charge" on implementation.
- test_sprint14_2_cards.gd moved to SPRINT_TEST_FILES_ARC_G_PENDING.
- test_sprint4.gd: 7 card-count assertions retired in-place with CUT markers.
- Overtime suppresses kite (combat_sim forces stance=0) — intentional per design.

## Canonical S25.3 win-rate baseline (combat_batch 600 matches)
- Scout: 54.0%
- Brawler: 44.2%
- Fortress: 49.8%
Future sprints regress against ±15% band.

## Carry-forwards to S25.4
- Extend evaluate() to multi-target (enemies: Array[BrottState])
- Add target-prioritization: nearest, lowest-HP, melee-range attacker
- S25.4 regression: compare combat_batch win-rates against S25.3 baseline above

## Arc F progress
S25.1 ✅ | S25.2 ✅ | S25.3 ✅ | S25.4 ⏳ | S25.5–S25.9 📋
