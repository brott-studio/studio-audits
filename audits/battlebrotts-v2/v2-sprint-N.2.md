# Arc N — Sub-sprint N.2 Audit
## Aim Telegraph + Strafe/Retreat Behavior

**Project:** battlebrotts-v2  
**Sub-sprint:** N.2  
**PR:** #359 (merge commit `9f92d27e`)  
**Audited by:** Specc (Inspector)  
**Audit date:** 2026-05-06  

---

## 1. Sub-sprint Summary

### What Shipped

| File | Changes |
|------|---------|
| `brott_state.gd` | Added `aim_telegraph_progress`, `aim_telegraph_active`, `hovered` fields |
| `brottbrain.gd` | Added `use_first_battle_ai` flag, `_strafe_direction`, `_strafe_flip_timer`; `_evaluate_first_battle()` sets `movement_override` every tick, bypassing TCR entirely for FBI-flagged enemies |
| `combat_sim._fire_weapons()` | Aim telegraph countdown driven from weapon cooldown, guarded by `use_first_battle_ai`; countdown resets on fire |
| `combat_sim._move_brott()` | Three `first_battle_*` dispatch branches (advance / strafe / retreat) inserted before the TCR else-branch |
| `arena_renderer.gd` | Orange sweep arc (aim telegraph) + white hover ring draw calls; cursor hover detection wired into `tick_visuals` |
| `test_arc_n_2_aim_telegraph_strafe.gd` | 4 tests: N2-1 telegraph unit, N2-2 strafe sim, N2-3 retreat, N1-3b live-HP carry-forward |
| `auto_driver.gd` | CF-N1-5 housekeeping doc comment (dual-signal path confirmed present) |
| `docs/gdd.md` | §13.4 N.2 implementation notes — movement_override strings, TCR bypass contract, vector formula |

### DoD Result

**N2-DoD: PASS** — all 7 checklist items green per Optic review.  
Deploy status was stale at review time due to pipeline propagation lag; confirmed as non-blocking.

### N.1 Carry-forwards Addressed

| ID | Description | Resolution |
|----|-------------|------------|
| CF-N1-2 | Stance consumed after first move | Partially resolved — FBI path honors Aggressive via `use_first_battle_ai` branch; general case deferred to future sprint |
| CF-N1-3 | Live-HP assertion missing | Resolved — N1-3b test added in this sprint |
| CF-N1-5 | Dual-signal back-apply | Resolved — doc review confirmed signal already present; housekeeping comment added |

---

## 2. Pipeline Notes

### Review Rounds
- **1 round** — code was clean on first pass; no functional re-work required.

### Optic Verified Workflow Skip Issue
- Merge was **blocked** after the initial code review because the Optic Verified status check had not been posted to the PR.
- Root cause: Optic did not auto-post its verification result; the status was absent from the required checks list.
- Resolution: Optic posted the verified status **manually**, unblocking the merge. This is a **workflow gap** — the Optic trigger should fire automatically on all PRs that touch simulation logic.
- Recommendation: Add a branch protection rule enforcement check to catch missing Optic status before a PR is marked ready for merge, rather than discovering the gap at merge time.

### Gizmo Arc-Intent Progress
- 6 spec gaps were identified and resolved by Specc/Gizmo **before** Nutts began implementation work.
- This represents a healthy upstream-spec pattern: arc-intent clarified early, reducing mid-sprint churn.

---

## 3. Learnings / KB Candidates

### KB-1: TCR Bypass Contract (FBI Path)
`_evaluate_first_battle()` sets `movement_override` every tick for FBI-flagged enemies, which causes the TCR (Tick-Controlled Routing) block to be **entirely skipped** for those enemies. This is intentional but must be documented as a named contract so future contributors don't assume TCR always runs.  
→ **KB entry:** "FBI enemies bypass TCR via movement_override pre-emption — see §13.4 GDD."

### KB-2: Aim Telegraph Reset-on-Fire Pattern
The aim telegraph countdown is driven from weapon cooldown and resets on fire. This creates a tight coupling between telegraph state and fire state. If weapon cooldown logic changes, telegraph behavior will silently change too.  
→ **KB entry:** "Aim telegraph countdown derives from weapon cooldown — changes to cooldown timing affect telegraph UX."

### KB-3: Optic Verified Must Be a Hard Gate
The manual-post workaround this sprint reveals that Optic Verified is treated as advisory in practice even when listed as a required check. Branch protection should enforce this as a hard gate.  
→ **KB entry:** "Optic Verified status must be enforced by branch protection, not assumed from reviewer discipline."

### KB-4: Test Isolation Level for N2-1
N2-1 tests aim telegraph logic via isolated lambda (not wired into a live sim run). This is an acceptable unit test but does not catch integration regressions where the telegraph fails to fire under actual sim conditions.  
→ **KB entry:** "N2-1 is a lambda unit test; a sim-integration-level telegraph test is not yet present."

---

## 4. Carry-forwards for N.3

| ID | Description | Priority |
|----|-------------|----------|
| CF-N1-4 | `#CUT:ArcN` chassis lock needs promotion to a feature flag or explicit removal before wider testing | High — risk of silent breakage if reached in non-FBI path |
| CF-N2-1 | N2-1 telegraph test is isolated lambda only; sim-integration test deferred | Medium — acceptable for now; revisit if regressions appear |
| CF-N2-2 | HCD judgment gate for N.2 (visual telegraph visible/readable) deferred to N.4 playtest | Low — visual QA not blocking functional work |
| CF-N1-2 (partial) | Stance consumed: general case (non-FBI path) still not covered | Medium — FBI path fixed; broader stance consumption contract undefined |

---

## 5. Grade

### Grade: **A−**

**Rationale:**

- **Scope delivery:** All N.2 DoD items shipped in one PR, clean on first review pass. No functional re-work. ✅
- **Test coverage:** 4 tests added, including a carry-forward live-HP test from N.1. The N2-1 isolation level is noted but acceptable for this sprint's scope. ✅
- **Spec hygiene:** 6 arc-intent gaps resolved upstream before implementation — excellent discipline. ✅
- **Carry-forward resolution:** 3 of 4 open N.1 CFs addressed (CF-N1-4 remains open, but scoped appropriately). ✅
- **Pipeline health:** One workflow gap (Optic Verified not auto-posting) required a manual workaround at merge time. This is a process deficiency that cost time and adds risk if missed in future sprints. The gap is documented but not yet fixed. −
- **HCD gate deferred:** Visual telegraph readability judgment deferred to N.4. Acceptable for a mechanics sprint, but noted. Minor −

Overall: high-quality sprint execution with one meaningful process gap to resolve.

---

*Audit generated by Specc (Inspector) — Arc N Sub-sprint N.2*
