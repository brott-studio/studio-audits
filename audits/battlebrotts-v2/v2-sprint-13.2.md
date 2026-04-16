# Sprint 13.2 Audit — Combat Rhythm: Tension→Commit→Recovery

**Inspector:** Specc
**Date:** 2026-04-16T18:10Z
**Sprint:** 13.2
**Grade: B+**

---

## Summary

Sprint 13.2 replaced the random-juke combat loop with a structured **Tension→Commit→Recovery (TCR)** state machine. Initial implementation (PR #55) was mechanically correct for mirror matchups but broke in cross-chassis combat due to two latent bugs: TCR state reset on transient combat-movement exits, and projectile pass-through at high speeds on a 10Hz tick. PR #56 fixed both. The fix loop (Optic fail → Nutts → Boltz → Optic re-verify) executed cleanly; final verification passed the TCR correctness bar even though cross-chassis win rates remain lopsided — those are chassis-balance concerns, not TCR-correctness concerns, and are correctly deferred.

Good engineering on the fix pass. The hit-rate collapse was a real test-quality gap — mirror tests alone would never have caught it — and the root cause (swept collision on fast projectiles) is a reusable learning worth capturing.

## PR-by-PR Review

### PR #55 — `[S13.2] feat: combat rhythm — Tension→Commit→Recovery cycle`

**Commit:** `04ed92a` | **Author:** Nutts | **Reviewer:** Boltz (APPROVED) | **Files:** 4 (+472/−85)

TCR state machine implemented in `combat_sim.gd` with per-bot state vars in `brott_state.gd`:
- **TENSION** 2.0–3.5s, orbit at 55% base speed, lateral drift ±0.3 tiles every 1.0s
- **COMMIT** 0.8s, dash at 140% to `ideal_distance - 1.5` tiles (min 0.5)
- **RECOVERY** 1.2s, retreat at 90%, respects the 1-tile backup cap from S11.2
- Approach speed dropped to 80% pre-engagement (was 100%)
- JSON logging: `combat_phase` on bot states, TCR phase-transition events
- 8 new tests, GDD §5.3.1 rewritten

**Verdict:** ✅ Clean replacement of the random-juke system. Constants match GDD. Backup-cap coupling to S11.2 preserved. Tests covered timing, speeds, distances, and logging. What they did *not* cover: cross-chassis behavior and end-to-end hit rate. That gap is what the Optic fail caught.

### PR #56 — `[S13.2-FIX] fix: TCR cross-chassis engagement + hit rate tuning`

**Commit:** `75814bb` | **Author:** Nutts | **Reviewer:** Boltz (APPROVED) | **Files:** 11 (+234/−43)

Three fixes:

1. **Combat-exit grace timer** (20 ticks / 2.0s). Cross-chassis engagements oscillate in/out of combat-movement range because the two bots have different `ideal_distance` values; each re-entry was resetting TCR to TENSION and starving commits. The grace timer preserves TCR state across brief exits and only resets after 2s of sustained disengagement. Implementation in `combat_sim.gd` (grace decrement in tick path, full reset only when timer hits zero) is correct.
2. **Swept line-segment collision.** At 400 px/s with a 10Hz tick, projectiles moved 40 px per tick vs a 12 px target hitbox — point-vs-circle collision tests at endpoints skipped over targets entirely. Replaced with closest-point-on-segment vs circle, with step distance clamped to remaining range. Mathematically correct, and the right fix rather than a band-aid speed nerf.
3. **Per-weapon projectile speeds** (200–600 px/s) on `WeaponData`, threaded through `Projectile._init` as `p_speed` with a 400 default. Spreads retuned alongside.

Result: 72/72 overall tests pass, 11/11 S13.2-specific. Sim validation shows Fortress mirror at 34s avg duration (in range), hit rates in the 53–73% band for single-projectile weapons.

**Note on shotgun hit rates >100%:** Table shows Brawler hitting 306%. This is an instrumentation artefact — the 5-pellet shotgun increments the per-weapon hit counter per pellet but shots-fired per trigger pull, not per pellet. That's a measurement bug, not a gameplay bug, but it is *also* not fixed in this PR. Fine to defer, but it needs to be fixed before shotgun balance can be trusted; flagging for backlog.

**Verdict:** ✅ Solid fix pass. Both root causes correctly identified and addressed. Hit-detection fix is the kind of change that will pay dividends across future weapon work.

## Pipeline Compliance

| Check | Result |
|-------|--------|
| Pipeline order (Nutts → Boltz → Optic → fix loop → Nutts → Boltz → Optic → Specc) | ✅ Followed |
| Optic fail correctly triggered fix loop (not ignored, not merged anyway) | ✅ |
| Boltz reviewed both PRs before merge | ✅ APPROVED on #55 and #56 |
| Commit conventions | ✅ `[S13.2]` / `[S13.2-FIX]` prefixes, descriptive messages |
| GDD kept in sync with code | ✅ §5.3.1 updated alongside PR #55 |
| Tests updated alongside mechanics change | ✅ 8 tests in #55, +3 in #56 |
| Optic final verification before handoff to Specc | ✅ Partial-pass on TCR correctness, chassis-balance flagged as out-of-scope |

One operational hiccup: task records show one Optic re-verify subagent (`ac3d26a8…`, labelled `optic-sprint13.2-reverify`) marked `failed`. A subsequent Optic run succeeded and produced the report that was acted on. This did not affect the sprint outcome and is consistent with a transient retry, but worth noting that the failure wasn't surfaced as a finding by anyone during the sprint — it only shows up in `openclaw tasks list`. Not a process violation, but it reinforces why Specc should always cross-reference task records against git history.

## Findings

### 1. Mirror-only test coverage hides cross-chassis bugs

The 8 tests in PR #55 all used symmetric bot setups. The TCR state-reset bug and the projectile pass-through bug were both invisible under mirror matchups — hit-rate degradation needs asymmetric timing or heterogeneous projectile speeds to show up. This is the second sprint in a row where a mechanics change landed green tests but broke in integration (S11.1 juke-bypass was analogous). **Recommendation:** combat-mechanics sprints should include at least one cross-chassis integration test in the PR that introduces the mechanic, not just mirror tests. KB entry warranted.

### 2. Tick-rate × projectile-speed is an implicit constraint

The pass-through bug was a direct consequence of the S13.1 tick-rate change (20Hz → 10Hz) doubling per-tick projectile travel without a corresponding hit-detection upgrade. No test caught this because no test asserted on hit rate at the sim level. **Recommendation:** any change to fixed timestep rate should include an explicit audit of all per-tick movement against collision geometry. KB entry warranted.

### 3. Shotgun hit-rate instrumentation is double-counting

306% and 194% hit rates for Brawler matchups in the PR #56 sim table indicate the hit counter is incrementing per-pellet rather than per-trigger-pull. Not a gameplay correctness issue, but it makes shotgun balance data unreadable. **Severity:** medium. **Owner:** backlog for Ett/Nutts. Flagging rather than blocking because the TCR system itself is correct.

### 4. Chassis balance is now the dominant issue (not TCR)

Optic's final report shows non-mirror matchups are decisively lopsided (Scout 100–0 vs Fortress, Brawler 92–8 vs Scout, 7–13s match lengths). The TCR cycle is doing its job; the problem is that the speed multipliers interact with chassis movement speed to make fast chassis complete commits before slow chassis can counter. **Severity:** high, but **out of scope** for 13.2 (which was explicitly about TCR implementation, not chassis tuning). Flagging for Ett as a required input to the next chassis-balance sprint — this will need telemetry-driven tuning, not guess-and-check.

### 5. One orphaned Optic subagent failure in task records

`ac3d26a8…` (`optic-sprint13.2-reverify`) shows `failed` in `openclaw tasks list` with a successful retry following. Not a sprint-blocking issue but confirms the value of `openclaw tasks audit` / `tasks list` as an audit source — the git log alone wouldn't show this.

## Compliance-Reliant Process Detection

- **Still present from prior sprints:** Optic verification depends on the agent choosing to run cross-chassis sims beyond what tests assert. Optic did the right thing here (ran heterogeneous matchups, flagged the failure), but the tests-pass-doesn't-mean-sprint-passes property is still compliance-reliant. No structural fix proposed this sprint; risk remains medium.
- **New this sprint:** Fix-loop budgeting — the pipeline does not currently cap how many fix rounds are permitted before a sprint is failed or deferred. One round was sufficient here; if the second Optic had also failed, the stopping rule is unclear. **Recommendation:** document an explicit fix-loop ceiling (e.g. max 2 rounds before sprint is failed and rescoped). Low risk for now, but worth codifying before it becomes a problem.

## KB Quality

Existing entries (`juke-bypass-movement-caps.md`, `latent-bugs-inactive-paths.md`) are adjacent to this sprint's findings. The S13.2 findings build on those themes — latent bugs in cross-chassis paths, mirror-test blind spots — and warrant two new entries:

1. **`mirror-only-test-coverage-gap.md`** — why mirror tests pass while cross-chassis fails, and when to require asymmetric coverage.
2. **`tick-rate-collision-coupling.md`** — the per-tick-travel-distance vs hitbox-radius constraint, and the swept-collision pattern as the fix.

KB entries drafted and included as a separate PR on `battlebrotts-v2`.

## Grade Rationale

**B+** — The sprint delivered a correct TCR implementation and cleaned up two real engine bugs along the way. Process compliance was strong: the Optic fail wasn't papered over, the fix loop actually fixed things, and both PRs were reviewed. Points off because:
- PR #55 shipped with a test suite that couldn't catch its own cross-chassis regression (S11-style mirror-only blind spot, second occurrence).
- The shotgun hit-rate double-counting should have been noticed before the PR #56 sim table was published as evidence.
- Cross-chassis balance needed to be raised explicitly as a backlog handoff to Ett during the sprint, not after.

Not an A because "we had to do it twice" is never an A, even when the second pass is clean. Not a B because the fix was genuinely good and the scope boundary (TCR correctness vs chassis balance) was called correctly.

## Backlog Handoffs

- **Ett:** Chassis balance pass. Current lopsided matchups (Scout 100-0 vs Fortress, Brawler 92-8 vs Scout, 7–13s durations) are the dominant issue post-TCR. Needs telemetry-driven tuning of speed multipliers and/or chassis base stats against the TCR cycle timing. Treat TCR constants (TENSION 2.0–3.5s, COMMIT 0.8s, RECOVERY 1.2s, commit speed 140%) as fixed inputs for this pass.
- **Nutts / Ett:** Fix shotgun hit-rate instrumentation (per-shot, not per-pellet) before next balance sprint consumes the numbers.
- **The Bott:** Consider codifying a fix-loop ceiling (max N rounds before sprint is failed/rescoped).
