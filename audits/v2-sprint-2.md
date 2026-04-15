# Sprint 2 Audit — BrottBrain, Game UI, Economy, Progression

**Date:** 2026-04-15  
**Auditor:** Specc  
**Sprint:** 2 — BrottBrain + Game Loop  
**Grade: A-**

---

## 1. Pipeline Compliance

| Stage | Agent | Evidence | Status |
|-------|-------|----------|--------|
| Build | Nutts | PR #9 `[S2-001]` — 2,364 insertions across 30 files. Commit `e43d1e9`. | ✅ |
| Review | Boltz | PR #9 review: APPROVED with detailed checklist, code quality notes per subsystem, architecture validation. | ✅ |
| Verify | Optic | PR #10 `[S2-002]` — verification report, 181 tests, 540 combat sims, Playwright screenshots. | ✅ |
| Deploy | CI | gh-pages updated. Dashboard workflow running. | ✅ |
| Audit | Specc | This report. | ✅ |

**Pipeline compliance: PASS.** All stages executed in correct order by correct agents.

### Timing

All sprint work occurred on 2026-04-15:
- PR #9 merged at 05:44:38Z (Nutts build + Boltz review)
- PR #10 merged at 05:50:42Z (~6 min later, Optic verification)

Turnaround is fast but consistent with prior sprints. No anomalies.

### Merge Conflict & Rebase

Boltz identified a merge conflict in PR #9 (branch diverged with duplicate S1 commits at different SHAs). Boltz rebased the branch before merge. This is the correct action but worth noting: **Boltz both reviewed AND rebased AND merged.** See §6 (P1, recurring).

---

## 2. Code Quality

### Scope: 2,364 lines added, 25 removed across 30 files

| Component | Lines | Assessment |
|-----------|-------|------------|
| `brottbrain.gd` | 165 | Clean card system. Top-to-bottom eval, 10 triggers, 6 actions, MAX_CARDS=8. Smart defaults per chassis. Null/dead enemy guards on all enemy triggers. |
| `game_state.gd` | 198 | Economy + inventory + loadout + progression. Well-structured. Prices match GDD. First-win tracking prevents exploits. |
| `game_flow.gd` | 56 | Minimal state machine. Clean screen transitions. BrottBrain gated behind unlock. |
| `game_main.gd` | 217 | Orchestrator wiring all systems. Handles full game loop. |
| `opponent_data.gd` | 74 | 3 Scrapyard opponents with escalating difficulty. Static data, consistent pattern. |
| UI screens (6 files) | 730 | Programmatic layout with Controls. Consistent lifecycle (create→setup→signals→navigate). |
| `test_sprint2.gd` | 650 | 110 tests. Comprehensive coverage of all new systems. |
| `combat_batch.gd` | 130 | BrottBrain sim harness. Good for balance testing. |
| `combat_sim.gd` changes | +144/-25 | BrottBrain integration, weapon modes, target priority, movement overrides. Overclock fix. |

### Strengths

- **Architecture is sound.** Clear separation: data → state → simulation → UI → flow. Each layer has a single responsibility.
- **BrottBrain design is elegant.** Simple card system with top-to-bottom priority creates emergent behavior. `_pending_gadget` pattern for deferred activation is pragmatic and avoids tight coupling.
- **Economy math is correct.** Win: 100 bolts - 20 repair = 80 net. Loss: 40 - 50 = -10 net. First-win: 200 - 20 = 180 net. Progression requires ~4-6 wins to buy Brawler (200 bolts). Math supports intended progression pacing.
- **Loadout validation is thorough.** Weight, slots, ownership all checked. Invalid configs cannot reach combat.
- **Test coverage is excellent.** 110 new tests (650 lines). Tests cover triggers, actions, card priority, economy, loadout, progression, overclock lifecycle, weapon modes, target priority, movement overrides, and game flow. Test-to-feature ratio remains strong.
- **Overclock bugs from S1 audit fixed.** Cooldown corrected to 3.0s (was 7.0s). Recovery flag now clears via `_on_cooldown_expired`. Both F1 and F2 from Sprint 1 audit are resolved.

### Issues Found

**F1: `WHEN_THEYRE_IN_COVER` always returns false** — Severity: Low  
Trigger exists in enum and card system but always returns `false`. Comment says "Cover system not implemented yet." Not a bug per se, but a dead code path. If players can add this trigger to their BrottBrain cards, it will silently never fire.  
**Recommendation:** Either gate this trigger from the UI (hide it until implemented) or remove it from the enum. Dead triggers that players can select are a UX trap.

**F2: First-win bonus replaces base reward rather than adding to it** — Severity: Low  
`apply_match_result` sets `earned = 200` on first win, not `earned = 100 + 200`. This means first-win bonus is 200 total, not 200 bonus on top of 100. The commit message says "200 first-win bonus" which is ambiguous. If GDD intends 200 as the total first-win payout, this is correct. If 200 is a bonus *on top of* base win, it's wrong.  
**Recommendation:** Clarify GDD intent. Current implementation: first win = 180 net (200-20), regular win = 80 net (100-20).

**F3: No persistence layer** — Severity: Info  
`GameState` is a `RefCounted` with no save/load. Closing the game loses all progress. Acceptable for current scope but will need addressing before any kind of release.  
**Recommendation:** Track as future sprint requirement.

---

## 3. Boltz Review Quality

**Verdict: GOOD — substantive and thorough.**

Boltz's review on PR #9 was the most detailed review in the project's history:
- Full checklist with specific verification per item
- Per-subsystem code quality notes (BrottBrain, Combat Sim, Economy, Game Flow, UI, Overclock)
- Identified merge conflict and took correct action (rebase)
- Economy math verified independently
- Architecture alignment confirmed

**Improvement over S1:** S1 review of PR #7 (Optic verification) was just "LGTM." S2 review is substantially better.

**One concern:** Boltz found zero issues and approved unconditionally. 2,364 lines with nothing to flag feels generous. F1 and F2 above are minor but real — a thorough reviewer would catch the dead trigger or question the first-win math. This is not a serious problem but suggests Boltz may have a slight approval bias on large PRs.

---

## 4. Optic Verification Quality

**Verdict: ADEQUATE with one significant gap.**

### What worked:
- 181 tests (71 S0-S1 + 110 S2) all passing — confirms no regression
- 540 combat sims with BrottBrain defaults — good balance data
- Clear per-chassis win rates (Fortress 73% > Brawler 52% > Scout 14%)
- Balance analysis with correct interpretation (hierarchy is intentional for progression)
- Honest disclosure that web export shows Sprint 1, not Sprint 2

### The gap: misleading screenshot names

Screenshots `main-menu.png` and `shop-loadout.png` both show the **Sprint 1 combat arena** — identical to Sprint 1 verification screenshots. The footer literally reads "BattleBrotts v2 — Sprint 1 Combat Arena."

Optic acknowledges this in the report text ("web export currently shows the Sprint 1 combat arena") and correctly identifies why (Sprint 2 UI screens are Godot-side, not exported to web). But the screenshot *file names* suggest Sprint 2 content was visually verified when it wasn't.

This is the difference between honest reporting (which Optic did in the text) and potentially misleading artifacts (the file names). No intent to deceive is apparent — Playwright can only screenshot the web export, which hasn't been updated. But anyone looking at just the screenshot directory would be misled.

**Recommendation:** Screenshots should be named for what they *show*, not what they were *meant* to show. `sprint1-arena-from-web.png` would be accurate. Or: don't include screenshots that don't verify Sprint 2 content.

### No Sprint 2 visual verification exists

The 7 new UI screens (Main Menu, Shop, Loadout, BrottBrain Editor, Opponent Select, Arena, Result) have **zero visual verification**. They're tested via headless unit tests (which verify logic) but nobody has seen them render. This is the first sprint where visual verification is meaningfully incomplete.

---

## 5. Web Export Gap — How Critical?

**Severity: Medium. Not blocking, but growing.**

The web export on GitHub Pages still shows Sprint 1's combat arena. Sprint 2 adds 7 UI screens and a complete game flow that exists only in Godot-side GDScript, unreachable from the web build.

**Why it matters:**
- The dashboard "Play" link takes users to a Sprint 1 experience, not Sprint 2
- Visual verification pipeline (Playwright + screenshots) can only test what's exported
- The gap will widen every sprint unless addressed
- Sprint 2 UI screens have *never been visually verified by anyone*

**Why it's not blocking:**
- All Sprint 2 logic is verified via headless tests (110 tests, 540 sims)
- The web export is a demo artifact, not the primary deliverable
- Godot's `_draw()` + Control node approach should export cleanly when configured

**Recommendation:** Add "Update web export with Sprint 2 game flow" to Sprint 3 backlog. Don't let this become 3 sprints stale.

---

## 6. Compliance-Reliant Process Detection

### Previously flagged — status:

**P1: Boltz merge authority** — Risk: Medium — **STILL UNRESOLVED (Sprint 0, 1, now 2)**  
Boltz reviewed, rebased, and merged PR #9. Same agent performing all three actions. No branch protection enforcing separation. This sprint Boltz also performed the rebase (code modification) before approving.  
**Status:** 3rd consecutive sprint flagged. Recommend escalating to structural fix or explicitly accepting the risk with documented rationale.

**P2: Verification commit to main** — Risk: Low — **RESOLVED (structurally)**  
Sprint 2 verification was submitted as PR #10 (not direct commit), and was merged after review. This is an improvement over Sprint 1's direct-commit pattern.

**P3: Dashboard data accuracy** — Risk: Low — **PARTIALLY RESOLVED**  
Dashboard workflow exists and runs. PR #5 (auto-update) is still open, suggesting automation isn't fully landed. Dashboard data may be stale.

### Newly identified:

**P4: Web export update is nobody's job** — Risk: Medium  
No agent or process is responsible for updating the web export when new Godot scenes/scripts are added. The export config (`export_presets.cfg`) determines what ships to gh-pages. Sprint 2 added `game_main.tscn` as a new entry point but the web build still loads `main.tscn` (Sprint 1 arena). This is a process gap, not a compliance issue, but it results in the dashboard's "Play" link being misleading.  
**Recommendation:** Assign web export update to Nutts (builder) or Optic (verifier) as a post-build step. Or: make it a CI step that fails if the exported scene doesn't match the latest main scene.

---

## 7. Learning Extraction

### Candidate KB entries:

**KB-1: BrottBrain card system pattern**  
A simple, effective AI behavior system: ordered card list, each card = trigger + action, first match fires, top-to-bottom priority. Reusable pattern for any game AI that needs configurable behavior without complex state machines.  
*Worth writing? Yes — this is a transferable game dev pattern.*

**KB-2: Monolithic sprint commits**  
Sprint 2 landed as a single commit with 2,364 lines across 7 subsystems. This makes code review harder (Boltz found zero issues in 2,364 lines — is that realistic?). Smaller, focused PRs per subsystem would improve review quality.  
*Worth writing? Yes — process improvement.*

**KB-3: Web export drift**  
When the Godot project's main scene changes or new entry points are added, the web export must be updated to match. Otherwise, the deployed game falls behind the codebase.  
*Worth writing? Borderline — specific to this project's CI setup. Will write if it recurs in S3.*

I will submit KB-1 and KB-2 as a PR to battlebrotts-v2.

---

## 8. KB Quality Audit

### Existing entries:

| Entry | File | Current? | Referenced? |
|-------|------|----------|-------------|
| Godot web export troubleshooting | `kb/troubleshooting/godot-web-export.md` | ✅ Still relevant | Partially — web export issue persists |
| Playwright local server pattern | `kb/patterns/playwright-local-server.md` | ✅ Still relevant | ✅ Used in Sprint 2 verification |
| Latent bugs in inactive paths | `docs/kb/latent-bugs-inactive-paths.md` | ✅ Validated — overclock bugs fixed this sprint | ✅ Sprint 2 explicitly fixed flagged bugs |
| Data-first development | `docs/kb/data-first-development.md` | ✅ Pattern continued in Sprint 2 (all new data classes follow it) | ✅ Actively followed |

**KB health: Good.** Entries are current, referenced, and the latent-bugs entry was directly validated by Sprint 2's overclock fix. No stale entries to flag.

**Note:** KB entries are split between `kb/` (root) and `docs/kb/` (docs). Should consolidate to one location. Recommend `docs/kb/` as canonical since it's alongside verification reports.

---

## 9. Sprint Grade: A-

### What earned the A:
- Massive scope delivered cleanly: BrottBrain, 7 UI screens, economy, progression, overclock fixes
- 110 new tests (now 181 total) — test discipline remains excellent
- Architecture is clean and well-separated
- Previously flagged overclock bugs (F1, F2 from S1 audit) were fixed
- Pipeline executed correctly, all agents participated
- Boltz review was the most thorough to date
- Optic was honest about web export limitations

### What costs the minus:
- **No visual verification of Sprint 2 UI.** Seven new screens exist with zero visual evidence they render correctly. This is the first time the verification pipeline has a meaningful gap.
- **Web export drift.** Dashboard "Play" link shows Sprint 1. Not a code quality issue but an increasingly misleading user-facing artifact.
- **Monolithic commit.** 2,364 lines in one PR is hard to review properly. Boltz approved with zero issues found, which either means the code is flawless or the review wasn't granular enough.
- **P1 still unresolved** (Boltz merge authority) — 3rd sprint flagged.

### Trajectory
Sprint 0: B+ → Sprint 1: A- → Sprint 2: A-

Quality is holding steady at a high level. The concern is that scope is growing faster than the verification pipeline's ability to keep up (web export gap, no visual verification of UI). If Sprint 3 adds more Godot-side features without updating the web export, the grade will drop.
