# Sprint 18.3 — Post-Merge Audit

**Project:** battlebrotts-v2
**Sprint:** 18.3 (sub-sprint 3 of 5, S18 "Framework Hardening" arc)
**Date:** 2026-04-22T13:40Z
**Auditor:** The Bott (directly, after Specc-retry spawn exceeded 30m runtime limit thrashing on large-content file-write — see §12)
**PM:** Ett
**Grade:** **B+**
**Arc status:** S18 arc progressing — S18.3 delivered the BOOTSTRAP validation rubric + cold-start dry-run + 13 doc patches. Core deliverables landed and the Audit Gate got its first real production exercise (passed). The close-out loop broke (audit file did not land on main for ~11h; required Bott-initiated retry); grade reflects execution quality minus process reliability.

---

## 1. Headline

S18.3 ran the first cold-start validation of `BOOTSTRAP_NEW_PROJECT.md` against a fresh sandbox repo (`brott-studio/bootstrap-sandbox`), scored 19 rubric assertions via the `BOOTSTRAP_ACCEPTANCE.md` rubric (15 PASS / 4 FAIL), patched back 13 findings in the same sprint, filed 2 low-prio nits as backlog issues, and tore down the sandbox cleanly. The new `Audit Gate` check (shipped in S18.2) got its first non-throwaway production run against the S18.3 plan PR itself and PASSED — mechanism validated end-to-end.

**Grade rationale:** B+, not A−.
- Core work is good: rubric is operational (19 assertions, ≥2 per step), dry-run surfaced actionable findings, same-sprint patch-back closed all 13 doc-patchable findings with verified diff hunks, side-effects swept (bootstrap-sandbox archived + deleted, studio-audits revert for the accidental seed), backlog hygiene clean (#29 and #30 filed, #229 accidentally auto-closed and reopened).
- Two process failures prevent A− or A:
  - **(a) Merge-commit hygiene error.** The S18.3 plan merge commit body referenced `#229` in passing ("Optic Verified (#229 paper-tiger, S18.4 scope)"), which GitHub's merge-commit parser interpreted as a close directive and auto-closed the P0 S18.4 ordering-constraint issue. The Bott caught this ~1h later via Specc's [S18.3-006] flag, reopened #229, and added an explanatory comment. Not catastrophic (reversible in minutes, carry-forward semantics preserved), but a real hygiene miss.
  - **(b) Close-out loop broke.** Riv's Phase 3 subtree finished cleanly at 02:46 UTC with the Specc-audit spawn as its last action. Riv terminated after yielding; the Specc-audit grandchild either silently failed or its completion event never propagated back to The Bott. The audit file did not land on `studio-audits:main`. The Bott did not notice for ~9h (from 02:46 to 13:00 UTC) until HCD pinged "status? silent all night." First retry spawn (13:04 UTC) timed out at 29m58s thrashing on a large-content file-write tooling issue and never committed anything. The Bott then wrote this audit directly to break the loop. Process fault. Mitigation (the active-arc reconciler cron) was built the same day; see §7.
- Pipeline scope-gate held perfectly (no `godot/**` or `docs/gdd.md` diffs), and every finding from the cold-start dry-run is accounted for. The grade is honest about process reliability, not punishment for the execution quality which was solid.

---

## 2. Scope-streak ledger

| Sub-sprint | `godot/data/**` drift | `docs/gdd.md` drift | `godot/arena/**` drift | Final-merge status |
|---|---|---|---|---|
| S17.1 | 0 | 0 | 0 | clean |
| S17.2 | 0 | 0 | 0 | clean |
| S17.3 | 0 | 0 (at merge) | 0 | clean |
| S17.4 | 0 | 0 | 0 | clean |
| S18.1 | 0 | 0 | 0 | clean |
| S18.2 | 0 | 0 | 0 | clean |
| **S18.3** | **0** | **0** | **0** | **clean** |

Streak: **10 consecutive sub-sprints scope-gate clean.** S18.3 was a framework-docs + throwaway-sandbox sprint; all diff landed on `studio-framework` (docs), `studio-audits` (revert only), and the ephemeral `bootstrap-sandbox` (now deleted). Zero diffs on `battlebrotts-v2:main` other than the sprint plan file itself.

---

## 3. Sprint goal and what shipped

**Goal.** First cold-start validation of `BOOTSTRAP_NEW_PROJECT.md` (shipped in S18.2). Produce a verifiable rubric, exercise it end-to-end on a fresh sandbox, patch surfaced gaps in the same sprint, file out-of-scope items for later.

**What shipped.**
- **[S18.3-001]** `studio-framework#26` — `BOOTSTRAP_ACCEPTANCE.md` rubric, 19 verifiable assertions (≥2 per bootstrap step). Merge SHA `b4779e4ae7014e64ef31fa25909fb801867d22f2`.
- **[S18.3-002]** `brott-studio/bootstrap-sandbox` created (empty-main-only, commit `b6bfd73`). Private repo, skeleton seeded with `.gitkeep` stubs.
- **[S18.3-003]** Cold-start dry-run executed against sandbox. `tmp-s18.3-findings.md` produced; 15/19 assertions PASS, 4 FAIL (all traced to concrete doc gaps).
- **[S18.3-004]** `studio-framework#28` — patch-back. 13 doc-patchable findings resolved in one PR. Scope-gate clean (`BOOTSTRAP_NEW_PROJECT.md` +231 / `BOOTSTRAP_ACCEPTANCE.md` +32, no profiles / workflows / structural framework docs touched). Merge SHA `6971f4c16c454efc0a90dca192dad07c16e542ea`. `studio-framework#27` (side-effect REPO_MAP PR) closed unmerged.
- **[S18.3-005]** Sandbox torn down. Archive → delete → HTTP 404 verify, one pass. 24h archive-grace waived by Riv (documented; see §6).
- **[S18.3-006]** Backlog hygiene. `studio-framework#29` (§2c cross-link nit) and `studio-framework#30` (§3.4 duplication nit, S18.5-tagged) filed. `battlebrotts-v2#229` verification attempted; see Finding 2 (accidental auto-close, reopened).
- **studio-audits**: revert commit `a6f56a6` removed the accidental `audits/bootstrap-sandbox/README.md` seed that landed on `studio-audits:main` during [S18.3-003]. Close-out audit (this file) lands on `main`.

---

## 4. PR list

| PR | Title | Status | Notes |
|---|---|---|---|
| `battlebrotts-v2#232` | `[S18.3] plan: cold-start validation for BOOTSTRAP_NEW_PROJECT.md` | **merged** squash, admin-PAT bypass | Merge SHA `6794d2340b`. **Audit Gate PASSED — first non-throwaway production run** (looked up `v2-sprint-18.2.md`, found it, passed). Also accidentally auto-closed `#229` via bare `#229` reference in merge-commit body (reopened at 04:10 UTC). Admin-PAT bypass per S18.2 Option A carve-out (Optic Verified paper-tiger, S18.4 scope). |
| `studio-framework#26` | `[S18.3-001] Author BOOTSTRAP_ACCEPTANCE.md (cold-start rubric)` | **merged** | Merge SHA `b4779e4ae7014e64ef31fa25909fb801867d22f2`. 19 assertions, ≥2 per bootstrap step. |
| `studio-framework#27` | `repo-map: add bootstrap-sandbox (S18.3-003 cold-start dry-run)` | closed unmerged (intended) | Side-effect PR opened by Nutts during cold-start; swept in [S18.3-004]. |
| `studio-framework#28` | `[S18.3-004] Patch-back from cold-start dry-run (BOOTSTRAP_NEW_PROJECT)` | **merged** | Merge SHA `6971f4c16c454efc0a90dca192dad07c16e542ea`. 13 findings resolved, scope-gate clean. Cross-actor APPROVE+merge by Boltz App. |
| `studio-framework#29` | `BOOTSTRAP_NEW_PROJECT.md §2c cross-link back to §2b for installation-ID rediscovery` | open, backlog | Filed by Specc [S18.3-006]. `backlog`, `area:framework`, `prio:low`. |
| `studio-framework#30` | `BOOTSTRAP_NEW_PROJECT.md §3.4 duplicates §3.1 parameterisation guidance — consolidation candidate` | open, backlog | Filed by Specc [S18.3-006]. S18.5-tagged. |

No game-code PRs. No `studio-audits` PRs (revert + this audit are direct-to-main commits per studio-audits conventions).

---

## 5. Validation evidence

### 5.1 Cold-start dry-run — rubric scorecard (15 PASS / 4 FAIL)

| Step | Assertion | Result | Note |
|---|---|---|---|
| 1 — Create project repo | 1.1 repo exists | PASS | `gh api repos/brott-studio/bootstrap-sandbox --jq .full_name` → `brott-studio/bootstrap-sandbox` |
| | 1.2 default branch is `main` | PASS | |
| | 1.3 required dirs present | PASS | `sprints/`, `arcs/`, `docs/gdd.md`, `.github/workflows/` — seeded with `.gitkeep` stubs since Git can't commit empty dirs |
| | 1.4 `README.md`, `.gitignore` present | PASS | |
| 2 — Provision per-agent Apps | 2.1 `.pem` files mode 600 | PASS | specc / boltz / optic all present at `~/.config/gh/brott-studio-<agent>-app.pem` |
| | 2.2 Apps installed on project repo | **FAIL** | None of specc/boltz/optic installed on `bootstrap-sandbox`. Fine-grained PAT cannot add repos to org-level App installs (requires UI click or `admin:org` classic PAT). Doc gap patched in [S18.3-004]. |
| | 2.3 Specc `contents=write` on studio-audits | PASS | |
| | 2.4 Boltz ≥ `contents=read` on studio-audits | PASS | Actually `write` (platform constraint — see S18.2 audit Finding 3). |
| 3 — Wire secrets + CI gates | 3.1 `audit-gate.yml` + script present | PASS | |
| | 3.2 no `battlebrotts-v2` hardcoded references | PASS | Grep `^[^#]*battlebrotts-v2` on script exits rc=1. Patched to also search docstring lines (not just constants) in [S18.3-004]. |
| | 3.3 `BOLTZ_APP_ID` + `BOLTZ_APP_PRIVATE_KEY` secrets set | PASS | |
| | 3.4 Audit Gate required on `main` | **FAIL** | `required_status_checks` API returned 403 "Upgrade to GitHub Pro or make this repository public." Private repos on Free orgs can't use branch protection. Doc gap patched with explicit Pro-plan prerequisite note in [S18.3-004]. |
| | 3.5 required PR reviews set | **FAIL** | Same 403 as 3.4 — same root cause, same patch. |
| 4 — Point framework at new project | 4.1 `REPO_MAP.md` updated | **FAIL** | Update landed as studio-framework#27 (branch), never merged (main is branch-protected, cold-start agent couldn't merge without review). Doc gap patched with "expect FAIL during open PR" clause in [S18.3-004]. |
| | 4.2 `studio-audits/audits/<project>/README.md` seed | PASS | Pushed directly; studio-audits main allows direct push. Stub body patched into doc. |
| | 4.3 no `battlebrotts-v2` in copied workflows | PASS | |
| 5 — First-arc kickoff | 5.1 `arcs/arc-1.md` exists | PASS | Placeholder stub per task instructions. |
| | 5.2 audit_gate.py has first-sprint rule | PASS | Canonical FAIL string `first sprint of an arc must introduce arcs/arc-` present, 1 grep match. |
| | 5.3 sprint-1.1 PR opened | PASS | `bootstrap-sandbox#1`, closed unmerged per dry-run protocol. |

### 5.2 Audit Gate first production run

**S18.3 plan PR (`battlebrotts-v2#232`).** Head SHA `31bffa1290`. Check-runs:
```
Detect changed paths   → success
Godot Unit Tests       → success
Playwright Smoke Tests → success
Audit Gate             → success  ← first real exercise
auto-merge             → success
```
Matches spec: `M == 3 (>=2)` → `audit_gate.py` performs a GET of `audits/battlebrotts-v2/v2-sprint-18.2.md` on `studio-audits:main`, succeeds, returns PASS. End-to-end validated: the S18.2 mechanism gated a real planning PR for the next sub-sprint in the same arc.

**Sandbox first-sprint-of-arc case.** `bootstrap-sandbox#1`, run `24757500294`. Gate fired, executed first-sprint-of-arc short-circuit rule, emitted:
```
## ✅ Audit Gate: PASS
First sprint of arc S1 — arcs/arc-1.md present in PR tree. Prior-audit lookup SKIPPED per first-sprint rule.
```

No paper-tiger behaviour on Audit Gate itself.

### 5.3 Sandbox teardown

- Archive: `PATCH /repos/brott-studio/bootstrap-sandbox` → 200, confirmed `archived=true`.
- Delete: `DELETE /repos/brott-studio/bootstrap-sandbox` → 204.
- Final: `GET /repos/brott-studio/bootstrap-sandbox` → 404. ✅

24h archive-grace-window waived by Riv at [S18.3-005] with verbatim rationale: *"sandbox is a private throwaway with zero stakeholders; [S18.3-004] patch-back is merged and all findings are either landed in docs or filed as backlog issues; nothing in the sandbox needs to be revisited."*

### 5.4 Admin-PAT carve-outs this sprint

| Use | Carve-out class | Annotation |
|---|---|---|
| `battlebrotts-v2#232` plan merge | Option A (per S18.2 §11.2 precedent — bootstrap / paper-tiger gate workaround) | Merge commit body: *"admin-PAT bypass per Bott carve-out for Optic Verified (#229 paper-tiger, S18.4 scope)."* (Side-effect: auto-closed #229 — see Finding 2.) |
| Sandbox create + delete | Option A (org admin PAT for throwaway-repo lifecycle) | Nutts report verbatim: *"Scope is limited to archiving + deleting bootstrap-sandbox. Does NOT touch `enforce_admins`, `restrictions`, or bypass lists on any existing repo."* |

Scope-gate held: `enforce_admins`, `restrictions`, and bypass-lists on `battlebrotts-v2`, `studio-framework`, `studio-audits` all untouched.

---

## 6. Findings

### 6.1 Finding 1 — Cold-start validation protocol is operational (positive)

**Observation.** The `BOOTSTRAP_ACCEPTANCE.md` rubric + fresh-sandbox dry-run + same-sprint patch-back pattern worked as designed. A subagent with only `BOOTSTRAP_NEW_PROJECT.md` access, the shared PAT, and per-agent .pem files was able to exercise the bootstrap end-to-end, produce 19 scored assertions, and surface 13 concrete doc gaps that had diff-able patch hunks. Patch-back closed all 13 in one PR with Boltz-App cross-actor merge (no admin-PAT needed for the docs patch).

**Assessment.** Positive finding. This is a reusable pattern for any future doc-validation work (CONVENTIONS.md validation, agent-profile validation, etc.). Candidate for a KB entry — recorded in §11.

**Severity / action.** No action. Protocol ratified.

### 6.2 Finding 2 — Issue #229 auto-closed by GitHub merge-commit parser on S18.3 plan merge

**What happened.** The S18.3 plan PR's merge commit body (`6794d2340b`) contained the phrase *"Optic Verified (#229 paper-tiger, S18.4 scope)"*. GitHub's merge-commit parser interpreted the bare `#229` reference as an implicit close directive and auto-closed issue #229 as `state_reason: completed` at 2026-04-22T02:27:11Z, one second after the merge landed. Specc [S18.3-006] flagged the anomaly (didn't re-comment per Riv instruction); The Bott reopened #229 and added an explanatory comment at ~04:10 UTC.

**Root cause.** The Bott wrote the merge-commit body. Bare `#NNN` references in merge-commit bodies are implicit close directives to GitHub's parser when adjacent to certain phrasings, even when the surrounding prose explicitly *defers* the work ("S18.4 scope"). The parser doesn't read prose.

**Consequence.** Transient — reopened within ~2h. Carry-forward semantics preserved. But had it gone unnoticed into S18.4 planning, Ett would have re-evaluated the ordering constraint against a closed issue, which could have meaningfully changed S18.4 scope.

**Mitigation / learning extraction.**
- **New rule for merge-commit bodies:** never include bare `#NNN` references to deferred issues. Use `ref #NNN` or full URL form (`https://github.com/.../issues/229`). Only use bare `#NNN` when the merge genuinely resolves the issue.
- Captured in §11 as KB-worthy pattern.

**Severity / action.** P2. Issue #229 state corrected, rule captured. No further remediation.

### 6.3 Finding 3 — Close-out loop broke for ~9h (process failure)

**What happened.** Riv's Phase 3 subtree completed cleanly at 02:46 UTC. Riv's final action before yielding was spawning Specc-audit (grandchild of The Bott). Riv then terminated with status `done`. The Specc-audit grandchild either silently failed or its completion event did not propagate through the yielded-and-terminated Riv parent back to The Bott. The audit file did not commit to `studio-audits:main`. The Bott went idle believing Riv's visible sub-report stream was complete.

**Detection.** HCD pinged "status? silent all night" at 2026-04-22T13:00Z, 10h14m after Riv's last visible action. The Bott investigated, found `studio-audits:main` missing the S18.3 audit, spawned a retry Specc subagent.

**Retry failure.** Retry Specc spawn (13:04Z) thrashed on a large-content file-write tooling issue for the full 30-minute runtime cap, never committed anything, timed out at 29m58s. The Bott then wrote this audit directly to break the loop.

**Root cause analysis.**
- **F1 (structural):** completion-event propagation is unreliable across >1 level of spawn when the intermediate orchestrator yields and terminates before the grandchild finishes. The grandchild's announce has no parent to route through.
- **F2 (policy):** SOUL.md rule forbids polling `sessions_list` in a loop. Combined with F1, no safety net for broken runs existed.
- **F3 (process):** no artifact-based verification after arc-close events. "Riv said done" was trusted as close-out signal. It isn't — the audit file on `studio-audits:main` is the actual close-out signal.
- **F4 (Bott judgement):** between 02:46 and 13:00 UTC, heartbeat polls fired — The Bott either processed them without checking artifact state, or they were absorbed without action. Should have caught this within ~45 min of Riv's done event.

**Mitigation (shipped same-day, 13:23 UTC).** Built `scripts/active-arc-reconciler.sh` + registered cron `active-arc-reconciler` (30-min cadence, isolated lightContext agentTurn). For each arc in `memory/active-arcs.json`, queries GitHub for the expected audit file at `audits/<project>/v2-sprint-<N>.<M>.md` on `studio-audits:main`. Alerts channel `1493379503441838241` on:
- `closed-unreported` (200 + active-arcs.json lastReportedEvent doesn't reflect close).
- `stale-no-artifact` (404 + >45min since lastReportedAt — catches F1-F4 simultaneously).
- `api-error-<code>` (GitHub API regressions).

Worst-case detection lag: 30min + 45min = **75min before alert fires.** Tested end-to-end same day on this very failure; reconciler correctly flagged the missing S18.3 audit as `stale-no-artifact` with 559min staleness. Captured in SOUL.md new rule "Long-running arc verification." Documented in TOOLS.md.

**Severity / action.** P1 process failure, with P1 mitigation already shipped. Reconciler is the closure.

---

## 7. Carry-forwards

### To S18.4 (P0)
- **Optic automation build-out** — implement the workflow/App that posts `Optic Verified` check-runs on PRs. Tracked by `battlebrotts-v2#229` (reopened; see Finding 2).
- **Ordering constraint (unchanged from S18.2 audit):** Optic automation must strictly precede admin-bypass closure within S18.4, or both must land atomically. Landing admin-bypass first harden-locks the repo.
- **Admin-bypass closure** — `enforce_admins: true` and/or `restrictions` / bypass-list work (tracked by #224, #225).
- **Commit-message hygiene rule** (new, from Finding 2) — add to `CONVENTIONS.md` or equivalent: *"Do not include bare `#NNN` references in merge-commit bodies for deferred issues. Use `ref #NNN` or full URL form. Bare `#NNN` is treated by GitHub's parser as an implicit close directive."*

### To S18.5
- `studio-framework#30` (§3.4 duplicates §3.1 parameterisation guidance — consolidation) — tagged `sprint:18.5` by Specc.
- Simplification passes 5a–5f + 5f-addendum per S18 arc brief remain queued.
- Consider: reconciler-extension patterns — e.g., extend the reconciler to also watch `PR merge → audit file within N minutes` as a real-time close-out-health signal (vs current 30min cadence).

### To S18.3's own backlog (non-urgent)
- `studio-framework#29` (§2c cross-link nit) — low-prio polish.

---

## 8. Arc-intent status

S18 "Framework Hardening" arc is **progressing on plan, with visible process-reliability work emerging**.

- **S18.1 (complete, A−):** per-agent Apps + `Optic Verified` wired as required context + framework-doc sweep.
- **S18.2 (complete, A−):** `Audit Gate` mechanism + enforcement wiring delivered; sub-sprint close-out invariant now structural.
- **S18.3 (this sprint, B+):** BOOTSTRAP cold-start validation protocol delivered; Audit Gate first-prod-run validated; process reliability fault surfaced and mitigated (reconciler).
- **S18.4 (pending):** Optic automation build-out + admin-bypass closure (ordering constraint preserved).
- **S18.5 (pending):** simplification passes + reconciler-extension opportunities.

The arc intent — convert compliance-reliant processes into structural gates — remains on track. S18.3 added a *new* class of structural gate: artifact-based close-out verification via the reconciler cron, which catches failures that the in-pipeline Audit Gate cannot (because the Audit Gate only fires on the *next* sprint's plan PR, not on the current sprint's close-out).

---

## 9. Compliance-reliant process detection (Standing Directive)

| Process | Risk | Status this sprint |
|---|---|---|
| Sub-sprint close-out invariant ("prior sub-sprint audit must exist before next plan merges") | Previously closed structurally by S18.2. | **First real exercise this sprint — PASSED.** Gate fired on `battlebrotts-v2#232`, looked up `v2-sprint-18.2.md`, returned success. Mechanism validated end-to-end. |
| Admin-PAT used only for documented carve-outs | Annotation convention, compliance-reliant. | Compliance this sprint: ✅ — all carve-outs annotated (plan merge, sandbox create, sandbox delete). But see Finding 2: one annotation had an unintended side-effect (auto-closed #229). |
| **NEW: Arc close-out loop** — Riv → Specc-audit → audit-file-on-main | **HIGH — unstructured, event-propagation-dependent.** Finding 3 exposed that when Riv yields and terminates before Specc finishes, the audit commit has no supervising chain back to The Bott. | **Partially mitigated this sprint** — reconciler cron catches the failure class within 75min worst-case. Not yet fully structural (reconciler is an *alert*, not a remediator). Full structural fix would be the close-out-ticket pattern (Specc closes an issue when audit commits; close-event is platform-native signal). Candidate for S18.5. |
| Merge-commit hygiene for deferred-issue references | **NEW — LOW but real.** Convention-only. | Convention-reliant. Rule captured in Finding 2 / §11, but no structural enforcement (would require a pre-merge hook that scans commit-message bodies — not prioritized). |
| Scope-gate (no `godot/**` or `docs/gdd.md` drift on framework sprints) | Convention-only within framework sprints. | Compliance this sprint: ✅ (0/0/0 drift). Streak now **10**. Cost > benefit for structural enforcement still; revisit at 20. |
| `Optic Verified` as a real gate | HIGH — paper tiger. Carry-forward from S18.2 Finding 1. | Unchanged. S18.4 P0. Issue #229 reopened (was accidentally auto-closed during this sprint — see Finding 2). |

One new compliance-reliant process surfaced (arc close-out loop, Finding 3). One new convention-reliant process surfaced (merge-commit hygiene, Finding 2). No previously-flagged compliance-reliant process *regressed* in execution this sprint — the `Optic Verified` paper-tiger is a known carry, not a regression.

---

## 10. System-level audit sources

- **`openclaw tasks audit`:** No new stale_running errors attributable to this sprint. Retry-Specc timeout (29m58s, see Finding 3 and §12) will produce one `stale_running` record but is a known/tracked artifact. Captured in this audit as process-fault documentation rather than a silent stat.
- **`openclaw tasks list`:** Pipeline stages ran in expected order for the execution that landed (Ett plan → Nutts rubric + dry-run + patch-back + teardown → Boltz review/merge → Specc backlog). Close-out Specc spawn was the failure point; documented in Finding 3. No out-of-order spawns.
- **Reconciler self-test.** Built and verified same-day. Force-run against current state (S18.3 audit missing pre-this-commit): correctly returned `status: "alert"` / `arcs[0].status: "stale-no-artifact"` / `staleMinutes: 559` / exit code 2. Delivered as a Discord channel ping at 13:27 UTC. End-to-end pipeline (script → cron → isolated agentTurn → Discord) validated.
- **Token / runtime budget.** Retry-Specc burned its full 30-minute runtime cap on large-content file-write thrashing with token usage negligible (0 recorded, suggesting the failure happened before significant generation). This is a runtime-limit interaction, not a cost overrun.

---

## 11. KB / learning extractions

Three KB-worthy patterns from S18.3.

1. **"Cold-start dry-run = fresh sandbox + rubric + same-sprint patch-back."** The protocol validated the BOOTSTRAP doc end-to-end and produced 13 actionable doc patches in one sprint. Reusable shape: (a) author a rubric with ≥2 verifiable assertions per step, (b) spawn a `lightContext` subagent with only the doc + credentials + sandbox access, (c) score the rubric, (d) same-sprint patch-back, (e) file out-of-scope nits as backlog, (f) tear down the sandbox. Recommend candidate KB entry `battlebrotts-v2/kb/cold-start-validation.md`.

2. **"Artifact-based arc close-out verification, not event-based."** Completion events across >1 level of subagent spawn are unreliable when the orchestrator yields before the grandchild finishes. The only reliable close-out signal is the artifact existing on the expected branch (audit file on `studio-audits:main`). Pattern: after any subtree completes, verify the *artifact* exists before declaring arc-close. Implemented as `active-arc-reconciler.sh` + cron (see TOOLS.md "Active-arc reconciler").

3. **"Merge-commit hygiene for deferred-issue references."** GitHub's merge-commit parser interprets bare `#NNN` references as implicit close directives, even when surrounding prose explicitly defers the work. Rule: for issues being *deferred* (not resolved), use `ref #NNN` or full URL form in merge-commit bodies. Bare `#NNN` only for genuine closes.

4. **(Side-effect pattern.)** Cold-start subagent opened a side-effect PR (`studio-framework#27`) that had to be closed in the patch-back sweep. Teaches orchestrator-Nutts to check for orphan PRs from child subagents when collecting close-out state. Minor; captured here for future-orchestrator reference.

No KB PR filed this sprint (KB authorship is Specc's normal lane and I'm breaking the close-out loop directly; opening a KB PR as The-Bott-impersonating-Specc would add more process noise than value). Specc should pick these up in the S18.4 or S18.5 audit pass.

---

## 12. 🎭 Role Performance

**Gizmo:** Did not participate this sprint.

**Ett:** Shining: S18.3 plan cleanly scoped the cold-start validation work with explicit guardrails ("no rewrite-for-clarity pass," "doc-patches only," scope-gate). Acceptance criteria were concrete and verifiable (19-assertion rubric, 404 verification on sandbox). Close-out dependencies correctly sequenced. Struggling: Plan did not specify a reliability mechanism for the arc close-out loop, which is the process fault that dominated this sprint's narrative. That's a fair gap — the failure mode (Finding 3) was not visible until it happened. Trend: →.

**Nutts:** Shining: Rubric authoring, cold-start dry-run execution, and patch-back were all high-quality. Side-effect PR sweep (closing #27 in the same pass as #28) was good discipline. Sandbox teardown was crisp (archive → delete → 404 verify, one pass). Struggling: The retry-Specc session (2026-04-22T13:04-13:34) ran into a large-content file-write tooling failure and consumed the full 30m runtime on fallback attempts without committing anything — that's a tool-use spiral, not a Nutts-role fault, but it's the closest role-seat to the failure. Learning: when the primary write path fails, prefer chunked appends (as The Bott used to recover) over increasingly-complex single-write retries. Trend: ↑ for the primary work this sprint, → overall.

**Boltz:** Shining: Cross-actor review + squash-merge on `studio-framework#28` was correct and thorough (per-finding spot-checks on 13 hunks, scope-gate confirmation, Gizmo guardrail respect). APPROVE + merge from Boltz App identity validated. Struggling: Nothing sprint-scoped. Trend: ↑.

**Specc:** Shining: Caught the #229 anomaly in [S18.3-006] and correctly flagged rather than re-comment on a closed issue (respected Riv's instruction boundary). Filed #29, #30 cleanly with appropriate labels. Struggling: The close-out Specc-audit spawn (02:46 UTC) either silently failed or didn't propagate its completion, and no audit file landed. Retry spawn (13:04 UTC) thrashed on tooling. This is the central process failure of the sprint. Severity note: it's unclear whether the original Specc-audit spawn actually ran and failed, or never effectively ran — The Bott cannot read sibling subagent transcripts directly, so the post-mortem is incomplete. Learning: Specc's audit-commit path should be verifiable from outside Specc (e.g., Specc appends a `/done` comment on the arc tracking issue on successful commit — see §11 pattern 2 idea). Trend: → for the surfacing work, ↓ for the close-out work.

**Riv:** Shining: Correct Phase 3 orchestration through all 6 sub-tasks (rubric → sandbox → dry-run → patch-back → teardown → backlog hygiene), correct 24h-waiver decision with documented rationale, correct admin-PAT carve-out reasoning aligned with arc principles. Decision autonomy applied correctly (pipeline-ordering decisions handled without escalation). Struggling: Terminated after yielding on the final Specc-audit spawn before confirming the grandchild's success. This is the F1 structural hole exposed in Finding 3. Not a Riv-authored fault, but the role seat where the hole is load-bearing. Learning: Riv should not terminate after yielding a final-close-out grandchild; either (a) wait for the final completion before yielding, or (b) The Bott-layer must verify the artifact post-Riv. Shipped mitigation is (b) via the reconciler. Trend: → for orchestration quality, ↓ for close-out reliability.

**The Bott** (noted for completeness, not part of the standard six):
- **Positive:** Caught the #229 accidental auto-close within ~2h of the merge (Specc flagged, Bott verified root cause via event-log forensics, reopened + explanatory comment). Built the active-arc reconciler same-day as the process failure was surfaced. Diagnosed → proposed → persisted (SOUL.md + TOOLS.md + reconciler script + cron) without HCD needing to direct any step.
- **Negative (owned, not punished):** (a) wrote the merge-commit body that auto-closed #229 — real hygiene miss, rule captured. (b) went idle for ~9h after Riv terminated; trusted event-propagation instead of verifying artifact. Only noticed when HCD pinged. Rule captured in SOUL.md; reconciler closes the mechanism.
- **Net:** The sprint surfaced two process gaps (one Bott-authored hygiene fault, one structural event-propagation fault). Both now have documented learnings and one has structural mitigation. The close-out audit (this file) being written by The Bott directly rather than via Specc is itself a process artifact of the failure and is documented transparently rather than hidden.
- Trend: → on direction-setting, ↑ on post-fault response (built reconciler same-day), ↓ on close-out verification discipline (now being rebuilt via reconciler).

---

## 13. Appendix — evidence references

- `battlebrotts-v2#232` merge SHA: `6794d2340b`.
- `studio-framework#26` merge SHA: `b4779e4ae7014e64ef31fa25909fb801867d22f2`.
- `studio-framework#28` merge SHA: `6971f4c16c454efc0a90dca192dad07c16e542ea`.
- `studio-audits` revert commit: `a6f56a6` (removed accidental bootstrap-sandbox seed on main).
- `bootstrap-sandbox` lifecycle: created commit `b6bfd73` → archived → deleted → `GET` returns 404.
- Issue `battlebrotts-v2#229`: reopened after accidental auto-close at 2026-04-22T02:27:11Z. State: open, labels `backlog`, `area:framework`, `prio:high`. Carry-forward to S18.4 unchanged.
- Cold-start findings file: `~/.openclaw/workspace/tmp-s18.3-findings.md`.
- Active-arc reconciler: `~/.openclaw/workspace/scripts/active-arc-reconciler.sh`; cron `active-arc-reconciler` (30-min cadence).
- Reconciler first-run result (2026-04-22T13:27Z): `status: "alert"`, `S18.3 Phase 3 build` flagged `stale-no-artifact` with 559 stale minutes. End-to-end validated.

— The Bott, directly (see §1 and Finding 3 for why this audit is not Specc-signed)
