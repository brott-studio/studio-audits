# Sprint 16.3 — Main-branch CI Observability (S16 arc close)

**Auditor:** Specc (`brott-studio-specc[bot]`, App ID `3444613`)
**Date:** 2026-04-20T19:05Z
**Sprint:** S16.3 (ops/infra — `push: main` trigger + warnings-policy paper trail)
**Build set:** PR #153 (`d04426ea`), PR #154 (`6ebe4ffb`), Optic S16.3-003 verification (no PR)
**Verify:** push:main run `24684730563` ✅; PR-trigger runs on sub-sprint heads ✅; Optic V1–V8 all PASS
**Grade:** **A**

---

## 1. Headline

S16.3 exit criteria HOLD on `main` as of 2026-04-20T19:05Z. The `push: main` trigger is live and produced its first green Verify run on the S16.3-001 merge commit itself (smoke-gun `24684730563`); the warnings-as-errors paper trail landed as a standalone KB doc (`docs/kb/warnings-as-errors-policy-s16.3.md`) documenting the aligned-by-construction finding; and Optic's V1–V8 probes all PASS with independent re-verification in this audit. The scope gate held cleanly across both PRs — zero diff under `godot/combat/**`, `godot/data/**`, `godot/arena/**`, or `docs/gdd.md`. This is the third HCD acceptance criterion for the S16 arc, and with it the arc closes. Clean A.

---

## 2. Summary

**Goal.** Per `sprints/sprint-16.3.md`: make main-branch CI health visible in real time by adding a `push: main` trigger to `verify.yml`, and produce a paper-trail confirmation that the GDScript warnings-as-errors policy is consistent between local Godot 4.4.1 headless and CI Godot 4.4.1 headless. S16.3-003 (Optic verification) validates both and explicitly calls the arc-acceptance moment.

**What happened.** S16.3-001 (PR #153, merged 2026-04-20T18:57Z at `d04426ea`) added the `push: main` trigger and parameterized the `changes` job's diff range by event type (implementation (a): `github.event.before..github.sha` on push, unchanged `base.sha..head.sha` on PR), with fallbacks that force `code=true` on zero-SHA / git-diff-failure / unknown-event edge cases. The inline YAML comment documenting the no-`paths-ignore` decision is in place and substantive (9 lines explaining the required-status-check deadlock rationale and directing future agents to the sprint plan). S16.3-002 (PR #154, merged 2026-04-20T18:54Z at `6ebe4ffb`) landed a 29-line KB doc; the finding is **aligned by construction** — `godot/project.godot` declares no `debug/gdscript/warnings/*` entries, so both local and CI resolve to identical Godot 4.4.1 engine defaults, and divergence is structurally impossible without a `project.godot` edit. S16.3-003 (no PR; Optic verification doc) produced V1–V8 all PASS, including smoke-gun confirmation that push-triggered run `24684730563` on merge SHA `d04426ea` is green.

**Outcome.** Main-branch CI is now observable in real time. Every merge to `main` produces a Verify run in the Actions tab; doc-only merges still short-circuit correctly via the parameterized `changes` job; the warnings-as-errors policy has a written paper trail; and all three HCD acceptance criteria for the S16 arc are met. This sub-sprint is also the arc-close moment for S16.

**Player POV.** No change. CI/ops only.

---

## 3. Acceptance verification

Each exit criterion from `sprints/sprint-16.3.md` re-verified against `main` today (2026-04-20, HEAD `d04426e`).

### 3.1 All three tasks landed ✅

| Task | Owner | PR | Merge SHA | Merged |
|---|---|---|---|---|
| S16.3-001 push:main trigger | Patch | [#153](https://github.com/brott-studio/battlebrotts-v2/pull/153) | `d04426ea` | 2026-04-20T18:57:53Z |
| S16.3-002 warnings-as-errors paper trail | Nutts | [#154](https://github.com/brott-studio/battlebrotts-v2/pull/154) | `6ebe4ffb` | 2026-04-20T18:54:25Z |
| S16.3-003 E2E validation + arc-acceptance | Optic | — (verification doc, no PR) | — | 2026-04-20 (pre-audit) |

### 3.2 `push: main` trigger present, no `paths-ignore`, inline comment explains the decision ✅

Verified against `.github/workflows/verify.yml` at HEAD `d04426e`:

- `on.push.branches: [main]` present (line 13).
- No `paths-ignore` on the push trigger.
- Inline YAML comment (lines 5–12) documents the decision, names the required-status-checks deadlock rationale, and explicitly directs future agents not to re-propose `paths-ignore`. Comment text: "DO NOT add `paths-ignore` here — mirror the PR trigger's pattern. The `changes` job below handles doc-only short-circuit at runtime, giving us a single source of truth for 'what counts as doc-only' across both event types. Adding `paths-ignore` on push would also create asymmetry with the PR trigger and re-introduce the required-status-checks deadlock risk on any future push-scoped required check."

This wording is strong — it names the asymmetry risk in addition to the deadlock, so the next agent reading this has two independent reasons for the decision rather than one.

### 3.3 `changes` job correctly handles push events ✅ (independent verification)

I read the `changes` job logic line-by-line rather than trusting the PR description:

- Event-type dispatch is a shell `if` on `$EVENT_NAME`, with SHAs injected via `env:` (not expression interpolation). This is the correct pattern — unset `pull_request.*.sha` on a push event would otherwise inject empty strings into shell and produce `git diff ""..""` failures. The `env:` injection pattern neutralizes that.
- Push path: `base_sha="$PUSH_BEFORE_SHA"`, `head_sha="$PUSH_HEAD_SHA"`. If `base_sha` is empty or all-zeros (branch-creation push edge case), forces `code=true` and exits. Correct conservative fallback.
- `git diff` failure fallback: if `git diff` returns non-zero (force-push edge case, missing SHA), forces `code=true`. Correct.
- Unknown event fallback (e.g. `workflow_dispatch`): forces `code=true`. Correct.
- Same glob rules (`docs/*`, `sprints/*`, `*.md` → doc-only) apply across both event types → single source of truth on doc-only classification holds.

Smoke-gun evidence: push-triggered run `24684730563` on merge SHA `d04426ea` (the S16.3-001 merge itself) is ✅. The run's `changes` job correctly classified the merge as code (verify.yml change), invoked the full suite, and reported success.

### 3.4 Doc-only merges still short-circuit ✅

This is structurally verifiable from the `changes` job logic (same glob rules apply to push events). No push-triggered run has hit a doc-only merge yet in the narrow window since S16.3-001 merged (the only post-S16.3-001 merge to main was not doc-only), so this is design-verified rather than runtime-verified. Accepting design verification is correct here — the logic is mechanically symmetric with the PR path, which has been exercised heavily.

### 3.5 S16.3-002 warnings-as-errors paper trail landed ✅

Verified `docs/kb/warnings-as-errors-policy-s16.3.md` exists and meets acceptance:

- Settings compared verbatim (local and CI both load `godot/project.godot` via `--path godot/`).
- `godot/project.godot` enumerated in full (23 lines); confirmed no `debug/gdscript/warnings/*` entries and no `warnings_as_errors` override.
- Verdict stated: **aligned by construction**. Divergence structurally impossible without a `project.godot` edit.
- Spot-check of recent green code-path run (`24675088337` / S16.2-005) confirms `arena_renderer.gd` warning fix from S16.1-006 is intact and has not re-surfaced.
- Runtime-shutdown warnings (ObjectDB / RID leak diagnostics) and test-asserted SCRIPT ERROR lines are correctly disambiguated as orthogonal to `warnings_as_errors`.

Ett's tightened requirement ("a paper trail for the arc close rather than verbal") is satisfied with a real PR and a real KB artifact. Honest no-op finding, properly documented.

### 3.6 S16.3-003 two-green-runs acceptance ✅

- **push:main green:** run `24684730563` on `d04426ea` (S16.3-001 merge commit). **Success.**
- **pull_request green(s) on sub-sprint heads:** runs `24684211274` and `24684602984` on `sprint-16.3-001-push-main-trigger`, run `24684284054` on `sprint-16.3-002-warnings-consistency`. All **success**.
- **Arc-acceptance framing:** per Riv's context summary of Optic's report, the verification doc explicitly declares "S16 arc complete — all three HCD acceptance criteria met" with per-criterion pointers (see §4 of this audit for the formal restatement).

Acceptance met, with redundancy (multiple PR greens rather than just one).

### 3.7 Scope gate held ✅

Verified programmatically — see §4 below.

### 3.8 No role/authority/policy changes ✅

- S16.3-001 diff is `.github/workflows/verify.yml` only (52 additions, 5 deletions).
- S16.3-002 diff is `docs/kb/warnings-as-errors-policy-s16.3.md` only (29 additions, 0 deletions).
- Zero changes to `studio-framework/` in either PR. No agent profile edits, no PIPELINE.md / FRAMEWORK.md / CONVENTIONS.md touches.
- Warnings policy itself is unchanged — S16.3-002 is a *confirmation* artifact, not a policy edit.

---

## 4. Formal S16 arc-acceptance statement (restated)

Per Riv's context summary of Optic's S16.3-003 report, all three HCD acceptance criteria for the S16 arc are met. Restated formally with per-criterion evidence pointers:

1. **`Godot Unit Tests` passes cleanly on `main` (`push: main`) AND on a dummy code-path PR — both ✅.**
   - push:main: run [`24684730563`](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24684730563) on merge SHA `d04426ea` — success.
   - dummy code-path PR: runs `24684211274` / `24684602984` (PR #153 head) and `24684284054` (PR #154 head) — all success.

2. **`test_runner.gd` enumerates all sprint test files explicitly — no reliance on shell glob `|| exit 1`.**
   - Satisfied by S16.1-005 (merge `36e64f8`) + S16.2-005 enumeration extensions.
   - Current `SPRINT_TEST_FILES` enumerates 24 sprint test files (verified in S16.2 audit §3.5 and re-confirmed in the Optic V1–V8 enumeration probe, 24/24).

3. **At least one agent (Specc) has a per-agent GitHub App or equivalent distinct identity wired into the review/merge path.**
   - Satisfied by S16.2 (App ID `3444613`, installation `125608421`).
   - Cross-actor flow proven at PR #149 (`Nutts-authors → Specc-approves`, HTTP 200).
   - Reference trail: `docs/kb/per-agent-github-apps.md` + S16.2 audit (`v2-sprint-16.2.md`, Grade A).

All three criteria MET. **S16 arc complete.**

---

## 5. Scope-gate verification (independent)

The S16.3 plan declared scope gate: `godot/combat/**`, `godot/data/**`, `godot/arena/**`, `docs/gdd.md` untouched.

Command used per merge SHA:
```
git show --name-only <sha> | grep -E "^(godot/combat|godot/data|godot/arena|docs/gdd\.md)"
```

| Merge | Hit under gated paths? |
|---|---|
| `d04426e` (S16.3-001, verify.yml only) | clean |
| `6ebe4ff` (S16.3-002, docs/kb/ only) | clean |

**Gate holds.** This is the fourth consecutive sub-sprint (S15.2 → S16.1 → S16.2 → S16.3) to hold a non-trivial scope gate cleanly. Pattern is reliable.

---

## 6. Per-task review

### S16.3-001 — Add `push: main` trigger to `verify.yml` ✅

- **PR:** [#153](https://github.com/brott-studio/battlebrotts-v2/pull/153) — merge SHA `d04426ea`.
- **Owner:** Patch. Reviewer: Boltz (COMMENT review — see §7 cross-actor note). Approver of record: `brott-studio-specc[bot]` (APPROVED 2026-04-20T18:54:23Z).
- **Merged by:** `brott-studio-specc[bot]` (Specc App identity).
- **Evidence:** `.github/workflows/verify.yml` at HEAD — push trigger live, no `paths-ignore`, inline comment substantive, `changes` job parameterized by event type with three conservative fallbacks (zero-SHA, git-diff-failure, unknown-event). Implementation (a) from the sprint plan, as recommended. Smoke-gun push:main run `24684730563` on the merge commit itself is green.
- **Concerns:** none on the work product. One small operational friction worth noting (below in §7): the initial merge attempt hit `studio-audits`-style strict branch protection on `battlebrotts-v2/main`, requiring `PUT /update-branch` + a re-Verify on the new head. Not a deduction; recorded for pipeline-ergonomics learning.

### S16.3-002 — Confirm warnings-as-errors consistency ✅

- **PR:** [#154](https://github.com/brott-studio/battlebrotts-v2/pull/154) — merge SHA `6ebe4ffb`.
- **Owner:** Nutts. Reviewer: Boltz (COMMENT review — see §7). Approver of record: `brott-studio-specc[bot]` (APPROVED 2026-04-20T18:54:23Z).
- **Merged by:** `brotatotes` (PAT identity — auto-merge shadowed the Specc merge call; see §7).
- **Evidence:** `docs/kb/warnings-as-errors-policy-s16.3.md` exists (29 lines), states the aligned-by-construction finding with evidence (full `project.godot` enumeration, spot-check of a recent green code-path run for `arena_renderer.gd` regression absence). Zero `.gd` or `project.godot` edits — the one-line carve-out was not exercised because no warning re-surfaced. Honest no-op finding, properly documented.
- **Concerns:** none. The PR body is rigorous and the KB doc is publishable as-is.

### S16.3-003 — E2E validation + arc-acceptance artifact ✅

- **Owner:** Optic. No PR (verification doc per convention).
- **Evidence:** V1–V8 probes all PASS per Riv's context summary. Independently re-verified the critical probes in this audit:
  - push:main run exists and is green: `24684730563` / `d04426ea` ✅.
  - PR-trigger runs on sub-sprint heads exist and are green: `24684211274`, `24684602984`, `24684284054` ✅.
  - Scope gate clean on both merges (§5 above) ✅.
  - Inline YAML comment present with substantive rationale (§3.2) ✅.
  - Enumeration intact (24/24 sprint test files, per S16.2 audit carry-through) ✅.
- **Arc-acceptance framing:** explicit — §4 of this audit restates the three HCD criteria with per-criterion evidence pointers.
- **Concerns:** none. The V-probes are strong prior evidence; this audit's independent re-verification agrees.

---

## 7. Cross-actor identity notes — Boltz shared-PAT 422 (new data)

This is the most interesting telemetry from S16.3 and it generalizes a finding from S16.2.

**Observation.** On both PR #153 and PR #154, Boltz attempted to submit a formal `APPROVE` review using the shared PAT (`brotatotes` identity) and received HTTP 422 — the same error pattern Specc hit in S16.2-003 when attempting self-approval with the shared PAT. Boltz fell back to posting COMMENT reviews on both PRs, visible in the review list:

```
PR #153:  brotatotes — COMMENTED — 2026-04-20T18:52:34Z
          brott-studio-specc[bot] — APPROVED — 2026-04-20T18:54:23Z

PR #154:  brotatotes — COMMENTED — 2026-04-20T18:53:10Z
          brott-studio-specc[bot] — APPROVED — 2026-04-20T18:54:23Z
```

**Diagnosis (extending the S16.2 finding).** The S16.2-003 conclusion — "the 422 is GitHub's universal same-actor approval block, not PAT-specific" — holds. Boltz authors nothing on these PRs, but the shared-PAT pipeline means *every* PAT-identity review is submitted as the same GitHub actor (`brotatotes`), which is also the actor that authored the PR (Patch and Nutts both commit as `brotatotes` via the shared PAT). GitHub refuses the formal APPROVE because the reviewing-actor-id matches the authoring-actor-id, regardless of which **role** (Boltz, Patch, Nutts, Specc) is actually operating.

This is the S16.2-003 learning **generalizing beyond Specc** — it applies to every formal-review-event role the pipeline has. The per-agent GitHub App pattern documented in `docs/kb/per-agent-github-apps.md` is not Specc-specific; it is the only actual fix for this class of error across all reviewer roles.

**Current impact: benign.** `battlebrotts-v2/main` branch protection currently counts *reviews* rather than formal APPROVE events, so a Boltz COMMENT review does not block merge. The Specc App APPROVE satisfies the protection requirement on both PRs. No merges stalled on this.

**Future risk: blocker if branch protection tightens.** If protection is hardened to require a distinct APPROVE event from a reviewer role (e.g. "Boltz must formally approve before merge"), every reviewer PAT-identity action will 422 and there will be no workaround short of per-agent Apps. This is a framework-patch candidate for the S16 arc retrospective (see §9 below), not an S16.3 deduction.

**Recommendation this audit:** extend the S16.2 per-agent-App pattern to Boltz (and any future reviewer role). Concrete next step tracked in the arc retrospective.

---

## 8. Process notes

### 8.1 Specc App merge on PR #153 — branch-protection friction (worth noting)

When the Specc App went to merge PR #153, `battlebrotts-v2/main` branch protection required the PR branch to be up-to-date with `main`. The merge path needed:
1. `PUT /repos/brott-studio/battlebrotts-v2/pulls/153/update-branch` to rebase/merge `main` into the PR head.
2. A re-run of the Verify PR trigger on the new head (run `24684602984` — green).
3. Then the App-identity merge call succeeded.

This is a small operational friction — not a defect in S16.3's work, but a data point on dogfooding the Specc App against strict branch protection. It is also a soft argument for tightening the Specc App's merge script to handle the `update-branch` + re-Verify poll automatically, so the next auditor does not have to do it manually.

### 8.2 PR #154 auto-merge shadowing (benign, known pattern)

PR #154's `merged_by` is `brotatotes` rather than `brott-studio-specc[bot]`, because the repo's auto-merge workflow landed the merge before the Specc App's explicit merge call. This is the same pattern S16.2-004's KB doc already documents (auto-merge shadowing when `battlebrotts-v2` auto-merge is enabled on the PR). Benign. The Specc approval event is the semantically meaningful unblocking action; auto-merge is mechanical.

**Dual environment parity:** PR #153 shows `merged_by: brott-studio-specc[bot]` (Specc merged before auto-merge could shadow it on that PR). Both environment cases from the KB doc's decision tree are now observed on the same sprint.

### 8.3 Audit authored using Specc App (dogfood — second audit PR)

This audit is the second real-world use of the Specc App identity (the first was the S16.2 audit). Actor trail recorded in §10 for telemetry.

### 8.4 Boltz COMMENT review reinforces S16.2-003 generalization

See §7. Framework takeaway: per-agent Apps are the real fix for same-actor 422 across *all* formal-review-event roles, not just Specc. Escalated to arc retrospective (§9).

---

## 9. Carry-forward items

No new items from S16.3-001 or S16.3-002 beyond the framework-patch recommendations already flagged in prior audits plus the new Boltz 422 finding.

**Framework-patch recommendations (carried into arc-complete retrospective, not filed as S16.3 backlog):**

1. **PIPELINE.md audit-gate.** Already flagged in S16.1 audit §7 and S16.2 audit §7/§8.2. Two sprints running. Concrete patch proposal lives in the arc-complete retrospective.

2. **Per-agent Apps for all formal-review-event roles (new this sprint).** Extend the S16.2 App pattern to Boltz (priority) and any other reviewer role. Evidence: §7 above. Concrete patch proposal lives in the arc-complete retrospective.

No new GitHub Issues filed this sprint.

---

## 10. Dogfooding observations (audit-PR actor trail)

Recorded live while authoring this audit:

| Step | Identity |
|---|---|
| Clone of `studio-audits` | PAT (`brotatotes`) — read-only, correct per fallback rule |
| Commit author on audit file | `brott-studio-specc[bot]` (App identity, via `~/bin/specc-gh-token`) |
| Push to `studio-audits` | App token (installation token on `x-access-token`) |
| PR open | App identity |
| Self-approval attempt | **Skipped** — 422 is universal per S16.2-004 finding; `studio-audits` branch protection is permissive |
| Merge | App identity (no auto-merge on `studio-audits`) |

**Telemetry match:** identical to the S16.2 audit's actor trail. No regressions; the pattern is reproducible.

---

## 11. 🎭 Role Performance Review

**Gizmo:** No direct participation this sprint (pure CI/ops). Trend: →.

**Ett:** Shining: the S16.3 plan correctly overrode the arc-plan's stale `paths-ignore` wording with a fresh rationale tied to the S15/S16.1 deadlock lesson, and tightened S16.3-002 to require a PR artifact (paper trail) rather than a verbal no-op. Both decisions were executed cleanly by the build agents. Struggling: the arc-plan wording inherited in S16.3-001 was itself stale (pre-required-status-check era) — caught and corrected at sub-sprint plan authoring time, not at arc-plan review time. Acceptable; that is precisely the staged-planning model's purpose. Trend: ↑.

**Nutts:** Shining: S16.3-002 is exactly what Ett asked for — a rigorous no-op confirmation with a publishable KB artifact, full `project.godot` enumeration, and a spot-check that rules out `arena_renderer.gd` regression. Zero scope creep (no `.gd` or `project.godot` edits). Struggling: none. Trend: ↑.

**Boltz:** Shining: reviewed both S16.3 PRs on time. Struggling: hit shared-PAT 422 on formal APPROVE for both PRs, fell back to COMMENT reviews. Not Boltz's fault — systemic shared-PAT issue, and the right behavior in the meantime (fall back + proceed). Noted as a generalization of the S16.2-003 finding and a framework-patch recommendation. Trend: → (blocked on per-agent App provisioning, not on Boltz's execution).

**Optic:** Shining: V1–V8 all PASS with strong smoke-gun evidence (`24684730563`). Verification doc explicitly called the arc-acceptance moment with per-criterion pointers, as the sprint plan required. Trend: →.

**Riv:** Shining: correctly spawned Patch + Nutts in parallel, handled the auto-merge-shadowing pattern on PR #154 without re-escalating, relayed the S16.3-003 verification doc cleanly into the Specc spawn. Struggling: none visible this sprint. Trend: →.

**Patch:** Shining: S16.3-001 implementation is clean, chose implementation (a) per plan, added three conservative fallbacks, and wrote a substantive inline YAML comment. Struggling: none. Trend: ↑.

**Specc (self):** Shining: independently re-verified scope gate, push:main run, PR-trigger greens, and inline YAML comment rather than rubber-stamping V-probes. Caught and documented the Boltz-422 generalization as a separate finding from the per-task review. Struggling: the standing PIPELINE.md audit-gate recommendation is being restated a third sprint running — I am pushing it into the arc-complete retrospective as a concrete framework-patch proposal this time rather than merely noting it. Trend: →.

---

## 12. Grade: A

**Justification.** All three tasks landed. Exit criteria hold cleanly with independent verification. Scope gate held (programmatically confirmed). The smoke-gun push:main run on the S16.3-001 merge commit itself is green, which is the strongest possible evidence that the trigger works. S16.3-002's aligned-by-construction finding is the right verdict and the KB doc is publishable as-is. Optic's V1–V8 probes align with independent verification. The arc-acceptance moment is formally recorded.

The Boltz shared-PAT 422 finding is new data, not a deduction — it is a generalization of the S16.2-003 finding that was already known to be a framework-level gap. S16.3 surfaced it promptly and it is correctly escalated to the arc retrospective as a framework-patch candidate.

Not A+: two small operational frictions worth noting honestly — (1) the Specc App merge on PR #153 required manual `update-branch` + re-Verify poll under strict branch protection, and (2) the auto-merge shadowing pattern on PR #154 continues to muddy the audit trail on `merged_by`. Neither is a defect in S16.3; both are dogfooding frictions. Neither rises to the level of grade deduction.

---

## 13. Verdict

**S16.3 exit criteria HOLD. S16 arc closes with this sub-sprint.**
