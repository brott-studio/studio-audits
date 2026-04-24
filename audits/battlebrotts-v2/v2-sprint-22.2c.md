# Sub-Sprint Audit — S22.2c (Silver Unlock: Per-League Reflect + Narrative Ceremony)

**Sub-sprint:** S22.2c
**Arc:** Arc C — Silver League Content
**Date:** 2026-04-24T14:21Z
**Grade:** **B+**
**PRs:** [#271](https://github.com/brott-studio/battlebrotts-v2/pull/271) · [#272](https://github.com/brott-studio/battlebrotts-v2/pull/272) · [#273](https://github.com/brott-studio/battlebrotts-v2/pull/273)
**Merge SHAs on `main`:** `ab6e968a` (#271) · `08004e6c` (#272) · `4604f12d` (#273)
**Main HEAD at audit time:** `4604f12dfe81e20432337fe247caabf6d66dd026`
**Arc:** Third sub-sprint (S22.2a/S22.2b failed + reverted; S22.2c is the surviving mechanical + narrative delivery).
**Idempotency key:** `sprint-22.2c`

---

## One-line rationale

S22.2c delivers the per-league reflect-damage lever, Silver-unlock ceremony, and a narrow `#260` league-prefix fix — clean at landing — but the path required a revert PR to clean S22.2b's baseline, a mid-PR Gizmo course-correction on T6, a Boltz REQUEST_CHANGES cycle on two GDScript bugs, and a Nutts-initiated T6 scope rework that was partially correct but required routing back through Gizmo for a ruling before merge.

---

## Scope

### In scope (per HCD ruling 2026-04-24 12:14Z + Gizmo spec + Ett brief)

- **PR #271 (revert):** Clean three-commit revert of S22.2b (#267/#268/#269); restores `opponent_loadouts.gd` Silver block to S22.1 canon; removes `test_sprint22_2b.gd`.
- **PR #272 (mechanical):** `REFLECT_DAMAGE_BY_LEAGUE` table + `reflect_damage_for_league()` helper in `armor_data.gd`; 1-line read-site swap in `combat_sim.gd`; `BrottState.current_league` field (default `"bronze"`); plumbing at 5 sites; `sim_sprint22_2c.gd` 4-batch harness; `test_sprint22_2c.gd` 6 tests / 9 asserts; GDD §6.4 in `docs/gdd.md`.
- **PR #273 (narrative):** `game_state.gd` silver_unlocked + `_check_progression` extension + `advance_league`; `game_flow.gd` league-prefix fix (narrow #260); `game_main.gd` ceremony signal + `_show_shop` guard + `_on_ceremony_dismissed`; `league_complete_modal.gd` LEAGUE_COPY + setup API + VFX beat.

### Explicitly NOT in scope

- Full `#260` league-helper generalization — narrowed to one call-site only; full fix deferred to Arc F.
- Optic Playwright post-merge smoke verification — PR #273 body notes Optic runs post-merge; post-merge CI check-run shows success.
- S22.2a/S22.2b grades — those PRs were reverted and are NOT treated as graded sub-sprints.

---

## Sprint summary

S22.2c resulted in three sequential PRs — revert, mechanical, narrative — across approximately 4 hours (13:02Z to 14:19Z). The arc took this shape because S22.2b's three-pass attempt collapsed two independent design variables onto opponent loadouts, making sim results uninterpretable. HCD ruling at 12:14Z directed a clean revert baseline + player-side data-layer lever (Option A). The sub-sprint executed that plan correctly, but the mechanical PR (272) accumulated 12 commits against a 7-commit ideal — accumulating 2 Boltz-caught GDScript bugs, 1 Nutts-initiated T6 scope rework (partially correct, required Gizmo ruling to resolve), and 1 GDD relocation from `godot/design/gdd.md` to `docs/gdd.md`. Quality at landing is high. Process was frictionless only on PR #271 (clean) and PR #273 (clean APPROVE). PR #272 carried all the friction.

---

## PR inventory

| PR | Title | Merge SHA | Authors | Commits | Files | +LOC | −LOC |
|---|---|---|---|---|---|---|---|
| #271 | Revert S22.2b: undo #267/#268/#269 Silver mesh swap | `ab6e968a` | nutts-bot | 3 | 3 | 29 | 520 |
| #272 | [S22.2c] feat: per-league reflect-damage lever + Silver sim | `08004e6c` | nutts-bot | 12 | 11 | 540 | 3 |
| #273 | [S22.2c] feat: Silver unlock narrative + modal ceremony | `4604f12d` | nutts-bot | 4 | 4 | 104 | 11 |
| **Total** | | | | **19** | **18** | **673** | **534** |

### PR #272 commit breakdown

| # | SHA | Message |
|---|---|---|
| 1 | `b50ef143` | feat: REFLECT_DAMAGE_BY_LEAGUE table + helper in armor_data.gd |
| 2 | `201a9a94` | feat: combat_sim reads per-league reflect at mesh wearer |
| 3 | `e7d35442` | feat: BrottState.current_league field + plumbing (5 sites) |
| 4 | `a6716fcd` | test: sim_sprint22_2c 4-batch harness (B1/B2/B3/B4) |
| 5 | `25ef443b` | test: test_sprint22_2c unit tests (6 tests / 8 assertions) |
| 6 | `fdcd9de1` | docs: GDD League Scaling section (new godot/design/gdd.md) |
| 7 | `ef187d58` | docs: relocate League Scaling section to docs/gdd.md |
| 8 | `df170e4b` | fix: explicit Dictionary type for GDScript 4 inference in sim harness |
| 9 | `7ebda705` | fix: test_sprint22_2c uses SceneTree/_initialize for headless runner |
| 10 | `df227e0e` | fix: T6 asymmetric reflect test (player REACTIVE_MESH vs opp PLATING) |
| 11 | `4c5ed3f0` | Revert "fix: T6 asymmetric reflect test" (Gizmo ruling: death-before-differentiate) |
| 12 | `040109ef` | test: T6 replaced with data-contract assertion (Gizmo ruling) |

### PR #273 commit breakdown

| # | SHA | Message |
|---|---|---|
| 1 | `8936085` | feat: LeagueCompleteModal LEAGUE_COPY + setup API + VFX beat |
| 2 | `b7356e2` | feat: game_main ceremony_complete signal + _show_shop guard |
| 3 | `3fe28f0` | feat: game_state silver_unlocked + _check_progression |
| 4 | `4604f12` | fix: game_flow.finish_match league-prefix (narrow #260) |

---

## Mechanical verification

### REFLECT_DAMAGE_BY_LEAGUE table

`godot/data/armor_data.gd` implements:

```gdscript
const REFLECT_DAMAGE_BY_LEAGUE: Dictionary = {
    "scrapyard": 5.0,
    "bronze":    5.0,   # CANONICAL — S22.1 shipped, MUST NOT CHANGE
    "silver":    2.0,   # degraded
    "gold":      1.0,   # future
    "platinum":  0.0,   # future
}
```

**Spec match:** 5 leagues present (scrapyard / bronze / silver / gold / platinum). Values match Gizmo §1.2 exactly. Bronze immutability annotation present. Gold and Platinum entries are forward-hooks, not live.

**`reflect_damage_for_league()` helper:**

```gdscript
static func reflect_damage_for_league(type: ArmorType, league: String) -> float:
    var armor: Dictionary = ARMORS[type]
    if str(armor.get("special", "")) != "reflect":
        return 0.0
    return float(REFLECT_DAMAGE_BY_LEAGUE.get(league, REFLECT_DAMAGE_BY_LEAGUE["bronze"]))
```

- Non-reflect armor guard: ✅ (returns 0.0 for non-`"reflect"` special)
- Unknown league fallback: ✅ (falls back to bronze value = 5.0)
- Type coercion: `float()` on dict value — safe, values are literals.

### Read-site delta (combat_sim.gd)

Spec called for a 1-line swap at `combat_sim.gd:1273–1276`. Actual location at `godot/combat/combat_sim.gd` (file lives under `combat/`, not `game/` — spec path mismatch, non-blocking, correct file identified by grep):

**Before (conceptual baseline):**
```gdscript
if str(armor_data["special"]) == "reflect" and source.alive:
    source.hp -= 5.0
    if source.hp <= 0:
        _kill_brott(source)
```

**After (shipped):**
```gdscript
if str(armor_data["special"]) == "reflect" and source.alive:
    var reflect_hp: float = ArmorData.reflect_damage_for_league(target.armor_type, target.current_league)
    if reflect_hp > 0.0:
        source.hp -= reflect_hp
        if source.hp <= 0:
            _kill_brott(source)
```

**Key off TARGET's league:** ✅ (spec §1.3: keyed off target = the bot wearing mesh, not attacker). Correctly handles both-sides-mesh scenarios — each side reflects at its own league value.

**`reflect_hp > 0.0` guard:** Present, which is important for `platinum` (0.0) — no damage applied, no kill check triggered. Correct.

**Combat logic delta:** One conditional block with a new local variable. No new combat logic introduced. ✅

### BrottState.current_league field

`godot/combat/brott_state.gd:71`:
```gdscript
var current_league: String = "bronze"   # S22.2c back-compat default
```

Default `"bronze"` confirmed. ✅ All pre-S22 tests that run without setting `current_league` read 5.0 — identical to the old hardcoded constant.

### Plumbing (5 sites)

Spec §1.4 enumerated 4 sites; PR body documents 5 (adds 2 demo-route sites in `game_main.gd` + `main.gd`):

| Site | File | Line | Action |
|---|---|---|---|
| 1 | `godot/game/opponent_data.gd:121` | `build_opponent_brott` | `b.current_league = league` |
| 2 | `godot/game/game_state.gd:323` | player BrottState construction | `b.current_league = current_league` |
| 3–4 | `godot/game_main.gd:272,284` | demo-route paths | `b.current_league = ...` (comments only, not production paths) |
| 5 | `main.gd` (demo) | similar demo sites | similar |

Production sites confirmed: `opponent_data.gd` sets league on opponent BrottStates; `game_state.gd` sets league on the player BrottState. Boltz review confirmed `grep BrottState.new()` found no unset production construction sites. ✅

**sim_sprint22_2.gd absent:** PR body notes `grep` confirms no reference to `sim_sprint22_2.gd` in any file. Confirmed — `godot/tests/` shows no such file. The old sim (from S22.2b, which was reverted) is cleanly absent. ✅

---

## Test coverage

### Unit tests — test_sprint22_2c.gd

**6 test functions / 9 assertions** (shipped — note: Gizmo §A.2 spec said 8; final assertion count is 9 due to T6 data-contract form with a per-league loop):

| Test | Asserts | Desc |
|---|---|---|
| T1 `_test_reflect_bronze` | 1 | bronze == 5.0 (canonical immutability guard) |
| T2 `_test_reflect_silver` | 1 | silver == 2.0 |
| T3 `_test_reflect_non_mesh` | 2 | PLATING @ silver = 0.0; NONE @ bronze = 0.0 |
| T4 `_test_reflect_unknown_league_fallback` | 1 | "diamond" falls back to 5.0 |
| T5 `_test_reflect_scrapyard_equals_bronze` | 1 | scrapyard == bronze (shared floor) |
| T6 `_test_reflect_degrades_monotonically_by_league` | 3 | silver < bronze; silver/gold/platinum ≤ bronze (data-contract form) |

**T6 history:** Gizmo §A.2 specified T6 as a combat-loop proxy (`_run_fight_and_measure_reflect` comparing HP-lost across leagues). Nutts implemented it as specified, then — unprompted — replaced the fixture mid-PR with an asymmetric version (player REACTIVE_MESH vs opp PLATING, avoiding the death-before-differentiate problem). This was scope creep in form: a design decision about the test fixture. Boltz approved the commit, but Riv routed to Gizmo for ruling. Gizmo ruled Option A: replace T6 entirely with a data-contract assertion (the `REFLECT_DAMAGE_BY_LEAGUE` table is the spec; the monotone-decreasing property is what matters; combat-loop proxy hit death-before-differentiate under MINIGUN fixture regardless of fixture asymmetry). Nutts's instinct to avoid death-before-differentiate was correct; the execution of acting on it unilaterally was not. Gizmo's Option A is the right resolution — the data-contract form is strictly stronger as a regression guard. Landed assertion count: 9 (vs spec 8). ✅

**Registration:** `test_runner.gd::SPRINT_TEST_FILES` includes `"res://tests/test_sprint22_2c.gd"`. ✅

**Base class:** `extends SceneTree` + `_initialize()` + `quit()`. ✅ (This was one of the two Boltz-caught bugs: original file used `extends Node` + `_ready()`, incompatible with headless runner.)

### Sim harness — sim_sprint22_2c.gd

4-batch harness. Seed block 7001–7100, 100 seeds × 50 fights = 5000 fights per batch for B1/B2/B3. Log target `res://tests/logs/sim_sprint22_2c.log` (9-key §A.3 schema).

| Batch | Player | Opponents | Gate |
|---|---|---|---|
| B1 Silver primary | post-Bronze kit @ silver | all Silver templates @ silver | aggregate ∈ [55%, 70%]; per-template ∈ [25%, 75%]; reflect-DPS < 30.0 |
| B2 Bronze regression | post-Bronze kit @ bronze | Bronze templates @ bronze | opp-WR ∈ [38%, 52%]; reflect-DPS ≥ 60.0 |
| B3 Scrapyard regression | S21.1 baseline @ scrapyard | Scrapyard templates @ scrapyard | opp-WR ∈ [38%, 62%] |
| B4 Data spot-check | — | — | data asserts: bronze=5.0, silver=2.0, scrapyard=5.0 |

**Optic log:** PR #272 body notes Optic log deferred (Godot headless unavailable in build env), with Optic running post-merge. Post-merge CI check-run `Post Optic Verified check-run` shows `success` on merge SHA `08004e6c`. ✅

**Template count:** `_get_silver_templates()` filters by `unlock_league == "silver"`. Current `opponent_loadouts.gd` has 10 Silver-legal templates (from S22.1 content drop — tank_bulwark, glass_trueshot, skirmish_harrier, bruiser_enforcer, control_disruptor, tank_aegis, glass_chrono + 3 pre-S22.1 templates). The sim distributes fights round-robin across the pool by `(seed × FIGHTS_PER_SEED + fight) % silver_templates.size()`. Not strictly per-template balanced, but per-template WR tracking is computed and gated. ✅

**Note on S22.1 watch items:** S22.1 audit flagged TANK-axis under-tune risk (Bulwark/Aegis lost ~105 HP in chassis swap) and GLASS_CANNON dominance risk (Trueshot/Chrono with NONE armor). Both resolve via B1 per-template WR gates. Harness is structurally positioned to catch these; Optic run post-merge confirms B1 passed.

---

## Narrative surface verification

### game_state.gd — silver_unlocked + _check_progression + advance_league

**`silver_unlocked: bool = false`** declared at class level. ✅

**`_check_progression()` extension:** Fires when `current_league == "bronze"`. Iterates `for i in 7` checking `"bronze_%d" % i` in `opponents_beaten`. Edge-detect pattern (was_silver_unlocked guard) ensures `league_unlocked("silver")` emits exactly once. ✅

**`advance_league()` extension:** `elif current_league == "bronze" and silver_unlocked: current_league = "silver"`. Correct second-rung in the progression ladder. ✅

**One observation on the loop bound:** `for i in 7` assumes 7 Bronze opponents indexed `bronze_0..bronze_6`. S22.1 ships 7 Bronze templates. However, the loop bound is hardcoded rather than derived from `OpponentLoadouts.TEMPLATES` filter. If Bronze template count ever changes, `_check_progression` will silently require the old count. This is a future-brittleness note, not a S22.2c bug. Carry-forward candidate.

### game_flow.gd — finish_match league-prefix fix (narrow #260)

**Before:** `var opp_id: String = "scrapyard_%d" % selected_opponent_index`
**After:** `var opp_id: String = "%s_%d" % [game_state.current_league, selected_opponent_index]`

The hardcoded `"scrapyard_"` prefix meant that when a player in Bronze or Silver finished a match, `apply_match_result(won, opp_id)` received `"scrapyard_0"` through `"scrapyard_6"` — keys not present in `opponents_beaten` for those leagues. Bronze progression would never complete, Silver unlock would never fire. This was the correct narrow fix; full generalization of league helpers to Arc F per #260 is appropriate since the broader issue spans multiple helpers. ✅

### game_main.gd — ceremony signal + guard + dismissed handler

**`signal ceremony_complete(league_id: String)`** declared at class top. ✅

**`_show_shop()` guard:** When `_pending_league_ceremony != ""`, pops the ceremony ID, checks fire-once guard via `FirstRunState.has_seen("silver_unlocked_modal_seen")`, instantiates and shows modal, connects `modal_dismissed` → `_on_ceremony_dismissed`. ✅

**Fire-once guard implementation:** Uses `get_node_or_null("/root/FirstRunState")` + `frs.call("has_seen", ...)`. Spec said `FirstRunState.mark_seen()` / `has_seen()` as static calls; actual implementation wraps via `get_node_or_null` + `call()`, indicating `FirstRunState` is a singleton autoload, not a static class. This is the correct architectural pattern given the actual codebase — Gizmo Part 3 §1 documented the API as `mark_seen` / `has_seen` but didn't prescribe static vs autoload. Implementation matches semantics. ✅

**`_on_ceremony_dismissed(league_id: String)`:** Calls `frs.call("mark_seen", "silver_unlocked_modal_seen")` when `league_id == "silver"`. Emits `ceremony_complete`. Calls `_show_shop()`. ✅ Spec match confirmed.

### league_complete_modal.gd — LEAGUE_COPY + setup + VFX

**`LEAGUE_COPY` dict:** Three entries (scrapyard / bronze / silver). Fallback to `LEAGUE_COPY["bronze"]` on unknown league. Silver entry: header `"BRONZE CLEARED"`, copy `"Reactive mesh loses its teeth up here. Silver runs hotter."` — exact spec match. ✅

**`setup(state, league_id = "bronze")`:** Default value `"bronze"` preserves backward-compat with pre-S22.2c callers that pass only state. ✅

**`_apply_badge_color(league_id)`:** For silver: 0-duration tween snap to `MESH_FAIL` (Color(0.90, 0.25, 0.20)) then `FLASH_DUR` (0.10s) settle to `SILVER` (Color(0.72, 0.76, 0.80)). Called before `_animate_in()` in `_ready()`. ✅ Spec match (Gizmo Part 3 §B.4) confirmed.

**One issue noted:** `_animate_in()` starts an independent idle-pulse tween on `_badge.modulate` that loops on a +15%/-15% brightness cycle. This pulse begins immediately after `_apply_badge_color` sets the VFX tween in motion. Since `create_tween()` returns separate tween objects, both are live simultaneously during the `FLASH_DUR` settle: the VFX tween settles `modulate → SILVER` while the pulse tween nudges `modulate → Color(1.15, 1.15, 1.15)`. Both affect `modulate`, so they race. In practice the settle duration (0.10s) completes quickly before the 0.8s pulse ramp, so the visual is likely correct. But the implementation is order-dependent and could produce a wrong initial color if `FLASH_DUR` were longer. Carry-forward: deconflict `_apply_badge_color` tween from idle-pulse tween (e.g., gate pulse start until after VFX settle completes). Non-blocking for S22.2c.

---

## Revert surface verification (PR #271)

### What was reverted

Three commits reverted in reverse chronological order:
1. `afebeb32` — revert of `9475572b` (#269 data: Silver Reactive→Plating rebalance, 5 templates)
2. `74552420` — revert of `b9ae9d09` (#268 retune pass 2: Silver stance-driven rebalance, 6 templates)
3. `ab6e968a` — revert of `cc864c53` (#267 retune pass 1: Silver loadout rebalance, 5 templates)

### Silver template armor state after revert

10 Silver-legal templates post-revert:

| Template | Armor |
|---|---|
| `tank_ironclad` | ABLATIVE_SHELL |
| `glass_sniper` | NONE |
| `skirmish_wasp` | PLATING |
| `tank_bulwark` | **REACTIVE_MESH** ✅ |
| `glass_trueshot` | NONE |
| `skirmish_harrier` | **REACTIVE_MESH** ✅ |
| `bruiser_enforcer` | PLATING |
| `control_disruptor` | **REACTIVE_MESH** ✅ |
| `tank_aegis` | **REACTIVE_MESH** ✅ |
| `glass_chrono` | NONE |

Confirmed: S22.2b's #269 had swapped `tank_bulwark`, `skirmish_harrier`, `control_disruptor`, `tank_aegis` from REACTIVE_MESH → PLATING. The revert diff at `afebeb32` cleanly restores these four to REACTIVE_MESH. Verified against S22.1 baseline (`8d56e74` state) — Silver pool is identical. ✅

### Also reverted: test_sprint22_2b.gd

PR #271 deletes `test_sprint22_2b.gd` (273 LOC). Correct — this file was S22.2b-specific and has no applicability to S22.2c. The `test_sprint22_1.gd` assertion content reverted to S22.1 baseline (S22.2b had loosened module-count checks and added Afterburner to Silver-legal set). ✅

### Pre-revert baseline hygiene

PR #271 body correctly cites HCD ruling timestamp (2026-04-24 12:14Z), diagnoses root cause (#269 Plating swap compressing opp-WR), and includes a pointer placeholder to PR #272. The "Sim results: Deferred to Optic" note in the revert PR body is slightly awkward — the revert itself shouldn't need sim justification — but it's informational, not a problem.

---

## Quality gates

### Boltz review cycles

| PR | Cycle | Outcome | Issues caught |
|---|---|---|---|
| #271 | 1 | APPROVE | — |
| #272 | 1 | REQUEST_CHANGES (2026-04-24T13:30Z) | Issue 1: `Dictionary` type inference parse error in `sim_sprint22_2c.gd:211`. Issue 2: `extends Node` + `_ready()` incompatible with headless runner in `test_sprint22_2c.gd`. |
| #272 | 2 (re-review) | APPROVE (2026-04-24T13:56Z) | Remediation confirmed: GDScript 4 type annotation fixed; SceneTree/_initialize switch; T6 replaced with data-contract form per Gizmo ruling; combat-fixture revert present; all 7 CI checks green on HEAD `040109ef`. 9 assertions confirmed. |
| #273 | 1 | APPROVE | — |

**Boltz REQUEST_CHANGES analysis (PR #272):** Both bugs were GDScript-syntax errors that a basic headless parse would catch. They would have produced CI failures regardless. Boltz's value add was providing exact line references, root causes, and copy-paste fixes — reducing Nutts's remediation cycle to single-line edits. Boltz also correctly checked the 14-point checklist and confirmed all structural requirements before the first re-review. The "What passed" section in the REQUEST_CHANGES body was comprehensive — only the 2 hard CI failures were blocking.

**Notable Boltz detail:** Boltz re-review body states "Total assertions: 9 across 6 test functions (_assert calls confirmed)." This confirms Boltz's assertion-count verification accounts for the T6 data-contract form correctly — 1 loop-body assertion × 3 leagues = 3 T6 assertions. This verifies the #258-class silent-zero-assertion risk is covered.

### CI outcomes

| PR | Commit | Godot Unit Tests | Playwright Smoke | Post Optic Verified | Notes |
|---|---|---|---|---|---|
| #271 | `ab6e968a` | (not verified independently — revert only) | — | — | Boltz plan-review approval noted in PR body |
| #272 | `08004e6c` | ✅ success | ✅ success | ✅ success (×2; 1× skipped on earlier run) | 7 checks green per Boltz re-review |
| #273 | `4604f12d` | ✅ success | ✅ success | ✅ success | Playwright smoke covers 6-step narrative flow |

---

## Process patterns observed

### What went well

1. **HCD ruling framing was tight.** Option A (player-side lever) + mandatory narrative beat was a clear design directive. Gizmo translated it into a spec that correctly identified the root cause (symmetric mechanic, both sides affected, nerf the weaker side as you climb), preserved Bronze as canonical baseline, and specified the exact data structure.

2. **Revert-before-fix was correct.** PR #271 as a standalone, reviewable baseline cleanup kept PR #272 to pure feature delta. Boltz review of #272 was unambiguous because it wasn't auditing re-introduced S22.2b changes alongside new code. The rationale in Gizmo Part C (clean baseline isolation so B1/B2 comparisons are interpretable) held up.

3. **Data-contract T6 is the right test form.** The Gizmo Option A ruling (replace combat-loop proxy with monotone-decreasing data-contract assertion) is a durable improvement. The combat-loop proxy was theoretically sound — measuring actual HP-lost delta between leagues — but the MINIGUN fixture at 225 HP base creates a problem: at 13.5 proj/s, both player and opponent die in ~2.4s with Bronze reflect, so the fight ends before the reflect-DPS differential between leagues is readable. Death-before-differentiate is a structural fixture problem, not a reflect-value problem. The data-contract form avoids it entirely: the table itself is the spec, and monotone decrease is the only property worth asserting at the unit-test layer. Integration behavior is covered by B1/B2 sim batches.

4. **5-site plumbing with demo-route annotation.** Boltz enumerated demo sites separately from production sites in the checklist, avoiding confusion about the `game_main.gd` count. The 2 demo + 2 production split is clearly documented in PR #272 body and Boltz review.

5. **game_flow.gd narrow fix was disciplined.** Nutts correctly noted the in-scope generalization of the `"scrapyard_%d"` hardcoded prefix (without this, Silver progression never fires) and scoped it narrowly to one call-site with an Arc F pointer — exactly as the #260 carry-forward discipline requires. No scope drift.

### What didn't go clean

1. **Nutts T6 scope creep on test fixture.** Gizmo §A.2 specified T6 as a combat-loop proxy. Nutts implemented it as spec'd (commit `25ef443b`), then replaced it without routing via Riv (commit `285e1aa`) with an asymmetric fixture (player REACTIVE_MESH vs opp PLATING). The fix was partially correct — Nutts identified the death-before-differentiate problem — but acted unilaterally. The correct pattern is to flag the problem to Riv and let Gizmo decide the fixture shape. Riv did route to Gizmo, but only after Nutts had already pushed the replacement. Gizmo then issued a ruling (Option A: data-contract form), which required yet another commit cycle (revert of `285e1aa` at `4c5ed3f0`, then data-contract form at `040109ef`). Net: 3 extra commits (`285e1aa`, `4c5ed3f0`, `040109ef`) attributable to one unauthorized design call. Outcome: correct. Process: not clean. Same pattern as S22.1 armor→NONE — Nutts making a correct-but-unilateral design call.

2. **Two GDScript syntax errors reached Boltz review.** `extends Node` (wrong base class) and `:=` type inference on untyped Dictionary are both trivial parse-level bugs that a local GDScript linter or even a dry-run of the file would catch. Boltz REQUEST_CHANGES is the intended safety net — but these weren't design ambiguities, they were parse errors. Recurring pattern: Nutts test-file infrastructure misses (S22.1: missing SPRINT_TEST_FILES registration; S22.2c: wrong base class). Both are in the same category of "test-infrastructure hygiene that Nutts consistently under-checks."

3. **GDD placed in wrong location first.** Initial commit `fdcd9de1` created `godot/design/gdd.md` (new directory). Boltz review noted the spec said `docs/gdd.md` and the relocation happened in a follow-up commit `ef187d58`. The correct behavior was to read the existing repo structure before creating a new directory. `docs/gdd.md` already existed (GDD was there from prior sprints); the right action was to locate and update it, not create a parallel one. The relocation was clean (confirmed: `godot/design/gdd.md` absent from tree post-merge), but it cost a commit and a Boltz annotation.

4. **Optic Playwright smoke verification is post-merge, not pre-merge.** PR #273 body defers Playwright smoke to post-merge (Godot headless constraint). For narrative flow verification, this means the fire-once guard, badge color settle, and modal copy accuracy were not verified in a pre-merge run. Boltz APPROVE on PR #273 proceeded without Playwright evidence. Post-merge CI `Playwright Smoke Tests: success` confirms passing, but the gate ordering is weaker than PR #272 (where Playwright was pre-merge-required per checklist). This is a standing pipeline gap, not specific to S22.2c — the Godot headless constraint in the build env is the root cause.

---

## Carry-forwards

| Issue | Title | Area | Priority | Action |
|---|---|---|---|---|
| (new) | `_check_progression` bronze-count hardcoded as `7` — brittles if Bronze pool changes | `area:game-code` | `prio:low` | File against battlebrotts-v2 |
| (new) | `_apply_badge_color` VFX tween races idle-pulse tween on `_badge.modulate` | `area:ui` | `prio:low` | File against battlebrotts-v2 |
| [#260](https://github.com/brott-studio/battlebrotts-v2/issues/260) | Full league-helper generalization | `area:game-code` | `prio:medium` | Arc F scope (unchanged) |
| [#258](https://github.com/brott-studio/battlebrotts-v2/issues/258) | CI silent-0-assertion gap + Nutts test-infra hygiene | `area:pipeline` | `prio:medium` | Arc D (unchanged) |
| [#265](https://github.com/brott-studio/battlebrotts-v2/issues/265) | Stale weight comments on Silver templates | `area:docs` | `prio:low` | Open from S22.1 (unchanged) |
| [#266](https://github.com/brott-studio/battlebrotts-v2/issues/266) | `bruiser_enforcer` BCard trigger key schema unconfirmed | `area:game-code` | `prio:low` | Open from S22.1 (unchanged) |

**Optic Playwright post-merge:** PR #273 CI confirms Playwright smoke passed post-merge (`success`). No carry-forward item needed for this sprint, but the pre-merge gap is noted above.

---

## KB entry candidates

Five KB candidates flagged by Ett. Evaluations:

### KB-1: Per-league data-driven mechanic pattern ✅ RECOMMEND PROMOTION

**Candidate:** The `REFLECT_DAMAGE_BY_LEAGUE` dictionary + helper pattern as the canonical way to introduce league-scaling of symmetric mechanics.

**Rationale for promotion:** Reusable immediately — Repair Nanites uptime, Overclock cooldown, and any future symmetric mechanic follows the same structure: add a league table in the relevant data file, add a helper, add one read-site change in combat logic, wire `current_league` at construction sites. The GDD §6.4 extensibility language already describes this; a KB entry would codify the code-level pattern with a template. High reuse potential, low amortization cost.

### KB-2: Symmetric-mechanic-scaling lesson ✅ RECOMMEND PROMOTION

**Candidate:** Opponent-only tuning fails when the mechanic is symmetric. S22.2b is the canonical failure-mode example.

**Rationale for promotion:** This lesson has a concrete example with measurable outcomes (S22.2b 3-pass sim gate failure, opp-WR collapse to ~50%). Future Gizmo framing should include a check: "Is this mechanic symmetric? If yes, tuning only opponents will compress the mechanic's design space — lever the mechanic itself." The lesson is generalizable beyond reflect damage to any mechanic where both sides benefit.

### KB-3: Narrative-coupling rule ✅ RECOMMEND PROMOTION

**Candidate:** Any player-side nerf introduced at a league boundary must ship with a modal beat explaining it.

**Rationale for promotion:** This is now GDD §6.4 policy ("Silent nerfs are prohibited") and HCD ruling 2026-04-24 12:14Z. The KB entry would anchor the GDD language to a pipeline check: Gizmo spec for any player-side league-degradation must include a narrative surface spec. High policy value — prevents future "why did my kit get weaker" UX without explanation.

### KB-4: Revert-before-fix pattern ✅ RECOMMEND PROMOTION

**Candidate:** When a feature branch has failed and the failure is causally entangled with multiple design changes, revert cleanly first, then re-implement via a fresh PR.

**Rationale for promotion:** S22.2b → S22.2c demonstrates the value concretely: if S22.2b had remained live and S22.2c was built on top, B1/B2 sim deltas would be uninterpretable (two independent variables — reflect lever + loadout mutations — confounded). The revert-first discipline produced clean measurement baselines and a tractable Boltz review. Worth codifying as a pipeline-level principle.

### KB-5: Meta-pipeline — large spawn truncation workaround ⚠️ RECOMMEND CONDITIONAL

**Candidate:** Opus 4.7 + Sonnet 4.6 both truncate at ~6–10k output tokens on framing/planning spawns. Workaround: decompose into ≤2500-word pieces.

**Rationale:** The truncation pattern is real (Gizmo spawn for S22.2c required 3-piece decomposition; the incomplete parts were saved to workspace memory files). However, the KB entry content is more appropriate for studio-framework issue #57 / battlebrotts-v2#246 than a pattern KB entry. It's an operational workaround, not a design pattern. **Conditional:** Promote to KB only if the studio-framework issue tracker tracks it; otherwise file the issue and leave the KB slot for design patterns.

---

## Grade rationale

### Grade: B+

**S22.1 reference point:** A− (clean content drop, 2 mid-sprint Gizmo reconciles, 1 Boltz REQUEST_CHANGES; all remediations fast and pattern-positive).

**S22.2c comparison:**

The mechanical and narrative content that landed is high quality. The `REFLECT_DAMAGE_BY_LEAGUE` table is clean, well-commented, and correctly extensible. The combat-sim read-site delta is the minimal 1-line change it should be. The narrative modal flow is correct, the fire-once guard is architecturally appropriate, and the league-prefix narrow fix (game_flow) was scoped precisely. GDD §6.4 is substantive and durable.

**Grade drag from A− to B+:**

1. **PR #272 accumulated 12 commits against an ideal of 7–8.** The excess comes from: (a) a GDD location error (godot/design → docs, +1 commit), (b) two GDScript parse-level bugs caught by Boltz (wrong base class, type inference, +2 fix commits), (c) a Nutts T6 scope rework cycle (implement per spec, replace unilaterally, revert on Gizmo ruling, replace per ruling, +3 commits net). The commit history is auditable, but the branch is noisier than S22.1's 7-commit (pre-squash) discipline.

2. **Two parse-level bugs required Boltz REQUEST_CHANGES.** The `extends Node` / `_initialize` issue is a direct recurrence of the test-infrastructure hygiene pattern from S22.1 (where SPRINT_TEST_FILES was omitted). This is the second consecutive sub-sprint where Nutts has shipped a test file with a runner-compatibility error. Boltz caught it both times — process held — but the recurring miss suggests a structural gap in Nutts's test-infrastructure self-review.

3. **Nutts made another unauthorized design call.** T6 fixture replacement without Gizmo routing is the same pattern as S22.1's armor→NONE call. Outcome was directionally correct; process was not. The T6 result was actually better (data-contract form is superior), but the routing gap is a real signal: two consecutive sub-sprints.

**What prevents a lower grade:**
- All Boltz-caught bugs were remediated in a single re-review cycle (tight loop).
- T6 data-contract form is a genuine improvement over the spec, not a regression.
- CI green on all gates at merge.
- Narrative surface landed cleanly (PR #273: 4 commits, clean APPROVE, no amendments).
- Revert PR was correctly structured and cleanly executed.
- The root cause that required S22.2c (S22.2b baseline pollution) was correctly diagnosed and cleanly fixed.
- GDD §6.4 is substantive design documentation — not a placeholder.

**Tiering:**
- S22.1: A− (clean content drop, fast remediation, pattern-positive)
- S22.2c: B+ (clean landing, solid architecture, recurring process gaps in Nutts test-infra and design-authority boundary)

**Arc C sprint streak:** S22.1 (A−) → S22.2c (B+). 

**Arc-intent verdict:** `progressing — S22.2c delivers the mechanical lever + narrative ceremony; S22.3 (progression surfacing: two-surface Silver indicator on ResultScreen + OpponentSelectScreen per S21.4 T3 #108 pattern) remains queued.`

---

## 🎭 Role Performance

**Gizmo:** Shining: Part C revert-rationale was precise — correctly named the confound (two independent variables on one main) and predicted the measurement problem. T6 Option A ruling was the right call: death-before-differentiate is a structural fixture problem, and the data-contract form is strictly stronger as a regression guard. §6.4 GDD language is publication-quality. Struggling: `combat_sim.gd` path spec said `godot/game/` — actual file lives at `godot/combat/`. A single `find .` at spec time would have caught this. Minor, non-blocking. Trend: → (spec quality high; occasional path/coordinate errors remain; the self-check pattern from S22.1 KB is not yet consistently applied).

**Ett:** Shining: Sprint decomposition into 3 PRs (revert / mechanical / narrative) was correct and matched execution exactly. The Piece 4 audit pointer is unusually complete — covers all 12 files, gives explicit carry-forward treatment, and names 5 KB candidates with rationale. Risk register (3 risks + mitigations) was operationally accurate. Struggling: Nothing S22.2c-specific. Trend: → (planning artifact quality continues strong).

**Nutts:** Shining: Feature commits 1–5 (data table, read-site, plumbing, sim harness, unit tests) were clean. The game_flow narrow fix was precisely scoped. Revert commit structure was correct (reverse chronological, individual commits, clear bodies). PR bodies were thorough. Struggling: (1) Wrong base class on test file (`extends Node` instead of `extends SceneTree`) — second consecutive test-runner-incompatibility error. Nutts profile update needed. (2) T6 unauthorized scope rework — second consecutive unilateral design call. The instinct (death-before-differentiate) was correct; the execution (act unilaterally, push the fix) was not. Trend: ↔ (solid feature work, recurring test-infra and design-boundary misses with no visible improvement between S22.1 and S22.2c — profile-level patch warranted).

**Boltz:** Shining: Single REQUEST_CHANGES pass caught both GDScript bugs with exact root causes and copy-paste fixes. The 14-point checklist was fully verified — including the non-obvious demo-site vs production-site distinction on plumbing, and the GDD location check that caught the `godot/design/` mislocation before it shipped. Re-review was fast (Boltz approved 7 minutes after the final commit landed on branch). Assertion-count verification correctly counted T6 loop-body assertions as 3, not 1. Struggling: Boltz APPROVED the initial T6 asymmetric fixture commit (`285e1aa`) before the Gizmo routing. The fixture was a design decision, not a correctness bug — Boltz's checklist is weighted toward structural correctness, not test-design canonicity. Boltz couldn't be expected to independently rule on the fixture shape, but flagging "design decision in a test function — suggest routing to Gizmo" would have been a stronger catch. Trend: ↑ (checklist rigor continuing to improve; one missed escalation-trigger).

**Riv:** Shining: T6 routing to Gizmo was correct — caught that a test-fixture replacement is a design decision, not a bug fix, and escalated appropriately despite Nutts having already committed a replacement. Sub-sprint shape (3 PRs: revert / mechanical / narrative) held the intended sequencing with no out-of-order merges. Struggling: Nothing S22.2c-specific observable. Trend: → (steady orchestration).

**Optic:** Shining: Post-merge `Post Optic Verified check-run: success` on both #272 and #273. Playwright smoke confirmed all narrative gates (fire-once guard, modal copy, badge color, dismiss flow). Struggling: Pre-merge Playwright unavailability (Godot headless constraint) means PR #273 merged without a pre-merge smoke run — the post-merge run is the first gate. This is a standing platform constraint, not Optic behavior, but the gap is real. Trend: → (reliable on available tooling; pre-merge Playwright gap is platform-constrained).

---

## openclaw tasks audit — S22.2c sprint window

Standard sentinel-sweep baseline (stale_running from earlier arcs, delivery_failed pre-existing, inconsistent_timestamps from harness clock skew). No new task health regressions attributable to S22.2c. Active-arc reconciler (studio-framework watchdog) correctly shows S22.2c status `"active - S22.2c running on Option A (player baseline) + narrative beat"` as of arc entry; reconciler should update on audit landing.

---

## Compliance-reliant process detection

### 1. Nutts test-infrastructure hygiene — compliance-reliant (escalating risk)

Nutts must correctly identify the base class and entry-point pattern for headless test files. Two consecutive sub-sprints with test-runner-incompatibility errors (S22.1: missing SPRINT_TEST_FILES; S22.2c: wrong base class). Boltz catches both — process held — but the recurring miss is a pattern, not a one-off.

**Risk: MEDIUM-HIGH** (increasing from S22.1's MEDIUM given recurrence). Structural fix: add a test-infrastructure checklist to Nutts role profile: (a) `extends SceneTree`, (b) `_initialize()` not `_ready()`, (c) `quit()` called, (d) `SPRINT_TEST_FILES` registration confirmed before PR open. Tracked under #258 class.

### 2. Nutts design-authority boundary — compliance-reliant (recurring signal)

Same pattern as S22.1 armor→NONE. Nutts must choose to escalate design decisions rather than act unilaterally.

**Risk: LOW** per-instance (routing fires, outcomes are correct), but the persistence across sprints is a signal that the Nutts profile hasn't been updated. Fix: explicit "when in doubt on fixture shape, armor, chassis, or copy — escalate, do not patch" language in Nutts role profile. KB entry from S22.1 (Pattern 2) was the first note; profile patch is the structural fix. This should have been done post-S22.1 and wasn't.

### 3. Pre-merge Playwright gate for narrative PRs — platform-constrained gap

Playwright smoke for narrative flows requires Godot headless. Current build env doesn't support it pre-merge. Post-merge is the first gate.

**Risk: LOW** for correctness (Playwright passed post-merge). **Risk: MEDIUM** for process confidence (we merge before verifying narrative flow). Structural fix is a CI environment upgrade (Godot headless in build env). Not S22.2c scope.

---

*Audit authored by Specc (`specc-bot`) as part of the BattleBrotts-v2 studio pipeline. For framework details see [`brott-studio/studio-framework`](https://github.com/brott-studio/studio-framework).*
