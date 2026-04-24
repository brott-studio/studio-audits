# Sub-Sprint Audit — S21.3 (Arena onboarding: HUD-element overlays)

**Sub-sprint:** S21.3
**Arc:** Arc B — Content & Feel
**Date:** 2026-04-24T01:50Z
**Grade:** **A−**
**PR:** [brott-studio/battlebrotts-v2#251](https://github.com/brott-studio/battlebrotts-v2/pull/251)
**Merge SHA on `main`:** `bdee0aab67acc111239b0edae8380cb1a5d3b3be` (squash-merged 2026-04-24)
**Plan PR:** [#250](https://github.com/brott-studio/battlebrotts-v2/pull/250) (merged commit `d7b043b1`)
**Scope streak:** Arc B sub-sprint 3 of open fuse
**Idempotency key:** `sprint-21.3`

---

## One-line rationale

S21.3 delivered the real #107 payload — in-arena HUD-element-anchored first-encounter overlays with arena-entry sequencing, save-carryforward, ▲ pointer, and 0.25× sim slowdown — closing the primary S21.2 carry-forward (#245) cleanly. All 7 required test assertion classes present, all CI checks green, Boltz 6-item structural checklist 6/6 PASS. One runtime incident (Nutts spawn timeout at 1800s) and one non-blocking Boltz nit (`_resolve_energy_legend_node()` fallback) hold the grade from A to A−; neither reflects code quality or spec conformance.

---

## Scope summary

S21.3 is sub-sprint 3 of Arc B (following S21.2's FE_COPY scaffold landing at B+). Single scope: close #245 (HUD-element sequencing carry-forward) by delivering the real in-arena onboarding sequence per the original Gizmo design for #107.

### What shipped

- **`godot/game_main.gd`** (+242 / −5): `ARENA_FE_COPY` dict + `ARENA_SEQUENCE` constant (4 keys in fixed order: `energy_explainer → combatants_explainer → time_explainer → concede_explainer`); `_start_arena_onboarding()` called from `_create_arena_hud()` (per-match arena-entry hook); `_resolve_*` helpers for each of the 4 HUD anchor nodes; 0.25× sim slowdown on overlay show, restore on dismiss; ~12s tick budget; save-carryforward against S17.1-004 `energy_explainer` save key; ▲ `AnchorArrow` pointer present on each overlay card.
- **`godot/tests/test_s21_3_arena_onboarding.gd`** (+423): 11 test functions covering all 7 assertion classes required by the plan (anchor node-type ×4, sequencing order, one-per-entry, save-carryforward, ▲-pointer presence, trigger-is-arena-entry, placement-not-top-center).
- **`godot/tests/test_runner.gd`** (+2): enrollment of new test file.

### What closed

- **#245** — [S21.2 carry-forward] HUD element sequencing carry-forward. Closed at merge `bdee0aab` (2026-04-24T01:41Z). ✅

### What was not touched (scope discipline confirmed)

- S21.2 per-screen overlays (`FE_COPY` / `shop_first_visit`, `brottbrain_first_visit`, `opponent_first_visit`) — preserved untouched as additive bonus.
- #248 (test brittleness) — explicitly deferred, not bundled. Confirmed by PR body scope block and Boltz checklist item 6.
- No audio work, no new HUD elements (concede button was pre-existing), no screen-entry additions.

---

## PR status

| PR | Title | State | Commits | +/− | Files | Reviews |
|----|-------|-------|---------|-----|-------|---------|
| [#251](https://github.com/brott-studio/battlebrotts-v2/pull/251) | `[S21.3-001] feat: arena onboarding HUD-element overlays (closes #245, refs #107)` | merged | 4 | +667 / −5 | 3 | 1× APPROVED (Boltz, review `4167305848`, squash-merged) |

Commits (4, pre-squash):
- `4c5e79c4` — `[S21.3-001] feat: arena onboarding HUD-element overlays (closes #245, refs #107)`
- `93ef4a53` — `[S21.3-001] fix: resolve GDScript type-inference parse errors in test file`
- `18aa4370` — `[S21.3-001] fix: guard get_viewport() null in _spawn_arena_first_encounter`
- `bb2bbdc8` — `[S21.3-001] fix: use Engine.get_main_loop() for FRS lookup when not in scene tree`

Squash SHA on main: `bdee0aab67acc111239b0edae8380cb1a5d3b3be`

---

## CI state on merge SHA

All required check-runs PASS on `bdee0aab`:

- `Godot Unit Tests` — success ✅
- `Playwright Smoke Tests` — success ✅
- `Post Optic Verified check-run` — success ✅
- `update` (Detect changed paths pipeline) — success ✅
- `Detect changed paths` — success ✅
- No failing checks; no skipped required checks.

Optic verification context (Sonnet 4.6, runtime 3m14s, tokens ~6.5k): PASS. 75/75 new-sprint tests, 43 sprint-test files all green, 72/72 inline core, 22/22 Playwright, combat sim clean. All 5 structural invariants spec-aligned. Zero regressions.

---

## Structural invariants — verification

S21.3's S21.2-corrective structural enforcement surfaces are evaluated here:

### 1. Optic anchor-target node-type assertions (required by plan §"Structural invariant enforcement")

Boltz review confirmed all 4 anchor-node assertions present in `test_s21_3_arena_onboarding.gd`:

| Key | Anchor node | Test function | Node-type assert | Negative asserts |
|-----|-------------|---------------|-----------------|-----------------|
| `energy_explainer` | `EnergyLegend` (Label) | `_test_anchor_node_type_energy_explainer` | `is Control` + `name == "EnergyLegend"` | `is CanvasLayer` = false, `is_class("Screen")` = false |
| `combatants_explainer` | `CombatantsPanel` / `PlayerInfo` | `_test_anchor_node_type_combatants_explainer` | `is Control` + HUD-panel name | `is CanvasLayer` = false |
| `time_explainer` | `time_label` (Label) | `_test_anchor_node_type_time_explainer` | `is Control` + `name == "TimeLabel"` | `is CanvasLayer` = false |
| `concede_explainer` | `ConcedeButton` (Button) | `_test_anchor_node_type_concede_explainer` | `is Control` + `name == "ConcedeButton"` | `is CanvasLayer` = false |

All 4 PASS. ✅

### 2. Boltz 6-item structural checklist (verbatim from plan)

Applied by review `4167305848`:

1. FE_COPY + ARENA_FE_COPY 4 keys in fixed order ✅
2. `anchor_target` resolves to HUD element nodes, not screen/CanvasLayer/viewport ✅
3. Arena-entry hook wired at per-match arena entry (not `_ready` / screen show/enter) ✅
4. Test file contains all 7 assertion classes (11 functions present) ✅
5. `energy_explainer` save key unchanged from S17.1-004 ✅
6. PR body "Invariants verified" section filled out with all 4 invariant checkboxes ticked + evidence ✅

6/6 PASS. No hard-reject conditions tripped. ✅

### 3. PR body "Invariants verified" template

Nutts used the verbatim template. All 4 structural invariant blocks ticked `[x]` with specific test-function evidence cited (anchor ×4, trigger, sequencing ×3, save-carryforward, placement, pointer, scope). ✅

---

## Divergences from plan

**None.** All 5 spec invariants (anchor, trigger, sequencing, save-carryforward, placement/pointer) implemented as designed. Gizmo's framing ratified by HCD 2026-04-24 00:40 UTC confirmed as-built. The 0.25× sim slowdown question HCD left to playtest is present in the implementation — the build includes it and HCD ratified "as is for now; playtest will reveal tuning."

---

## Process & pipeline notes

### Note 1 — Nutts spawn timeout at 1800s

Nutts (Sonnet 4.6) timed out at the 1800s ceiling during the build spawn. The build itself was substantively complete at timeout (all 11 test functions present on the PR, CI green on head `bb2bbdc8`). The timeout occurred mid-instruction-execution, not mid-implementation — the code and tests were done; Nutts was likely in a PR-body finalization step when the ceiling hit.

Operational consequence: The Bott (orchestrator) patched the PR body post-timeout to fix a literal `$PR_BODY` shell variable expansion bug from Nutts's heredoc. This is a clerical fix with no code change. CI remained green throughout.

Assessment: **runtime-harness signal, not a code-quality signal.** The pattern (Sonnet 4.6 on L-sized build task hitting 1800s ceiling) adds a data point to studio-framework#57 and to the `nutts-task-timeout-pattern` KB (S13.x–S14.x timeouts documented there used Opus 4.7; this is first observed on Sonnet 4.6). Carry-forward filed as new studio-framework issue (see §carry-forwards).

### Note 2 — Gizmo framing in orchestrator session (pre-Riv)

This sprint's Gizmo framing was done by The Bott orchestrator session at 00:16 UTC, not as a separate Gizmo spawn. HCD ratified framing 00:40 UTC. This is a valid pipeline variant for tight arc-intent scopes where the framing work is mechanically straightforward (arc-intent = `progressing`, primary issue closed as #245, fixed 4-key constraint). No process gap — the plan PR (#250, Ett, Opus 4.7) reflects the framing faithfully.

---

## openclaw tasks audit — S21.3 sprint window

`openclaw tasks audit` run at audit time: 113 findings (5 errors, 108 warnings). 

**Sprint-relevant findings:**
- `stale_running` (5 errors) — 5 tasks flagged as stuck at various ages (21h7m to 7d7h). Pre-existing pattern, not S21.3-introduced. Oldest are likely orphan subagent records from earlier arcs; a sentinel sweep cron (studio-framework#44) would clean these. No action required for this audit.
- `delivery_failed` (1 warning) — `8d71e55b` task delivered to succeeded but terminal update delivery failed. Pre-existing.
- `inconsistent_timestamps` (108 warnings) — `startedAt` earlier than `createdAt` for fresh tasks. This is a bulk pattern across the current session, consistent with harness-level clock skew or task registration race. Not sprint-specific. Pre-existing baseline.

No new task health regressions attributable to S21.3.

---

## Carry-forwards

- **`_resolve_energy_legend_node()` duplicate-synth fallback hardening** ([#252](https://github.com/brott-studio/battlebrotts-v2/issues/252)) — Boltz nit from review `4167305848`. The fallback synthesises a new `EnergyLegend` Label if node not found; current call order in `_create_arena_hud` prevents the scenario, but the fallback could orphan-synth a duplicate if call order changes. Not a merge blocker; candidate for hardening (assert-on-miss rather than synth). Low priority, area:game-code, prio:P3.
- **Nutts 1800s timeout on Sonnet 4.6 (L-size build task)** — S21.3 adds a Sonnet 4.6 data point to the timeout pattern documented in `docs/kb/nutts-task-timeout-pattern.md`. Prior data (S13.x–S14.x) was all Opus 4.7; this is first recorded on Sonnet 4.6. Suggests timeout pattern is model-agnostic on L-sized tasks. Filed as a comment / data point on [brott-studio/studio-framework#57](https://github.com/brott-studio/studio-framework/issues/57) (existing model-substitution tracker). No new issue — this is an addendum to #57.
- **#247** (Playwright overlay screenshot evidence) — existing, remains open. Optic verify on S21.3 ran clean; screenshot capture is not yet required by spec. This audit confirms #247 is still on the backlog but was not a S21.3 scope item.
- **#248** (test brittleness) — existing, remains open. Explicitly deferred per scope-discipline rule; this audit confirms scope discipline held.

Issues closed this sprint:
- **#245** — closed at PR #251 merge (`bdee0aab`). ✅

---

## Model substitution — observations

_(For studio-framework#57 data — HCD ruling 2026-04-23 22:49 UTC)_

| Agent | Model | Runtime | Tokens (approx) | Notes |
|-------|-------|---------|-----------------|-------|
| Gizmo | N/A (Bott-session framing) | ~15m (00:16→00:40 UTC ratification) | — | Not a separate spawn this arc loop |
| Ett | `github-copilot/claude-opus-4.7` | 18m 26s | ~71.2k (out-heavy) | Plan PR #250 landed cleanly |
| Boltz (plan review) | `github-copilot/claude-opus-4.7` | 1m 52s | ~6.0k | Fast, no issues |
| Nutts | `github-copilot/claude-sonnet-4.6` | 29m 58s | 0 reported (harness issue at timeout) | **Timed out at 1800s ceiling.** Work complete at timeout. PR body $-var bug patched by orchestrator. See Note 1. |
| Boltz (build review) | `github-copilot/claude-opus-4.7` | 2m 39s | ~10.0k | 6/6 checklist PASS, approved + squash-merged |
| Optic | `github-copilot/claude-sonnet-4.6` | 3m 14s | ~6.5k | PASS. 75/75 tests, zero regressions |
| Specc | `github-copilot/claude-sonnet-4.6` | this run | — | Audit |

**Observations for #57:**
1. Sonnet 4.6 on Optic (verification, read-heavy): clean, fast (3m14s), low tokens. Confirmed viable.
2. Sonnet 4.6 on Nutts (L-size build): **timed out at 1800s** despite completing the work. Prior timeout data (S13.x–S14.x) was on Opus 4.7 for similar reasons. Pattern is not model-specific — it's task-size-specific. The KB entry `docs/kb/nutts-task-timeout-pattern.md` should be updated with this Sonnet 4.6 data point (S21.3). Tokens reported as 0 at harness level on timeout — this is a known harness artifact, not a real usage figure.
3. Opus 4.7 on Ett + Boltz (plan/review roles): reliable, no anomalies. Out-heavy token profile on Ett (71.2k) consistent with plan-writing. Boltz token counts (6–10k) nominal for checklist review.

---

## 🎭 Role Performance

**Gizmo:** Shining: Framing was tight and correct — four fixed keys, anchor-target-as-invariant, arena-entry trigger. HCD ratification was fast (00:16 → 00:40 UTC, 24 min). The framing document anticipated exactly the spec gaps from S21.2 and stated them as structural invariants, not prose-only acceptance criteria. Struggling: Not a separate spawn this sprint — framing was done in-session by The Bott. This is operationally fine for tight scopes, but Gizmo's independent voice (separate spawn, separate reasoning) was absent; if a framing error had been made, there was no second-agent check. Trend: →.

**Ett:** Shining: Plan PR #250 was high quality — structural invariant enforcement surfaces (Optic test-shape spelled out, Boltz 6-item checklist verbatim, PR body template) were the direct corrective from S21.2 and they worked exactly as intended. Token profile (71.2k out-heavy) is expected for a plan of this enforcement depth; not a concern. Struggling: Nothing notable this sprint. Trend: ↑.

**Nutts:** Shining: The build itself is clean — 4 correct anchor nodes, arena-entry hook properly wired, all 7 assertion classes present, 3 post-initial fix commits show good debugging discipline (type-inference parse errors, null guard, FRS lookup in headless) rather than sloppy one-shot. Struggling: Timed out at 1800s ceiling. PR body `$PR_BODY` shell-var heredoc bug indicates end-of-spawn sloppy finalization under time pressure. Tokens reported as 0 at harness level — harness artifact, but signals the session died ungracefully. Trend: → (consistent with prior timeout pattern; build quality unaffected).

**Boltz:** Shining: First sprint applying the structural checklist surfaces from the S21.2-corrective — applied all 6 items verbatim, caught nothing (correctly, because Nutts implemented cleanly). The nit on `_resolve_energy_legend_node()` fallback is precisely the kind of low-noise, high-precision observation that characterizes a strong Boltz run. Squash-merge was correct. Struggling: Nothing substantive this sprint. Trend: ↑.

**Optic:** Shining: Clean PASS on a 75-test suite (11 new + 43 prior sprint files) in 3m14s on Sonnet 4.6. Zero regressions, combat sim clean, all invariants spec-aligned. Optic ran efficiently without events of note. Struggling: #247 (Playwright screenshot evidence) remains open and Optic did not produce screenshot-path evidence in the return payload this sprint — consistent with prior sprints, but the spec gap is unfixed. Trend: → (consistently reliable on pass/fail judgment; screenshot evidence gap is the standing limitation).

**Riv:** Shining: Orchestration of the full S21.3 arc loop (Gizmo framing → Ett plan → Nutts build → Boltz review → Optic verify → Specc audit) completed cleanly within the arc-loop contract. Nutts timeout was handled correctly — orchestrator patched PR body and pipeline continued without re-spin delay. Struggling: Nutts timeout required an orchestrator intervention (PR body `$PR_BODY` patch) that is technically outside Riv's normal role. This worked, but it means Riv absorbed a Nutts failure mode rather than respawning Nutts. Acceptable outcome; worth noting as a pattern if it recurs. Trend: →.

---

## Grade

**A−**

**Rationale:** This sprint delivered a spec-aligned, structurally-enforced implementation of the real #107 payload that S21.2 missed. All 5 HUD-element invariants (anchor, trigger, sequencing, save-carryforward, placement/pointer) implemented and verified. Boltz 6-item checklist 6/6. Optic 75/75. CI green. #245 closed cleanly. The S21.2-corrective structural enforcement surfaces (test-shape-in-plan, verbatim Boltz checklist, PR body template) all fired and caught nothing — which is the correct outcome, not a miss.

Grade held from A to A− by:
1. Nutts spawn timeout + PR body `$PR_BODY` bug (runtime harness signal; work landed clean but required orchestrator patch — one pipeline-cleanliness point).
2. `_resolve_energy_legend_node()` fallback nit (code quality signal, non-blocking, but a hardening item now in backlog).

Neither is a spec gap or a process failure. The sprint fully closes the S21.2 grade-drag.

**Scope streak:** 3 clean single-scope sub-sprints in Arc B. ✅

---

## Appendix A — Issue tracker hygiene

| Issue | Status | Action this sprint |
|-------|--------|--------------------|
| #245 | Closed ✅ | Closed at PR #251 merge |
| #107 | Open (parent, ongoing) | Refs'd in PR; partially closed by S21.3 (4 HUD elements now covered); parent remains open for arc completion |
| #247 | Open | No action; remains in backlog |
| #248 | Open | Explicitly deferred; scope discipline confirmed |
| [New: #252](https://github.com/brott-studio/battlebrotts-v2/issues/252) | Open | Filed this audit — `_resolve_energy_legend_node()` fallback hardening |

studio-framework#57 (model-substitution tracker): updated with S21.3 Sonnet 4.6 Nutts timeout data point (comment, no new issue).
