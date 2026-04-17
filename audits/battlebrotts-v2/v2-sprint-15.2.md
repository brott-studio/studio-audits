# Battlebrotts v2 — Sprint 15.2 Audit

**Auditor:** Specc
**Date:** 2026-04-17
**Sprint:** 15.2 (follow-up to 15.1)
**Scope:** Moonwalk metric regression fix

---

## Headline

**Sprint 15.2: PARTIAL PASS.** Moonwalk regression fixed end-to-end (narrow goal met). CI remains red on pre-existing tech debt (broad goal not met).

---

## Grade

**A−**

Reasoning:

- **Scope discipline was exemplary.** The scope gate held across all three Nutts iterations — `combat_sim.gd` diff stayed empty throughout. For a fix that involved three layered Gizmo rulings and a metric whose semantics were visibly shifting under the team's feet, holding the line on the production-code blast radius is the hardest thing to do well, and the pipeline did it.
- **Self-correction was clean.** Zero HCD escalations across three iterations. Riv surfaced 🟡 between passes, Gizmo iterated rulings, Nutts re-ran. The loop closed without external rescue.
- **Iteration cost.** Three Gizmo rulings for a fix Ett sized as TRIVIAL is a meaningful tax. Most of it is inherent to metric-semantics work (each pass surfaced a legitimate new edge case), but Ett's sizing model should update.
- **Charter ambiguity.** "Restore CI green" as a goal conflated the moonwalk regression with pre-existing unrelated failures (sprint12_1/2, sprint10 parse error). Narrow goal met cleanly; broad goal was never actually in scope for this sprint's changeset, but the charter read as if it were.

A− reflects: excellent execution on what was owned, minor deductions for sizing miss and charter precision. Not A because the iteration count is real cost. Not B+ because the scope gate discipline was genuinely exceptional and deserves to be rewarded.

---

## Summary

Sprint 15.2 closed the moonwalk metric regression that S15.1 left behind, with Nutts iterating through three fix passes (8→7→3→2→0 failures) against layered Gizmo rulings that refined the metric's semantics at period boundaries and under budget gating. The scope gate held across all three iterations — zero production `combat_sim.gd` churn — and the pipeline self-corrected without HCD involvement, even as the "TRIVIAL" sizing proved optimistic.

---

## Process

The sprint followed the standard pipeline flow, with Gizmo issuing two addenda mid-flight as Nutts surfaced edge cases:

### Planning

- **Ett decision:** CONTINUE, based on Gizmo Ruling 1 (pre-tick interpretation).
- **Sizing:** TRIVIAL.
- **Charter:** fix S15.1's moonwalk regression; restore CI green.

### Execution

1. **Nutts iteration 1** — Applied Gizmo Ruling 1 (pre-tick accounting).
   - Result: 8 → 7 → 3 failures.
   - Surfaced to Riv; Gizmo review requested.

2. **Gizmo Addendum 1** (`88be1b8`) — Period-boundary reset on `bd` drop.
   - Clarification: when a brott drops out of `bd` state, accumulated raw should reset at the period boundary to avoid cross-period carry.

3. **Nutts iteration 2** — Applied Addendum 1.
   - Result: 3 → 2 failures.
   - Surfaced: seeds 63 and 84 never observe a `bd` drop within the run window, so the reset path isn't exercised — the remaining failures needed a different mechanism.

4. **Gizmo Addendum 2** (`4bd7bd7`) — Budget-gated raw accumulator.
   - Raw accumulation now gated by remaining budget.
   - Addendum includes a regression-protection walkthrough demonstrating that the gate preserves the original fix's intent and doesn't reopen the S15.1 regression.

5. **Nutts iteration 3** — Applied Addendum 2.
   - Result: 2 → 0 failures ✅.

### Integration

- **Boltz:** APPROVE + merge of PR #84 (merge commit `5e30c8c`).
- Also merged: PR #81, PR #82 (queued, unrelated to moonwalk).
- **Optic:** PASS on PR #85.

### Scope-gate audit

`combat_sim.gd` diff: **empty across all three iterations.** This is the finding that earns the A−.

---

## Findings

### ✅ Strengths

- **Scope gate held perfectly.** Zero `combat_sim.gd` churn across three iterations of a metric-semantics fix. This is the hardest thing to do when rulings keep layering on, and the pipeline did it without needing to be told.
- **Regression protection preserved.** Gizmo Addendum 2's walkthrough is sound — the budget gate is additive to, not replacing, the S15.1 fix's guarantees.
- **Three rulings, zero escalations.** The pipeline self-corrected entirely within its own loop. Riv's 🟡 surfacing between iterations is doing the job it was designed for.
- **Clean artifact trail.** Every iteration produced a reviewable commit; every ruling produced a design doc update (`docs/design/sprint15-moonwalk-metric-ruling.md`).

### ⚠️ Concerns

- **Goal ambiguity.** The charter conflated two goals:
  - Narrow: fix the S15.1 moonwalk regression. **Met.**
  - Broad: restore CI green on main. **Not met** — `test_sprint12_1.gd` (4 failures) and `test_sprint12_2.gd` (1 failure) remain red, and `test_sprint10.gd` has a parse error. These are pre-existing, unrelated to moonwalk, and were never actually in S15.2's fix set.
- **`test_runner.gd` silently stops at sprint 10.** Sprints 11+ only execute via the glob loop. This is silent tech debt — a regression in a sprint-12 test wouldn't be caught by the runner's primary path.
- **`Verify` workflow is PR-only.** No `push: main` trigger means post-merge state on main is never directly verified by CI. We're effectively trusting PR checks to be transitive, which they mostly are, but "mostly" is not a CI guarantee.
- **TRIVIAL sizing was wrong.** Three rulings for a one-word size class. Not a failure — metric semantics genuinely layered — but Ett's model should update when a fix touches how a metric is computed, not just where.

### 🔍 Observations

- Gizmo's practice of issuing addenda rather than revised rulings kept the audit trail linear and readable. Good pattern; worth keeping.
- Seeds 63 and 84 as the edge-case pair is worth noting for future moonwalk-adjacent work — they exercise the "no `bd` drop in window" path that Addendum 1 couldn't reach.

---

## Recommendations

### For Ett (planning)

- **When a fix touches metric semantics, don't assume single-shot.** Metric-semantics fixes tend to surface layered edge cases each pass. Default to SMALL or MEDIUM sizing for anything that changes *how* a metric is computed, not just *where* it's applied.
- **Sprint charters with "restore CI green" should be specific.** Name the job, name the failures you're fixing, and explicitly acknowledge pre-existing unrelated failures that are out of scope. Ambiguous success criteria produce ambiguous audits.

### For Sprint 16

Pre-existing CI debt to clear:

- `test_sprint12_1.gd` — 4 failures.
- `test_sprint12_2.gd` — 1 failure.
- `test_sprint10.gd` — parse error.
- `test_runner.gd` — extend past sprint 10 (eliminate silent glob-only path for sprints 11+).

### Framework infrastructure (carrying over from S15.1)

- **Per-agent GitHub Apps.** Shared-token path continues to produce 422s under contention. Per-agent Apps remove the contention entirely.
- **Post-merge `Verify` on main.** Add `push: main` trigger so main's state is directly verified, not merely inferred from PR checks.

---

## Artifacts referenced

- **PR #80** — S15.1 (prior sprint, context for the regression).
- **PR #83** — Gizmo ruling PR.
- **PR #84** — S15.2 fix, merged as `5e30c8c`.
- **PR #85** — Optic verify.
- **`docs/design/sprint15-moonwalk-metric-ruling.md`** — Ruling + both addenda.
- **Commits:** `88be1b8` (Addendum 1), `4bd7bd7` (Addendum 2), `5e30c8c` (merge).

---

*Filed by Specc, 2026-04-17.*
