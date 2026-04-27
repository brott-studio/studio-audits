# S(I).2 Audit — Arc I: AutoDriver Flow Coverage + _find_child_of_type Fix

**Sprint:** Arc I S(I).2 (sprint-27.2)
**Arc:** I — Optic Plays The Game
**Pillar:** 1 — Native GDScript auto-driver (COMPLETE)
**PR:** #327
**Merged:** 2026-04-27T20:37:09Z
**Merge commit:** 274d9a5dacd42861fd97b04bf26644050b7b69f5
**Auditor:** Specc

---

## Deliverables

**Files created:**
- `godot/tests/auto/test_reward_pick_flow.gd` — battle win → reward pick → next battle (~5.4s, 325 ticks @ 60fps)
- `godot/tests/auto/test_run_end_flow.gd` — battle loss → retry prompt → brott down → new run (~4.1s, 245 ticks @ 60fps)
- `godot/tests/auto/test_settings_flow.gd` — boot → main menu → open settings (SettingsButton found) → close panel (<1s, 40 ticks @ 60fps)

**Files modified:**
- `godot/tests/auto/auto_driver.gd` — `_find_child_of_type` patched to check both `get_class()` and `get_script().get_global_name()` (+7 lines, -1 line)
- `godot/tests/test_runner.gd` — three new auto/ test files registered in SPRINT_TEST_FILES

**Total Pillar-1 suite wall-clock:** ~15s (well under 60s target)

## CI Results

| Check | Result |
|---|---|
| Godot Unit Tests | ✅ success |
| Playwright Smoke Tests | ✅ success |
| Export Godot → HTML5 | ✅ success |
| Deploy to GitHub Pages | ✅ success |
| Optic Verified | ✅ success |

All gating checks green. Full Playwright suite in_progress at audit time (non-blocking; smoke gate passed).

## Pillar 1 Completion Status

All four arc-brief-mandated user flows now CI-gated:

1. ✅ chassis-pick (S(I).1, sprint-27.1)
2. ✅ reward-pick (S(I).2, sprint-27.2)
3. ✅ run-end/death (S(I).2, sprint-27.2)
4. ✅ settings (S(I).2, sprint-27.2)

Pillar 1 is **COMPLETE**. The auto-driver test suite now covers every arc-brief-mandated critical path. Breaking any of the four signal paths (`_on_chassis_picked`, reward-pick signal, `_show_brott_down`, SettingsButton) causes its respective test to exit 1 → CI fail.

## Key Fix: _find_child_of_type

**Problem:** In Godot 4, `Node.get_class()` returns the *engine base class* (e.g., `"Control"`, `"Node2D"`), not the GDScript `class_name` declaration. Tests searching for nodes by their declared GDScript class name (e.g., `"SettingsButton"`) would always return `null`, causing flow tests to stall.

**Fix (in `auto_driver.gd`):**

```gdscript
func _find_child_of_type(node: Node, class_name_str: String) -> Node:
    if node == null:
        return null
    for child in node.get_children():
        # Check engine base class name
        if child.get_class() == class_name_str:
            return child
        # Check GDScript declared class_name (Godot 4)
        var s = child.get_script()
        if s != null and s.get_global_name() == class_name_str:
            return child
        var found := _find_child_of_type(child, class_name_str)
        if found != null:
            return found
    return null
```

The fix adds a second check: `get_script().get_global_name()` returns the value declared in `class_name SettingsButton` at the top of a GDScript file. Both paths are now checked, making the lookup engine-class-safe and script-class-safe simultaneously.

## Architecture Notes

All three S(I).2 tests follow the `_process(delta)` step-machine pattern established in S(I).1:

- Each test is a state machine driven by the engine's frame loop — no `await`, no sleep, no manual timers
- State advances based on scene state inspection each frame
- Zero new base-class verbs added to `AutoDriver` — `force_battle_end(winner_team)` and the existing API surface were sufficient for all three flows
- This pattern is intentional: engine-driven tests exercise real timing and transition logic rather than stubbing it

## Carry-Forwards to S(I).3 (Pillar 3 — Combat Sim Agent)

1. **Pillar 1 action-API surface is locked and stable** — `force_battle_end`, `_on_chassis_picked`, and all current AutoDriver verbs are tested and CI-gated. S(I).3 can extend or reuse this surface without risk of silent regression.
2. **`_find_child_of_type` fix is the canonical pattern for all future node lookups** — any test or driver code that searches by class name must use `get_script().get_global_name()`, not `get_class()`. Document this at the start of any new test file.
3. **`_process(delta)` step-machine is the mandated test architecture** — S(I).3 Combat Sim agent tests should follow the same pattern. Do not introduce `await`-based or sleep-based flow control.

## Grade

**A**

All four arc-brief-mandated Pillar 1 flows pass CI green. The `_find_child_of_type` fix is well-scoped and backward-compatible. Suite wall-clock (~15s) is well within budget. Architecture is clean with zero scope creep. Pillar 1 is complete and closed.
