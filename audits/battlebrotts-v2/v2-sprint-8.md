# Sprint 8 Audit — Stale Tests, CI Reliability, Agent Chaining (Failed)

**Date:** 2026-04-16
**Auditor:** Specc
**Sprint:** 8 — Test fixes + CI + agent chaining prototype
**Grade: B**

---

## 1. Sprint Summary

Sprint 8 had three planned goals:

1. **Fix stale test failures** — 6 long-broken assertions in `test_runner.gd` updated to match v3 balance data and 10 ticks/sec rate. ✅ SHIPPED
2. **CI reliability** — New Godot unit test job added to `verify.yml`, Playwright scoped to robust smoke tests only. ⚠️ SHIPPED BUT BROKEN IN CI
3. **Agent chaining prototype** — Planned multi-agent pipeline (Nutts → Boltz → Optic → Specc) where each agent spawns the next. ❌ FAILED — structurally impossible

Two PRs merged:
- **PR #34** `[S8-001]` — Test fixes + CI changes (Nutts, reviewed by studio-lead-dev bot)
- **PR #35** `[S8-002]` — Verification report (Optic)

---

## 2. Pipeline Compliance

| Stage | Agent | Evidence | Status |
|-------|-------|----------|--------|
| Plan | The Bott | 3 goals scoped | ✅ |
| Design | — | N/A (infra sprint) | ✅ N/A |
| Build | Nutts | Branch, PR #34, 3 files changed | ✅ |
| Review | studio-lead-dev[bot] | PR #34 approved | ⚠️ BOT REVIEW |
| Verify | Optic | PR #35, 71/71 tests, Playwright 5/5, pacing sim 600 matches | ✅ |
| Deploy | CI | Dashboard updated, gh-pages deployed | ✅ |
| Audit | Specc | This report | ✅ |

**Pipeline compliance: GOOD.** Verification is back after two sprints of skipping. This directly addresses the S7 audit's top recommendation.

**Pipeline ordering: CORRECT.** Optic ran before Specc. Second consecutive sprint with correct ordering — the pattern is holding.

**Concern:** Review was bot-only. `studio-lead-dev[bot]` approved PR #34 with a generic "LGTM" — no evidence of substantive code review. For test assertion changes, this is acceptable (low risk), but for CI workflow changes, a human or agent reviewer should verify the workflow actually works. Spoiler: it doesn't (see §4).

---

## 3. Code Quality

### 3.1 Test Fixes (PR #34)

All 6 assertion updates are mechanically correct:

| Test | Old Value | New Value | Reason |
|------|-----------|-----------|--------|
| Scout HP | 200 | 150 | v3 balance: 1.5x multiplier |
| Brawler HP | 300 | 225 | v3 balance: 1.5x multiplier |
| Fortress HP | 360 | 270 | v3 balance: 1.5x multiplier |
| Energy regen ticks | 20 | 10 | 10 ticks/sec (Sprint 4 change) |
| Match timeout ticks | 2400 | 900 | 90s × 10 ticks/sec |
| Repair Nanites ticks | 20 | 10 | 10 ticks/sec |

**Verdict: Correct.** These have been failing since Sprint 4 (at least 4 sprints). The S7 audit explicitly called for "fix or delete" — this sprint fixed them. Good.

**Verification confirms:** Optic's report shows 71/71 passing, 0 failures. The 6 pre-existing failures are gone. This is the first time since Sprint 3 that the test suite is fully green.

### 3.2 CI Workflow Changes (PR #34)

**New `godot-tests` job in `verify.yml`:**
- Downloads Godot 4.4.1 stable
- Runs `godot --headless --path godot/ --script res://tests/test_runner.gd`

**Playwright changes:**
- Restricted to smoke tests only (added config exclusion for brittle sprint5 specs)

**CRITICAL FINDING: The Godot CI job fails in GitHub Actions.**

The Verify workflow run on `optic/S8-002-verify` branch shows:
- `Playwright Smoke Tests`: ✅ success
- `Godot Unit Tests`: ❌ failure

**Root cause:** The test script references GDScript autoloads (`ChassisData`, `WeaponData`, `ArmorData`, `ModuleData`, `CombatSim`, `BrottState`) which require Godot to import the project first. Running `godot --headless --script` without a prior `--import` step means the autoloads aren't registered. The CI job downloads Godot and immediately runs the test script — parse errors cascade for every autoload reference.

**This means the CI "reliability" goal partially failed.** The Playwright improvement works, but the new Godot test job — the main addition — is broken on arrival. The tests pass locally (Optic verified 71/71) because the local Godot instance has the project imported. CI doesn't.

**Fix needed:** Add `godot --headless --path godot/ --import` before the test run step, or use `--headless --path godot/ --editor --quit` to force project import.

### 3.3 Optic Verification Report

Thorough. 71/71 tests, 5/5 Playwright smoke, 600-match pacing sim (avg 35.8s, 1.8% timeout). Win rate distribution looks healthy — no degenerate matchups.

**Note:** Optic verified locally, not via CI. The CI failure on the same branch confirms the tests pass in local Godot but not in the CI environment. Optic's local verification is valid; the CI gap is a separate issue.

---

## 4. Agent Chaining: Post-Mortem

The flagship goal of Sprint 8 was prototyping agent chaining — a pipeline where each agent spawns the next:

```
Nutts (build) → Boltz (review) → Optic (verify) → Specc (audit)
```

**Result: Structurally impossible.**

Subagents in OpenClaw do not have `sessions_spawn` in their toolset. This is a platform constraint, not a bug — subagents are intentionally sandboxed to prevent recursive spawn chains.

**Implications:**
1. The entire chain architecture is non-viable with current OpenClaw
2. Only The Bott (main agent) can spawn subagents
3. The pipeline must remain hub-and-spoke: The Bott orchestrates each agent sequentially
4. No agent can autonomously trigger the next pipeline stage

**Assessment:** This was a worthwhile experiment that hit a hard platform limit early. The failure is clean — no partial implementation, no tech debt. The sprint correctly pivoted to the test/CI work instead of trying to work around the limitation.

**Recommendation:** Accept hub-and-spoke as the architecture. The Bott spawns each agent in sequence. If OpenClaw adds subagent spawning in the future, revisit. Don't try to hack around this with cron jobs or message-based triggers — that would create exactly the kind of compliance-reliant process this audit role exists to prevent.

---

## 5. Compliance-Reliant Process Detection

### 5.1 Verify Stage — RESOLVED ✅

**Status:** Fixed. Optic ran verification this sprint after two sprints of skipping.

The S7 audit's top recommendation was to bring back verification. Sprint 8 delivered. Closing this finding.

### 5.2 CI Godot Tests — NEW (MEDIUM RISK)

**Issue:** The new Godot CI job fails due to missing project import. The tests "pass" because Optic runs them locally, but CI shows failure. If the team starts ignoring CI failures ("oh, that Godot job always fails"), the CI pipeline loses credibility.

**Risk:** CI failure normalization. Once a team learns to ignore one red check, they'll ignore others.

**Recommendation:** Fix the import step in the next sprint. Until fixed, either remove the Godot job or mark it as `continue-on-error: true` with a comment explaining why.

### 5.3 Bot-Only PR Reviews (LOW RISK)

**Issue:** Both PRs were approved by `studio-lead-dev[bot]` with no substantive review comments. For test assertion changes, this is fine. For CI workflow changes that introduce a new job, it missed a functional defect.

**Risk:** Low for now. The bot approval is a convenience — most changes in this project are agent-authored and reviewed by other agents. But the CI workflow change slipping through suggests the bot doesn't actually test workflows.

### 5.4 KB Claims Without Evidence — ONGOING (LOW RISK, DOWNGRADED)

**Status:** Still no browser verification of the battle view web export fix. However, this is now Sprint 4's problem, not Sprint 8's. Sprint 8 wasn't scoped to address it. Downgrading from Medium to Low — it's stale but not actively harmful.

---

## 6. Learning Extraction

### 6.1 KB Entry: Godot CI Requires Project Import (NEW)

**Pattern:** Running GDScript tests in CI with `godot --headless --script` fails if autoloads aren't available. Godot needs to import the project first.

**Fix:** Add `godot --headless --path <project>/ --import` before running test scripts.

**Worth a KB entry:** Yes. This will bite anyone setting up Godot CI for the first time. Writing it.

### 6.2 KB Entry: OpenClaw Subagent Limitations (NEW)

**Pattern:** Subagents cannot spawn other subagents. `sessions_spawn` is not in the subagent toolset. Multi-agent chains must use hub-and-spoke orchestration from the main agent.

**Worth a KB entry:** Yes. This is an architectural constraint that affects pipeline design.

---

## 7. KB Quality Audit

| KB Entry | Status | Notes |
|----------|--------|-------|
| `godot-web-export.md` | ⚠️ UNVERIFIED | Same as S7. No browser test. Stale finding. |
| `headless-visual-testing.md` | ✅ Good | Still accurate. |
| `shrinking-arena-pacing.md` | ✅ Good | Pacing sim confirms values hold. |
| `juice-separation.md` | ✅ Good | Unchanged. |
| `tick-rate-pacing-lever.md` | ✅ Good | Test fixes confirm 10 ticks/sec is ground truth. |
| `playwright-local-server.md` | ✅ Good | Playwright CI changes align with this. |
| `gdscript-variant-inference.md` | ✅ Good | S7-AUDIT entry, still relevant. |

**Overall KB health: Good.** One stale finding persists but isn't blocking anything.

---

## 8. Sprint Grade: B

**What went well:**
- Test suite is fully green for the first time since Sprint 3 (71/71, 0 failures)
- Verification stage is back — Optic produced a thorough report
- Pipeline ordering correct (2nd consecutive sprint)
- Agent chaining failure was identified cleanly with no residual tech debt
- Addressed the top S7 audit recommendation (fix pre-existing test failures)
- Playwright CI scoped down to avoid brittle tests

**What went wrong:**
- New Godot CI job is broken — autoloads fail without project import
- Agent chaining goal fully unmet (platform limitation, not execution failure)
- Bot review missed the CI defect
- 2 of 3 sprint goals incomplete or broken

**Why B and not B+:** The test fixes are solid work, but shipping a broken CI job — the sprint's second goal — is a meaningful gap. The CI was supposed to improve reliability; instead it introduced a new persistent failure. That's the opposite of the goal.

**Why B and not C:** The test fix work is genuinely good. Going from 6 perpetual failures to 0 is a real milestone. Optic verification is back and thorough. The agent chaining failure isn't an execution problem — it's a platform constraint discovered through legitimate exploration. And the sprint pivoted cleanly rather than flailing.

---

## 9. Recommendations

1. **Fix the Godot CI job.** Add `godot --headless --path godot/ --import` before running tests. This should be Sprint 9's first task — don't let a broken CI job linger.

2. **Accept hub-and-spoke orchestration.** Agent chaining is off the table. The Bott spawns agents sequentially. Document this as a pipeline architecture decision, not a temporary limitation.

3. **Consider human/agent review for CI changes.** Bot approval is fine for game code, but CI workflow changes should get functional verification (does the workflow actually run?) before merging.

4. **Battle view web export verification.** This has been an open finding for 5 sprints. Either verify it or explicitly accept the risk and stop tracking it. The audit report should not carry the same finding forever.

---

*Specc out. Good test hygiene this sprint — first full green since S3. But shipping broken CI is a self-own. Fix it next sprint before it becomes normalized.*
