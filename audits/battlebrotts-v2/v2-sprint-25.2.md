# S25.2 Audit — Multi-target Arena Renderer + Click Overlay
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#301
**Merge commit:** eaccf0eee5e56db45c453189125b4f51c3547d08
**Grade:** A

## Summary
S25.2 extends the arena renderer with multi-bot targeting clarity (numbered labels 1–N) and the player click-to-move/click-to-target control scheme. BrottBrain gains a clean override API with latest-wins semantics; the click handler in arena_renderer.gd routes floor vs. enemy clicks through testable helpers. Click overlay rendering (waypoint diamond, reticle ring, player outline pulse) is allocation-free using sin-wave accumulators. Override behavior is additive — S25.3 wires actual movement/targeting logic. All structural, behavioral, and test gates pass on main.

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. Multi-bot structural (no hardcoded slots) | ✅ PASS | sim.brotts iteration at all sites; numbered labels at L976 |
| 2. Click overlay state vars | ✅ PASS | 5 vars present (L107–L113) |
| 3. Latest-wins BrottBrain | ✅ PASS | each setter clears the other; evaluate() short-circuits |
| 4. Overlay rendering | ✅ PASS | _draw_click_overlay at L1100, called from _draw at L736 |
| 5. No Tween in hot path | ✅ PASS | zero Tween refs in arena_renderer.gd |
| 6. test_arena_renderer_multi registered | ✅ PASS | SPRINT_TEST_FILES, 18 conditions, 1394 total assertions clean |
| 7. Headless test | ✅ PASS | 18 passed, 0 failed (Godot 4.4.1) |
| 8. Visual regression screenshots | ⏭️ SKIPPED | CI Playwright/Optic Verified handles; already passing pre-merge |
| 9. FPS baseline | ⏭️ SKIPPED | CI-owned; combat_batch.gd doesn't emit FPS metrics |
| 10. Deploy landed | ⏳ PENDING | Build & Deploy in-flight at verification; not disabled |

## Deviations / Notes
- No bot_id on BrottState: index in sim.brotts used as stable per-match identifier. Valid since bots aren't removed on death (only flagged !alive). Noted for S25.3.
- _unhandled_input merged into existing function (F3 toggle coexists). Preserves dev overlay hotkey.
- set_player_brain wired at 3 game_main.gd sites (roguelike + legacy demo + league paths). Harmless on legacy paths.
- Override methods are additive stubs: movement_override strings "move_to_override"/"target_override" are new values S25.3 will interpret. No behavior change until S25.3.

## Carry-forwards to S25.3
- S25.3 must interpret movement_override == "move_to_override" and "target_override" in combat_sim/BrottBrain to produce actual movement and targeting behavior
- S25.3 introduces hardcoded baseline AI (gutting card internals) — builds on override API established here
- combat_batch.gd FPS emission: a one-line FPS emit to stderr would make Gate 9 automatable if desired

## Arc F progress
S25.1 ✅ | S25.2 ✅ | S25.3 ⏳ | S25.4–S25.9 📋
