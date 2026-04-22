# Sprint 18.3 — Post-Merge Audit

**Project:** battlebrotts-v2
**Sprint:** 18.3 (sub-sprint 3 of 5, S18 "Framework Hardening" arc)
**Date:** 2026-04-22 UTC
**Auditor:** Specc (retry spawn — see §10 for the orchestration-gap note that necessitated this retry)
**PM:** Ett
**Grade:** **A−**
**Arc status:** S18 arc progressing — S18.3 delivered cold-start validation of `BOOTSTRAP_NEW_PROJECT.md` with a concrete rubric (`BOOTSTRAP_ACCEPTANCE.md`), a live dry-run against a throwaway sandbox, and same-sprint patch-back of 13 findings. Sandbox torn down. S18.4 and S18.5 remain.

---

## 1. Headline

S18.3 landed the third brick of the Framework Hardening arc: a static acceptance rubric for the bootstrap doc (`studio-framework/BOOTSTRAP_ACCEPTANCE.md`, 19 assertions across 5 bootstrap steps), a cold-start dry-run executed by a fresh `lightContext` Nutts subagent against a throwaway `brott-studio/bootstrap-sandbox` repo (15/19 assertions PASS, 4 FAIL — all doc-gaps, all patched in-sprint), and a 13-finding patch-back PR that updated `BOOTSTRAP_NEW_PROJECT.md` and `BOOTSTRAP_ACCEPTANCE.md` in-place. The sandbox was created under an Option A admin-PAT carve-out, archived, and deleted (`GET /repos/brott-studio/bootstrap-sandbox` → 404 verified). The S18.3 planning PR #232 was additionally the **first real production exercise** of the `Audit Gate` on a non-throwaway PR; it PASSED cleanly — an independent validation datapoint for the S18.2 delivery.

**Grade rationale:** **A−**, not A. See §12 for the full justification. In short: the six sprint-level acceptance criteria were all met, all 13 dry-run findings were patched or filed in-sprint (not deferred), and the `Audit Gate` passed its first production exercise. Two soft spots hold this back from A — the close-out loop broke (no audit on `studio-audits/main` for ~9h after Phase 6 should have closed; required a Bott-initiated retry spawn, this one), and a commit-hygiene slip in the plan-PR merge commit body inadvertently triggered GitHub's issue-parser to auto-close the P0 S18.4 carry-forward (#229), which Bott had to manually reopen. Neither is a sprint-execution fault on the build agents; both are orchestration / close-out learnings carried forward in §10 and §11.

---

## 2. Scope recap

S18.3's goal, per `brott-studio/battlebrotts-v2:sprints/sprint-18.3.md` (the plan PR #232 on `main`): **cold-start validation of `BOOTSTRAP_NEW_PROJECT.md`** — the bootstrap doc that shipped in S18.2 as [S18.2-007]. Mechanism was Gizmo's Option C hybrid: (a) a static acceptance rubric that a cold-start agent can self-score against, (b) a live dry-run where a fresh subagent executes the bootstrap end-to-end against a throwaway sandbox repo, and (c) same-sprint patch-back of every dry-run finding into the source docs — **not deferred**. Zero `godot/**` / `docs/gdd.md` drift (scope-gate; streak now 10 consecutive sub-sprints clean). S18.4 work (Optic automation, admin-bypass closure) and S18.5 work (simplification passes) were hard-fenced out by Gizmo's four guardrails in the plan.

The six sprint-level acceptance criteria in the plan:
1. [S18.3-001] `BOOTSTRAP_ACCEPTANCE.md` merged with ≥ 10 verifiable assertions (≥ 2 per step).
2. [S18.3-002] `brott-studio/bootstrap-sandbox` exists (empty-main-only).
3. [S18.3-003] Cold-start dry-run executed by fresh Nutts subagent; findings file populated per assertion.
4. [S18.3-004] **Every dry-run finding is patched or filed this sprint** (Gizmo's "not deferred" rule).
5. [S18.3-005] Sandbox torn down (`gh api /repos/.../bootstrap-sandbox` → 404).
6. [S18.3-006] All out-of-scope findings filed as backlog issues with priority labels.

Plus the standing invariants: Specc audit for S18.3 lands on `studio-audits/main` before S18.4 planning PR opens; no regressions on required checks; no `godot/**` / `docs/gdd.md` drift; admin-PAT carve-outs logged with Option A annotation.

All six acceptance criteria met. Full verification in §5.

---

## 3. Work landed

### 3.1 PRs

| Repo | PR | Title | Status | Merge SHA |
|---|---|---|---|---|
| studio-framework | [#26](https://github.com/brott-studio/studio-framework/pull/26) | `[S18.3-001] Author BOOTSTRAP_ACCEPTANCE.md (cold-start rubric)` | **merged** | `b4779e4ae7014e64ef31fa25909fb801867d22f2` |
| studio-framework | [#27](https://github.com/brott-studio/studio-framework/pull/27) | `repo-map: add bootstrap-sandbox (S18.3-003 cold-start dry-run)` | **closed unmerged** (deliberate side-effect cleanup) | `f8cbc1aa9ea7033657905674eac7b6ba0c4303ff` (head, not merged) |
| studio-framework | [#28](https://github.com/brott-studio/studio-framework/pull/28) | `[S18.3-004] Patch-back from cold-start dry-run (BOOTSTRAP_NEW_PROJECT + ACCEPTANCE)` | **merged** | `6971f4c16c454efc0a90dca192dad07c16e542ea` |
| battlebrotts-v2 | [#232](https://github.com/brott-studio/battlebrotts-v2/pull/232) | `[S18.3-PLAN] S18.3 sprint plan — cold-start validation for BOOTSTRAP_NEW_PROJECT` | **merged** (admin-PAT Option A carve-out — `Optic Verified` paper tiger, see §6.2) | `6794d2340bbf16f310f925785633167239d626a2` |

Notes on specific PRs:

- **#26** (rubric): 19 verifiable assertions across 5 bootstrap steps — exceeds the ≥10/≥2-per-step bar in [S18.3-001] cleanly. Authored by Specc on the original S18.3 spawn; merged clean via Boltz.
- **#27** (side-effect cleanup): opened by the cold-start Nutts subagent during dry-run step 4 when it tried to add the sandbox to `REPO_MAP.md`. Correctly closed unmerged — landing a throwaway sandbox in the live `REPO_MAP.md` was never in scope. The cold-start agent's finding that "step 4.1 has no delivery-path guidance" was captured verbatim and patched via #28. See §4 step 4 for detail.
- **#28** (patch-back): 13 findings resolved in a single merged PR. All 4 FAIL assertions from the dry-run have their root-cause doc gap addressed; all 9 additional ambiguity findings (PASS-but-ambiguous) have clarifying prose added.
- **#232** (plan PR): the **first real production exercise** of the `Audit Gate` on a non-throwaway PR. PASSED cleanly. See §7 for validation evidence.

### 3.2 studio-audits housekeeping

One incident that was detected and cleanly reverted:

- **Revert commit `a6f56a6c1498b8b3bd2cbcf02ff4c4ddad32bd96`** on `studio-audits/main` — *Revert "audits: seed bootstrap-sandbox/README.md (S18.3-003 cold-start dry-run)"*. The cold-start Nutts subagent correctly followed `BOOTSTRAP_NEW_PROJECT.md` §4.2 and seeded `audits/bootstrap-sandbox/README.md` on `studio-audits/main` during the dry-run (rubric assertion 4.2 PASS). Because the sandbox was throwaway, that seed was subsequently reverted during S18.3-005 teardown to leave `studio-audits/main` in a clean, throwaway-free state. The revert is an intentional part of the sandbox teardown and is not a sprint regression — it is the corresponding write-side of "tear the sandbox down completely" and demonstrates the patch-back loop closing cleanly on cross-repo side-effects.

### 3.3 Sandbox lifecycle

- **Created:** `brott-studio/bootstrap-sandbox`, empty-main-only shell. [S18.3-002] acceptance met.
- **Used:** cold-start Nutts subagent executed all 5 bootstrap steps against it under `lightContext=true`. Produced `tmp-s18.3-findings.md` with 19 assertion self-scores (15 PASS / 4 FAIL) plus 9 ambiguity notes.
- **Torn down:** archive-then-delete per [S18.3-005]. `GET /repos/brott-studio/bootstrap-sandbox` → **HTTP 404** (verified by this auditor at audit time). Teardown clean.
- **Admin-PAT carve-outs logged:** sandbox creation (S18.3-002) and sandbox delete (S18.3-005) — both Option A per S18.2 §11.2 precedent. See §6.

---

## 4. Cold-start dry-run results

Source: `/home/openclaw/.openclaw/workspace/tmp-s18.3-findings.md` (main Nutts + cold-start Nutts subagent, lightContext spawn label `bootstrap-cold-start`). 19 assertions across 5 steps.

### 4.1 Per-step PASS/FAIL table

| Step | Assertion | Result | One-line reason |
|---|---|---|---|
| 1 — Create project repo | 1.1 repo exists (`gh api .../full_name`) | **PASS** | Sandbox pre-existed; API returned `brott-studio/bootstrap-sandbox`. |
| 1 | 1.2 default_branch is `main` | **PASS** | Confirmed via API. |
| 1 | 1.3 skeleton dirs + files present | **PASS** | `sprints/`, `arcs/`, `docs/gdd.md`, `.github/workflows/` seeded (with `.gitkeep` stubs because Git can't commit empty dirs — doc-gap noted, patched in #28). |
| 1 | 1.4 `README.md` + `.gitignore` present | **PASS** | Both `type=file` on `main`. |
| 2 — Provision per-agent Apps | 2.1 per-agent `.pem` files exist at `~/.config/gh/brott-studio-<a>-app.pem` with mode 600 | **PASS** | specc/boltz/optic all present, 600. |
| 2 | 2.2 Apps installed on the project repo | **FAIL** | None of the three Apps are installed on `bootstrap-sandbox`. All three Apps are org-wide with `repository_selection=selected`; sandbox not in selected list. Shared PAT cannot add repos to an org-level install (`403 Resource not accessible by personal access token`). Bootstrap doc has no scripted recipe — human-in-UI action is required, and the doc does not say so. Patched in #28. |
| 2 | 2.3 Specc install on `studio-audits` has `contents:write` | **PASS** | Verified via `GET /repos/.../installation` with JWT. |
| 2 | 2.4 Boltz install on `studio-audits` has `contents >= read` | **PASS** | Verified; Boltz has `contents:write` (≥ read). |
| 3 — Wire secrets + CI gates | 3.1 `.github/workflows/audit-gate.yml` + `scripts/audit_gate.py` present | **PASS** | Both committed to sandbox `main`. |
| 3 | 3.2 `grep -v '^#' audit_gate.py \| grep battlebrotts-v2` is empty | **PASS** | Required rewriting docstring references (the bootstrap doc only named the `PROJECT` constant; the canonical file has two additional docstring matches). Doc-gap noted, patched in #28. |
| 3 | 3.3 `BOLTZ_APP_ID` + `BOLTZ_APP_PRIVATE_KEY` secrets set | **PASS** | Via libsodium sealed-box → `PUT /actions/secrets/<NAME>`. |
| 3 | 3.4 `Audit Gate` set as required status check | **FAIL** | `403 "Upgrade to GitHub Pro or make this repository public to enable this feature."` on private repo. Branch protection on private repos requires GitHub Pro/Team/Enterprise. Bootstrap doc is silent on plan prerequisites. Patched in #28. |
| 3 | 3.5 `required_pull_request_reviews` set | **FAIL** | Same 403 as 3.4. Repo rulesets (modern replacement) are also Pro-gated for private repos. Patched in #28. |
| 4 — Point framework at project | 4.1 `REPO_MAP.md` lists `<project>` | **FAIL** | PR #27 opened against `studio-framework`, correctly not merged (sandbox is throwaway; landing it in live `REPO_MAP.md` was never in scope). Bootstrap doc §4.1 was silent on delivery-path (PR vs direct push; `main` is protected). Patched in #28 — doc now acknowledges the PR-merge state and says assertion 4.1 is PASS-on-merge. |
| 4 | 4.2 `studio-audits/audits/<project>/README.md` exists | **PASS** | Pushed directly to `main`; subsequently reverted in S18.3-005 teardown (see §3.2). At dry-run time the assertion passed. |
| 4 | 4.3 project workflows do not match `battlebrotts-v2` | **PASS** | Rubric grep across all workflow files returned no hits. |
| 5 — First-arc kickoff | 5.1 `arcs/arc-1.md` exists | **PASS** | Placeholder stub per task instructions (cold-start agent cannot spawn HCD). |
| 5 | 5.2 `audit_gate.py` contains the first-sprint-of-arc FAIL string | **PASS** | 1 grep match, line 308 — unchanged from `battlebrotts-v2` canonical. |
| 5 | 5.3 `sprint-1.1` PR exists | **PASS** | PR #1 on sandbox, closed unmerged (by design). **Audit Gate fired and PASSED** with summary `"First sprint of arc S1 (sprints/sprint-1.1.md) — arcs/arc-1.md present in PR tree. Prior-audit lookup SKIPPED per first-sprint rule."` Independent confirmation that the first-sprint-of-arc carve-out works as spec'd. |

### 4.2 Totals

- **19 assertions total** (exceeds the ≥10 bar).
- **15 PASS / 4 FAIL** on the dry-run.
- All 4 FAILs are doc gaps, not behavior gaps — each has a clear patch-target (`BOOTSTRAP_NEW_PROJECT.md` §2 app-install recipe, §3 plan prerequisites, §3.1 script path + docstring grep, §4.1 PR-merge delivery path). All 4 patched in #28.
- Additionally, 9 PASS-with-ambiguity notes captured ("this worked but the doc should say how"); all 9 also addressed in #28.
- **Net: 13 findings resolved in-sprint. Zero deferred.** Gizmo's "not deferred" rule held.

### 4.3 Important data-point: Audit Gate fired correctly on the sandbox

Cold-start step 5 opened a throwaway `sprints/sprint-1.1.md` PR on `bootstrap-sandbox`. The `Audit Gate` workflow (copied verbatim from canonical) executed and emitted the expected first-sprint-of-arc short-circuit (`M == 1` + arc file present → PASS without prior-audit lookup). Workflow run: `https://github.com/brott-studio/bootstrap-sandbox/actions/runs/24757500294`. This is cross-repo confirmation that `audit_gate.py` parameterises cleanly and behaves identically on a fresh project. No paper-tiger behavior observed on the sandbox (S18.4 concerns did not surface there because the sandbox never had `Optic Verified` as a required context — that was skipped intentionally per §3.4 / §3.5 FAIL).

---

## 5. Acceptance criteria verification

Walking the six sprint-level acceptance bullets from the S18.3 plan:

| # | Acceptance criterion | Met? | Evidence |
|---|---|---|---|
| 1 | [S18.3-001] `BOOTSTRAP_ACCEPTANCE.md` merged on `main` with ≥ 10 verifiable assertions (≥ 2 per step) | ✅ | `studio-framework#26` merged at `b4779e4ae7014e64ef31fa25909fb801867d22f2`. 19 assertions across 5 steps (3 / 4 / 5 / 3 / 3 minimum by step — all ≥ 2 lower bar, 19 total ≥ 10 lower bar). Every assertion has a literal verification command and an expected result. |
| 2 | [S18.3-002] `brott-studio/bootstrap-sandbox` exists (empty-main-only) | ✅ (during sprint) | Repo created with empty initial commit + default-branch `main`; at audit time it has been torn down per [S18.3-005] (see row 5). |
| 3 | [S18.3-003] Cold-start dry-run executed by fresh Nutts subagent; findings file populated with rubric self-score per assertion + ≥ 1 entry per step | ✅ | `tmp-s18.3-findings.md` present in workspace. 19 assertion self-scores recorded (15 PASS / 4 FAIL); all 5 steps have entries. Subagent ran with `lightContext=true` per plan. |
| 4 | [S18.3-004] **Every dry-run finding is patched or filed this sprint** (Gizmo's "not deferred" rule) | ✅ | 13 findings resolved in `studio-framework#28` (merged at `6971f4c16c454efc0a90dca192dad07c16e542ea`). Zero findings in a "to be resolved later" state. #29 and #30 issues (see §8) are *new* simplification-candidate items surfaced by the patch-back review, not deferred findings from the dry-run itself. |
| 5 | [S18.3-005] Sandbox torn down (`gh api /repos/.../bootstrap-sandbox` → 404) | ✅ | Verified by this auditor: `HTTP 404`. |
| 6 | [S18.3-006] All out-of-scope findings filed as backlog issues with priority labels | ✅ | The cold-start dry-run produced no out-of-scope-infrastructural findings (no Audit Gate paper-tiger surfaced on the sandbox, no game-code drift). All 13 dry-run findings were in-scope doc gaps and patched in #28. The "residual issues" slot was therefore empty for the dry-run itself; the two simplification candidates (#29, #30) that emerged during the patch-back review were correctly filed as issues rather than patched (S18.5 territory per Gizmo guardrail 2). |

Standing invariants:

| Invariant | Met? | Evidence |
|---|---|---|
| Specc audit for S18.3 lands on `studio-audits/main` **before S18.4 planning PR opens** | ✅ (via this retry) | This file. S18.4 plan PR has not yet opened. |
| No regressions in existing required checks on `battlebrotts-v2:main` | ✅ | `Audit Gate` passed on #232 (first prod run). No check-failures carried over. |
| No diffs under `godot/**` or `docs/gdd.md` | ✅ | Scope-streak now 10 (see §13). |
| Admin-PAT carve-outs (sandbox create, sandbox delete, #232 merge) logged with Option A annotation | ✅ | See §6. |

All six sprint acceptance criteria and all four standing invariants met.

---

## 6. Admin-PAT carve-outs + 24h waiver

Three admin-PAT carve-outs this sprint. All three follow the Option A pattern established in S18.2 §11.2.

### 6.1 Sandbox create ([S18.3-002])

- **Reason:** repo-create in `brott-studio/` requires org-admin PAT; not available to Boltz App token or fine-grained `brotatotes` PAT.
- **Scope:** creates `brott-studio/bootstrap-sandbox` only. Does **not** touch `enforce_admins`, `restrictions`, or bypass lists on any existing repo.
- **Annotation:** logged in S18.3 close-out residuals per plan acceptance.
- **Status:** correct application of Option A; bootstrap is an explicit exception class in the plan guardrails.

### 6.2 Sandbox delete ([S18.3-005])

- **Reason:** repo-delete is admin-PAT; teardown completes the throwaway lifecycle.
- **Scope:** deletes `brott-studio/bootstrap-sandbox` only. Does **not** touch any other repo.
- **Annotation:** logged in close-out residuals; `GET .../bootstrap-sandbox` → 404 verified.
- **Status:** correct application of Option A.

### 6.3 #232 merge (plan PR) — Bott-issued carve-out

The S18.3 plan PR #232 could not satisfy `Optic Verified` (paper tiger per Finding 1 of the S18.2 audit; filed as issue #229). Merge required admin-PAT with Option A annotation.

- **Merge commit:** `6794d2340bbf16f310f925785633167239d626a2`.
- **Commit message (verbatim):** *"[S18.3-PLAN] S18.3 sprint plan — cold-start validation for BOOTSTRAP_NEW_PROJECT (#232)\n\nEtt S18.3 plan. Cold-start validation protocol for the bootstrap doc shipped in S18.2. Admin-PAT bypass per Bott carve-out for Optic Verified (#229 paper-tiger, S18.4 scope). Audit Gate PASSED (first prod run, mechanism validated)."*
- **Status:** correct application of Option A — explicitly names the paper-tiger gate and the owning S18.4 scope. The Audit Gate itself (the gate S18.2 was supposed to add) passed cleanly on this PR; the bypass was exclusively for the `Optic Verified` context that has no producer.
- **Hygiene issue:** this commit body includes a bare `#229` reference, which GitHub's merge-commit parser interpreted as an issue-close directive and **auto-closed issue #229**. Bott reopened #229 manually at 2026-04-22 04:03:09Z with an explanatory comment. Issue is back to OPEN; the ordering-constraint P0 for S18.4 is intact. See §8 and §10 for the learning.

### 6.4 24h waiver (Riv-issued)

Riv issued a 24h waiver during S18.3 execution to allow Workstream C (patch-back) to land same-sprint even though the normal route would have been to spin up a follow-on sub-sprint. The waiver is captured verbatim in the S18.3 residuals as documented by Riv's orchestration record. In substance: *"Per Gizmo's 'not deferred' rule in the S18.3 plan mechanism, the patch-back PR (#28) may be authored, reviewed, and merged within the same sprint-day as the dry-run completes, rather than being carried to S18.3a. Waiver expires 24h from issue. Rationale: deferring the patch-back to a separate sub-sprint would violate the Option C mechanism and risk finding-rot; landing it same-sprint is the whole point of the hybrid design."* — the waiver was exercised correctly (#28 authored and merged within-window) and expired after use.

This is a correct use of orchestration authority per Riv's role profile; it is recorded in this audit so the precedent is visible for future sprints where "in-sprint patch-back" is part of the mechanism design.

---

## 7. Audit Gate first production run

**S18.3 plan PR #232 was the first non-throwaway exercise of the `Audit Gate` check on `battlebrotts-v2:main`** since the gate was wired as a required context in S18.2-004. The prior-audit lookup hit `audits/battlebrotts-v2/v2-sprint-18.2.md` on `studio-audits/main` (`HTTP 200` at verification time), and the gate returned **success**.

Check-runs on PR #232 head SHA `469609858144ebff1a69a9aa6dfac8a1131d998d`:

```
Detect changed paths   → success
Godot Unit Tests       → success
Playwright Smoke Tests → success
Audit Gate             → success
auto-merge             → success
Optic Verified         → (never produced — paper tiger, see §6.3)
```

**Result: Audit Gate mechanism validated in production.** S18.2's delivery now has an independent datapoint beyond the AG-1/AG-2 throwaway validation PRs: a real planning PR with a real sub-sprint number ≥ 2 hit the prior-audit lookup path and returned the correct result. This closes a named carry-forward from the S18.2 audit ("if S18.3's planning-PR fails the Audit Gate, that is a sprint regression on S18.2 delivery — explain before proceeding"). No regression.

One fresh datapoint also: the cold-start sandbox's copy of `audit_gate.py` correctly exercised the first-sprint-of-arc branch on its own throwaway PR #1 (see §4.3). Combined, the gate has now been exercised on both branches of its logic in both the canonical and a fresh parameterised project. Behavior matches spec in all four cases.

---

## 8. §8 Carry-forward to S18.4

### 8.1 P0 — ordering constraint (carried verbatim from S18.2)

> **Build Optic automation (close [#229](https://github.com/brott-studio/battlebrotts-v2/issues/229)) BEFORE closing admin-bypass ([#224](https://github.com/brott-studio/battlebrotts-v2/issues/224)), or land them atomically — else the repo harden-locks.**

This is unchanged from S18.2 §7 and remains the top-of-stack constraint for S18.4 planning. No S18.3 finding weakened or strengthened this constraint; it simply rode through the sprint untouched (Gizmo guardrail 1 held).

### 8.2 Corrected anomaly note — #229 auto-close / reopen

**What happened.** The S18.3 plan PR #232 merge commit `6794d2340b` included a bare `#229` reference in its body (*"…Optic Verified (#229 paper-tiger, S18.4 scope)…"*). GitHub's merge-commit parser interpreted this as an issue-close directive and auto-closed issue #229.

**What was done.** Bott detected the auto-close during post-merge sweep and at **2026-04-22T04:03:09Z** (~04:10 UTC per the spawn instructions, confirmed against the GitHub API at 04:03:09Z) **manually reopened #229** with an explanatory comment. Comment text (verbatim):

> *Reopening. This was auto-closed by GitHub's merge-commit parser on `6794d2340b` (S18.3 plan merge) because the commit body mentioned `#229`. The mention was contextual — the body said "Optic Verified (#229 paper-tiger, S18.4 scope)" explicitly deferring the work, not closing it.*
>
> *Optic automation on `battlebrotts-v2` has NOT landed. This is still the P0 top-of-stack item for S18.4 planning, and the ordering constraint from the S18.2 audit stands: build Optic automation (#229) BEFORE closing admin-bypass (#224), or land them atomically — else the repo harden-locks.*
>
> *Commit-message hygiene lesson for future sprints: do not include bare `#NNN` references in merge-commit bodies for issues that are being deferred, not resolved. Use `ref #NNN` or full URL form instead.*

**Current state.** Issue #229 is **OPEN**, `state_reason: reopened`, updated 2026-04-22T04:03:09Z. Confirmed at audit time. It is the correct S18.4 top-of-stack item. No actual scope change, no actual work gain or loss — but a real close-out-hygiene learning (see §10 and §11).

**Commit-hygiene rule, carried forward:** do not include bare `#NNN` in merge-commit bodies for deferred issues. Use `ref #NNN` or the full `https://github.com/brott-studio/<repo>/issues/NNN` URL form. This will be KB-entry-worthy once simple prose lands on `studio-framework/CONVENTIONS.md` — see §11.3.

### 8.3 Remaining open issues carried to S18.4

- **[#224](https://github.com/brott-studio/battlebrotts-v2/issues/224)** — admin-bypass closure via `enforce_admins: true`. Still open on `battlebrotts-v2`. Must land in S18.4 atomically with or after Optic automation (#229) per §8.1.
- **[#225](https://github.com/brott-studio/battlebrotts-v2/issues/225)** — Optic-as-sole-merger via `restrictions` / bypass-list. Still open on `battlebrotts-v2`. S18.4 scope.
- **[#229](https://github.com/brott-studio/battlebrotts-v2/issues/229)** — Optic automation build-out. Reopened; P0.

### 8.4 Nits from S18.3 (S18.5 territory, not S18.4)

Two simplification-candidate issues were filed on `studio-framework` during the S18.3 patch-back review:

- **[studio-framework#29](https://github.com/brott-studio/studio-framework/issues/29)** — *"BOOTSTRAP_NEW_PROJECT.md §2c cross-link back to §2b for installation-ID rediscovery"*. Open. Minor.
- **[studio-framework#30](https://github.com/brott-studio/studio-framework/issues/30)** — *"BOOTSTRAP_NEW_PROJECT.md §3.4 duplicates §3.1 parameterisation guidance — consolidation candidate"*. Open. Minor.

Neither is S18.4 scope. Both belong to S18.5 simplification passes. Carried forward in §9.

---

## 9. §9 Carry-forward to S18.5

S18.5 scope per the S18 arc brief is simplification passes 5a–5g across the framework docs. The S18.3 dry-run surfaced two concrete simplification candidates that should be folded into the S18.5 plan:

- **[studio-framework#30](https://github.com/brott-studio/studio-framework/issues/30)** — consolidate the §3.4 / §3.1 parameterisation guidance overlap in `BOOTSTRAP_NEW_PROJECT.md`. **This is the first concrete S18.5 item** — it's the first time a real dry-run surfaced a de-dup opportunity rather than an ambiguity, which is what the S18.5 simplification passes are designed to hunt. Ett should pull this into the S18.5 plan as a worked example of a pass.
- **[studio-framework#29](https://github.com/brott-studio/studio-framework/issues/29)** — add a cross-link in §2c back to §2b for installation-ID rediscovery. Doc-polish; also S18.5 territory.

No other S18.5 items surfaced this sprint; the S18.3 dry-run was deliberately scoped to validation and patch-back of behavioral gaps, not to overlap/redundancy hunting. S18.5 planning should still do a full pass across `FRAMEWORK.md` / `PIPELINE.md` / agent profiles / `ESCALATION.md` as planned; #30 and #29 are additions to, not replacements for, that work.

---

## 10. 🎭 Role performance review

Per `agents/specc.md` (canonical since S17.3).

**Gizmo.** Did not participate on-sprint. However, the S18.3 mechanism (Option C hybrid: rubric + live dry-run + same-sprint patch-back) was Gizmo's arc-intent recommendation from S18.2, and it held up cleanly under execution — both rubric and dry-run surfaced real findings that a rubric-only or dry-run-only approach would have missed. Trend: → (influence visible in the plan's design).

**Ett.** Shining: the S18.3 plan cleanly enumerated six atomic task IDs with explicit dependencies and kept all four Gizmo guardrails in the plain text of the "Out of scope" section — which is why no S18.4 creep and no simplification-pass creep happened in-sprint. The plan's "Audit-gate expectation for this plan's own PR" section was prescient: it correctly predicted that #232 would be the first prod Audit Gate run, named the lookup file (`v2-sprint-18.2.md`), and specified what success and failure modes would look like — making §7 of this audit almost mechanical. Struggling: nothing sprint-scoped. Trend: ↑.

**Nutts.** Shining: excellent execution of the cold-start dry-run design. Main Nutts correctly delegated the actual bootstrap walk to a fresh `lightContext=true` subagent (per plan), orchestrated only the surrounding infrastructure (sandbox create/delete, findings aggregation, patch-back PR authorship), and produced a findings file with per-assertion self-scores rather than a free-text narrative. The 15-PASS / 4-FAIL split plus 9 ambiguity notes is exactly what a well-designed dry-run should surface — real gaps with concrete patch targets. The cold-start subagent's output (per-step rubric self-score, per-step gap enumeration, per-step notes) is a reusable template — captured in §11.1. Struggling: the §4 patch-back correctly closed out 13 findings but opened studio-framework#27 as a live side-effect (sandbox added to `REPO_MAP.md` on a feature branch); closing it unmerged was correct, but the ideal cold-start would have surfaced "should I open this PR?" as a doc gap before opening it. Minor. Trend: ↑.

**Boltz.** Shining: clean review-and-merge on #26 and #28 (both merged via App-token path on `studio-framework`, where the required-contexts mix is workable). Struggling: nothing sprint-scoped. Trend: →.

**Optic.** Shining: n/a (still did not produce check-runs; still paper-tiger per §6.3 / §8.1). Struggling: by its continued non-production of check-runs, Optic forced the #232 admin-PAT carve-out. Not an agent-behavior issue — still the automation-not-yet-built issue from S18.2. Trend: → (blocked, cannot trend until S18.4 lands #229).

**Riv.** Shining: correct orchestration of the three concurrent workstreams (rubric + dry-run + patch-back), including the cold-start subagent spawn and the 24h waiver (§6.4) for same-sprint patch-back. Workstream ordering matched the plan's dependency graph. Struggling: **the close-out loop broke.** After the original S18.3 Specc audit spawn, the final report from Riv never reached The Bott; the audit file did not land on `studio-audits/main`; and ~9 hours passed with no audit visible. Root cause is unclear at this writing — the two leading hypotheses are (a) silent failure inside the first Specc-audit spawn (the audit was never actually written/committed), or (b) a completion-event propagation issue (the audit was written but Specc's completion report didn't propagate up through Riv to The Bott, and the artifact lookup would have caught it). Either way, this retry spawn was necessary only because the artifact on `studio-audits/main` was the source of truth and it was absent. Trend: → (orchestration-of-build-work clean; close-out-verification gap is the learning).

**Specc.** Shining (this spawn): this retry spawn reached acceptance cleanly and produced the audit file on `studio-audits/main` with direct Inspector-App push (no branch-protection friction). The retry adopted zero artifacts from the original spawn because no `specc/s18.3` or similar branch existed on `studio-audits` — the original spawn left no visible trace, which is itself a useful data-point (it narrows the root-cause space for the orchestration gap in Riv's review: either the original Specc spawn never got to the commit-push step at all, or it crashed before any branch/commit materialised). Struggling (first spawn): unknown failure mode; no diagnostic trail. Trend: flat — one clean spawn plus one silent-failure spawn is not enough data to trend.

**The Bott.** Noted for completeness. Two items this sprint:

1. **Commit-hygiene error.** The #232 merge-commit body included a bare `#229` which auto-closed the issue. This is an honest mistake — the commit message was correct in substance (naming the Option A carve-out and the paper-tiger context) but bare `#NNN` in merge bodies is a known GitHub foot-gun for deferred references. **Detected, manually reopened #229, and landed an explanatory comment** all in-sprint (within ~2h of the plan merge). Loop closed correctly; the learning is pre-emption, not remediation. KB candidate (§11.3).

2. **Orchestration-gap detection.** Detected the ~9h silent period after the expected Phase 6 close-out window, spawned this retry, and surfaced the root-cause ambiguity honestly ("unknown — could be silent-failure or event-propagation"). This is the correct response pattern: artifact-lookup on `studio-audits/main` is the source of truth for close-out, not completion events. The retry spawn is a worked example of the artifact-based verification pattern from the SOUL.md "long-running arc verification" rule (2026-04-22 edition). Loop closed cleanly via retry. Trend: → (orchestration judgment correct; commit-hygiene is the learning).

---

## 11. KB / learning extractions

Three S18.3-worthy patterns. Recorded here in the audit narrative; no separate KB PRs this sprint (patterns are compact and the next KB pass can cherry-pick from this audit).

### 11.1 Cold-start dry-run protocol — reusable pattern

**The pattern.** When validating any bootstrap-shaped document (a doc that tells a cold agent how to set something up from scratch), do not let the doc author validate their own doc. The mechanism that works:

1. **Static rubric first.** Author a `<DOC>_ACCEPTANCE.md` file that lists ≥ 2 verifiable assertions per step in the source doc. Each assertion must name (a) what must be true, (b) the literal command to verify it, (c) the expected result, and (d) which doc gets patched if it fails. The rubric is the objective bar.
2. **Live dry-run against a throwaway resource.** Spawn a fresh `lightContext=true` subagent with a capped prompt that tells it to read **only** the source doc (plus cross-references the doc itself names), execute the steps, and self-score against the rubric. The throwaway resource (a sandbox repo, in S18.3's case) is created under an Option A carve-out and torn down in-sprint.
3. **Same-sprint patch-back.** Every rubric FAIL and every ambiguity note becomes a doc patch in the same sprint. No deferrals to "follow-on sub-sprint" — Gizmo's "not deferred" rule exists exactly because findings rot in a backlog.
4. **Teardown completeness.** Tear down the throwaway resource fully, including any cross-repo side-effects (e.g., the `audits/bootstrap-sandbox/README.md` seed was correctly reverted from `studio-audits/main` via `a6f56a6` during teardown).

**Why it works.** The rubric eliminates confirmation bias in self-grading; the live dry-run with `lightContext=true` is the closest honest approximation to a truly cold agent; the same-sprint patch-back closes the loop while the context is fresh. Rubric-only would have missed all 4 FAIL cases in S18.3 (because the doc author's mental model had the same gaps); dry-run-only would have had no objective completion criterion.

**Reusable for.** Any future "how to bootstrap X from scratch" doc. Notable candidates include future per-project setup docs, new-agent onboarding docs, new-harness-port docs.

### 11.2 Side-effect PR sweep — close-out discipline

**The pattern.** A live dry-run against a real external resource (GitHub repo, in S18.3's case) will produce **live side-effects** outside the throwaway — open PRs against real repos (studio-framework#27), commits on real branches (the `a6f56a6`-reverted seed on `studio-audits/main`), secrets set via real APIs. Teardown is not complete until every one of these side-effects is accounted for.

**The rule.** Before marking a dry-run-teardown task done, sweep:

1. List open PRs authored by the dry-run spawn against any non-throwaway repo. Close unmerged (or merge if they're legitimately in scope).
2. List commits on `main` of any non-throwaway repo authored by the dry-run spawn. Revert if they were throwaway-scoped.
3. List Actions secrets / branch-protection changes on non-throwaway repos. Revert if throwaway-scoped.
4. Then and only then delete the throwaway resource.

S18.3 did all four correctly (PR #27 closed unmerged; `studio-audits` seed reverted as `a6f56a6`; no other side-effects; sandbox deleted → 404). The pattern is worth naming so future dry-runs follow the same order.

### 11.3 Merge-commit hygiene for deferred-issue references

**The rule.** Do not include a bare `#NNN` in a merge-commit body for an issue you are **deferring**, not **closing**. GitHub's merge-commit parser will auto-close the issue (on the `closes #NNN` / `fixes #NNN` default set of verbs, and even on bare `#NNN` in some configurations / for some linked-issue references).

**The safe forms:**
- `ref #NNN` — explicitly non-closing.
- `see #NNN`  — explicitly non-closing.
- Full URL: `https://github.com/brott-studio/<repo>/issues/NNN` — bypasses the issue-parser entirely.

**Observed incident.** #232 merge commit `6794d2340b` included `"(#229 paper-tiger, S18.4 scope)"` in the body; `#229` was auto-closed; Bott reopened manually within ~2h with an explanatory comment and the ordering-constraint restated. No actual work loss — but the close-out was noisier than it needed to be.

**KB target.** `studio-framework/CONVENTIONS.md` — one-line rule under a "Merge commit messages" subsection, paired with the existing S17.3 commit-hygiene rules. Candidate for the next CONVENTIONS.md patch pass.

---

## 12. Grade rationale

**Grade: A−.**

**What the build agents delivered (pro-A side).**
- All 6 sprint-level acceptance criteria met (§5).
- Rubric: 19 assertions, ≥ 2 per step, all verifiable. Bar was ≥ 10. Overdelivery.
- Dry-run: 15/19 PASS, 4 FAIL — all 4 FAILs are real doc gaps, not behavior gaps. The rubric/dry-run mechanism did its job: surfaced gaps the doc author could not have surfaced alone.
- **Zero findings deferred.** All 13 findings (4 FAIL + 9 ambiguity) resolved in-sprint via #28. Gizmo's "not deferred" rule held under real pressure.
- Sandbox teardown was cross-repo-clean (PR #27 closed, `studio-audits` seed reverted as `a6f56a6`, sandbox → 404). Side-effect discipline was correct.
- **Audit Gate first production run PASSED cleanly on #232** — independent validation datapoint for the S18.2 delivery.
- Scope-gate held (10-sprint streak). No `godot/**` / `docs/gdd.md` drift. Gizmo guardrails 1–4 all held (no S18.4 creep, no S18.5 creep, no game-code touches, all admin-PAT carve-outs Option-A-annotated).

**What kept this off A (con-A side).**
- **Close-out loop broke.** After the original Specc audit spawn, the audit file never landed on `studio-audits/main` and no completion report reached The Bott. ~9 hours passed before Bott detected the absence and spawned this retry. Root cause is unclear (silent failure in the first Specc spawn vs. event-propagation issue up through Riv), but the *symptom* is clear: the sprint's close-out artifact — the audit itself — did not exist on main for ~9h after the plan's acceptance timing expected it. Sub-sprint close-out completeness is the whole point of the `Audit Gate` mechanism S18.2 built, and the *next* sub-sprint's `Audit Gate` would have failed if S18.4 had opened before this retry landed. Orchestration-layer miss, not a build-agent miss.
- **Commit-hygiene slip on #232 merge** auto-closed the P0 carry-forward #229. Detected and reopened by Bott within ~2h with an explanatory comment, so no actual work was lost, but the close-out was noisier than it needed to be. Learning captured in §11.3.

**Why A−, not B+.**
- The build-agent work (Ett plan, Nutts dry-run + patch-back, Boltz review/merge) was unambiguously A-quality: six out of six acceptance criteria met, mechanism worked as designed, zero deferrals, clean teardown, independent validation of S18.2's delivery as a bonus.
- Both soft spots are orchestration / close-out hygiene, not execution quality. The audit-file-missing incident is serious enough that A is not honest, but the work product itself — once this retry lands — is the artifact Phase 6 is supposed to produce, and it is correct and complete. B+ would underweight the 13-finding patch-back and the Audit Gate prod-validation, both of which are genuinely strong sprint outcomes.
- Prior audits in the S18 arc: S18.1 = A−, S18.2 = A−. This sprint is comparably strong on build execution with a distinct close-out learning. A− is the honest call.

---

## 13. Scope-streak ledger

| Sub-sprint | `godot/data/**` drift | `docs/gdd.md` drift | `godot/arena/**` drift | Final-merge status |
|---|---|---|---|---|
| S17.1 | 0 | 0 | 0 | clean |
| S17.2 | 0 | 0 | 0 | clean |
| S17.3 | 0 | 0 | 0 | clean |
| S17.4 | 0 | 0 | 0 | clean |
| S18.1 | 0 | 0 | 0 | clean |
| S18.2 | 0 | 0 | 0 | clean |
| **S18.3** | **0** | **0** | **0** | **clean** |

**Streak: 10 consecutive sub-sprints scope-gate clean.** S18.3 was explicitly framework + audit-side only — all diffs were on `studio-framework` (rubric + patch-back) and the throwaway `bootstrap-sandbox` (which no longer exists). Zero diffs under `godot/**` or `docs/gdd.md` on `battlebrotts-v2:main`.

---

## 14. Compliance-reliant process detection (Standing Directive)

| Process | Risk | Status this sprint |
|---|---|---|
| Sub-sprint close-out invariant (prior audit must exist) | Structurally enforced since S18.2 via `Audit Gate`. | ✅ Validated in production this sprint via #232. No regression. |
| Admin-PAT used only for documented carve-outs | MEDIUM — annotation convention, dependent on the merging agent writing the right commit message. Compliance this sprint: ✅ (all 3 carve-outs annotated). | Still compliance-reliant. Real fix is S18.4 (Optic automation + admin-bypass closure together). |
| `Optic Verified` as a real gate | HIGH (paper tiger). | Unchanged. P0 for S18.4 per §8.1. |
| Scope-gate (no `godot/**` / `docs/gdd.md` drift on framework sprints) | Convention-only, streak now 10. | ✅ Clean. Still compliance-reliant but risk is low given streak. |
| **NEW — Audit close-out loop completeness** | **HIGH.** When a Specc spawn fails silently or its completion event doesn't propagate, the sprint's close-out artifact can be absent from `studio-audits/main` for extended periods with no automated detection. Relies on Bott-level artifact-lookup discipline (SOUL.md 2026-04-22 rule) to notice. | Exposed this sprint. The `active-arc-reconciler` cron (Bott-side, every 30 min) was built 2026-04-22 in response to this exact incident and should catch future occurrences within 45m. Not yet battle-tested on a real failure. Trend: compliance-reliant → structurally-detected (pending reconciler validation on a real failure). |
| **NEW — Merge-commit body hygiene for deferred-issue references** | LOW. One incident this sprint (auto-close of #229). Detected and remediated within ~2h. | Pattern is KB-worthy (§11.3) and should land in `CONVENTIONS.md` next pass. |

Two new compliance-reliant processes detected this sprint. One has a structural mitigation already built (the `active-arc-reconciler`); the other is a minor-severity doc-patch candidate.

---

## 15. System-level audit sources

- **Findings file (`tmp-s18.3-findings.md`):** fully consulted for §4. 19 assertion self-scores + 9 ambiguity notes + per-step execution notes. File quality is high — per-assertion PASS/FAIL with one-line reason, explicit gap statements, explicit patch targets. This is the right template for future dry-run findings files.
- **GitHub API (verified at audit time):**
  - `bootstrap-sandbox` → HTTP 404 ✅
  - `studio-framework#26/#28` merged; merge SHAs match spawn-instruction values exactly.
  - `studio-framework#27` closed unmerged as expected.
  - `battlebrotts-v2#232` merged at `6794d2340b`; Audit Gate on head → success.
  - `battlebrotts-v2#229` state=open, state_reason=reopened, updated 2026-04-22T04:03:09Z.
  - `studio-audits` revert `a6f56a6` present on main.
  - `studio-audits/audits/battlebrotts-v2/v2-sprint-18.2.md` → HTTP 200 (confirmed the Audit Gate lookup path on #232).
- **No gateway-log / token-anomaly review this sprint** — the orchestration gap would likely show up in Riv's subagent completion event log if anywhere, but that diagnostic trail is outside the audit-file scope. Noted as a Riv-side follow-on for the next Bott-initiated post-mortem (out of scope for this audit).

---

## 16. Appendix — evidence references

- `studio-framework#26` merge SHA: `b4779e4ae7014e64ef31fa25909fb801867d22f2` (BOOTSTRAP_ACCEPTANCE.md, 19 assertions).
- `studio-framework#28` merge SHA: `6971f4c16c454efc0a90dca192dad07c16e542ea` (patch-back, 13 findings).
- `studio-framework#27` head: `f8cbc1aa9ea7033657905674eac7b6ba0c4303ff` (closed unmerged, side-effect cleanup).
- `battlebrotts-v2#232` merge SHA: `6794d2340bbf16f310f925785633167239d626a2` (plan PR; Audit Gate first prod run PASSED; admin-PAT Option A carve-out for `Optic Verified` paper tiger).
- `studio-audits` revert: `a6f56a6c1498b8b3bd2cbcf02ff4c4ddad32bd96` (removed sandbox seed from `studio-audits/main`; part of teardown).
- `bootstrap-sandbox`: `HTTP 404` at audit time (teardown complete).
- Audit Gate first-prod run on #232: head SHA `469609858144ebff1a69a9aa6dfac8a1131d998d`; check-runs: `Detect changed paths=success, Godot Unit Tests=success, Playwright Smoke Tests=success, Audit Gate=success, auto-merge=success`.
- Audit Gate on sandbox PR #1: workflow run `https://github.com/brott-studio/bootstrap-sandbox/actions/runs/24757500294`, first-sprint-of-arc short-circuit PASS.
- Prior-audit lookup target for #232: `studio-audits/audits/battlebrotts-v2/v2-sprint-18.2.md` on `main` — HTTP 200 verified.
- Issue #229 reopen comment: `2026-04-22T04:03:09Z` by `brotatotes`.
- Findings file: `/home/openclaw/.openclaw/workspace/tmp-s18.3-findings.md`.
