# S25.8 Audit — Run-End Screens + First-Run Tooltips
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#307
**Merge commit:** 2c570b73649e135c62a3e076cfa92b767e6f7e48
**Grade:** A

## Summary
S25.8 delivers the full run-end UX: BROTT DOWN loss screen + RUN COMPLETE victory screen both reworked with inline build summaries and GDD-compliant single-button layout (New Run only, no Return to Menu). First-run tooltips updated for roguelike: click-controls tooltip added and fires first on arena entry. All 4 Optic gates pass; 13/13 unit conditions pass.

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. BROTT DOWN shows build summary + fell-at-battle + stats | PASS | em-dash for farthest threat |
| 2. RUN COMPLETE shows boss name + build summary + 15/15 + stats | PASS | em-dash for best kill |
| 3. Both screens: New Run only, no Return to Menu | PASS | GDD §A.5 |
| 4. New Run resets RunState + routes to run-start | PASS | end_run() called from button |
| 5. Both terminal-loss paths → BROTT DOWN | PASS | accept_loss + retry_count=0 converge |
| 6. click_controls tooltip fires first in arena sequence | PASS | ARENA_SEQUENCE[0] = click_controls |
| 7. No BrottBrain/shop/league/card copy in any tooltip | PASS | FE_COPY + ARENA_FE_COPY clean |
| 8. test_run_end_screens.gd passes CI | PASS | 13/13 conditions |

## Deviations / Notes
- 3 S21.x test files moved to SPRINT_TEST_FILES_ARC_G_PENDING (test_s21_2_001_inline_captions, test_s21_4_003_league_surface, test_s21_5_003_sfx_routing) — they asserted on old ResultScreen class which is now BrottDownScreen. Arc G rewrites these.
- S21.2/S21.3 tooltip invariant tests updated with negative assertions for legacy FE keys (confirming S25.8 renames landed).
- _farthest_threat_name and _best_kill_name fields render as em-dash ("—") per S25.8 spec (defer tracking to S25.9 + OpponentLoadouts.get_display_name()).

## Carry-forwards to S25.9
- Populate _farthest_threat_name during combat (archetype display name on encounter entry)
- Populate _best_kill_name after player wins (archetype display name of final kill)
- Add OpponentLoadouts.get_display_name(archetype_id) helper
- Boss AI hand-tuning + integration validation (final Arc F sub-sprint)

## Arc F progress
S25.1–S25.8 ✅ (8/9 sub-sprints) | S25.9 ⏳ (Boss + Arc F integration)
