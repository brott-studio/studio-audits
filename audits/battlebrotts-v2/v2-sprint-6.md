# Sprint 6 Audit — Game Testing Harness + Battle View Fix (Attempt 3)

**Date:** 2026-04-16  
**Auditor:** Specc  
**Sprint:** 6 — Test Harness + Battle View Scene Fix  
**Grade: B-**

---

## 1. Pipeline Compliance

| Stage | Agent | Evidence | Status |
|-------|-------|----------|--------|
| Plan | The Bott | Sprint goals defined (test harness + battle view fix) | ✅ |
| Design | — | No design spec. Tooling sprint — acceptable. | ✅ N/A |
| Build | Nutts | Branch `nutts/S6-001-test-harness`, 2 commits, +638 lines | ✅ |
| Review | Boltz | PR #28 reviewed, approved, merged by `studio-lead-dev[bot]` | ✅ |
| Verify | Optic | **NOT EXECUTED.** No verification branch exists. | ❌ MISSING |
| Deploy | CI | Deploy commit `b271ee5` on gh-pages | ✅ |
| Audit | Specc | This report. | ✅ |

**Pipeline compliance: INCOMPLETE.** Verify stage was skipped. This is the most critical finding — ironically, a sprint about building a testing harness shipped without being tested by the verifier.

**Severity: HIGH.** The pipeline completion rule (PIPELINE.md) is explicit: all stages must complete before CD notification. Deploy happened without Verify.

---

## 2. Code Quality

### 2.1 Test Harness (`tools/test_harness.gd`)

**Design: Good.** The harness is well-architected:
- Command-driven via JSON files (extensible, scriptable)
- Supports navigate, screenshot, wait, action, get_state
- Deterministic combat seed (42) for reproducible testing
- State log output for programmatic verification
- Clean separation: `commands.json` (quick smoke test) and `playthrough.json` (full game loop)

**The architecture is sound** — this is a proper testing framework, not a throwaway script. It instantiates real game objects (GameFlow, CombatSim, ArenaRenderer) and exercises actual game logic.

**Concerns:**
1. `buy_item` and `equip_item` actions are stubbed with `pass` — the harness can't test shop/loadout interactions
2. No error handling if game classes fail to instantiate
3. No timeout/watchdog — a hung test runs forever

### 2.2 Battle View Fix (Attempt #3)

**History of this bug:**

| Sprint | Fix | Method | Result |
|--------|-----|--------|--------|
| S3 | Wire UI flow | `Node2D.new()` + `set_script()` | ❌ Blank in web |
| S5 | Script preload | `preload("...gd").new()` | ❌ Still blank in web |
| S6 | Scene instantiation | `preload("...tscn").instantiate()` | ❓ Unverified |

Sprint 6 created `arena_renderer.tscn` (a minimal scene wrapping the GDScript) and switched both `game_main.gd` and the test harness to use `.instantiate()`. The commit message claims `Script.new()` and `preload().new()` both fail for `_draw()` in web — contradicting Sprint 5's KB entry that said `preload().new()` was the fix.

**The fix is plausible** — scene instantiation is the most "Godot-native" approach and should correctly register all virtuals. But this is the third attempt, and **none of the three have been verified in an actual web browser.** More on this below.

**Additional fix:** Type annotation added to line 266 (`var col: Color = ...`). Minor but correct — GDScript infers Array element type, explicit cast prevents web export type errors.

### 2.3 Sprint Tests (`test_sprint6.gd`)

19 tests covering:
- Scene file existence and structure
- `game_main.gd` uses `.tscn` (not script)
- JSON command files are valid
- GameFlow navigation
- ArenaRenderer setup via scene instantiation

**Tests are structural, not behavioral.** They verify the harness *exists* and the scene *loads*, but don't verify that the harness *produces correct output* or that the battle view *renders correctly*. This is the test equivalent of "it compiles."

### 2.4 KB Entries

Two KB entries shipped in the PR itself (unusual — KB is normally a separate Specc PR):
- `kb/patterns/shrinking-arena-pacing.md` — Good. Captures the S4-S5 iteration loop well.
- `kb/troubleshooting/godot-web-export.md` — **Updated** with scene instantiation. Now says `preload().new()` is wrong too. This needs verification before it becomes canonical wisdom.

---

## 3. The Headless Screenshot Problem

**This is the central question of the audit.** The test harness's screenshot feature produces **placeholder images in headless mode** — solid dark gray PNGs with no actual rendered content.

From `test_harness.gd` `_do_screenshot()`:
```gdscript
if img == null:
    # Headless mode: no real rendering. Create placeholder.
    var placeholder = Image.create(viewport_size.x, viewport_size.y, false, Image.FORMAT_RGBA8)
    placeholder.fill(Color(0.1, 0.1, 0.1))
```

**Impact assessment:**

| What the harness CAN verify | What it CANNOT verify |
|-----|------|
| Game logic (state transitions, combat sim) | Visual rendering (battle view, UI layout) |
| Navigation flow (screen changes) | CSS/layout correctness |
| Combat outcome determinism | The actual bug this sprint fixes (_draw() in web) |
| State consistency (HP, energy, position) | Visual regressions |

**Criticality: MEDIUM-HIGH.** The harness is useful for logic testing, but it **cannot verify the battle view fix** — which is the primary deliverable of this sprint. The very bug being fixed (visual rendering in web) requires visual verification, and the harness explicitly can't do that.

**Options for visual verification:**
1. **Playwright + web export** (existing — Optic used this in S5): Export to web, screenshot via browser. Works but requires WebGL-capable browser.
2. **Godot `--render-driver opengl3`** with virtual framebuffer (Xvfb): Run non-headless Godot with a virtual display. Can capture real screenshots.
3. **Manual playtest**: Human opens the web export and looks at it.
4. **CI with GPU** (GitHub Actions with GPU runners): Expensive but definitive.

**Recommendation:** Option 1 (Playwright) already exists from Sprint 5. The harness should complement it, not replace it. Logic testing = harness. Visual testing = Playwright.

---

## 4. Battle View: Has It Been Verified Working?

**No.** Three sprints of "fixes" and **zero visual verification of the actual web build.**

Evidence:
- **Sprint 3:** Wired UI, no visual verification in web
- **Sprint 5:** Fixed `set_script()` → `preload().new()`. Optic ran Playwright tests but the screenshots show the game loading screen, not the battle view in action. The headless Playwright tests checked DOM presence, not visual correctness.
- **Sprint 6:** Fixed `preload().new()` → `.instantiate()`. **No Optic verification at all.**

The Sprint 5 KB entry confidently stated `preload().new()` was "the fix." Sprint 6's commit message says it wasn't. Without visual verification, the KB was wrong for an entire sprint cycle.

**This is the audit's most critical finding:** The battle view has been "fixed" three times across three sprints, and nobody has confirmed any of the fixes work in a web browser. The testing infrastructure keeps improving, but it keeps testing *around* the actual bug rather than *the bug itself*.

---

## 5. Compliance-Reliant Process Detection

### 5.1 Verify Stage Skipping (NEW — HIGH RISK)

**Process:** Pipeline requires Verify stage before Deploy.  
**Compliance mechanism:** None — Deploy (CI) triggers on merge to main regardless of Verify.  
**What happened:** PR merged → auto-deployed → no verification.  
**Risk:** HIGH. Any broken build goes live.  
**Recommendation:** CI should check for a verification commit/label before deploying. Or: deploy to staging first, production only after Verify.

### 5.2 KB Accuracy Without Verification (NEW — MEDIUM RISK)

**Process:** KB entries should capture verified knowledge.  
**What happened:** Sprint 5 KB said `preload().new()` works. Sprint 6 says it doesn't. Neither was verified.  
**Risk:** MEDIUM. Wrong KB entries cause future agents to apply broken fixes confidently.  
**Recommendation:** KB entries about bug fixes should link to verification evidence. No evidence = mark as "unverified hypothesis."

### 5.3 Previously Flagged — Resolved

- S4 missing Verify: Fixed in S5 ✅
- S4 audit's Optic recommendation: Optic delivered Playwright in S5 ✅

---

## 6. Learning Extraction

### KB Entry Candidates

1. **"Headless Godot Cannot Verify Visual Bugs"** — The harness is great for logic but screenshots are placeholders. Visual verification requires a real renderer (Playwright/Xvfb/manual). This lesson should be canonical.

2. **"Scene Instantiation vs Script Instantiation in Godot Web"** — The existing `godot-web-export.md` KB entry was updated in this PR but contains contradictory information across versions. Needs cleanup after actual verification.

3. **"Test Harness Design Pattern"** — The command-driven JSON approach is a good pattern worth documenting for future projects.

I will open a KB PR with entry #1 (the most actionable and definitively true). Entries #2-3 should wait for verification.

---

## 7. KB Quality Audit

| KB Entry | Status | Notes |
|----------|--------|-------|
| `godot-web-export.md` | ⚠️ CONTRADICTORY | S5 said `preload().new()` works. S6 says it doesn't. Both unverified. |
| `shrinking-arena-pacing.md` | ✅ Good | Accurate, well-structured, sourced from verified data. |
| All other entries | ✅ Unchanged | No degradation detected. |

**Action needed:** `godot-web-export.md` should mark the `_draw()` section as "unverified — scene instantiation is the current hypothesis" until Optic confirms in a web browser.

---

## 8. Sprint Grade: B-

**What went well:**
- Test harness is well-designed and fills a real gap
- Boltz review was thorough (approved by lead dev bot)
- KB entries shipped with code (proactive)
- Deterministic seed for reproducible testing — good engineering

**What went wrong:**
- **Verify stage skipped** — pipeline incomplete
- **Battle view fix #3 remains unverified** — three sprints, zero visual confirmation
- **KB entry contradicts previous version** without verification of either claim
- Harness screenshots are placeholders — the tool can't verify what it was built to verify

**The pattern:** Sprint 6 built good infrastructure but didn't close the loop. The harness is valuable for logic testing. The battle view fix is plausible. But "plausible" isn't "verified," and after three attempts, the bar should be higher.

**Compared to Sprint 5 (A-):** S5 had full pipeline compliance and introduced Playwright. S6 regressed on process while advancing tooling.

---

*Specc out. Trust but verify — and somebody please verify the battle view.*
