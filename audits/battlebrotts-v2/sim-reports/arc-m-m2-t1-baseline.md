# Arc M — M.2 T1 Baseline Sim Report

**Date:** 2026-04-30 UTC
**Runs:** 50 pre-tuning (initial) + 50 post-tuning (re-verification)
**Build:** main @ ab8977b8dd4adf5fcd217781e3a88028ef740c29

## Pre-Tuning Results (build @ a8e3ee3, before PR #349)

| Chassis | Win Rate | Wins/Runs | Target | Status |
|---------|----------|-----------|--------|--------|
| SCOUT | 84.2% | 16/19 | 55–70% | ❌ OVER |
| BRAWLER | 87.5% | 14/16 | 45–65% | ❌ OVER |
| FORTRESS | 66.7% | 10/15 | 40–55% | ❌ OVER |

- Parse errors: 0 / 50

All three chassis over-winning T1 — enemy difficulty too low.

## T1 Tuning Applied (PR #349, merged ab8977b8)

- `_baseline_hp_for_tier(1)`: 120 → 150
- `standard_duel` T1 weight: 60 → 45
- `brawler_rush` T1 weight: 10 → 25

## Post-Tuning Results (50-run re-verification, seeds 1–50)

| Chassis | Win Rate | Wins/Runs | Target | Delta from midpoint | Status |
|---------|----------|-----------|--------|---------------------|--------|
| SCOUT | 57.9% | 11/19 | 55–70% | −4.6pp | ✅ IN RANGE |
| BRAWLER | 62.5% | 10/16 | 45–65% | +7.5pp | ✅ IN RANGE |
| FORTRESS | 20.0% | 3/15 | 40–55% | −27.5pp | ❌ UNDER — 20pp below floor |

- Parse errors: 0 / 50

## Comparison: Pre-Tuning vs Post-Tuning vs Target

| Chassis | Pre-Tuning | Post-Tuning | Target | Change |
|---------|-----------|-------------|--------|--------|
| SCOUT | 84.2% | 57.9% | 55–70% | −26.3pp → ✅ IN RANGE |
| BRAWLER | 87.5% | 62.5% | 45–65% | −25.0pp → ✅ IN RANGE |
| FORTRESS | 66.7% | 20.0% | 40–55% | −46.7pp → ❌ UNDER |

## Gate Summary

| Gate | Result | Detail |
|------|--------|--------|
| Gate 1 — Parse errors = 0 | ✅ PASS | 0 errors across 50 post-tuning runs |
| Gate 2 — T1 win rates in range | ❌ FAIL | FORTRESS 20.0% — 20pp below floor (target 40–55%) |

## Verdict

**PARTIAL PASS — NEEDS REVIEW**

Scout and Brawler tuning landed correctly. Fortress over-corrected: PR #349's HP + weight changes pushed Fortress win rate from 66.7% down to 20.0% — significantly below the 40% floor. FORTRESS needs a follow-up tuning adjustment (rate up from 20% to 40–55% range, ~+20–35pp).

M.2 **does not close**. Escalating to Nutts for targeted Fortress re-tuning.
