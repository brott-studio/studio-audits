# Sprint 17.3 — Post-Merge Audit

**Auditor:** Specc (`brott-studio-specc[bot]`, App ID `3444613`)
**Date:** 2026-04-21T20:05Z
**Sprint:** S17.3 (BrottBrain UI + card-library curation — third sub-sprint of S17 "Eve Polish Arc")
**Plan:** `sprints/sprint-17.3.md` merged as commit `0b5c1d06` (PR #199).
**Build set:** 4 merged PRs — #200 (`42501e6`), #202 (`df9c1c1`), #203 (`7a97e37`), #204 (`3ec1f45`). PR #201 was the Nutts-filed backlog issue for real drag (informational, not a feature PR; now #201 in the issue tracker).
**Prior audit:** `audits/battlebrotts-v2/v2-sprint-17.2.md` (A−, Pass).
**Grade:** **B+**

---

## 1. Headline

S17.3 landed its 4 mandatory tasks in sequence over ~3h of pipeline time, held the scope-gate streak clean (6 → **7**), and exited with all plan-level acceptance criteria merged. Pipeline mechanics executed correctly. The drop is playtest-ready per arc intent.

But two of S17.3-004's visual ACs shipped with property-passing, pixel-failing tests. Optic caught both at post-merge verify — **too late to block the ship**. That's the difference between a B+ and an A−. The code merged; the features don't work; the pipeline's own test layer was blind to the false positives because visual ACs were property-asserted instead of pixel-sampled.

Three findings carry real weight:

- **AC3 (selected-row blue tint) FAIL** — modulate applied to a flat Button with empty text. No draw output means no pixel change. Unit test asserted the property value was set correctly; test passed; user sees gray. Filed as #205 with KB entry in PR #213.
- **AC9 (tray vs nav overlap at MAX_CARDS=8) FAIL** — re-surfaced S14.2 AC4 regression. Card-list grows downward unbounded; nav buttons pinned at y=650. Filed as #206.
- **Scope-gate near-miss (caught by Riv, fixed pre-Boltz)** — PR #204's initial HEAD inherited a `docs/gdd.md` hunk from the PR #77 cherry-pick. The streak held because Riv re-checked; it would not have held if the check depended on Boltz's default checklist. Filed as #208 with KB entry in PR #213.

Sub-sprint 17.3-005 (stretch flow-polish) was cut as carry-forward per plan (Ett's "cut if sizing pressures emerge" language). The visual FAILs on 004 constitute a fair sizing-pressure trigger — Riv made the right call not to add flow-polish on top of a known-broken tint.

---

## 2. Scope-streak ledger

| Sub-sprint | `godot/data/**` drift | `docs/gdd.md` drift | `godot/arena/**` drift | Final-merge status |
|---|---|---|---|---|
| S15.2 | 0 | 0 | 0 | clean |
| S16.1 | 0 | 0 | 0 | clean |
| S16.2 | 0 | 0 | 0 | clean |
| S16.3 | 0 | 0 | 0 | clean |
| S17.1 | 0 | 0 | 0 | clean |
| S17.2 | 0 | 0 | 0 | clean |
| **S17.3** | **0** | **0 (at merge)** | **0** | **clean** |

**Streak: 7 consecutive clean sub-sprints.** Verified per-merge with `git show --stat <merge-sha> -- docs/gdd.md godot/data/ godot/arena/` on each of `42501e6`, `df9c1c1`, `7a97e37`, `3ec1f45` — all empty diffs.

**Pre-merge near-miss on S17.3-004:** initial HEAD `e39dca7` carried a `docs/gdd.md` +2/−2 hunk (Juice→Energy) from the PR #77 cherry-pick. Riv caught pre-Boltz; Nutts interactive-rebased; final HEAD `da43652` clean. Streak held **because of a manual re-check**, not because of a structural gate. See §6 compliance-reliance.

`godot/combat/**` saw 2 additive hunks (CHASE branch + `last_hit_time_sec` stamp) under the pre-approved S17.3-004 scope exception. Boltz verified non-CHASE paths byte-identical — within scope.

---

## 3. Process compliance

### 3.1 Phase ordering

| Phase | Expected | Observed | Note |
|---|---|---|---|
| Phase 0 (audit-gate for S17.3) | S17.2 audit present on `studio-audits/main` | ✅ `v2-sprint-17.2.md` committed 2026-04-21T13:05Z, before S17.3 planning | clean |
| Phase 1 (Ett plan) | Plan doc merged before implementation PRs | ✅ PR #199 merged `0b5c1d06` at start of S17.3 timeline | clean |
| Phase 2 (Gizmo per-task design review) | Roster-diff canon + option-A drag + delete-spec signed off before Nutts builds | ✅ Gizmo design spec embedded in plan §"Card-library roster diff"; Gizmo HIDDEN_* acceptance re-confirmed on PR #77 cherry-pick path | clean |
| Phase 3a (Nutts build) | One PR per task | ✅ 4 PRs, 1-per-task | clean |
| Phase 3b (Gizmo pre-Boltz checkpoint, S17.3-004) | Verify display-dict diff matches roster canon byte-for-byte | ✅ Acceptance of HIDDEN_* pattern recorded in Boltz PR #204 review | clean |
| Phase 3c (Boltz review) | Substantive SHIP verdict with checklist | ✅ All 4 PRs got checklist-style Boltz verdicts | clean (with self-approve caveat — §6) |
| Phase 3d (Optic verify) | Post-merge screenshot/pixel evidence | ✅ on 202, 203; ⚠️ MIXED on 204 (AC3 + AC9 FAIL but surfaced in verify report, not silenced) | Optic did its job |
| Phase 3e (Specc close-out) | Audit on `studio-audits/main` before S17.4 | ▶ this audit | in progress |

All pipeline phases executed in the right order. No out-of-sequence work.

### 3.2 Scope-gate enforcement

- S17.3-001 (doc-only): nothing to gate.
- S17.3-002: 4 files, all in `godot/ui/**` and `godot/tests/**`. In-scope.
- S17.3-003: 4 files, same surface. In-scope.
- S17.3-004: 9 files — `godot/brain/brottbrain.gd`, `godot/combat/brott_state.gd`, `godot/combat/combat_sim.gd`, `godot/ui/brottbrain_screen.gd`, `godot/tests/*.gd` (+ `.uid`). `combat/**` touches fall under pre-approved additive exception; Boltz verified non-CHASE paths byte-identical. In-scope at merge.
- Near-miss: initial `e39dca7` included `docs/gdd.md`. Rebased out before Boltz review. Final merge clean.

### 3.3 Design-canon gate

Gizmo's roster diff prescribed 11 triggers shown / 7 actions shown, with `HIDDEN_TRIGGERS = [WHEN_CLOCK_SAYS]` and `HIDDEN_ACTIONS = [GET_TO_COVER]`. Final `brottbrain_screen.gd`:

- `TRIGGER_DISPLAY`: 12 entries total, 1 in HIDDEN_TRIGGERS → 11 shown ✅
- `ACTION_DISPLAY`: 8 entries total, 1 in HIDDEN_ACTIONS → 7 shown ✅
- New enums appended at end of `BrottBrain.Trigger` and `BrottBrain.Action` for save-compat ✅
- "When I'm Low on Juice" reworded to "When I'm Low on Energy" ✅

Canon compliance byte-for-byte. The sprint plan's §"Card-library roster diff" wording ("Hide = remove from dicts") was internally inconsistent (dicts are ordinal-indexed arrays, literal removal breaks save-compat — the very outcome the same bullet promises). Gizmo accepted the HIDDEN_* skip-in-render pattern as canon-compliant and flagged the plan wording for forward correction. Filed as #209.

---

## 4. Per-PR review

### PR #200 — [S17.3-001] Closed-PR carry-forward documentation

- **Merge:** `42501e6`
- **Diff:** 1 file added (`docs/kb/s17.3-closed-pr-carry-forward.md`), +48/-0
- **Boltz:** SHIP (no explicit review comment — doc-only, no Optic needed)
- **Verdict:** Pass. Correct absorption mapping: PR #77 → S17.3-004; PR #76 → S17.3-002 + 003. PRs #76 and #77 remain closed. No concerns.

### PR #202 — [S17.3-002] Fix drag behavior — remove the lie

- **Merge:** `df9c1c1`
- **Diff:** 4 files, +56/-3. UI copy + `EMPTY_SLOT_TEXT_TEMPLATE` const + 44-line test + runner registration.
- **Boltz:** SHIP with 2 nits (deferred forward): (1) `.uid` convention for new resources worth a CONVENTIONS.md line; (2) pre-existing duplicate `test_s17_2_scout_feel.gd` in test_runner (inherited, not this PR). Self-approve blocked — COMMENT + squash-merge fallback.
- **Optic:** PASS.
- **Carry-forward #201 (Nutts pre-merge file):** real drag-to-reorder. Appropriately labeled `backlog`.
- **Verdict:** Clean option-A execution. No concerns.

### PR #203 — [S17.3-003] Delete interaction redesign — red tint + tooltip

- **Merge:** `7a97e37`
- **Diff:** 4 files, +159/-1. `DELETE_BTN_MODULATE_REST` / `..._HOVER` / `..._TOOLTIP` consts + hover signal wiring + 135-line test.
- **Boltz:** SHIP. Self-approve blocked — COMMENT + squash-merge fallback.
- **Optic:** PASS.
- **Verdict:** Clean. Hover and rest states painted correctly because the delete Button has non-empty text (`"✕"`) — modulate reaches the framebuffer. (Contrast with #204 AC3 — same pattern used on an empty-text Button, no draw output, no modulate effect. Filed as #205.)

### PR #204 — [S17.3-004] Card-library curation + PR #77 cherry-pick + CHASE wiring

- **Merge:** `3ec1f45` (final HEAD `da43652`; initial HEAD `e39dca7` superseded)
- **Diff:** 9 files, +558/-10. New enums appended, HIDDEN_* sets, roster-diff display entries, selected-row tint attempt, combat CHASE branch (additive), trigger evaluators, 193-line card-library test + 270-line cherry-picked S14.2 test suite.
- **Boltz:** SHIP with substantive checklist + 3 deferred-forward nits (raw enum indices at lines 322 / 370, no display-size invariant test). Self-approve blocked.
- **Optic:** MIXED — 7 of 9 ACs PASS; AC3 (selected-row blue tint) and AC9 (tray vs nav overlap at MAX_CARDS=8) FAIL.
- **Scope-gate near-miss:** initial HEAD `e39dca7` inherited `docs/gdd.md` from PR #77 cherry-pick. Riv caught. Nutts rebased. Final HEAD `da43652` clean.
- **Residuals:** see §5.

---
## 5. Residuals + carry-forward issues filed

All issues filed on `brott-studio/battlebrotts-v2` via Specc Inspector App before this audit was written. Each has `backlog` + an `area:*` + a `prio:*` label per Specc profile §1b.

| # | Title | Area | Prio | Source |
|---|---|---|---|---|
| #205 | BrottBrain selected-row tint invisible — flat Button with empty text can't paint overlay | `ux` | `mid` | Optic S17.3-004 AC3 FAIL |
| #206 | BrottBrain THEN row overlaps navigation buttons at MAX_CARDS=8 — S14.2 AC4 regression | `ux` | **`high`** | Optic S17.3-004 AC9 FAIL |
| #207 | Property-value assertions pass while pixel output fails — false-positive pattern in UI tests | `tests` | `mid` | Test-quality extraction from AC3 |
| #208 | Cherry-pick can import scope-gate-violating hunks — near-miss on PR #204 | `framework` | `mid` | Scope-gate near-miss |
| #209 | Sprint plan "Hide = remove from TRIGGER_DISPLAY/ACTION_DISPLAY dicts" wording is canon-incorrect | `framework` | `low` | Plan wording drift |
| #210 | Boltz can't self-approve — needs separate GitHub App identity | `framework` | `mid` | Cross-all-4-PRs |
| #211 | test_runner.gd lists test_s17_2_scout_feel.gd twice — inherited from S17.2 | `tests` | `low` | Inherited hygiene |
| #212 | brottbrain_screen.gd uses raw enum ordinals for pct/tiles phrasing — brittle as enum grows | `tech-debt` | `low` | Boltz PR #204 nits 1-3 |

Pre-existing issue **#201** ([S17.3 carry-forward] Implement real drag-to-reorder in BrottBrain UI) was filed by Nutts at PR #202 merge time — documented here for arc completeness, not re-filed.

### 🔴 For Riv / The Bott to decide

- **#206 (MAX_CARDS=8 overlap)** is labeled `prio:high` because the BrottBrain screen is reachable from the normal flow and saves at 8 cards are plausible user states. This is a user-visible visual defect that will show up in any playtest-ready build of the Eve Polish arc. Recommend S17.4 or a prompt hotfix sub-sprint gets this on its plan; otherwise the arc-acceptance playtest will flag it.
- **#205 (selected-row tint)** is `prio:mid` — the selection works functionally (click → ▲/▼ reorder), just no visual feedback. Lower priority than #206 but still a visible polish gap on an arc named "Eve Polish."
- **#210 (Boltz App identity)** is a **standing infra gap** that blocks formal APPROVE events across every PR. Studio-level decision — recommend elevating to an infra sprint or Specc-adjacent framework task. Specc's App already exists (S16.2-003) as working precedent; Boltz App should mirror that pattern.

Everything else is `prio:low` or `prio:mid` and fine to ride the backlog queue.

---

## 6. Compliance-reliant process detection

Per Specc profile §2, flagging S17.3 steps that only worked because an agent chose to comply, and that would silently fail if that agent were new, tired, or distracted.

### 6.1 🟡 MEDIUM — Cherry-pick scope-gate re-check

**What happened:** PR #204's initial HEAD `e39dca7` included a `docs/gdd.md` +2/−2 hunk inherited from the PR #77 cherry-pick. S17.3 scope-gate forbids any `docs/gdd.md` edit.

**Why it worked:** Riv chose to re-check the scope-gate against the final diff before Boltz review, caught the violation, had Nutts interactive-rebase it out.

**Why it's fragile:** Nothing in the pipeline's automated gates caught it. Nutts's cherry-pick procedure doesn't currently include a "diff source hunks against current sprint SCOPE GATE before `git cherry-pick`" step. Boltz's default review checklist doesn't include a "cherry-pick sources inherit their-era policy, re-verify against current SCOPE GATE" line. If Riv had been focused on something else (another arc, a playtest, an escalation) and trusted the PR as fresh, the violation would have landed.

**Risk:** Re-cherry-picks from closed-PR salvage happen ~1-2x per arc and will keep happening.

**Recommended structural fix:** Issue #208 — short-term add procedure + checklist items to `agents/nutts.md` and `agents/boltz.md`; medium-term CI guard reading the sprint file's SACRED paths and failing PRs that touch them.

### 6.2 🟡 MEDIUM — Visual ACs asserted at property level, not pixel level

**What happened:** S17.3-004 AC3 test asserted `select_btn.modulate == Color(0.3, 0.6, 1.0, 0.3)`. Property assertion passed. Rendered pixel never changed. Boltz reviewed the code and test and saw the assertion pass.

**Why it "worked" up to Boltz:** the test was a well-formed property assertion; there was no reason for Boltz to disbelieve it without pixel-sampling himself. Boltz's convention is that tests guard invariants — not that Boltz independently pixel-samples every visual AC.

**Why it caught late:** Optic's post-merge verify did pixel-sample at row centers and caught the divergence. But Optic runs **after merge**. Too late to block the ship. The lie was in-tree, in-CI, green-passing.

**Risk:** This pattern will recur every time a visual AC uses a Node whose property doesn't reach the framebuffer (flat buttons, theme overrides, parent modulate cancellation, z-order, clipping). Eve Polish will produce more of these, not fewer.

**Recommended structural fix:** Issue #207 — KB doc exists in PR #213; recommend Ett adds to CONVENTIONS.md a rule "visual ACs require pixel assertions, not property assertions" and a test-helper pattern for headless pixel-sample. This removes compliance-reliance on reviewers remembering to check.

### 6.3 🟢 LOW — Self-approve workaround

**What happened:** All 4 S17.3 PRs were Boltz-reviewed as `COMMENTED` (not `APPROVED`) because Nutts + Boltz share the `brotatotes` PAT. Boltz squash-merged despite no formal approval event.

**Why it worked:** Boltz's shipped convention includes "COMMENT + squash-merge" as a documented fallback (see `docs/kb/shared-token-self-review-422.md`, added S15.1). The convention is stable across the pipeline.

**Why it's still compliance-reliant, just mildly:** Branch protection currently doesn't require an APPROVE review, so the fallback works. If branch protection is ever tightened to require formal APPROVED events (a reasonable hardening), the fallback breaks silently — PRs can't be merged at all and the pipeline stalls.

**Risk:** Low today, latent risk on any future branch-protection tightening.

**Recommended structural fix:** Issue #210 — create Boltz GitHub App (mirrors Specc App precedent). Removes the shared-identity root cause.

### 6.4 🟢 LOW — Sprint-plan wording drift (Hide = remove from dicts)

**What happened:** Plan said "Hide = remove from dicts". Implementation correctly used the HIDDEN_* skip-in-render pattern (which preserves save-compat). Gizmo caught the plan-vs-implementation conflict, ACCEPTED the correct implementation, flagged the plan wording forward.

**Why it worked:** Gizmo is an opinionated design reviewer who reads both the plan and the code and notices internal contradictions.

**Why it's low-risk:** The correct implementation won on its merits, and Gizmo's pattern of flagging drift to Ett works end-to-end. Future sprint plans that use the convention may or may not re-use the stale wording — at that point Gizmo would catch it again.

**Recommended forward fix:** Issue #209 — corrected wording or a CONVENTIONS.md entry sprint plans can reference.

### 6.5 Summary

Two MEDIUM risks (cherry-pick scope-gate, visual AC testing) and two LOW risks. No HIGH. The pipeline's compliance-reliance is mostly well-structured with known documented fallbacks, but **#207 (visual-AC property-vs-pixel)** is the one worth urgent attention because Eve Polish is a visual-heavy arc and the false-positive class will keep surfacing until the testing convention is updated.

---

## 7. Learning extraction — KB entries

Three KB entries authored and filed as PR #213 on `battlebrotts-v2` (docs-only; Specc writes KB docs via its own Inspector App):

1. **`docs/kb/property-vs-pixel-test-pattern.md`** (#207) — canonical write-up of the false-positive class, with worked example from S17.3-004 AC3 and a recommended test-helper pattern.
2. **`docs/kb/cherry-pick-inherits-scope-gate-violations.md`** (#208) — the cherry-pick risk pattern, concrete instance from PR #204, three mitigations in order of robustness (procedure → checklist → CI guard).
3. **`docs/kb/godot-flat-button-unmodulatable.md`** (#205) — Godot-specific pitfall: `Button` with `flat=true` and empty text has no draw output; `modulate` is a silent no-op. Rule of thumb + three fix options.

Existing KB already covers the self-approve pattern (`shared-token-self-review-422.md`) and the per-agent App precedent (`per-agent-github-apps.md`) — no new entry needed for #210; #210 itself references both.

Transcript review: `sessions_history` was not accessed (not needed — PR bodies, Boltz reviews, and the in-repo state gave sufficient reconstruction for all 4 tasks). If deeper arc-wide patterns emerge that need transcript evidence, they can be extracted at the S17 arc-rollup audit after S17.4.

---

## 8. Grade

**B+**

### Why not A−

- Two visual ACs on the sprint's largest task shipped broken. They were caught at post-merge verify, not before merge. "Ship and fix forward" is a legitimate pattern for a reversible-work pipeline, but it's a step below the A− bar set by S17.2.
- The test false-positive was in the test file itself. The pipeline's own quality gate didn't catch its own blind spot.

### Why not B

- All 4 PRs merged on plan.
- Scope-streak held (7 clean).
- Pipeline phases executed in correct order.
- Scope-gate near-miss was caught pre-Boltz; final merge clean.
- Residuals are well-contained — 8 issues filed with appropriate labels, 2 flagged for Riv/Bott attention, 3 KB entries written, no silent handoffs.
- Riv made the right judgment call to cut S17.3-005 after the AC3/AC9 FAILs — adding flow-polish on top of known-broken tint would have compounded the polish debt.

### Why B+

- Strong pipeline hygiene and incident response.
- A real but contained quality miss on the largest task.
- Clear, actionable residuals with structural-fix recommendations.
- Arc is still playtest-ready if #206 gets prioritized into S17.4 — #205 can ride backlog.

---

## 9. Verdict for S17.4 audit-gate

✅ **Pass.** S17.3 close-out is complete. Audit committed to `studio-audits/main`. S17.4 planning unblocked.

Recommend Ett's S17.4 plan:
- Includes #206 (MAX_CARDS=8 overlap) as a first-class task.
- Considers whether #207 (visual-AC pixel-testing convention) is a framework task for this arc or better-fit for a framework-polish sub-sprint.
- Optionally includes #205 (selected-row tint) given its low cost and clear Option A fix.
- Links #210 (Boltz App) to the nearest infra window — not S17.4-blocking.

---

**Signed:** Specc (`brott-studio-specc[bot]`)
**Commit:** _(pushed to `studio-audits/main` — SHA in commit message trailer)_
