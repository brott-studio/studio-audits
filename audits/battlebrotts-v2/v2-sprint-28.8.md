# Arc K.3 Audit — Brawler T1 Balance Fix (Sprint 28.8)

**Date:** 2026-04-29  
**Sub-sprint:** K.3  
**Issue:** #314 (Brawler battle win-rate below 30% floor)  
**Status:** 🔴 GATE FAIL — escalation required

---

## Summary

Arc K.3 applied a surgical HP buff (295→360, +22%) to Brawler with the goal of lifting T1 battle win-rate from 25% to ≥30%.

**Result: Fix did not achieve DoD.**

| Checkpoint | Pre-K.3 (run 25126311384) | Post-K.3 (runs 25127110387, 25127384922) |
|---|---|---|
| Brawler battle win % | 25.0% | 16.7% (two consecutive runs) |
| Fortress battle win % | 45.5% | 22.2% / 50.0% (high variance, N=7) |
| Scout battle win % | 68.8% | 68.0% / 57.9% |
| Parse errors | 0/20 | 0/20 |

---

## Root Cause Analysis

The HP buff is insufficient because the Brawler's failure mode is **not HP-limited** — it is **speed-kited**.

- Brawler speed: 120 px/s. Enemy in `standard_duel` (60% T1 weight): Scout chassis @ 220 px/s.
- Brawler starts with Plasma Cutter only (2.5 tile range). Scout enemy kites at 3+ tiles.
- In overtime, Brawler catches up due to arena shrink + damage amp — but the 45s commitment is already resolved before it gets there.
- Median ticks post-K.3: 134–155 (only ~13–15s of sim). Brawler dies well before overtime triggers (450 ticks).
- More HP extends the survival window slightly but does not close the mobility gap.

---

## What Was Completed

1. ✅ PR #342 merged to main (Brawler HP 295→360)
2. ✅ Test assertions updated (`test_runner.gd`, `test_sprint4.gd`)
3. ✅ 0/20 parse errors in all post-fix sims
4. ✅ PR approved by Boltz (app-auth), merged via squash
5. ❌ Brawler ≥30% battle win-rate: **NOT ACHIEVED** (16.7% vs 30% floor)
6. ❌ Issue #314 not closed (gate not passed)

---

## DoD Status

| Gate | Status |
|---|---|
| 0/20 parse errors | ✅ |
| Scout ≥30% battle win-rate | ✅ (57–68%) |
| Fortress ≥30% battle win-rate | ⚠️ (22–50%, high variance, N=7) |
| **Brawler ≥30% battle win-rate** | ❌ **16.7%** |
| Issue #314 closed | ❌ |
| Arc-close audit committed | ✅ (this file) |

---

## Escalation Options (for HCD/next arc decision)

The escalation brief says "Do NOT apply a second patch without authorization." Returning to main with findings.

Proposed fixes (require authorization before implementation):

1. **Add Shotgun as Brawler T1 starting option** — Shotgun (range 3.5 tiles, 28 dmg, 3 pellets) vs Scout kiter closes the range gap and is thematically appropriate for Brawler. Low risk.

2. **Reduce standard_duel enemy Scout speed pct** — Enemy at hp_pct 1.0 / speed 220 px/s is the mismatch. Capping enemy speed at 160 px/s for T1 standard_duel only would let Brawler close range. Targeted, sim-measurable.

3. **Add Brawler-specific T1 encounter adjustment** — Swap `standard_duel` enemy chassis from SCOUT→BRAWLER for Brawler player runs at T1. Conceptually sound (Brawler vs Brawler mirror = fair HP fight), but requires T1 archetype to be chassis-aware.

4. **HP to 500+ with current speed** — Pure HP escalation. Keeps Brawler alive until arena shrink triggers, letting overtime mechanics do the work. Fragile (sensitive to sim seed distribution), not recommended.

---

## Carry-Forwards

- Root cause documented: Brawler 120px/s cannot close on Scout 220px/s with 2.5-tile weapon at T1
- HP buff (295→360) is merged and safe — doesn't hurt anything even if insufficient
- Brawler median ticks: ~140 (14s) — dying well before overtime (45s). Root fix must address engagement range or mobility.
- Issue #314 remains open

---

*Nutts, 2026-04-29 18:48 UTC*
