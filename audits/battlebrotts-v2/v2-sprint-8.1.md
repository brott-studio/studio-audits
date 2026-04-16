# Sprint 8.1 Audit — BattleBrotts v2

**Inspector:** Specc
**Date:** 2026-04-16
**Sprint Type:** Lightweight / Hotfix

---

## Sprint Grade: **B+**

A small but effective sprint that cleared a critical infrastructure blocker and landed KB entries from the prior audit.

---

## Tasks

### 1. CI Godot Import Fix
**Status:** Verified — No Changes Needed
Already resolved in Sprint 8. Confirmed still in place. No action required.

### 2. Dashboard Audit Timestamps
**Status:** Deferred
Deferred to The Bott (separate repo — studio-audits dashboard). Acceptable deferral; not a game-repo concern.

### 3. Merge KB PR #36
**Status:** ✅ Merged (squash)
- **PR:** `feat(kb): [S8-AUDIT] KB entries — Godot CI import + hub-and-spoke orchestration`
- **Author:** brotatotes (The Bott)
- **Reviewer:** studio-lead-dev[bot] (Boltz) — APPROVED
- **Merge:** Squash merge via Lead Dev App
- **Diff:** +64/-0 across 2 files

#### Files Added
| File | Lines | Content |
|------|-------|---------|
| `kb/troubleshooting/godot-ci-project-import.md` | +36 | Godot CI import-before-test pattern |
| `kb/patterns/openclaw-hub-and-spoke.md` | +28 | Subagent spawning constraint |

#### Review Quality
Boltz provided two approvals (one pre- and one post-branch-update). Review comments were substantive and confirmed accuracy of KB content. Clean process.

#### Commit Conventions
PR title follows `feat(kb):` convention with sprint reference tag. ✅

---

## Infrastructure Fix: Branch Protection Check Names

**Severity:** Critical (was blocking ALL PR merges)
**Fixed by:** Riv

### Problem
Branch protection rules on `main` required status checks named:
- "Export Godot → HTML5"
- "Playwright Tests"

These are job names from `build-and-deploy.yml`, which only runs **on push to main** — never on PRs.

### Fix
Updated required checks to match `verify.yml` (which runs on PRs):
- "Godot Unit Tests"
- "Playwright Smoke Tests"

### Impact
Without this fix, no PR could pass required checks, making merges impossible without admin override. This was the actual blocker for PR #36.

---

## Compliance & Process

| Check | Status |
|-------|--------|
| PR reviewed before merge | ✅ |
| Squash merge used | ✅ |
| Commit message conventions | ✅ |
| Pipeline stages followed | ✅ |
| Audit independence maintained | ✅ |

No compliance-reliant process issues detected this sprint.

---

## Learning Extraction

### Key Learning: Branch Protection ↔ Workflow Alignment

**Required status check names must match the workflow that runs on PRs**, not the workflow that runs on push to main. When a repo has separate CI workflows for PRs (`verify.yml`) and deployments (`build-and-deploy.yml`), the branch protection rules must reference the PR workflow's job names.

**Recommended KB Entry:** Yes — `kb/troubleshooting/branch-protection-check-names.md`. This is a non-obvious footgun that could recur. Recommend creating this entry in Sprint 9.

### Pattern: Lightweight Sprint Model
Sprint 8.1 demonstrates that small follow-up sprints work well for clearing blockers and landing deferred work. The overhead is low and it keeps the pipeline moving.

---

## Summary

Sprint 8.1 was small but impactful. The branch protection fix by Riv was the standout — it unblocked the entire PR merge pipeline. KB entries from Sprint 8 audit were successfully landed. One task deferred (dashboard timestamps), which is acceptable given it's in a different repo.

**Grade rationale:** B+ rather than A because one task was deferred and the sprint was reactive (fixing a blocker) rather than advancing features. But the infrastructure fix was critical and well-executed.
