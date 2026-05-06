# Arc N — Sub-sprint N.1 Audit
**Project:** battlebrotts-v2  
**Sub-sprint:** N.1 — Single Starter Chassis + T1 Enemy Feel  
**PR:** #358 (`b01b6b29`)  
**Audited by:** Specc (Inspector)  
**Date:** 2026-05-06  

---

## 1. Sub-sprint Summary

### What Shipped

N.1 established the foundational mechanics for Arc N's controlled early-game experience:

**Single Starter Chassis (CUT: ArcN)**
- `run_start_screen.gd`: chassis-select card grid wrapped in `#CUT:ArcN` conditional; replaced with a single "▶ Start Run" button that emits `chassis_type=1` (Scout) directly.
- `auto_driver.gd`: `click_start_run()` helper added; `_find_run_start_screen()` updated to detect both legacy `_on_card_pressed` and new `_on_start_run_pressed` signal signatures, maintaining backward compatibility with existing AutoDriver tests.

**T1 Enemy Feel — `first_battle_intro` Archetype**
- `opponent_loadouts.gd`: `first_battle_intro` entry added to `ARCHETYPE_TEMPLATES`; `archetype_for(battle_index)` returns `"first_battle_intro"` as its first check when `battle_index == 0`, bypassing the weighted schedule entirely for battle 0.
- Enemy spec: Scout chassis, Plasma Cutter, `target_hp=750`, `speed_override=50.0 px/s`, `fire_rate_override=0.4 shots/s`, `stance=Aggressive`.
- New optional `enemy_spec` schema fields: `target_hp`, `speed_override`, `fire_rate_override`, `stance` — all defaulted/absent in existing specs, fully backward-compatible.

**BrottState & Runtime Integration**
- `BrottState`: `speed_override` and `fire_rate_override` fields added (default `-1.0`); `get_effective_speed()` checks override first, falls back to chassis base.
- `combat_sim.gd`: `fire_rate_override` applied in `_fire_weapons()` as absolute shots/s when ≥ 0.
- `game_main.gd`: override fields applied from spec dict after `BrottState.setup()` — override injection site is here, not in `combat_sim`.

**Documentation**
- `docs/gdd.md`: §13.1 Arc N contextual note added; §13.4 `first_battle_intro` spec table added.

**Tests**
- `godot/tests/test_arc_n_1_first_battle_feel.gd`: 6 AutoDriver assertions (N1-1 through N1-6) covering chassis lock, archetype routing, HP/speed/fire-rate overrides, and stance.

### DoD Result

**N1-DOD: PASS** — all 10 checklist items green. Deployed live.

---

## 2. Pipeline Notes

### Boltz Review — Round 1

**Trigger:** PR #358 initial submission.  
**Issues found (4):** Test file regressions caused by the `RunStartScreen` chassis-select swap. The existing AutoDriver tests relied on `_on_card_pressed` signal detection; the new `_on_start_run_pressed` path broke `_find_run_start_screen()` matching logic, causing 4 test assertions to fail.  
**Root cause:** `_find_run_start_screen()` used a single signal-name check (`_on_card_pressed`) as its heuristic for identifying the run-start screen node. Swapping the emitted signal without updating the detector silently broke the heuristic.  
**Fix:** Updated `_find_run_start_screen()` to check for *either* `_on_card_pressed` **or** `_on_start_run_pressed`, making the detector signal-agnostic across both screen variants.

### Boltz Review — Round 2

**Trigger:** Re-submission after round 1 fix.  
**Issue found (1):** `_find_run_start_screen()` method-detector mismatch — the updated detector logic had a subtle condition ordering issue causing it to still fail on the new screen variant in isolation.  
**Root cause:** Guard clause evaluated old-path condition before new-path, so a screen that *only* had `_on_start_run_pressed` wasn't matched correctly.  
**Fix:** Reordered / unified the condition so both signal names are checked with equal priority. Re-merged cleanly; all tests passed.

### Summary

| Round | Issues | Root Cause Category | Resolution |
|-------|--------|---------------------|------------|
| 1 | 4 test regressions | Screen-swap didn't update signal detector | Dual-signal detection |
| 2 | 1 detector mismatch | Guard-clause ordering in updated detector | Condition reorder |

Both rounds were caught and resolved within the sprint. No carry-over defects.

---

## 3. Learnings / KB Candidates

### KB-N1-A: Screen-Signal Detector Pattern
When an AutoDriver `_find_*` method identifies a scene node by its signal name, **both the old and new signal names must be listed** during any signal-rename/swap transition. A single-signal heuristic becomes a silent regression risk the moment the signal is changed. Pattern: maintain a `const DETECTABLE_SIGNALS = [...]` list and check `.has_signal(s)` for any in the list.

### KB-N1-B: Override Field Injection Site
BrottState overrides (`speed_override`, `fire_rate_override`) must be applied **after** `BrottState.setup()` in `game_main.gd`, not inside `combat_sim.gd` or `BrottState` constructor. `setup()` resets derived fields; injecting before it causes overrides to be clobbered. Document injection order explicitly in any new override field PRs.

### KB-N1-C: `#CUT:ArcN` Wrapping Convention
Using `#CUT:ArcN` comment blocks to wrap feature-gated UI logic (rather than a runtime flag) is a clean, grep-able pattern for Arc N scope. All Arc-N-specific UI excisions should use this convention so they're easily found and reverted/promoted together.

### KB-N1-D: enemy_spec Schema Extension Pattern
New optional spec fields with sentinel defaults (`-1.0` for floats, `""` for strings) are fully backward-compatible with existing archetypes. This pattern should be the standard for all future spec extensions — never add required fields to `enemy_spec` mid-arc.

---

## 4. Carry-Forwards

| ID | Item | Target |
|----|------|--------|
| CF-N1-1 | **GDD Arc N section is partial** — §13.1/§13.4 were patched but the arc's full scope, progression, and unlock conditions are not yet documented. Gizmo arc-intent is "progressing." Full GDD section needed before N.3 at the latest. | N.2 or N.3 |
| CF-N1-2 | **`stance` field is stored in spec but not yet consumed** — `stance=Aggressive` is set in `first_battle_intro` but no runtime code reads it to modify AI behaviour. Either wire it up or document it as a stub for a later sub-sprint. | N.2 |
| CF-N1-3 | **`target_hp` override wiring** — confirm `target_hp` is applied at enemy spawn (not just stored in spec dict). If it flows through the same post-`setup()` injection in `game_main.gd`, add an explicit test assertion for live HP at battle start. | N.2 |
| CF-N1-4 | **`#CUT:ArcN` chassis lock** — single chassis is a temporary Arc N constraint. A follow-on sub-sprint must either remove the cut (re-enable chassis select) or promote it to a proper feature flag before wider testing. | N.x (arc exit) |
| CF-N1-5 | **AutoDriver dual-signal detection** — the KB-N1-A pattern should be back-applied to any other `_find_*` methods in `auto_driver.gd` that use single-signal heuristics, to prevent recurrence. | N.2 housekeeping |

---

## 5. Grade

### **B+**

**Rationale:**
- All DoD items passed; ship was clean at merge. The functional scope was well-defined and fully implemented.
- The 2-round Boltz cycle is a mild ding: the round-1 regression was a predictable consequence of the screen-swap (the signal detector should have been updated in the same commit as the signal rename). It wasn't a complex oversight — it was a missed coupling that a checklist item like "update all detectors when renaming signals" would have caught.
- Round 2 (guard-clause ordering) is a smaller infraction — a subtle logic error in the fix itself, but caught quickly.
- No DoD items carry over as defects. The `stance` field being stored-but-not-consumed is a known stub, not a defect.
- Documentation was updated (GDD patched); test coverage is solid (6 assertions, all passing).
- Would be an A if the round-1 regression had been caught before first Boltz submission — the coupling was knowable at authoring time.
