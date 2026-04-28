# Audit: BattleBrotts v2 — Sprint 28.1 (Arc J, Sub-Sprint J.1)

| Field         | Value |
|---------------|-------|
| **Arc**       | J |
| **Sub-Sprint**| J.1 (sprint-28.1) |
| **PR**        | [#333 — \[sprint-28.1\] Battle pacing fix + sim screen-state fix (#314)](https://github.com/brott-studio/battlebrotts-v2/pull/333) |
| **Merge commit** | `661f82e8118a8c0df4ee8e2344a36861290e1538` |
| **Merged at** | 2026-04-28T03:21:24Z |
| **Grade**     | **A−** |
| **Issue ref** | #314 (open — awaiting sim histogram confirmation in J.4) |

---

## What Landed

### SI1-001 · Sim screen-state fix (`godot/game_main.gd`)
Added guard in `_start_roguelike_match()`: before setting `in_arena = true`, the code now checks
`if game_flow.current_screen == GameFlow.Screen.RUN_START` and advances the screen to
`GameFlow.Screen.ARENA`. Without this, the sim hung indefinitely (20/20 timeouts at 250 s
pre-J.1). Post-J.1: 20/20 complete in ≈36 s. Test coverage: `test_sim_screen_state.gd`.

### SI1-002 · T1 baseline HP bump (`godot/data/opponent_loadouts.gd`)
`_baseline_hp_for_tier(1)` raised from **80 → 120**. Goal: T1 battles should last 15–40 s;
prior value produced fights that ended too quickly for meaningful pacing decisions.
Test coverage: `test_s28_1_t1_hp_baseline.gd`.

### SI1-003 · T1 archetype weight rebalance (`godot/data/opponent_loadouts.gd`)
`ARCHETYPE_WEIGHTS_BY_TIER[1]`: `standard_duel` 40 → **55**, `small_swarm` 30 → **15**.
Shifts T1 matchups toward duel-style opponents to stabilise timing variance.
Test coverage: `test_s28_1_t1_weights.gd`.

### SI1-004 · GDD documentation update (`docs/gdd.md`)
Added **T1 Battle Timing Target** subsection to §13.3. Documents the 15–40 s target window
and rationale for the HP/weight changes, keeping design intent discoverable.

### Test infrastructure
`test_runner.gd` updated to register all three new test files. Tests are unit-level and
verify the data constants directly (HP value, weight table, screen-state transition logic).

---

## Verification Gates

| Gate | Description | Status | Notes |
|------|-------------|--------|-------|
| **Gate 1** | Sim histogram (T1 battle duration distribution) | ⏳ PENDING | Sim hang resolved (20/20 complete, 36 s avg). Blocked by `sim_aggregate.py` parse error: Godot engine console text prepended to JSON output files causes `json.load()` to fail. T1 stat extraction deferred to J.4. See carry-forward CF-J1-001. |
| **Gate 2** | AutoDriver chassis-pick smoke test | ✅ PASS | Exit 0, 2 s. No regressions in chassis selection path. |
| **Gate 3** | CI green (Verify + Build & Deploy + Optic Verified) | ✅ PASS | All three CI jobs green on merge commit `661f82e`. |
| **Gate 3e.5** | Deploy freshness check | ✅ PASS | Last-Modified `2026-04-28T03:23:04Z` — deployed ~2 min post-merge, within expected window. |
| **Gate 4** | Issue #314 closed | ⏳ DEFERRED | Issue left open; closure gated on Gate 1 confirmation in J.4. |

---

## Grade Rationale

**A−** — Three of four substantive gates pass outright (AutoDriver, CI, deploy). Gate 1 (sim
histogram) is *structurally unblocked* — the underlying sim hang is fixed — but a tooling
defect (`sim_aggregate.py` JSON parse error) prevents statistical confirmation. Because the
root cause is in the aggregation script rather than the game code, and because the sim
completion time dropped from timeout to 36 s, the sprint outcome is treated as substantially
complete. Grade is A− rather than A to reflect the open measurement gap. Full A available
after CF-J1-001 is resolved in J.4.

---

## Carry-Forwards

| ID | Item | Target | Owner |
|----|------|--------|-------|
| **CF-J1-001** | Fix `sim_aggregate.py` to strip/skip Godot engine console preamble before `json.load()`. Confirm T1 battle duration histogram falls in 15–40 s window. Close issue #314. | J.4 | Eng |

---

## Learning Extractions

### KB-J1-A · Godot CLI output contamination pattern
When invoking Godot headless for simulation output, engine diagnostic lines (version banner,
scene load messages, GPU info) are written to stdout ahead of any `print()` JSON payload.
Scripts consuming that output must either: (a) strip lines until the first `{` or `[`
character, (b) redirect engine output to stderr via `--quiet` flag or `OS.set_stdout()`,
or (c) write JSON to a separate file rather than stdout. Failing to handle this causes
silent `json.load()` failures that look like sim crashes rather than parse errors.
**Applies to:** any Godot headless pipeline (sim runners, test harnesses, batch exporters).

### KB-J1-B · Screen-state guard pattern for deferred arena entry
When a game-flow screen machine can be in multiple entry states at the moment a match
starts (e.g. `RUN_START` vs direct `ARENA`), the match-init function must normalise the
screen state before setting arena flags. Omitting the guard causes the sim loop to wait
for a screen transition that never fires, producing an indefinite hang rather than a
fast-fail error. Pattern: always assert-and-advance screen state at the top of any
function that assumes a particular screen context.
