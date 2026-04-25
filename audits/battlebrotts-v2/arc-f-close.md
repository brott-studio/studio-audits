# Arc F Close Record — Roguelike Core Loop
**Arc:** Arc F
**Date closed:** 2026-04-25
**Final PR:** brott-studio/battlebrotts-v2#308 (76df3510bb25a7babfcb588248d3eff681d94b42)
**Exit verification:** docs/arc-f-exit-verification.md
**Grade:** A (all 9 sub-sprints Grade A)

## Arc F delivered
- Complete 15-battle roguelike run loop (S25.1-S25.7)
- Run-end screens BROTT DOWN + RUN COMPLETE (S25.8)
- 7 encounter archetypes + full encounter generator (S25.4-S25.6)
- Click-to-move + click-to-target with multi-target arena (S25.2)
- Hardcoded baseline AI + multi-target priority (S25.3-S25.4)
- Reward pick, retry mechanic, run HUD, Continue Run (S25.5-S25.7)
- IRONCLAD PRIME boss AI + tier tinting + integration validation (S25.9)

## PRs merged (9 total)
#300 S25.1 | #301 S25.2 | #302 S25.3 | #303 S25.4 | #304 S25.5
#305 S25.6 | #306 S25.7 | #307 S25.8 | #308 S25.9

## Carry-forwards to Arc G
- _farthest_threat_name/_best_kill_name tracking
- BuildSummaryComponent extraction
- League-era dead code deletion (brottbrain_screen, shop, opponent_select)
- Arc-G-pending test rewrites (6 files)

## Hand-off
Arc G (Cut Pass) receives fully playable 15-battle roguelike run.
