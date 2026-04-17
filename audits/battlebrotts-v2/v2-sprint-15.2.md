# Sprint 15.2 — Post-Merge Audit

**Auditor:** Specc
**Date:** 2026-04-17T19:10Z
**Merge:** PR #84, merge commit `5e30c8c` on `main`
**Verification:** PR #85 — Optic, PASS (0/100 reproduced, no regressions)
**Scope:** Test-metric correctness fix. `combat_sim.gd` diff vs pre-S15.2 main: **EMPTY** across 3 iterations.

---

## 1. Headline

**Grade: B+ (narrow goal PASS, broad-goal ambiguity unresolved).** Sprint 15.2 achieved its narrow objective cleanly: the `test_away_juke_cap_across_seeds` violation arc closed 7 → 3 → 2 → 0 over three iterations, zero production-code lines in `combat_sim.gd` were touched, and the original S11.1 regression protection was preserved (Gizmo's walkthrough, verified empirically). Scope gate discipline was exemplary — Boltz enforcement + Gizmo self-awareness + Nutts restraint kept the fix confined to the test's measurement metric across three design addenda. However, if the sprint's charter is read as "CI is green on `main`" (a defensible reading, given S15.1's framing), the bar is **not** met: pre-existing failures in `test_sprint12_1.gd` (4), `test_sprint12_2.gd` (1), and `test_sprint10.gd` (parse error) still red the `Godot Unit Tests` job. Narrow reading → A-. Broad reading → C. Splitting the difference at B+, and flagging the ambiguity as the single most important framework question coming out of this sprint.

---

## 2. Summary

**Goal.** Per Ett's plan: close CI health by applying Gizmo's ruling on the `to_target` sampling semantics, sized TRIVIAL. SN-103 (test change) + SN-104 (verify + merge choreography).

**What actually happened.** The "trivial test change" was layered: the failing metric had nested semantics — pre-tick vs post-tick sampling × rolling vs per-period accumulation × raw-distance vs budget-gated measurement. Each Gizmo ruling was correct on its face, but resolving one layer exposed the next. Three iterations of Nutts-applies → violations-drop → residual-seeds-surface → Gizmo-addendum landed the fix in a clean arc: **8 → 7 → 3 → 2 → 0**. Critically, across all three iterations, `combat_sim.gd` was never touched — the entire fix lived in the test harness. Boltz approved and merged PR #84 as `5e30c8c`, also clearing housekeeping PRs #81 (Optic S15.1 verify) and #82 (Specc S15.1 KB). Optic verified on PR #85: 0/100 reproduced deterministically, no regressions, scope gate held. Riv surfaced 🟡 after Gizmo Addendum 1 didn't close the gap (3 seeds remaining) — correct escalation signal before spawning the 3rd ruling.

**Outcome.** The S11.1 moonwalk regression is closed. Test metric now correctly distinguishes intended motion from tick-artifact motion via a budget-gated raw accumulator. Production movement code is unchanged end-to-end. CI `Godot Unit Tests` job remains red on pre-existing tech debt unrelated to this sprint.

**Player POV.** No change. Pure test-correctness work.

---

## 3. Process

### 3.1 Pipeline flow

```
Ett    → CONTINUE, S15.2, TRIVIAL sizing, plan SN-103 + SN-104.
Nutts  → merges PR #83 (Gizmo Ruling 1 doc).
         iter-1: pre-tick to_target sampling applied. 7 → 3.
         Surfaces: 3 seeds still violate, bd drops don't reset run.
Gizmo  → Addendum 1 (commit 88be1b8): reset backup_run when bd drops
         (period boundary).
Nutts  → iter-2: applies reset. 3 → 2.
         Surfaces: seeds 63, 84 — bd pins at cap without dropping.
Riv    → surfaces 🟡 (gap not closing after 2 rulings, before 3rd).
Gizmo  → Addendum 2 (commit 4bd7bd7): budget-gated raw accumulator
         (gate on bd < TILE_SIZE; freeze when capped).
         Walkthrough proves original S11.1 protection preserved.
Nutts  → iter-3: applies gate. 2 → 0 ✅. PR #84 ready.
Boltz  → APPROVE + merge PR #84 as 5e30c8c.
         Also merges housekeeping #81 (Optic S15.1) + #82 (Specc S15.1 KB).
Optic  → PASS verified on PR #85. 0/100, no regressions,
         scope gate confirmed (combat_sim.gd diff empty).
Riv    → spawns Specc (this audit).
```

### 3.2 Self-correction — scope gate held across 3 iterations

The most important process artifact of this sprint. Each Gizmo addendum could have been a scope-expansion vector: "just patch the simulation to not enter this edge case" was a real option at every step. Instead:

- **Gizmo** framed every addendum as a *measurement* correction, never a *motion* correction, and proved (in Addendum 2's walkthrough) that the S11.1 regression detector still trips on the original regression pattern.
- **Boltz** enforced the scope gate on review — approved only when the diff confirmed `combat_sim.gd` untouched.
- **Nutts** applied each ruling narrowly and surfaced residual seeds honestly rather than sneaking a "small" sim tweak in to close the gap.

Three iterations, three opportunities to break scope, zero breaches. This is the mirror image of S15.1's wrong-target issue: there, the plan named a dead code path and Nutts correctly refused to fabricate; here, the plan named a live test and the team correctly refused to stray into production code. Both are scope-discipline wins from different angles.

### 3.3 Self-correction — Riv's 🟡 surface before the 3rd ruling

After Addendum 1 only dropped 3 → 2 (and on the same broad seed profile, not new failures), Riv surfaced 🟡 **before** dispatching Gizmo for Addendum 2. This is the correct escalation pattern: iteration-count is a leading indicator that a "trivial" fix has non-trivial structure. Surfacing at iter-2 gave HCD visibility without blocking progress; no page, no interruption, but the signal was on the board. Pattern to preserve.

### 3.4 Escalation discipline

- Gizmo self-escalated twice (Addendum 1, Addendum 2) instead of insisting the first ruling should hold.
- Boltz's merge window was held closed until the 0/100 bar was actually met — no "good enough" pressure.
- Riv's 🟡 surface was proactive, not reactive to a complaint.
- Zero HCD pages across three iterations. Same pattern as S15.1. Two sprints in a row matches → this is now the studio's default mode, not an exception.

### 3.5 Artifact quality

- **Gizmo Ruling 1 + Addendum 1 + Addendum 2:** Each is a standalone design document that records the semantics question, the ruling, and (for Addendum 2) a walkthrough proving the pre-existing regression detector still works. Durable; future moonwalk questions will refer to these as the canonical semantics reference.
- **PR #84 body:** Clean arc narrative with iteration-by-iteration violation counts. Honest about the three-ruling cost.
- **PR #85 (Optic verify):** Explicit confirmation that `combat_sim.gd` diff is empty vs pre-S15.2 main. This is the artifact that makes the scope-discipline claim falsifiable. Adopt as convention: every test-only fix sprint should include a production-code diff report in verify.
- **Housekeeping roll-up:** Boltz merged #81 + #82 alongside #84. Correct batching — reduces PR drift without conflating unrelated work.

---

## 4. Findings

### 4.1 What went right

1. **Scope gate held 3/3 iterations.** `combat_sim.gd` untouched. This is the headline process win. Frame it, write it into the patterns KB, reference it whenever anyone proposes a "quick sim tweak" to dodge a metric question.
2. **Violation arc closed cleanly.** 8 → 7 → 3 → 2 → 0. Monotonic, no regressions introduced by any iteration.
3. **Gizmo's Addendum 2 walkthrough.** Proving the S11.1 regression detector still catches the original regression is the correct burden of proof when changing a test metric. Adopt as convention: **changes to regression-guard metrics must ship with a proof the guard still fires on its original target.**
4. **Riv's 🟡 surface at iter-2.** Surfaced before the 3rd ruling, not after the sprint closed. Leading-indicator escalation, exactly right.
5. **Zero HCD pages, 3 iterations deep.** Consistent with S15.1. The pipeline handled a legitimately hard problem (nested semantics) without demanding HCD time.
6. **Housekeeping cleared alongside merge.** PRs #81 + #82 merged with #84. No backlog drift.

### 4.2 What went wrong (or: flagged for attention)

1. **Goal ambiguity — "CI green" is under-defined.** The critical framing issue of this sprint.
   - **Narrow reading:** "fix the S11.1 moonwalk regression test." **MET** ✅.
   - **Broad reading:** "make `Godot Unit Tests` CI job pass on `main`." **NOT MET** ❌. Pre-existing failures remain: `test_sprint12_1.gd` (4 assertions: Scout 0→max timing, Scout stop time, Plasma Cutter range, 2v2 match length), `test_sprint12_2.gd` (1: Plasma Cutter + Plating weight), `test_sprint10.gd` (parse error). The `|| exit 1` glob loop in the workflow bails on the first failure, so downstream tests may also not run.
   - Neither reading is "wrong." Ett's plan language supports the narrow reading; the S15.1 → S15.2 charter framing suggests the broad one. **The sprint cannot be graded higher than B+ without resolving which reading governs.** This is an Ett/HCD call, not Specc's.

2. **Ett's TRIVIAL sizing undersold iteration count.** A "trivial test change" that needed three Gizmo rulings and three Nutts iterations is not trivial. The *per-iteration* work was small, but the *sprint aggregate* was medium. Sizing should price in expected iteration count on design-sensitive test-metric fixes. Recommend SMALL-M as the default floor for "test metric correctness" sprints that touch regression-guard semantics.

3. **Layered semantics weren't surfaced at plan time.** Gizmo's first ruling was correct. It was also incomplete — the metric had three layers (sampling-phase × period-accumulation × budget-gating) and the first ruling only addressed the first layer. A pre-plan semantics audit (listing every axis of the measurement) would have flagged this. This is a Gizmo-authoring discipline recommendation, not a blame point — the pipeline handled it correctly reactively.

4. **Tech debt carried forward.** Same list as S15.1, untouched:
   - `test_sprint12_1.gd` (4 fails), `test_sprint12_2.gd` (1 fail), `test_sprint10.gd` (parse error) — silent-green-where-red under the `|| exit 1` glob.
   - `test_runner.gd` only covers up to sprint 10.
   - `Verify` workflow is PR-only; no `push: main` trigger.
   - `arena/arena_renderer.gd`: warnings-as-errors warning.
   - Shared-token 422 pattern (KB exists from S15.1).

   S15.1 recommended these. S15.2 did not take them. If the broad-goal reading governs, these are now **the** blocker and must be S16 scope.

5. **No production code means no playtest signal.** Pure test fix. Boltz and Optic are both signing off on "no regression," but a broader-than-unit-test sanity pass wasn't run. Low risk given the empty `combat_sim.gd` diff, but worth noting: if a future sprint ships a test-only fix that *does* touch production, the verify protocol needs a playtest gate, not just a unit-test pass.

---

## 5. Recommendations

### 5.1 For S16 (next sprint)

1. **Resolve the "CI green" ambiguity first, scope second.** Before Ett plans S16, Riv or HCD should explicitly rule: does "CI green" mean "the one regression we introduced is fixed" (narrow) or "`Godot Unit Tests` job passes on `main`" (broad)? This determines whether S16 is a normal feature sprint or a tech-debt sprint.
2. **If broad reading governs:** S16 is a tech-debt sweep.
   - Fix or re-baseline `test_sprint12_1.gd` (4 assertions).
   - Fix or re-baseline `test_sprint12_2.gd` (1 assertion).
   - Fix `test_sprint10.gd` parse error (Godot 4.4 strict-type).
   - Extend `test_runner.gd` to cover through sprint 14.
   - Replace the `|| exit 1` glob with a fail-safe loop that reports every failure before exiting non-zero.
3. **If narrow reading governs:** S16 returns to feature work, and tech debt stays on the backlog with an explicit "we chose not to fix this" note appended to `docs/kb/troubleshooting/silent-green-tests.md` (or equivalent).

### 5.2 Framework-level

1. **Size floor for regression-guard metric fixes: SMALL-M, not TRIVIAL.** Any sprint that changes the semantics of a regression-guard test (i.e., a test whose job is to detect a specific past regression) should be sized SMALL minimum, with explicit expectation of ≥2 design-ruling iterations. TRIVIAL sizing on S15.2 wasn't wrong in spirit but set a false expectation for iteration count.
2. **Regression-guard invariance proof.** Any change to a regression-guard test must ship with a walkthrough (Gizmo Addendum 2 is the canonical example) showing the guard still fires on its original target regression. Without this, a "fix" can silently neuter the guard.
3. **Scope-gate diff report in verify.** For any sprint whose plan declares a scope gate ("test-only," "docs-only," "no production code"), Optic's verify report should include an explicit diff summary proving the gate held. PR #85 did this for `combat_sim.gd`. Codify as convention.
4. **Riv's 🟡 surface at iteration N.** Surface yellow to HCD when a "trivial" sprint enters its 2nd unplanned iteration. Not a page — a visibility signal. S15.2 did this correctly; write it into Riv's playbook so it's systematic, not instinctive.
5. **Layered-semantics pre-plan audit for Gizmo.** Before issuing a design ruling on a measurement metric, list every orthogonal axis of the measurement (sampling phase, accumulation window, gating condition, tie-breakers). One addendum cycle is acceptable; three suggests the initial audit missed axes that were visible up front.

---

## 6. KB entries (created this audit)

Written to `brott-studio/battlebrotts-v2` on branch `kb/s15-2-specc-entries`:

- **`docs/kb/patterns/layered-design-rulings.md`** — Recognizing when a "trivial fix" hides nested design questions. Documents the S15.2 arc (3 rulings, 3 iterations, nested sampling × accumulation × gating semantics) and the addenda pattern. Heuristics for Gizmo: list every orthogonal axis of a measurement before issuing a ruling. Heuristics for Ett: size test-metric fixes at SMALL-M floor, not TRIVIAL.
- **`docs/kb/patterns/scope-gate-enforcement.md`** — Cross-role collaboration pattern (Boltz enforcement + Gizmo framing + Nutts restraint) that kept `combat_sim.gd` untouched across 3 iterations of a moonwalk fix. Canonical template for test-only or docs-only sprints. Includes verify-report convention (explicit production-code diff summary).
- **`docs/kb/troubleshooting/ci-goal-ambiguity.md`** — Narrow-vs-broad goal framing when a sprint charter is "CI green." Uses S15.2 as the worked example: narrow reading passes, broad reading fails, both are defensible. Decision tree for Ett/Riv: name the reading at plan time, and if "CI green" is the charter, define which CI job and which tests.

PR: (see §8 Appendix A for URL once opened.)

---

## 7. Role Performance Review

### 🎭 Role Performance

**Gizmo:** Shining: Three rulings, each correct on its face, with Addendum 2 including an empirical proof that the S11.1 regression detector still fires on its original target. Framed every addendum as *measurement* not *motion*, which was the scope-gate linchpin. Trend: ↑. Struggling: The first ruling was incomplete — the metric's layered structure (sampling × accumulation × gating) was visible at plan time to a sufficiently careful semantics audit. Three rulings instead of one is expensive. Framework recommendation in §5.2.5 addresses this.
**Ett:** Shining: Plan shape was correct (test change, not production change). SN-103 + SN-104 split kept test work and merge choreography clean. Trend: →. Struggling: TRIVIAL sizing was wrong for the actual iteration count. Second sizing miss in two sprints (S15.1 dead-target, S15.2 undersized iteration). Pattern worth watching — recommend the sizing-floor rule in §5.2.1.
**Nutts:** Shining: Three iterations, three honest surfaces of residual seeds. No scope creep into production code even when it would have closed the gap faster. Debug-harness reuse from S15.1 paid off in iteration speed. Trend: ↑.
**Boltz:** Shining: Enforced the scope gate on review each iteration. Batched housekeeping PRs (#81 + #82) alongside the feature merge (#84) — reduces drift. Held the merge window until 0/100 actually. Trend: ↑.
**Optic:** Shining: Verify report includes the explicit `combat_sim.gd`-diff-is-empty confirmation, which is the falsifiable form of the scope-gate claim. Recommend adopting as a convention (see §5.2.3). Trend: ↑.
**Riv:** Shining: 🟡 surface at iter-2 was the right proactive move. Spawn order (Nutts → Gizmo → Nutts → Gizmo → Nutts → Boltz → Optic → Specc) was clean, no dropped balls. Zero HCD pages on a 3-iteration sprint. Trend: ↑. Struggling: Did not flag the "CI green" ambiguity at sprint entry — this sprint inherits S15.1's framing and neither Riv nor Ett re-asked the question. Not a miss so much as a systemic gap; §5.1.1 addresses.

---

## 8. Gate status

**Sprint 15.2 audit: COMMITTED. Gate cleared for S16 — pending the goal-ambiguity resolution in §5.1.1.**

Narrow-goal work is complete. Broad-goal work (tech debt sweep) is queued if selected.

---

## Appendix A — Key refs

- Merge commit: `5e30c8c` (PR #84)
- Housekeeping merges: PR #81 (Optic S15.1 verify), PR #82 (Specc S15.1 KB)
- Gizmo rulings: PR #83 (Ruling 1 doc), commit `88be1b8` (Addendum 1), commit `4bd7bd7` (Addendum 2)
- Verify PR: #85 (Optic, PASS)
- Previous audit: `audits/battlebrotts-v2/v2-sprint-15.1.md`

## Appendix B — Test state at merge

| Suite | Result | Notes |
|---|---|---|
| `test_sprint11_2.gd :: test_away_juke_cap_across_seeds` | 100/100 | **0 violations** ✅ (was 7 at S15.1 close) |
| `test_sprint11_2.gd :: test_away_juke_capped_at_one_tile` | pass | ✅ |
| `combat_sim.gd` | untouched | **diff vs pre-S15.2 main: EMPTY** across 3 iterations ✅ |
| `test_sprint12_1.gd` | 4 fail | **pre-existing**, silent-green-where-red |
| `test_sprint12_2.gd` | 1 fail | **pre-existing**, silent-green-where-red |
| `test_sprint10.gd` | parse error | **pre-existing**, Godot 4.4 strict-type |
| `test_runner.gd` | covers ≤ sprint 10 | **pre-existing gap** |
| `Godot Unit Tests` CI job (main) | RED | bails on first pre-existing failure via `\|\| exit 1` glob |

Arc of violation count: **8 → 7 → 3 → 2 → 0** (S15.1 close → Nutts iter-1 → iter-2 → iter-3).

---

_Audit complete. 2026-04-17T19:10Z — Specc._
