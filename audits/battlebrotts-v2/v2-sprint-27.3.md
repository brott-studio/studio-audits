# S(I).3 Audit — Arc I: Combat Sim Agent Scaffold

**Sprint:** Arc I S(I).3 (sprint-27.3)
**Arc:** I — Optic Plays The Game
**Pillar:** 3 — Combat sim agent (scaffold)
**PR:** #328
**Merged:** 2026-04-27
**Merge commit:** e6b5792d83e2d36877f7df57b71452f7e2de280f
**Auditor:** Specc

---

## Deliverables

- `godot/tests/auto/sim_single_run.gd` — Single-run sim driver. extends AutoDriver, state-driven screen dispatcher, random chassis + reward picks (seeded RNG), always-accept-loss policy, per-run JSON output to stdout. sim_* prefix keeps out of per-PR gate.
- `godot/tests/auto/sim_runner.sh` — Parallel N-run wrapper. Spawns N godot --headless processes with sequential seeds, collects results to /tmp/sim_results_TIMESTAMP/.
- `.github/workflows/sim.yml` — Separate workflow (NOT verify.yml). Manual dispatch + nightly 3AM UTC cron. Not per-PR.

## CI Results

All green on merge commit e6b5792d: Godot Unit Tests ✅ | Playwright ✅ | Audit Gate ✅ | Optic Verified ✅. sim.yml correctly did not trigger on the PR push.

## Design Verification

- Screen constants match GameFlow.Screen enum (ARENA=5, REWARD_PICK=8, RETRY_PROMPT=9, BOSS_ARENA=10, RUN_COMPLETE=11) ✅
- speed_multiplier re-set inside ARENA/BOSS_ARENA branch every poll cycle ✅
- start_run(chassis, seed) + _start_roguelike_match() for seed propagation ✅
- OS.get_cmdline_user_args() for --seed=N (correct: args after --) ✅
- JSON schema_version=1 with all required fields ✅

## Carry-Forwards to S(I).4

1. sim_runner.sh currently collects raw JSON; S(I).4 adds aggregation (win-rate, death-rate, battles_won distribution per chassis, median run length)
2. S(I).4 adds nightly Markdown report committed to studio-audits
3. Runtime screen-transition timing in headless should be validated on first nightly run — any RUN_START re-entry loop would show as timeout in results
4. Consider SIM_SPEED_MULT tuning: 8.0 is initial value; measure actual wall-clock on first run

## Grade

**A** — Pillar 3 scaffold complete. sim_single_run.gd architecture is correct and extensible for S(I).4 aggregation. All CI green. Design constraints satisfied (nightly-only, not per-PR, correct exclusion from test glob).
