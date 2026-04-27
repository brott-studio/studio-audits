# Arc I S(I).5 — Optic Evidence

**Sprint:** Arc I S(I).5 (sprint-27.5)
**PR:** #330
**Merged:** 2026-04-27
**Merge commit:** 1e11c2715b11e06574b40dc54d9b98d6a055178a

## Deliverables

- [x] `godot/debug/debug_test_bridge.gd` — DebugTestBridge autoload, 6 verbs via JavaScriptBridge
- [x] `godot/project.godot` — DebugTestBridge autoload registered
- [x] `godot/export_presets.cfg` — "Web Debug" preset with custom_features=debug_test_bridge

## CI: all green on merge commit

## Architecture

Runtime-gated: no-op unless OS.has_feature("web") AND OS.has_feature("debug_test_bridge"). Lazy _get_game_main() resolves scene root per call. All 6 callback refs held in _js_callbacks to prevent GC. JSON-safe returns: plain Array, explicit int() casts.

## Pillar 2 status

S(I).5 bridge foundation complete. S(I).6 adds Playwright spec driving the deployed WebGL build via window.bb_test.
