# S(I).5 Audit — Arc I: bb_test JS Bridge (DebugTestBridge autoload)

**Sprint:** Arc I S(I).5 (sprint-27.5)
**Arc:** I — Optic Plays The Game
**Pillar:** 2 — Web-export drive (foundation)
**PR:** #330
**Merged:** 2026-04-27
**Merge commit:** 1e11c2715b11e06574b40dc54d9b98d6a055178a
**Auditor:** Specc

---

## Deliverables

- `godot/debug/debug_test_bridge.gd` — extends Node. `window.bb_test` created via JavaScriptBridge.get_interface("window") + create_object("Object"). 6 verbs: click_chassis, click_reward, get_run_state, get_arena_state, force_battle_end, get_version. Lazy _get_game_main(). GC-safe callback refs. JSON-safe serialization.
- `godot/project.godot` — DebugTestBridge="*res://debug/debug_test_bridge.gd" autoload added.
- `godot/export_presets.cfg` — [preset.1] "Web Debug" with custom_features="debug_test_bridge".

## CI Results

Godot Unit Tests ✅ | Playwright ✅ | Audit Gate ✅ | Optic Verified ✅

## Design Verification

- Runtime gate: OS.has_feature("web") AND OS.has_feature("debug_test_bridge") — early return if either false ✅
- _js_callbacks Array holds all 6 create_callback refs to prevent GC ✅
- _get_game_main(): lazy, is_instance_valid() re-resolve ✅
- _find_child_of_type: get_class() + get_script().get_global_name() dual-check ✅
- All returns JSON-safe: plain Array via _plain_array(), explicit int() casts, {error:} on failure ✅
- Release "Web" preset has no custom_features → bb_test never injected in production ✅

## Carry-Forwards to S(I).6

1. Verify window.bb_test is accessible in actual WebGL build (manual test or CI with GPU runner)
2. S(I).6 Playwright spec: bb_test.click_chassis(0) + poll get_arena_state().in_arena + getPixelStats() non-monochrome
3. Post-export CI grep check: `grep -c 'bb_test' build/*.js` must return 0 for release build

## Grade

**A** — Bridge foundation complete. Clean runtime gate, GC-safe, JSON-safe API surface. CI green. Pillar 2 foundation ready for S(I).6 Playwright spec.
