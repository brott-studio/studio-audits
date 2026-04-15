# Sprint 7 — End-of-Sprint Audit

**Inspector:** Specc
**Date:** 2026-04-14
**Sprint:** 7 — "Process Quality Sprint"
**Status:** 🔴 CRITICAL ISSUES

---

## Summary

Sprint 7 was supposed to fix process issues. Instead, it reveals the studio's deepest structural problem: **the dashboard has been "fixed" at least 3 times and is still broken**, because the system that generates it is architecturally incoherent. Meanwhile, all 11 S7 commits were authored by `studio-lead-dev[bot]` with no PR merge commits on main, no PLAN.md update, no message log entries, and STATUS.md still frozen at Sprint 5. The sprint did deliver real work — P0 fix, 41 integration tests, playtest report, CI improvements — but the process scaffolding that was supposed to track it all failed completely.

375 tests confirmed. 8 tagged S7 commits landed on main. PR references in commit messages cite PRs #25–36.

---

## 1. Dashboard Root Cause Analysis

**Rating: 🔴 SYSTEMIC FAILURE — not a bug, an architecture problem**

Eric found: wrong sprint number, empty history, empty PRs, unknown actor. This is the third "fix." Here's why it keeps breaking:

### The Conflict

Two CI workflows fight over the same file:

| Workflow | What it does | FORMAT it produces |
|----------|-------------|-------------------|
| `status-gen.yml` | Auto-generates `STATUS.md` from git log + PR API | Metrics-only format: commit count, test count, recent commits list. **No task tables. No agent status.** |
| `update-dashboard.yml` | Reads `STATUS.md` to build `data.json` for the dashboard | Expects manual format: `## Sprint N Tasks` with pipe-delimited tables, `## Agent Status` with status emojis |

**These two workflows are incompatible.** One generates STATUS.md in Format A; the other reads it expecting Format B.

### Failure Chain

1. `status-gen.yml` overwrites STATUS.md with auto-generated metrics (no tasks, no agents)
2. `update-dashboard.yml` reads this STATUS.md, finds no task tables → `tasks: []`
3. Agent status section missing → `agents: {}` (or stale data from last manual update)
4. Sprint regex `\*\*Sprint (\d+) — (.+?)\*\*` finds nothing in auto-gen format → `sprint.number: 0`
5. PR list requires `gh` CLI with proper token → empty in some CI contexts
6. Git author `studio-lead-dev[bot]` doesn't match any key in `author_map` → shows as `"unknown"`

### Why "Fixes" Don't Stick

Each "fix" addresses a symptom:
- Sprint 5 (S5-001): Fixed shell injection, improved data sourcing
- Sprint 7 (7629235): Fixed "dashboard deployment" — tweaked the workflow
- Dashboard auto-update PRs: Updated data.json — but from the same broken pipeline

Nobody has addressed the **structural contradiction**: two workflows with incompatible assumptions about STATUS.md's format.

### Current State of `data.json`

```
sprint.number: 5          ← Two sprints behind
tasks: S5-001 through S5-004  ← Wrong sprint entirely  
agents: Sprint 5 assignments   ← Stale
activity[0].agent: "unknown"   ← studio-lead-dev[bot] not in author_map
pullRequests: []               ← gh CLI token issue
```

### Fix (Structural)

**Option A (recommended):** Kill `status-gen.yml`. Make `update-dashboard.yml` the sole consumer of git/PR data. Don't route through STATUS.md at all — have the dashboard workflow query git log, PR API, and a dedicated `SPRINT.json` or `PLAN.md` directly.

**Option B:** Define a single canonical format for STATUS.md. Make both workflows agree on it. Add a schema validation step.

**Option C:** Replace STATUS.md entirely with structured data (`sprint.json`, `agents.json`) that both humans and CI can read unambiguously.

The `author_map` in `update-dashboard.yml` also needs `'studio-lead-dev': 'lead-dev'` to resolve Boltz's bot commits.

### Standing Directive 1 Flag

**The dashboard is a compliance-reliant process.** It depends on:
- Someone updating STATUS.md in the right format (behavioral)
- Someone NOT running status-gen.yml which overwrites it (behavioral)
- The `author_map` being manually kept in sync with actual committer identities (behavioral)

All three are structural gaps disguised as "automation."

---

## 2. Sprint 7 Process Compliance

**Rating: 🟡 MIXED**

### What Was Done (Good)
| Commit | Work | Agent (per commit msg) |
|--------|------|----------------------|
| 5d32b94 | P0: class_name cascade fix (Sprint 6 carryover) | Nutts |
| 7629235 | Dashboard deployment fix + branch cleanup + PR checklist | Patch |
| 7f87890 | Role boundary CI + export verification + test gate | Patch |
| 4167e5e | 41 integration tests | Glytch |
| 68e843e | Playtest report — 1804 matches, 3 P0 issues | Optic |
| 7530d1f | CI test failure fix + post-deploy verification | Patch |
| 41dcd06, acbdc89, 2f5425e | Test compilation fixes (Variant types, export compat) | Nutts |
| 98beb93, 5eb2bdc | Export template path fix, PWA disable | Patch |

Real work got done. The P0 from Sprint 6 was fixed. Test count reached 375. CI was significantly improved with role-boundary checking, post-deploy verification, and better test gating.

### What Failed (Bad)

| Issue | Severity |
|-------|----------|
| **STATUS.md not updated** — still shows Sprint 5 | 🔴 Critical |
| **PLAN.md not updated** — still shows Sprint 6 | 🔴 Critical |
| **Message log not updated** — last entry is Sprint 6 | 🔴 Critical |
| **No S7 merge commits** — all pushed directly to main or squash-merged via bot | 🟡 Moderate |
| **All commits by `studio-lead-dev[bot]`** — individual agent attribution lost in git | 🟡 Moderate |
| **No Sprint 7 entry in game-dev-studio** — zero operational logging | 🔴 Critical |

### PR Process

Commit messages reference PRs #25–36 (~12 PRs for S7), which aligns with the reported "14 PRs merged." However, all commits on main are authored by `studio-lead-dev[bot]`, which means PRs were squash-merged through the GitHub App bot. This is fine mechanically but loses individual agent attribution in the git log — the very thing the dashboard depends on.

---

## 3. Rivett Role Drift Check

**Rating: 🟡 IMPROVED but new concern**

### Positive
- No evidence of Rivett writing `.gd` files this sprint (Sprint 6 violation addressed)
- No evidence of Rivett authoring other agents' reports

### Concerning
- **Rivett was effectively absent from Sprint 7.** No PLAN.md update, no message log entries, no STATUS.md update, no operational commits.
- Sprint 6 audit flagged Rivett for doing too much (role drift into dev/QA). Sprint 7 shows the opposite problem: Rivett did nothing visible.
- If Rivett delegated all S7 work but didn't track it, that's an operations failure — the Head of Operations' core job is tracking.

### Verdict
Role drift improved (no code touching), but operational duties were neglected. The studio ran Sprint 7 without its operations coordinator doing any visible coordination.

---

## 4. Code Quality

**Rating: ✅ Good**

- P0 class_name cascade fixed properly — removed problematic `class_name` declarations and switched to `load()`/`preload()` patterns
- 41 new integration tests verify cross-system interactions
- Playtest report is thorough: 1804 matches, statistical analysis, 3 P0 issues identified
- CI additions (role-boundary, post-deploy-verify, pr-checklist) are well-structured
- Test compilation fixes show attention to Godot export pipeline quirks

---

## 5. Standing Directive 1: Compliance-Reliant Process Detection

### Flagged Processes

| Process | Relies On | Risk | Structural Fix |
|---------|-----------|------|---------------|
| **Dashboard accuracy** | Someone updating STATUS.md in correct format | 🔴 High | Eliminate STATUS.md as intermediary; query data directly |
| **Sprint tracking** | Rivett updating PLAN.md + STATUS.md + message log | 🔴 High | Sprint metadata in structured file (SPRINT.json) with CI validation |
| **Agent attribution** | Commit authors matching hardcoded name map | 🟡 Medium | Use PR labels or structured commit trailers instead of author-name parsing |
| **Message logging** | Rivett manually logging all comms | 🟡 Medium | Auto-capture from session transcripts (per capture-session.sh, but it's not being used) |
| **PR process** | Agents creating branches + PRs instead of pushing to main | 🟡 Medium | Branch protection rules (require PR, require review) — currently not enforced at GitHub level |

### Key Insight
The studio has built CI enforcement for some things (test-gate, review-check, agent-log-check) but the most critical process — **knowing what sprint you're in and what's happening** — has zero structural enforcement. The dashboard, STATUS.md, PLAN.md, and message log are all manually maintained. This is why they're always stale.

---

## 6. Standing Directive 2: Learning Extraction

### Learning 1: The Dashboard Problem Is a Data Architecture Problem

**Pattern:** The dashboard has been "fixed" in Sprints 4, 5, and 7. Each fix addressed surface issues (layout, deployment, data sourcing) without resolving the core conflict: two CI workflows with incompatible assumptions about STATUS.md format.

**KB Entry Needed:** `kb/postmortems/dashboard-three-fixes.md` — document the full failure chain so the next fix addresses root cause.

### Learning 2: Bot Account Attribution Breaks Tooling

**Pattern:** Using `studio-lead-dev[bot]` for squash merges loses individual agent identity. Every downstream system (dashboard, audit, attribution CI) breaks because they pattern-match on author name.

**KB Entry Needed:** `kb/patterns/bot-account-attribution.md` — document the tradeoff and recommend PR labels or commit trailers for attribution.

### Learning 3: The Projectile Bug Was a Godot Headless Architecture Issue

**Pattern:** `class_name` declarations in Godot create global registrations. In headless mode, class loading order differs from editor mode. Chain: `Projectile` → `TickSystem` → `MatchManager` → `GameController` → all UI tests fail.

**Fix pattern:** Remove `class_name` from classes that don't need global registration; use explicit `load()`/`preload()` instead.

**KB Entry Needed:** `kb/troubleshooting/godot-classname-headless.md`

### Learning 4: Rivett Oscillates Between Too Much and Too Little

**Pattern:** Sprint 6 audit flagged Rivett for role drift (writing code, authoring reports). Sprint 7 shows the opposite: Rivett was invisible. The role needs clearer "must do" checklist, not just "must not do" boundaries.

**KB Entry Needed:** `kb/patterns/ops-role-checklist.md` — minimum viable operations per sprint.

---

## 7. Standing Directive 3: KB Quality Audit

### Current KB State (game-dev-studio)

| Path | Status |
|------|--------|
| `kb/decisions/review-note-enforcement.md` | ✅ Good — clear rationale, trade-offs documented |
| `kb/decisions/status-auto-generation.md` | ⚠️ Outdated — describes auto-gen STATUS.md but doesn't mention conflict with dashboard workflow |
| `kb/decisions/test-gate-enforcement.md` | ✅ Good |
| `kb/how-to/agent-logging.md` | ✅ Good — comprehensive |
| `kb/how-to/cross-repo-logging.md` | ✅ Good |
| `kb/postmortems/` | ❌ Empty — zero postmortems after 7 sprints |
| `kb/troubleshooting/` | ❌ Empty — the Projectile bug alone warrants an entry |
| `kb/patterns/` | ❌ Empty |

### Gaps

1. **No postmortems.** 7 sprints, multiple critical bugs, 3 dashboard failures — zero postmortems written.
2. **No troubleshooting entries.** The Projectile class_name issue is exactly the kind of thing troubleshooting/ exists for.
3. **No patterns.** Role drift, dashboard failures, bot attribution — all recurring patterns worth documenting.
4. **status-auto-generation.md is misleading.** It describes STATUS.md auto-gen as solving staleness, but doesn't mention that it breaks the dashboard. Needs updating.

---

## 8. Recommendations (Priority Order)

1. **🔴 P0: Fix dashboard architecture.** Stop routing through STATUS.md. Have the dashboard workflow query git + PR API + a structured sprint file directly. Add `studio-lead-dev[bot]` to the author map immediately.

2. **🔴 P0: Enable branch protection on main.** Require PR + at least 1 review for all pushes to main. This is the single highest-leverage structural fix — it forces PR process compliance without relying on behavior.

3. **🟡 P1: Define Rivett's minimum viable sprint checklist.** At sprint start: update PLAN.md. During sprint: update message log. At sprint end: update STATUS.md (or its replacement). Make this a CI check if possible.

4. **🟡 P1: Write the missing KB entries.** Postmortem for dashboard failures, troubleshooting for Projectile bug, patterns for bot attribution and ops role scope.

5. **🟢 P2: Reconcile status-gen.yml and update-dashboard.yml.** Either kill one or make them compatible. Currently they're in silent conflict.

---

## Appendix: Sprint 7 Commit Log

```
5eb2bdc ci: disable PWA in export preset (S7)
98beb93 ci: fix export template path for GitHub Actions container (S7)
2f5425e fix: rewrite test files for export compilation + fix Variant types (S7)
acbdc89 fix: explicit types for Variant inference in test_match_hud.gd (S7)
41dcd06 fix: correct weight calculation in test_exactly_at_cap_valid (S7)
7530d1f ci: fix CI test failures + add post-deploy verification (S7-011)
bbaad1a chore: auto-update dashboard data.json
68e843e playtest: sprint 7 balance report — 1804 matches, 3 P0 issues (S7)
124115f chore: auto-update dashboard data.json
7f87890 ci: agent role boundary enforcement + export verification + test gate (S7)
4167e5e test: add 41 integration tests for cross-system verification (S7-QA)
7629235 ci: fix dashboard deployment, add branch cleanup & PR checklist (S7)
5d32b94 fix: resolve class_name cascade failure in headless tests (S7-P0)
```

All authored by `studio-lead-dev[bot]`. Referenced PRs: #25–36.
