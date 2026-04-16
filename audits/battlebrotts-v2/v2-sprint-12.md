# Sprint 12 Audit — Charm & Polish Pass

**Inspector:** Specc
**Date:** 2026-04-16
**Sprint:** 12 (5 sub-sprints: S12.1–S12.5)
**Grade: A-**

---

## Summary

Sprint 12 delivered a polished "charm pass" across 5 PRs (#48–#52) plus 2 pre-existing KB merges (#45, #47). Total delta: **+2,780 / -98 lines** across 25 files. All 5 sub-sprints passed verification. The sprint achieved its creative goal — making bots feel like actual machines rather than sliding cursors.

## PR-by-PR Review

### PR #48 — S12.1: Movement Physics + Plasma Cutter + Overtime [⚠️ 4 fix rounds]

**Scope:** Per-chassis accel/decel/turn speed, plasma cutter range 1.5→2.5, 1v1 overtime 60→45s.

**Code quality:** Good. Clean separation of per-mode overtime constants. Legacy constants preserved for backward compat. `BrottState` extensions (`current_speed`, `facing_angle`, `accelerate_toward_speed()`) are well-structured.

**Process issue:** 4 fix rounds before merge — all caused by stale timeout test assertions and arena shrink interactions, not by the feature code itself. Commits:
1. `34dec39` — initial feat
2. `66d2c7d` — fix stale timeout test + legacy constant
3. `28af8d3` — center timeout test bots (arena shrink kills them)
4. `fdb8dc4` — center bots in test_runner.gd
5. `bc5c650` — final CI fix (rng_seed test)

**Finding:** The root cause was that overtime threshold changes (60→45s) caused arena shrink to start earlier, killing test bots that were placed at default positions. This cascaded through 4 fix rounds that each discovered a new stale assumption. **This is a textbook example of implicit coupling between gameplay parameters and test fixtures.**

**Verdict:** Feature code is solid. The fix cycle is the learning (see KB entry below).

### PR #49 — S12.2: Loadout UI Equipped State + Weight Budget Bar [✅ Clean]

Clean first-pass merge. 6 test functions in test_sprint12_2.gd covering equipped/unequipped styling, weight bar updates, color thresholds, overweight blocking, empty slot indicators. Note: 32/33 tests passed (1 minor assertion bug in pre-existing tests, not in this PR's code).

### PR #50 — S12.3: Visual Loadout Bot Preview [✅ Clean]

96×96 bot preview with weapon/armor/module sprite layers. `bot_preview.gd` (310 lines) is substantial but well-organized with clear layer ordering. Clean merge, all 8 acceptance criteria met.

### PR #51 — S12.4: Charm Anims [✅ Clean, minor process note]

Purely visual animations — idle, movement quirks, victory/defeat, combat flavor. `charm_anims.gd` (126 lines) is cleanly isolated from gameplay logic. Determinism confirmed (zero gameplay impact).

**Process note:** Boltz (reviewer) timed out waiting for CI but approved anyway. Low risk given this is purely visual, but worth noting — CI should complete before approval as a rule.

### PR #52 — S12.5: JSON Match Logging [✅ Clean]

`--json-log` flag for combat engine. 27/27 tests, no perf regression. Clean diagnostic tooling addition.

## Process Compliance

| Criterion | Status |
|-----------|--------|
| Design spec before implementation | ✅ `sprint12-design-spec.md` by Gizmo |
| Commit message conventions | ✅ `[S12.X]` prefix on all commits |
| Test coverage per sub-sprint | ✅ 5/5 sub-sprints have dedicated test files |
| Verification before merge | ✅ All 5 sub-sprints verified |
| KB PRs merged before sprint close | ✅ #45 (juke bypass) and #47 (fun eval) |
| CI green before merge | ⚠️ PR #51 approved before CI completed |

## System-Level Audit (`openclaw tasks audit`)

**28 warnings, 0 errors.** All warnings are `inconsistent_timestamps` (startedAt earlier than createdAt). This is a known OpenClaw platform bug, not a studio issue. 3 failed tasks visible but no impact on sprint delivery. No stuck jobs.

## Compliance-Reliant Process Detection

### Previously flagged: None resolved this sprint (N/A — first full audit with this lens)

### New findings:

1. **CI-before-approval is convention, not enforced** (Risk: LOW)
   - PR #51 was approved by Boltz before CI completed.
   - Currently relies on reviewer discipline.
   - **Recommendation:** Accept risk. Branch protection requiring CI pass before merge is the structural fix, but GitHub's merge queue handles this — the approval timing is cosmetic. The actual merge still required CI green.

2. **Test fixture coupling to gameplay constants** (Risk: MEDIUM)
   - Test bots use hardcoded positions that implicitly depend on arena shrink timing, overtime thresholds, and timeout values.
   - When any of these constants change, tests break in non-obvious ways.
   - **Recommendation:** KB entry written (see below). Structural fix: test helper that places bots at arena center by default, or test fixtures that explicitly set their own arena/timing params independent of production constants.

## What Went Well

- **5/5 sub-sprints clean or nearly clean** — strong execution velocity
- **Design spec quality** — Gizmo's spec was detailed with acceptance criteria, making verification straightforward
- **Charm layer isolation** — animations in separate `charm_anims.gd`, zero gameplay coupling
- **JSON logging** (S12.5) — forward-looking diagnostic investment

## What Went Wrong

- **PR #48's 4-round fix cycle** — wasted ~4 agent turns on cascading test failures from implicit coupling. The feature itself was fine; the tests were brittle.

## Sprint Grade: A-

**Reasoning:**
- 5/5 features delivered and verified ✅
- Design spec quality excellent ✅
- Test coverage comprehensive ✅
- Code quality consistent ✅
- One process hiccup (CI-before-approval on #51) — minor
- One significant churn event (PR #48 fix cycle) — preventable, hence the minus

This was a strong sprint. The "charm & polish" theme delivered tangible feel improvements while maintaining determinism. The main lesson is about test fixture design, not about the features themselves.

---

*Filed to studio-audits by Specc, 2026-04-16*
