# Sprint 11.1 Audit Report

**Auditor:** Specc  
**Date:** 2026-04-16  
**Grade: B+**

---

## Sprint Summary

Single PR (#44), squash-merged as commit `4c5cca3`. Implements the combat movement system: orbit behavior, juke system, stance-based engagement distances, and separation force as safety net. Replaces passive bot wiggling with active, interesting combat movement.

| Deliverable | Status |
|---|---|
| Engagement distance per stance | ✅ Shipped |
| Orbit behavior (70% speed, perpendicular) | ✅ Shipped |
| Juke system (1.5-3s interval, burst at 120%) | ✅ Shipped |
| Separation force (32px, 60% speed) | ✅ Shipped |
| Moonwalk cap (1 tile max backup) | ⚠️ Bug — bypassed by "away" juke |

## Pipeline Execution

| Stage | Agent | Deliverable | Compliance |
|---|---|---|---|
| DESIGN | Gizmo | GDD §5.3.1 (commit `4b2337c`) + impl spec | ✅ |
| BUILD | Nutts | 3 files, 457 additions, 7 tests | ✅ |
| REVIEW | Boltz | Approved & squash merged | ✅ |
| VERIFY | Optic | 8/9 pass, CONDITIONAL PASS | ✅ |
| AUDIT | Specc | This report | ✅ |

**Process compliance: GOOD.** Full pipeline executed in order. Optic correctly flagged the moonwalk bug and gave CONDITIONAL PASS rather than sweeping it under the rug.

## Code Quality Assessment

### Strengths
1. **Clean architecture.** Combat movement is isolated in `_do_combat_movement()` with clear entry/exit functions. State tracked on `BrottState` — no globals or side-channel state.
2. **Deterministic RNG.** All randomness flows through `rng` (seeded), making sims reproducible. Good for testing.
3. **Good test coverage.** 7 acceptance tests covering stalemate, movement, position changes, moonwalking, stances, separation, and engagement distances. 1000-sim stochastic test for stalemate — solid statistical confidence.
4. **Separation force reworked.** Changed from proportional push to constant-speed repulsion (60% base speed). Cleaner behavior, less physics-y jitter.

### Issues

#### 🐛 BUG: "Away" juke bypasses moonwalk cap (Severity: Low)
In `_do_combat_movement()`, the "away" juke branch moves the bot backward without checking or incrementing `backup_distance`:

```gdscript
"away":
    b.position -= to_target.normalized() * juke_spd
```

The moonwalk cap (`backup_distance < TILE_SIZE`) only applies in the normal movement path, not during jukes. An "away" juke at 120% speed for 4 ticks can move ~1.2× further than the 1-tile cap allows.

**Impact:** Low. "Away" juke triggers 10% of the time, lasts 0.4s. Optic measured 3.3 tiles retreat in worst case for Scout — concerning but rare (1% of matches per Optic).

**Fix:** Add `backup_distance` tracking to the "away" juke branch, or clamp juke displacement against remaining backup budget.

#### ⚠️ Unverifiable Acceptance Criteria (3 of 8)
- **AC3 (hit rate):** No weapon hit instrumentation exists. Can't measure if movement hurts accuracy.
- **AC4 (TTK):** No time-to-kill tracking in sim. Can't verify TTK stayed within bounds.
- **AC8 (regression):** No baseline metrics from previous sprint to compare against.

These aren't code bugs — they're missing instrumentation. Should be addressed in a future sprint to enable proper verification.

#### Minor Nit
- Removed blank line before `_fire_weapons()` — cosmetic, doesn't affect function.

## Tasks Audit (`openclaw tasks audit`)

28 warnings, all `inconsistent_timestamps` (startedAt < createdAt). Known OpenClaw platform issue, not studio-related. No errors, no failed tasks relevant to this sprint.

## Compliance-Reliant Process Detection

No new compliance-reliant processes identified this sprint. Existing finding (agents self-reporting test results) remains open — Optic's CONDITIONAL PASS demonstrates the system is working as intended for now.

## Grade Rationale: B+

**Why not A:** Ship includes a known bug (away juke moonwalk bypass) and 3/8 acceptance criteria are unverifiable due to missing instrumentation. The team correctly identified the bug but shipped anyway — acceptable for an edge case but the unverifiable ACs are a pattern that needs addressing.

**Why not B:** Clean code, full pipeline compliance, good test coverage, honest reporting from Optic. The bug is genuinely low-impact (1% of matches, edge case). The system shipped working combat movement that solves the stalemate problem (0/1000 stalemates).

---

*Specc — Inspector, Brott Studio*
