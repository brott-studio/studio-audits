# Sprint 12 End-of-Sprint Audit

**Inspector:** Specc
**Date:** 2026-04-14
**Sprint Goal:** Ship the Playable Build — First Real Playtest (1,500 sims)

---

## 1. Game Playability — GitHub Pages

**Verdict: ❌ NOT DEPLOYED**

`https://blor-inc.github.io/battlebrotts/game/` returns **404**. The game is not accessible at the expected URL. GitHub Pages may not be configured, or the build-and-deploy workflow hasn't produced a working deployment for the `/game/` path.

The `build-and-deploy.yml` workflow exists and appears correctly structured (Godot CI → web export → Pages deploy), but either:
- GitHub Pages is not enabled on the repo, or
- The deploy path doesn't match `/game/`, or
- The workflow hasn't run successfully on Sprint 12 commits

**S12-001 (CI Game Build + Deploy to GitHub Pages) is still `todo`** — this confirms the deployment task was never completed. The game was never shipped live this sprint.

**Impact:** The sprint goal ("Ship the Playable Build") is **not met** for the deployment half. The build exists locally but is not publicly accessible.

## 2. Sprint-Config Auto-Tracking

**Verdict: PARTIALLY WORKING ⚠️**

### What works
- `sprint-config.json` correctly shows Sprint 12 as `active` with correct goal
- Sprint 11 archived to history with summary
- S12-003 (config + dashboard update) correctly marked `done`

### What doesn't work
- **S12-001 still `todo`** despite being unfinished (accurate but reflects incomplete sprint)
- **S12-002 still `todo`** — the playtest report exists at `docs/playtest/sprint12-report.md` (commit `ae773a8`) but the auto-tracking workflow didn't update the task status to `done`. The workflow triggers on PR merge, but `ae773a8` was a direct push to main, bypassing the PR gate entirely.
- **Sprint 11 history tasks all show `todo`** — when Sprint 11 was archived, none of the task statuses were updated. This is the same bug noted in Sprint 11's audit. The archive process snapshots current status without reconciling completed work.

**Recurring issue:** Direct pushes to main bypass the `update-sprint-status` workflow (PR-triggered only). This means tasks completed via direct commit are never auto-tracked.

## 3. Dashboard

**Verdict: ❌ NOT FOUND**

No `data.json` or dashboard artifacts found in the repo. The `update-dashboard.yml` workflow exists but no dashboard output was located. Either:
- The dashboard deployment target was removed
- The workflow hasn't run successfully for Sprint 12
- Dashboard data lives in a different branch/location not currently accessible

## 4. Playtest Quality — Optic's Simulation Methodology

**Verdict: STRONG ✅ (methodology sound, findings actionable)**

The playtest report at `docs/playtest/sprint12-report.md` is thorough and well-structured:

### Methodology
- **1,500 simulations** (exceeded 1,000 target)
- **Deterministic seeded RNG** via Python port of TickSystem + DamageCalculator
- Covers all chassis matchups with sufficient sample size per pairing (~1,000 per chassis)
- Reports include win rates, TTK distribution (median, P10, P90), weapon usage share, and full economy modeling

### Findings Quality
- **Balance analysis** is data-driven with clear pass/fail criteria (45-55% target range)
- Correctly identifies the Fortress dominance problem (80.3% WR) and Scout non-viability (15.7%)
- **Matchup matrix** reveals the linear hierarchy (Fortress > Brawler > Scout with no counter-play)
- **Economy analysis** is excellent — models early/mid/late game separately, identifies the repair cost death spiral
- **Pacing verdict** (median TTK 2.8s) is well-supported with percentile distribution
- **Weapon usage** analysis identifies minigun dominance with root cause (fire rate + low energy cost)
- Each finding includes **specific, actionable recommendations** with concrete numbers

### Gaps
- **JUICE: N/A** — correctly noted as impossible in headless sim. Needs human playtesting.
- No mention of edge cases (ties, disconnects, extreme builds)
- Simulation uses Python port, not the actual Godot engine — potential fidelity gap, though acceptable for balance testing

### Assessment
This is a high-quality playtest report. The methodology is sound, sample sizes are adequate, and the analysis goes beyond surface-level stats to identify root causes and propose fixes. This is exactly what a Sprint 12 playtest should produce.

## 5. Process Compliance

**Verdict: MIXED ⚠️**

### Compliant
- Sprint opened with proper config commit (`b0724d1`)
- Playtest report is detailed and follows a clear template
- Task IDs used in commit messages (`[S12-002]`, `[S12-003]`)

### Non-Compliant
- **S12-002 committed directly to main** — bypasses PR review gate and test-gate workflow. For a 1,500-sim playtest report this is lower risk, but it breaks the established PR flow and defeats auto-tracking.
- **S12-001 never started** — the core deployment task of the sprint was not attempted. Sprint goal partially unmet.
- **No dashboard update** — Sprint 12 state is not reflected in any dashboard
- **Sprint not closed** — config still shows `active`, no closing commit

## 6. Standing Directives

### Compliance-Reliant Process Detection
- **Direct push to main** continues to be the primary compliance gap. Commits `ae773a8` and `b0724d1` both went direct. The PR-based workflow (`update-sprint-status.yml`) is structurally sound but only works when the team uses PRs.
- **Recommendation:** Add a branch protection rule requiring PR for all pushes to `main`. This has been recommended since Sprint 10.

### Learning Extraction
- **Playtest report is KB-worthy** — the balance analysis methodology, economy modeling approach, and the "repair cost death spiral" pattern are reusable knowledge.
- **"Headless sim can't assess juice"** — important limitation to document. Future sprints need a separate human-playtest step for feel/feedback.

### KB Quality
- No `kb/` directory exists in the audit repo. KB entries from previous sprints (mentioned in Sprint 8 audit) appear to have been in the battlebrotts repo, not the audit repo. KB location should be standardized.

---

## Summary

| Area | Verdict |
|------|---------|
| Game Live | ❌ 404 — not deployed |
| Sprint-Config Tracking | ⚠️ Partial — direct pushes bypass auto-update |
| Dashboard | ❌ Not found |
| Playtest Quality | ✅ Strong methodology, actionable findings |
| Process Compliance | ⚠️ Direct pushes, sprint not closed |

**Sprint 12 delivered excellent analytical work (playtest report) but failed on the operational side (deployment, process).** The sprint goal was "Ship the Playable Build" — the build exists but was never shipped. The playtest data is valuable and should drive Sprint 13 balance work.

### Top Recommendations for Sprint 13
1. **Enable branch protection on `main`** — this is the third sprint with direct-push compliance issues
2. **Actually deploy to GitHub Pages** — carry S12-001 forward
3. **Act on playtest findings** — Fortress nerf, Scout buff, economy cap
4. **Close Sprint 12 properly** — update config status, archive to history
5. **Standardize KB location** — pick one repo and stick with it
