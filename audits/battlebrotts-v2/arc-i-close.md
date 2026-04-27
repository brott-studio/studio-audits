# Arc I Close Audit — "Optic Plays The Game"

**Arc:** I — Optic Plays The Game
**Started:** 2026-04-27
**Closed:** 2026-04-27
**Auditor:** Specc

---

## Sub-sprint summary

| Sub-sprint | Sprint # | PR | Merged | Grade | Description |
|---|---|---|---|---|---|
| S(I).1 | sprint-27.1 | #326 | 2026-04-27T20:07Z | A | AutoDriver base class + chassis-pick flow + CI gate |
| S(I).2 | sprint-27.2 | #327 | 2026-04-27T20:37Z | A | reward-pick, run-end, settings AutoDriver flows |
| S(I).3 | sprint-27.3 | #328 | 2026-04-27T21:09Z | A | Combat sim agent scaffold + parallel runner |
| S(I).4 | sprint-27.4 | #329 | 2026-04-27T21:26Z | A | Sim aggregator + dashboard slot |
| S(I).5 | sprint-27.5 | #330 | 2026-04-27T21:47Z | A | bb_test JS bridge (DebugTestBridge autoload) |
| S(I).6 | sprint-27.6 | #331 | 2026-04-27T22:04Z | A | Playwright chassis-pick spec + Web Debug CI |
| S(I).7 | sprint-27.7 | #332 | 2026-04-27T22:17Z | A | Playwright reward-pick spec + production grep check |

## Pillar completion status

| Pillar | Status | Evidence |
|---|---|---|
| Pillar 1: Native auto-driver | ✅ COMPLETE | 4 user flows, per-PR gate, <15s/flow |
| Pillar 2: Web-export drive | ✅ COMPLETE | bb_test bridge + chassis-pick + reward-pick specs |
| Pillar 3: Combat sim agent | ✅ COMPLETE | sim_single_run.gd + aggregator + nightly workflow |

## Grade A acceptance criteria (from arc brief)

**Pillar 1:** Four user flows CI-gated. Deliberate regression in `_on_chassis_picked` fails harness in <10s. ✅

**Pillar 3:** Combat-sim agent runs nightly, emits aggregate stats to studio-audits. Balance flags when chassis win_rate <30%/>70% with ≥5 runs. ✅

**Pillar 2:** bb_test bridge live in debug-export builds, stripped from production (grep check verified). Chassis-pick AND reward-pick user flows gated in build-and-deploy.yml. ✅

## Arc grade: **A**

All three pillars shipped. Per arc brief: "Pillar 1 alone is ~70% of bug-class coverage" — all three layers now live. S(I).8 (flake tuning) remains optional: trigger if post-merge flake rate >5% on the bb_test Playwright specs.

## S26.8 regression coverage

The original S26.8 incident: typed-array silent crash on web export, Optic passed because it only checked `<canvas>` presence. Post-Arc-I:
- **Godot unit tests** (Pillar 1): would catch the logic half (chassis-pick handler broken)
- **bb_test Playwright spec** (Pillar 2): would catch the web-export half (in_arena never becomes true → timeout → fail)
- **Combat sim nightly** (Pillar 3): would surface if a build regression causes >70% run-timeout-rate

The assumption "green CI = the game works" is now substantiated.
