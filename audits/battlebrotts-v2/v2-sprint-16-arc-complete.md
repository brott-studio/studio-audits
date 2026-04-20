# Sprint 16 (Arc) — Tech Debt Cleanup + Infrastructure Health — Arc Retrospective

**Auditor:** Specc (`brott-studio-specc[bot]`, App ID `3444613`)
**Date:** 2026-04-20T19:10Z
**Arc:** S16 (tech debt + CI/infra + per-agent identity)
**Sub-sprints:** S16.1, S16.2, S16.3
**Sub-sprint audits:** `v2-sprint-16.1.md` (A−), `v2-sprint-16.2.md` (A), `v2-sprint-16.3.md` (A)
**Arc grade:** **A**

---

## 1. Arc summary

S16 set out to close three intertwined pieces of accumulated tech debt: (1) the Godot Unit Tests suite had drifted into a state where failing-silently glob-`|| exit 1` patterns hid real regressions, (2) reviewer self-approval across the pipeline depended on a fragile shared-PAT 422 workaround misdiagnosed as PAT-specific, and (3) main-branch CI health was invisible between PRs. All three pieces landed. The arc delivered a clean, enumerated test suite; a production per-agent GitHub App for Specc with a reproducible cross-actor review flow and a publishable KB pattern for all future reviewer-role Apps; and a `push: main` Verify trigger that makes main-branch health visible in real time. All three HCD arc-acceptance criteria are MET. The arc also produced two healthy autonomous-correction data points (spec-wording errors caught and fixed by the pipeline without HCD escalation), reinforcing the 2026-04-20 autonomy directive in practice.

---

## 2. Formal arc-acceptance (per Optic S16.3-003)

Per Optic's S16.3-003 verification doc and restated in the S16.3 sub-sprint audit §4, the three HCD acceptance criteria for the S16 arc are formally MET with evidence:

### Criterion 1: `Godot Unit Tests` passes cleanly on `main` (`push: main`) AND on a dummy code-path PR — both ✅.

- **push:main:** run [`24684730563`](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24684730563) on merge SHA `d04426ea` (S16.3-001 merge commit itself) — **success**.
- **dummy code-path PR:** runs `24684211274` and `24684602984` (PR #153 head, `sprint-16.3-001-push-main-trigger`), run `24684284054` (PR #154 head, `sprint-16.3-002-warnings-consistency`) — all **success**.

### Criterion 2: `test_runner.gd` enumerates all sprint test files explicitly — no reliance on shell glob `|| exit 1`.

- Satisfied by S16.1-005 (merge SHA `36e64f8`) introducing the enumerated `SPRINT_TEST_FILES` constant with non-short-circuit per-file exit-code aggregation.
- Extended by S16.2-005 (merge SHA `ce1adab`) to include sprints 3/4/5/6 (24 total entries today).
- Enumeration re-verified at 24/24 in both the S16.2 audit §3.5 and the Optic V1–V8 enumeration probe.

### Criterion 3: At least one agent (Specc) has a per-agent GitHub App or equivalent distinct identity wired into the review/merge path.

- Satisfied by S16.2 — App ID `3444613`, installation `125608421`, private key at `~/.config/gh/brott-studio-specc-app.pem` (0600).
- Cross-actor review flow proven at PR #149 (`Nutts-authors → Specc-approves`, HTTP 200).
- Reference trail: `docs/kb/per-agent-github-apps.md` + `v2-sprint-16.2.md` (Grade A).
- Dogfooded live on both S16.2 and S16.3 audit PRs (second and third real-world uses of the App identity).

**All three criteria MET. S16 arc formally complete.**

---

## 3. Per-sub-sprint summary

### S16.1 — Test suite cleanup + quarantines (audited retroactively)

Fixed or quarantined every failing test in the Godot Unit Tests suite. Replaced the shell-glob `|| exit 1` pattern in `test_runner.gd` with explicit enumeration + per-file exit-code aggregation. Resurfaced the `arena_renderer.gd` warning-as-errors fix. Three combat-side regressions correctly quarantined (not papered over) with `TestUtil.skip_with_reason` pointers and carry-forward issues filed. Audit authored retroactively at arc-resumption; this is itself one of the arc's lessons (see §4 and §5.1).

**Audit:** `v2-sprint-16.1.md` — Grade **A−**. The only deduction was the ship-without-audit process miss, which the S16.1 audit itself surfaced as a framework-patch recommendation (see §5.1).

### S16.2 — Per-agent App identity + test-hygiene carry-forwards

HCD-created GitHub App for Specc; profile + SECRETS.md wired to `~/bin/specc-gh-token`; cross-actor identity validation proven (`Nutts-authors → Specc-approves` via PR #149, HTTP 200); comprehensive KB doc (`docs/kb/per-agent-github-apps.md`) covering setup, rotation, failure modes, and the universal-self-approval-block finding. Three S16.1 carry-forward issues closed in parallel (#138 sprints 3/4/5/6 triage, #140 `SceneTree.quit()` doc, #141 quarantine registry + drift-lint at 49 lines). Cross-actor flow also produced a corrective finding: the S15 PAT-422 issue was misdiagnosed as PAT-specific; it is actually GitHub's universal same-actor approval block.

**Audit:** `v2-sprint-16.2.md` — Grade **A**. Core deliverable works end-to-end and is dogfooded live. Notable autonomous correction of an inherited spec-wording error (see §4).

### S16.3 — Main-branch CI observability + warnings-policy paper trail

`push: main` trigger added to `verify.yml` (PR #153, `d04426ea`) with event-type-parameterized `changes` job diff range and three conservative fallbacks; substantive inline YAML comment documents the no-`paths-ignore` decision. Warnings-as-errors KB artifact (PR #154, `6ebe4ffb`) documents the aligned-by-construction finding — `project.godot` declares no warnings policy, so both local and CI resolve to identical Godot 4.4.1 engine defaults. Optic S16.3-003 V1–V8 all PASS with smoke-gun push:main run `24684730563` green on the merge commit itself.

**Audit:** `v2-sprint-16.3.md` — Grade **A**. All exit criteria hold, scope gate clean, arc-acceptance moment formally recorded.

---

## 4. Lessons learned

The three lessons below are the ones worth carrying forward. Each is evidenced by a specific sprint event and has a concrete framework-level implication.

### 4.1 S16.2-003 spec-wording error — self-approval is a GitHub platform block, not a PAT-specific bug

**What happened.** The S16.2-003 task spec asked Specc to self-approve its own PR to validate the App identity. GitHub returned HTTP 422 — but not because of the App identity wiring. The 422 is a platform-level block: GitHub refuses APPROVE when the reviewing actor matches the authoring actor, regardless of identity type (PAT, GitHub App, or human user). The S15 "PAT 422" diagnosis was actually the universal same-actor block, masked by the shared-PAT pipeline where the same actor always appeared on both ends.

**How it was resolved.** Patch identified the error during execution, proposed two options (close-and-document vs. redo-with-correct-acceptance), and executed Option 2 (cross-actor redo via PR #149) *without escalating to HCD*. Riv relayed the redo decision cleanly. The correct acceptance — `Nutts-authors → Specc-approves` — proved the real pipeline requirement and closed the S16.2-003 task with honest evidence. Finding is documented prominently in `docs/kb/per-agent-github-apps.md`.

**Why it matters.** This is a healthy autonomous-correction data point. The decision was reversible, aligned with the clear underlying goal (validate the identity wiring) rather than the verbatim spec text, and filled a gap Riv missed rather than one Riv explicitly deferred. The pipeline self-corrected a Riv/Ett spec-wording error end-to-end without HCD involvement, which is precisely what the FRAMEWORK autonomy directive asks for. Framework-level takeaway (already internalized): spec acceptance in terms of *outcomes that prove the mechanism works* (cross-actor review is the pipeline requirement) rather than *specific mechanical actions* (self-approve).

### 4.2 S16.3-001 `paths-ignore` vs runtime-short-circuit — arc plans go stale between planning and execution

**What happened.** The S16 arc plan §S16.3-001 prescribed `paths-ignore: [docs/**, sprints/**, '**/*.md']` on the new push trigger. By the time S16.3 executed, the current `verify.yml` had *deliberately removed* `paths-ignore` from the PR trigger (S15/S16.1 era) to avoid a required-status-checks deadlock on doc-only auto-merge PRs — the fix was to filter at runtime via the `changes` job instead. The arc-plan wording predated that lesson.

**How it was resolved.** Gizmo flagged the stale wording at S16.3 sub-sprint plan authoring time. Ett overrode the arc-plan wording in the sub-sprint plan, mirroring the PR trigger's no-`paths-ignore` pattern for symmetry (single source of truth on "what counts as doc-only"). Patch implemented it with a substantive inline YAML comment so the next agent reading the file does not re-propose `paths-ignore`. Riv resolved the decision autonomously. Documented in `verify.yml` inline.

**Why it matters.** Arc plans authored at arc start will often go stale by the time late-arc sub-sprints execute, because earlier sub-sprints surface lessons that invalidate specific prescriptions. The staged-planning model (arc plan → per-iteration sub-sprint plans emitted by Ett after each prior audit lands) is precisely the right defense for this — sub-sprint plans are where arc-plan wording should be re-validated and overridden when it has gone stale. This sprint demonstrates the model working as designed, and it is worth recording as an explicit expectation rather than an exception. Second healthy autonomous-correction data point this arc.

### 4.3 Per-agent App finding generalizes to all formal-review-event roles — not just Specc

**What happened.** On both S16.3 PRs (#153 and #154), Boltz attempted formal APPROVE reviews using the shared PAT and received HTTP 422 — the exact same pattern Specc hit in S16.2-003. Boltz fell back to COMMENT reviews on both PRs; Specc App APPROVE satisfied branch protection and merges proceeded.

**Why it matters.** This confirms that the S16.2-003 universal-same-actor-block finding is not Specc-specific. In the shared-PAT pipeline, *every* PAT-identity review is submitted as the same GitHub actor (`brotatotes`), which is typically also the author actor. GitHub will 422 every formal APPROVE from every reviewer role while shared-PAT is in use. The per-agent-App pattern documented in `docs/kb/per-agent-github-apps.md` is not a Specc feature — it is the only actual fix for this class of error across all reviewer roles.

**Current impact: benign.** `battlebrotts-v2/main` branch protection counts *reviews* (including COMMENT reviews), not formal APPROVE events, so the Boltz COMMENT + Specc APPROVE combination unblocks merge. No merges stalled.

**Future risk: blocker if protection tightens.** Any move to require a distinct formal APPROVE from a specific reviewer role (e.g. "Boltz must formally approve before merge") will hit 422 on every PAT-identity attempt with no workaround short of per-agent Apps. This is a framework-patch candidate (see §5.2) — not urgent today, blocker tomorrow.

---

## 5. Framework-patch recommendations (carry into a separate framework PR next arc)

These are the arc-complete retrospective's concrete asks. Surface to HCD via Riv → The Bott.

### 5.1 PIPELINE.md audit-gate invariant

**Problem.** The S16.1 audit (§7) and the S16.2 audit (§7 / §8.2) flagged the same framework-level gap: nothing in the pipeline today structurally prevents a sub-sprint from being declared closed without its Specc audit landed on `studio-audits/main`. S16.1 itself shipped without an audit at the time (the retroactive audit was only written at arc resumption). S16.1 and S16.2 both flagged the gap; the S16.3 audit would have been the third sprint running if S16.3 itself had not landed its audit on arc-close. Three sprints of evidence is enough.

**Concrete patch proposal:**
1. Add a required checklist item to `studio-framework/PIPELINE.md`'s "sub-sprint close-out" section: **"Audit landed on `studio-audits/main` at `audits/<project>/v2-sprint-<N.M>.md`."** The item must be checked before the sub-sprint is declared closed.
2. Optional (stronger): add a GitHub Action on the `battlebrotts-v2` repo that fails if a `sprints/sprint-<N.M>.md` merges to `main` (close-out PR) without a corresponding audit file existing on `studio-audits/main`. Mechanical enforcement of the checklist item.

**Expected effort:** (1) is a 5–10 line patch to PIPELINE.md; (2) is a small custom workflow (~50 lines) using `gh api` to check the sister repo. (1) alone is valuable; (2) is belt-and-suspenders.

**Priority: high.** Three sprints running with the same flag is a pattern.

### 5.2 Per-agent GitHub Apps for all formal-review-event roles

**Problem.** The S16.3 Boltz-422 finding (§4.3 above) proves the S16.2-003 universal-same-actor-block generalization. All formal-review-event roles — Boltz in particular, and any future reviewer role — will continue to hit 422 on formal APPROVE until they have a distinct GitHub App identity. Benign under current branch protection; blocker if protection tightens to require specific role-based formal APPROVEs.

**Concrete patch proposal:**
1. Extend the S16.2 App pattern (documented in `docs/kb/per-agent-github-apps.md` §"template for future Apps") to Boltz. Reuse the playbook: create org App → install on both repos → generate private key → wire into `studio-framework/agents/boltz.md` + `SECRETS.md` → deploy `~/bin/boltz-gh-token` helper.
2. Operational cost: HCD-executed org-admin step (App creation + install) identical to S16.2-001; the rest is build-agent work.
3. Benefits: eliminate COMMENT-review workaround, enable formal APPROVE events for future branch-protection hardening, improve audit-trail legibility (distinct bot identity per role).
4. Sequence: start with Boltz (most frequently-reviewing role); defer Nutts/Patch/Optic/Riv unless specific future need emerges.

**Expected effort:** one sprint sub-sprint sized (≈S16.2 scale minus the KB doc authoring, since the pattern is already documented).

**Priority: medium.** Benign today, but cheap to fix preemptively before any branch-protection tightening forces an urgent fix.

### 5.3 Arc-plan staleness: no patch needed

The §4.2 lesson (arc plans go stale between planning and execution) is already handled by the staged-planning model (Ett emits per-iteration sub-sprint plans that re-validate arc-plan prescriptions). No framework patch needed. Recording the pattern explicitly here so it is understood as an expectation rather than an exception.

---

## 6. Operational frictions recorded

These are not lessons per se, but small dogfooding observations worth keeping so the next arc's retrospective can spot regressions or improvements.

- **S16.3-001 strict-branch-protection rebase friction.** Specc App merge on PR #153 required manual `PUT /update-branch` + re-Verify poll on the new head before the merge call succeeded. Small operational friction; argues for the Specc App merge helper to handle `update-branch` + re-Verify polling automatically. Not urgent.
- **Auto-merge shadowing pattern.** PR #154 `merged_by: brotatotes` because the repo auto-merge workflow beat the Specc App's explicit merge call. Known pattern, documented in `docs/kb/per-agent-github-apps.md`. The Specc approval event is the semantically meaningful unblocking action; auto-merge is mechanical. Dual environment case observed this arc — PR #153 shows Specc as `merged_by`, PR #154 shows `brotatotes` — both cases from the KB decision tree now exercised live.
- **Boltz 422 × 2.** New data point (§4.3). Recorded.

---

## 7. Autonomy directive (2026-04-20) — how it played out

HCD published the autonomy directive on 2026-04-20 (same day as most of this arc): "if a workflow/arc is moving in the right overall creative/technical direction with the correct priorities, run it autonomously." S16 was the first arc to execute end-to-end under that directive, and it executed cleanly:

- HCD set the arc acceptance criteria once (three criteria, in the arc plan).
- Two mid-arc Riv/Ett spec-wording errors were caught and self-corrected by the pipeline without HCD escalation (§4.1 and §4.2). Both decisions were reversible and aligned with the clear underlying goal.
- Ett emitted three sub-sprint plans; Riv spawned build agents; audits landed per sub-sprint.
- The only HCD-bound action was S16.2-001 (org-admin App creation), which is structurally HCD-only.
- No approval-bouncing for mid-flow decisions. No status-check noise.

This is a positive data point for the directive. The pipeline can absorb spec-wording corrections at the sub-sprint-execution layer, and arc plans can be overridden at sub-sprint-plan-authoring time, all without HCD involvement.

---

## 8. Arc-level grade: A

**Justification.**

- All three HCD arc-acceptance criteria MET, with strong evidence: push:main smoke-gun run green on the S16.3-001 merge commit itself; `test_runner.gd` enumerates 24/24 sprint test files with per-file exit-code aggregation; Specc App identity proven end-to-end on cross-actor review flow at PR #149 and dogfooded live on two audit PRs.
- Per-sub-sprint grades: A− / A / A. The only A− (S16.1) was the ship-without-audit process miss, which the pipeline is now driving to close framework-level (§5.1). The two A sub-sprints held their scope gates cleanly and delivered their headline mechanisms.
- Scope gate held cleanly across the entire arc (S15.2 → S16.1 → S16.2 → S16.3 is now four consecutive sub-sprints with non-trivial gates held clean — the pattern is reliable).
- Two healthy autonomous-correction data points (§4.1, §4.2) — the pipeline self-corrected two Riv/Ett spec-wording errors without HCD escalation, which is precisely the autonomy directive's intent.
- Two framework-patch recommendations with concrete proposals (§5.1, §5.2), both derived from multi-sprint evidence rather than single-sprint hunches.

**Not A+:**

- The S16.1 ship-without-audit gap is the third sprint running (S16.1 itself, then flagged in S16.2, then flagged in S16.3) — evidence that the framework-patch recommendation has been noted-not-acted for multiple sprints. Filing it as a concrete proposal this arc (§5.1) is the right escalation, but the standing drift in the feedback loop itself is worth naming.
- The shared-PAT 422 finding had to be rediscovered by Patch in S16.2-003 because it was originally misdiagnosed as PAT-specific in S15. Misdiagnosis-carried-forward is the kind of thing a more rigorous arc-start review might have surfaced sooner.
- Two operational frictions on S16.3 (strict-branch-protection rebase, auto-merge shadowing) continue to muddy the dogfooding signal on the Specc App identity. Both are documented; neither is urgent.

None of these rise to the level of demoting the grade. All three criteria MET; the work products are production-quality; the lessons are captured concretely; the autonomy directive proved itself in practice. This is a clean A.

---

## 9. Verdict

**S16 arc complete. All three HCD arc-acceptance criteria MET. Ready to begin S17 arc planning.**
