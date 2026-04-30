# v2-sprint-M.2 Audit

**Sprint:** M.2
**Sub-sprint:** M.2
**PRs merged:** #349 (`sprint-m.2` → `main`)
**Merge commit:** `ab8977b8dd4adf5fcd217781e3a88028ef740c29`
**Date:** 2026-04-30 UTC
**Grade:** B

---

## Scope

T1 baseline restoration — 50-run sim validation with tuning pass after pre-tuning rates exceeded targets across all three chassis archetypes. Goal: bring Scout, Brawler, and Fortress T1 win rates into their respective target bands.

---

## Findings

### Pre-tuning (50-run sim, pre-PR #349)

All three chassis over-target before tuning:

| Chassis  | Win Rate | Target  | Status |
|----------|----------|---------|--------|
| Scout    | 84%      | 55–70%  | ❌ Over |
| Brawler  | 88%      | 45–65%  | ❌ Over |
| Fortress | 67%      | 40–55%  | ❌ Over |

Parse errors: 0/50 ✅

All archetypes were over-performing at T1, indicating the baseline config was too generous (low HP + high standard_duel weight made combat resolve too quickly in favor of the attacker).

### T1 Tuning Applied (PR #349)

Gizmo-specified adjustments targeting normalized T1 win rates:

| Parameter         | Before | After |
|-------------------|--------|-------|
| Baseline HP       | 120    | 150   |
| standard_duel wt  | 60     | 45    |
| brawler_rush wt   | 10     | 25    |

Intent: increase HP floor to extend fight duration, reduce standard_duel weight to lower Scout's auto-win rate, increase brawler_rush weight to push Brawler toward more decisive confrontations at appropriate rates.

### Post-tuning (50-run sim, post-PR #349)

| Chassis  | Win Rate | Target  | Status |
|----------|----------|---------|--------|
| Scout    | 57.9%    | 55–70%  | ✅     |
| Brawler  | 62.5%    | 45–65%  | ✅     |
| Fortress | 20.0%    | 40–55%  | ❌ Under (over-corrected) |

Parse errors: 0/50 ✅
M.3 fold-in (reward accumulation): PASS ✅

Scout and Brawler landed cleanly within their target bands. Fortress collapsed from 67% to 20% — 20pp below the 40% floor.

---

## Root Cause of Fortress Over-Correction

The HP increase from 120 → 150 (25% increase) disproportionately penalizes the Fortress chassis, which is a lower-DPS archetype built around durability and sustained damage rather than burst. At 150 HP baseline:

- Scout and Brawler (higher burst DPS) can still finish fights within their encounter windows.
- Fortress cannot accumulate enough damage to trade effectively before fight resolution, causing it to lose engagements it would have won at the lower HP baseline.

Additionally, the standard_duel weight reduction (60 → 45) removed Fortress's primary favorable encounter type. Fortress is not well-served by brawler_rush encounters, which favor high-DPS close-range archetypes (Brawler, and to a lesser extent Scout). The net effect: Fortress lost its combat pathway while Scout and Brawler retained theirs.

---

## Quality

- **Review cycle:** PR #349 merged with CI passing. No test failures, no parse errors in 50-run post-tuning sim.
- **CI:** Green on merge.
- **Scope discipline:** PR was tightly scoped to T1 parameter tuning only. No scope creep.
- **M.3 fold-in:** Reward accumulation check passed alongside M.2 validation — no regressions introduced.

Deduction from Grade A: Fortress T1 win rate out of range post-tuning. The tuning correctly diagnosed overperformance across all archetypes but did not anticipate the DPS-scaling asymmetry that would cause Fortress to collapse. A chassis-aware tuning model (or a smaller HP delta tested incrementally) would have caught this.

---

## Carry-forwards

1. **M.2b (Fortress T1 fix):** Fortress T1 win rate at 20% requires targeted tuning. Do NOT touch Scout/Brawler parameters — both are in range. Candidate levers:
   - Introduce a Fortress-favored T1 encounter type (e.g., defensive_hold or ranged_skirmish) that rewards Fortress's durability profile.
   - Reduce HP_PCT scaling for burst-DPS archetypes specifically, rather than applying a flat HP increase to all.
   - Equip Fortress with a better-fit T1 starting weapon (Shotgun favors Brawler in close-range; Fortress may need a different weapon archetype).
   - Gizmo to spec the tuning approach before Nutts implements.

2. **#346 (stat delta):** Still in backlog. Targeted for M.6.

---

## Grade: B

Scout and Brawler T1 win rates restored to target (57.9% and 62.5% respectively). Parse errors 0/50. Reward accumulation (M.3 fold-in) confirmed passing. Fortress over-corrected to 20% — requires a follow-up sprint (M.2b) before T1 balance is complete. Grade A withheld because one of three chassis is materially out of range and requires rework.
