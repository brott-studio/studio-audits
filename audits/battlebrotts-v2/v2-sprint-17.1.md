# Sprint 17.1 — Post-Merge Audit (retroactive)

**Auditor:** Specc (`brott-studio-specc[bot]`, App ID `3444613`)
**Date:** 2026-04-21T07:45Z
**Sprint:** S17.1 (Shop / Loadout / Event UX fixes — arc-opening slice of S17 "Eve Polish Arc")
**Build set:** PRs #157, #158, #159, #160, #161, #162, #163, #164, #165, #167, #168, #170, #171, #172, #174, #175, #176 (17 merged PRs)
**Still open at audit time:** PR #166 (S17.1-003 verify), PR #169 (S17.1-004 verify)
**Verify:** `push: main` Verify runs green across the S17.1 merge sequence; final S17.1 merge commit `9aa7b2a6` (PR #172) landed 2026-04-21T02:17Z with Verify ✅
**Grade:** **B+**

---

## 1. Headline

**S17.1 landed functionally on `main` but the sub-sprint was never formally closed and the audit gate was skipped a second consecutive time.** All six task implementations merged with green CI; scope-gate held perfectly (zero diffs under `godot/combat/**`, `godot/data/**`, `godot/arena/**`, `docs/gdd.md` across the entire build set); the test-runner enumeration gained six new `test_sprint17_1_*` files. But two verify PRs (#166, #169) are still open at audit time, `sprints/sprint-17.1.md` still shows `**Status:** Planning` with every exit-criteria checkbox unchecked, there is no close-out PR, and S17.2 has already begun merging work on `main` (PRs #178, #181, #183). The audit gate added by `studio-framework` PR #12 ("S17.1 is NOT closed until `audits/battlebrotts-v2/v2-sprint-17.1.md` lands on `studio-audits/main`") was breached before it could bite — the pipeline moved past S17.1 without seeking audit. The code is good; the process hygiene is the problem. Not an A.

---

## 2. Meta — retroactive audit, second occurrence

This is a **retroactive post-merge audit**. Specc was not spawned at S17.1 close-out. The sprint loop advanced into S17.2 before the auditor was invoked; HCD noticed at 2026-04-21T07:39Z and spawned this audit manually.

This is the **second consecutive sprint** in which the audit gate was skipped in-sprint and filled after the fact. S16.1 was the first (audit PR #2 on `studio-audits`, 2026-04-20). S17.1 is the second. One instance was a blip; two instances means the close-out checklist item recommended in the S16.1 audit §7.2 has not been absorbed into pipeline practice. Escalated in §7 below.

No blame assigned. Logging the fact.

---

## 3. Summary

**Goal.** Per `sprints/sprint-17.1.md` §"Goal": remove the top Shop / Loadout / Event UX friction points surfaced in the 2026-04-18 playtest, as the arc-opening slice of S17's "convert playable-but-rough into something that feels professional" charter. Six tasks, S17.1-001 through S17.1-006. Scope gate: UX-only — no `godot/combat/**`, `godot/data/**`, `godot/arena/**`, or `docs/gdd.md` edits.

**What happened.** Sub-sprint plan PR #157 merged 2026-04-20T21:28Z. First implementation (S17.1-001, PR #159) merged 15 minutes later at 21:43Z. Final merged artifact (S17.1-005 post-hoc verify, PR #172) landed 2026-04-21T02:17Z. Total elapsed time from plan-merge to last-verify-merge: **4h 49m** across 17 merged PRs. All six task implementations reached `main` with their own test file, a design doc, and (for four of six) a merged verify report. Two verify PRs remain open. No close-out PR was ever opened. S17.2 planning and implementation began while S17.1 was still informally in-flight.

**Outcome.** Six playtest UX complaints addressed at the code level; functional quality appears solid based on merged verify reports for 001, 002, 005, 006 plus the PR bodies on open verify PRs 003/004. Scope gate held — this is the fourth straight sub-sprint (S15.2, S16.1, S16.2, S16.3, now S17.1) with zero gameplay-data drift, a real studio-norm pattern now. But the pipeline's own close-out invariant (audit gate, sprint-doc sealing, exit-criteria checkboxes) was not honored.

**Player POV.** Player-facing changes landed: Shop scroll no longer snaps to top on click, Loadout UI no longer occludes the Shop button at high inventory, Loadout items surface name + description without hover, energy bar has a first-encounter explainer, random-event popup has an always-present skip button and pre-commit item preview, first-run crate popup has contextual framing. Unverified end-to-end in a full playtest — Optic ran automated smoke tests, not a fresh HCD playtest.

---

## 4. Acceptance verification

Each of the 9 exit criteria listed in `sprints/sprint-17.1.md` §"Exit criteria" re-verified against `main` today (HEAD as of 2026-04-21T07:45Z).

### 4.1 [S17.1-001] Shop scroll — PR merged ✅, Playwright test present ✅

- **Design:** PR [#158](https://github.com/brott-studio/battlebrotts-v2/pull/158), merged 2026-04-20T22:21Z (`c4c63bf5`).
- **Impl:** PR [#159](https://github.com/brott-studio/battlebrotts-v2/pull/159), merged 2026-04-20T21:43Z (`be7619c1`).
- **Verify:** PR [#160](https://github.com/brott-studio/battlebrotts-v2/pull/160), merged 2026-04-20T23:02Z (`8819a6a0`). Verify doc at `verify/battlebrotts-v2/s17.1-001.md`.
- **Test file on main:** `godot/tests/test_sprint17_1_shop_scroll.gd` enumerated in `test_runner.gd` line 48. ✅
- **⚠ Order anomaly:** Impl PR #159 merged **38 minutes before** design PR #158. Design-first discipline is a stated S17.1 principle (sprint plan §"Pipeline flow": "Gizmo designs task-by-task → Nutts builds"). On S17.1-001 the order was inverted: Nutts implemented first, Gizmo's spec ratified after. Not fatal — the implementation matches the spec on inspection — but it's a process slip worth naming.

### 4.2 [S17.1-002] Loadout overlap — PR merged ✅, max-inventory snapshot test ✅

- **Design:** PR [#161](https://github.com/brott-studio/battlebrotts-v2/pull/161), merged 2026-04-20T22:22Z.
- **Impl:** PR [#162](https://github.com/brott-studio/battlebrotts-v2/pull/162), merged 2026-04-20T22:18Z.
- **Verify:** PR [#163](https://github.com/brott-studio/battlebrotts-v2/pull/163), merged 2026-04-20T23:07Z. Verify doc + 4 inventory-size screenshots at `verify/battlebrotts-v2/screenshots-s17.1-002/` (inv_0, inv_5, inv_20, inv_50).
- **Test file on main:** `test_sprint17_1_loadout_overlap.gd` enumerated ✅.
- **⚠ Order anomaly (same as 001):** Impl merged 4 minutes before design. Same pattern, less egregious. By S17.1-003 onward the order normalizes (design → impl → verify in every subsequent task). So the anomaly is isolated to the first two tasks — the pipeline self-corrected by task 3.

### 4.3 [S17.1-003] Visible tooltips — PR merged ✅, visual-snapshot test ⚠ (verify PR still open)

- **Design:** PR [#164](https://github.com/brott-studio/battlebrotts-v2/pull/164), merged 2026-04-20T23:00Z.
- **Impl:** PR [#165](https://github.com/brott-studio/battlebrotts-v2/pull/165), merged 2026-04-20T23:17Z. Touches `loadout_screen.gd`, `shop_screen.gd`, adds `test_sprint17_1_visible_tooltips.gd`. 7 files, +372/-24.
- **Verify:** PR [#166](https://github.com/brott-studio/battlebrotts-v2/pull/166) **STILL OPEN** (`mergeable_state: behind`). Body claims ✅ Pass with "Playwright Smoke + Godot Unit Tests green on PR #165 head (`5965d211`)" and "Local AC unit suite: 38/38 passed." But the verify artifact (`verify/battlebrotts-v2/s17.1-003.md`) is **not on `main`** — it exists only on the verify branch.
- **Test file on main:** enumerated ✅. The test passes as part of the main-branch Verify run, so functional coverage is there even without the verify doc merged.
- **Finding:** the exit criterion "visual-snapshot test present" is satisfied at the test-code level but the verify-doc artifact is not on `main`. This is the #1 carry-over process item from S17.1 into S17.2.

### 4.4 [S17.1-004] First-encounter HUD — PR merged ✅, dismissal persistence verified ⚠ (verify PR still open)

- **Design:** PR [#167](https://github.com/brott-studio/battlebrotts-v2/pull/167), merged 2026-04-20T23:23Z.
- **Impl:** PR [#168](https://github.com/brott-studio/battlebrotts-v2/pull/168), merged 2026-04-20T23:37Z. Introduces `godot/ui/first_run_state.gd` autoload, `test_sprint17_1_first_encounter_hud.gd`. Touches `main.gd`, `project.godot` (to register the autoload). 7 files, +428/-0.
- **Verify:** PR [#169](https://github.com/brott-studio/battlebrotts-v2/pull/169) **STILL OPEN** (`mergeable_state: behind`). Body claims ✅ Pass, "All 3 required CI checks green on head SHA (run 24695671027). Local unit suite 26/26 assertions pass — covers AC-1..AC-6 per design §8. **AC-5 pixel-identity co-…**" (truncated). Verify doc not on `main`.
- **Scope note — `project.godot` edit:** The impl touched `godot/project.godot` to register the `first_run_state` autoload. `project.godot` is **not** on the sacred-paths list (sacred = `godot/combat/**`, `godot/data/**`, `godot/arena/**`, `docs/gdd.md`), so this is in-scope. Flagging it for visibility because `project.godot` is engine-config territory and worth naming any time it moves.
- **Finding:** same shape as S17.1-003. Test passes in main Verify, artifact not merged.

### 4.5 [S17.1-005] Random-event popup — PR merged ✅

- **Design:** PR [#170](https://github.com/brott-studio/battlebrotts-v2/pull/170), merged 2026-04-20T23:42Z.
- **Impl:** PR [#171](https://github.com/brott-studio/battlebrotts-v2/pull/171), merged 2026-04-20T23:53Z. Adds skip button + pre-commit item preview to `trick_choice_modal.*`, `shop_screen.gd`. 6 files, +371/-7.
- **Verify:** PR [#172](https://github.com/brott-studio/battlebrotts-v2/pull/172) merged 2026-04-21T02:17Z. **Title explicitly says "post-hoc"** — verify was written after the impl had already landed and after S17.1-006 work was underway. Verify doc + 1 screenshot on main.
- **Test file on main:** `test_sprint17_1_random_event_popup.gd` enumerated ✅.
- **Finding:** "post-hoc" verify is a yellow flag. Verify exists to catch regressions *before* the next task builds on the current one. Post-hoc verify still provides the artifact but loses the gatekeeping function.

### 4.6 [S17.1-006] First-run crate framing — PR merged ✅, non-first-run unchanged ✅

- **Design:** PR [#174](https://github.com/brott-studio/battlebrotts-v2/pull/174), merged 2026-04-21T01:52Z. (Note: PR #173 is unrelated — `docket: Arc Framework Hardening (post-S17)`, still open.)
- **Impl:** PR [#175](https://github.com/brott-studio/battlebrotts-v2/pull/175), merged 2026-04-21T02:07Z. Adds contextual framing to `trick_choice_modal.*`, `test_sprint17_1_first_run_crate.gd`. 5 files, +263/-0.
- **Verify:** PR [#176](https://github.com/brott-studio/battlebrotts-v2/pull/176), merged 2026-04-21T02:11Z. Verify doc on main.
- **Test file on main:** enumerated ✅.
- **Finding:** cleanest task in the sprint — design → impl → verify order, fast turnaround (19 minutes plan-to-verify-merged), verify artifact on main, coordinates with S17.1-004's `first_run_state` autoload (explicit reuse rather than parallel infra — the risk mitigation from sprint plan §Risks worked).

### 4.7 Optic verification doc — no regressions ⚠

- Per-task verify docs exist on main for **4 of 6** tasks (001, 002, 005, 006). Missing on main: 003, 004 (verify PRs still open).
- No aggregate "S17.1 regression sweep" verify doc exists. The sprint plan exit criteria phrased this as "Optic Playwright run confirms no regressions in Shop / Loadout / Event popup screens" — that could be read as per-task or as aggregate. Individual task verify docs claim their slice green, but there is no single document asserting "S17.1 as a whole introduces no regressions." Accepting the per-task reading as partial satisfaction; flagging the aggregate as absent.

### 4.8 Scope-gate verification ✅

Per-PR diff inspection across all 17 merged S17.1 PRs. Files touched span: `sprints/`, `docs/design/`, `godot/ui/`, `godot/tests/`, `godot/main.gd`, `godot/project.godot`, `verify/`.

**Zero files touched under `godot/combat/**`, `godot/data/**`, `godot/arena/**`, or `docs/gdd.md` across the entire build set.**

| PR | Combat? | Data? | Arena? | GDD? |
|---|---|---|---|---|
| #157 plan | ✗ | ✗ | ✗ | ✗ |
| #158 design 001 | ✗ | ✗ | ✗ | ✗ |
| #159 impl 001 | ✗ | ✗ | ✗ | ✗ |
| #160 verify 001 | ✗ | ✗ | ✗ | ✗ |
| #161 design 002 | ✗ | ✗ | ✗ | ✗ |
| #162 impl 002 | ✗ | ✗ | ✗ | ✗ |
| #163 verify 002 | ✗ | ✗ | ✗ | ✗ |
| #164 design 003 | ✗ | ✗ | ✗ | ✗ |
| #165 impl 003 | ✗ | ✗ | ✗ | ✗ |
| #167 design 004 | ✗ | ✗ | ✗ | ✗ |
| #168 impl 004 | ✗ | ✗ | ✗ | ✗ |
| #170 design 005 | ✗ | ✗ | ✗ | ✗ |
| #171 impl 005 | ✗ | ✗ | ✗ | ✗ |
| #172 verify 005 | ✗ | ✗ | ✗ | ✗ |
| #174 design 006 | ✗ | ✗ | ✗ | ✗ |
| #175 impl 006 | ✗ | ✗ | ✗ | ✗ |
| #176 verify 006 | ✗ | ✗ | ✗ | ✗ |

**Scope gate: clean. Fifth consecutive sub-sprint with perfect discipline on sacred paths** (S15.2 → S16.1 → S16.2 → S16.3 → S17.1). This is now a load-bearing studio pattern; new agents should be onboarded assuming this is the norm.

### 4.9 Audit gate — Specc audit on `studio-audits/main` ⚠

This audit, landing now. Merged retroactively. See §2, §7.

---

## 5. Quality observations

### 5.1 Tests

- All 6 new `test_sprint17_1_*.gd` files landed with their respective impl PR. No "we'll add tests next" hand-waves.
- All 6 test files are enumerated explicitly in `test_runner.gd` (lines 48–53) per the S16.1-005 explicit-enumeration pattern. The post-S16 norm holds.
- Every push to `main` during the S17.1 window triggered a Verify run (S16.3's `push: main` trigger is load-bearing here). Every one came back green. No silent-red moments.
- Test thinness caveat: these are unit tests against UI controllers, not end-to-end Playwright runs of a real session. The verify-PR bodies claim Playwright smoke passed on PR heads — trusting that assertion since the CI logs were green, but the merged verify docs don't reproduce the Playwright output, only the unit-suite counts (e.g. "38/38 passed" on #166's body). Adequate for UX-polish work; would want more for behavior changes.

### 5.2 Verification evidence

- **Strong:** screenshots at 4 inventory sizes (inv_0 / inv_5 / inv_20 / inv_50) for S17.1-002 is exactly the right shape for a layout-overlap fix. That's a template for future UI verify docs.
- **Weak:** no aggregate verify doc for the sub-sprint, no fresh playtest. S17.1's whole raison d'être is the 2026-04-18 playtest — closing the loop with a 2026-04-21 re-playtest would have been the cleanest acceptance signal. HCD can decide whether to schedule one separately.
- **Missing on main:** verify docs for S17.1-003 and S17.1-004. PR bodies assert pass, CI backs them, but the artifacts aren't merged. Audit gate cannot claim "verify docs complete" for the sprint until #166 and #169 land.

### 5.3 Design adherence

- **S17.1-004/006 coordination worked.** The risk flagged in sprint plan §Risks ("first-run persistence infra sprawl") was mitigated as intended: S17.1-004 introduced `first_run_state.gd` autoload, S17.1-006 reused it. One system, two consumers. Gizmo and Nutts coordinated across tasks.
- **S17.1-002 ↔ S17.1-003 interaction held.** Visible-by-default tooltips (003) did not re-break max-inventory layout (002). Both pass their respective tests on main.
- **S17.1-001 / S17.1-002 design-after-impl slip.** Flagged in §4.1 and §4.2. On inspection the impl matches the later-merged design, so the design doc was post-facto ratification rather than retroactive rewrite — but the whole point of design-first was to have Gizmo's spec land before Nutts builds. First two tasks of the arc inverted that.
- **S17.1-005 post-hoc verify.** The verify PR title literally says "(post-hoc)." Acknowledged by the role itself.

### 5.4 Sprint-doc hygiene

`sprints/sprint-17.1.md` on main at audit time:
- `**Status:** Planning` (should be `Sealed` or `Closed`).
- All 9 exit-criteria checkboxes are `- [ ]` (unchecked).
- No close-out PR in the build set. S16.1 had PR #127, S16.3 had a sealing commit. S17.1 has neither.
- Carry-forward backlog section is empty — either no carry-forwards surfaced (possible for a tight UX sub-sprint) or none were captured (more likely).

This is the clearest single-file evidence that the close-out step was skipped.

---

## 6. Role performance notes

### 🎭 Role Performance

**Gizmo:** Shining: S17.1-004 design introduced a clean first-run-state autoload that S17.1-006 reused cleanly — the kind of cross-task coordination the sprint plan §Risks section explicitly asked for. S17.1-002 screenshot-based spec (4 inventory sizes) was well-scoped. Struggling: S17.1-001 and S17.1-002 design PRs merged *after* the impl PRs — either Gizmo was reacting to Nutts's implementation rather than leading it, or the design was batched last in a hurry. Trend: →.

**Ett:** Shining: Sub-sprint plan (PR #157) was strong — 6 tasks, clear acceptance, explicit scope gate reference, complexity estimates, risks section that correctly anticipated the S17.1-004↔006 interaction. The plan itself is one of the best-shaped in the S15–S17 range. Struggling: No close-out. `sprint-17.1.md` still reads `Status: Planning` with zero checkboxes ticked. Whoever owns the close-out step (Ett per S16.1 pattern, Riv per arc-level) did not execute it. Trend: ↓ (first time Ett has been flagged on close-out execution).

**Nutts:** Shining: Six implementations delivered in roughly 4.5 hours with green CI and tests landing alongside each. Clean autoload integration for S17.1-004. `trick_choice_modal` refactor handled both S17.1-005 and S17.1-006 without stepping on itself. Struggling: Sprinted ahead of Gizmo on the first two tasks (impl merged before design) — doesn't match the design-first discipline the sprint plan mandates. Trend: ↑ on code quality, → on pipeline discipline.

**Boltz:** Shining: All 17 PRs approved and merged with no scope-gate breaches across the entire build set. That's a non-trivial amount of review throughput in a 4.5-hour window. Struggling: Did not flag the design-after-impl sequencing on S17.1-001/002, and did not flag PR #172's "post-hoc" verify framing at review time. Also did not block the close-out-that-wasn't — although there was no close-out PR to review, so this is more a systemic observation than a Boltz-specific miss. Trend: →.

**Optic:** Shining: Four verify PRs merged (001, 002, 005, 006) with substantive evidence — the 4-size screenshot matrix for S17.1-002 is a high-water mark. Struggling: Two verify PRs still open (003, 004) at audit time. Verify PRs #166 and #169 are `mergeable_state: behind` — they didn't fail, they just weren't rebased and merged before the sprint rolled forward. And the S17.1-005 verify was explicitly post-hoc (PR #172 title). Verify-as-gate requires verify-before-next-task, not verify-after-next-task. Trend: ↓.

**Riv:** Shining: Arc-level orchestration kept S17.1 moving fast — 4.5 hours plan-to-last-merged is efficient. S17.2 kickoff happened smoothly. Struggling: Closed the loop on S17.1 badly. Audit gate skipped (same miss as S16.1). `sprint-17.1.md` never sealed. S17.2 spawned before S17.1 was formally closed. This is the canonical "sprint loop advanced past close-out" failure — the S16.1 audit §7.2 recommended a Specc-audit-existence check at close-out, and that recommendation clearly has not been absorbed. Trend: ↓.

**Patch:** Did not participate in S17.1 (no infra / ops tasks in this sub-sprint). Not graded.

**HCD:** Caught the audit-gate miss at 2026-04-21T07:39Z (~5h after the last S17.1 PR merged, ~2h after S17.2 had already begun shipping code). Spawning this audit manually is the right recovery; but HCD should not be the fallback check on the audit gate — that's a pipeline-internal invariant.

---

## 7. Process notes — audit-gate miss, second instance

**This is the second consecutive sub-sprint to close without a Specc audit in-loop.** S16.1 was the first. The S16.1 audit (§7.2) explicitly recommended:

> add a pre-close-out checklist item to Ett's close-out template and Riv's arc-resumption protocol: "Before closing a sub-sprint, confirm a Specc audit file exists at `audits/<project>/sprint-<N.M>.md` on `main` of `studio-audits`. If not, spawn Specc before close-out PR, not after."

The `studio-framework/PIPELINE.md` update landed in PR #12 (referenced directly in `sprints/sprint-17.1.md` §"Audit gate (HARD RULE)"). The rule is documented. The rule was not followed.

**Severity: elevated.** S16.1 was a single miss. S17.1 makes it a pattern. A "hard rule" that is ignored twice in two sub-sprints is not functioning as a gate — it's functioning as aspirational documentation. Either the gate needs enforcement (e.g. a GitHub Actions check that blocks the S17.2 plan PR from merging until S17.1 audit exists), or the checklist needs to be moved upstream of the actor most likely to skip it.

**Root-cause hypotheses (not conclusive without transcript review):**

1. **S17.1 close-out was never actually performed.** Unlike S16.1 (where a close-out PR #127 existed and sealed the sprint without the audit file), S17.1 has no close-out PR at all. The sprint didn't skip the audit gate at close-out — it skipped close-out itself. S17.2 planning began while S17.1 was informally "done" (all tasks merged) but formally still "Planning."
2. **Arc velocity optimization overran pipeline hygiene.** S17 is explicitly a polish arc with playtest-driven tasks. The instinct to keep momentum (ship the next fix fast) may have outrun the close-out ritual.
3. **The PIPELINE.md hard-rule was known to the plan author (Ett cited it in the sprint plan itself) but not re-invoked by whoever was orchestrating close-out.** Documentation is not automation.

**Remediation (standing recommendation to HCD + The Bott):**

1. **This audit exists now.** S17.2 can continue (it's already in-flight) but should not seal without its own audit.
2. **Strong recommendation: automated audit-gate enforcement.** A GitHub Actions check on any `sprints/sprint-<N+1>.md` PR that fails unless the corresponding `audits/battlebrotts-v2/v2-sprint-<N>.md` exists on `studio-audits/main`. Documentation failed twice in a row. Automation would have caught both.
3. **Ett or Riv should retroactively seal `sprint-17.1.md`** — update `Status`, tick exit-criteria boxes, note carry-forwards (if any). Not part of this audit's scope; flagging for follow-up.
4. **Verify PRs #166 and #169 should be rebased and merged.** Both report pass, both are just "behind." The verify artifacts belong on main for the audit trail to be complete. Even though S17.1's functional work is done, the paper trail is not.

This is the cross-reference moment: S15.2 §5.1.1 flagged ambiguous close-out framing. S16.1 §7 flagged the same. S17.1 §7 (this section) flags it again. **Three sprints, same root-cause family, no systemic fix adopted yet.** Escalate to HCD for a framework-level intervention at the next arc gate.

---

## 8. KB entries worth preserving

No new KB docs were authored during S17.1 (no `docs/kb/*.md` additions in the build set). However, several patterns from S17.1 are worth surfacing as KB candidates for future arcs:

1. **First-run state persistence autoload pattern** — `godot/ui/first_run_state.gd` from S17.1-004. Reused cleanly by S17.1-006. This is a reusable primitive for any future "show on first encounter, persist dismissal" UX work. Candidate: `docs/kb/first-run-state-pattern.md` (recommended for S17.2 or S17.3 to author).
2. **Max-inventory layout regression testing** — the 4-size screenshot matrix (`inv_0`, `inv_5`, `inv_20`, `inv_50`) from S17.1-002 is a strong template for any UI-layout verify. Candidate: `docs/kb/ui-layout-verify-template.md` or absorbed into `docs/kb/ux-vision.md`.
3. **`trick_choice_modal` as shared surface** — both S17.1-005 and S17.1-006 modified it. If future random-event or decision work lands here, there's an implicit extensibility contract worth documenting.

None of these are blockers. Flagging for Ett's next-sprint planning input.

---

## 9. Grade

**B+.**

**Why not A or A−:**
- Audit gate skipped for the second consecutive sub-sprint. A hard rule documented in PIPELINE.md and cited in the sprint plan itself was bypassed. This is a B-grade structural concern.
- `sprint-17.1.md` was never sealed. `Status: Planning` on main at audit time, zero exit-criteria checkboxes ticked, no close-out PR. This is a process regression even from S16.1 (which at least had a close-out PR #127).
- Two verify PRs (#166, #169) still open at audit time. The sprint rolled into S17.2 with verification paperwork literally incomplete.
- Design-after-impl order on S17.1-001 and S17.1-002 breaks the design-first discipline the sprint plan itself mandated.
- S17.1-005 verify explicitly labeled "(post-hoc)."

**Why not B or B−:**
- Scope gate held cleanly across 17 PRs. Fifth straight sub-sprint with zero sacred-path drift. This is genuinely excellent and a real studio-norm pattern.
- All 6 implementations merged with green CI, tests enumerated, functional quality apparently solid (within the limits of automated smoke tests).
- Cross-task coordination on first-run persistence (S17.1-004 ↔ S17.1-006) worked exactly as risk-mitigated in the sprint plan.
- Execution speed was strong — 4.5h from plan-merge to last-verify-merge for 6 tasks across 5 agents.
- The sprint plan itself (Ett's PR #157) is one of the best-structured in the S15–S17 range.

**Net:** code side is A-range. Pipeline hygiene is C+. Average = B+, and I'm not rounding up.

If the audit gate had been honored in-sprint, `sprint-17.1.md` had been sealed, and verify PRs #166/#169 had landed, this would be a straight A. The gap is entirely close-out discipline, not code.

---

## 10. Exit criteria recommendation

**CONTINUE (with caveats).** S17.2 is already in-flight and has been delivering clean code (`[S17.2-002] Wall-stuck` shipped clean per `push: main` Verify). Pausing S17.2 to retroactively repair S17.1 paperwork would be less useful than letting S17.2 continue and enforcing tighter close-out on **that** sprint so the pattern breaks.

**Not HOLD:** functional outcomes of S17.1 are in main and appear correct. Scope gate held. No regressions flagged.

**Not RELEASE:** the sub-sprint is formally not closed. "RELEASE" would require `sprint-17.1.md` sealed, verify PRs merged, exit-criteria ticked. None of that has happened.

**CONTINUE:** run S17.2 to completion, but apply the following three must-do items before S17.2 close-out:

1. **Automated audit-gate enforcement** — CI check blocks `sprint-<N+1>.md` planning PRs until `audits/...sprint-<N>.md` exists on `studio-audits/main`. Framework-level change; owner: The Bott via studio-framework PR.
2. **Retroactive S17.1 close-out** — Ett or Riv opens a PR to update `sprints/sprint-17.1.md`: `Status: Sealed (retroactive)`, tick exit criteria, note that the audit landed retroactively via this Specc PR.
3. **Merge verify PRs #166 and #169** — both are "behind" but passing. Rebase and merge so S17.1's verify artifacts are complete on main.

None of these block S17.2 from continuing. They're end-of-sprint paperwork that should have happened and didn't.

---

## 11. Notes for S17.2

- **Audit gate on S17.2 is non-negotiable.** Third miss in a row would be a systemic pipeline failure, not an incident. Riv should spawn Specc before opening the S17.2 close-out, not after.
- **Close-out PR pattern from S16.1 (PR #127) is the baseline.** Match it: update sprint-doc status, tick boxes, file carry-forwards, seal. A 5-minute PR that locks the sprint.
- **Design-first discipline reset.** S17.2-001 investigation / spec sequencing (PRs #178 → #181 → #183 by glance) looks better-ordered than S17.1-001/002. Hold that line.
- **Verify-before-next-task, not verify-after.** S17.1's "post-hoc verify" and two open verify PRs are symptoms of verify running async from the critical path. Put verify on the critical path.
- **Scope-gate streak at 5 sub-sprints.** Don't break it casually. S17.2's wall-stuck work touches movement code — flag any `godot/combat/**` or `godot/arena/**` drift early, and escalate to HCD if the sub-sprint genuinely needs a sacred-path edit rather than sneaking one in.
- **Consider KB candidates** (§8) during S17.2 planning: first-run-state pattern is ripe for codification while the authoring hands are still on the code.

---

## 12. Gate status

**Sprint 17.1 audit: COMMITTED (retroactive). Gate cleared for S17.2 close-out, conditional on S17.2 honoring its own audit gate in-sprint rather than retroactively.**

Recommendations to HCD + The Bott are in §7 (remediation) and §10 (exit criteria). Most important single action: **automate the audit-gate check.** Documentation has now failed twice in a row.

---

## Appendix A — Key refs

- Sub-sprint plan: [`sprints/sprint-17.1.md`](https://github.com/brott-studio/battlebrotts-v2/blob/main/sprints/sprint-17.1.md)
- Arc brief: [`sprints/sprint-17.md`](https://github.com/brott-studio/battlebrotts-v2/blob/main/sprints/sprint-17.md) ("Eve Polish Arc")
- Build set — merged: PRs [#157](https://github.com/brott-studio/battlebrotts-v2/pull/157), [#158](https://github.com/brott-studio/battlebrotts-v2/pull/158), [#159](https://github.com/brott-studio/battlebrotts-v2/pull/159), [#160](https://github.com/brott-studio/battlebrotts-v2/pull/160), [#161](https://github.com/brott-studio/battlebrotts-v2/pull/161), [#162](https://github.com/brott-studio/battlebrotts-v2/pull/162), [#163](https://github.com/brott-studio/battlebrotts-v2/pull/163), [#164](https://github.com/brott-studio/battlebrotts-v2/pull/164), [#165](https://github.com/brott-studio/battlebrotts-v2/pull/165), [#167](https://github.com/brott-studio/battlebrotts-v2/pull/167), [#168](https://github.com/brott-studio/battlebrotts-v2/pull/168), [#170](https://github.com/brott-studio/battlebrotts-v2/pull/170), [#171](https://github.com/brott-studio/battlebrotts-v2/pull/171), [#172](https://github.com/brott-studio/battlebrotts-v2/pull/172), [#174](https://github.com/brott-studio/battlebrotts-v2/pull/174), [#175](https://github.com/brott-studio/battlebrotts-v2/pull/175), [#176](https://github.com/brott-studio/battlebrotts-v2/pull/176)
- Build set — still open: PRs [#166](https://github.com/brott-studio/battlebrotts-v2/pull/166) (S17.1-003 verify), [#169](https://github.com/brott-studio/battlebrotts-v2/pull/169) (S17.1-004 verify)
- Final S17.1 merge commit: `9aa7b2a6` (PR #172, 2026-04-21T02:17Z)
- Previous audit: [`audits/battlebrotts-v2/v2-sprint-16.3.md`](./v2-sprint-16.3.md) (S16 arc close)
- S16.1 retroactive-audit precedent: [`audits/battlebrotts-v2/v2-sprint-16.1.md`](./v2-sprint-16.1.md) §7

## Appendix B — State snapshot at audit time

| Check | Result | Notes |
|---|---|---|
| Scope-gate: `godot/combat/**` across build set | ✅ EMPTY | 17 PRs, zero touches |
| Scope-gate: `godot/data/**` across build set | ✅ EMPTY | " |
| Scope-gate: `godot/arena/**` across build set | ✅ EMPTY | " |
| Scope-gate: `docs/gdd.md` across build set | ✅ EMPTY | " |
| 6 new `test_sprint17_1_*` files enumerated in `test_runner.gd` | ✅ 6/6 | lines 48–53 |
| `push: main` Verify green on S17.1 merges | ✅ PASS | sampled final merge `9aa7b2a6` and prior |
| Verify PRs merged | ⚠ 4/6 | #166, #169 still open (`behind`) |
| Verify artifacts on main | ⚠ 4/6 | 001, 002, 005, 006 present; 003, 004 absent |
| `sprints/sprint-17.1.md` sealed | ❌ NO | `Status: Planning`, zero boxes ticked |
| Close-out PR | ❌ NONE | No equivalent of S16.1's PR #127 |
| S17.2 already in-flight | ✓ YES | PRs #178, #181, #183 shipping on main |
| Specc audit in-sprint | ❌ NO | This audit is retroactive; second consecutive instance |

---

_Audit complete. 2026-04-21T07:45Z — Specc (retroactive)._
