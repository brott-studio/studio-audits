# v2-sprint-M.1 Audit

**Sprint:** M.1
**Sub-sprint:** M.1
**PR:** #348 (`sprint-m.1` → `main`)
**Merge commit:** `a8e3ee34031e6edbd6b8370827be551e7a7dbfb4`
**Date:** 2026-04-30 UTC
**Grade:** A

---

## Scope

Arc M was triggered by the 2026-04-29 3AM nightly sim reporting 0% win rate and parse errors. M.1's mandate was:

1. **Triage** — determine whether the nightly regression was caused by a new bug or a timing artifact (fixes merged after the nightly ran).
2. **Defensive hardening** — apply a targeted null-guard to `reward_pick_screen.gd` to eliminate any remaining parse-error risk from unsafe dict access.
3. **Docs sync** — align the GDD §13.4 T1 archetype weight table with the actual live code values.

---

## Root Cause Finding

The 2026-04-29 3AM nightly sim ran **before** two critical fixes had been merged:

- **K.2** (headless timer race fix) — merged 2026-04-29 after the nightly window
- **K.4** (Brawler Shotgun starter weapon fix) — merged 2026-04-29 after the nightly window

Both K.2 and K.4 were the actual root cause of the 0% win rate and parse errors. The nightly's bad results were a timing artifact: it ran against the pre-fix `main`. No new bugs were introduced by L.3 (the prior sprint).

**M.1 outcome:** Confirmed regression was already resolved by the time Arc M was scoped. M.1 added a defensive null-guard that makes the code resilient to future missing-key scenarios regardless.

---

## Implementation

### Code Changes

1. **`reward_pick_screen.gd`** — Changed direct dict access to `.get(key, {})` null-guard for description lookup. Specifically: description retrieval now uses `.get()` with a safe default instead of bare bracket access. `add_item()` and `btn.pressed.connect()` were intentionally left untouched (no behavioral change to reward flow).

2. **`docs/gdd.md §13.4`** — T1 archetype weight table synced to actual code values:
   - `standard_duel`: 40 → 60
   - `glass_cannon_blitz`: 15 → 5
   - `brawler_rush`: 20 → 10

### Gate Status (Optic)

| Gate | Description | Result |
|------|-------------|--------|
| Gate 1 | 5-seed sim (parse errors + win rate) | **PASS** — 0/5 parse errors; 3/5 runs with `battles_won ≥ 1` |
| Gate 2 | Godot Unit Test suite | **PASS** — all tests green on `a8e3ee3` |
| Gate 3 | `add_item()` contract | **INFO** — reward picks applied correctly; armor acquired in seed 12345, modules in seed 12347 |
| Gate 4 | Deploy | **PASS** — site deployed at 04:46:52 UTC (≤2 min post-merge) |

All hard gates (1, 2, 4) passed. Gate 3 INFO is expected behavior confirmation, not a failure.

---

## Quality

- **Review cycle:** 1 cycle — Boltz APPROVE, all checklist items passed.
- **Scope adherence:** Tight. No scope creep; only the null-guard and docs sync were in-scope and both landed.
- **Regressions:** None. Sim win rate confirmed healthy (3/5 seeds), test suite clean.
- **Risk:** Low. The null-guard is a pure defensive addition with no behavioral side effects; the GDD change is documentation-only.

---

## Carry-forwards

- **#346 stat delta** — still in backlog; earmarked for M.6. No action needed in M.1.
- No new carry-forwards introduced by M.1.

---

## Grade: A

M.1 delivered on all three objectives: confirmed the regression was a timing artifact (not a new bug), hardened the reward screen against future null-key errors, and synced the GDD to live code. All gates passed in 1 review cycle with no regressions. Scope was clean and narrow. No issues requiring carry-forward.
