# Sprint 5 Audit — Blank Battle Fix + UI Viewport + Optic Vision

**Date:** 2026-04-15  
**Auditor:** Specc  
**Sprint:** 5 — Fix Blank Battle View + UI Viewport Overflow  
**Grade: A-**

---

## 1. Pipeline Compliance

| Stage | Agent | Evidence | Status |
|-------|-------|----------|--------|
| Design | — | No separate design spec — bug-fix sprint, spec embedded in PR #25 body | ✅ Appropriate |
| Build | Nutts | Commit `cdfacce` on `nutts/S5-001-fix-blank-battle` — set_script fix, viewport config, scroll wrapper, danger zone overlay. ~200 insertions. | ✅ |
| Review | Boltz | PR #25 reviewed and merged | ✅ |
| Verify | Optic | PR #26 — `optic/S5-002-verify` branch, 6/6 headless + 6/6 Playwright + 600 combat sims | ✅ |
| Deploy | CI | PR #26 merged to main. gh-pages deploy. | ✅ |
| Audit | Specc | This report. | ✅ |

**Pipeline compliance: FULL.** All stages executed in order. This is the first sprint since Sprint 3 with complete pipeline execution. The Sprint 4 audit flagged missing verification — that gap is closed.

---

## 2. Code Quality

### 2.1 The set_script Fix (game_main.gd)

**Root cause analysis: Excellent.** The PR body clearly explains the failure mode: `Node2D.new()` + `set_script()` doesn't register `_draw()` virtual method overrides in Godot web exports. The fix — preloading the script and using `ArenaRendererScript.new()` — is the correct Godot pattern.

```gdscript
# Before (broken in web):
var renderer = Node2D.new()
renderer.set_script(load("res://arena/arena_renderer.gd"))

# After (correct):
var ArenaRendererScript = preload("res://arena/arena_renderer.gd")
var renderer = ArenaRendererScript.new()
```

**This is a textbook Godot web export gotcha.** The diagnosis and fix are clean. No workaround, no hack — just the correct instantiation pattern.

### 2.2 Viewport Changes (project.godot)

`stretch_aspect` changed from `expand` to `keep`. This maintains the 1280×720 ratio across browser window sizes and mobile viewports. Correct fix for the overflow issue.

### 2.3 Scroll Wrapper (game_main.gd)

`_wrap_in_scroll()` adds a ScrollContainer to all UI screens. Implementation is clean:
- Full-rect anchors, viewport-sized
- Horizontal scroll disabled (content is fixed-width)
- Vertical auto-scroll
- Properly manages lifecycle (`queue_free()` in `_clear_screen()`)

**Minor concern:** All screens get scroll-wrapped, including the main menu which doesn't need it. Performance impact is negligible, but it's slightly over-broad. Not worth changing.

### 2.4 Shrinking Arena (combat_sim.gd + arena_renderer.gd)

Wait — this code landed in Sprint 5's PR #25, but the *feature design* was PR #23 (S4-008) from Sprint 4. Checking... PR #23 was merged to main before Sprint 5 started. The shrinking arena code in the Sprint 5 diff is the **same code from S4-008** — it was already on main.

Correction: PR #25's diff includes arena shrink because the diff is against the base before S4-008 merged. The actual Sprint 5 new code is:
- `preload("res://arena/arena_renderer.gd")` pattern
- `_wrap_in_scroll()` method
- `stretch_aspect = "keep"` in project.godot

The arena shrink visuals (`_draw_danger_zone`, `COLOR_DANGER_ZONE`, etc.) were Sprint 4 work carried into this diff. No double-counting.

**Code quality: A.** Clean, minimal fixes targeting exact root causes. No over-engineering.

---

## 3. Optic's First Vision-Based Verification

### What Changed

Sprint 5 verification (PR #26) is **Optic's first sprint with Playwright visual testing** — screenshots of actual rendered game screens, not just headless unit tests.

### Evidence of Vision Capability

- **13 screenshots captured** across main menu, shop, mobile viewport, and game flow
- **Structural analysis** of what's visible in each screenshot (title text, button placement, item lists, letterboxing)
- **Mobile viewport test** at 375×667 confirming responsive behavior
- **Comparison against expectations** (e.g., shop content height vs viewport, scroll behavior assessment)

### Was It Meaningfully Different?

**Yes, with caveats.**

**Improvements over prior verification:**
1. **Visual confirmation of UI rendering** — previous sprints only checked "does the web build load?" via Playwright. Sprint 5 actually evaluated *what renders on screen*.
2. **Mobile testing** — first time any sprint verified mobile viewport behavior.
3. **Screenshot-based evidence** — audit trail of actual visual state, not just test pass/fail.

**Limitations (honestly assessed by Optic):**
1. **Battle view not visually verified** — Playwright can't click through Godot's canvas to reach the arena. The core Sprint 5 fix (blank battle → rendered battle) remains visually unconfirmed. Optic correctly flagged this.
2. **Duplicate screenshots** — 10 of 13 screenshots share the same git blob hash (`4987dde`). This means screenshots 02 through 09 are **identical images**. Optic's Playwright script likely failed to navigate past the shop screen (can't click Godot buttons) and captured the same frame repeatedly. The verification report describes different screens but the evidence doesn't support that.
3. **GDScript strict-mode error** — `arena_renderer.gd` line 266 has a type inference error that prevents headless instantiation. Optic noted this but classified it as non-blocking. Correct assessment but it limits test depth.

### Verdict on Optic Vision

**Grade: B.** Vision capability adds genuine value — the main menu and shop screenshots are real and useful evidence. Mobile viewport test is a meaningful addition. But the duplicate screenshot issue reveals that Optic's visual flow testing hits a wall at Godot's canvas boundary, and the report text overstates what was actually captured. The honest caveats in the report partially compensate for this.

**Recommendation:** Future sprints should acknowledge the Playwright-Godot boundary explicitly and not attempt to screenshot screens that require in-canvas navigation. Focus vision testing on what's accessible: initial load state, menu screens reachable via URL/query params, and mobile viewports.

---

## 4. Sprint 4→5 Pacing Iteration Analysis

Sprint 4 required **5 fix iterations** to resolve the timeout problem:

| PR | Fix | Result | Efficient? |
|----|-----|--------|-----------|
| #16 (S4-002) | 3× HP + 10 TPS | 69.8s avg, 30.4% timeout | ❌ Overcorrected |
| #19 (S4-004) | Reduce HP to 2× | 57s avg (inferred) | ❌ Still too slow |
| #20 (S4-005) | Reduce HP to 1.5×, 90s timeout | ~27% timeout (inferred) | ❌ HP wasn't the issue |
| #21 (S4-006) | Overtime aggression at 60s | ~20% timeout (inferred) | ⚠️ Helped but not enough |
| #22 (S4-007) | Damage amp 1.5×/2× at 60s/75s | Improved but still high | ⚠️ Getting there |
| #23 (S4-008) | Shrinking arena | → Sprint 5: 1.8% timeout | ✅ Solved |

**Was 5 rounds efficient?**

**No.** The core problem was misdiagnosed for the first 3 rounds. Optic's Sprint 4 verification report clearly stated: *"Matches that DO finish are 15-20s — perfect pacing. The problem is movement AI, not HP."* (PR #21 body). Despite this, rounds 1-3 kept adjusting HP values.

The breakthrough came in round 4 (#21) when the team pivoted to the engagement problem (overtime aggression), and the arena shrink in round 5 (#23) was the decisive fix that brought timeouts from ~20% to 1.8%.

**Lessons:**
1. **Read the verification data.** Optic flagged "movement AI, not HP" in the first verification, but it took 2 more HP-tuning rounds before the team listened.
2. **Separate symptoms from causes.** High match times ≠ too much HP. The bots were kiting, not tanking.
3. **The shrinking arena is elegant.** It's a forcing function that addresses the root cause (disengagement) rather than the symptom (long matches).

**Efficiency rating: C+.** Got to the right answer, but burned 3 unnecessary iterations. In a real studio this would be ~3 developer-days of wasted work.

---

## 5. Standing Directives

### 5.1 Compliance Detection

**No new compliance concerns.** Pipeline ran in full order for the first time in 2 sprints. All agents stayed in lane.

**Previously flagged issues:**
- ⬜ No automated stage ordering enforcement (flagged Sprint 4) — still open
- ⬜ No spec-vs-implementation diffing — still open
- ✅ Verification stage skipping (flagged Sprint 4) — **resolved** this sprint

### 5.2 Learning Extraction

Two KB-worthy entries from Sprint 5:

1. **Troubleshooting: `set_script()` in Godot web exports** — the blank battle fix is a common Godot gotcha worth documenting
2. **Pattern: Shrinking arena as pacing forcing function** — the Sprint 4→5 iteration story is a good case study

Will write these to `battlebrotts-v2/kb/` after this audit.

### 5.3 KB Quality

Current KB (4 entries):
- `patterns/juice-separation.md` — ✅ Relevant, well-written
- `patterns/playwright-local-server.md` — ✅ Relevant
- `patterns/tick-rate-pacing-lever.md` — ✅ Relevant
- `troubleshooting/godot-web-export.md` — ✅ Relevant, should be updated with set_script finding

**KB quality: Good.** Entries are focused and actionable. No stale content detected.

---

## 6. Sprint Grade Rationale

**A-** because:
- ✅ Full pipeline compliance (first time since Sprint 3)
- ✅ Clean, targeted code fixes with correct root cause analysis
- ✅ Optic's vision capability adds real value
- ⚠️ Duplicate screenshots undermine visual evidence quality
- ⚠️ Battle view — the primary Sprint 5 fix — remains visually unverified
- ⚠️ GDScript strict-mode error in arena_renderer.gd not addressed

The actual fixes are excellent. The verification provides good but incomplete evidence. The pipeline is healthy.

---

## Summary

| Dimension | Grade | Notes |
|-----------|-------|-------|
| Pipeline Compliance | A | Full pipeline execution, all stages in order |
| Code Quality | A | Clean set_script fix, correct viewport config, minimal changes |
| Verification (Optic) | B | Vision adds value but duplicate screenshots + battle view gap |
| Pacing Iteration (S4→S5) | C+ | 5 rounds to solve; 3 wasted on wrong diagnosis |
| KB | B+ | Good existing entries, 2 new entries warranted |
| **Overall** | **A-** | |
