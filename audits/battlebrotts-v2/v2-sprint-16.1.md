# Sprint 16.1 — Post-Merge Audit (retroactive)

**Auditor:** Specc
**Date:** 2026-04-20T14:55Z
**Sprint:** S16.1 (Test suite cleanup + quarantines)
**Build set:** PRs #89, #90, #91, #92, #125, #126, close-out #127 — all merged 2026-04-17
**Close-out commit on `main`:** `0267b71` (PR #127)
**Verify:** Optic V1–V6 all ✅ (per S16.1 close-out in `sprints/sprint-16.md`)
**Grade:** **A−**

---

## 1. Headline

**S16.1 exit criteria HOLD on `main` as of 2026-04-20.** All six tasks landed, the scope gate held (zero `godot/combat/**` edits across the S16.1 build set), the quarantine/skip-with-reason helper is in place and logs the three combat-side carry-forwards verbatim in CI, and `test_runner.gd` now explicitly enumerates all sprint 10+ test files with the shell-glob loop removed from `verify.yml`. One process flag: **S16.1 shipped without a Specc audit** — the pipeline's audit gate was skipped at close-out and is only being filled retroactively now at S16 arc resumption. The code is clean; the gate violation is the pipeline concern that pulls this off a straight A.

---

## 2. Summary

**Goal.** Per arc plan in `sprints/sprint-16.md` §S16.1: get the Godot Unit Tests suite green on a dummy code-path PR, with every failing test either fixed (test-side) or quarantined via `skip-with-reason` (combat-side). Six tasks S16.1-001 through S16.1-006, strict scope gate on `godot/combat/**`.

**What happened.** All six tasks merged cleanly on 2026-04-17 in under 70 minutes (PR #89 merged 18:46 UTC → close-out PR #127 merged 19:55 UTC). S16.1-001 and S16.1-002 were pure test-data / parse fixes. S16.1-003 triaged the Plasma Cutter fire-at-range failure as scaffolding drift and fixed it test-side; the coupled movement+range "approach tick" invariant was explicitly moved to carry-forward (item A) rather than fixed in scope. S16.1-004 added a minimal 13-line `TestUtil.skip_with_reason` helper and quarantined the three real combat-side regressions. S16.1-005 replaced the fragile `for f in ... || exit 1` glob in `verify.yml` with a 20-entry explicit `SPRINT_TEST_FILES` array in `test_runner.gd`, aggregating per-file exit codes without short-circuiting. S16.1-006 landed GDD §3.2 range correction, the `arena_renderer.gd` warning fix, and surfaced the Minigun fire-rate canon mismatch as 🟡 rather than silently editing balance data.

**Outcome.** Godot Unit Tests job is green on `main` and on the dummy code-path PR verified by Optic. The three quarantined combat regressions are preserved as visible canaries with `SKIP:` lines printed every CI run. The fragile shell-glob pattern that silently hid failures for sprints is gone. Five process/infrastructure carry-forward items surfaced during the sprint and are now filed as GitHub Issues per the new convention (see §6).

**Player POV.** No change. Pure test + CI plumbing.

---

## 3. Acceptance verification

Each of the 6 exit criteria in `sprints/sprint-16.md` §"S16.1 exit criteria" was re-verified against `main` today (2026-04-20, HEAD `cccf534`), not merely against PR descriptions.

### 3.1 Criterion 1 — All six tasks landed on main ✅

| Task | Commit | PR | Merged |
|---|---|---|---|
| S16.1-001 Plating weight | `da09699` | [#89](https://github.com/brott-studio/battlebrotts-v2/pull/89) | 2026-04-17T18:46Z |
| S16.1-002 test_sprint10 parse fix | `9fcd439` | [#90](https://github.com/brott-studio/battlebrotts-v2/pull/90) | 2026-04-17T18:53Z |
| S16.1-003 fire-at-range triage | `3726f8e` | [#91](https://github.com/brott-studio/battlebrotts-v2/pull/91) | 2026-04-17T19:03Z |
| S16.1-004 combat-side quarantine | `ddc3b57` | [#92](https://github.com/brott-studio/battlebrotts-v2/pull/92) | 2026-04-17T19:23Z |
| S16.1-005 explicit enumeration | `36e64f8` | [#125](https://github.com/brott-studio/battlebrotts-v2/pull/125) | 2026-04-17T19:35Z |
| S16.1-006 docs + warning | `f1362d6` | [#126](https://github.com/brott-studio/battlebrotts-v2/pull/126) | 2026-04-17T19:41Z |
| S16.1 close-out | `0267b71` | [#127](https://github.com/brott-studio/battlebrotts-v2/pull/127) | 2026-04-17T19:54Z |

All present on `main`; verified via `git log --oneline` on the freshly cloned repo.

### 3.2 Criterion 2 — Dummy code-path PR shows `Godot Unit Tests` ✅

The `Godot Unit Tests` check on PR [#92](https://github.com/brott-studio/battlebrotts-v2/pull/92) (head `7ce9524`) is the first S16.1 PR that triggered a code-path run post-quarantine and is [green](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24582700945/job/71884376438). PRs [#125](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24583116144/job/71885806200) and [#126](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24583378142/job/71886715950) are also green.

PRs #89/90/91 show `Godot Unit Tests: failure` on their head commits — this is **expected and correct**: those PRs shipped before S16.1-004 landed the quarantines, so the four pre-existing combat-side failures (Scout 0→max, Scout decel, Plasma Cutter @ 2.6 tiles pre-test-fix, 2v2 timeout) still tripped the suite. Verified the failure signature in PR #89's [job log](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24581198014/job/71879201317) — the 4 failures match the expected quarantined set exactly; no new breakage was introduced. From #92 onward the suite is clean.

(PR #127 is doc-only and correctly skipped the Godot Unit Tests check via `paths-ignore`. No `push: main` verification run exists yet — that is S16.3 scope, not S16.1.)

### 3.3 Criterion 3 — Skip reasons visible in CI log ✅

Confirmed by reading the Godot Unit Tests job log for PR #92 ([runs/24582700945/job/71884376309](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24582700945/job/71884376309)). Every S16.1-004 skip prints verbatim:

```
SKIP: test_scout_time_to_max — real regression: brott_state.accelerate_toward_speed — Scout 0→max expected ~0.33s, currently ~0.40s (out-of-scope for S16, see godot/combat/brott_state.gd) — carry-forward to future gameplay sprint (see sprints/sprint-16.md)
SKIP: test_decel_to_stop — real regression: brott_state.accelerate_toward_speed — Scout decel-to-stop expected ~0.25s, currently ~0.30s (out-of-scope for S16, see godot/combat/brott_state.gd) — carry-forward to future gameplay sprint (see sprints/sprint-16.md)
SKIP: test_timeout_2v2_at_120s — real regression: combat_sim.gd overtime/SD plumbing — 2v2 match ends at 100s instead of running to 120s timeout (out-of-scope for S16, see godot/combat/combat_sim.gd) — carry-forward to future gameplay sprint (see sprints/sprint-16.md)
```

All three carry-forwards #1, #2, #4 from the combat-regression table are covered. Carry-forward #3 (fire-at-range) was triaged test-side in S16.1-003 and restored to passing; the approach-tick invariant is a new item (A) tracked as an issue (see §6). Skip helper: `godot/tests/test_util.gd` lines 11–13.

### 3.4 Criterion 4 — `test_runner.gd` explicit enumeration ✅

`godot/tests/test_runner.gd` lines 22–43 contain a 20-entry `const SPRINT_TEST_FILES` array enumerating every sprint-10-and-up test file:

```
test_sprint10, test_sprint11, test_sprint11_2, test_sprint12_{1..5},
test_sprint13_{2..10} (incl. 13_8_modal_hardening + 13_8_toast),
test_sprint14_1, test_sprint14_1_nav
```

Cross-checked against `ls godot/tests/test_sprint*.gd | grep -v .uid` — every sprint-10+ file on disk is enumerated. Sprints 3/4/5/6 files are present on disk and **intentionally not** in the array (carry-forward item B; the header comment on lines 16–22 explicitly documents why, pointing to the scope-gate constraint that S16.1-005 must not change which tests pass/fail). This is correct and tracked.

The runner does not short-circuit: the loop at `_init` lines 64–68 calls `_run_sprint_test_file()` for each path and aggregates `file_pass_count` / `file_fail_count` without breaking early. Exit code is non-zero iff any file failed — matches the acceptance bar.

### 3.5 Criterion 5 — `verify.yml` glob removed ✅

`.github/workflows/verify.yml` line 72 now reads:

```yaml
godot --headless --path godot/ --script res://tests/test_runner.gd
```

The prior `for f in godot/tests/test_sprint1[0-9]_*.gd ... do ... || exit 1` loop is gone. `grep -n "test_sprint1" .github/workflows/verify.yml` returns no matches. Lines 73–75 carry an explicit comment linking the change to S16.1-005.

### 3.6 Criterion 6 — `godot/combat/**` diff empty across S16.1 build set ✅

Per-commit scope-gate check on each of the 7 merge commits in the S16.1 build set:

```
git show --name-only --format="" <sha> -- godot/combat/
```

Output is empty for `da09699`, `9fcd439`, `3726f8e`, `ddc3b57`, `36e64f8`, `f1362d6`, `0267b71`. **Zero S16.1 commits touched `godot/combat/**`.**

(Note on windowed `git log`: `git log --since=2026-04-15 --until=2026-04-18 -- godot/combat/` returns S15 moonwalk commits `1e60bb6`, `dc0e49d`, and earlier S11–S14 work. Those are **not** part of the S16.1 build set — they predate and are unrelated. Scope-gate verification is per-build-set, not per-calendar-window; build-set diff is empty.)

**All 6 exit criteria hold. Verdict: S16.1 exit criteria HOLD.**

---

## 4. Scope-gate verification

The arc-level scope gate forbids any edits to `godot/combat/**` gameplay code, particularly `combat_sim.gd` and `brott_state.gd`. Verified via explicit per-PR diff, not a calendar-window sweep:

| PR | `godot/combat/` files touched |
|---|---|
| #89 | (none) |
| #90 | (none) |
| #91 | (none) |
| #92 | (none) |
| #125 | (none) |
| #126 | (none) |
| #127 | (none) |

Scope gate held cleanly. S16.1-003 was the most likely vector for a breach — it required determining whether `fire_at_range` was test-side or combat-side. Nutts triaged correctly as test-scaffolding drift and kept the fix confined to `test_sprint12_1.gd`. When the full `fire_at_range` story was identified as having a second invariant (approach-tick), it was routed to carry-forward item A rather than absorbed into S16.1.

Matches the pattern S15.2 established (scope gate held across 3 iterations on a moonwalk fix). Two sprints in a row with perfect scope-gate discipline → this is now the studio norm, not an exception.

---

## 5. Per-task review

### 5.1 [S16.1-001] Plating weight fix — PASS

- **Commit:** `da09699` | **PR:** [#89](https://github.com/brott-studio/battlebrotts-v2/pull/89)
- **Scope:** single constant change in `godot/tests/test_sprint12_2.gd`.
- **Diff discipline:** `armor_data.gd` untouched, as required. Pure test-data sync.
- **Notes:** Trivial work, clean execution. No concerns.

### 5.2 [S16.1-002] `test_sprint10.gd` parse fix — PASS

- **Commit:** `9fcd439` | **PR:** [#90](https://github.com/brott-studio/battlebrotts-v2/pull/90)
- **Scope:** explicit type annotation on the offending loop variable.
- **Diff discipline:** confined to `test_sprint10.gd`. No test-logic rewrite.
- **Notes:** Fix fit within the `<10 lines` / no-rewrite budget Nutts was given. No escalation to quarantine needed. Clean.

### 5.3 [S16.1-003] Plasma Cutter fire-at-range triage — PASS (with carry-forward A spawned)

- **Commit:** `3726f8e` | **PR:** [#91](https://github.com/brott-studio/battlebrotts-v2/pull/91)
- **Scope:** triaged as test-scaffolding drift against the new `simulate_tick` API; fixed at the call site.
- **Notes:** The full original test intent — Aggressive-Scout-with-Plasma-Cutter "Roach" can't fire on the approach tick — has a second invariant (movement+range coupling on tick 0) that is genuinely combat-side. Gizmo's S16.1-003 ratification correctly separated the pure range-gate canary (restored here, passing) from the approach-tick canary (new test, future gameplay sprint). This is the right decomposition: don't let a "fix one test" task quietly smuggle combat-code changes. Split + carry-forward = correct.
- **Carry-forward:** item A, filed as issue (see §6).

### 5.4 [S16.1-004] Combat-side quarantines — PASS

- **Commit:** `ddc3b57` | **PR:** [#92](https://github.com/brott-studio/battlebrotts-v2/pull/92)
- **Scope:** 13-line `TestUtil.skip_with_reason` helper in a new `godot/tests/test_util.gd`; three call sites in `test_sprint12_1.gd` at lines 75, 122, 284.
- **Diff discipline:** tests not deleted; assertions not loosened; `godot/combat/**` untouched. Canary preservation is exactly what the plan called for.
- **Notes:** The SKIP line format includes file pointers (`see godot/combat/brott_state.gd`, `see godot/combat/combat_sim.gd`) so a future gameplay-sprint author can start from the SKIP message and land on the right code path in one jump. Good future-proofing. The helper stayed well inside the 15-line budget (no S16.1-004a/b split needed).

### 5.5 [S16.1-005] Explicit enumeration — PASS

- **Commit:** `36e64f8` | **PR:** [#125](https://github.com/brott-studio/battlebrotts-v2/pull/125)
- **Scope:** `SPRINT_TEST_FILES` array in `test_runner.gd`; shell-glob loop removed from `verify.yml`; per-file subprocess invocation with non-short-circuiting exit-code aggregation.
- **Diff discipline:** no test pass/fail outcomes changed by this PR (plumbing-only). The header comment on the array explicitly calls out that sprints 3/4/5/6 are intentionally not enumerated because they have pre-existing failures and re-enumerating them would violate the S16 scope gate — that's the correct boundary.
- **Notes:** This is the structurally most important change in S16.1. The `|| exit 1` loop was the silent-green-where-red mechanism called out in S15.1 and S15.2 audits. It is now gone; a failure in one sprint file no longer prevents the others from running, and the runner reports *all* failing files, not just the first.
- **Carry-forward:** item B (sprint 3/4/5/6 triage) and item E (machine-readable quarantine registry) both surface from this work (§6).

### 5.6 [S16.1-006] GDD + renderer warning + Minigun audit — PASS (with 🟡 surface preserved)

- **Commit:** `f1362d6` | **PR:** [#126](https://github.com/brott-studio/battlebrotts-v2/pull/126)
- **Scope:** GDD §3.2 Plasma Cutter range corrected to 2.5; `arena_renderer.gd` warning resolved at source; Minigun fire-rate canon mismatch surfaced in PR body without editing `weapon_data.gd`.
- **Diff discipline:** correctly declined to change balance data unilaterally. 🟡 escalated per plan — this is the textbook scope-respecting move. HCD can rule on canon separately without the audit trail being polluted by a silent balance edit.

### 5.7 [S16.1 Close-out] — PASS (but see §7 process flag)

- **Commit:** `0267b71` | **PR:** [#127](https://github.com/brott-studio/battlebrotts-v2/pull/127)
- **Scope:** marked all six tasks complete in `sprints/sprint-16.md`; populated the Process & Infrastructure Carry-Forward table with items A–E; checked all six exit-criteria boxes; sealed the sub-sprint.
- **Notes:** Close-out narrative is accurate and complete. The only problem is structural, not content-based: **this PR declared the S16.1 audit-gate cleared without a Specc audit existing**. See §7.

---

## 6. Carry-forward items — filed as GitHub Issues

Per the new convention (studio-framework SUBAGENT_PLAYBOOK §Carry-Forward → Issues), each of the five Process & Infrastructure Carry-Forward items in `sprints/sprint-16.md` is now filed as a GitHub Issue on `brott-studio/battlebrotts-v2` with labels `backlog` + one `area:*` + one `prio:*`. The combat-regression carry-forwards (#1, #2, #4 in the main table) are **not** re-filed here — those are gameplay-sprint items, not S16-process debt, and remain visible via their `SKIP:` lines in CI.

| Tag | Item | Issue | Labels |
|---|---|---|---|
| A | Scout "approach tick" canary — new test authoring | [#137](https://github.com/brott-studio/battlebrotts-v2/issues/137) | `backlog`, `area:tests`, `prio:low` |
| B | Sprints 3/4/5/6 test files: quarantine-and-enumerate vs retire | [#138](https://github.com/brott-studio/battlebrotts-v2/issues/138) | `backlog`, `area:tests`, `prio:low` |
| C | ObjectDB / resource leaks in `test_sprint14_1_nav.gd` | [#139](https://github.com/brott-studio/battlebrotts-v2/issues/139) | `backlog`, `area:tests`, `prio:low` |
| D | `SceneTree.quit()` mid-function doc comment | [#140](https://github.com/brott-studio/battlebrotts-v2/issues/140) | `backlog`, `area:docs`, `prio:low` |
| E | Machine-readable quarantine registry | [#141](https://github.com/brott-studio/battlebrotts-v2/issues/141) | `backlog`, `area:tests`, `prio:mid` |

All issue bodies link back to `sprints/sprint-16.md#process--infrastructure-carry-forward` so the narrative stays reconstructable from either direction.

---

## 7. Process notes — audit-gate miss

**S16.1 shipped without a Specc audit.** This is the single biggest process finding of this sub-sprint.

The arc plan in `sprints/sprint-16.md` explicitly lists `Audit: Specc → studio-audits/audits/battlebrotts-v2/v2-sprint-16.1.md` as an S16.1 gate. `sprints/sprint-16.md` `sealed 2026-04-17` with all exit-criteria boxes checked. No audit file existed in `studio-audits/audits/battlebrotts-v2/` between S15.2 and S16.2-plan. The gap was caught at S16 arc resumption (2026-04-20) and is being filled retroactively by this audit.

**Severity.** Medium. The code is clean and the exit criteria hold, so no harm materialized — but the audit gate is the studio's primary independent check on pipeline claims. A sub-sprint closing without it means the pipeline self-certified, which is exactly the failure mode the audit gate exists to prevent.

**Root cause hypothesis** (not conclusive without transcript review, which Specc does not have Riv-session access for at the moment):

1. S16.1 ran fast (70 minutes, merge to close-out). The pipeline may have closed out on Optic verification alone, treating "Verify V1–V6 ✅" as sufficient.
2. The S16 arc plan's exit criteria are objective and verifiable, which can create a false sense that an audit is redundant. It isn't — the audit is where we *detect that the pipeline did what it said it did*, including the gates themselves.
3. S16 was flagged as pure tech-debt with fixed acceptance criteria and HCD-authorized autonomous operation. That autonomy mandate may have been misread as "skip audit gate," when in fact it only covered "don't ping HCD for creative approval mid-sprint."

**Remediation (this audit itself + standing):**

1. This audit now exists at `audits/battlebrotts-v2/v2-sprint-16.1.md` on `main` of `studio-audits`. S16.2 can proceed.
2. **Recommend to The Bott:** add a pre-close-out checklist item to Ett's close-out template and Riv's arc-resumption protocol: "Before closing a sub-sprint, confirm a Specc audit file exists at `audits/<project>/sprint-<N.M>.md` on `main` of `studio-audits`. If not, spawn Specc before close-out PR, not after." This is the kind of compliance-reliant process Specc §2 exists to flag — it relied on the pipeline *remembering* to spawn the auditor. A lightweight check at close-out time closes the loop.
3. **Cross-reference:** this is consistent with S15.2's observation (§5.1.1) that pipeline-gate framings need explicit resolution at close-out, not after. Two sprints in a row have surfaced "the gate framing was ambiguous" findings — worth watching whether a third appears before treating as systemic.

---

## 8. Grade

**A−.**

- **+A-range:** All 6 exit criteria hold on `main` today, not just at merge time. Scope gate perfect (zero `godot/combat/**` edits). Quarantine helper is minimal and correct. Explicit enumeration eliminates the silent-green-where-red class of failure that S15.1 and S15.2 audits both flagged. Plan-to-close-out elapsed time under 70 minutes for six tasks across five agents is fast without being sloppy. Boltz, Nutts, and Optic all executed cleanly. Gizmo's S16.1-003 ratification (splitting approach-tick from range-gate) is exactly the kind of scope-preserving design call the studio wants more of.
- **−:** The audit-gate miss at close-out is a pipeline-process defect. S16.1 is the first sub-sprint in recent memory to close without its auditor spawning. The code doesn't suffer for it, but the pipeline gave itself a grade it had not yet earned. That's a B-grade structural concern overlaid on A-grade content. Net: **A−**.

If the audit gate had been honored in-sprint, this would have been a straight A: execution quality on the code side is excellent.

---

## 9. Role Performance Review

### 🎭 Role Performance

**Gizmo:** Shining: S16.1-003 ratification — separated the pure range-gate canary (in-scope) from the approach-tick canary (out-of-scope, carry-forward A) cleanly, preserving test intent while respecting the scope gate. Also authored the skip-line format (explicit file pointer in the reason) that Nutts adopted — future-proofs the quarantine. Struggling: Minigun fire-rate canon ambiguity still unresolved (HCD ruling pending). Trend: ↑.
**Ett:** Shining: Plan was well-shaped — 6 tasks, clean ownership, explicit scope gate, triage-with-fallback-to-quarantine rule on S16.1-003 with a 30-minute budget. Carry-forward table populated at close-out with five new items correctly classified. Struggling: Close-out sealed the sub-sprint without confirming the audit gate had cleared. Whether Ett owns the close-out gate check or Riv does is a framework question (§7), but the miss happened inside Ett's close-out PR. Trend: →.
**Nutts:** Shining: Six tasks landed in under an hour with no scope breaches and no rework. S16.1-003 triage decision was correct and bounded (didn't burn the 30-min budget). The 13-line helper in S16.1-004 came in well under its 15-line ceiling. Honest surfacing on S16.1-006 (Minigun mismatch as 🟡 instead of silent edit). Trend: ↑.
**Boltz:** Shining: Six PRs approved and merged cleanly in order. Scope-gate enforcement held across all six — no PR landed with a `godot/combat/**` diff. Struggling: Did not flag that the close-out PR #127 was sealing S16.1 without an audit file existing in `studio-audits` — this is exactly the kind of pipeline-gate check Boltz review is positioned to catch. Trend: →.
**Optic:** Shining: V1–V6 verification covered the dummy code-path PR ✅, skip-line visibility, and test-runner non-short-circuit behavior. Caught ObjectDB leak warnings (carry-forward C) and `SceneTree.quit()` semantics (carry-forward D) that code review would not have caught — this is the structural value of Optic as a distinct role. Trend: ↑.
**Riv:** Shining: Arc sequencing S16.1 → S16.2 → S16.3 is correct; S16.3 (push: main trigger) genuinely depends on S16.1 having made main green first. Caught the audit-gate miss at S16 arc resumption and spawned Specc retroactively rather than blowing past it. Struggling: Did not catch the missing audit file at S16.1 close-out itself — only at arc resumption. Surfacing the miss 3 days later is better than never, but closing the loop in-sprint would have been the higher bar. Trend: → (with intent to ↑ pending adoption of §7 remediation).

Patch did not participate in S16.1 (Patch is S16.2 scope). Not graded.

---

## 10. Gate status

**Sprint 16.1 audit: COMMITTED. Gate cleared for S16.2.**

Recommendations to The Bott are in §7 remediation. S16.2 can proceed.

---

## Appendix A — Key refs

- Arc plan: [`sprints/sprint-16.md`](https://github.com/brott-studio/battlebrotts-v2/blob/main/sprints/sprint-16.md)
- Build set: PRs [#89](https://github.com/brott-studio/battlebrotts-v2/pull/89), [#90](https://github.com/brott-studio/battlebrotts-v2/pull/90), [#91](https://github.com/brott-studio/battlebrotts-v2/pull/91), [#92](https://github.com/brott-studio/battlebrotts-v2/pull/92), [#125](https://github.com/brott-studio/battlebrotts-v2/pull/125), [#126](https://github.com/brott-studio/battlebrotts-v2/pull/126), [#127](https://github.com/brott-studio/battlebrotts-v2/pull/127)
- Close-out commit: `0267b71`
- Green-suite reference run: [Godot Unit Tests on PR #92](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24582700945/job/71884376309)
- Previous audit: [`audits/battlebrotts-v2/v2-sprint-15.2.md`](./v2-sprint-15.2.md)

## Appendix B — Test state at S16.1 close-out

| Suite / Check | Result | Notes |
|---|---|---|
| `Godot Unit Tests` on PR #92 head | ✅ PASS | First green run after quarantine |
| `Godot Unit Tests` on PR #125 head | ✅ PASS | Post explicit-enumeration |
| `Godot Unit Tests` on PR #126 head | ✅ PASS | Post GDD + renderer warning fix |
| `Godot Unit Tests` on PR #127 head | (skipped) | Doc-only; `paths-ignore` correctly excluded it |
| `godot/combat/**` diff across S16.1 build set | EMPTY | Scope gate held |
| `test_runner.gd` sprint 10+ coverage | 20/20 explicit | Sprint 3/4/5/6 intentionally excluded (carry-forward B) |
| `verify.yml` shell glob | REMOVED | Single-line runner invocation |
| Three combat-side SKIP lines in CI | visible every run | Exact text preserved in §3.3 |

---

_Audit complete. 2026-04-20T14:55Z — Specc (retroactive)._
