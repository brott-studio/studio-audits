# Arc N — Sub-sprint N.3 Audit
**Project:** battlebrotts-v2  
**Sub-sprint:** N.3 — Interaction Hint (click-to-target + click-to-move reliability)  
**PR:** #360 (`edb67f15`)  
**Audit date:** 2026-05-07  
**Inspector:** Specc  

---

## Summary

N.3 delivered five targeted fixes across three engine files plus a 5-test suite and GDD spec update. All five GAPs closed cleanly in a single implementation pass with no regressions.

| GAP | Description | File | Status |
|-----|-------------|------|--------|
| GAP-1 | `_override_target_id` pin before `brain_set_valid` gate — click-to-target always wins | `combat_sim.gd` | ✅ Closed |
| GAP-2 | Brawler/Fortress sprites rotate with `facing_angle` | `arena_renderer.gd` | ✅ Closed |
| GAP-3 | Hover highlight excludes team==0 (neutral/environment) | `arena_renderer.gd` | ✅ Closed |
| GAP-4 | Waypoint circle fade radius 8 → 24 px | `arena_renderer.gd` | ✅ Closed |
| GAP-5 | `MIN_TRAVEL_PX=32` guard + `_override_move_initial_dist` seeding | `combat_sim.gd` | ✅ Closed |

**Optic gates:** PASS all 6  
**Review rounds:** 1 (Boltz approved clean)  

---

## Implementation Notes

### combat_sim.gd
- **GAP-1:** `_override_target_id` is now pinned unconditionally before the `brain_set_valid` guard evaluates. Previously, the pin fell inside the guard and could be skipped if brain evaluation ran first — click-to-target was unreliable under fast input. Correct fix: player intent must gate brain state, not the reverse.
- **GAP-5:** `MIN_TRAVEL_PX = 32` constant guards against degenerate move commands (tap-in-place noise). `_override_move_initial_dist` is seeded at command time so the brain can track proportional progress even if the unit is immediately re-commanded.

### brottbrain.gd
- Added `_override_move_initial_dist: float = -1.0` field; `-1.0` sentinel means "not seeded."
- `clear_move_override()` resets both the dist field and the move override cleanly — no stale state leaks between commands.

### arena_renderer.gd
- **GAP-2:** Replaced static sprite draw with angle-aware draw using `facing_angle`. Uses `draw_colored_polygon` (rotatable) rather than `draw_rect` (cannot rotate in Godot 4 — see KB-N3-C).
- **GAP-3:** Hover exclude guard `if unit.team == 0: continue` prevents neutral/environment objects from lighting up on mouse-over.
- **GAP-4:** Waypoint fade radius expanded 8 → 24 px; visually legible at typical play distance.

### test_arc_n_3_interaction_hint.gd
Five tests covering the N.3 spec (§13.7 GDD):

| Test | Description |
|------|-------------|
| N3-1 | Click-to-target pins override before brain gate |
| N3-2 | Brawler facing angle reflected in renderer (single-enemy sim — see CF-N3-2) |
| N3-3 | Hover highlight skips team==0 units |
| N3-4 | Waypoint radius ≥ 20 px at fade start |
| N3-5 | Move command with dist < MIN_TRAVEL_PX is suppressed |

### docs/gdd.md
§13.7 added documenting N.3 interaction hint spec. No prior section existed; clean addition.

---

## Pipeline Notes

**Optic Verified workflow skip (recurring):**  
Optic auto-post was skipped again this sprint (third consecutive: N.1, N.2, N.3). Optic posted the verification manually and merge proceeded. This is an infra issue — not a code quality issue — and does not affect grade. The "Post Optic Verified check-run" workflow likely has a missing path filter or incorrect `workflow_run` trigger event. A dedicated infra ticket is warranted (CF-N3-1).

**Review quality:** Boltz review was clean with no requested changes. Single-round approval is consistent with N.1 and N.2 cadence.

---

## KB Candidates

**KB-N3-A — Unconditional override pattern**  
Player input must pin state *before* brain evaluation, not inside a brain-valid guard. When input conditioning is nested inside engine-state guards, fast input paths are silently dropped. Pattern: set override fields → then evaluate brain validity.  
*Source: GAP-1 fix in combat_sim.gd*

**KB-N3-B — Optic Verified workflow skip**  
The "Post Optic Verified check-run" workflow has failed to auto-post across N.1, N.2, and N.3. Likely cause: missing path filter (workflow only triggers on specific file changes) or `workflow_run` event misconfiguration. Manual workaround is available but adds friction. File infra ticket; do not normalize the skip.  
*Source: recurring pipeline observation*

**KB-N3-C — `draw_rect` cannot rotate in Godot 4**  
`CanvasItem.draw_rect()` does not accept a rotation parameter. For angle-aware shapes (e.g., unit orientation indicators), use `draw_colored_polygon()` with pre-rotated vertex arrays. This is a Godot 4 API constraint, not a bug.  
*Source: GAP-2 fix in arena_renderer.gd*

---

## Carry-Forwards to N.4

| ID | Description | Priority |
|----|-------------|----------|
| CF-N3-1 | File infra ticket for Optic Verified workflow skip (recurring N.1–N.3) | High |
| CF-N3-2 | N3-2 orientation test uses single-enemy sim — weak isolation; acceptable for now, strengthen if flake observed | Low |
| CF-N3-3 | GAP-5 wall-stuck edge case: `MIN_TRAVEL_PX=32` may suppress valid micro-moves near walls — deferred | Medium |
| CF-N1-4 | #CUT:ArcN chassis lock — arc-exit item, still open | Arc-exit |

**N.4 gate:** N.4 is an HCD playtest gate. No automated sprint follows until HCD answers 3 judgment questions. Sprint cadence pauses here.

---

## Grade

**A−**

Clean, focused implementation. All 5 GAPs closed in one pass, Optic PASS on all 6 gates, single review round, no regressions, spec documented. Grade docked from A solely for the recurring Optic Verified workflow skip (infra noise, not code quality — but it is a systemic friction point that warrants escalation).
