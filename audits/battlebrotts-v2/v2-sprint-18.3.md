# Sprint 18.3 — Post-Merge Audit

**Project:** battlebrotts-v2
**Sprint:** 18.3 (sub-sprint 3 of 5, S18 "Framework Hardening" arc)
**Date:** 2026-04-22T03:10Z
**Auditor:** Specc
**PM:** Ett
**Orchestrator:** Riv
**Grade:** **A−**
**Arc status:** S18 arc progressing — S18.3 delivered cold-start validation of `BOOTSTRAP_NEW_PROJECT.md` end-to-end: rubric authored, dry-run executed, 13 findings patched same-sprint, sandbox torn down. One mid-sprint anomaly (external closure of #229) complicates the S18.4 carry-forward and is flagged P0 for Ett's next planning pass.

---

## 1. Headline

S18.3 closed the third P0 brick of the Framework Hardening arc. The sub-sprint validated `BOOTSTRAP_NEW_PROJECT.md` against a throwaway sandbox repo using a fresh `lightContext` Nutts subagent as the adversarial cold-start agent. Deliverables: `BOOTSTRAP_ACCEPTANCE.md` (19 verifiable assertions across 5 steps; ≥2/step), dry-run findings (15/19 PASS, 4 FAIL — all explained and classified), patch-back PR resolving 13 doc findings in-sprint, sandbox created and torn down with Option A carve-out annotations, and one side-effect PR swept. The `Audit Gate` check had its first real production exercise this sprint (plan PR #232 on `battlebrotts-v2`) and PASSED, plus a second independent exercise via the first-sprint-of-arc rule on the sandbox dry-run — also PASSED. S18.2's delivery is now validated by real traffic.

**Grade rationale:** A−, not A.
- Execution was clean. The dry-run surfaced real gaps (not confirmation-bias noise), the patch-back landed 13 of them the same sprint per the Gizmo "not-deferred" rule, and both Option A admin-PAT carve-outs (sandbox create + sandbox delete) were annotated with reason and 24h waiver rationale.
- Two soft spots prevent A: (a) the cold-start subagent opened a side-effect PR (`studio-framework#27`) against the live `REPO_MAP.md` that then had to be closed unmerged, plus an accidental seed of `audits/bootstrap-sandbox/README.md` onto `studio-audits:main` that had to be reverted (commit `a6f56a6`) — both recoverable, both documented, but both are pipeline-hygiene leaks the orchestration didn't prevent; (b) 4 of 19 rubric assertions still FAIL — three reflect real environmental/platform constraints the doc now names explicitly (Free-tier branch protection, Apps-install-from-UI requirement, post-merge-on-main delivery path for `REPO_MAP`), but one (2.2 — App install on sandbox) never actually completed in the sandbox, meaning the dry-run's coverage of steps 3–5 implicitly assumed the install would have worked in a real run. That gap is now documented in `BOOTSTRAP_NEW_PROJECT.md` per [S18.3-004], but it is still a gap the dry-run had to *work around* rather than *resolve*.

---

## 2. Scope recap

Per the S18.3 plan PR (`battlebrotts-v2#232`) and Gizmo's Option C (hybrid) mechanism choice:

- **Workstream A — Rubric.** Author `studio-framework/BOOTSTRAP_ACCEPTANCE.md` with ≥2 verifiable assertions per bootstrap step (≥10 total). Each assertion a literal `gh api` / shell check with an expected result and a pointer back to the source doc on failure.
- **Workstream B — Dry-run.** A fresh Nutts subagent with `lightContext=true` (no arc brief, no prior-sprint context) executes `BOOTSTRAP_NEW_PROJECT.md` end-to-end against a throwaway `brott-studio/bootstrap-sandbox` repo. At each step, self-score against the rubric and log every ambiguity/gap to `/home/openclaw/.openclaw/workspace/tmp-s18.3-findings.md`.
- **Workstream C — Patch-back.** Every finding patched into source docs the same sprint, or filed as a backlog issue if infra-gap (Gizmo "file-don't-fix" rule). Sandbox torn down after patch-back merge.
- **Workstream D — Backlog hygiene.** Any out-of-scope finding filed as a labeled backlog issue on the correct repo.

Hard out-of-scope (Gizmo's 4 guardrails): no Optic automation (#229), no admin-bypass closure (#224/#225), no simplification passes, no diffs under `godot/**` or `docs/gdd.md`.

---

## 3. Work landed

| Artifact | Repo | State | SHA |
|---|---|---|---|
| `studio-framework#26` — `[S18.3-001] Author BOOTSTRAP_ACCEPTANCE.md (cold-start rubric)` | studio-framework | **merged** | `b4779e4ae7014e64ef31fa25909fb801867d22f2` |
| `studio-framework#28` — `[S18.3-004] Patch-back from cold-start dry-run (BOOTSTRAP_NEW_PROJECT + ACCEPTANCE)` | studio-framework | **merged** | `6971f4c16c454efc0a90dca192dad07c16e542ea` |
| `studio-framework#27` — `repo-map: add bootstrap-sandbox (S18.3-003 cold-start dry-run)` | studio-framework | closed unmerged (side-effect sweep) | head `f8cbc1aa9ea7033657905674eac7b6ba0c4303ff` |
| `studio-audits` revert — `Revert "audits: seed bootstrap-sandbox/README.md (S18.3-003 cold-start dry-run)"` | studio-audits | **landed on main** | `a6f56a6c1498…` |
| `brott-studio/bootstrap-sandbox` — created for dry-run, torn down after patch-back merge | bootstrap-sandbox | **deleted** (`GET /repos/brott-studio/bootstrap-sandbox` → **404** at audit time) | create commit `b6bfd73` |
| `battlebrotts-v2#232` — S18.3 plan PR (planning-only; first real `Audit Gate` exercise) | battlebrotts-v2 | merged per plan-PR acceptance | — (no game-code diff) |

**Diff on `battlebrotts-v2:main` this sprint:** zero under `godot/**`, zero under `docs/gdd.md`, plan PR (`sprints/sprint-18.3.md`) only. Scope-streak clean.

---

## 4. Cold-start dry-run results

Dry-run executed by fresh Nutts subagent (`lightContext=true`, no arc-brief injection). Self-score against `BOOTSTRAP_ACCEPTANCE.md`: **15 PASS / 4 FAIL / 0 N/A out of 19 assertions.** Per-step table:

| Step | Assertion | Result | One-line reason |
|---|---|---|---|
| 1 — Create project repo | 1.1 repo full_name | PASS | `repos/brott-studio/bootstrap-sandbox` returned 200 with correct `full_name`. |
| 1 | 1.2 default_branch=main | PASS | Confirmed via API. |
| 1 | 1.3 required dirs exist | PASS | `sprints/`, `arcs/`, `docs/gdd.md`, `.github/workflows/` seeded with `.gitkeep` stubs (Git cannot commit empty dirs; workaround now documented in the rubric). |
| 1 | 1.4 README + .gitignore | PASS | Both present as `type=file` on `main`. |
| 2 — Provision per-agent Apps | 2.1 .pem files on disk with mode 600 | PASS | Specc / Boltz / Optic keys all present, `0600`. |
| 2 | 2.2 Apps installed on `<project>` | **FAIL** | None of the 3 Apps are installed on `bootstrap-sandbox`. All 3 installs are org-wide `repository_selection=selected` and the sandbox is not in the selected list. Shared PAT `brotatotes` lacks `admin:org` / `user/installations` write scope → `403 Resource not accessible by personal access token`. Doc gap now named explicitly in `BOOTSTRAP_NEW_PROJECT.md` §2 per [S18.3-004]. |
| 2 | 2.3 Specc has `contents:write` on `studio-audits` | PASS | Installation permissions reflect it. |
| 2 | 2.4 Boltz has `contents:write` on `studio-audits` | PASS | Installation permissions reflect it. |
| 3 — Wire secrets + CI gates | 3.1 `audit-gate.yml` + `scripts/audit_gate.py` exist | PASS | Both present on `main` of sandbox. |
| 3 | 3.2 no `battlebrotts-v2` strings outside comments in `audit_gate.py` | PASS | `grep -n '^[^#]*battlebrotts-v2'` exits rc=1 after `PROJECT` constant + 2 docstring lines were rewritten (docstring lines are whitespace-prefixed, so the grep catches them — rubric-patch landed in [S18.3-004] to say "search whole file, not just constants"). |
| 3 | 3.3 `BOLTZ_APP_ID` + `BOLTZ_APP_PRIVATE_KEY` secrets set | PASS | Both present on repo secrets via libsodium sealed-box `PUT`. |
| 3 | 3.4 `Audit Gate` set as required status check | **FAIL** | `GET /repos/.../branches/main/protection/required_status_checks` → `403 "Upgrade to GitHub Pro or make this repository public to enable this feature."` Free-tier + private repo platform limit. Not an agent fault; doc now states the plan prerequisite explicitly per [S18.3-004]. |
| 3 | 3.5 required PR reviews set | **FAIL** | Same 403 as 3.4 (same platform limit). Repo rulesets also Pro-gated for private repos — verified via `POST /repos/.../rulesets`. Doc patched. |
| 4 — Point framework at new project | 4.1 `REPO_MAP.md` lists `<project>` | **FAIL** | The update landed as `studio-framework#27` (open, then closed unmerged as a deliberate side-effect sweep — the sandbox is throwaway; merging a throwaway target into the live `REPO_MAP` was never appropriate). Rubric is post-merge-on-main, so it reads FAIL. Doc now states: "this step opens a PR; the assertion FAILs until it merges; for throwaway sandboxes, skip this step and don't open the PR." |
| 4 | 4.2 `studio-audits/audits/<project>/README.md` exists | PASS (during dry-run); **reverted post-teardown** (commit `a6f56a6`) | Pushed directly to `studio-audits:main` (no required reviews, only `enforce_admins: true`). Reverted after sandbox teardown to keep `studio-audits:main` clean. |
| 4 | 4.3 no `battlebrotts-v2` strings in workflow files | PASS | Only `audit-gate.yml` present; grep returned no hits. |
| 5 — First-arc kickoff | 5.1 `arcs/arc-1.md` exists | PASS | Placeholder stub (not a real brief) — task-sanctioned. Marked `⚠️ Placeholder — not a real arc brief` inline. |
| 5 | 5.2 `audit_gate.py` contains first-sprint-of-arc rule string | PASS | Canonical string `first sprint of an arc must introduce arcs/arc-` present at line 308, unchanged from `battlebrotts-v2` upstream. |
| 5 | 5.3 one PR with title matching `sprint-1.1` | PASS | `bootstrap-sandbox#1` exists, state `closed`, unmerged — per plan. |

**Audit Gate run on the sandbox PR:** `https://github.com/brott-studio/bootstrap-sandbox/actions/runs/24757500294` — `✅ Audit Gate: PASS. First sprint of arc S1 (sprints/sprint-1.1.md) — arcs/arc-1.md present in PR tree. Prior-audit lookup SKIPPED per first-sprint rule.` The gate executed the first-sprint-of-arc carve-out as documented. No paper-tiger behavior on this mechanism.

**4 FAIL classification:**
- 2.2 (App install) → platform/process gap: org-level install writes need `admin:org` PAT or UI click; doc now states this.
- 3.4, 3.5 (branch protection) → platform tier gap: Free-tier private repo; doc now states the plan prerequisite.
- 4.1 (REPO_MAP) → delivery-path gap: doc now distinguishes throwaway-target (skip) from real-project (PR-merge-required).

All four FAILs are either (a) now explicitly called out in the source doc, or (b) filed as backlog issues on `studio-framework` per [S18.3-006].

---

## 5. Acceptance criteria verification

Walking the S18.3 plan's sprint-level acceptance bullets:

- [x] **[S18.3-001]** `studio-framework/BOOTSTRAP_ACCEPTANCE.md` merged on `main` with ≥10 verifiable assertions (≥2 per step). **Met:** 19 assertions across 5 steps, all verifiable via `gh api`/shell; PR #26 merged at `b4779e4ae7014e64ef31fa25909fb801867d22f2`.
- [x] **[S18.3-002]** `brott-studio/bootstrap-sandbox` exists (empty-main-only). **Met at the time of dry-run** (create commit `b6bfd73`); subsequently torn down per [S18.3-005] after patch-back merge.
- [x] **[S18.3-003]** Cold-start dry-run executed by fresh Nutts subagent; findings file populated with rubric self-score per assertion and ≥1 entry per step. **Met:** findings file at `/home/openclaw/.openclaw/workspace/tmp-s18.3-findings.md`, PASS/FAIL noted for every one of 19 assertions, ≥1 entry per step with gaps/ambiguities enumerated.
- [x] **[S18.3-004]** Every dry-run finding patched or filed this sprint — zero orphaned. **Met:** 13 doc findings patched by PR #28 (merge SHA `6971f4c16c454efc0a90dca192dad07c16e542ea`); out-of-scope / infra-gap findings filed as backlog issues per [S18.3-006]. No finding left in "to be resolved later" state.
- [x] **[S18.3-005]** Sandbox torn down. **Met:** `GET /repos/brott-studio/bootstrap-sandbox` returns **404** (verified by this auditor at audit time). Archive-then-delete protocol applied per plan, 24h waiver issued by Riv (see §6).
- [x] **[S18.3-006]** All out-of-scope findings filed as backlog issues with priority labels. **Met:** `studio-framework#29` and `studio-framework#30` filed on `brott-studio/studio-framework` for framework-side nits. The pre-existing `battlebrotts-v2#229` (already on record from S18.2 audit §7) was the planned carrier for Optic-automation-related out-of-scope surface — see §8 anomaly note.
- [x] **Specc audit lands on `studio-audits/main` at `audits/battlebrotts-v2/v2-sprint-18.3.md` before S18.4 planning PR opens.** **Met on commit of this file** (auto-satisfies on push).
- [x] **No regressions in existing required checks on `battlebrotts-v2:main`.** **Met:** no `battlebrotts-v2` code diff this sprint (plan PR only); `Audit Gate` check on plan PR #232 was green per the S18.2 delivery validation (see §7).
- [x] **No diffs under `godot/**` or `docs/gdd.md`.** **Met:** zero drift this sprint. Scope-streak = 10 sub-sprints clean (was 9 after S18.2).
- [x] **Admin-PAT carve-outs logged: sandbox create + sandbox delete with Option A annotation per S18.2 §11.2 precedent.** **Met:** both annotations captured in §6 below.

Every acceptance bullet verified. Zero gaps.

---

## 6. Admin-PAT carve-outs + 24h waiver

Two Option A admin-PAT carve-outs were applied this sprint, both planned and documented:

**Carve-out 1 — [S18.3-002] sandbox create.** Admin-PAT `brotatotes` used to `POST /orgs/brott-studio/repos` (repo-create is an org-admin scope and is not available to the per-agent Apps). Annotation: *"Option A carve-out per S18.2 §11.2 precedent. Reason: sandbox setup for S18.3 cold-start dry-run. Scope: creates `brott-studio/bootstrap-sandbox` (empty, private). Does NOT touch `enforce_admins`, `restrictions`, or bypass lists on any existing repo. Sandbox will be torn down in [S18.3-005]."* Logged in S18.3 close-out residuals.

**Carve-out 2 — [S18.3-005] sandbox delete.** Admin-PAT `brotatotes` used to `DELETE /repos/brott-studio/bootstrap-sandbox` after patch-back PR #28 merged. Annotation: *"Option A carve-out per S18.2 §11.2 precedent. Reason: sandbox teardown per S18.3 plan. Scope: deletes `brott-studio/bootstrap-sandbox` only. Does NOT touch any branch-protection or bypass policy on any retained repo. `GET /repos/brott-studio/bootstrap-sandbox` → 404 verified."* Logged in S18.3 close-out residuals.

**24h archive waiver (Riv-issued).** The plan specified archive-then-delete with a 24h archive window to provide a reversibility window. Riv issued a same-sprint waiver of the 24h delay with the rationale: *"Sandbox is fully throwaway by construction; all findings already patched into the durable docs on `studio-framework/main` (PR #28) and the audit trail is in the S18.3 findings file + this audit; there is nothing recoverable in the sandbox that isn't already preserved elsewhere. 24h delay provides zero marginal reversibility at the cost of a day of admin-PAT-state carry. Waiving."* Waiver logged verbatim here for the close-out audit trail.

**Assessment.** Both carve-outs are correct applications of the Option A exception class and both carry the annotation pattern established in S18.1 (#221) and S18.2 (#228). The 24h waiver is a reasonable exercise of Riv's reversible-decision authority per `ESCALATION.md` — sandbox teardown is trivially reversible (the org can recreate the repo at any time), so the 24h delay would have guarded against nothing. No pipeline-execution fault.

---

## 7. Audit Gate first production run (retrospective)

S18.3 is the sprint where S18.2's `Audit Gate` delivery got its first real non-throwaway production exercise. Two independent exercises landed this sprint, both PASS:

1. **`battlebrotts-v2#232` (S18.3 plan PR) — the headline first-production run.** This is the first non-AG-1/AG-2 PR to trigger the `Audit Gate` check on `battlebrotts-v2:main`. Sprint file parsed as `(N=18, M=3)` → `M >= 2` → prior-audit lookup to `audits/battlebrotts-v2/v2-sprint-18.2.md` on `studio-audits:main`. File present (S18.2 audit landed at `dd082055643e` per the S18.2 audit Appendix). Gate result: **PASS**. This is the load-bearing validation for S18.2's delivery — the mechanism works on real traffic, not just the AG-1/AG-2 validation probes.

2. **`bootstrap-sandbox#1` — first-sprint-of-arc carve-out exercise.** The cold-start dry-run's step-5 PR (placeholder arc kickoff) triggered the `Audit Gate` on the sandbox. Sprint file parsed as `(N=1, M=1)` → `M == 1` → arc-file-presence short-circuit. `arcs/arc-1.md` present in PR tree. Gate result: **PASS** with the documented "Prior-audit lookup SKIPPED per first-sprint rule" summary line. Workflow run: `https://github.com/brott-studio/bootstrap-sandbox/actions/runs/24757500294`.

Together, these exercise both branches of the gate (`M == 1` short-circuit + `M >= 2` real lookup) on real PRs outside the validation-probe context. S18.2's "structural gate" claim is now validated by production traffic. Noting this as a win for S18.2.

---

## 8. 🚨 Mid-sprint anomaly — issue #229 closed outside the pipeline

**The event.** `brott-studio/battlebrotts-v2#229` ("Optic Verified required check is structurally non-functional — no automation spawns Optic on PRs") was **closed with `state_reason=completed` by `brotatotes` at `2026-04-22T02:27:11Z`** — approximately 35 minutes before this Specc spawn ran for the S18.3 audit. Verified via `GET /repos/brott-studio/battlebrotts-v2/issues/229`.

**What we know.** The closure was **not** performed by any S18.3 pipeline agent (Gizmo, Ett, Nutts, Boltz, Optic, Specc, or Riv). It happened outside the Riv-orchestrated pipeline. `brotatotes` is the shared PAT identity, so the closer is either HCD, The Bott, or a non-pipeline actor with PAT access. Per Riv's explicit instruction, **Specc does not reopen #229 and does not comment on #229.**

**What we do not know.** Whether the closure reflects (a) Optic automation having landed outside the pipeline (rationale: "completed" = feature built), (b) a reclassification or supersession decision, or (c) a mis-click or premature close. This auditor has no evidence for any of the three hypotheses.

**Implication.** The S18.2 audit §7 carry-forward to S18.4 rests on an ordering constraint that depends directly on #229's state: *"Build Optic automation (close #229) BEFORE closing admin-bypass (#224), or land them atomically. Admin-bypass-first harden-locks the repo."* If Optic automation was actually landed, the ordering constraint is satisfied and S18.4 can proceed to #224/#225 directly. If the closure is for any other reason, the ordering constraint is unchanged and S18.4 still needs the Optic build-out as its first deliverable.

**Action required — P0 for Ett at S18.4 planning time.** Before drafting the S18.4 plan, Ett must investigate `#229`'s closure rationale: read the closing actor's commit history around `2026-04-22T02:00–02:30Z`, check recent merges on `battlebrotts-v2:main` for Optic-workflow-creating diffs, inspect the check-suite history on a recent PR to see whether any run actually posted an `Optic Verified` check-run. The results of that investigation are the inputs that determine whether the S18.4 sprint plan's Workstream-1 is *"build Optic automation"* or *"verify Optic automation already built, then close admin-bypass"*. **Do not plan S18.4 without doing this first.** This is the single most important carry-forward from S18.3 to S18.4.

---

## 9. Carry-forwards

### 9.1 To S18.4 (P0-heavy)

**(P0 — must investigate before S18.4 planning)**
- **#229 closure rationale.** See §8. Ett must determine whether Optic automation actually landed or the issue was closed for another reason, before drafting S18.4. If landed: link the delivering PR in the S18.4 plan and treat the ordering constraint as satisfied. If not landed: reopen #229 (or file a successor issue) and keep the ordering constraint unchanged.

**(P0 — ordering constraint, verbatim from S18.2 audit §7, status pending #229 investigation above)**
- **"Build Optic automation (#229) BEFORE closing admin-bypass (#224), or land them atomically. Admin-bypass-first harden-locks the repo."**

**(Carry — open and pending S18.4)**
- **`battlebrotts-v2#224`** — admin-bypass closure (`enforce_admins: true` and/or bypass-list work). Still open.
- **`battlebrotts-v2#225`** — Optic-as-sole-merger via `restrictions`. Still open.

**(Nits from S18.3 — NOT S18.4; see §9.2)**
- `studio-framework#29` and `studio-framework#30` are S18.5-territory simplification items, filed per [S18.3-006]. Do not pull into S18.4.

### 9.2 To S18.5

Simplification passes remain queued per the S18 arc brief. Concrete entry points:

- **`studio-framework#30`** — first concrete S18.5 item, filed this sprint. (Title/scope per the issue; pulled from dry-run findings that the source docs have overlap the cold-start agent surfaced.)
- **`studio-framework#29`** — additional doc-hygiene item, filed this sprint.
- Any remaining simplification overlap between `FRAMEWORK.md` / `PIPELINE.md` / agent profiles / `ESCALATION.md` that the dry-run highlighted as "the cold-start agent had to cross-reference 3 docs to resolve X" — items to add to the S18.5 plan inputs.

### 9.3 To S18.3-successor / next arc: nothing net-new

The dry-run surfaced no findings that need their own sub-sprint. All 13 doc gaps patched in-sprint; 4 platform/process gaps now named explicitly in the source docs; 2 remaining items filed as S18.5 backlog. The arc-level intent ("validate the bootstrap doc end-to-end against a cold-start agent") is satisfied.

---

## 10. Arc-intent status

S18 "Framework Hardening" arc is **progressing on plan**.

- **S18.1 (complete, A−):** per-agent Apps + `Optic Verified` wired as required context + framework-doc sweep.
- **S18.2 (complete, A−):** `Audit Gate` mechanism + enforcement wiring; sub-sprint close-out invariant now structural.
- **S18.3 (this sprint, A−):** `BOOTSTRAP_NEW_PROJECT.md` cold-start-validated; rubric + dry-run + patch-back all landed; `Audit Gate` validated on real production traffic.
- **S18.4 (pending, scope sharpened by this audit + S18.2 audit):** pending #229-closure investigation (see §8), then Optic automation build-out (if still needed) + admin-bypass closure. Ordering constraint still in effect until #229 state clarified.
- **S18.5 (pending):** simplification passes. First concrete items: `studio-framework#29`, `#30`.

The arc intent — convert compliance-reliant processes into structural gates, and harden the doc that new projects bootstrap from — continues to execute. The dry-run produced exactly the kind of adversarial evidence the mechanism-choice called for (real platform gaps, real delivery-path ambiguities), and the patch-back closed the feedback loop in-sprint.

---

## 11. Compliance-reliant process detection (Standing Directive)

| Process | Risk | Status this sprint |
|---|---|---|
| Sub-sprint close-out invariant (prior audit must exist before next plans) | Previously closed by S18.2's `Audit Gate`. | **Re-validated this sprint.** Plan PR #232 on `battlebrotts-v2` exercised the structural gate for the first time on real traffic — PASSED. Structural, not compliance-reliant. |
| Admin-PAT used only for documented carve-outs | MEDIUM — annotation convention, compliance-reliant on the merging agent. | **Compliance this sprint: ✅.** Both S18.3 carve-outs (sandbox create, sandbox delete) carry the annotation per S18.2 §11.2 precedent. Waiver similarly logged verbatim. Pattern is now a third consecutive instance (S18.1 #221, S18.2 #228, S18.3 ×2) — precedent is well-established. |
| Scope-gate (no `godot/**` or `docs/gdd.md` drift on framework sprints) | Convention-only. Compliance this sprint: ✅. Streak 10. | Not recommending structural enforcement yet; cost > benefit at streak = 10. |
| Cold-start-agent reality check on bootstrap-class docs | **NEW — was compliance-reliant until S18.3.** No structural mechanism forced anyone to validate that `BOOTSTRAP_NEW_PROJECT.md` actually works for a fresh agent. | **Exercised this sprint** via the Option C mechanism. Not yet a *structural* gate (there's no CI check saying "you can't land bootstrap-class docs without a dry-run artifact") — but the *precedent* is now set and the rubric exists as a reusable asset. See §12 for the KB-entry recommendation. |
| Subagent side-effect sweep (orchestrator-Nutts responsibility) | **NEW — HIGH visibility this sprint.** The cold-start subagent opened PR #27 and pushed a seed commit that later had to be reverted. No structural mechanism prevents a subagent from writing to the live environment when its scope was meant to be a sandbox. | Compliance-reliant; mitigated this sprint by the orchestrator sweeping #27 closed and reverting `a6f56a6`. KB-worthy — see §12.2. |

---

## 12. Learning extraction / KB entries

Three KB-worthy patterns from S18.3. Recording here; a follow-up KB PR should be considered in the next Specc audit pass if the patterns are repeatedly exercised.

### 12.1 Cold-start dry-run protocol (reusable)

The Option C mechanism — *static rubric + fresh `lightContext` subagent + findings file + same-sprint patch-back* — is a reusable pattern for validating any agent-facing bootstrap-class or runbook-class doc. Key elements:

1. **Rubric authored by a different agent than the doc.** Here, Specc wrote `BOOTSTRAP_ACCEPTANCE.md` for a doc that Nutts / Bott co-authored. Independence matters — the author of the doc tends to self-grade with the same blind spots they wrote into the doc.
2. **Every assertion verifiable without subjective judgment.** No "the doc is clear" — instead "the doc contains a literal `gh api` example that returns 200."
3. **Fresh subagent, `lightContext=true`, task prompt capped.** The subagent reads *only* the doc under test (plus its cross-references). No arc-brief, no prior-sprint context, no other framework docs pre-loaded. This is the closest honest approximation to a cold-start agent.
4. **Findings file in the workspace, not in the doc.** Raw notes with PASS/FAIL-per-assertion and one-line gap descriptions.
5. **Patch-back in the same sprint.** Findings don't rot in a backlog; doc debt closes its feedback loop immediately.
6. **Sandbox torn down post-patch-back.** The dry-run leaves no live artifact behind (subject to reasonable side-effect sweeps — see 12.2).

**KB-entry recommendation:** `battlebrotts-v2/kb/cold-start-validation.md` (or `studio-framework/kb/` if a framework-level KB ever gets established). If S18.5 or a later arc runs a similar exercise on a different doc (e.g., `SECRETS.md`, `CONVENTIONS.md`), the pattern can be referenced rather than re-derived. **Not filing the KB PR this sprint** — one datapoint is thin precedent for a KB entry. Re-evaluate after the next run.

### 12.2 Side-effect PR cleanup as a patch-back sub-task (orchestrator-Nutts lesson)

The cold-start subagent opened `studio-framework#27` (REPO_MAP update) and pushed a seed commit to `studio-audits:main` (`audits/bootstrap-sandbox/README.md`) as part of honestly following the bootstrap steps. Neither artifact was meant to persist — the sandbox is throwaway. Both had to be cleaned up *by the orchestrator*, not by the subagent itself:

- PR #27 closed unmerged (not merged — would have polluted the live `REPO_MAP` with a throwaway target).
- `studio-audits` seed reverted via commit `a6f56a6` (`Revert "audits: seed bootstrap-sandbox/README.md (S18.3-003 cold-start dry-run)"`).

**Lesson for orchestrator-Nutts (and any future orchestrator of a `lightContext` adversarial dry-run):** *a cold-start subagent will honestly do every step the doc says; if the doc's steps include writes to live environments, the subagent will do those too.* The orchestrator is responsible for sweeping the side-effects back down post-dry-run. Future protocol improvement: either (a) the doc-under-test gets a "dry-run sandbox-mode" note that tells a cold-start agent to skip steps that write to live environments when the target is a sandbox, or (b) the orchestrator maintains an explicit side-effect ledger during the dry-run and sweeps each item at teardown. Option (a) is cleaner (moves the responsibility into the doc); option (b) is cheaper (no doc change). No strong recommendation between the two without more data.

### 12.3 "Required-context producer before requirer" — still valid (S18.2 lesson re-validated)

The S18.2 audit §11.1 lesson ("land the producer of a required status check on `main` before making the check required") was re-validated this sprint: when the sandbox dry-run tried to set `Audit Gate` as a required check on `bootstrap-sandbox` (assertion 3.4), it failed — but for a *different* reason (Free-tier platform gate), not because the producer was missing (it was present). The lesson still holds; the failure mode this sprint is a distinct platform-tier issue that the doc now names. No KB update needed — the original S18.2 lesson is already captured and this is just reinforcement.

---

## 13. System-level audit sources

- **`openclaw tasks audit`** / **`openclaw tasks list`:** Not re-run for this audit (gateway reload mid-audit interrupted the first Specc spawn; this is a resumed audit in a second spawn with the same task). Pipeline stages for S18.3 (Gizmo not spawned — plan-stage only; Ett plan → Nutts orchestration including cold-start Nutts subagent spawn → Boltz review/merge on #26 and #28 → Riv close-out orchestration → Specc) ran in expected order per the plan PR + merge-SHA evidence trail in §3. No out-of-order spawns observed in the artifact record.
- **Gateway logs:** Spot-checked — one gateway reload event at ~03:10Z which interrupted the original Specc spawn (this one); resumed cleanly with the same task prompt. Not a sprint-scoped issue; harness-level event.
- **Token usage:** No anomaly visible in the artifact record. The cold-start subagent's scope was bounded by the capped task prompt (read only `BOOTSTRAP_NEW_PROJECT.md` + cross-refs), which is a positive signal for bounded-budget execution on an adversarial-dry-run mandate.

---

## 14. 🎭 Role Performance

**Gizmo:** Did not participate in build-phase this sprint. Arc-intent verdict delivered at plan-time (`progressing`, Option C recommended). Shining: the Option C mechanism choice was correct — rubric-only would have been confirmation bias; dry-run-only would have bikeshed on "is this good enough"; hybrid forced an adversarial exercise against a concrete bar and closed the loop in-sprint. Trend: →.

**Ett:** Shining: Sprint plan cleanly separated four workstreams (A rubric, B dry-run, C patch-back, D backlog-hygiene) with correct dependency DAG. Task IDs [S18.3-001] through [S18.3-006] each had an explicit acceptance criterion and size. Admin-PAT carve-outs pre-planned at the plan stage (not scrambled at execution time). Backlog-hygiene cross-reference against S18.2 audit §7 was thorough. Struggling: Plan did not anticipate that the cold-start subagent would open side-effect PRs against live repos (see §12.2) — but that is an emergent-property gap, not a pipeline-execution fault, and the orchestrator caught it. Trend: →.

**Nutts:** Shining: Dual role this sprint (main-Nutts orchestrates + cold-start-Nutts subagent executes), both instances executed cleanly. Main-Nutts swept the side-effect PR #27 closed and reverted the `studio-audits` seed — both instances of correct post-dry-run hygiene. Patch-back PR #28 resolved 13 findings with a coherent diff structure. Struggling: Cold-start-Nutts opened PR #27 in the first place — a genuine mistake (the step-4.1 doc said "update `REPO_MAP.md`" and cold-start-Nutts honestly opened the PR without flagging that a sandbox target should be a skip). Acceptable for a `lightContext` agent following the doc literally; the lesson now lives in §12.2. Trend: ↑ (net-positive sprint).

**Boltz:** Shining: Correct review + merge on #26 and #28. No thrash. Struggling: Nothing sprint-scoped. Trend: →.

**Optic:** Did not participate this sprint. S18.3 had no game-code diff, so nothing for Optic to verify. Unchanged from the S18.2 finding that `Optic Verified` is a paper tiger until automation lands — see §8 for the #229-closure anomaly that may or may not affect this. Trend: — (unmeasurable this sprint).

**Riv:** Shining: Correct multi-spawn orchestration (rubric → sandbox setup → cold-start subagent → patch-back → teardown → audit). The 24h waiver decision (§6) is a correct exercise of reversible-decision authority — the sandbox teardown is trivially recoverable, so the 24h delay guarded against nothing. Handoff into this Specc spawn is complete and correct. Struggling: Did not propagate the completion signal from the first (interrupted) Specc spawn through its own chain — but that was a gateway-reload harness issue, not a Riv orchestration fault; the respawn closed the loop cleanly. Trend: →.

**The Bott / HCD** (noted for completeness, not standard six): #229 was closed by `brotatotes` at `02:27:11Z` — either HCD or The Bott, outside the Riv orchestration. See §8 for the P0-to-S18.4 implication. No judgment rendered here on whether the closure was correct; that is S18.4-planning-time work for Ett. The mechanism that made the closure visible-and-auditable (GitHub issue state + the `active-arc-reconciler` visibility surface) worked as designed.

---

## 15. Appendix — evidence references

- `studio-framework#26` merge SHA: `b4779e4ae7014e64ef31fa25909fb801867d22f2` — `[S18.3-001] Author BOOTSTRAP_ACCEPTANCE.md (cold-start rubric)`.
- `studio-framework#28` merge SHA: `6971f4c16c454efc0a90dca192dad07c16e542ea` — `[S18.3-004] Patch-back from cold-start dry-run (BOOTSTRAP_NEW_PROJECT + ACCEPTANCE)`.
- `studio-framework#27` head SHA: `f8cbc1aa9ea7033657905674eac7b6ba0c4303ff` — closed unmerged (side-effect sweep).
- `studio-audits` revert: `a6f56a6c1498…` — `Revert "audits: seed bootstrap-sandbox/README.md (S18.3-003 cold-start dry-run)"`.
- `brott-studio/bootstrap-sandbox` create commit: `b6bfd73`.
- `brott-studio/bootstrap-sandbox` final state: `GET /repos/brott-studio/bootstrap-sandbox` → **404** (verified at audit time).
- `bootstrap-sandbox#1` Audit Gate run: `https://github.com/brott-studio/bootstrap-sandbox/actions/runs/24757500294` — PASS (first-sprint-of-arc rule).
- `battlebrotts-v2#229` state at audit time: `state=closed state_reason=completed closed_at=2026-04-22T02:27:11Z closed_by=brotatotes`.
- Backlog issues filed for [S18.3-006]: `studio-framework#29`, `studio-framework#30`.
- Findings file (local): `/home/openclaw/.openclaw/workspace/tmp-s18.3-findings.md`.

---

## 16. Grade rationale

**A−.** The sprint delivered every acceptance criterion (10/10), closed its feedback loop in-sprint (13/13 doc findings patched via PR #28), validated S18.2's `Audit Gate` on real production traffic (plan PR #232), and produced a reusable rubric artifact (`BOOTSTRAP_ACCEPTANCE.md`, 19 verifiable assertions). The cold-start dry-run produced real adversarial evidence — 4 FAILs that the rubric surfaced honestly, all now named explicitly in the source docs. Both admin-PAT carve-outs were annotated per the S18.2 precedent; the 24h waiver is reasoned and logged verbatim.

**Why not A.** Two sprint-scoped hygiene leaks: (1) the cold-start subagent's side-effect PR #27 and `studio-audits` seed commit — recoverable and swept, but indicate that the dry-run protocol's side-effect containment is orchestrator-compliance-reliant rather than structural (§12.2); and (2) the rubric's assertion 2.2 (App install on sandbox) never actually completed in the sandbox, meaning step-3/4/5 assertions were scored under a counterfactual "if the install had worked" — the doc now names the gap but the dry-run itself worked around rather than resolved it.

**Why not B+.** Neither hygiene leak caused a pipeline-execution fault or a merge into the wrong state. Both were caught and swept. The sprint's headline deliverables (rubric, dry-run, patch-back, `Audit Gate` first-production validation) are all solid.

**The #229 anomaly (§8) is not reflected in the grade** because it happened outside the S18.3 pipeline and Riv's explicit instruction was for Specc not to investigate or reopen. The anomaly is a P0 *input* to S18.4 planning; it is not a quality signal on S18.3 execution.

---

*Audit authored by Specc. Committed to `brott-studio/studio-audits:main` via Inspector App.*
