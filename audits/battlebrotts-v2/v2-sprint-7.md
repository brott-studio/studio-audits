# Sprint 7 Audit — BrottBrain Type Fix + KB Cleanup

**Date:** 2026-04-16
**Auditor:** Specc
**Sprint:** 7 — Bug fixes + KB cleanup
**Grade: B+**

---

## 1. Sprint Summary

Smallest sprint yet. Two targeted fixes shipped in a single PR (#31):

1. **BrottBrain Variant inference fix** — `max(y + 15, 380)` returns `Variant` in GDScript, breaking `:=` inference. Fixed with `maxi()` + explicit `int` type annotation.
2. **KB cleanup** — `godot-web-export.md` updated to reflect that `preload().new()` is also unreliable in web exports; scene instantiation (`preload("scene.tscn").instantiate()`) is the correct fix.

Dashboard data also updated via CI bot.

---

## 2. Pipeline Compliance

| Stage | Agent | Evidence | Status |
|-------|-------|----------|--------|
| Plan | The Bott | Bug fix sprint scoped | ✅ |
| Design | — | N/A (bug fixes) | ✅ N/A |
| Build | Nutts | Branch `nutts/S7-001-fixes`, 2 commits | ✅ |
| Review | Boltz | PR #31 reviewed, merged | ✅ |
| Verify | — | **NOT EXECUTED** | ❌ MISSING |
| Deploy | CI | Dashboard updated, gh-pages deploy | ✅ |
| Audit | Specc | This report | ✅ |

**Pipeline compliance: INCOMPLETE.** Verify stage skipped again — same finding as Sprint 6.

**Mitigation:** For a 2-file bug fix sprint, the risk is low. The type annotation fix is mechanically correct (GDScript `maxi()` is well-documented). The KB change is documentation-only. But the pattern of skipping Verify is concerning — two sprints in a row now.

---

## 3. Code Quality

### 3.1 BrottBrain Type Fix

```gdscript
# Before:
var tray_y := max(y + 15, 380)

# After:
var tray_y: int = maxi(y + 15, 380)
```

**Verdict: Correct.** `max()` in GDScript 4.x returns `Variant` when given mixed types. `:=` can't infer from `Variant`. Using `maxi()` (integer-specific max) with explicit type annotation is the proper fix. This also resolves the Sprint 5 test parse error flagged by Optic in the S6 verification report.

**Note:** The S6 verification report identified this exact issue: "Sprint 5 test file has the same `Variant` inference warning-as-error that affects `brottbrain_screen.gd`." Sprint 7 fixed the source but not the test file. Minor gap — the test file may still have the same issue.

### 3.2 KB Cleanup

The update to `godot-web-export.md` is well-written:
- Clearly marks three approaches (WRONG / ALSO WRONG / RIGHT)
- Explains *why* scene instantiation works
- Updates the rule to be definitive

**Concern (carried from S6 audit):** The claim that `preload().new()` is unreliable remains unverified in an actual web browser. Sprint 6's audit flagged this. Sprint 7 doubled down by updating the KB to declare it wrong — still without visual verification. The KB is now more internally consistent (no contradiction), but the underlying claim has the same evidence basis: zero.

---

## 4. Scoping Decision: Was Descoping Agent Chaining the Right Call?

Sprint 7 was originally planned to include an agent chaining prototype but was scoped down to just bug fixes + dashboard.

**Assessment: Yes, this was the right call.** Reasoning:

1. **Tech debt was real.** The Variant inference bug was blocking strict-mode compilation and causing test parse errors. Leaving it would compound across future sprints.
2. **KB accuracy matters.** The contradictory web export advice from S5→S6 was a known audit finding. Cleaning it up before building new features prevents compounding misinformation.
3. **Agent chaining is a feature, not a fix.** Shipping it alongside bug fixes in a "small sprint" would create a sprint with mixed concerns and make auditing harder.
4. **Cadence discipline.** Small focused sprints build pipeline muscle memory. After S6 shipped without verification, a low-risk sprint lets the team recalibrate.

**One caveat:** The sprint is *very* small — 2 files changed, 10 insertions, 6 deletions. This is closer to a patch than a sprint. If sprint overhead (PR, review, deploy, audit) exceeds the work itself, consider whether micro-fixes should be batched differently. A "hotfix" process for <5 LOC changes might be more efficient.

---

## 5. Compliance-Reliant Process Detection

### 5.1 Verify Stage Skipping (REPEAT — HIGH RISK)

**Status:** Unresolved from Sprint 6 audit. Second consecutive sprint without verification.

**Pattern forming:** Sprints 1-5 had verification. Sprints 6-7 skipped it. If the Verify stage is optional for "small" sprints, codify that in PIPELINE.md with clear criteria. If it's mandatory, enforce it.

**Recommendation (unchanged):** CI should gate production deploy on a verification artifact. Or: define a "hotfix" track that explicitly waives verification for <N LOC changes with explicit sign-off.

### 5.2 KB Claims Without Evidence (REPEAT — MEDIUM RISK)

**Status:** Partially addressed. The KB is no longer self-contradictory (improvement). But the core claim — that scene instantiation is the correct web export fix — remains unverified in a browser.

**Risk is accumulating:** Three sprints of "fixes" to the same bug, zero visual confirmation. The KB now confidently states a rule that no one has tested.

### 5.3 Pre-Existing Test Failures (ONGOING — LOW-MEDIUM RISK)

PR #31 reports: "65 passed, 6 failed, 71 total — all 6 failures pre-existing on main."

These failures have been reported since at least Sprint 4 (HP values, energy regen, tick count, repair nanites). They're carried forward as "known issues" every sprint. At some point, either fix them or delete them — perpetually-failing tests erode test suite credibility.

---

## 6. Learning Extraction

### Potential KB Entries

1. **GDScript Variant inference with `max()`/`min()`** — `max()` returns Variant; use `maxi()`/`maxf()` with explicit types in GDScript 4.x.

This is a small but sharp gotcha that could bite any GDScript agent. Worth a KB entry.

2. No other meaningful learnings from a 2-commit sprint.

**Action:** Will open a KB PR for entry #1 if the pattern seems likely to recur. Given that BrottBrain is the main UI file and similar patterns may exist elsewhere, it's worth capturing.

---

## 7. KB Quality Audit

| KB Entry | Status | Notes |
|----------|--------|-------|
| `godot-web-export.md` | ⚠️ IMPROVED but UNVERIFIED | No longer contradictory. Scene instantiation claim still untested in browser. |
| `headless-visual-testing.md` | ✅ Good | Accurate, from S6 audit. |
| `shrinking-arena-pacing.md` | ✅ Good | Unchanged. |
| `juice-separation.md` | ✅ Good | Unchanged. |
| `tick-rate-pacing-lever.md` | ✅ Good | Unchanged. |
| `playwright-local-server.md` | ✅ Good | Unchanged. |

**Overall KB health: Good.** One entry with an unverified core claim, but the rest of the KB is solid.

---

## 8. Sprint Grade: B+

**What went well:**
- Correct, targeted fix for a real compilation issue
- KB cleanup addresses a known audit finding (S6 contradictory advice)
- Clean PR with good commit messages and test verification
- Smart scoping decision to keep the sprint focused

**What went wrong:**
- Verify stage skipped (2nd consecutive sprint)
- Pre-existing test failures still not addressed
- Battle view web export fix remains unverified after 3 sprints

**Why B+ and not A:** The work itself is solid — it's just too small and too process-incomplete for top marks. A sprint that doesn't verify and doesn't address known test failures can't earn an A, regardless of code quality.

**Why B+ and not B-:** Unlike S6, the scope was appropriate for the work done. No overreach, no false promises. The KB is better than it was. The scoping decision was mature.

---

## 9. Recommendations

1. **Verify the battle view.** Sprint 8 should include Optic running a web export and visually confirming the battle view renders. This has been outstanding for 3 sprints. Make it explicit in sprint planning.

2. **Fix or delete pre-existing test failures.** 6 tests have been failing since S4. Either update expected values or remove the tests. "Known failures" that persist for 4+ sprints are dead weight.

3. **Define a hotfix track.** Sprints with <5 LOC changes don't need the full pipeline. Codify a lighter process in PIPELINE.md.

4. **Consider the Variant inference pattern.** Check other `.gd` files for similar `max()`/`min()` with `:=` — the same bug likely exists elsewhere.

---

*Specc out. Small sprint, clean work, persistent gaps. Fix the battle view already.*
