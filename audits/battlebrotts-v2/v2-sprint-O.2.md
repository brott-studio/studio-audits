# Sprint Audit — v2-sprint-O.2: Brawler Speed 120→60px/s

**Project:** battlebrotts-v2  
**Sub-sprint:** O.2 — Brawler Speed 120→60px/s  
**PR:** #364 (SHA: `9ca02a57d3f3583e981d3e8a5a58eb5b63be6e3c`)  
**Date:** 2026-05-08T02:36Z  
**Auditor:** Specc  
**Grade:** B+

---

## 1. Sprint Summary

Arc O continued with a player-side feel fix: the Brawler chassis was moving at 120 px/s — too fast for its identity as a slow, durable fighter. HCD flagged this via playtest feedback. O.2 halved all three Brawler movement stats proportionally (speed 120→60, accel 240→120, decel 360→180) while preserving enemy `brawler_rush` encounter difficulty via `speed_override: 120.0` on the enemy template.

The design decision to use Option B (`speed_override` on enemy template rather than a separate enemy chassis) was correct — it leverages an existing, tested mechanism and keeps chassis_data clean. The implementation itself was tight and well-scoped. Three Boltz review cycles were required due to incomplete stale-assertion cleanup on the first fix pass.

---

## 2. What Was Implemented

**File: `godot/data/chassis_data.gd`**

| Stat | Before | After |
|------|--------|-------|
| Brawler speed | 120.0 px/s | 60.0 px/s |
| Brawler accel | 240.0 px/s² | 120.0 px/s² |
| Brawler decel | 360.0 px/s² | 180.0 px/s² |

Proportional halving — ratio preserved across all three stats. Scout (220 px/s) and Fortress (60 px/s) unchanged; Brawler now matches Fortress on raw speed, reinforcing the T2 slow-and-tough tier.

**File: `godot/data/opponent_loadouts.gd`**

- `brawler_rush` enemy template: added `speed_override: 120.0` — pins enemy Brawler at original 120 px/s despite chassis_data change
- Follows the established `first_battle_intro: speed_override: 50.0` pattern

**File: `godot/tests/test_arc_o2_brawler_speed.gd`** (new, 58 lines, 4 test functions, 7 assertions)

| Test | Assertion |
|------|-----------|
| `_test_o2_brawler_chassis_speed` | speed==60.0, accel==120.0, decel==180.0 |
| `_test_o2_scout_unchanged` | Scout speed==220.0 (no regression) |
| `_test_o2_fortress_unchanged` | Fortress speed==60.0 (no regression) |
| `_test_o2_brawler_rush_speed_override` | composed brawler_rush carries speed_override==120.0 |

**File: `godot/tests/test_runner.gd`** — test file registered in `SPRINT_TEST_FILES`

**File: `godot/tests/test_sprint12_1.gd`** — stale Brawler accel/decel/speed assertions updated to O.2 values (3 assertions across 2 fix commits)

---

## 3. Optic Verification — PASS

All 4 gates green.

| Gate | Result |
|------|--------|
| Gate 1: Code presence check | ✅ PASS |
| Gate 2: Test file present and registered | ✅ PASS |
| Gate 3: CI green on main | ✅ PASS — all CI checks passed |
| Gate 4: Spec integration test (code-path trace) | ✅ PASS — all 4 behavioral invariants confirmed |

Merge gated on `Optic Verified` check-run per branch protection. Confirmed passing before merge.

---

## 4. Process Compliance

- **Pipeline:** Nutts → Boltz (3 review cycles) → Optic → merge. Pipeline order correct.
- **Boltz review cycles:** 3 rounds, all through proper review-request/dismiss flow:
  - **Round 1 (CHANGES_REQUESTED, 02:01Z):** Boltz caught stale assertions in `test_sprint12_1.gd` — `accel==240.0` and `decel==360.0` failing after chassis change. Valid blocker.
  - **Round 2 (CHANGES_REQUESTED, 02:10Z):** Round 1 fix addressed accel/decel but missed the inline `Brawler speed == 120` assertion in `test_runner.gd`. Second valid blocker — distinct file, not a re-raise.
  - **Round 3 (APPROVED, 02:30Z):** All stale assertions fixed. CI green. Clean approve.
- **Root cause of 3 rounds:** Nutts fixed what Boltz specifically cited rather than grepping the full test suite for all stale stat references. A single comprehensive fix pass would have reduced this to 1 review cycle.
- **PR body:** Includes `idempotency-key: sprint-O.2`. Scope clean — 5 files, all on-spec.
- **Commit convention:** `[SO.2-001]` prefix. Fix commits follow `fix(test):` prefix. Compliant.
- **Gizmo pre-flight:** Gizmo correctly identified the shared-chassis conflict upfront and presented Option A (separate enemy chassis) vs Option B (speed_override). Option B chosen — correct call.
- **Merge commit author:** `Eric <erichao2018@gmail.com>` with `Co-authored-by: Nutts`. Squash merge via Boltz. Correct.

---

## 5. Carry-Forward → GitHub Issues

Two technical residuals identified and filed:

- **Stale cross-suite assertion pattern** — chassis stat changes require a full grep before committing; Nutts fixed iteratively rather than comprehensively, causing 2 extra review cycles. Recommended fix: KB entry documenting a chassis-stat-change checklist. ([O.2 carry-forward] Stale cross-suite assertion pattern — chassis stat changes require grep-all before PR (#365))
- **`speed_override` field undocumented** — the override mechanism is powerful but invisible to future sprint authors without inline docs. Low urgency but silently dangerous if a future arc adds loadouts without knowing the contract. ([O.2 carry-forward] speed_override field undocumented — add inline comment in opponent_loadouts.gd and chassis_data schema (#366))

---

## 6. Compliance-Reliant Process Detection

**Finding: Nutts self-validates fix completeness (medium risk)**  
The fix-review loop requires Nutts to proactively find all stale references before pushing. This sprint demonstrated that Nutts will fix what Boltz cites but not necessarily audit beyond the cited scope. The process relies on Nutts' thoroughness or Boltz catching every miss — both are compliance-dependent.

**Recommendation:** KB entry + Nutts profile update: before pushing any fix-pass for a stat-change PR, run `grep -r "<old_value>" godot/tests/` and confirm zero hits. This converts a compliance-dependent habit into a mechanical check. Low implementation cost.

**Risk rating:** Medium (process overhead cost, not correctness risk — CI catches it eventually, but Boltz cycles are expensive).

---

## 7. Learning Extraction

**Lesson: Stat changes need full-suite grep before fix commit (O.2 root cause)**  
When a shared constant (chassis stat, global config value) changes, all test assertions referencing the old value across the entire test suite must be updated atomically. Iterative fixes driven by CI failures are slow and waste Boltz cycles. Pattern to add to Nutts KB: `grep -r "<old_value>" godot/tests/` before any fix push.

**Positive pattern: speed_override as per-loadout tuning lever**  
`speed_override` is now used twice (`first_battle_intro`, `brawler_rush`) and is proving to be the correct mechanism for decoupling enemy encounter speed from chassis defaults. Gizmo's upfront Option B recommendation and Nutts' correct implementation of it should be captured as a KB reference: "When a chassis stat change would collaterally alter enemy difficulty, use `speed_override` on the enemy loadout template."

---

## 8. System Health

`openclaw tasks audit` was unavailable (hung, timed out). Gateway logs present at `~/.openclaw/logs/` but showed no errors related to this sprint's pipeline run. CI run on merge commit `9ca02a5` confirmed green via GitHub API. No system-level anomalies detected through available channels.

---

## 9. Grade Reasoning

**Grade: B+**

Spec fully met. All 4 Optic gates green. CI clean on merge. Design decision (Option B) was correct and well-reasoned. Implementation tight and well-scoped.

Grade capped at B+ (not A) due to 3 Boltz review cycles where 1 was the standard. Rounds 2 and 3 were caused by Nutts fixing iteratively rather than comprehensively — a process efficiency gap, not a correctness gap. The work landed correctly; the path was bumpier than needed.

Grade rubric reference: A = spec met + tests + CI green + no regressions. B = minor gaps (e.g. multiple fix rounds needed). B+ reflects: fully correct outcome, process friction above baseline.

**Scope streak:** Arc O is 2 sub-sprints old; both landed in-scope and CI-green.

---

## 10. Role Performance

### 🎭 Role Performance

**Gizmo:** Shining: Correctly identified the shared-chassis conflict before a single line of code was written; presented two concrete options (A: separate chassis, B: speed_override) with trade-offs. Option B was the right call and Gizmo's framing made it easy to choose. Struggling: Nothing notable this sprint. Trend: →.

**Ett:** Did not participate this sprint.

**Nutts:** Shining: Core implementation clean and correct on the first commit — chassis stat halving, brawler_rush speed_override, arc test file, test runner registration, all correct. Struggling: Fix pass for stale assertions was iterative, not comprehensive — fixed what Boltz cited rather than auditing the full test suite. Cost: 2 extra Boltz review cycles. Trend: →.

**Boltz:** Shining: Caught both stale assertion misses across two separate files in two sequential CHANGES_REQUESTED reviews. Reviews were precise — cited exact line, exact expected vs got value, clear fix instruction. No false positives. Struggling: Nothing notable. Trend: ↑.

**Optic:** Shining: All 4 gates green; gate coverage includes speed_override behavioral invariant (brawler_rush speed_override==120.0 confirmed via compose_encounter() path trace). Struggling: Nothing notable. Trend: →.

**Riv:** Shining: Sprint scoped and dispatched cleanly; O.2 followed directly from O.1 close without idle. Struggling: Nothing notable. Trend: →.
