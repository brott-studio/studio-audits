# Arc K Close Audit — "T1 Chassis Balance: Brawler Fix"

**Arc:** K — T1 Chassis Balance: Brawler Fix
**Started:** 2026-04-28
**Closed:** 2026-04-29
**Status:** ✅ CLOSED — All DoD criteria met
**Auditor:** Specc

---

## Background

Arc K launched to resolve issue #314 ([playtest 2026-04-27] T1 swarm encounters too fast vs fresh chassis). Arc J halted with 0% run win-rate across all chassis. K rebuilt from there, fixing T1 opponent speed, then Brawler HP, then identifying the root cause: a weapon-mobility mismatch.

## Sub-sprint summary

| Sub-sprint | Sprint # | PR | Grade | Description |
|---|---|---|---|---|
| K.1 | sprint-28.5 | #338 | B | T1 opponent speed 220→180px/s to reduce kiting (reverted — changed opponent identity, wrong fix) |
| K.1 revert | sprint-28.6 | #339 | A- | Reverted speed change; restored opponent authenticity |
| K.2 | sprint-28.7 | #337* | A- | Brawler HP 225→295 (+31%) — partial improvement |
| K.3 | sprint-28.8 | #342 | A- | Brawler HP 295→360 (+22%) — still 16.7% win-rate; HP insufficient alone |
| K.4 | sprint-28.9 | #343 | A | Brawler T1 starting weapon → Shotgun; closes #314 |

*Note: #337 was the Arc J.5 Sprint-28.7 Brawler HP PR, carried forward as K.2 context.

## Root cause analysis

Brawler at 120px/s vs Scout-chassis enemy at 220px/s: Brawler **cannot close the gap**. Plasma Cutter is a mid-range weapon (projectile speed 500px/s, assumed ~4-5 tile effective range) that requires positioning Brawler never achieves. HP buffs (K.2, K.3) kept Brawler alive longer but didn't fix the fundamental engagement failure.

**K.4 fix:** Shotgun (3-tile range, 5 pellets × 6 damage = 30 burst, fire rate 1.5/s) rewards and incentivizes aggressive close-range play. When Brawler closes, Shotgun wins the engagement decisively.

## Sim results (K.4, run 25130426413 — 20 runs, seed auto)

| Chassis | Runs | Battle win % | Pre-K.4 baseline |
|---|---|---|---|
| **Brawler** | 4 | **55.6%** ✅ | 16.7% (K.3) |
| Fortress | 8 | **46.7%** ✅ | 22–50% (within variance) |
| Scout | 8 | **61.9%** ✅ | 57–68% (within variance) |
| ALL | 20 | 55.6% | — |

**Parse errors:** 0/20 ✅  
**AutoDriver 4 flows:** green (CI Verify pass) ✅

## Code changes (PR #343)

- `godot/game/run_state.gd`: per-chassis starter weapon assignment
  - Brawler (chassis 1) → `SHOTGUN` (WeaponData.WeaponType.SHOTGUN == 2)
  - Scout/Fortress → `PLASMA_CUTTER` (WeaponData.WeaponType.PLASMA_CUTTER == 4) [unchanged]
- `godot/tests/test_s26_1_starter_weapon.gd`: updated assertions to reflect per-chassis weapon start; added K.4 T2 checks

## DoD verification

1. ✅ Parse errors: 0/20
2. ✅ Scout 61.9% ≥30%, Fortress 46.7% ≥30%, Brawler 55.6% ≥30%
3. ✅ AutoDriver 4 flows green (CI Verify pass on PR #343)
4. ✅ Issue #314 closed
5. ✅ This file: `audits/battlebrotts-v2/arc-k-close.md`

## Carry-forwards

- None from this arc. All 3 chassis within acceptable T1 balance range.
- Monitor Brawler battle win-rate in nightly sim — 55.6% on 4 runs is small sample; flag if it drifts below 30% over next week.

## Grade: A

Correct root cause identified after two HP iterations confirmed HP alone was insufficient. Weapon fix was surgical (2 files, 15 lines), fully covered by existing test regression suite. No regressions introduced.
