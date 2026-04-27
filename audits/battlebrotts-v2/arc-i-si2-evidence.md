# Arc I S(I).2 — Optic Evidence

**Sprint:** Arc I S(I).2 (sprint-27.2)
**PR:** #327
**Merged:** 2026-04-27T20:37:09Z
**Merge commit:** 274d9a5dacd42861fd97b04bf26644050b7b69f5

## Deliverables confirmed on main

- [x] `godot/tests/auto/test_reward_pick_flow.gd` — battle win → reward pick → next battle
- [x] `godot/tests/auto/test_run_end_flow.gd` — battle loss → retry prompt → brott down → new run
- [x] `godot/tests/auto/test_settings_flow.gd` — boot → main menu → settings open/close
- [x] `godot/tests/auto/auto_driver.gd` — `_find_child_of_type` fixed for GDScript class_name
- [x] `godot/tests/test_runner.gd` — all 4 auto/ tests registered in SPRINT_TEST_FILES

## CI status on merge commit

All required checks green: Godot Unit Tests ✅ | Playwright Smoke Tests ✅ | Audit Gate ✅ | Optic Verified ✅

## Architecture notes

`_find_child_of_type` now checks both `get_class()` (engine base class) and `get_script().get_global_name()` (GDScript declared class_name). This is the correct Godot 4 pattern for finding nodes by script class name in headless tests.

## Pillar 1 coverage status

All four arc-brief-mandated user flows now covered:
1. ✅ chassis-pick (S(I).1)
2. ✅ reward-pick (S(I).2)
3. ✅ run-end/death (S(I).2)
4. ✅ settings (S(I).2)

Pillar 1 complete. Per-PR gate live for all four flows.
