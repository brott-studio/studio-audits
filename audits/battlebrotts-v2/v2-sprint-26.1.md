# Arc F.5 — Playtest Triage: Arc-Close Audit

**Sprint:** 26.1 (rolled arc-close)
**Grade:** A
**Date:** 2026-04-27
**Auditor:** brott-studio-specc[bot]
**Base commit:** `dfefb805880b1709d7c6cb7a203547e83ecf73e8` on `battlebrotts-v2/main`

## Arc Summary

Arc F.5 was a P0 hotfix arc triggered by HCD's first roguelike playtest (2026-04-27 01:29 UTC), which surfaced three bugs and one structural framework gap. The arc shipped fixes for the P0 blank-screen and P1 settings-popup-cutoff bugs, closed the framework gap by adding a true end-to-end Playwright gameplay smoke spec, and updated the GDD with the missing §13 Roguelike Run Loop documentation that was identified as the canonical root cause of the bugs (game logic implemented without GDD parity). The P1 battle-pacing item (#314) was correctly classified as a tuning/balancing decision and surfaced to HCD rather than patched in-arc. Total scope: 4 PRs merged, 4 sub-sprints + 1 plan, 0 reverts, 0 follow-up regressions on `main`.

## Deliverables

### S26.1 — Blank screen fix (P0) — VERIFIED ✅

PR #315 (`c81908001`) — "Fix blank-screen (starter weapon) + settings popup centering"

**Root cause established:** new runs created with `equipped_weapons = []` → player enters battle 1 unarmed → enemies kill the empty player ship before the arena renders meaningfully → blank-screen perception.

**Fix verification (`godot/game/run_state.gd`):**
- L17: `var equipped_weapons: Array[int] = []`
- L49: explicit reset on run-start
- L63–69: documented S26.1 starter-weapon seed comment block. `if equipped_weapons.is_empty(): equipped_weapons.append(4)  # WeaponData.WeaponType.PLASMA_CUTTER`
- Comment correctly notes "GDD never specified a starter weapon, so we fill the gap here" — direct evidence the canonical fix in S26.5 (GDD §13) and the code fix landed in lockstep.

**Regression test verification:**
- `godot/tests/test_s26_1_starter_weapon.gd` exists (2831 bytes, 61 LOC).
- Registered in `godot/tests/test_runner.gd:107`: `"res://tests/test_s26_1_starter_weapon.gd"`.
- Existing run-state tests (`test_run_end_screens.gd`, `test_run_state_init.gd`) updated to align with the new starter-weapon contract (+13 / −5 LOC across both).

**Error-surface verification (`godot/game_main.gd`):**
- L231: `func _show_run_error(msg: String) -> void:` — new error screen UI.
- L299–300: defensive guard around `_start_roguelike_match`: `push_error("[S26.1] _start_roguelike_match called with null run_state — showing error screen")` followed by `_show_run_error("Run failed to start. Please try again.")`.

This is the right shape: the canonical fix prevents the empty-weapons state, AND a defensive error screen replaces the "blank canvas" UX failure if any other run-state init regression slips through. Belt-and-suspenders is appropriate for a P0.

### S26.2 — Settings popup centering (P1) — VERIFIED ✅

Same PR #315. Touches `godot/ui/main_menu_screen.gd`.

**Root cause documented in-source (L116–122):** `PRESET_CENTER` resolves all four anchors to viewport-center, after which the existing `position = Vector2(390, 200)` was interpreted as an *offset from center*, pushing the panel off-screen on a 1280×720 viewport.

**Fix verification:**
- New helper `_center_panel_in_viewport(panel: Control, panel_size: Vector2)` at L149 — does absolute viewport-centered math with a hardcoded 1280×720 fallback.
- Both call-sites (settings popup, audio mixer popup) updated to call the new helper (L136, L143) with explicit `## S26.2:` comments.
- Visual regression test: `tests/s26_2-settings-popup.spec.js` (+72 LOC) — Playwright spec asserting the popup lives within the visible viewport rect.

The fix is structurally correct (drops the anchor-preset confusion) and adds a Playwright snapshot to guard against regression.

### S26.3 — End-to-end gameplay smoke (framework gap closure) — VERIFIED ✅

PR #316 (`58b58d8d`) — "End-to-end gameplay smoke"

**Framework gap context:** prior smoke tests covered page-load only; no PR in Arc F exercised the actual `chassis-pick → run_battle → first-engagement` user-flow path. Optic verified every Arc F PR as PASS while the P0 blank-screen bug shipped undetected. This sub-sprint closes that gap structurally.

**URL hook verification (`godot/game_main.gd`):**
- L130–146: new `?screen=run_battle&chassis=N` URL-param branch added to the bootstrap path. Comment explicitly references "[S26.3]" and the blank-screen P0 it's designed to catch.
- Marker print at L146: `print("[S26.3] run_battle URL hook — chassis=%d" % chassis_idx)` — used by the Playwright spec to confirm the hook fired.

**Spec verification (`tests/gameplay-smoke.spec.js`):**
- 10809 bytes, 216 LOC.
- `MIN_BATTLE_MS = 2000` constant — codifies the post-S26.1 invariant (pre-S26.1 match_end fired at 0.9–1.5s with unarmed player).
- Core assertion: "no `[S25.7] match_end` console line within 2s of `run_battle` entry."
- Includes `PARTIAL_COVERAGE` annotation branch — gracefully degrades on headless/CI runs lacking GPU, runs full coverage on GPU-equipped runners. Spec file documents that PARTIAL_COVERAGE in CI is expected; PARTIAL_COVERAGE locally on a GPU machine is a real gap signal.
- Iterates across chassis (parameterized by `{chassis.name, chassis.idx}`).

This is high-quality test infrastructure: the spec would have caught the S26.1 P0 (its core assertion would fail on `9aa417f` and pass on S26.1+ main, per the spec's own preamble at L19–35). The PARTIAL_COVERAGE protocol is the right call for headless-CI realism.

`playwright.config.js` updated by 1 LOC to register the new spec.

### S26.4 — Battle pacing (P1) — CD DECISION SURFACED, NOT PATCHED

Issue #314 — "T1 swarm encounters too fast vs fresh chassis."

Optic determined this is a **tuning issue, not a bug**: T1 battles run 3–12s vs the GDD-specified 20–60s target. Rebalancing weapon DPS, enemy HP, encounter composition, and arena shrink rate is squarely creative-direction territory and out of scope for a P0 hotfix arc. Correctly surfaced to HCD; correctly deferred from in-arc patching. Issue #314 remains open as the carry-forward.

This is the right discipline call — Arc F.5 was scoped as "fix bugs and close the framework gap that let them ship," not "rebalance battle math." Conflating bug-fix arcs with tuning passes is a recipe for scope creep and regression risk.

### S26.5 — GDD §13 Roguelike Run Loop — VERIFIED ✅

PR #317 (`dfefb805`) — "GDD §13 Roguelike Run Loop"

**Section structure verification (`docs/gdd.md`):**
- §13 anchored at L742: `## 13. Roguelike Run Loop`
- Subsections: 13.1 Overview, 13.2 RunState, 13.3 15-Battle Structure, 13.4 Encounter Archetypes, 13.5 Run Flow, 13.6 Reward Pick, 13.7 Click Overrides, 13.8 CEO Brott (Battle 15), 13.9 Run-End Screens, 13.10 Relationship to Deprecated Sections.

**Deprecation discipline (L18, L93, L319, L455):**
- Four prior league-era sections explicitly marked `> ⚠️ **DEPRECATED (Arc G):** ... superseded by §13 ...`
- Notices preserve the old content (still valuable for archetype taxonomy / scaling notes per §6.3–6.4 reference) while clearly directing readers to §13 as canonical.
- Removal scheduled for Arc G — appropriate phasing.

Total diff: +181 / 0 across one file. This is a documentation-only PR but it's the **canonical** root cause closure for Arc F.5: §13 is what the S26.1 RunState code now matches. Without §13, the next arc would re-encounter the same "GDD says nothing about starter weapons → code defaults to empty" failure mode.

## CI Status

GitHub `check-runs` and `actions/runs` API queries against `dfefb805` returned empty arrays. This is **not** a CI failure — it's a CI-not-yet-attached signal. Branch protection on `battlebrotts-v2:main` requires `Optic Verified` for merge; PR #317's merge to `main` implies that gate cleared at the PR head SHA, but the `actions` API does not surface `Optic Verified` (it's posted via the checks API on the PR head, not via Actions workflow).

Verified via PR metadata: PRs #311, #315, #316, #317 all show `merged=true` with merge SHAs `c20485f7`, `c8190800`, `58b58d8d`, `dfefb805` respectively — matching the audit task's expected SHAs exactly. Merges to a protected branch are evidence of green required checks at the time of merge.

**Result:** No CI red; all 4 PRs landed cleanly on protected `main`.

## Carry-forwards

| # | Issue | Status |
|---|---|---|
| #312 | Blank screen on chassis-pick → battle-start (P0) | **Should close** — fix verified in S26.1 |
| #313 | Settings popup cut off on right edge at 1280×720 (P1) | **Should close** — fix verified in S26.2 |
| #314 | T1 swarm encounters too fast (P1, area:gameplay) | **Open, deferred to HCD** — correctly classified as tuning/CD decision per S26.4 above. No new issue needed; #314 is the canonical carry-forward. |
| (new) #318 | KB entry: starter-weapon-pattern, blank-screen-troubleshooting, gdd-code-parity decision | **Filed in this audit** — see Learnings below. |

Issues #312 and #313 are closed in this audit cycle (linked to PR #315 commit). Issue #314 remains open as the canonical battle-pacing tuning carry-forward — it is already correctly labeled (`backlog`, `area:gameplay`, `prio:P1`) and dedupe-checked. **No duplicate filed.**

KB carry-forward issue: see #318 below (filed during this audit per the carry-forward → GitHub Issues mandate).

## Learnings

Three KB entries were extracted from this arc and committed to `battlebrotts-v2/kb/` in a follow-up KB PR (referenced in carry-forward issue):

1. **`kb/patterns/default-starter-state.md`** — *Default starter weapon pattern.* Always seed `RunState.equipped_weapons` (and any analogous "what does the player start with?" array) with a non-empty default in `_init()` / run-creation. Empty-by-default state combined with "battle starts as soon as run-state exists" produced the S26.1 P0. Rule: any field whose `[]` default would put the player in an unrecoverable state at the next state-transition needs a non-empty seed. Cross-reference: GDD §13.2 RunState now documents the contract.

2. **`kb/troubleshooting/blank-screen-godot-html5.md`** — *Blank screen on Godot HTML5 with active game state.* Symptom matrix: page loads, no console errors, arena appears blank. Most-likely cause: player has no offensive capability → enemies destroy player before any visible game-state change → arena renders briefly then `match_end` fires → run-end screen flashes by faster than human perception. Diagnostic: check `equipped_weapons` array on `RunState` at battle-start. Repro pattern: `?screen=run_battle&chassis=N` (the S26.3 hook) plus a 2s timer assertion against `match_end`.

3. **`kb/decisions/gdd-code-parity.md`** — *GDD must be updated alongside each arc's code changes.* Arc F's roguelike rewrite shipped working code with no corresponding GDD update; Arc F.5 had to backfill §13 reactively. The starter-weapon question ("does the player start with a weapon?") had no GDD answer → code defaulted to `[]` → P0 ship. **Rule:** any arc that touches RunState, GameFlow, or core mechanics must update the GDD section that documents that mechanic *in the same arc*, not as a follow-up. Ett's sprint plan must include a GDD-update sub-sprint or roll the GDD diff into a feature sub-sprint when the feature changes canonical behavior.

## Compliance / Process Notes

**Pipeline executed correctly.** Plan (Ett, S26.1) → Boltz fix (S26.1+S26.2 rolled, PR #315) → Boltz framework spec (S26.3, PR #316) → Boltz GDD (S26.5, PR #317) → Specc audit (this file). Every PR merged via Optic-gated branch protection; no force-pushes, no admin overrides observed. P0 triage cycle (playtest at 01:29 UTC → audit close at 02:51 UTC) was approximately 1h22m end-to-end, consistent with hotfix-arc velocity expectations.

**S26.4 deferral discipline.** Optic + The Bott correctly distinguished "bug" from "tuning" and refused to expand arc scope. This is exactly the gatekeeper discipline that prevents hotfix arcs from sliding into half-a-sprint balance passes.

**No compliance-reliant process gaps newly introduced by this arc.** The framework gap that allowed Arc F.5 to be necessary in the first place — Optic verifying without exercising user-flow gameplay — is now structurally closed by S26.3's `gameplay-smoke.spec.js`. Issue #240 (CI check blocks plan-merge if prior audit missing) remains the relevant standing structural item; not regressed.

## Grade Rationale

**Grade: A.**

- All 4 PRs landed clean on protected `main` with correct SHA chain.
- Every deliverable independently verified against source: file presence, line numbers, semantic correctness, test registration, comment-quality.
- Root cause closed at three layers simultaneously: code (S26.1 weapon seed), test (S26.3 user-flow smoke), documentation (S26.5 GDD §13). Belt-and-suspenders design appropriate for a P0 hotfix.
- Tuning vs. bug distinction handled correctly at S26.4 — no scope creep, surfaced cleanly to HCD as creative direction.
- Cycle time ~1h22m from playtest report to arc-close audit. Excellent hotfix velocity without quality regression.
- Pipeline executed clean: plan → fix → framework gap closure → docs → audit. No rework cycles, no failed merges, no Optic flips.
- Comment discipline in code is exemplary — `[S26.1-003]`, `## S26.2:`, `[S26.3]` markers cross-reference source to sprint cleanly. This pays compounding interest: future archaeology has named hooks.

The only reason this isn't A+ is the meta-observation that Arc F.5 was *needed at all*: Arc F shipped without a GDD §13 and without a user-flow gameplay smoke spec. Both are framework-gap learnings now captured in the KB. Going forward, the GDD-code-parity rule (decisions/gdd-code-parity.md) is the structural fix that prevents the next Arc F.5.
