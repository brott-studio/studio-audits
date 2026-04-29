# Sprint 28.6 Audit — J.5.2 Fortress T1 Fix

**Sprint:** J.5.2  
**PR:** #338 — [sprint-28.6] J.5.2: Fortress T1 HP buff + T1 weight rebalance + sim REWARD_PICK fix (#314)  
**Status:** ✅ COMPLETE  
**Date:** 2026-04-29  
**Closes:** #314

## Summary

J.5.1 fixed Scout (~50% WR) and Brawler (~33% WR) but left Fortress unchanged at 0% win-rate due to a name mix-up in prior playtest feedback (HCD had Brawler/Fortress names inverted). J.5.2 corrects this with two surgical changes.

## Root Cause

- Fortress HP unchanged at 330 while Scout/Brawler got +30-31% in J.5.1
- T1 `glass_cannon_blitz` encounter (2× Railgun+Minigun Scout enemies kiting at 12 tiles) = near-instant death for Fortress (60px/s, 0 dodge, Defensive stance) before any reward picks
- Fortress dies in 74 ticks (~7.4 seconds) — cannot close to Plasma Cutter range (2.5 tiles) before being deleted

## Changes

### A. Fortress HP: 330→450 (+36%)
`godot/data/chassis_data.gd`

Fortress is the slowest chassis with 0 dodge chance. Scout/Brawler received +30-31% in J.5.1; Fortress needed a larger absolute bump because it cannot evade. At 450 HP, Fortress survives long enough to reach engagement range or wait for overtime arena shrink.

### B. T1 encounter weight rebalance
`godot/data/opponent_loadouts.gd`

| Archetype | Before | After |
|-----------|--------|-------|
| standard_duel | 50 | 60 |
| glass_cannon_blitz | 15 | 5 |
| small_swarm | 15 | 15 (unchanged) |
| large_swarm | 10 | 10 (unchanged) |
| brawler_rush | 10 | 10 (unchanged) |

`glass_cannon_blitz` at T1 is fundamentally mismatched against pre-reward-pick builds. This is a **permanent balance decision** — T1 is the onboarding tier; extreme kite-sniper encounters belong at T2+.

### C. Sim REWARD_PICK crash fix
`godot/tests/auto/sim_single_run.gd`

Arena match_over `_ticks_remaining` 60→120 (covers 1s real-time transition timer at 8x sim speed). REWARD_PICK branch now retries 5× with 20-tick grace before hard-failing. Fixes 7/20 parse errors from prior sim runs.

### D. Test assertion updates
- `test_sprint4.gd`: Fortress HP assertion 330→450
- `test_s28_1_t1_weights.gd`: glass_cannon_blitz 15→5, standard_duel 50→60

## DoD Results

| Gate | Target | Result | Status |
|------|--------|--------|--------|
| Fortress WR | ≥30% | 42.9% | ✅ PASS |
| Scout WR | ≥30% | 57.1% | ✅ PASS |
| Brawler WR | ≥30% | 33.3% | ✅ PASS |
| Parse errors | 0/20 | 0/20 | ✅ PASS |
| AutoDriver | 4 flows green | 4 flows green | ✅ PASS |
| Issue #314 | Closes | CLOSED | ✅ PASS |

## Carry-Forwards

None. All 3 chassis now above 30% WR floor. Arc J balance objective achieved.

## Grade

**A** — All DoD gates passed, root cause correctly identified and fixed, no scope creep.
