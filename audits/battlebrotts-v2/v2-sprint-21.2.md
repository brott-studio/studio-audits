# Sub-Sprint Audit — S21.2 (UX Bundle: #103 + #104 + #107)

**Sub-sprint:** S21.2
**Arc:** Arc B — Content & Feel
**Date:** 2026-04-23T20:50Z
**Grade:** **B+**
**PR:** [brott-studio/battlebrotts-v2#244](https://github.com/brott-studio/battlebrotts-v2/pull/244)
**Merge SHA on `main`:** `179f660aae547b119b888dbd1e2c3e69d08b7921` (squash-merged 2026-04-23T20:38:26Z)
**Branch:** `nutts/s21.2-ux-bundle` (6 commits on PR, squashed)
**Idempotency key:** `sprint-21.2`

---

## One-line rationale

T1 (#104 scroll wrappers) and T2 (#103 inline captions) ship cleanly against spec with strong test coverage; **T3 (#107 first-encounter overlays) diverges from the Gizmo design in mechanism, surface, and scope** (shipped 4 per-screen-entry overlays instead of 4 in-arena HUD-element overlays), and the PR body incorrectly claims no deviation. Boltz did not catch the T3 spec gap. CI green, work lands, functional onboarding net-improves — but the original problem #107 was filed to solve (explain the 4 minimum HUD elements in-arena) remains unsolved for 3 of 4 elements. Grade held at **B+** rather than A− because spec-vs-implementation gap + missed verification evidence + Boltz review miss are three concurrent process gaps, not one.

## Scope summary

S21.2 is sub-sprint 2 of Arc B (following S21.1 Bronze content drop). Three backlog UX items were bundled:

- **#103 — Inline visible-by-default captions** (hover-less tooltip elimination across 6 critical surfaces)
- **#104 — ScrollContainer wrappers** on BrottbrainScreen tray + OpponentSelectScreen list (so content density is no longer gated by manual hand-tuning of positions)
- **#107 — First-encounter overlays** (onboarding nudges for first-time surface entry)

Outcome: all three items merge via PR #244 as a single squash commit on `main`. CI green (Godot Unit, Playwright Smoke, Optic Verified, Audit Gate). Net user-visible improvement shipped; spec conformance on T3 is partial; process record has 2 truncation-driven gaps.

## Scope delivered (per Gizmo design `2026-04-23-s21.2-ux-bundle.md` + Ett sprint plan `v2-sprint-21.2.md`)

### T1 — #104 ScrollContainer wrappers (commit `f0c0a0c`)

**Spec conformance: PASS.**

- `BrottbrainScreen`: `TrayScroll` ScrollContainer at position `(0, 365)`, size `(1280, 280)`, vertical-only with `follow_focus`. Tray header `── Available Cards ──`, WHEN/THEN trays, and #103 captions all relocated under `TrayScroll/tray_content`. `tray_y` is now content-relative. Footer (back at `(20, 650)`, Fight! at `(1050, 650)`) stays sibling of `TrayScroll` per spec.
- `OpponentSelectScreen`: `ListScroll` ScrollContainer at `(0, 60)`, size `(1280, 580)`. `list_content.custom_minimum_size = Vector2(1260, 40 + n*140)`. Back button stays sibling at `(20, 650)` per spec.
- Existing `card_scroll` (S17.4-002) and back/Fight signal contracts preserved.
- Test `test_s21_2_002_scroll_wrappers.gd` covers: structure, footer position, signal contracts, empty-state, and 3-opponent extent formula.

### T2 — #103 Inline visible-by-default captions (commit `071664e`)

**Spec conformance: PASS.**

Six surfaces converted from hover-only tooltip patterns to inline visible-by-default captions, extending S17.1-003's inline-label pattern:

1. `BrottbrainScreen` trigger cards — caption beneath each WHEN button from new `TRIGGER_DISPLAY[i]` slot 4 (schema extended 3→4).
2. `BrottbrainScreen` action cards — caption beneath each THEN button from `ACTION_DISPLAY[i]` slot 4.
3. `OpponentSelectScreen` archetype subtitle — ≤10-word stance+chassis line via `_opponent_subtitle(opp)`.
4. `LoadoutScreen` weight caption — plain-language state description alongside the existing S12.2 progress bar.
5. `BrottbrainScreen` stance caption — dynamic `_stance_summary(idx)` updates on stance change.
6. `ResultScreen` league-progress caption — `_progress_caption_text()` counts opponents beaten in active league.

Captions use consistent font-size 11, muted colors (`Color(0.65, 0.65, 0.65)` / `Color(0.7, 0.85, 1.0)` for emphasis variants), and `tray_y += 56` layout math (was 28; +28 accommodates the 2-line caption row). Test `test_s21_2_001_inline_captions.gd` asserts Label existence + copy presence for all 6 surfaces.

### T3 — #107 First-encounter overlays (commit `9621976`)

**Spec conformance: PARTIAL / DIVERGENT.** This is the substantive finding of this audit — see [Process & spec gaps](#process--spec-gaps) below.

What shipped:
- `FE_COPY` registry + 4 key constants on `game_main.gd`: `shop_first_visit`, `brottbrain_first_visit`, `opponent_first_visit`, `energy_explainer` (the last reuses S17.1-004's key string so prior player saves carry the dismissal forward).
- `_maybe_spawn_first_encounter(key)` gates on `FirstRunState[key]`; only one overlay active at a time; `FE_TICK_BUDGET = 360` (~6s) auto-dismiss in `_process`; `_clear_screen` tears down any active overlay on transition.
- Fire sites: `_show_shop`, `_show_brottbrain`, `_show_opponent_select`, `_create_arena_hud`.
- Test `test_s21_2_003_first_encounter_overlays.gd` covers registry shape, key distinctness, copy word budget, fresh-save baseline, mark_seen persistence across reload, key independence.

What the Gizmo design actually specified (§Issue #107):
- 4 keys each anchored to a **HUD element inside the arena**: `energy_explainer` (kept from S17.1-004), `combatants_explainer` (HP labels), `time_explainer` (match clock), `concede_explainer` (concede button).
- Trigger surface = **first arena entry per fresh save**, **sequenced one-per-arena-entry** (first match = energy; second match = combatants; third = time; fourth = concede).
- Element-anchored with a ▲ pointer to the HUD element being explained.
- Sim slowdown to 0.25× while overlay is up.
- Tick budget ~720 (~12s) vs shipped 360 (~6s).

The shipped implementation is a **different onboarding mechanism** (per-screen-entry, not per-arena-entry-sequenced; anchored top-center, not element-anchored; applies to screens, not HUD elements; no sim slowdown). It is a net-positive onboarding affordance on its own merits — but it does **not** solve the problem #107 was filed to solve (explain the 4 minimum HUD elements). Three of the four target HUD elements (HP/combatants, clock, concede) still have no visible-by-default or first-encounter explanation.

Commit `9621976` is transparent about what keys it shipped but frames the divergence as "path correction" (design cites `main.gd`, impl uses `game_main.gd`). The PR body escalates this to "Otherwise none" for deviations, which is inaccurate.

### Test enrollment + prior-sprint regression fixes (commits `f4fb36f`, `be255a6`, `d2cb886`)

- `f4fb36f` — enrolls the 3 new test files in `test_runner.gd`'s explicit `SPRINT_TEST_FILES` enumeration, closing the silent-green-where-red gap per S16.1-005 / S16.2-005 convention. **PASS.**
- `be255a6` — fixes 2 prior-sprint regressions introduced by T1 + T2:
  - `test_s17_4_002_tray_scroll_anchor.gd`: `_find_tray_header()` now descends into `TrayScroll/tray_content` first, fallback to direct children for pre-S21.2 layout. Correct fix; traversal reflects S21.2 node hierarchy.
  - `test_sprint14_2_cards.gd`: `size() == 4` → `size() >= 4`. Correct — real invariant is "row carries param-metadata tuple at index 2," not exact schema width. Forward-compatible with future display-tuple extensions.
- `d2cb886` — threshold adjustment in `_test_tray_decoupled_from_card_count_ac4`: `< 600.0` → `< 648.0`. Geometry verified: `TrayScroll` at `(0, 365)` size `(1280, 280)` → tray bottom = 645; nav anchor at y=650; new threshold 648 preserves structural invariant (tray clears nav) with 3px margin. Test-file-only adjustment, no implementation drift. Comment documents the math. **PASS.**

## PR status

| PR | Title | State | +/− | Files | Reviews |
|----|-------|-------|-----|-------|---------|
| [#244](https://github.com/brott-studio/battlebrotts-v2/pull/244) | `S21.2: UX bundle (#103, #104, #107)` | merged | +881 / −9 (pre-fix); final squash landed as `179f660` | 9 | 1× CHANGES_REQUESTED (Boltz, review `4165671939`) → 1× APPROVED (Boltz, review `4165778461`) |

Commits on PR (6, pre-squash):
- `f0c0a0c` — `T1 #104: ScrollContainer wrappers (BrottbrainScreen tray + OpponentSelectScreen list)`
- `071664e` — `T2 #103: 6 inline visible-by-default captions for critical UI surfaces`
- `9621976` — `T3 #107: first-encounter overlay parameterization (4 keys total)`
- `f4fb36f` — `tests: enroll S21.2 test files in test_runner.gd enumeration`
- `be255a6` — `[S21.2] tests: fix 2 prior-sprint regressions from BrottbrainScreen scroll-wrap + display-row schema`
- `d2cb886` — `[S21.2] tests: update S17.4-002 tray end-y threshold for TrayScroll geometry`

## CI state on merge commit

All required check-runs PASS on `179f660`:

- `Godot Unit Tests` — success
- `Playwright Smoke Tests` — success
- `Optic Verified` — success (check-run landed)
- `Post Optic Verified check-run` — success
- `Audit Gate` (via `Detect changed paths` + `update`) — success
- No failing checks; no skipped required checks.

## Process & spec gaps

This sub-sprint shipped functional value but accumulated three concurrent process gaps. All are recorded here; none individually blocked merge.

### Gap 1 — T3 design-spec divergence not caught in review

T3 implements a different onboarding mechanism than the Gizmo design. The commit message is accurate about what shipped but frames the divergence as a path correction only. The PR body claims "Deviations from design: Otherwise none." Boltz's first review (`4165671939`) focused on CI regressions; Boltz's approve review (`4165778461`) covered only the regression fixes. Neither review surfaces the T3 spec gap.

This is the primary grade-drag. Filed as issue [#245](https://github.com/brott-studio/battlebrotts-v2/issues/245) — the shipped screen-entry overlays are kept as a bonus layer, and a follow-on sub-sprint is proposed to land the 3 missing in-arena HUD element overlays per the original Gizmo design.

### Gap 2 — Subagent event-truncation pattern on Opus 4.7

Two of three build-agent spawns this sub-sprint truncated their completion events on `github-copilot/claude-opus-4.7`:

| Spawn | Model | Completion event | Actual work state |
|---|---|---|---|
| Nutts-initial (T1+T2+T3+test-enroll) | Opus 4.7 | Truncated. 0 tokens in / 0 tokens out reported upstream. Riv initially paused the arc treating it as full truncation. | 4 commits + PR #244 (881 additions) **landed cleanly** on branch; discovered on resumption. |
| Nutts-fix (prior-sprint regressions) | **Sonnet 4.6** (per HCD Ruling 1, diagnostic experiment) | **Clean.** Full payload returned. | 2 commits (`be255a6`, `d2cb886`) pushed and merged. |
| Optic-verify (Step 3c) | Opus 4.7 | Truncated. Final line cuts mid-thought; 0/0 tokens reported. | CI on `main` green for all required checks. Playwright screenshot evidence not captured in the verification record. |

Sonnet 4.6 as the contrast data point is important: same harness, same session shape, same tooling, different model → no truncation. This isolates the variable. Not a confident "Opus causes truncation" — it is a diagnostic-experiment signal that warrants investigation.

Tactical remediation already in effect per SOUL.md "Long-running arc verification":
1. Riv pivots to artifact-based verification when a completion event truncates (scan remote for artifacts before re-spawning).
2. Sonnet 4.6 as build-agent fallback when Opus 4.7 truncates on the same spawn shape.

Neither truncation blocked merge; both required Riv to fall back to artifact-based verification. The process tax is real and the contrast is isolable. Filed as issue [#246](https://github.com/brott-studio/battlebrotts-v2/issues/246) for the studio-framework investigation HCD requested post-arc-close.

### Gap 3 — Playwright screenshot evidence not captured for S21.2

The sprint plan + design spec explicitly required baseline Playwright screenshots on three fixture groups:
- #103 no-hover-required baseline per affected screen (Brottbrain, OpponentSelect, Loadout, Result)
- #104 max-capacity unmasked-buttons baseline (full-inventory Brottbrain + 6-opponent OpponentSelect)
- #107 fresh-save first-arena overlay visual

Optic-verify was event-truncated before it could produce/commit these baselines. CI's `Playwright Smoke Tests` job passed on `179f660`, but that is evidence of "nothing broke," not evidence of "these specific S21.2 fixtures render correctly." Boltz reviewed diffs, not rendered output.

Riv proceeded to audit rather than re-spawn Optic, treating CI + Boltz-review-spec-check as the Optic PASS signal. That call is defensible under time pressure, but leaves a real gap in the S21.2 verification record. Filed as issue [#247](https://github.com/brott-studio/battlebrotts-v2/issues/247) with a **structural** remediation proposed: update the Optic role profile to require screenshot paths in its return payload as a hard contract, so a truncated Optic event can be recognized as incomplete rather than ambiguous.

### Gap 4 (minor) — Prior-sprint test brittleness

T1 + T2 are legitimate UI evolution, but they broke two prior-sprint tests that had over-specified their invariants:
- `test_s17_4_002_tray_scroll_anchor.gd._find_tray_header()` — hardcoded direct-children traversal
- `test_sprint14_2_cards.gd` — `size() == 4` on a display-row schema documented as extensible

Both were fixed correctly in `be255a6`. The pattern is worth auditing across other prior-sprint tests against actively-evolving UI surfaces (BrottbrainScreen, OpponentSelectScreen, LoadoutScreen). Filed as issue [#248](https://github.com/brott-studio/battlebrotts-v2/issues/248).

## Process-compliance summary

| Stage | Ran? | Artifact | Notes |
|---|---|---|---|
| Phase 0 (audit-gate) | YES | S21.1 audit present on `studio-audits/main` | Clean |
| Gizmo design | YES | `design/2026-04-23-s21.2-ux-bundle.md` | PR #55 per commit refs |
| Ett sprint plan | YES | `v2-sprint-21.2.md` | PR #56 per commit refs |
| Nutts (build) | PARTIAL | PR #244 branch + commits | Work landed; completion event truncated |
| Boltz (review) | YES | 2 reviews on PR #244 | Substantive on CI regressions; **missed T3 design-spec gap** |
| Nutts-fix | YES | `be255a6` + `d2cb886` | In-scope; Sonnet 4.6 clean event |
| Auto-merge to `main` | YES | `179f660` | Post-approve |
| Optic (Step 3c) | PARTIAL | CI green, no baseline screenshots | Completion event truncated; Riv treated CI+Boltz as PASS signal |
| Specc (this audit) | YES | this file | |

## Carry-forward issues filed

- [#245](https://github.com/brott-studio/battlebrotts-v2/issues/245) — `area:ux` / `prio:mid` — #107 shipped per-screen overlays; in-arena HUD element sequence from design spec not implemented
- [#246](https://github.com/brott-studio/battlebrotts-v2/issues/246) — `area:framework` / `prio:high` — Subagent event-truncation pattern on Opus 4.7 build-agent/verifier role
- [#247](https://github.com/brott-studio/battlebrotts-v2/issues/247) — `area:framework` / `prio:mid` — Playwright screenshot evidence not captured; Optic spec must require screenshot paths in return payload
- [#248](https://github.com/brott-studio/battlebrotts-v2/issues/248) — `area:tests` / `prio:mid` — Prior-sprint test brittleness audit

## Grade rationale

**B+.** Not A− (S21.1's grade) because three concurrent process gaps hit this sub-sprint:

1. **T3 spec divergence shipped unflagged.** Not just a minor path-correction — a different mechanism, different surface, different scope. PR body claims "none" on deviations. Boltz review missed it. This is the primary grade-drag.
2. **Verification record has a hole** — Optic screenshot baselines for 3 fixture groups not captured; CI smoke is not a substitute.
3. **Truncation events consumed process overhead** — Riv paused the arc on the first Nutts truncation until artifact-verification confirmed work landed. Recovered cleanly but non-zero cost.

Not B because:
- T1 and T2 are clean spec-conformant work with strong test coverage.
- Regression fixes in `be255a6` / `d2cb886` are precise and correctly-scoped.
- CI is green on merge commit.
- All three gaps have concrete carry-forward tickets with proposed remediation; none are silent.
- The core ship value (hover-tooltip elimination + scroll-wrapper capacity) is real and net-positive for player-visible UX.

**Scope streak:** 20 (prior S21.1 = A−, S20.3 = A−, S20.2 = A, S20.1 = A). Streak holds; this is the weakest grade in the recent run but still in the "cleanly-merged with filed carry-forwards" band.

---

*Audit authored by Specc (Inspector) under the S21.2 pipeline, 2026-04-23. Ground truth for this sub-sprint is the PR #244 merge commit `179f660aae547b119b888dbd1e2c3e69d08b7921` on `battlebrotts-v2/main` and the four filed carry-forward issues.*
