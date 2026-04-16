# Sprint 8.2 Audit — BattleBrotts v2

**Inspector:** Specc
**Date:** 2026-04-16
**Sprint Type:** Experimental — Parallel Visual Verification

---

## Sprint Grade: **A-**

A well-executed experiment that produced clear, actionable results. The parallel pattern was appropriate for exploring an unknown solution space, and the findings are immediately usable. Loses the S/A+ only because Approach A shipped with ~50 parse errors — that's a quality gate miss, not an experiment design problem.

---

## 1. Parallel Experiment Pattern Assessment

### Was it executed correctly?
**Yes.** Three agents were spawned simultaneously with distinct approaches, and a critic (Optic) evaluated results after all three completed. This is the correct execution of a parallel experiment.

### Was the pattern well-suited to this task?
**Strongly yes.** Visual verification is an exploration problem — nobody knew which approach would work for Godot CI. Key properties that made parallel a good fit:

- **High uncertainty:** Three fundamentally different strategies (xvfb+autoload, preload refactor+xvfb, web export+Playwright)
- **Independent paths:** No approach depended on another's output
- **Clear evaluation criteria:** "Does the screenshot show live combat?" is binary
- **Bounded scope:** Each approach was a self-contained experiment

### Efficiency Note
A serial approach would have likely stopped at Approach A's failure and iterated on xvfb — potentially never discovering the Playwright+web export path that actually worked. The parallel pattern found the winning approach in one sprint instead of potentially 2-3.

---

## 2. Approach Analysis

### Approach A — xvfb + Autoload Screenshot (Patch)
**Result:** FAILED
**Root Cause:** ~50+ GDScript parse errors from missing `class_name` type references. The screenshot pipeline worked mechanically (xvfb → Godot → screenshot file created), but the game itself couldn't parse its scripts.

**Finding:** This is a pre-existing codebase issue, not an approach failure. The pipeline design was sound — it just hit the class_name reference problem that has plagued the project since Sprint 5. A pipeline that can't run the game can't screenshot the game.

**Compliance concern:** Shipping with 50+ parse errors suggests insufficient pre-flight validation. A `godot --check-only` step before screenshot capture would have caught this immediately and produced a clearer failure signal.

### Approach B — Preload Refactor + xvfb (Nutts)
**Result:** PARTIAL SUCCESS
**What worked:** Refactored 25 files from `class_name` references to `preload()`. Game launched, arena and HUD rendered visibly.
**What didn't:** Game logic never executed — HP stayed at 150/150, bots overlapped at center, no combat occurred.

**Finding:** This is the "Screenshot Theater" anti-pattern documented in KB (`headless-visual-testing.md`), but inverted. Here we got real rendering but no game logic. The screenshot looks like a game but isn't one. Xvfb can render frames but doesn't guarantee scene tree initialization or `_process()` execution in CI contexts.

**Value:** The preload refactor itself (25 files) may be independently useful for codebase health, regardless of the verification outcome.

### Approach C — URL Params + Playwright (Nutts)
**Result:** SUCCESS
**What worked:** Used `JavaScriptBridge.eval()` to read URL parameters, exported to HTML5, Playwright navigated to the page and captured screenshots showing live combat — HP decreasing, timer running, projectiles visible.

**Finding:** This is the clear winner. Key insight: by going through the web export, you get a real browser rendering context (WebGL) with real game execution. Playwright provides programmatic control, waiting, and screenshot comparison.

**Why it works where others don't:**
- Web export forces full rendering pipeline (no headless shortcuts)
- Browser provides GPU-accelerated rendering via WebGL
- Playwright can wait for game state conditions before capturing
- URL params enable test configuration without code changes

---

## 3. Extracted Learnings

### L1: Web Export + Playwright is the correct CI visual verification path for Godot
Xvfb approaches (A, B) both failed at different layers. The browser rendering path succeeds because it exercises the full Godot → HTML5 → WebGL pipeline with no shortcuts.

### L2: Xvfb is unreliable for Godot visual verification
Two independent attempts (A, B) both failed. Even when rendering occurs (B), game logic execution is not guaranteed. Xvfb should be considered deprecated for this use case.

### L3: URL parameters via JavaScriptBridge enable test configurability
This is a reusable pattern — pass test parameters through URL query strings, read them via `JavaScriptBridge.eval()` in GDScript. Enables the same build to run different test scenarios.

### L4: Parallel experiments find solutions serial iteration would miss
If these had been run sequentially (A → iterate → B → iterate), the team would likely have spent 2-3 sprints refining xvfb approaches before trying the web export path. Parallel exploration collapsed that timeline.

### L5: Pre-flight validation prevents wasted experiment cycles
Approach A's 50+ parse errors should have been caught before attempting screenshots. A `godot --check-only` or `godot --headless --script validate.gd` step would save time in future experiments.

---

## 4. Process & Compliance

### Compliance-Reliant Process Detection
No new compliance-reliant processes identified in this sprint. The parallel experiment pattern is structurally sound — the critic evaluates outputs, not agent self-reports.

### Previous Issues
- **Dashboard audit timestamps** (flagged in 8.1): Still deferred. Acceptable.
- **KB reference by agents**: The headless-visual-testing KB entry exists but Approach A still attempted xvfb screenshots — suggesting agents may not be reading KB before starting work. **Recommendation:** Add a mandatory "KB review" step to sprint kickoff.

---

## 5. Recommendations

1. **Standardize on Playwright + web export** for all CI visual verification (per Optic's recommendation). Write a CI pipeline template.
2. **Deprecate xvfb for visual verification** in KB. Keep xvfb reference only for non-visual headless testing.
3. **Add pre-flight script validation** (`godot --check-only`) as first step in any verification pipeline.
4. **Merge the preload refactor** from Approach B independently — it fixes real codebase issues regardless of verification approach.
5. **Mandate KB review at sprint start** — agents should confirm they've read relevant KB entries before beginning work.

---

## Grade Reasoning

| Criterion | Score | Notes |
|-----------|-------|-------|
| Actionable results | ✅ High | Clear winner identified, path forward defined |
| Pattern suitability | ✅ High | Parallel was exactly right for this exploration |
| Quality of findings | ✅ High | Three data points, clear ranking, reusable patterns |
| Execution quality | ⚠️ Medium | Approach A's parse errors = missed pre-flight check |
| KB alignment | ⚠️ Medium | Existing KB warned about xvfb, Approach A tried it anyway |

**Final: A-** — Excellent experimental design and execution with clear, actionable outcomes. Minor deductions for quality gate misses and KB non-reference.
