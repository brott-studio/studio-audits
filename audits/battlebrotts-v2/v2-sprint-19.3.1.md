# BattleBrotts-v2 Sprint Audit — v2-sprint-19.3.1

**Date:** 2026-04-23T03:55Z
**Auditor:** Specc (`brott-studio-specc[bot]`)
**Sub-sprint:** S19.3.1 — Label taxonomy + #34 structural enforcement
**Arc:** Orphan-Recovery Durability Arc
**Grade:** A
**Scope streak:** 15

---

## 1. Summary

S19.3.1 closed the long-running structural gap behind `studio-framework#34` (Boltz merge-checklist label-presence — three manual occurrences across S19.1/S19.2/S19.3) and established a canonical label taxonomy for the studio-framework repo. Approach was Option C (Hybrid) per Gizmo T7 spec: Boltz-profile contract line + GitHub Actions `label-check` workflow + label taxonomy reconciliation. CI-stack growth (1 → 2 workflows on studio-framework) was a flagged design call, surfaced by Gizmo, approved by The Bott under HCD-delegated CI-call authority at 2026-04-23T03:41Z.

The pipeline executed in five clean tasks (T7 → T11) with no rework loops, no escalations beyond the one approved CI-stack call, and a load-bearing live workflow self-test in T10 that proved the new gate actually rejects bad PRs and accepts good ones.

## 2. Pipeline execution

| Task | Role | Artifact | Outcome |
|---|---|---|---|
| T7 | Gizmo | `memory/2026-04-23-s19.3.1-t7-gizmo-label-taxonomy-spec.md` | Single-recommendation design spec (Option C); CI-stack-growth flag surfaced and approved |
| T8 | Nutts | studio-framework PR #45 (head `c35542e2`); 5 labels created via REST API | First-pass clean; 2 labels deferred for deletion (triage required first) |
| T9 | Boltz | PR #45 squash-merged at `1644448d` (~03:48Z); 7-check review PASS via `brott-studio-boltz[bot]` | Anti-#34 self-test held: PR carried `area:compliance` + `prio:P1` + `arc:orphan-recovery` + `enhancement` |
| T10 | Optic | 5-check verification ALL PASS, including live workflow self-test (PR #46) | Test PR with no labels → workflow failure (run `24815706818`); after adding `area:framework` + `prio:P3` → success (runs `24815721941`/`24815721962`); test PR closed, branch deleted (HTTP 204) |
| T11 | Specc | This audit | (this file) |

### 2.1 Bootstrap nuance (worth noting for future readers)

The new `label-check` workflow does **not** enforce on PR #45 itself, because the workflow file did not exist on `main` until #45 merged — first-merge bootstraps the gate. PR #45 satisfied the contract via Nutts's manually-applied labels (verified independently in this audit). The first real enforcement event was Optic's test PR #46 in T10. This is a normal CI-bootstrap pattern, but PR #45's check signature looks "different" from subsequent PRs and the structural reason should be documented for future readers.

## 3. Independent verification (this audit)

Confirmed via REST API at audit-write time:

- PR #45: `state=closed merged=true merge_commit_sha=1644448d0117a7bb19a37251072b1e2d5323a737`, head `c35542e2…`, base `main`, labels `[enhancement, area:compliance, prio:P1, arc:orphan-recovery]`. ✓
- PR #46: `state=closed merged=false`, labels `[area:framework, prio:P3]`. ✓
- Workflow `label-check.yml` runs (most recent 5):
  - `24815706818` (PR #46 head `ed84ad02`, NO labels): `failure` ✓
  - `24815721941` / `24815721962` (PR #46 head `ed84ad02`, WITH labels): `success` ✓
  - `24815582999` / `24815582845` (PR #45 head `c35542e2`): `success` (bootstrap-noise; workflow first runs on #45 merge SHA but does not gate it) ✓
- Repo labels: all 5 new labels present with the spec colors; all 5 pre-existing labels intact (no collateral damage); 2 deferred-deletion labels (`prio:low`, `sprint:18.5`) still present as expected per carry-forward 2.

The load-bearing structural verification (workflow rejects bad PRs, accepts good ones) is the strongest possible end-to-end proof of the #34 fix.

## 4. Compliance-Reliant Process Detection (Standing Directive)

| Process | Status | Disposition |
|---|---|---|
| Boltz manual label-check at merge time (was: 3 occurrences across S19.1/S19.2/S19.3) | **STRUCTURALLY FIXED** in S19.3.1 via `label-check` workflow | Compliance contract now backed by CI gate (workflow + Boltz profile checklist). #34 closes once branch protection adds `label-check / verify-required-labels` as required (carry-forward 1). |
| Branch protection on `studio-framework:main` requiring `label-check` | **NOT YET REQUIRED** — workflow runs but doesn't BLOCK merge | Carry-forward 1: admin-PAT pending (Bott action, mirror S18.4 enforce_admins flow). Until applied, Boltz's compliance contract is the interim line of defense. **Not regressive vs pre-S19.3.1 state** — Boltz checklist + visible red CI status is strictly better than the silent-empty-labels pattern that produced #33/#36/#41. |
| Subagent write-tool reliability (S19.3 T6 30min retry, runtime-harness layer) | UNDER INVESTIGATION (memo: `memory/2026-04-23-subagent-write-tool-reliability.md`) | Did NOT recur in S19.3.1 — all role profiles now default to exec-heredoc, which is the proven workaround. Investigation remains a runtime-harness carry-forward. |

## 5. Carry-forwards

1. **Branch protection — admin-PAT pending.** Add `label-check / verify-required-labels` as a required status check on `brott-studio/studio-framework:main`. Same flow as S18.4 enforce_admins. **Owner: The Bott.** Until applied, the workflow surfaces a red check on PRs without required labels but does not BLOCK merge — Boltz's compliance contract is what's holding the line in the interim. **This is the load-bearing follow-up from S19.3.1.**
2. **Label deletions deferred.** `prio:low` (open issues #29, #30) and `sprint:18.5` (open issue #30) need triage relabeling before retirement. Recommend a triage pass: `prio:low` → `prio:P3` on the 2 issues; drop `sprint:18.5` outright (or migrate to `arc:s18-hardening` if a retroactive arc label is wanted). Scoped follow-up, not an S19.3.1 deficiency.
3. **studio-framework#40** still deferred per Ett scope-call (philosophical spec-vs-convention call).
4. **Subagent write-tool reliability** (carried from S19.3) — workspace memo at `memory/2026-04-23-subagent-write-tool-reliability.md`; runtime-harness investigation pending. Did NOT recur in S19.3.1 because all role profiles now use exec-heredoc by default.
5. **Riv-profile resume-declined handler** — S19.4+ candidate per Gizmo §4 of S19.3 spec.
6. **Sentinel cleanup cron** — optional 7-day sweep of stale `~/.openclaw/subagents/*/write-phase-entered.sentinel`. Not blocking.
7. **Boltz GitHub App env vars** — `BOLTZ_APP_ID=3459519` and `BOLTZ_INSTALLATION_ID=125975574` not pre-exported in Boltz's spawn env (he set them inline). Minor: consider documenting in `agents/boltz.md` or a wrapper script. Not blocking.

## 6. Grade rationale: A

Strong A. Reasoning:

- **Clean five-task pipeline.** Gizmo → Nutts → Boltz → Optic → Specc, no rework, no pinging, no off-pipeline escalations beyond the single approved CI-stack call.
- **Load-bearing structural verification.** Optic's T10 didn't just check that the YAML parses — he opened a real test PR with no labels and confirmed the workflow failed it, then added labels and confirmed it passed. This is the strongest possible structural proof, and it materially exceeds typical "spec-passes-syntax-check" verification.
- **Anti-#34 self-test held.** PR #45 satisfied the very contract it was shipping (`area:compliance` + `prio:P1` + `arc:orphan-recovery` + `enhancement`). Eat-your-own-dogfood discipline was perfect.
- **Sentinel discipline held.** All write-phase spawns (Nutts T8, Boltz T9, Optic T10, this Specc T11) wrote `write-phase-entered.sentinel` at first-entry, continuing the dogfood pattern from S19.3.
- **No collateral damage.** All 5 pre-existing labels remained intact; deferred deletions correctly identified and held back pending triage rather than yanking labels with live attachments.
- **Approved scope-cap respected.** Workflow validates namespace presence only — does not validate spelling, does not require `arc:*`, does not require any specific value. v1 scoped exactly per spec; no scope-creep in implementation.

Considered for A−:
- (a) Branch-protection deferral means the gate is "soft" until admin-PAT is applied.
- (b) Two label deletions deferred.

Both are scoped follow-ups (carry-forwards 1 and 2), not deficiencies in the S19.3.1 work itself. (a) follows the established S18.4 enforce_admins handoff pattern, and (b) is correct safety behavior (don't delete labels with live attachments). Neither weakens the substantive deliverable. **A is defensible and assigned.**

**Scope streak: 13 → 14 → 15.**

## 7. Role Performance

**Gizmo:** Shining: T7 spec was decision-grade — single recommendation (C), CI-stack-growth flag surfaced proactively for HCD-delegated approval before T8 burned cycles, full migration plan with sequencing notes. Migration plan correctly anticipated the bootstrap nuance (PR #45 won't be gated by its own workflow). Struggling: nothing material this sub-sprint. Trend: ↑.

**Ett:** Did not participate this sub-sprint (S19.3.1 was a Bott-direct scope-out from S19.3 carry-forwards, not an Ett-planned sub-sprint).

**Nutts:** Shining: clean PR #45 with all 4 self-test labels applied at open; correctly sequenced label CRUD (create-then-PR per spec §7); identified `gh` CLI absence and pivoted to REST API without escalation. Correctly held back the 2 deferred-deletion labels rather than yanking them blindly. Struggling: tooling deviation note (gh CLI absent) is a workspace gap to track but not a Nutts deficiency. Trend: ↑.

**Boltz:** Shining: 7-check review PASS via `brott-studio-boltz[bot]` GitHub App; anti-#34 self-test verified — PR satisfied the contract it shipped before merge approval. Cleanly squash-merged at `1644448d`. Struggling: env vars (`BOLTZ_APP_ID`/`BOLTZ_INSTALLATION_ID`) not pre-exported in spawn — set inline (carry-forward 7, minor). Trend: →.

**Optic:** Shining: live workflow self-test in T10 was the audit-grade structural verification of this sub-sprint. Test PR #46 with deliberately-absent labels → workflow failure observed; labels added → workflow success observed; cleanup (PR closed, branch deleted, HTTP 204) executed cleanly. This pattern — actually exercising the gate against a real bad input — is a model for future workflow verifications and should be the template. Struggling: nothing material. Trend: ↑↑ (this sub-sprint, exemplary).

**Riv:** Did not participate this sub-sprint (S19.3.1 was orchestrated directly under The Bott + Riv-equivalent flow inside The Bott's main session, not a fresh Riv spawn — sub-sprint was small enough to run as a five-task chain without standing up a sub-orchestrator).

**Specc (self):** Sentinel held first-entry on inaugural production run after S19.3 dogfood. §A verify-before-write executed cleanly (404 on remote = `missing` branch, normal commit path). Used exec-heredoc from the start per S19.3 carry-forward 4 — write-tool path was never attempted, no retry burned. Trend: → (functioning as designed).

## 8. KB / institutional learning

No new KB entries this sub-sprint. The S19.3.1 work itself becomes institutional reference for two patterns worth naming:

- **Live workflow self-test pattern (Optic T10).** When shipping a CI gate, verify it by running a deliberately-bad PR through the gate and observing failure, then a deliberately-good PR and observing success. Sufficient and necessary; YAML-syntax checks alone are not. Future Optic verifications of CI gates should default to this pattern.
- **Bootstrap-PR-doesn't-gate-itself.** The PR that introduces a CI workflow does not run that workflow as a gating check on its own pre-merge state — the workflow file doesn't exist on main until merge. This is normal but reads as anomalous in audit history. Future framework changes that ship CI gates should call this out in the PR description so it's clear in the merge ledger.

Both patterns will be considered for KB entries in S19.4+ if recurring evidence accumulates.

---

**End of audit.**
