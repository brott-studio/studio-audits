# S25.1 Audit — RunState Scaffold + GameFlow Rework
**Arc:** Arc F — Roguelike Core Loop
**Date:** 2026-04-25
**PR:** brott-studio/battlebrotts-v2#300
**Merge commit:** 18cf11ed3bf2a8ffd45784321b554bb7c5ee1c1d
**Grade:** A

## Summary
Introduced `RunState` (RefCounted, replaces league-era `GameState` for active run-scoped data) and reworked `GameFlow` with a `RUN_START` screen, `run_state` property, and `start_run/advance_battle/end_run` API. Wired the new roguelike entry path in `game_main.gd` (`_on_new_game → _show_run_start → _on_chassis_picked → _start_roguelike_match → _show_stub_result`) using `RunState.build_player_brott()`, added `RunStartScreen` (3-chassis Fisher-Yates shuffle, seeded RNG), and excised GDD §B league-reflect machinery (`reflect_damage_for_league`, `REFLECT_DAMAGE_BY_LEAGUE`, `BrottState.current_league`, plus `opponent_data.gd` cascade). Lays the foundation for S25.2+ to build battles, AI, rewards, and retry on top.

## Acceptance gates
| Gate | Result | Notes |
|------|--------|-------|
| 1. reflect/league grep clean | ✅ PASS | GitHub code search: 0 hits for `reflect_damage_for_league` and `REFLECT_DAMAGE_BY_LEAGUE` repo-wide; spot-checked `combat_sim.gd`, `armor_data.gd`, `brott_state.gd`, `opponent_data.gd` — all clean |
| 2. RunState fields complete | ✅ PASS | `godot/game/run_state.gd` (60 lines): chassis/weapons/armor/modules, retry_count=3, current_battle_index, battles_won, _last_encounter_archetype=-1, _farthest_threat_name, _best_kill_name, seed; `build_player_brott()` constructs BrottState without GameState reference |
| 3. GameFlow RUN_START + run_state | ✅ PASS | `godot/game/game_flow.gd`: `Screen.RUN_START` enum added, `run_state: RunState` property, `start_run/advance_battle/end_run/has_active_run/go_to_run_start` implemented; legacy SHOP/LOADOUT/BROTTBRAIN_EDITOR/OPPONENT_SELECT enums kept dormant w/ Arc-G CUT comments |
| 4. game_main active path clean | ✅ PASS | `_on_new_game` (L205) → `_show_run_start` (L212) → `_on_chassis_picked` (L220) → `_start_roguelike_match` (L224) → `_show_stub_result` (L264); player brott built via `game_flow.run_state.build_player_brott()` (L230), no GameState reads on the active path |
| 5. RunStartScreen API | ✅ PASS | `godot/ui/run_start_screen.gd` (76 lines): `class_name RunStartScreen`, `signal start_run_requested(chassis_type: int)`, `setup(rng_seed)` with seeded Fisher-Yates shuffle of `[Scout=0, Brawler=1, Fortress=2]` |
| 6. MainMenuScreen "New Run" | ✅ PASS | "⚡ NEW RUN" button at (515,350), wired to `_on_new_game` which emits `new_game_pressed`, consumed by `game_main._on_new_game` |
| 7. test_run_state_init registered | ✅ PASS | Registered in `SPRINT_TEST_FILES` at L106 of `test_runner.gd`; 14 assertions (T1=7 default-construction, T2=3 chassis-construction, T3=4 build_player_brott) |
| 8. Arc-G quarantine | ✅ PASS | `SPRINT_TEST_FILES_ARC_G_PENDING` constant at L114-117 holds `test_sprint3.gd`, `test_sprint14_1.gd`, `test_sprint22_2c.gd`; runner executes them informationally and does not affect exit code |
| 9. Headless test | ✅ PASS | "Godot Unit Tests" check on merge commit: `success` (17:35:36Z → 17:37:20Z, 1m44s); 14/14 assertions per Optic |
| 10. Deploy landed | ✅ PASS | "Deploy to GitHub Pages": `success` at 17:36:21Z (~55s post-push); "Build & Deploy" workflow: `success` at 17:38:35Z |

## Deviations / Notes
- **Dormant compatibility shims in GameFlow** (`new_game()`, `go_to_shop()`, `go_to_loadout()`, `go_to_brottbrain()`, `go_to_opponent_select()`, `select_opponent()`, `finish_match()`, `continue_from_result()`) plus `game_state: GameState`, `selected_opponent_index`, `last_bolts_earned` retained for `tools/test_harness.gd` and the demo URL route. Each annotated `# CUT: Arc G — dormant`. Active S25.1 flow does not invoke any of them. Acceptable bridge; Arc G removes.
- **Cascade fix in `opponent_data.gd`** (removal of `b.current_league`) was not in the explicit S25.1 spec but was correctly applied by Nutts as a downstream consequence of removing `BrottState.current_league`. Without it, the file would not have compiled.
- **Arc-G-pending quarantine pattern** is a new test-runner mechanism: tests that reference removed APIs run informationally (output captured, exit code ignored) instead of being deleted preemptively. Pattern documented for Arc G to clean up the constant + files together.

## Known failing tests (expected, Arc G cleanup)
- `test_sprint3.gd` — exercises old GameFlow new_game→SHOP behavior
- `test_sprint14_1.gd` — references `BrottState.current_league`
- `test_sprint22_2c.gd` — league-reflect tests (REFLECT_DAMAGE_BY_LEAGUE)

## Carry-forwards to S25.2
- Arena renderer must be extended to N-bot (multi-target from battle 1, per HCD 16:40 refinement)
- Stub arena currently uses bronze-0 opponent; S25.4/S25.6 replaces with encounter archetype generator
- `RunState._last_encounter_archetype` field is in place but unused until S25.4
- `retry_count` decrement and `end_run` invocation belong to S25.5; S25.2 should leave the retry/lose paths as pass-through stubs
- `current_battle_index` is incremented by `advance_battle()` but no caller wires it yet — S25.2's win-path is the natural integration point

## Learnings / KB entries
- **Quarantine-by-constant pattern for cross-arc cleanup.** When an arc cuts an API but downstream tests for that API will be deleted in a later arc, isolate them in a separate runner constant (`SPRINT_TEST_FILES_ARC_G_PENDING`) and execute them informationally. Keeps CI green at the arc boundary without tempting premature deletion or losing the diagnostic value of the failing output. Pair with explicit "Arc G removes files + constant together" comment so the cleanup is unambiguous.
- **RunState as a pure replacement, not a wrapper.** `RunState.build_player_brott()` constructs `BrottState` directly from its own fields with zero `GameState` reads on the active path. Resists the easy mistake of having the new state class delegate to the old one for "compatibility" — that delegation would have re-coupled the league-era GameState into the roguelike loop and made Arc G's deletion non-trivial. Future arc-replacement classes should follow this no-delegation rule.

## Arc F progress
S25.1 ✅ | S25.2 ⏳ | S25.3–S25.9 📋
