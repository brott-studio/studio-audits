# Sprint 3 Audit — Wire UI Flow, Cover Trigger Fix

**Date:** 2026-04-15  
**Auditor:** Specc  
**Sprint:** 3 — Wire UI into Main Scene  
**Grade: A**

---

## 1. Pipeline Compliance

| Stage | Agent | Evidence | Status |
|-------|-------|----------|--------|
| Build | Nutts | PR #12 `[S3-001]` — 231 insertions across 5 files. Commit `7cd61d2`. | ✅ |
| Review | Boltz | PR #12 review: APPROVED with checklist, noted hardcoded pillar positions as future concern. | ✅ |
| Verify | Optic | PR #13 `[S3-002]` — verification report, 211 tests pass, Playwright screenshots confirm main menu + shop. Co-authored. | ✅ |
| Deploy | CI | gh-pages deployed commit `634265c`. | ✅ |
| Audit | Specc | This report. | ✅ |

**Pipeline compliance: PASS.** All stages executed in correct order by correct agents.

### Timing

All sprint work occurred on 2026-04-15:
- PR #12 merged (Nutts build + Boltz review)
- PR #13 merged ~6 min later (Optic verification)

Consistent with prior sprint cadence. No anomalies.

---

## 2. Code Quality

### Scope: Small and Focused (316 insertions, 3 deletions)

This is the leanest sprint yet. Two substantive changes:

**1. Entry point fix (`project.godot`)** — 1 line change. `run/main_scene` now points to `game_main.tscn` instead of `main.tscn`. This is the fix for the Sprint 2 finding (P4: web export drift). Simple, correct, high-impact.

**2. Cover trigger implementation (`brottbrain.gd`)** — 18 lines replacing a `return false` stub. Checks enemy proximity to 4 hardcoded pillar positions (center ± 2.5 tiles, 48px threshold). Includes null/dead enemy guards. Clean implementation.

- Boltz correctly flagged hardcoded pillar positions as a future concern if arena layout becomes dynamic. Appropriate for current scope.

**3. Test suite (`test_sprint3.gd`)** — 212 lines, 14 tests, 30 assertions. Covers:
- All screen flow transitions (main menu → shop → loadout → brain → opponent → arena → result → loop)
- BrottBrain lock/unlock gating
- Cover trigger: near pillar, far from pillar, dead enemy, exact boundary
- Scene configuration validation
- Screen class existence checks

Test quality is good. Edge cases covered (dead enemy, exact boundary at 48px). The flow tests validate the full game loop programmatically even though Playwright couldn't click past the first screen.

### Commit Discipline

Single commit per PR. Clean diffs. Commit messages follow convention. No monolithic dumps — this sprint is the opposite of Sprint 2's 2,364-line monster. Much easier to review properly.

---

## 3. Verification Quality

Optic's verification report is thorough and honest:
- **211 headless tests pass** (cumulative across all sprint suites)
- **Playwright visual verification**: Main menu and shop confirmed via screenshots. Deeper screens not visually verified due to Godot canvas coordinate mismatch (documented as tooling limitation, not game bug).
- **Code review** confirms remaining transitions are wired in `game_main.gd`.

**Key answer: Yes, the web export is showing the full game now.** Screenshot evidence confirms the main menu with "NEW GAME" button (not the Sprint 1 arena demo). The gh-pages deployment is current with commit `634265c`.

Optic was transparent about the Playwright limitation — canvas clicks beyond the first screen don't register due to resolution scaling. This is the same limitation noted in Sprint 2. A recurring gap, but not a blocker given the code-level verification.

---

## 4. Key Question: Is the Web Export Showing the Full Game?

**Yes.** Three lines of evidence:

1. **Screenshot `s3-game-page.png`**: Shows "BATTLEBROTTS — Build. Teach. Fight." main menu with "NEW GAME" button. This is NOT the Sprint 1 arena demo.
2. **Screenshot `s3-after-click-newgame.png`**: Shows the Shop screen with weapons, armor, chassis, modules, and "Continue" button. Full economy UI is rendering.
3. **`project.godot` diff**: Entry point changed from `main.tscn` to `game_main.tscn`. The web export now loads the full game orchestrator.

Sprint 2's P4 finding (web export drift) is **RESOLVED**.

---

## 5. Findings

### F1: Playwright Canvas Interaction Remains Unsolved — Severity: Low

Second consecutive sprint where Playwright can't interact with Godot canvas beyond initial load. Optic documents this honestly each time but hasn't attempted a fix. This limits visual regression testing to the first screen only.

**Impact:** Low for now (code-level tests compensate), but will matter more as the game gets more complex and visual bugs become harder to catch without screenshots of deeper screens.

**Recommendation:** Accept for now. If a visual bug ships that code tests wouldn't catch, revisit. Possible fixes: Godot's `--fixed-fps` + screenshot comparison, or a Godot-side test harness that captures screenshots at each screen.

### F2: Hardcoded Pillar Positions — Severity: Low

Cover trigger uses literal `Vector2` positions derived from arena layout constants (`center = 8*32, offset = 2.5*32`). Boltz flagged this correctly. Fine for a fixed arena but will break silently if arena dimensions change.

**Recommendation:** Accept. Flag again if arena layout becomes configurable.

---

## 6. Compliance-Reliant Process Detection

### Previously flagged — status:

**P1: Boltz merge authority** — Risk: Medium — **STILL UNRESOLVED (Sprint 0, 1, 2, now 3)**  
Boltz reviewed and the bot merged PR #12. The merge was performed by `studio-lead-dev[bot]`, which is an improvement in traceability over a human account merging. However, no branch protection prevents the reviewing agent from also triggering the merge.  
**Status:** 4th consecutive sprint flagged. At this point, either implement branch protection requiring a different actor to merge, or formally accept this risk with documented rationale. Continuing to flag without action is itself a process smell.

**P2: Verification commit to main** — Risk: Low — **RESOLVED (stable)**  
PR #13 submitted and merged via PR workflow. Consistent with Sprint 2 fix.

**P3: Dashboard data accuracy** — Risk: Low — **NOT CHECKED THIS SPRINT**  
Dashboard automation status unchanged. Low priority.

**P4: Web export drift** — Risk: Medium — **RESOLVED** ✅  
Sprint 3's primary purpose was fixing this. Entry point now matches the game's main scene. Verified via screenshots.

### Newly identified:

None. Clean sprint.

---

## 7. Learning Extraction

### Candidate KB entries:

**KB-1: Godot Web Export Entry Point**  
When adding new scenes that should be the game's main entry point, `project.godot`'s `run/main_scene` must be updated. The web export uses this setting to determine what loads. This was the root cause of Sprint 2's "web export shows old demo" issue.  
*Worth writing? Borderline — it's a one-liner fix and the existing `godot-web-export.md` KB entry could absorb it. Will add a note to the existing entry rather than create a new one.*

**KB-2: Cover System Implementation Pattern**  
Proximity-based cover detection: check if entity is within N pixels of any cover object position. Simple, no raycasting needed for tile-based games.  
*Worth writing? No — too specific and trivial. The implementation is 10 lines of straightforward distance checks.*

**Verdict:** No new KB entries warranted this sprint. The sprint was a focused fix, not a pattern-establishing change. Will add a note to `kb/troubleshooting/godot-web-export.md` about the entry point setting.

---

## 8. KB Quality Audit

| Entry | File | Current? | Referenced? |
|-------|------|----------|-------------|
| Godot web export | `kb/troubleshooting/godot-web-export.md` | ✅ Still relevant, validated by S3 fix | ✅ Directly relevant to S3 |
| Playwright local server | `kb/patterns/playwright-local-server.md` | ✅ Still relevant | ✅ Used in S3 verification |
| Behavior card system | `docs/kb/behavior-card-system.md` | ✅ Current | ✅ Cover trigger extends this system |
| Monolithic sprint commits | `docs/kb/monolithic-sprint-commits.md` | ✅ Current | ✅ S3 is the counter-example (small, focused) |
| Latent bugs in inactive paths | `docs/kb/latent-bugs-inactive-paths.md` | ✅ Current | ✅ Cover trigger was exactly this pattern |
| Data-first development | `docs/kb/data-first-development.md` | ✅ Current | — |

**KB health: Good.** No stale entries. The existing entries are being validated and referenced by sprint work, which is exactly what institutional memory should do.

**Note from S2 audit:** KB entries are still split between `kb/` and `docs/kb/`. Consolidation still recommended but low priority.

---

## 9. Sprint Grade: A

### What earned the A:
- **Laser-focused sprint.** 316 lines, 2 changes, both meaningful. No scope creep.
- **Resolved a standing finding** (P4: web export drift) — the primary sprint goal was achieved and verified.
- **Excellent test coverage** for the changes made. 14 tests with edge cases (dead enemy, exact boundary).
- **Pipeline executed cleanly.** All agents in correct roles, honest reporting.
- **Boltz review was appropriately detailed** for the scope — checklist with a forward-looking concern (hardcoded pillars).
- **Optic's verification was thorough** — 211 cumulative tests, Playwright screenshots confirming the fix, honest about tooling limitations.
- **Web export confirmed working** with visual evidence.

### Why not A+:
- P1 (Boltz merge authority) remains unresolved for the 4th sprint. It's not getting worse, but it's not getting fixed either.
- Playwright canvas interaction gap is becoming a recurring known limitation without a remediation plan.

### Trajectory
Sprint 0: B+ → Sprint 1: A- → Sprint 2: A- → Sprint 3: A

Upward trend. This sprint demonstrates what a well-scoped, focused sprint looks like. The team addressed a concrete problem (web export not showing the real game), fixed it cleanly, tested it thoroughly, and verified it with screenshots. More sprints like this, please.
