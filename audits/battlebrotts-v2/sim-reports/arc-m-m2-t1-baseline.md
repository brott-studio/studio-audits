# Arc M — M.2 T1 Baseline Sim Report

**Date:** 2026-04-30 UTC
**Runs:** 50 (seeds 1–50)
**Build:** main @ a8e3ee34031e6edbd6b8370827be551e7a7dbfb4
**Runner:** sim_runner.sh (50 parallel runs, seeds 1–50)

## T1 Win Rates

| Chassis | Win Rate | Wins/Runs | Target | Status |
|---------|----------|-----------|--------|--------|
| SCOUT | 84.2% | 16/19 | 55–70% | ❌ OVER |
| BRAWLER | 87.5% | 14/16 | 45–65% | ❌ OVER |
| FORTRESS | 66.7% | 10/15 | 40–55% | ❌ OVER |

All three chassis are over-winning T1 battles. T1 enemy difficulty is too low.

## M.3 Fold-in: Reward Accumulation

- Runs with battles_won >= 2: **16**
- Runs with items acquired (weapons > 1 OR armor > 0 OR modules present): **16/16 (100%)**
- M.3 reward accumulation confirmed working correctly.

## Parse Errors

- Parse errors: **0 / 50**
- All 50 runs produced valid JSON output.

## Chassis Distribution

- SCOUT: 19 runs
- BRAWLER: 16 runs
- FORTRESS: 15 runs

## Raw Results Sample (seeds 1–10)

```
seed 1:  chassis=SCOUT    battles_won=1  terminal=death  loadout_weapons=[4, 0]
seed 2:  chassis=BRAWLER  battles_won=1  terminal=death  loadout_weapons=[2]
seed 3:  chassis=SCOUT    battles_won=9  terminal=death  loadout_weapons=[4, 1, 5, 3, 6, 0]
seed 4:  chassis=SCOUT    battles_won=1  terminal=death  loadout_weapons=[4, 5]
seed 5:  chassis=FORTRESS battles_won=1  terminal=death  loadout_weapons=[4]
seed 6:  chassis=BRAWLER  battles_won=1  terminal=death  loadout_weapons=[2]
seed 7:  chassis=FORTRESS battles_won=2  terminal=death  loadout_weapons=[4, 0]
seed 8:  chassis=FORTRESS battles_won=1  terminal=death  loadout_weapons=[4]
seed 9:  chassis=SCOUT    battles_won=4  terminal=death  loadout_weapons=[4]
seed 10: chassis=SCOUT    battles_won=1  terminal=death  loadout_weapons=[4]
```

## Gate Summary

| Gate | Result | Detail |
|------|--------|--------|
| Gate 1 — Parse errors = 0 | ✅ PASS | 0 errors across 50 runs |
| Gate 2 — T1 win rates in range | ❌ FAIL | SCOUT +14.2pp, BRAWLER +22.5pp, FORTRESS +11.7pp above target ceilings |
| Gate 3 — M.3 fold-in reward accumulation | ✅ PASS | 16/16 multi-battle runs show item acquisition |

## Verdict

**TUNING_NEEDED**

T1 enemy weights are too weak across all chassis. Nutts tuning sprint required to bring T1 win rates into targets:
- SCOUT: reduce from ~84% to 55–70% range (need ~10–30pp harder)
- BRAWLER: reduce from ~87.5% to 45–65% range (need ~25pp harder)
- FORTRESS: reduce from ~67% to 40–55% range (need ~12–27pp harder)

M.3 reward accumulation is confirmed healthy — no standalone M.3 sprint needed.
