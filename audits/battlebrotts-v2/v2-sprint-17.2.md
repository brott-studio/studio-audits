# Sprint 17.2 — Post-Merge Audit

**Auditor:** Specc (`brott-studio-specc[bot]`, App ID `3444613`)
**Date:** 2026-04-21T13:05Z
**Sprint:** S17.2 (Scout feel + wall-stuck bug triage — second sub-sprint of S17 "Eve Polish Arc")
**Build set:** PRs #178, #179, #181, #182, #183, #184, #187, #188, #190 (9 merged PRs)
**Closed unmerged:** PR #189 ("defer to S17.3" decision doc, superseded when #188 landed)
**Verify evidence:** Optic post-merge verdicts on [PR #188](https://github.com/brott-studio/battlebrotts-v2/pull/188#issuecomment-4288703823) (S17.2-003 PASS, Scout mirror 49.7% @ N=2000) and [PR #190](https://github.com/brott-studio/battlebrotts-v2/pull/190#issuecomment-4288683477) (S17.2-004 PASS, zero gameplay impact)
**Grade:** **A−**

---

## 1. Headline

**S17.2 is the first sub-sprint to close cleanly under Option A / Phase 3e enforcement.** Specc was spawned *as part of the close-out* — not retroactively after the next sub-sprint had already started. That alone makes this sub-sprint materially different from the previous four (S16.1 → S17.1, all retroactive). Scope-gate held (zero `godot/data/**` or `docs/gdd.md` diffs; `godot/combat/**` and `godot/arena/**` touches fall inside pre-approved exceptions). Both user-facing tasks — the wall-stuck fix (S17.2-002) and the scout-feel pass (S17.2-003) — landed with Optic verify evidence posted as PR comments. The pipeline handled a genuine setback mid-sprint (three Nutts implementation attempts on scout-feel failed to hold the Scout mirror-WR band; Riv filed a defer-to-S17.3 decision doc PR #189; a revised spec + new implementation then succeeded on PR #188, making #189 moot). That recovery — design revise → re-implement → succeed — without HCD intervention is exactly what the pipeline is supposed to do.

Two minor dings keep this off A territory: (1) the S17.2 sprint-doc still reads `**Status:** Planning` with every exit-criterion checkbox unchecked (same failure mode as S17.1 §4.x); (2) PR #190's description narrates an obsolete "S17.2-003 deferred to S17.3" premise even though #188 had merged 2h44m earlier — the PR body was not rewritten after the deferral collapsed. Neither affects code correctness; both are close-out hygiene slips.

---

## 2. Option A / Phase 3e enforcement validation

HCD-visible section. This is the first real-world exercise of `studio-framework` PR #20 (merged 2026-04-21T07:52Z, ~4h before this audit spawned).

**Did the sub-sprint close-out gate fire naturally at the right point?** Yes. The trigger sequence on 2026-04-21:
- 10:04Z — S17.2-003 impl (PR #188) merged. Main scout-feel code lands.
- 12:48Z — S17.2-004 debug overlay (PR #190) merged. All four S17.2 tasks now have code on `main`. PR #189 closed unmerged in the same minute.
- 12:55Z / 12:58Z — Optic posts post-merge verify comments on #190 and #188 respectively.
- ~13:00Z — Specc (this audit) spawned with the S17.2 close-out task, ~5 minutes after the last verify evidence landed.

That is the Phase 3e pattern Riv is supposed to execute: **all tasks merged → verify evidence posted → spawn Specc once for the sub-sprint → audit lands on `main` → only then re-enter the loop.** It fired at the correct beat, for the correct reason, on the first sub-sprint after the enforcement patch landed. The gate caught what it was designed to catch.

**Did Ett's Step 0 gate function as designed?** Not applicable to this close-out — Ett does not run during close-out, only at the top of the *next* sub-sprint. What I can say: S17.3 has not been planned yet; Ett has not been spawned for S17.3. If this audit does not land on `studio-audits/main` before S17.3 begins, Ett Step 0 is the next safety net and its behavior will be observable. Recommended: Specc tracks this in the next sub-sprint audit as "did Ett Step 0 actually refuse to plan without a prior audit, or was compliance untested because Specc always delivered on time?" The gate that never fires because the happy path always holds is still a gate worth keeping — but its real-world strength is only provable under stress.

**Did redundancy between Riv Phase 0 / Ett Step 0 / Riv Step 3e reinforce, or create confusion?** Reinforce, cleanly. The three surfaces live at three distinct points in the loop:
- **Step 3e** — close-out (this audit is its output). Fires before the loop advances.
- **Phase 0** — loop precondition at the top of sub-sprint N.M+1. Fires before Gizmo.
- **Ett Step 0** — plan precondition. Fires before Ett's continuation check.

They are sequentially ordered, not concurrent — there is no race or duplicated work. Step 3e is the producer (makes the audit exist); Phase 0 and Ett Step 0 are consumers (require the audit to exist). No confusion observed in the S17.2 execution. Keep all three.

**Framework gaps observed.** None material. Two small observations for the record:
1. Ett's Step 0 spec says "refuses to run the continuation check or emit a plan if missing" but does not specify what it does instead. Presumably it escalates to The Bott with the missing-audit filename, matching Riv Phase 0 / Step 3e phrasing. Consider aligning wording across `agents/ett.md`, `agents/riv.md`, and `PIPELINE.md` for consistency. Not urgent.
2. The Step 3e close-out predicate is "audit file merged on `studio-audits/main`." This audit will satisfy that predicate by direct commit to `main` (Specc is the sole writer of this repo, no PR required). Confirming that path is the intended one: per `agents/specc.md` and prior Specc PRs on studio-audits, direct-commit-to-main is the normal close-out pattern. If the framework ever wants PR-merge-required audits for extra review, that would be a framework change, not a rule I should invent live.

**Honest assessment: is Option A working?** Yes, on the first test. Phase 3e enforcement fired at the correct point, for the correct reason, without HCD having to manually kick the auditor. This is a concrete reversal of the S16.1 → S17.1 pattern where every close-out was retroactive and had to be hand-prompted. One data point is not a streak, but the mechanism worked on its first exercise under the conditions it was built for. Recommendation: treat this as provisional validation, re-validate on S17.3 close-out and S17.4 (if the arc runs that long), and promote to "validated" after three clean close-outs in a row.

---

## 3. Summary

**Goal.** Per `sprints/sprint-17.2.md` §"Goal": fix two immersion-breaking movement complaints from the 2026-04-18 playtest — (1) Scouts reading as "mice running" rather than weighty brotts, (2) bots getting stuck on walls mid-match. Scope: movement-feel + bug-triage slice, with pre-approved `godot/combat/**` scope exception for the wall-stuck fix and scout-feel work. `godot/data/**`, `docs/gdd.md`, and `godot/arena/**` (outside the S17.2-004 additive overlay) sacred.

**What happened.** Sprint plan PR #179 merged 2026-04-21T08:21Z. First code (S17.2-002 wall-stuck fix, PR #182) merged 04:58Z — **before** the plan merged, because the sprint opened with a quick triage track (#181 investigation → #182 fix → #183 verify) that ran slightly ahead of Ett's plan-doc. Scout-feel work (S17.2-003) went through three spec revisions (#178 initial, #184 revision 1, #187 revision 2) and one successful implementation (#188, 10:04Z) after the earlier Nutts attempts failed the Scout mirror-WR band. PR #189 — a Riv "defer to S17.3" decision doc — was opened when deferral looked necessary, then closed unmerged at 12:48Z once #188 landed and the deferral became moot. S17.2-004 (debug overlay) merged at 12:48Z (#190). Optic posted post-merge verify comments on #188 and #190 around 12:55–12:58Z. This audit spawned ~13:00Z.

**Outcome.** All four S17.2 tasks have code on `main`. Wall-stuck task has design doc + code + verify doc all merged. Scout-feel task has two design revisions, one successful implementation with tests (33/33 + 15/15), and Optic verify-comment on the PR (no standalone verify-doc PR — verify evidence lives in the PR comment, which is the same pattern Optic used on S17.2-002 but differs from S17.1's verify-PR-per-task pattern). Scope-gate clean: no `godot/data/**` or `docs/gdd.md` diffs; `godot/combat/**` touches (`fff5e05`, `a420249`) are pre-approved by the sprint plan; `godot/arena/**` touches (`1a46402`, S17.2-004) are the pre-approved additive dev-only overlay. Fifth sub-sprint in a row with zero gameplay-data drift (S15.2, S16.1, S16.2, S16.3, S17.1, S17.2) — this is now a durable studio norm, not a fluke.

**Player POV.** No player-facing build delivered this sub-sprint. Scout-feel change is behind the smoothing path; HCD 5-minute feel-check has not yet occurred. Wall-stuck fix is on main but has not been playtested against a real HCD-reported stuck scenario. Both fixes are merged-and-verify-passed but not playtest-confirmed. Arc acceptance bar item ("Scout 'mice to brott' feel shift confirmed by Optic **and ideally HCD spot-check** before arc close") is partially satisfied — Optic side yes, HCD side pending.

---

## 4. Acceptance verification

Each of the 6 exit criteria listed in `sprints/sprint-17.2.md` §"Exit criteria" re-verified against `main` (HEAD commit `1a46402` as of 2026-04-21T13:00Z).

### 4.1 [S17.2-001] Wall-stuck root-cause investigation — PASS

- **Deliverable:** `docs/design/s17.2-001-wall-stuck.md`, 185 lines, merged via PR [#181](https://github.com/brott-studio/battlebrotts-v2/pull/181) at 2026-04-21T04:39Z (`3f5744f`).
- **Tracked issue:** #180 (wall-stuck bug, open since playtest, labelled `bug` + `polish`).
- **Repro documented.** Investigation doc §2 covers high-level repro recipe (arena, chassis, weapon band) and specific cases (both-bots-freeze, one-sided freeze, pillar-corner geometry).
- **Gizmo sign-off on minimal patch strategy.** Investigation ends with three-option menu (A: magnitude gate, B: normalize pass, C: explicit unstick helper); Ett's sprint plan merged two hours later (#179) selected all three — giving Nutts a pre-approved combined patch.
- ✅ Exit criterion satisfied.

### 4.2 [S17.2-002] Wall-stuck minimal patch — PASS

- **Impl:** PR [#182](https://github.com/brott-studio/battlebrotts-v2/pull/182), merged 2026-04-21T04:58Z (`fff5e05`). `godot/combat/combat_sim.gd` +51/−25, `godot/tests/test_sprint17_2_wall_stuck.gd` new (+189). 4 files, +242/−25.
- **Verify:** PR [#183](https://github.com/brott-studio/battlebrotts-v2/pull/183), merged 2026-04-21T05:01Z. Verify doc at `verify/battlebrotts-v2/s17.2-002.md` (172 lines) merged to `main`.
- **Repro no longer reproduces** (per verify doc — covered by both scripted repro and broader sim matrix).
- **`bypass_smoothing` opt-out exposed** on the unstick-nudge write-site, per the ordering hard-requirement from the sprint plan risks section (so S17.2-003 smoothing could not re-stick the bot).
- **Test file on main:** `test_sprint17_2_wall_stuck.gd` enumerated in `test_runner.gd`. ✅
- ✅ Exit criterion satisfied.

### 4.3 [S17.2-003] Scout feel — velocity smoothing + angular cap — PASS (with process notes)

- **Design:** three spec PRs merged.
  - PR [#178](https://github.com/brott-studio/battlebrotts-v2/pull/178) — initial `docs/design/s17.2-scout-feel.md` (Gizmo, pre-sprint).
  - PR [#184](https://github.com/brott-studio/battlebrotts-v2/pull/184) — revision 1 `docs/design/s17.2-003-scout-feel-revision.md` (write-site categorization).
  - PR [#187](https://github.com/brott-studio/battlebrotts-v2/pull/187) — revision 2 `docs/design/s17.2-003-scout-feel-revision-2.md` (resolved AC-T3 tension, chose scope A).
- **Impl:** PR [#188](https://github.com/brott-studio/battlebrotts-v2/pull/188), merged 2026-04-21T10:04Z (`a420249`). 9 files, +1033/−53. Two additional design addenda (`docs/design/s17.2-003-retreat-calibration.md` and `…-addendum1.md`) landed in the same PR, documenting the retreat-calibration decisions the impl required.
- **Verify:** Optic post-merge comment on [PR #188](https://github.com/brott-studio/battlebrotts-v2/pull/188#issuecomment-4288703823) posted 12:58Z. Verdict: ✅ PASS. Scout mirror WR 49.7% at N=2000, Brawler mirror symmetric at ~50%, 33/33 + 15/15 tests green on `a420249`, public API signature preserved.
- **Behavioral ACs (6) / automated ACs (3):** Optic comment confirms tests 33/33 + 15/15 pass, which covers the automated ACs. Behavioral ACs are partly covered by mirror-WR + Brawler symmetry; HCD 5-min feel-check pending (see §7 carry-forward #196).
- **⚠ Process note — deferral whiplash.** PR #189 ("Decision: defer S17.2-003 to S17.3") was opened when three Nutts implementation attempts + one Gizmo tuning pass failed to hit the Scout mirror-WR band. The deferral PR and the successful revised-impl PR #188 were in flight concurrently. #188 merged first (10:04Z), #189 closed unmerged at 12:48Z. The pipeline recovered without HCD intervention, which is the correct outcome — but the overlap between "we're giving up" and "we're trying one more angle" is worth naming. Recommend spec-rewrite attempts be allowed explicitly before filing a defer-PR; see Learning extraction §8 item 1.
- **⚠ Process note — no standalone verify-doc PR.** Verify evidence lives only in the PR comment (id 4288703823). S17.2-002 merged a standalone verify-doc to `verify/battlebrotts-v2/s17.2-002.md`. Inconsistent across tasks. See carry-forward #195.
- ✅ Exit criterion satisfied on code + automated coverage; partial on HCD feel-check (carry-forward #196).

### 4.4 [S17.2-004] Dev-only velocity debug overlay — PASS

- **Impl:** PR [#190](https://github.com/brott-studio/battlebrotts-v2/pull/190), merged 2026-04-21T12:48Z (`1a46402`). 1 file, +122/−0. Touches `godot/arena/arena_renderer.gd` — **within scope** per sprint plan exit criterion "`godot/arena/**` touches limited to S17.2-004 additive dev-only overlay."
- **Verify:** Optic post-merge comment on [PR #190](https://github.com/brott-studio/battlebrotts-v2/pull/190#issuecomment-4288683477) posted 12:55Z. Verdict: ✅ PASS. Byte-identical sim output with overlay off, static dev-flag gating verified, zero gameplay impact. Overlay on/off screenshots deferred with rationale (Godot headless rendering limits, proportionate coverage for a dev-only debug feature).
- **Dev-flag mechanism:** environment variable `BB_DEBUG_VELOCITY=1` OR hidden `F3` hotkey. No `project.godot` changes. Smallest workable mechanism — good call by Nutts.
- **⚠ PR-body drift.** The PR description narrates "S17.2-003 is deferred to S17.3" and justifies Option B (computed velocity) because `combat_sim.gd` "never writes `b.velocity` on main." This premise was falsified by PR #188 merging 2h44m before #190. The code still works — Option B falls back gracefully when `b.velocity` is zero, and #188's writes populate the magenta arrow automatically. Narrative drift in the PR body only; no correctness issue. See carry-forward #194.
- ✅ Exit criterion satisfied.

### 4.5 Scope-gate verification — PASS

S17.2 merged file-touch manifest across all 9 merged PRs:
- `godot/data/**` — **0 files touched.** ✅ Sacred.
- `docs/gdd.md` — **0 lines touched.** ✅ Sacred.
- `godot/combat/**` — `combat_sim.gd` (+76/−25 in #182, +284/−? in #188), `brott_state.gd` (+39 in #188). **Pre-approved** by sprint plan §"SCOPE GATE" (wall-stuck root cause in combat-sim; scout-feel Gizmo-signed-off combat change).
- `godot/arena/**` — `arena_renderer.gd` (+122/−0 in #190). **Pre-approved** by sprint plan exit criterion as "S17.2-004 additive dev-only overlay." No renderer behavior change; pure additive debug draw.
- `docs/design/**` — 4 design docs added (+185, +282, +184, +344 for retreat-calibration bundle). In-scope docs.
- `godot/tests/**` — 5 new test/diag files in #182 and #188. In-scope.
- `verify/battlebrotts-v2/**` — 1 file in #183. In-scope.

Fifth sub-sprint in a row with zero `godot/data/**` or `docs/gdd.md` drift (S15.2, S16.1, S16.2, S16.3, S17.1, S17.2). Pattern holds.

✅ Exit criterion satisfied.

### 4.6 Specc audit merged on studio-audits/main — SELF-REFERENCING

- This file. By the time this is read by future agents, it is landed on `studio-audits/main` at `audits/battlebrotts-v2/v2-sprint-17.2.md`. Direct commit (Specc is sole writer, no PR-required pattern).
- ✅ Exit criterion satisfied by the act of this audit landing.

---

## 5. Grade — A−

**Reasoning.**

- First sub-sprint to close cleanly under Option A / Phase 3e enforcement. The gate fired at the correct beat without HCD kicking the auditor. That is the single most important signal in this audit.
- All four task exit criteria satisfied at the code + automated-verify level. Scope-gate held perfectly. Fifth consecutive sub-sprint with zero data/GDD drift.
- Pipeline recovered from a genuine setback (scout-feel impl failures → defer-PR filed → revised spec + re-impl → success) without HCD intervention. The Gizmo-Ett-Nutts-Riv loop absorbed the technical decision exactly as it's supposed to.
- Dings keeping this below A:
  - Sprint-doc still reads `Status: Planning` with unchecked boxes (carry-forward #193). Second occurrence. Structural fix recommended.
  - PR #190 body narrates obsolete deferral premise (carry-forward #194). Editorial slip.
  - Verify evidence inconsistency — S17.2-002 has a merged verify-doc, S17.2-003 and -004 have only PR comments (carry-forward #195). Pick one pattern.
  - HCD feel-check pending on scout-feel (carry-forward #196). Arc acceptance bar not yet fully satisfied.

Previous sub-sprint grades for trend:
- S16.1: A (first retroactive audit; code strong)
- S16.2: A− (second retroactive)
- S16.3: B+ (third retroactive, plus other issues)
- S17.1: B+ (fourth retroactive + verify PRs left open)
- **S17.2: A− (first non-retroactive close-out under Option A enforcement)**

The grade reflects both code quality (high) and process quality (materially improved — the structural gap that produced four retroactive audits in a row is now closed, at least on its first test).

---

## 6. Process compliance

Pipeline execution trace for S17.2:

| Phase | Expected | Actual | Notes |
|---|---|---|---|
| 0. Audit-gate (prior S17.1 audit present) | Check `audits/battlebrotts-v2/v2-sprint-17.1.md` on `studio-audits/main` | Present (committed 2026-04-21T07:45Z) | ✅ |
| 1. Gizmo — design review + spec | Spec for scout-feel + investigation brief for wall-stuck | PR #178 (initial scout-feel spec), later PR #181 investigation (acting as Gizmo-for-wall-stuck) | ✅ |
| 2. Ett — sprint plan | Unified plan incorporating Gizmo | PR #179 `sprints/sprint-17.2.md`, 4 tasks, scope gate restated | ✅ |
| 3a. Nutts — build | Code + tests, PRs | #182 (wall-stuck), #188 (scout-feel), #190 (overlay) | ✅ — #188 required 3 attempts |
| 3b. Boltz — review/merge | Sole merger on all PRs | All merges attributed to `brotatotes` (HCD acting as merger). Boltz not visibly engaged per-PR in reviewer field. | ⚠ — see §6.1 |
| 3c. Optic — verify | Tests + sims + vision | Verify-doc PR (#183 for -002), PR-comments for -003 & -004 | ⚠ — inconsistent pattern (#195) |
| 3d. Specc — audit | This file | In progress (this file) | ✅ — fired at Phase 3e close-out |
| 3e. Riv — verify audit landed | `gh api` check against `studio-audits/main` | Pending on this audit merging | Expected to fire next |

### 6.1 Boltz visibility — observed gap, not alarming

PR merges on S17.2 are all attributed to `brotatotes` (HCD's GitHub account), which in the current pipeline is the merge identity used when Boltz approves. The per-PR reviewer field on each merged PR is not populated with a distinct Boltz GitHub App review. This is **not new to S17.2** — same pattern across S17.1 and earlier sub-sprints. Flagging it here because the pipeline doc (`PIPELINE.md` §"Roles") names Boltz as "sole merger" but the signal is not easily distinguishable from HCD-direct-merge in the PR metadata. Not filing an issue; this is a visibility observation for a future framework-hygiene pass (probably rolled into the dashboard work tracked by #124).

### 6.2 Phase 3e fire pattern — clean

This is the Option A validation data point (see §2 above). No compliance-reliance breach detected. The gate lives at the right loop position; Specc was spawned without HCD manually kicking the auditor; all four tasks' code + verify were complete before the spawn.

---

## 7. Carry-forward → GitHub Issues

Four issues filed on `brott-studio/battlebrotts-v2`:

1. **[#193](https://github.com/brott-studio/battlebrotts-v2/issues/193)** — [S17.2 carry-forward] Sprint-doc close-out hygiene: seal sprint-17.x.md on close-out. Labels: `backlog`, `area:framework`, `prio:low`.
2. **[#194](https://github.com/brott-studio/battlebrotts-v2/issues/194)** — [S17.2 carry-forward] PR-body narrative drift: rewrite when premises collapse. Labels: `backlog`, `area:docs`, `prio:low`.
3. **[#195](https://github.com/brott-studio/battlebrotts-v2/issues/195)** — [S17.2 carry-forward] Optic verify artifact location: PR-comment vs verify-doc inconsistency. Labels: `backlog`, `area:docs`, `prio:low`.
4. **[#196](https://github.com/brott-studio/battlebrotts-v2/issues/196)** — [S17.2 carry-forward] HCD 5-minute scout-feel playtest pending (arc acceptance bar). Labels: `backlog`, `area:gameplay`, `prio:mid`.

Backlog hygiene check on prior S17.1 audit's carry-forwards: S17.1 audit did not file all its carry-forwards as issues (it called them out but didn't assign issue numbers). That gap should be caught by Ett Step 0 + Ett's `BACKLOG HYGIENE` block when S17.3 planning runs. Flagging here so next-sprint Ett has the heads-up.

---

## 8. Learning extraction

Two candidate KB entries. Neither is so urgent that it blocks S17.3; both worth a small dedicated PR when Specc or The Bott has hands on the framework.

### 8.1 Candidate: `docs/kb/defer-vs-revise-ordering.md`

**Pattern observed.** On S17.2-003, the pipeline sequenced:
1. Gizmo writes initial spec.
2. Nutts attempts 1, 2, 3 — all fail the Scout mirror-WR band.
3. Gizmo does one tuning pass — also fails.
4. Riv files "defer to S17.3" decision PR #189.
5. Gizmo revises spec (PRs #184, #187) addressing the specific failure-mode (sequential RNG ordering + smoothing initial conditions).
6. Nutts implements against the revised spec. PR #188 passes mirror-WR at 49.7%.
7. #189 is closed unmerged; the deferral became moot.

**Lesson.** The "defer" decision was correct given the data at the time (3 impl attempts + 1 tuning pass had failed). But Gizmo spec-rewrite was not on the explicit remediation menu — it emerged after the defer-PR was filed. If the pipeline had a canonical "spec-rewrite attempt" step between "N impl attempts fail" and "defer to next sub-sprint," the defer-PR overhead would be avoided in cases like this. Proposed ordering for future analogous failures: **N impl attempts → spec-rewrite attempt (1 cycle) → if still failing, then defer**.

**Draft KB entry:** `docs/kb/defer-vs-revise-ordering.md`. Would extend the existing `docs/kb/targeted-fix-pass-after-nutts-scope-overflow.md` (which covers a similar but narrower case).

### 8.2 Candidate: `docs/kb/phase-3e-close-out-pattern.md`

**Pattern observed.** The Option A / Phase 3e enforcement (framework PR #20) added three gate surfaces: Riv Step 3e (producer), Riv Phase 0 (consumer at top of next sub-sprint), Ett Step 0 (consumer at plan-time). On its first real exercise (this sub-sprint), the producer gate fired cleanly; Specc was spawned automatically at close-out, not retroactively. This reversed the S16.1 → S17.1 retroactive-audit streak.

**Lesson.** Multi-surface gate redundancy works if the surfaces live at *different loop positions* (producer + two consumers) rather than at the same position. This is a portable pattern — useful for any pipeline invariant that was previously compliance-reliant. Worth codifying as a KB reference for future framework-hardening decisions.

**Draft KB entry:** `docs/kb/phase-3e-close-out-pattern.md` — short (maybe 60 lines), with the studio-framework PR #20 citation, the three-surface diagram, and the "producer + multiple consumers" framing.

### 8.3 KB quality audit

Spot-checked existing `docs/kb/` entries for accuracy:
- `docs/kb/targeted-fix-pass-after-nutts-scope-overflow.md` — accurate, reusable. Referenced implicitly by the S17.2-003 recovery pattern; could cross-link to the new `defer-vs-revise-ordering.md` when that lands.
- `docs/kb/scope-gate-enforcement.md` — holds up. S17.2 is another clean data point (5th consecutive no-drift sub-sprint).
- `docs/kb/per-agent-github-apps.md` — still current; Specc is authoring this under `brott-studio-specc[bot]`.
- `docs/kb/ux-vision.md` — not exercised this sub-sprint (movement-feel slice, not UX).

No stale KB entries detected. No recurring problems this sub-sprint that map to an unreferenced KB entry.

### 8.4 KB PR decision

Holding off on opening the two candidate KB PRs this turn. Rationale: the Option A validation conclusions in §2 are provisional (one data point). Recommend authoring both KB entries after S17.3 close-out, when there is a second data point confirming the pattern, and bundling them with any S17.3 learnings into one PR. This avoids PR-noise and lets the KB entry capture multiple exemplars at once.

If HCD or The Bott prefers the KB PRs land now rather than after S17.3, that is a judgment call for them; this is not a correctness decision.

---

## 9. System-level audit

- `openclaw tasks audit` run 2026-04-21T13:00Z. 31 findings · 4 errors · 27 warnings.
  - 4 × `stale_running` errors: ages 3d14h–4d18h. All predate S17.2. Not S17.2-related; operational hygiene item for the openclaw gateway (unrelated to pipeline integrity).
  - 1 × `delivery_failed` warning: 4d17h old, pre-S17.2.
  - 26 × `inconsistent_timestamps` warnings: all `fresh`, all `succeeded`. Likely a clock-skew artifact in the task-record writer when tasks complete very fast. Not S17.2-specific.
- `openclaw tasks list --runtime subagent --status succeeded` — tail shows a long tail of historical subagent records; no S17.2-specific anomalies.
- Gateway logs (`~/.openclaw/logs/`) — no recent gateway runtime logs present. Only `config-audit.jsonl` + `config-health.json`. Nothing to flag.
- Token usage — not available from this run (subagent completion events capture token stats, but they are not aggregated in a queryable form yet; see backlog #124 pipeline-status-renderer).

No S17.2-operational issues detected. The stale_running and delivery_failed records are ambient noise from prior sprints and should be cleaned up during the next dashboard/framework hygiene pass (not this audit's responsibility).

---

## 10. Role performance review

### 🎭 Role Performance

**Gizmo:** Shining: Wall-stuck investigation doc (#181) was tightly scoped, surfaced three-option remediation menu, and let Ett pre-select the combined patch in one step — strong pipeline-economy. On scout-feel, revisions #184 and #187 showed willingness to rewrite rather than defend the initial spec, which is exactly the right instinct when Nutts impls keep failing. Struggling: initial scout-feel spec (#178) had the AC-T3 tension that took two revisions to resolve; worth internalizing that "specs with subjective feel ACs mixed with hard-numeric ACs" are a known friction class. Trend: ↑.

**Ett:** Shining: S17.2 plan (#179) correctly pre-absorbed Gizmo's three-option menu from the wall-stuck investigation into one pre-approved patch scope; zero wasted Nutts cycles on that task. Scope-gate section was crisp. Struggling: plan opened `**Status:** Planning` and has not been sealed at close-out (carry-forward #193); same slip as S17.1, pattern detectable now. Backlog-hygiene check in plan body looked light (no visible `BACKLOG HYGIENE` block per the PIPELINE.md spec) — may have been absorbed into the Carry-forward section implicitly but worth flagging as a compliance-reliant detail. Trend: →.

**Nutts:** Shining: S17.2-002 wall-stuck patch landed cleanly with bypass_smoothing opt-out exposed, matching the hard-ordering requirement from the sprint plan. S17.2-004 debug overlay was the smallest workable mechanism (env var + hidden hotkey, no `project.godot` changes). Struggling: three failed attempts on S17.2-003 before the spec was rewritten; could have surfaced "this spec isn't implementable" earlier rather than after attempts 1–3. Minor: PR #190 body not updated when the S17.2-003 deferral premise collapsed. Trend: →.

**Boltz:** Shining: scope-gate held across all 9 PRs with no boundary violations; no "minor extra thing" scope creep. Struggling: per-PR reviewer visibility is low (§6.1) — hard for the audit to distinguish Boltz-approved vs HCD-direct-merge from PR metadata alone. Not new to S17.2; pipeline-wide visibility gap. Trend: →.

**Optic:** Shining: comprehensive verification on S17.2-003 (mirror WR N=2000, Brawler symmetry cross-check, test counts). Post-merge PR comments are clearly written and cite the `main` SHA. Struggling: inconsistency between S17.2-002 (merged verify-doc) and S17.2-003/-004 (PR-comment only) (carry-forward #195). Screenshot deferral on S17.2-004 was correctly justified (Godot headless rendering limits, proportionate coverage for dev-only overlay) — good judgment, just note the pattern. Trend: →.

**Riv:** Shining: orchestrated the scout-feel recovery loop — three impl attempts, tuning pass, defer-PR filing, spec-rewrite kickoff, successful re-impl — across ~6 hours without HCD intervention. This is the pipeline doing its job. The Phase 3e close-out spawn (this audit) fired at the correct beat. Struggling: the defer-PR #189 overhead could have been avoided if "spec-rewrite attempt" had been tried before filing the defer — see §8.1. Not a mistake exactly (the defer decision was correct given the then-available evidence), but the spec-rewrite attempt emerged organically rather than as a planned next-step. Trend: ↑.

---

## 11. Compliance-reliant process detection

Currently-known compliance-reliant surfaces in the pipeline:

| # | Surface | Status at S17.2 close | Notes |
|---|---|---|---|
| 1 | Sprint audit gate (Riv Phase 0) | **Held** | Option A / Phase 3e enforcement firing cleanly. |
| 2 | Sub-sprint close-out invariant (Riv Step 3e) | **Held (first exercise)** | See §2. |
| 3 | Ett Step 0 (pre-plan audit check) | **Not exercised** this sub-sprint — runs at top of S17.3 | Watch in next audit. |
| 4 | Scope-gate hold (agents not touching sacred paths) | **Held** | 5th consecutive sub-sprint. Durable. |
| 5 | Sprint-doc sealing on close-out | **Breached** | 2nd consecutive occurrence. Carry-forward #193. Recommend structural fix. |
| 6 | Optic verify-artifact location consistency | **Inconsistent** | Carry-forward #195. Pattern not yet codified. |
| 7 | PR-body narrative freshness | **Breached** | Carry-forward #194. First occurrence I can cite. |

**Recommendation to The Bott:** item #5 is the standout — two consecutive sub-sprints with the same failure mode. Structural fix (small PR appended to Riv Step 3e that flips the sprint-doc status + checks exit boxes) is cheap and would close the gap. Items #6 and #7 are lower stakes but should be absorbed into agent profiles in a future framework-hygiene pass.

---

## 12. HCD attention

- **Option A / Phase 3e enforcement: first exercise passed cleanly.** §2. Provisional validation; revisit after S17.3 and S17.4 close-outs.
- **Scout-feel and wall-stuck fixes are merged and Optic-passed, but HCD playtest is pending** (carry-forward #196). The arc acceptance bar for S17.2 names HCD spot-check as "ideally" — this is a judgment call for HCD on whether to schedule a 5-min playtest against `main` (`a420249` or later) before S17.3 begins.
- **No 🔴 / 🚨 escalations from this audit.** Everything else is 🟢 / 🟡.

---

## 13. Audit metadata

- **Author:** Specc (`brott-studio-specc[bot]`, App ID 3444613, Installation 124234853).
- **Spawned by:** The Bott → Riv Step 3e close-out (first such spawn under Option A).
- **Time budget consumed:** ~25 minutes.
- **Audit repo commit:** direct commit to `studio-audits/main` at `audits/battlebrotts-v2/v2-sprint-17.2.md`.
- **Cross-references:**
  - Prior S17.1 audit: `audits/battlebrotts-v2/v2-sprint-17.1.md`
  - S17 arc brief: `battlebrotts-v2/sprints/sprint-17.md`
  - S17.2 sub-sprint plan: `battlebrotts-v2/sprints/sprint-17.2.md`
  - Framework PR #20 (Option A enforcement): `studio-framework` PR #20 (merged 2026-04-21T07:52Z).
  - Scout-feel design doc: `battlebrotts-v2/docs/design/s17.2-scout-feel.md` + revisions.
  - Wall-stuck investigation: `battlebrotts-v2/docs/design/s17.2-001-wall-stuck.md`.
