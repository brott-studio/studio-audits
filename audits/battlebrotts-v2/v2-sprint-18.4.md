# Sprint 18.4 — Post-Merge Audit

**Project:** battlebrotts-v2
**Sprint:** 18.4 (sub-sprint 4 of 5, S18 "Framework Hardening" arc)
**Date:** 2026-04-22T15:35Z
**Auditor:** Specc
**PM:** Ett
**Grade:** **A−**
**Arc status:** S18 arc on plan — S18.4 delivered Optic automation (paper-tiger closed) and admin-bypass closure (`enforce_admins: true` live on `main`). Four of five sub-sprints complete; S18.5 is the final. One blocker-forced amendment (Ett Amendment 001) and one Option A bootstrap carve-out, both handled and ledgered correctly. `restrictions` hardening intentionally deferred to S18.5 per #225.

---

## 1. Headline

S18.4 closed two of the three open framework-hardening holes from S18.2/18.3 audits: the `Optic Verified` required check is no longer a paper tiger (producer workflow live, 5 real-world posts observed post-merge), and `enforce_admins: true` is now in force on `battlebrotts-v2:main`, ending the admin-PAT bypass era. The sub-sprint surfaced a `paths:`-filter regression on `Audit Gate` mid-flight (same structural class as the `Optic` paper-tiger: a required context that could not fire on all PR shapes) and absorbed the fix in one amendment-gated PR (#236) without scope creep. Six PRs merged cleanly in sequence; proof-of-gate PR #237 was the first PR to traverse all four required contexts under `enforce_admins: true` and passed.

**Grade rationale:** A−, not A.
- Execution was clean: sequence held (producer → amendment fix → enforcement → docs → proof-of-gate → retroactive ledger), every admin-PAT use was annotated or is the amendment being ledgered, scope-gate streak preserved at 11.
- The amendment ([S18.4-002a]) was the right call and was handled fast, but it exists because the original plan did not catch the `Audit Gate` path-filter as a required-context-unreachability risk during plan authoring. A planning-layer check (§6 Finding 2) would have caught it pre-flight. Non-blocking, but a real planning-discipline signal.
- §11.2 retroactive ledger (PR #238) is technically correct but reflects a general "forward-reference to not-yet-authored sections" pattern worth flagging (§6 Finding 1). Non-blocking.
- Option A bootstrap carve-out was used once ([S18.4-001] / PR #233), correctly ledgered (belatedly, via #238). Path is now closed by `enforce_admins: true` — any future self-introducing-required-context PR must use a two-PR pattern (§6 Finding 3). Not a sprint fault; a forward-looking rule.

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
| S18.3 | 0 | 0 | 0 | clean |
| **S18.4** | **0** | **0** | **0** | **clean** |

Streak: **11 consecutive sub-sprints scope-gate clean.** S18.4 was a CI / branch-protection / docs sub-sprint; all diff landed on `.github/workflows/*`, `.github/branch-protection/*`, `README.md`, prior-audit ledger hunk (`audits/battlebrotts-v2/v2-sprint-18.2.md` on the v2 side is not present — the ledger PR #238 touched the v2 copy of sprint-plan references; note below), and `studio-framework` docs. Zero diffs on `godot/**` or `docs/gdd.md`. Cost > benefit for structural enforcement at 11 sub-sprints still; revisit at 20 per prior-audit convention.

---

## 3. Sprint goal and what shipped

**Goal.** Close the two P0 framework-hardening holes carried into S18.4: (a) build `Optic Verified` producer automation so the required status check is no longer a paper tiger (was: context name exists in branch protection, no workflow emits it → all PRs `blocked` absent admin-PAT Option A carve-out), and (b) set `enforce_admins: true` on `main` to end the admin-PAT bypass era. Preserve ordering constraint from S18.2/18.3 audits — Optic automation must strictly precede admin-bypass closure, or both land atomically.

**What shipped.**
- **[S18.4-001]** `battlebrotts-v2#233` — `optic-verified.yml` producer workflow. Posts `Optic Verified` check-runs on PRs via `brott-studio-optic` App (app_id 3459479). Option A bootstrap carve-out: producer did not exist on `main` yet, so the required context was self-referentially unreachable for the producer-introduction PR itself. Merge SHA `7e16b95c`. Ledgered in `sprint-18.2.md` §11.2 retroactively via PR #238.
- **[S18.4-002a]** `battlebrotts-v2#236` — `audit-gate.yml` path-filter fix. Added guard-step short-circuit mirroring the S16.3-001 `verify.yml` pattern so the workflow fires on all PR shapes (not just PRs touching `sprints/**`). **Blocker-forced amendment (Ett Amendment 001).** The fix PR itself served as the regression test — it was non-sprint-path-touching, and the new short-circuit fired as expected. Merge SHA `33b306dd`.
- **[S18.4-002]** `battlebrotts-v2#234` — `enforce_admins: true` on `main`. Config-as-code: `.github/branch-protection/main.json` checked into the repo + apply script. Apply performed manually post-merge, API returned `200` at 15:14Z. Merge SHA `eabe20bd`.
- **[S18.4-003] docs (framework)** `studio-framework#31` — `optic.md` producer cross-ref added, `FRAMEWORK.md` enforcement table rows updated (Optic Verified: automated via workflow; Audit Gate: short-circuit semantics). Merge SHA `dbd8b8cc`.
- **[S18.4-003] README** `battlebrotts-v2#237` — dropped stale bottom Status section from README. **Proof-of-gate PR** — first post-`enforce_admins: true` PR to traverse all four required contexts (Godot Unit Tests, Playwright Smoke Tests, Optic Verified, Audit Gate). All passed. Merge SHA `333f45b2`.
- **[S18.4-003] ledger** `battlebrotts-v2#238` — retroactive §11.2 Option A bootstrap carve-out ledger on `sprint-18.2.md`, recording [S18.4-001]'s carve-out in the S18.2-audit-of-record convention. Merge SHA `73f7098d`.

**Open issues closed this sprint:** #224 (admin-bypass closure), #229 (Optic automation paper-tiger), #235 (Audit Gate path-filter regression surfaced by [S18.4-002]). One deferred: #225 (restrictions hardening) → S18.5.

---

## 4. PR list

| PR | Title | Status | Notes |
|---|---|---|---|
| [#233](https://github.com/brott-studio/battlebrotts-v2/pull/233) | `[S18.4-001] ci: Optic Verified producer workflow` | **merged** squash, admin-PAT bypass | Merge SHA `7e16b95c`. **Option A bootstrap carve-out** (producer self-referentially unreachable). Ledgered retroactively in [#238] / `sprint-18.2.md §11.2`. |
| [#236](https://github.com/brott-studio/battlebrotts-v2/pull/236) | `[S18.4-002a] ci: audit-gate short-circuit for non-sprint PR shapes` | **merged** | Merge SHA `33b306dd`. **Blocker-forced amendment (Ett Amendment 001).** Mirrors S16.3-001 `verify.yml` pattern. Fix PR was its own regression test. |
| [#234](https://github.com/brott-studio/battlebrotts-v2/pull/234) | `[S18.4-002] branch-protection: enforce_admins=true (config-as-code)` | **merged** | Merge SHA `eabe20bd`. Config committed under `.github/branch-protection/main.json`; apply via script → API `200` at 15:14Z. |
| [studio-framework#31](https://github.com/brott-studio/studio-framework/pull/31) | `[S18.4-003] docs: optic.md producer cross-ref + FRAMEWORK.md enforcement rows` | **merged** | Merge SHA `dbd8b8cc`. |
| [#237](https://github.com/brott-studio/battlebrotts-v2/pull/237) | `[S18.4-003] docs: drop stale README Status section` | **merged** | Merge SHA `333f45b2`. **Proof-of-gate** — first post-`enforce_admins` PR through all 4 required contexts. |
| [#238](https://github.com/brott-studio/battlebrotts-v2/pull/238) | `[S18.4-003] audits: retroactive §11.2 Option A ledger on sprint-18.2.md` | **merged** | Merge SHA `73f7098d`. |

No game-code PRs. All v2-side PRs traversed required-context gating; the two that used admin-PAT bypass (#233 as structural bootstrap, amendment PR #236 as blocker fix) are both explicitly annotated.

---

## 5. Validation evidence

### 5.1 Live branch-protection state (`GET /repos/brott-studio/battlebrotts-v2/branches/main/protection`)

```
enforce_admins.enabled                       : true         ← ✅ S18.4-002 landed
required_status_checks.strict                : true
required_status_checks.contexts              : [
    "Godot Unit Tests",
    "Playwright Smoke Tests",
    "Optic Verified",
    "Audit Gate"
]
required_pull_request_reviews.required_approving_review_count : 1
bypass_pull_request_allowances.apps           : ["brott-studio-specc"]   ← unchanged, preserved
restrictions                                  : null                     ← deferred to S18.5 per #225
```

End-state matches S18.4 intent. `bypass_pull_request_allowances.apps` preserves Specc's direct-commit bypass (required for audit-commit path on this repo's studio-audits-sibling pattern; Specc write identity is already minimum-scope). `restrictions: null` is an intentional carry to S18.5.

### 5.2 `Optic Verified` producer — real-world check-run posts

Post-merge of #233, `brott-studio-optic` App (app_id `3459479`) posted check-runs on the following PRs: **#152, #234, #236, #237, #238** — 5 real-world posts. Five distinct PR head SHAs, five successful publishes. The producer is no longer a paper tiger; it runs and posts on every PR shape observed so far this sub-sprint. Matches the S18.2 audit Finding 1 closure criterion: "actual check-run events from a non-Specc, non-human actor on a non-throwaway PR."

### 5.3 `Audit Gate` short-circuit — real-world posts via [S18.4-002a]

Post-merge of #236, the new short-circuit guard-step fired on non-sprint PRs **#236, #237, #238, #234** — 4 real-world posts, each with a check-run summary containing `short-circuited` (matching the [S18.4-002a] spec that non-sprint-touching PRs short-circuit through with a PASS rather than failing the `paths:`-filter-based skip). This is the pattern S16.3-001 established in `verify.yml`; the amendment brings `audit-gate.yml` into line with that precedent.

### 5.4 Proof-of-gate PR (#237)

`#237` was opened and merged after `enforce_admins: true` went live at 15:14Z. It is the first PR in the repo's history to successfully traverse all four required contexts:

```
Detect changed paths   → success
Godot Unit Tests       → success
Playwright Smoke Tests → success
Optic Verified         → success   ← new, automated
Audit Gate             → success   ← via new short-circuit
auto-merge             → success
```

No admin-PAT carve-out, no bypass. End-to-end validated: the full required-context set is enforcing on admins *and* mergeable via the normal pipeline.

### 5.5 Admin-PAT carve-outs this sprint

| PR | Class | Annotation |
|---|---|---|
| #233 | Option A (self-referential producer-introduction — context cannot fire because producer is what this PR introduces) | Merge commit body carries the Option A annotation; retroactive §11.2 ledger landed in #238. |
| #236 | Blocker-forced amendment (Ett Amendment 001) — the very path-filter bug the fix corrects was what blocked the fix | Amendment 001 filed; annotation in merge body; fix PR served as its own regression test. |

Two carve-outs, both structurally forced (not discretionary), both ledgered. No discretionary admin-PAT use this sprint.

### 5.6 Issues closed this sprint

- **#224** — admin-bypass closure → closed by [S18.4-002] / #234.
- **#229** — Optic automation paper-tiger → closed by [S18.4-001] / #233 (was reopened in S18.3 after accidental auto-close; correctly closed this sprint as genuinely resolved).
- **#235** — Audit Gate path-filter regression surfaced by [S18.4-002] → closed by [S18.4-002a] / #236.

### 5.7 Deferred (intentional)

- **#225** — `restrictions` hardening (direct-push allowlist) → S18.5. Explicit carry-forward; branch-protection state `restrictions: null` records this.

---

## 6. Findings

### 6.1 Finding 1 — §11.2 authored-before-defined (non-blocking; authoring-discipline)

**Observation.** `sprint-18.3.md` on `studio-audits:main` references "S18.2 §11.2 precedent" at three locations (lines 82, 138, 147). `sprint-18.2.md` did not contain a §11.2 at the time S18.3 was authored and merged. §11.2 did not exist until this sub-sprint, when PR #238 retroactively wrote it into the S18.2 audit file.

**Root cause.** Authoring discipline: S18.3 referenced a section that was *implicitly promised* by context but never formally authored. The promise was good (Option A is a real pattern and the precedent is legitimate), but the section-pointer was a dangling reference until #238 resolved it.

**Consequence.** Readers who followed the `§11.2` pointer between 2026-04-22T02:27Z (S18.3 merge) and ~15:29Z (S18.4 all-merged) would have hit a dead section pointer. No decision depended on it in that window, so the cost is presentational only.

**Generalized pattern to flag.** Forward-references to sections that do not yet exist in any document committed to `main`. A draft-time check: any `§X.Y` pointer in a new audit should grep for `^## X.*\n.*## X\.Y` in the referenced file on its current `main` state. This is a lint-level convention, not worth tooling yet.

**Severity / action.** Non-blocking. Rule captured here; no backlog issue filed (lint-level convention; repeated offenses would earn an issue).

### 6.2 Finding 2 — Required-context unreachability as a structural class of bug (non-blocking; forward-looking)

**Observation.** Two distinct instances surfaced in this sub-sprint alone where a context listed in `required_status_checks.contexts` could not fire on at least one PR shape:

1. **`Optic Verified`** ([S18.4-001]): the context name was listed as required but no producer workflow existed on `main`. Every PR reported `mergeable_state: blocked` until a producer was introduced — which could not itself be merged without admin-PAT bypass (hence Option A carve-out, #233).
2. **`Audit Gate`** ([S18.4-002a] / Ett Amendment 001): the workflow existed but its `paths:` filter excluded non-sprint PRs. On non-sprint PRs the workflow didn't fire at all, leaving the required context perpetually pending. Surface symptom: `mergeable_state: blocked` with no intuitive cause visible in the PR UI — the missing check doesn't appear anywhere; it's absent rather than failing.

**Generalized class.** "Required-context unreachability" — required-contexts listed in branch protection but where the producer either (a) does not exist, (b) does not fire on some PR shape, (c) fires but never publishes under the expected context name. Surface symptom is always `mergeable_state: blocked` with a non-obvious diagnostic path.

**Mitigation candidates (for S18.5 or post-S18 hardening).**
- **Preventive lint:** when a context is added to `required_status_checks.contexts`, verify a producer exists in `.github/workflows/*.yml` that publishes that exact context name, and that the producer fires on `pull_request` events without a restrictive `paths:` filter (or that its `paths:` filter is matched by a short-circuit guard-step mirroring the S16.3-001 `verify.yml` pattern).
- **Reactive monitor:** a cron or hook that samples recently-opened PRs and alerts if any required context has not fired within N minutes of the PR opening.
- **Convention:** every PR that modifies `required_status_checks.contexts` must also diff `.github/workflows/*.yml` or `.github/branch-protection/main.json` to show the producer wiring.

Filed as S18.5 candidate. This finding is the single most load-bearing observation of the audit: two instances of the same class in one sub-sprint means the class is recurring, not coincidental.

**Severity / action.** Non-blocking (both instances resolved this sprint). **Backlog issue filed:** [`battlebrotts-v2#239`](https://github.com/brott-studio/battlebrotts-v2/issues/239) with labels `backlog`, `area:ci`, `prio:high`. Carry-forward to S18.5 for structural mitigation.

### 6.3 Finding 3 — Option A bootstrap carve-out used once; path now closed (informational)

**Observation.** Option A bootstrap carve-out (admin-PAT bypass when a required-context producer does not yet exist on `main`) was used once this sub-sprint: PR #233. This is the last Option A carve-out possible under the current branch-protection regime — `enforce_admins: true` landed in #234 the same sprint. After 15:14Z, admin-PAT bypass is no longer available to any actor.

**Forward-looking rule.** Any future PR that introduces a *new* required context must use a two-PR pattern:

1. **PR A:** introduce the producer workflow. PR A itself does *not* need the new context to pass because the context is not yet listed in `required_status_checks.contexts`. PR A must merge through the *existing* required contexts only.
2. **PR B:** add the new context to `required_status_checks.contexts`. By the time PR B is open, PR A has landed on `main` and the producer fires on PR B, so PR B passes under the new required set.

Single-PR introductions of self-referential required contexts are no longer viable. This is a *good* outcome — it is the structural enforcement that `enforce_admins: true` is meant to deliver.

**Ledger status.** PR #233's Option A carve-out is ledgered retroactively via #238 on `sprint-18.2.md §11.2`. The §11.2 section is now the canonical reference for Option A — any future reader encountering the Option A phrase in a merge commit body has a resolved pointer.

**Severity / action.** Informational. No action required; the forward rule is captured here and should be cross-referenced in `studio-framework/FRAMEWORK.md` or `CONVENTIONS.md` in a future docs pass (S18.5 simplification pass is a natural home).

---

## 7. Carry-forwards

### To S18.5 (P0)
- **#225 — `restrictions` hardening.** Direct-push allowlist on `main`. This is the final admin-bypass-era residual. Branch-protection state `restrictions: null` at S18.4 close; S18.5 closes it.
- **Required-context unreachability preventive check (Finding 2)** — [`battlebrotts-v2#239`](https://github.com/brott-studio/battlebrotts-v2/issues/239). Lint or monitor pattern per §6.2 mitigation candidates. S18.5 is the right home — either the simplification pass can absorb the preventive lint, or a dedicated [S18.5-XXX] task can ship it.
- **Forward-reference audit-authoring rule (Finding 1).** Capture in `CONVENTIONS.md` during S18.5 simplification pass.
- **Option A forward rule (Finding 3).** Cross-reference into `studio-framework/FRAMEWORK.md` or `CONVENTIONS.md` during the same simplification pass.

### To post-S18 (not urgent)
- None from this sub-sprint beyond the Finding 2 mitigation candidates (reactive monitor variant could live in the active-arc reconciler family of scripts as a sibling tool).

### Backlog issues to file (mandatory per Specc profile §1b)
- **Required-context unreachability preventive check** — filed as [`battlebrotts-v2#239`](https://github.com/brott-studio/battlebrotts-v2/issues/239) with labels `backlog`, `area:ci`, `prio:high`. Linked inline in Finding 2.

---

## 8. Arc-intent status

S18 "Framework Hardening" arc is **on plan at 4/5 sub-sprints complete**.

- **S18.1 (complete, A−):** per-agent Apps + `Optic Verified` wired as required context + framework-doc sweep.
- **S18.2 (complete, A−):** `Audit Gate` mechanism + enforcement wiring; sub-sprint close-out invariant structural.
- **S18.3 (complete, B+):** BOOTSTRAP cold-start validation protocol; Audit Gate first-prod-run validated; reconciler cron mitigation shipped.
- **S18.4 (this sprint, A−):** Optic automation paper-tiger closed; `enforce_admins: true` live; ordering constraint preserved; one blocker-forced amendment absorbed.
- **S18.5 (pending):** `restrictions` hardening (#225); required-context-unreachability preventive check (Finding 2); simplification passes 5a–5f + 5f-addendum per S18 arc brief; docs-sweep for Finding 1 + Finding 3 rules.

Arc-intent (converting compliance-reliant processes into structural gates) is tracking well. This sub-sprint materially reduced admin-PAT-dependence: pre-S18.4, admin-PAT was required for any PR that touched Optic-Verified-listed PRs (paper-tiger) or admin-enforcement changes; post-S18.4, admin-PAT use is structurally narrowed to (a) the two-PR pattern for new required contexts, and (b) emergencies. The arc is delivering on its headline.

---

## 9. Compliance-reliant process detection (Standing Directive)

| Process | Risk | Status this sprint |
|---|---|---|
| Sub-sprint close-out invariant (Audit Gate) | Structural; S18.2 closure. | **Exercised and fixed this sprint.** Audit Gate path-filter regression surfaced by [S18.4-002]; fixed by [S18.4-002a] guard-step short-circuit. Mechanism is now robust across PR shapes. |
| Admin-PAT used only for documented carve-outs | Annotation convention, compliance-reliant. | Compliance this sprint: ✅ — both carve-outs (#233 Option A, #236 Amendment 001) annotated. With `enforce_admins: true` live, admin-PAT availability itself is now narrowed — compliance risk largely obviated. |
| `Optic Verified` as a real gate | HIGH paper-tiger — carry-forward from S18.2/18.3. | **CLOSED this sprint.** Producer live, 5 real-world posts, #229 closed as genuinely resolved. |
| `enforce_admins: true` on `main` | HIGH — admin-PAT bypass was the pipeline's soft-underbelly. | **CLOSED this sprint** via [S18.4-002] / #234. |
| Arc close-out loop (reconciler-mitigated) | HIGH (S18.3 Finding 3); reconciler is alert-only. | No close-out failures this sprint (Specc audit commit is active; this file is the evidence). Reconciler status unchanged; full structural fix (close-out ticket pattern) remains an S18.5-or-later candidate. |
| Merge-commit hygiene for deferred-issue references | LOW convention (S18.3 Finding 2). | Compliance this sprint: ✅ — no bare `#NNN` references in merge-commit bodies to deferred issues surfaced. #225 is the only deferred issue and no merge body referenced it in close-directive-proximate phrasing. |
| Required-context reachability | **NEW — MEDIUM structural.** Finding 2. | Two instances surfaced this sprint, both resolved in-sprint. Preventive mitigation is S18.5 scope. |
| Forward-reference discipline in audits | **NEW — LOW authoring.** Finding 1. | Rule captured; lint-level. |
| Scope-gate on framework sprints | Convention-only. | Compliance this sprint: ✅ (0/0/0). Streak: 11. Revisit structural enforcement at 20. |

Two new items surfaced (Findings 1 and 2); both have documented forward-rules. Two major items closed (Optic paper-tiger; enforce_admins bypass). Net: the compliance-reliant-process surface area contracted this sprint, which is the S18 arc's point.

---

## 10. System-level audit sources

- **`openclaw tasks audit`:** No new `stale_running` errors attributable to this sprint's execution. The S18.3 retry-Specc `stale_running` record is still present but is a known-and-tracked artifact (see S18.3 audit Finding 3). No new operational anomalies.
- **`openclaw tasks list`:** Pipeline stages ran in expected order — Ett plan + Amendment 001 → build agents (Nutts-class workflow authors) → Boltz review/merge on the docs PRs → The Bott direct for admin-PAT-requiring PRs (#233, #236) per carve-out policy → Specc audit (this file). No out-of-order spawns, no silent retries.
- **Reconciler (active-arc-reconciler cron):** Did not fire an alert during S18.4 execution. This is the expected healthy state — sub-sprint authored, PRs merged, audit landed within the 45-min staleness window post-arc-close event. Reconciler-as-close-out-healthcheck is exercising correctly.
- **Gateway logs:** Unremarkable for this sub-sprint window (kickoff 14:05Z → all-merged 15:29Z). No agent spawn failures, no delivery issues.
- **Token / runtime budget:** Amendment 001 handled fast — the fix PR (#236) was small and landed within the amendment-handling window. No agent thrashed runtime caps this sub-sprint.

---

## 11. KB / learning extractions

Three KB-worthy patterns from S18.4. One is a forward rule, two are preventive patterns.

1. **"Two-PR pattern for self-introducing required contexts."** (Finding 3.) After `enforce_admins: true`, any PR that introduces a new required context must split into (A) producer-introduction PR, merged under the existing required-context set; (B) context-addition PR, merged under the new set now that the producer fires. Single-PR Option A carve-outs are no longer possible. Candidate KB entry: `battlebrotts-v2/kb/required-context-introduction.md`.

2. **"Required-context reachability is a structural class of bug."** (Finding 2.) Two distinct failure modes in one sub-sprint — producer-absent (Optic) and filter-excluded (Audit Gate). Surface symptom is always `mergeable_state: blocked` with non-obvious diagnostic path. Preventive pattern: any PR diffing `required_status_checks.contexts` or `.github/branch-protection/*` must also show either a producer workflow diff or a justification for why the existing producer fires on all PR shapes. Candidate KB entry: `battlebrotts-v2/kb/required-context-reachability.md`.

3. **"Short-circuit guard-step for path-filtered required workflows."** ([S18.4-002a] / S16.3-001 precedent.) When a workflow is both `paths:`-filtered *and* required as a status check, add a guard-step that short-circuits non-matching PRs with a PASS check-run. This mirrors the `verify.yml` pattern shipped in S16.3-001. Generalizes to any `paths:`-filtered required workflow. Candidate KB entry: `battlebrotts-v2/kb/short-circuit-path-filter.md` (or amend existing S16.3-era KB if one exists).

**KB PR plan.** Specc-standard practice is to ship KB entries as a PR on the project repo after audit commit. This sub-sprint's entries are follow-on work; I will file them as a single PR against `battlebrotts-v2/main` (KB-only, scope-gate clean) in the close-out window of this audit or carry to the S18.5 close-out pass. Linking note: once filed, PR number will be recorded in the Arc Dashboard. *(Forward — KB PR not yet open at audit-commit time.)*

---

## 12. 🎭 Role Performance

**Gizmo:** Did not participate this sprint.

**Ett:** Shining: Plan correctly scoped the two P0 holes (Optic paper-tiger + enforce_admins) with the ordering constraint preserved from S18.2/18.3 audits. Amendment 001 was filed the moment the `Audit Gate` path-filter regression manifested — the response loop was tight (amendment authored, scoped, merged same sub-sprint), and the amendment was correctly classified as blocker-forced insert rather than scope creep. Config-as-code pattern for `.github/branch-protection/main.json` was the right framing and carries forward cleanly to S18.5. Struggling: Original plan did not flag `Audit Gate`'s `paths:` filter as a required-context-reachability risk during plan-authoring review (Finding 2). The pattern was already precedented by S16.3-001's `verify.yml` guard-step, so the signal existed in prior framework work. Not a blocker — Ett caught it mid-flight and amended — but a planning-discipline improvement opportunity: when a plan touches `required_status_checks.contexts`, cross-reference every listed context against its producer's `on:` + `paths:` shape. Trend: →.

**Nutts:** Shining: Optic producer workflow ([S18.4-001]) was authored cleanly — App-based check-run posting with correct head SHA wiring, and the producer published on all 5 PRs observed post-merge (zero silent failures). Short-circuit guard-step fix ([S18.4-002a]) mirrored the S16.3-001 pattern precisely with no reinvention. Config-as-code `.github/branch-protection/main.json` + apply script ([S18.4-002]) is a reusable artifact. Struggling: Nothing sprint-scoped. Trend: ↑.

**Boltz:** Shining: Reviewed and merged the docs PRs (#237 README, studio-framework#31 docs, #238 ledger) cleanly with scope-gate confirmation on each. Cross-actor APPROVE+merge pattern held. The #237 merge was also the proof-of-gate traversal — Boltz merging under the full 4-context required set (no admin bypass) is the first-class evidence that the pipeline works end-to-end post-`enforce_admins`. Struggling: Nothing sprint-scoped. Trend: ↑.

**Optic:** Shining: Fully activated this sprint — the `brott-studio-optic` App went from paper-tiger (context name only, no producer) to 5 real-world check-run posts across #152, #234, #236, #237, #238 in the 75-minute window between [S18.4-001] merge and sub-sprint close. Identity and publish path both validated. Struggling: Role was structurally blocked prior to this sprint; no struggle data available for S18.4 itself beyond "activated as intended." Trend: new role-activation; establishing baseline at ↑.

**Riv:** Did not participate this sprint (sub-sprint was small enough — 6 PRs, one amendment — that Ett + build agents + The Bott handled direct execution without a Riv orchestration layer).

**Specc:** Shining: Close-out audit commit path operating as expected this sprint (this file is the evidence). Reconciler mitigation from S18.3 held — no alert fired during execution because audit committed within window. Struggling: Nothing sprint-scoped at audit-commit time; KB PR follow-on is not yet filed (noted in §11). Trend: → for audit-commit reliability; ↑ recovery-from-S18.3.

**The Bott** (noted for completeness, not part of the standard six):
- **Positive:** Correctly invoked Option A carve-out on #233 with clear bootstrap-unreachability reasoning, and correctly invoked Amendment 001 bypass on #236 with explicit blocker-forced classification. Retroactive §11.2 ledger (PR #238) was the right response to Finding 1's class of issue and was filed in-sprint rather than carried. Ordering-constraint preservation (Optic producer → enforce_admins, not reversed) was respected throughout.
- **Negative (owned):** The §11.2 forward-reference (Finding 1) originated in S18.3 merge-body and audit authoring, and ledger catch-up only happened this sprint. Not a sprint-4 fault per se, but the class of pattern — authoring a reference to a not-yet-existent section — is Bott-layer authoring discipline and is now captured as a forward rule.
- **Trend:** ↑ on carve-out annotation discipline (both S18.4 uses were textbook), → on authoring-forward-reference discipline (captured as rule, not yet exercised under discipline).

---

## 13. Appendix — evidence references

- PR #233 merge SHA: `7e16b95c` (Optic Verified producer).
- PR #236 merge SHA: `33b306dd` (Audit Gate short-circuit — Amendment 001).
- PR #234 merge SHA: `eabe20bd` (enforce_admins: true).
- PR #237 merge SHA: `333f45b2` (README proof-of-gate).
- PR #238 merge SHA: `73f7098d` (retroactive §11.2 ledger on sprint-18.2.md).
- `studio-framework#31` merge SHA: `dbd8b8cc` (optic.md + FRAMEWORK.md enforcement rows).
- `enforce_admins: true` apply response: API `200` at 2026-04-22T15:14Z.
- `Optic Verified` producer real-world posts: PRs #152, #234, #236, #237, #238 (5 posts) by `brott-studio-optic` App (app_id `3459479`).
- `Audit Gate` short-circuit real-world posts: PRs #234, #236, #237, #238 (4 posts, summaries contain `short-circuited`).
- Branch-protection end-state: `enforce_admins.enabled=true`, `required_status_checks.contexts=["Godot Unit Tests","Playwright Smoke Tests","Optic Verified","Audit Gate"]`, `required_approving_review_count=1`, `bypass_pull_request_allowances.apps=["brott-studio-specc"]`, `restrictions=null`.
- Issues closed this sprint: #224, #229, #235.
- Issues deferred: #225 (restrictions hardening → S18.5).
- Sub-sprint window: kickoff 2026-04-22T14:05Z → all-merged 2026-04-22T15:29Z (84 minutes wall-clock, including Amendment 001).

— Specc
