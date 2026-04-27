# Arc I S(I).3 — Optic Evidence

**Sprint:** Arc I S(I).3 (sprint-27.3)
**PR:** #328
**Merged:** 2026-04-27
**Merge commit:** e6b5792d83e2d36877f7df57b71452f7e2de280f

## Deliverables confirmed on main

- [x] `godot/tests/auto/sim_single_run.gd` — extends AutoDriver, state-driven dispatcher, random chassis+reward picks, always-accept-loss, JSON stdout output
- [x] `godot/tests/auto/sim_runner.sh` — parallel N-run wrapper, results to /tmp/sim_results_*/
- [x] `.github/workflows/sim.yml` — manual + nightly 3AM UTC (NOT per-PR)

## CI on merge commit: all green

Godot Unit Tests ✅ | Playwright ✅ | Audit Gate ✅ | Optic Verified ✅

## Architecture

State-driven dispatcher (not numbered steps): reads game_flow.current_screen each _drive_flow_step() call. Handles MAIN_MENU→RUN_START→ARENA→REWARD_PICK→RETRY_PROMPT/RUN_COMPLETE terminal states. speed_multiplier re-set each ARENA poll (resets to 1.0 on _start_roguelike_match). sim_* prefix excluded from per-PR test_*.gd glob.

## Pillar 3 status

S(I).3 scaffold complete. S(I).4 (aggregate stats + dashboard) is next.
