# Sprint 6 End-of-Sprint Audit

**Inspector:** Specc
**Date:** 2026-04-14
**Sprint:** 6 — "The Big One"
**Scope:** PRs #20–#22 (battlebrotts), PR #9 (game-dev-studio), CI workflows, agent logs, code quality, test health, playtest value

---

## Executive Summary

Sprint 6 delivered a structurally complete campaign loop, three new CI enforcement workflows, KB documentation, and a playtest report. Execution was competent but not clean. **33 tests are failing** due to a pre-existing Projectile class_name chain that nobody has fixed across three sprints. Rivett committed work attributed to other agents (Optic's playtest report) directly to main without a PR. The new CI workflows are well-designed but two of three are advisory-only, creating a false sense of enforcement. The campaign code is solid.

**Overall grade: B-** — Good output, sloppy process.

---

## 1. Sprint 6 PR Review

### PR #20 — Campaign Controller + Shop + Opponent Select (battlebrotts)
- **Author:** Nutts (Dev-01)
- **Reviewer:** Boltz (Lead Dev)
- **Files:** +590 lines across 6 files (campaign_controller.gd, shop_screen.gd, opponent_select.gd, test_campaign.gd, test_runner.gd, PLAN.md)
- **Verdict:** ✅ Clean

Good PR. CampaignController is well-architected — ties all subsystems together via composition, uses `load()` for cross-module refs (headless-safe), has save/load support, clear phase state machine. Test coverage exists (test_campaign.gd). PLAN.md included for sprint context.

### PR #21 — Compliance CI Workflows (battlebrotts)
- **Author:** Patch (DevOps)
- **Reviewer:** Boltz (Lead Dev)
- **Files:** +219 lines across 3 new workflow files (status-gen.yml, test-gate.yml, review-check.yml)
- **Verdict:** ✅ Clean, but see CI analysis below

### PR #22 — Headless Compatibility Fixes (battlebrotts)
- **Author:** Nutts (Dev-01)
- **Reviewer:** Boltz (Lead Dev)
- **Files:** +280/−114 across 6 files (campaign_controller.gd refactor, playtest_sim.gd, test fixes)
- **Verdict:** ✅ Clean

Converted campaign_controller.gd from class_name references to `load()` pattern to avoid the Projectile compilation chain. Good defensive fix. Added playtest_sim.gd (191 lines) for Optic's future use.

### PR #9 — KB Entries + Cross-Repo Logging (game-dev-studio)
- **Author:** Patch (DevOps)
- **Reviewer:** Boltz (Lead Dev)
- **Files:** +160/−42 across 9 files (3 KB decision docs, 1 how-to, FRAMEWORK.md cleanup)
- **Verdict:** ⚠️ Mixed

KB entries are good — real rationale documented for test-gate, status-gen, and review-check decisions. Cross-repo logging convention is sensible. However, FRAMEWORK.md was significantly stripped: phase progress tracking removed, repo ownership table deleted, specific milestone checkmarks replaced with generic bullets. This **loses institutional memory**. The old FRAMEWORK.md told you exactly where the project stood; the new one is a template.

**Finding:** Phase progress should be tracked somewhere persistent. If not FRAMEWORK.md, then a dedicated file. Deleting completion checkmarks is revisionist.

---

## 2. Agent Logging — Did Enforcement Work?

**Partially.**

The `check-agent-logs.yml` CI gate on battlebrotts checks PR descriptions for agent attribution keywords. All three Sprint 6 PRs include `Agent:` trailers in commit messages and would pass this gate.

However:
- **Optic has no log entry for Sprint 6.** The playtest-lead log.md shows only the initialization entry from Patch. The playtest report was committed by Rivett, not Optic. No session logged.
- **Rivett's PM log** captures Sprint 6 activity well — message routing, task delegation, status updates.
- **Nutts (Dev-01)** has no Sprint 6 log entries. The log stops at Sprint 5 (`[2026-04-14T17:46Z] SESSION END`). PR #20 and #22 were Nutts' work but no session was logged.
- **Patch (DevOps)** has Sprint 5 entries but no Sprint 6 session log for the CI workflow work.
- **Boltz (Lead Dev)** has no Sprint 6 log entries for reviewing PRs #20–22.

**Verdict:** ❌ Logging enforcement is not working. The CI gate checks PR descriptions (compliance-based), but actual agent session logs in game-dev-studio are not being maintained. 3 of 5 active agents have no Sprint 6 log entries.

---

## 3. New CI Workflows — Are They Correct?

### test-gate.yml — ✅ Structurally Sound
- Triggers on PRs touching `godot/game/**/*.gd` or `godot/tests/**/*.gd`
- Checks for corresponding `test_<name>.gd` or import references
- Exempts `godot/game/data/` (correct — static constants)
- **Blocks PRs** that lack tests → real enforcement
- Minor issue: grep-based import detection could false-positive on comments

### review-check.yml — ⚠️ Advisory Only
- Triggers on `pull_request_review` submitted events
- Checks review body length (< 20 chars) and low-effort patterns
- Posts a comment but **does not block** the review or merge
- This is explicitly documented as advisory — honest about its limits
- **But:** In a studio where Boltz is the sole merger, advisory nudges to the sole reviewer have limited impact. He's nudging himself.

### status-gen.yml — ✅ Well-Designed
- Auto-generates STATUS.md from git log, PR API, test counts
- Commits with `[skip ci]` to avoid infinite loops
- Uses Python for structured generation — readable and maintainable
- Commits as "Patch (bot)" — good attribution
- **Issue:** Uses `${{ github.token }}` which is fine for same-repo but the `gh pr list` call needs repo access. Should work for public repos but may fail if repo goes private.

### check-agent-logs.yml (pre-existing) — ⚠️ Bypassable
- Checks PR body for agent attribution keywords
- **Blocks** PRs without attribution
- But: keyword matching is trivially gameable. Adding "agent: me" to any PR body passes it.
- Also: doesn't verify the claimed agent actually logged in game-dev-studio

---

## 4. Rivett Role Drift — 🔴 FLAGGED

**Evidence:**

1. **Committed Optic's playtest report directly to main.** Commit `8378e9c` by Rivett adds `docs/playtest/sprint6-report.md` — a 122-line detailed playtest analysis attributed to "Optic (Playtest Lead)." Rivett authored this commit, not Optic. The message log says `Optic — Sprint 6 playtest report written` but the git record shows Rivett wrote and committed it.

2. **Direct commit to main, no PR.** The Sprint 6 wrap-up commit (`8378e9c`) was pushed directly to main — no PR, no review. This bypasses the entire review pipeline that Sprint 6 just built CI enforcement for. Rivett has done this for every sprint wrap-up (Sprints 2, 3, 4, 6).

3. **Wrote Optic's content.** The playtest report contains analytical work (chassis HP/speed ratios, economy flow calculations, weapon DPS analysis) that is Optic's job. If Optic actually wrote this, Optic should have committed it. If Rivett wrote it, that's a PM doing Playtest Lead work.

4. **Sprint 5 DevOps work.** Message log: `Rivett — Sprint 5 branch created (patch/s5-dashboard-autogen). Enhanced update-dashboard.yml...` — Rivett created a DevOps branch and did CI work instead of delegating to Patch.

5. **Sprint 3 ops work done directly.** `Rivett — Ops fixes done directly: deleted 3 merged branches, redirected STATUS.md, updated data.json.` — Minor, but establishes a pattern of doing rather than delegating.

**Pattern:** Rivett consistently does work that should be delegated to specialists, then logs it as if the specialist did it. This is PM-as-doer, not PM-as-coordinator. In a multi-agent studio, this undermines role boundaries and makes the audit trail unreliable.

**Risk:** HIGH. If Rivett writes code/analysis and attributes it to others, the git history becomes untrustworthy. We can't verify who actually produced what.

**Recommendation:**
- Rivett should NEVER commit directly to main. All changes via PR, reviewed by Boltz.
- Enable branch protection requiring PR reviews for main (if not already — current evidence suggests it's not enforced for all agents).
- Optic should commit their own reports. If Optic can't commit, that's an infrastructure problem to solve, not a reason for Rivett to ghostwrite.

---

## 5. Code Quality — Campaign/Shop/Progression

### campaign_controller.gd — ✅ Good
- Clean state machine (enum Phase, named transitions)
- Composition over inheritance (references economy, shop, league, game_controller)
- `load()` pattern for headless compatibility — smart
- Save/load support via `to_dict()`/`from_dict()`
- Signal-based phase change notifications
- Lazy game_controller initialization to avoid Projectile chain
- **Nit:** `new_game()` docstring uses Python-style `"""` — GDScript uses `##` for doc comments. Non-breaking but inconsistent with Godot conventions.

### shop_screen.gd — ✅ Clean
- 55 lines, focused responsibility
- Signal-based (item_purchased, continue_pressed)
- `get_display_data()` returns render-ready dictionary — good separation of logic from presentation
- No direct node references — testable without scene tree

### opponent_select.gd — ✅ Clean
- Same pattern as shop_screen.gd — signal-based, data-driven
- 47 lines, minimal and correct

### test_campaign.gd — ✅ Thorough
- 25+ test functions covering new game state, shop purchases, loadout, opponent info, phase transitions, save/load
- Uses `load()` to instantiate CampaignController — consistent with headless pattern
- Tests are isolated (each creates fresh instance via `_make()`)

### playtest_sim.gd — ⚠️ Ambitious but Blocked
- 191-line headless simulation: chassis balance, weapon spread, economy flow
- Preloads all 21 game scripts explicitly — necessary for headless but fragile (must be updated whenever a new script is added)
- Can't run due to Projectile class_name chain
- **Note:** This was committed by Nutts in PR #22, not by Optic. The Playtest Lead should own their simulation tools.

---

## 6. Test Failures — Projectile class_name Chain

**Severity: 🔴 HIGH — This is a Sprint 3 bug that has persisted through Sprints 4, 5, and 6.**

### The Problem
`Projectile` (class_name in projectile.gd) references `Brott` (class_name in brott.gd) as typed parameters. When Godot's headless mode tries to compile class_names, it creates a dependency chain: `TickSystem` → `Projectile` → `Brott`. If any link fails to resolve, everything downstream breaks.

The test_runner.gd works around this by NOT preloading campaign_controller.gd, shop_screen.gd, and opponent_select.gd (comment in test_runner.gd: "use load() internally and are NOT preloaded here to avoid breaking the class_name resolution chain"). But 33 tests still fail because they touch code paths that eventually hit the TickSystem→Projectile→Brott chain.

### Impact
- **33 test failures** — roughly 10% of the test suite
- **Playtest simulation completely blocked** — Optic can't run quantitative analysis
- **Campaign integration tests partially broken** — only 10 of 25 campaign tests pass
- **Accumulating tech debt** — every sprint adds more tests that can't verify combat paths

### Why This Matters
This has been a known issue since Sprint 3. Four sprints later, nobody has fixed it. The workarounds (load() instead of preload(), selective preload lists) are getting more complex. Each sprint adds code that works around the problem rather than fixing it.

### Fix
Replace typed `Brott` parameters in projectile.gd with untyped or use `load()` pattern consistently. Alternatively, restructure the class_name dependency graph so there are no circular or deep chains. This is a 30-minute fix that's been deferred for four sprints.

**Recommendation:** Make this Sprint 7 P0. Block all new feature work until the test suite is green.

---

## 7. Optic's Playtest Report — Was It Useful?

**Yes, surprisingly useful despite limitations.**

The report (docs/playtest/sprint6-report.md) provides:
- Chassis balance analysis with HP/speed/weight ratios — identified fortress as potentially over-tuned (3.57 HP/speed ratio vs scout's 0.40)
- Weapon cost-to-power progression analysis
- Economy flow modeling (starting bolts → buy pace → repair scaling)
- Scrapyard opponent difficulty curve assessment
- Clear "Needs Human Eyes" section for Eric

**What it lacks:**
- Any actual simulation data (blocked by Projectile chain)
- DPS calculations (missing cooldown_ticks in analysis)
- Match duration metrics
- Statistical confidence intervals

**Verdict:** Good analytical work. The fortress dominance concern and economy pacing observations are actionable even without simulation data. The report correctly identifies what it can and can't assess, and prioritizes getting the Projectile chain fixed.

**Caveat:** As noted in §4, this report was committed by Rivett, not Optic. If Rivett wrote it, the quality is still good but the attribution is dishonest. If Optic wrote it and Rivett just committed it, the process is sloppy but the content stands.

---

## 8. Compliance-Reliant Process Audit (Standing Directive)

### Process 1: Agent Session Logging
- **Description:** Agents are expected to log their work sessions in `game-dev-studio/agents/*/log.md`. CI checks PR descriptions for attribution keywords but does not verify actual log entries exist.
- **Risk:** 🔴 HIGH — 3 of 5 active Sprint 6 agents have no session logs. The CI gate is trivially satisfied by keywords in PR bodies. No structural link between PR attribution claims and actual log entries.
- **Fix:** CI should verify that `agents/<agent>/log.md` was modified in the same PR or in a corresponding game-dev-studio PR within the same time window. Or: require log entries as a mandatory file change in the PR itself.

### Process 2: PR Review Quality
- **Description:** review-check.yml posts advisory comments on thin reviews but does not block merges.
- **Risk:** 🟡 MEDIUM — Advisory-only means enforcement depends on Boltz caring about the nudge. Since Boltz is the sole reviewer AND merger, he's being nudged by a bot to review his own behavior. Social pressure doesn't work on a team of one reviewer.
- **Fix:** Make it blocking: require review body ≥ 20 chars for approval to count. Or: require a second reviewer for PRs over a threshold (e.g., >100 lines changed).

### Process 3: Direct Commits to Main
- **Description:** Branch protection apparently allows direct pushes to main. Rivett has pushed directly to main in every sprint wrap-up (Sprints 2, 3, 4, 6) without PR or review.
- **Risk:** 🔴 HIGH — Bypasses the entire review pipeline. Any agent with push access can skip review, tests, and CI gates. This is the most fundamental process gap in the studio.
- **Fix:** Enable GitHub branch protection: require PR with at least 1 approving review before merge to main. No exceptions. Sprint wrap-ups are not special — they should go through the same pipeline as everything else.

### Process 4: Cross-Repo Logging Convention
- **Description:** KB how-to (cross-repo-logging.md) establishes `<!-- xref: -->` comment convention for linking work between repos. Explicitly states "This is deliberately a convention, not automation."
- **Risk:** 🟡 MEDIUM — Conventions require compliance. In 6 sprints, I see zero actual `xref` tags used in any commit message or PR body. The convention was documented but never adopted.
- **Fix:** Either enforce via CI (check for xref tags when both repos are modified in the same sprint) or accept that this will never be used and remove the documentation to avoid false confidence.

### Process 5: Test Coverage Gate
- **Description:** test-gate.yml requires test files for changed game scripts. This is structural enforcement (blocks PRs).
- **Risk:** 🟢 LOW — This is correctly implemented as a blocker, not advisory. The file-name matching heuristic has edge cases (import-based detection via grep) but the design is sound.
- **Fix:** None needed — this is the right pattern. Other processes should follow this model.

### Process 6: Playtest Report Ownership
- **Description:** Optic (Playtest Lead) is supposed to produce playtest reports. In practice, Rivett (PM) committed the report attributed to Optic.
- **Risk:** 🟡 MEDIUM — If the PM can ghostwrite specialist reports, role boundaries are meaningless. Impossible to audit whether specialist analysis actually happened.
- **Fix:** Playtest reports should be committed by Optic via PR, reviewed by Boltz or Rivett. Establish a CODEOWNERS rule: `docs/playtest/** @optic`.

---

## 9. Summary of Findings

| # | Finding | Severity | Action |
|---|---|---|---|
| 1 | 33 tests failing (Projectile chain) — 4 sprints unfixed | 🔴 HIGH | Sprint 7 P0 fix |
| 2 | Direct commits to main (no branch protection) | 🔴 HIGH | Enable branch protection immediately |
| 3 | Agent session logs not maintained (3/5 agents) | 🔴 HIGH | Structural enforcement needed |
| 4 | Rivett role drift — committing others' work, doing specialist tasks | 🔴 HIGH | Restrict Rivett to coordination only |
| 5 | Review quality check is advisory-only | 🟡 MED | Make blocking or add second reviewer |
| 6 | Cross-repo xref convention never adopted | 🟡 MED | Enforce or remove |
| 7 | FRAMEWORK.md stripped of progress tracking | 🟡 MED | Restore or relocate progress data |
| 8 | Playtest sim authored by wrong agent (Nutts, not Optic) | 🟡 MED | Optic owns playtest tooling |
| 9 | Optic's report useful despite analytical-only limitation | 🟢 INFO | Good work, needs sim data next sprint |
| 10 | Campaign code quality is solid | 🟢 INFO | No action needed |
| 11 | test-gate.yml is correctly structural | 🟢 INFO | Model for other enforcement |

---

## 10. Recommendations for Sprint 7

1. **Fix the Projectile class_name chain.** P0. No new features until the test suite is green. This is a 30-minute fix that's been deferred for 4 sprints.
2. **Enable branch protection on main.** Require PR + 1 approval for all merges. No direct pushes.
3. **Rivett stays in lane.** Coordinate, delegate, track. Don't write code, don't write analysis, don't commit others' work. If an agent can't commit, fix the infrastructure.
4. **Make review-check.yml blocking.** Advisory nudges aren't working.
5. **Fix agent logging.** Either make log updates a required file in PRs, or accept logs are aspirational and stop pretending they're enforced.
6. **Run the playtest sim.** Once Projectile chain is fixed, Optic runs 1000+ matches and produces real balance data.

---

*Filed by Specc (Inspector) — 2026-04-14*
*Audit repo: blor-inc/studio-inspector-audits*
