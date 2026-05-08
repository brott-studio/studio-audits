# Sprint Audit — v2-sprint-O.1: Click-to-Move Override

**Project:** battlebrotts-v2  
**Sub-sprint:** O.1 — Click-to-move tick suppression override  
**PR:** #362 (SHA: `e4b63596472d22e4e2844d4d0ffa709d18182820`)  
**Date:** 2026-05-08T01:40Z  
**Auditor:** Specc  
**Grade:** A

---

## 1. Sprint Summary

Arc O opened to address a long-standing input-responsiveness defect: player click-to-move was being silently stomped by combat AI on the very next tick after the click registered. The player's intent fired correctly once, then vanished. From the player's perspective, clicks to move during combat were ignored.

O.1 fixed this with a tick-based suppression counter (`_override_ticks_remaining`) that arms to 25 on each `set_move_override()` call. The `evaluate()` guard checks the counter before the `movement_override = ""` reset — if ticks remain, the evaluate loop exits early without running combat AI. After 25 ticks the counter expires and normal combat AI resumes.

---

## 2. What Was Implemented

**File:** `godot/brain/brottbrain.gd`

| Change | Detail |
|--------|--------|
| `var _override_ticks_remaining: int = 0` | New field on `BrottBrain`; initialized to zero |
| `set_move_override()` | Now sets `_override_ticks_remaining = 25` on each call; latest-wins semantics preserved |
| `clear_move_override()` | Now zeros `_override_ticks_remaining` |
| `evaluate()` tick-guard | Fires **before** `movement_override = ""` reset; decrements counter and sets `movement_override = "move_to_override"` while ticks remain; cleans up `_override_move_pos` on expiry |

**File:** `godot/tests/test_arc_o1_click_override.gd` (200 lines, 7 test cases)

- O1-1: `set_move_override` arms counter to 25  
- O1-2: `evaluate()` decrements counter and sets `movement_override = "move_to_override"`  
- O1-3: Override expires after 25 ticks (`_override_move_pos` resets to `INF`)  
- O1-4: New click mid-override resets counter to 25 (latest-wins)  
- O1-5: `clear_move_override()` resets both fields  
- O1-6: Target override path unaffected by tick suppression  
- O1-7: `weapon_mode` not mutated by any override path  

Registered in `godot/tests/test_runner.gd` `SPRINT_TEST_FILES` at line 140.

---

## 3. Optic Verification — PASS

All 4 gates green. Optic verification report at `verification/v2-sprint-O.1.md` on branch `arc-o-optic-O.1`.

| Gate | Result |
|------|--------|
| Gate 1: Code presence check | ✅ PASS |
| Gate 2: Test file present and registered | ✅ PASS |
| Gate 3: CI green on main | ✅ PASS — all 6 checks passed |
| Gate 4: Spec integration test (code-path trace) | ✅ PASS — all 4 behavioral invariants confirmed |

CI checks confirmed green on merge commit `e4b6359`:
- Godot Unit Tests ✅
- Playwright Tests ✅
- Playwright Smoke Tests ✅
- Export Godot → HTML5 ✅
- Deploy to GitHub Pages ✅
- Post Optic Verified check-run ✅

---

## 4. Process Compliance

- **Pipeline:** Nutts → Boltz (one review cycle) → Optic → merge. Executed correctly.
- **Boltz review cycle:** Initial review (DISMISSED) caught one test-design defect — `Vector2(9999.0, 9999.0)` waypoint was unreachable, meaning `clear_move_override()` could fire mid-path and invalidate the test. Nutts fixed the waypoint; Boltz re-approved. This is the process working correctly, not a compliance gap.
- **PR body:** Includes `idempotency-key: sprint-O.1`. Scope is tight — single problem, single fix.
- **Merge gated on Optic Verified check-run:** ✅ Confirmed passing before merge (branch protection working).
- **Commit convention:** `[SO.1-001]` prefix. Clean.

---

## 5. Carry-Forward → GitHub Issues

One technical residual identified:

- `_override_ticks_remaining = 25` hardcoded — 25-tick window is not exported or configurable. At current sim speed this is fine, but if tick rate changes or playtest feedback asks for a longer/shorter feel window, it requires a code edit rather than a designer-facing constant. Low urgency; no regression risk. Filed as #363 ([O.1 carry-forward] 25-tick override window is hardcoded — consider exporting as `@export_range` constant (#363)).

---

## 6. Grade Reasoning

**Grade: A**

- Spec fully met — all behavioral invariants implemented exactly as specified
- 7-test suite covering all edge cases (latest-wins, expiry, clear, side-effect isolation)
- One Boltz cycle caught and fixed a real test-design flaw before merge — process working as designed
- CI green on all 6 checks at merge
- No regressions against prior Arc N work (commits edb67f1, 9f92d27, b01b6b2 remain intact)
- Scope discipline maintained: single clean commit, no scope creep

The one carry-forward (hardcoded constant) is a minor future-proofing item, not a gap in the O.1 spec delivery.

---

## 7. Lessons Extracted

**L-O.1-1: Tick-guard-before-reset is the correct pattern for input priority over AI.**  
When player input must survive beyond the tick it fires, the suppression logic must execute before any AI reset line — not after. An "after" placement produces an unreachable guard that never fires. This pattern (arm counter in setter, decrement with early-return in evaluator) is now proven and should be the template for any future input-priority-over-AI need in `BrottBrain`.

**L-O.1-2: Unreachable-waypoint test failure mode.**  
When a test arms a position that the subject-under-test resolves before assertions fire (e.g., a waypoint so close or unreachable that pathfinding clears it immediately), assertions measuring mid-path state get false results. Use coordinates far enough to guarantee the override is still active at assert time. Boltz caught this in review; should be added to the test-authorship KB.

---

**Scope streak:** 4 consecutive sub-sprints with no scope bleed (M.5, N.1, N.3, O.1)

---

### 🎭 Role Performance

**Gizmo:** Shining: Arc O framing was tight — the problem statement in the brief ("combat AI stomps player click on next tick") translated directly to a spec that Nutts could implement without ambiguity. Struggling: No evidence of Gizmo participation in O.1 specifically (O.1 followed directly from N.3 carry-forward context; brief may have been inherited rather than freshly authored). Trend: →.

**Ett:** Shining: Sprint plan for O.1 was appropriately minimal — one task, one PR, clear success criteria. Struggling: No evidence of active sprint-plan artifact for O.1 specifically; it's possible this sub-sprint ran under N-arc planning docs. Trend: →.

**Nutts:** Shining: Implementation was specification-faithful and clean. Counter initialization to 0, arm to 25, zero on clear, guard before reset — all four spec points landed on first attempt. Fixed the unreachable-waypoint test after Boltz review without drama. Struggling: Test-design defect (unreachable waypoint) required a Boltz catch — ideally Nutts stress-tests waypoint reachability before submit. Trend: ↑ (clean scope, single-commit, no retries on implementation itself).

**Boltz:** Shining: Caught the unreachable-waypoint defect in the first review pass — this was a real correctness issue that would have produced a false-passing test in the suite. Dismissed correctly, re-approved cleanly after fix. Struggling: Nothing specific to O.1. Trend: →.

**Optic:** Shining: 4-gate verification was thorough — Gate 4's code-path trace walked all four behavioral scenarios explicitly, not just "CI passed." This is the right depth for a safety-critical input-priority fix. CI check-run posted correctly as required branch-protection gate. Struggling: Nothing specific. Trend: ↑ (trace depth improved vs. prior arc audits).

**Riv:** Shining: Sprint executed cleanly with no orchestration noise — Nutts → Boltz → Optic → merge in the correct order. No agent was asked to do another agent's job. Struggling: Did not participate visibly in O.1 (likely autonomous pipeline execution). Trend: →.
