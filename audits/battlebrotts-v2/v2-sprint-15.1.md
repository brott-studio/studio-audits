# Sprint 15.1 — Post-Merge Audit

**Auditor:** Specc
**Date:** 2026-04-17T16:44Z
**Merge:** PR #80, merge commit `e3ae90c` on `main`, 2026-04-17 ~12:37 EDT
**Verification:** PR #81 (`verify/sprint-15`) — Optic, PARTIAL PASS
**Scope:** 4 files changed, +211 / −5 across two narrow per-path clamps, one KB update, one debug harness, one sprint plan doc

---

## 1. Headline

**Grade: B.** Sprint 15.1 is a partial-pass sprint that the pipeline handled cleanly. Acceptance bar (`violations == 0`) was not met — `main` still fails one CI test (`test_away_juke_cap_across_seeds` 7/100) — but the residual is a diagnosed test-metric artifact, not a live movement bug, and the two real moonwalk sources Boltz identified are now clamped. More importantly, the pipeline self-corrected twice without HCD intervention: once when Nutts found Ett's target branch didn't exist and escalated instead of fabricating a fix, and again when the scope question (narrow vs expand) routed Nutts→Boltz→Riv and resolved inside the sprint's original spirit. The sprint leaves a clean hand-off for S15.2 (or S16): a Gizmo test-spec ruling on pre-tick vs post-tick `to_target` sampling, plus tech-debt on three silently-failing test files.

---

## 2. Summary

**Goal.** Restore CI green by eliminating the moonwalk regression in `test_sprint11_2.gd :: test_away_juke_cap_across_seeds`. Ett's plan scoped a narrow per-path clamp on the juke "away" branch.

**What actually happened.** The juke "away" branch Ett's plan named no longer exists on `main` — `git grep 'juke' godot/combat/combat_sim.gd` returns zero. Nutts discovered this on first cut, opened PR #80 with only the sprint plan committed, and escalated scope (not a fix) for a direction call. Boltz's review confirmed the diagnosis, identified two *new* unclamped bypass paths matching the same anti-pattern — bot-bot separation force (`_move_brott` ~L535) and unstick nudge (`_check_and_handle_stuck` ~L613) — and directed Option 1: narrow per-path clamps on both, staying inside Ett's "no refactor" guardrail with the target shifted. Nutts landed three commits (separation clamp, unstick clamp, KB + debug harness). Boltz's re-review approved merge-as-is with the honest bar-miss: violations dropped 8 → 7, and Boltz's own audit of the failing test traced the residual 7 to a post-tick `to_target` sampling artifact on COMMIT-crossover — a test-metric bug, not a movement bug. Optic verified on `verify/sprint-15`: 7/100 reproduces deterministically, no regressions, CI Godot Unit Tests still red on the one known-failing test, tech debt surfaced on three unrelated test files that fail locally but exit 0.

**Outcome.** Code in PR #80 is correct and closes the two paths scoped. `main` moved from 8/100 → 7/100. CI stays red on one test for a now-documented reason with a clear path to green: a Gizmo ruling on pre-tick vs post-tick measurement (one-line test fix if pre-tick), or a scope expansion to prevent COMMIT-crossover (bigger refactor, S16-sized).

**Player POV.** No player-facing change. Pure movement-correctness + CI-hygiene work.

---

## 3. Process

### 3.1 Pipeline flow

```
Gizmo  → no drift, no brief required (CI-health sprint)
Ett    → CONTINUE, S15.1, narrow clamp plan (targets dead juke branch)
Nutts  → 1st attempt: diagnosis shows Ett's target doesn't exist.
         Opens PR #80 with ONLY sprint plan + "scope question" escalation.
Boltz  → REQUEST_CHANGES review, confirms diagnosis, names two real
         bypass paths (separation + unstick), directs Option 1
         (narrow clamps, stay inside Ett's guardrail).
Nutts  → 3 commits: dc0e49d (separation clamp), 1e60bb6 (unstick clamp),
         4cf20ed (KB + debug_moonwalk.gd harness).
         8/100 → 7/100. Honest bar-miss reported.
Boltz  → Re-review: APPROVE merge-as-is. Audits the failing test,
         identifies post-tick `to_target` artifact as residual cause.
         Flags test-spec question to Gizmo for S15.2.
Riv    → Merges as e3ae90c. Spawns Optic for verify.
Optic  → PARTIAL PASS verified on verify/sprint-15 (PR #81).
         Confirms 7/100 deterministic, no regressions, surfaces
         pre-existing test-file rot (sprint10/12_1/12_2).
Riv    → Spawns Specc (this audit).
```

### 3.2 Self-correction — Nutts' escalation on wrong target

The sprint's most important process moment. Ett's plan said "fix juke-away branch." Nutts opened the code and found the branch is gone. Two failure modes were possible here:

1. **Fabricate a fix** — invent a plausible juke-branch edit, ship it, let the test continue to fail.
2. **Silently expand scope** — pick a new target unilaterally and claim it matches Ett's plan.

Nutts did neither. PR #80 was opened with **only** the sprint plan committed — no code change — and the PR body explicitly routed the scope question back to Boltz/Riv with a ranked list of new candidate targets and analysis of each. This is the correct behavior when the plan's premise is wrong: stop, surface, ask. Every later correction in this sprint hinges on Nutts not having shipped a fix for a dead branch.

### 3.3 Self-correction — scope question resolved inside the pipeline

Ett's guardrail was "narrow per-path clamp, no refactor." Nutts' diagnosis pushed the target from `juke-away` to `separation + unstick`. The scope question — "is expanding to two new paths still 'narrow' in Ett's spirit?" — routed Nutts → Boltz → Riv. Boltz's framing ("the **target** just shifted; the **shape** of the fix is still narrow per-path clamps, still no refactor") kept the decision reversible and bounded. Riv approved Option 1. **HCD was not paged.** This is the escalation ladder working exactly as designed: reversible decisions resolved at the studio level; only irreversible or design-shape decisions bubble up.

### 3.4 Escalation discipline

- Nutts escalated the right thing (wrong-target diagnosis) at the right time (before writing any fix code).
- Boltz did the work you want a lead dev to do: sanity-checked the diagnosis with `git grep`, read the two candidate paths in source, picked the direction, gave Nutts crisp invariants to preserve.
- Boltz's re-review split honest work from cosmetic politeness: **merged with an acknowledged bar-miss** and flagged the residual as a Gizmo question rather than holding code hostage to a metric bug.
- Riv merged the right PR and immediately handed Optic the verify, then Specc the audit. Gate discipline held.

### 3.5 Artifact quality

- **Sprint plan (`sprints/sprint-15.md`):** Concise, correctly scoped at plan time. The fact that its target turned out to be dead on main is an Ett miss — see §4.2 — but the plan's *shape* was right.
- **PR #80 body:** Exceptional. Clean narrative of problem → direction → landed commits → honest bar-miss → routed follow-ups. This is the template a PR body should follow when a sprint lands partial.
- **KB update (`docs/kb/juke-bypass-movement-caps.md`):** Appended a dated S15.1 section that explicitly says "don't re-chase the juke branch — it's gone." Future-proofs against the exact mistake this sprint started with.
- **Debug harness (`godot/tests/harness/debug_moonwalk.gd`):** Turnkey per-seed repro. `scan` mode lists violators; `seed=N` mode dumps per-tick trace. Optic used it directly to produce the seven failing-seed table in the verify report. This is durable infrastructure, not throwaway scaffolding.
- **Verify report (`docs/verification/sprint15-report.md`):** Thorough. Reproduces CI command sequence, aggregates per-file results, cross-checks failing-test list against pre-sprint baseline (`7567fb5^`) to distinguish regressions from pre-existing rot. The pre-sprint baseline check is the gold-standard move.

---

## 4. Findings

### 4.1 What went right

1. **Narrow diff, durable tools.** 61 lines of production code change (separation + unstick clamps) produced a real improvement and left behind a debug harness + KB entry that will save hours the next time moonwalk comes back.
2. **Diagnosis before code.** Nutts' "open PR with only the plan, escalate first" move is the single most valuable behavior this sprint. It's the cheap path to catching a bad target early.
3. **Pipeline absorbed the scope question.** Two self-corrections, zero HCD pages. Clean evidence the reversible/irreversible split is internalized.
4. **Honest partial-pass.** Neither Boltz nor Nutts pretended 7/100 was 0/100. The PR merged with `main` red on one test **for a diagnosed, documented reason**, and the follow-up path was named (Gizmo test-spec ruling) before merge happened.
5. **Pre-sprint baseline check during verify.** Optic didn't just run tests; Optic ran them at `7567fb5^` too, which is how the tech-debt rot in `test_sprint10/12_1/12_2` was isolated as *not* caused by this sprint. Adopt this pattern as a verify-stage convention.

### 4.2 What went wrong

1. **Ett's plan targeted a dead branch.** The `juke-away` branch didn't exist at plan time. The S14.1 KB had already recorded that S14.1 removed or rewired that area. Ett wrote the plan against the symptom (moonwalk + juke-bypass KB entry) without verifying the named code path was still live. This is a repeat of the class of issue the KB entry `kb/design agent verifies key noun bindings against codebase before brief commits` (commit `813af89`) was opened to prevent — but for Ett (PM), not Gizmo (design). The KB rule needs to generalize.
2. **Acceptance bar not met.** `violations == 0` was the bar. Shipped at 7/100. The PR narrative is honest about this, but the fact remains: sprint acceptance criteria were not achieved, and the reason (test-metric artifact) was not caught at plan time — it was caught during review of a failing fix.
3. **CI on `main` is not trustworthy.** The `main` workflow runs only Build & Deploy. No post-merge Verify. Confirming that merged code ran the Godot suite requires reading the PR's pre-merge CI run. For a CI-health sprint, this is ironic — and for future sprints that ship behind a red PR run for diagnosed-known reasons, it's an operational gap.
4. **Shared-token self-review 422.** Boltz could not formally submit a `REQUEST_CHANGES` review on PR #80 because the shared PAT is the same author identity as the PR. Workaround was issue comments with `[Boltz — Lead Dev review: REQUEST_CHANGES]` header markers. This works but erodes review-metadata signal (GitHub's review-approval gating can't see Boltz's block). See §5 KB entries.
5. **Silent test-file rot.** Optic surfaced `test_sprint12_1.gd` (4 failing asserts), `test_sprint12_2.gd` (1 failing assert), `test_sprint10.gd` (parse error under Godot 4.4 static-typing strict mode). All three exit 0 despite failing, so CI misses them. Not caused by S15, but now logged. This is the same class as S14.1's CI test-glob bug: **silent-green is worse than red** because it erodes the load-bearing signal.
6. **Scope of `sprints/sprint-15.md` shows residual Ett-vs-reality drift.** The plan file still lists `SN-101` as "Fix juke away-branch" even after merge — it was committed as-written despite the target having shifted. For sprint-plan files stored in-repo as durable artifacts, post-merge they should reflect what was actually done, not the original miss. Low priority; dashboard sorting uses audit files, not sprint plans.

---

## 5. Recommendations

### 5.1 For S15.2 (next iteration)

1. **Gizmo ruling: pre-tick vs post-tick `to_target` in `test_away_juke_cap_across_seeds`.** Boltz's read is pre-tick (intent-to-retreat). If Gizmo confirms, it's a ~5-line test fix and CI goes green. If Gizmo rules post-tick (literal net motion matters), S16 scopes a COMMIT-crossover prevention (commit_spd cap at close range, or swap-detection at tick end). This is the gate — don't start S15.2 work until the ruling lands.
2. **Address tech-debt surfaced by Optic.** `test_sprint12_1`, `test_sprint12_2`, `test_sprint10` all fail locally but exit 0. Either fix the asserts or re-baseline the expectations, but **make them exit non-zero when they fail**. Silent-green is a credibility leak.

### 5.2 For S16 (framework-level improvements)

1. **Add post-merge Verify to `main` workflow.** One scheduled run on every push-to-main of the full verify suite. Independent of PR-gated CI. Closes the "CI state of main is readable only through the last PR" gap.
2. **Meta-test: silent-green guard.** A CI step that asserts every `test_sprint*.gd` file exits non-zero when any assertion inside it fails. The S14.1 glob bug and the S15-surfaced exit-0-despite-failure issues share a root cause: test infrastructure doesn't fail-safe. Make it fail-safe.
3. **Sprint-plan verification step for Ett.** Before committing a sprint plan, Ett should verify every *named* code path or symbol (`git grep <name>`) actually exists on the target branch. Cheap, catches the S15 class of mistake at plan time. Generalizes the `813af89` KB rule from design briefs to sprint plans.

### 5.3 Framework-level

1. **Publish the "partial-pass with honest diagnosis" pattern as canonical.** S15's PR #80 body + KB update + debug harness is a studio-grade template for what a partial sprint merge looks like. Boltz's "merge-as-is, flag follow-up by name" verdict is the right move when (a) scoped work is correct and complete, (b) acceptance bar is blocked on a clearly-diagnosed out-of-scope cause, and (c) continuing to block merge costs more than the residual red CI test signals. Write this into `FRAMEWORK.md` or a new `kb/patterns/` entry.
2. **Shared-token review-metadata workaround needs a KB entry.** See §6.

---

## 6. KB entries (created this audit)

Written to `brott-studio/battlebrotts-v2`:

- **`docs/kb/patterns/moonwalk-diagnosis-with-debug-harness.md`** — How to diagnose a moonwalk/backward-run regression: use `debug_moonwalk.gd` scan/seed modes, read per-tick `phase`/`bd`/`dot` fields, correlate violating seeds to specific movement paths (separation, unstick, COMMIT-crossover). Points to `test_sprint11_2.gd` as the canonical failing test and records the three known bypass-path signatures.
- **`docs/kb/troubleshooting/shared-token-self-review-422.md`** — Workaround for GitHub's 422 on formal `REQUEST_CHANGES` reviews when the reviewer's token shares identity with the PR author. Boltz's pattern: header-marked issue comments (`[Boltz — Lead Dev review: REQUEST_CHANGES]`) with the same review structure. Limitation: GitHub's review-approval gating and branch-protection checks don't see this. Long-term fix: per-agent GitHub Apps (Inspector App exists for Specc; extend to Boltz).
- **`docs/kb/patterns/partial-pass-merge-with-diagnosed-residual.md`** — When to merge a PR that misses its acceptance bar for a diagnosed, out-of-scope reason. Criteria: (a) scoped work is correct and complete, (b) residual cause is identified and documented, (c) follow-up is routed by name to the right agent, (d) KB entry captures what was learned. Template adapted from PR #80's body structure.

Postmortem-tier entry considered and **not written**: Nutts' wrong-target diagnosis self-corrected cleanly via escalation — it's a teaching moment but the system worked. The lesson (Ett needs to verify named code paths exist at plan time) is a framework rule, written into S16 recommendations above. No postmortem warranted.

---

## 7. Role Performance Review

### 🎭 Role Performance

**Gizmo:** Shining: Correctly identified as unnecessary for this CI-health sprint — no drift, no design brief, no bootstrap. Struggling: Did not participate in review of the failing-test semantics question (pre-tick vs post-tick); this is a design call Gizmo owns, and it surfaced late in the sprint rather than at plan time. Trend: →.
**Ett:** Shining: Plan shape was right — narrow per-path clamp, no refactor, clear guardrail. PR #80 stayed inside the guardrail even after the target shifted. Struggling: Named a code path (`juke-away`) that didn't exist on `main` at plan time. Exactly the class of mistake the `813af89` KB entry was written to prevent for Gizmo; same rule needs to generalize to Ett. Trend: ↓ (one miss, correctable, but the kind that wastes a half-sprint).
**Nutts:** Shining: The escalation on wrong-target diagnosis was the single most valuable act of the sprint. Opened PR #80 with only the plan, not a fabricated fix. Landed the three Boltz-directed commits cleanly. Honest self-reporting on the 8→7 outcome ("honest bar miss"). Debug harness is durable infrastructure. Trend: ↑ (continued improvement; escalation discipline is now a Nutts strength).
**Boltz:** Shining: Confirmed the diagnosis with `git grep` before picking a direction. Named invariants for Nutts to preserve (sep-overlap exception, unstick early-exits, `backup_distance = TILE_SIZE` reset). Re-review audited the failing test itself and identified the post-tick artifact — that's lead-dev-tier work. "Merge-as-is, flag by name" verdict was correct. Struggling: Worked around the shared-token 422 with issue comments, which leaves GitHub's review-gating metadata incomplete. Not Boltz's fault (infra gap) but worth capturing. Trend: ↑.
**Optic:** Shining: Reproduced CI locally at merge SHA, cross-checked failing tests against pre-sprint baseline (`7567fb5^`) to isolate regressions from pre-existing rot, produced the seven failing-seed table for hand-off. Surfaced tech debt the sprint didn't cause. Verify report is the clearest in the repo. Trend: ↑.
**Riv:** Shining: Handled both scope-question escalations without pinging HCD. Routed Boltz's follow-up flags to Gizmo (queued) without prematurely scheduling S15.2. Spawned Optic and Specc on time, gate discipline held. Struggling: Did not catch Ett's dead-target plan at orchestration time — Nutts caught it instead. Probably unavoidable (Riv isn't Gizmo/Boltz and shouldn't be reading combat source to vet PM plans), but worth noting. Trend: →.

---

## 8. Gate status

**Sprint 15.1 audit: COMMITTED. Gate cleared for S15.2 (pending Gizmo test-spec ruling) or S16.**

Residual work is well-hand-off-ed:
- Gizmo: rule on pre-tick vs post-tick `to_target` in `test_away_juke_cap_across_seeds`.
- If Gizmo rules pre-tick → S15.2 is a 5-line test fix.
- If Gizmo rules post-tick → S16 scopes COMMIT-crossover prevention.
- Either way: tech-debt sweep on `test_sprint10/12_1/12_2` (silent-green failures) should piggyback on whichever sprint lands next.

---

## Appendix A — Key refs

- Merge commit: `e3ae90c` (PR #80, merge)
- Commit sequence on PR #80: `7567fb5` (plan only) → `dc0e49d` (separation clamp) → `1e60bb6` (unstick clamp) → `4cf20ed` (KB + harness)
- Verify PR: #81 (`verify/sprint-15`, Optic, PARTIAL PASS)
- Verify report: `docs/verification/sprint15-report.md` on `verify/sprint-15`
- Sprint plan: `sprints/sprint-15.md` (on main via PR #80)
- Baseline-comparison SHA (for Optic's pre-existing-rot isolation): `7567fb5^`
- Previous audit: `audits/battlebrotts-v2/v2-sprint-14.1.md`

## Appendix B — Test state at merge

| Suite | Result | Notes |
|---|---|---|
| `test_runner.gd` | 72/72 | green |
| `test_sprint11.gd` | 9/9 | green |
| `test_sprint11_2.gd` | 11/12 | **1 fail**: `test_away_juke_cap_across_seeds` 7/100 (target 0) — diagnosed test-metric artifact |
| `test_sprint13_*` (all) | all green | |
| `test_sprint14_1*.gd` | 24/24 | green |
| `test_sprint12_1.gd` | 26/30 | 4 fail — **pre-existing**, silent-green (exits 0) |
| `test_sprint12_2.gd` | 32/33 | 1 fail — **pre-existing**, silent-green |
| `test_sprint10.gd` | parse error | **pre-existing**, Godot 4.4 strict-type, silent-green |

---

_Audit complete. 2026-04-17T16:44Z — Specc._
