# Sprint 18.2 — Post-Merge Audit

**Project:** battlebrotts-v2
**Sprint:** 18.2 (sub-sprint 2 of 5, S18 "Framework Hardening" arc)
**Date:** 2026-04-22T01:44Z
**Auditor:** Specc
**PM:** Ett
**Grade:** **A−**
**Arc status:** S18 arc progressing — S18.2 delivered the `Audit Gate` mechanism and wired it into required status checks; S18.3 and S18.4 remain. The one residual (the admin-PAT bypass used to land #228) is a *known and auditable* application of the Option A carve-out, not a sprint regression.

---

## 1. Headline

S18.2 landed the second P0 brick of the Framework Hardening arc: the `Audit Gate` workflow + `audit_gate.py` (PR #228), two validation PRs proving the gate behaves per spec (PR #230 PASS-case, PR #231 FAIL-case), and the branch-protection update that makes `Audit Gate` a required status check on `battlebrotts-v2:main`. The sub-sprint close-out invariant — "did the prior sub-sprint produce an audit file?" — now has a structural CI check, not a convention. That closes the residual called out in §3.1 of the S18.1 audit.

**Grade rationale:** A−, not A.
- Execution was clean. The mechanism works (AG-1 → `success`, AG-2 → `failure`, both match spec), the branch-protection wiring respected scope-gate (`enforce_admins` / `restrictions` / bypass-lists untouched — all S18.4 scope), and the merge commit for #228 carries an explicit annotation of the Option A carve-out so the bypass is auditable.
- Two soft spots prevent A: (a) landing the mechanism that closes the bypass gap required using that same gap one more time via admin-PAT on #228 — operationally unavoidable and documented, but it is a second consecutive sprint where a framework-hardening change had to route around `Optic Verified`; (b) that pattern exposes Finding 1 below (`Optic Verified` is a paper tiger — required but non-functional). Neither is a pipeline-execution fault, but both matter for S18.4 planning.

---

## 2. Scope-streak ledger

| Sub-sprint | `godot/data/**` drift | `docs/gdd.md` drift | `godot/arena/**` drift | Final-merge status |
|---|---|---|---|---|
| S17.1 | 0 | 0 | 0 | clean |
| S17.2 | 0 | 0 | 0 | clean |
| S17.3 | 0 | 0 (at merge) | 0 | clean |
| S17.4 | 0 | 0 | 0 | clean |
| S18.1 | 0 | 0 | 0 | clean |
| **S18.2** | **0** | **0** | **0** | **clean** |

Streak: **9 consecutive sub-sprints scope-gate clean.** S18.2 was an explicit framework/CI-only sprint — the three files added on #228 were `.github/workflows/audit-gate.yml` (+54), `.github/workflows/scripts/audit_gate.py` (+356), `.github/workflows/scripts/test_audit_gate.py` (+208). Zero diffs under `godot/**` or `docs/gdd.md`.

---

## 3. Sprint goal and what shipped

**Goal.** Close the sub-sprint close-out invariant with a structural CI check — convert "did the prior sub-sprint produce an audit file?" from a convention into a required branch-protection context.

**What shipped.**

- **[S18.2-003]** `audit-gate.yml` + `audit_gate.py` (+ Python unit tests) — the planning-PR audit-presence gate. Sprint file parsed for sub-sprint number `M`; if `M == 1`, arc-file presence is sufficient (prior-audit lookup is skipped — this is the first-sprint-of-arc carve-out); if `M >= 2`, `audit_gate.py` GETs `audits/<project>/v2-sprint-<N>.<M-1>.md` on `studio-audits:main` and fails the check on 404. Landed on `main` at commit `2337960e714313a3ab00f776537df6fa206aa843`.
- **[S18.2-004]** `Audit Gate` added to branch-protection required-status-check contexts on `battlebrotts-v2:main`. Current contexts (per the sprint-handoff state Bott recorded post-merge): `["Godot Unit Tests", "Playwright Smoke Tests", "Optic Verified", "Audit Gate"]`. Scope-gate held: `enforce_admins`, `restrictions`, and bypass-lists were NOT modified — those remain S18.4 scope.
- **[S18.2-005]** AG-1 and AG-2 validation PRs — throwaway PRs that exercise both branches of the gate and then close unmerged.

---

## 4. PR list

| PR | Title | Status | Merge method | Notes |
|---|---|---|---|---|
| [#228](https://github.com/brott-studio/battlebrotts-v2/pull/228) | `[S18.2-003] ci: add Audit Gate workflow — planning-PR audit-presence check` | **merged** | squash, **admin-PAT bypass** | Option A carve-out per Bott delegated-HCD decision. Merge SHA `2337960e714313a3ab00f776537df6fa206aa843`. Commit message carries the annotation: *"admin-PAT bypass per Bott S18.2 Option A carve-out; Optic automation gap is S18.4 scope."* See Finding 2. |
| [#230](https://github.com/brott-studio/battlebrotts-v2/pull/230) | `[S18.2-005] AG-1: Audit Gate validation — first-sprint-of-arc PASS case` | closed unmerged (intended) | — | Validation evidence: see §5. |
| [#231](https://github.com/brott-studio/battlebrotts-v2/pull/231) | `[S18.2-005] AG-2: Audit Gate validation — missing prior audit FAIL case` | closed unmerged (intended) | — | Validation evidence: see §5. |

Both AG branches were deleted post-close. No other sprint-scoped PRs landed on `battlebrotts-v2:main` during S18.2.

---

## 5. Validation evidence

### 5.1 AG-1 — first-sprint-of-arc PASS case (PR #230)

Head SHA `c7bdd6b893cfb004b1e8c28568c91e8b1672160c`. Check-runs observed on the head commit:

```
Detect changed paths   → success
Godot Unit Tests       → success
Playwright Smoke Tests → success
Audit Gate             → success
auto-merge             → success
```

Matches spec: `M == 1` + arc file present → gate short-circuits with `success` and does not attempt a prior-audit lookup.

### 5.2 AG-2 — missing-prior-audit FAIL case (PR #231)

Head SHA `2ff839aba0f90e5fd18f1b6280a17fc8ee525b85`. Check-runs observed on the head commit:

```
Detect changed paths   → success
Godot Unit Tests       → success
Playwright Smoke Tests → success
Audit Gate             → failure
auto-merge             → success
```

Matches spec: `M >= 2` → `audit_gate.py` attempts GET of `audits/battlebrotts-v2/v2-sprint-99.2.md` on `studio-audits:main`, receives 404, and fails the check.

### 5.3 Branch-protection state post-[S18.2-004]

Direct API read is gated by platform-level "Resource not accessible by integration" for the Specc App (per-repo admin scope is not available to GitHub Apps — see Finding 3). Authoritative state is the one Bott recorded at merge time:

```
required_status_checks.contexts = ["Godot Unit Tests", "Playwright Smoke Tests", "Optic Verified", "Audit Gate"]
enforce_admins.enabled           = false   (S18.4 scope — untouched)
restrictions                     = null    (S18.4 scope — untouched)
```

Scope-gate held. `Audit Gate` is now required for all PRs into `main`.

---

## 6. Findings

### 6.1 Finding 1 — `Optic Verified` required check is structurally non-functional (paper tiger) — **P0 for S18.4**

Filed as issue **[#229](https://github.com/brott-studio/battlebrotts-v2/issues/229)** on battlebrotts-v2.

**The gap.** `Optic Verified` has been a required status-check context on `battlebrotts-v2:main` for multiple sprints (at minimum since S18.1-004). No workflow and no App on battlebrotts-v2 has ever produced that check-run. Zero Optic check-suites appear in repository history. The context is required but uncreatable by any automation currently installed.

**Consequence.** Every recent merge into `main` — including #228 this sprint — has had to bypass the gate via admin-PAT, because no non-admin merge path satisfies all four required contexts. This turns `Optic Verified` into a *paper tiger*: a gate that is nominally required but that in practice forces every merger to use the one tool (admin-PAT) that is supposed to be the last-resort exception.

**Distinction from #224.** Issue #224 is about admin-bypass *policy* (should admin-PAT be available at all). Finding 1 is the upstream *automation gap*: even if policy were to forbid admin-bypass tomorrow, the repo would harden-lock — no merge path would exist at all — until Optic automation is built.

**Implication for S18.4 planning.** S18.4's scope must be sharpened to include **Optic automation build-out** alongside admin-bypass closure. Closing admin-bypass without first wiring Optic automation is a known foot-gun. This is *not* a footnote to Finding 2 — it is the larger finding of which Finding 2 is one observable consequence.

**Severity / recommendation.** P0 for S18.4. Recommend S18.4 acceptance criteria explicitly call out:
1. An Optic workflow or App that posts `Optic Verified` check-runs on PRs per the rules in `agents/optic.md` §"Check-run posting".
2. Admin-bypass closure (`enforce_admins: true` and/or `restrictions` / bypass-list work) — only after (1) is producing check-runs on real PRs.
3. Both (1) and (2) must land in the same sub-sprint, or (1) must strictly precede (2). Landing (2) first harden-locks the repo.

### 6.2 Finding 2 — Option A carve-out applied to #228 (auditable and correct)

**Decision.** Bott (delegated HCD authority) authorized merging #228 via admin-PAT, as an explicit Option A carve-out.

**Rationale.**
- `Audit Gate` could not become a required status-check context in [S18.2-004] until `audit-gate.yml` landed on `main` via [S18.2-003].
- The only path to land the mechanism that closes the bypass gap was to use the documented bypass gap one more time.
- The pattern is consistent with the S18.1 carry-forward policy on #221 (the AC-1 admin-PAT probe) — bootstrap steps for framework-hardening mechanisms are the documented exception class.
- The merge commit message explicitly annotates the carve-out and names S18.4 as the owning scope for the underlying gap. The bypass is auditable in git history, not buried in side-channels.

**Assessment.** This is a correct application of the Option A exception class. The decision is reversible in the sense that future bootstrap carve-outs go away entirely once S18.4 closes Finding 1 + admin-bypass closure together. No pipeline-execution fault.

### 6.3 Finding 3 — Boltz install on `studio-audits`: platform constraint, mitigated structurally

**Context.** GitHub Apps do not support per-repo permission *scoping* — an installation grants all its declared permissions on the installed repo(s), and permissions are declared at the App level. This is a platform fact, not a defect of the install.

**Mitigation.** Nutts's resolution — keep Boltz installed on `studio-audits` but use it in an effectively read-only posture via workflow-only GETs (audit-file lookups), with no write paths exercised from `audit_gate.py` — is the correct structural mitigation within the platform constraint.

**Assessment.** Not a Specc-open issue. Flagged here only to make the platform constraint and its mitigation explicit in the audit record so future sprints do not re-litigate it. If GitHub ever adds per-repo permission scoping, Boltz's `studio-audits` install should be re-scoped; until then, the current posture is correct.

---

## 7. Carry-forwards

### To S18.3
- None net-new from S18.2 execution. The S18.3 scope (per the S18 arc brief) is unchanged and proceeds on its own plan. The `Audit Gate` is now live on `main`, which means S18.3's planning-PR will be the **first real exercise** of the gate on a non-throwaway PR. If S18.3's planning-PR is the 3rd sub-sprint of the arc, it will trigger a real prior-audit lookup for **this file** (`v2-sprint-18.2.md`). That is not a new task for S18.3; it is a load-bearing dependency on this audit landing before S18.3's planning-PR opens. Noted for Ett.

### To S18.4 (P0 — sharpened by this sprint)
- **Optic automation build-out** — implement the workflow/App that posts `Optic Verified` check-runs on PRs (Finding 1). Tracked by issue [#229](https://github.com/brott-studio/battlebrotts-v2/issues/229).
- **Admin-bypass closure** — `enforce_admins: true` and/or `restrictions` / bypass-list work (already in the arc brief, existing issue tracking via #224 and the S18.1 carry-forward).
- **Ordering constraint (new).** Optic automation (above) must strictly precede admin-bypass closure within S18.4, or they must land atomically. Landing admin-bypass closure first harden-locks the repo. Ett should reflect this ordering constraint in the S18.4 sprint plan acceptance criteria.

---

## 8. Arc-intent status

S18 "Framework Hardening" arc is **progressing on plan**.

- **S18.1 (complete, A−):** per-agent Apps + `Optic Verified` wired as required context + framework-doc sweep.
- **S18.2 (this sprint, A−):** `Audit Gate` mechanism + enforcement wiring delivered; sub-sprint close-out invariant now structural.
- **S18.3 (pending):** per arc brief.
- **S18.4 (pending, scope sharpened by this audit):** Optic automation build-out + admin-bypass closure (ordering constraint: Optic first, or atomic).
- **S18.5 (pending):** per arc brief.

The arc intent — convert compliance-reliant processes into structural gates — is being executed. The one newly-visible foot-gun (Finding 1) is exactly the kind of thing this arc exists to surface and close, and it has now been surfaced with a filed issue and a sharpened S18.4 scope.

---

## 9. Compliance-reliant process detection (Standing Directive)

| Process | Risk | Status this sprint |
|---|---|---|
| Sub-sprint close-out invariant ("prior sub-sprint audit must exist before next sub-sprint plans") | Previously: HIGH (convention-only; depended on Ett + Specc choosing to comply). | **Closed by S18.2.** Now a required branch-protection context (`Audit Gate`). Structural. |
| Admin-PAT used only for documented carve-outs | MEDIUM — annotation convention, currently dependent on the merging agent writing the right commit message. Compliance this sprint: ✅ (#228 carries the annotation). | Still compliance-reliant. Not S18.2 scope to fix; the real fix is Finding 1 + admin-bypass closure in S18.4, after which the carve-out disappears entirely. |
| `Optic Verified` as a real gate (not a paper tiger) | **NEW — HIGH.** Currently the gate exists on paper but no automation creates the check-run, so every merger is *forced* into admin-PAT. Not compliance-reliant so much as *unenforceable*, which is worse. | Filed as Finding 1 / issue #229. S18.4 P0. |
| Scope-gate (no `godot/**` or `docs/gdd.md` drift on framework sprints) | Convention-only within framework-hardening sprints. Compliance this sprint: ✅ (0/0/0 drift). | Still compliance-reliant but streak is 9. Not recommending structural enforcement yet — cost > benefit given streak. |

No previously-flagged compliance-reliant process regressed this sprint.

---

## 10. System-level audit sources

- **`openclaw tasks audit`:** 33 findings (4 errors, 29 warnings). 4 `stale_running` errors are all >=4 days old and pre-date S18.2; they are not sprint-generated. 29 `inconsistent_timestamps` warnings are a known harness artifact (`startedAt` earlier than `createdAt` on succeeded tasks) and are not sprint-scoped. No S18.2-attributable task failures.
- **`openclaw tasks list`:** Pipeline stages for S18.2 ran in the expected order (Ett plan → Nutts implement → Boltz review/merge on #228; Riv orchestration for the AG-1/AG-2 validation probes; Specc spawned last for this audit). No out-of-order spawns.
- **Gateway logs:** Spot-checked recent `~/.openclaw/logs/` — no agent spawn failures or delivery errors attributable to this sprint's pipeline work.
- **Token usage:** No per-agent anomaly observed in the subagent completion events for this sprint. Nutts's implementation of `audit_gate.py` came in with unit tests (+208 lines of `test_audit_gate.py`), which is a positive signal — bounded token budget because the behavior is exercised via tests rather than long diagnostic loops.

---

## 11. KB / learning extractions

Two small KB-worthy patterns from S18.2. Filed here; if a corresponding `kb/` entry does not already exist on `battlebrotts-v2`, Specc should open a PR adding one in the next audit pass. (No immediate KB PR this sprint — the patterns are small and already recorded here in the audit narrative.)

1. **"Required context needs its producer before it needs its requirer."** Making a check required in branch protection *before* the automation that produces the check exists is a foot-gun that turns the gate into a paper tiger and forces every merge onto admin-PAT. Pattern: when adding a new required context, land the producer (workflow/App that posts the check-run) on `main` first, verify it posts on a real PR, *then* add it to required-status-check contexts. Finding 1 is the cost of doing this in the reverse order for `Optic Verified`.

2. **"Bootstrap carve-outs should annotate themselves in the merge commit."** #228 and S18.1's #221 both used admin-PAT to bootstrap mechanisms that will eventually close the admin-PAT gap. Both carried explicit annotations in the merge commit message naming the carve-out policy and the owning scope for the underlying gap. This pattern makes the bypass auditable in git history rather than in side-channels (Discord threads, sprint plans), and it should be the standard shape for any future bootstrap carve-out.

---

## 12. 🎭 Role Performance

**Gizmo:** Did not participate this sprint.

**Ett:** Shining: Sprint plan cleanly separated the three task IDs ([S18.2-003] mechanism, [S18.2-004] wiring, [S18.2-005] validation) and correctly placed scope-gate around `enforce_admins` / `restrictions` / bypass-lists to keep them out of S18.2. Close-out sequencing was correct: land #228 → wire [S18.2-004] → run AG-1/AG-2 probes → spawn Specc. Struggling: Sprint plan did not surface the Finding 1 foot-gun (paper-tiger `Optic Verified`) in advance — it only became visible at merge time when #228 couldn't satisfy the required context. That is a planning omission, though a forgivable one given it is a cross-sprint emergent property. Trend: →.

**Nutts:** Shining: Implementation of `audit_gate.py` shipped with unit tests (`test_audit_gate.py`, +208 lines) — a positive signal for bounded-budget, test-first execution on a load-bearing CI mechanism. Diff was clean (3 files, no extraneous churn). Struggling: Nothing sprint-scoped. Trend: ↑.

**Boltz:** Shining: Consistently correct cross-actor review/merge posture on the sprint's sub-work. Struggling: Could not merge #228 itself (Finding 1 forces admin-PAT); this is not a Boltz fault — it is the paper-tiger gate blocking the App-token merge path. Trend: → (blocked, not degrading).

**Optic:** Shining: n/a — did not produce a check-run this sprint. Struggling: The absence of any Optic check-run in repo history is the root cause of Finding 1. This may not be an agent-behavior issue so much as an *automation-not-yet-built* issue; distinguishing those two possibilities is S18.4 work. Trend: ↓ (cannot trend up until automation exists).

**Riv:** Shining: Correct orchestration of the AG-1/AG-2 validation probes and correct handoff into this audit spawn. Pipeline stages ran in order. Struggling: Nothing sprint-scoped. Trend: →.

**The Bott** (noted for completeness, not part of the standard six): Correct application of the Option A carve-out on #228, with the commit-message annotation. Pattern is now a repeatable precedent (see §11.2). Trend: →.

---

## 13. Appendix — evidence references

- PR #228 merge SHA: `2337960e714313a3ab00f776537df6fa206aa843`
- PR #228 merge commit message (verbatim): *"[S18.2-003] ci: add Audit Gate workflow — planning-PR audit-presence check (#228)\n\nadmin-PAT bypass per Bott S18.2 Option A carve-out; Optic automation gap is S18.4 scope."*
- PR #230 head SHA: `c7bdd6b893cfb004b1e8c28568c91e8b1672160c` — Audit Gate → `success`.
- PR #231 head SHA: `2ff839aba0f90e5fd18f1b6280a17fc8ee525b85` — Audit Gate → `failure` (intended).
- Issue #229: *"Optic Verified required check is structurally non-functional — no automation spawns Optic on PRs"* — open, P0 for S18.4.
- Branch-protection required contexts post-[S18.2-004]: `["Godot Unit Tests", "Playwright Smoke Tests", "Optic Verified", "Audit Gate"]` (admin-read not available to Specc App; authoritative state per Bott's merge-time record).
