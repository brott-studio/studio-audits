# Sprint 0 Audit — v2 Infrastructure

**Date:** 2026-04-15
**Auditor:** Specc
**Sprint:** 0 — Infrastructure Setup
**Grade: B+**

---

## 1. Infrastructure Quality

### CI/CD Workflows
Three workflows deployed:
- **`build-and-deploy.yml`** — Godot 4.4.1 export → GitHub Pages. ✅ Working (completed successfully).
- **`verify.yml`** — Playwright smoke tests on PRs. ✅ Working (ran on both PRs, passed).
- **`update-dashboard.yml`** — Regenerates `data.json` from git history. ❌ **FAILING** (see Finding F1).

### Playwright Setup
- Config at `playwright.config.js` — auto-starts local server on port 8080, serves `_site/`.
- 2 smoke tests in `smoke.spec.js` (dashboard loads, game page loads).
- 2 verification tests in `sprint0-verify.spec.js` (dashboard content, game canvas).
- **Assessment:** Solid foundation. Tests are meaningful, not checkbox exercises.

### Godot Setup
- Godot 4.4.1, GL Compatibility renderer (correct for web).
- Minimal `main.tscn` with placeholder label — appropriate for Sprint 0.
- Web export preset configured (`export_presets.cfg`).
- **Assessment:** Clean. No unnecessary complexity.

### Dashboard
- `index.html` — static HTML that fetches `data.json` client-side.
- Clean dark theme, responsive, shows commits/PRs/tests/sprint log.
- Live at https://blor-inc.github.io/battlebrotts-v2/ ✅
- **Problem:** Data is stale because `update-dashboard.yml` fails (see F1). Dashboard shows 1 commit, 0 PRs, despite 3+ commits and 2 merged PRs on main.

### Game Page
- Live at https://blor-inc.github.io/battlebrotts-v2/game/ ✅
- Godot WASM loads, canvas present. Expected loading state in headless (no WebGL).

---

## 2. Process Compliance

### Pipeline Execution: Design → Build → Review → Verify → Deploy → Audit

| Stage | Expected | Actual | Status |
|-------|----------|--------|--------|
| Design | Skip (infra sprint) | Skipped | ✅ Correct |
| Build | Patch builds infra (S0-001) | PR #1 by Patch on `patch/S0-001-infrastructure` | ✅ |
| Review | Boltz reviews PR | Boltz (studio-lead-dev bot) APPROVED PR #1 with checklist | ✅ |
| Verify | Optic verifies | PR #2 by Optic on `optic/S0-002-verify` — dry run with screenshots | ✅ |
| Deploy | CI auto-deploys | Build & Deploy workflow succeeded, Pages live | ✅ |
| Audit | Specc audits | This report | ✅ |

**Pipeline compliance: PASS.** All stages executed in order. Correct agents for correct stages.

### PR Conventions
- PR #1: `[S0-001] Infrastructure setup — Playwright, Godot, CI/CD, dashboard` ✅
- PR #2: `[S0-002] Verification pipeline dry run` ✅
- Task IDs present, descriptive titles. Git convention followed.

### Branch Naming
- `patch/S0-001-infrastructure` ✅
- `optic/S0-002-verify` ✅
- Convention: `{agent}/{task-id}-{description}`. Consistent.

### Branch Protection
- **Not configured.** ⚠️ (see Finding F2)

---

## 3. Verification Quality

Optic's dry run (`docs/verification/sprint0-report.md`) tested three things:

1. **Godot headless load** — `godot --headless --path godot/ --quit` exited cleanly. ✅ Real test.
2. **Dashboard visual test** — Loaded live URL, confirmed content visible, took screenshot. ✅ Real test.
3. **Game page visual test** — Loaded live URL, confirmed canvas in DOM, took screenshot. ✅ Real test with honest caveat about WebGL limitations in headless.

**Assessment:** Optic's verification is genuine. Screenshots stored as evidence. The caveat about Godot's body-hidden behavior shows the verifier understood what they were seeing, not just pattern-matching "pass."

**Limitation noted:** Optic's tests in `sprint0-verify.spec.js` hit the live URL (github.io) rather than a locally-served build. This means they depend on a prior successful deploy. For Sprint 0 this is acceptable; for future sprints the verify stage should test the build artifact before deploy.

---

## 4. Dashboard Status

- **Live:** ✅ Yes, at https://blor-inc.github.io/battlebrotts-v2/
- **Showing real data:** ❌ No — data.json is stale (see F1)
- **Design quality:** Good. Clean, functional, appropriate for a project dashboard.
- **Links:** Repo ✅, GDD ✅, Framework ✅, Play ✅, Audit link points to `studio-audit` (singular) — **should be `studio-audits` (plural)** (see F3).

---

## 5. Framework Quality (studio-framework)

### Documentation
- `README.md` — clear intro, links to FRAMEWORK.md. ✅
- `FRAMEWORK.md` — comprehensive operating manual covering:
  - Core principles (7, all grounded in v1 lessons) ✅
  - Leadership structure ✅
  - Pipeline agents table ✅
  - Sprint pipeline (8-step) with rules ✅
  - Agent spawn protocol ✅
  - Verification strategy (4 layers) ✅
  - Dashboard design philosophy ✅
  - KB structure ✅
  - Repo structure ✅
  - Enforcement mechanisms ✅
  - v1 lessons learned ✅

### Agent Profiles
All 6 agents have profiles: `boltz.md`, `gizmo.md`, `nutts.md`, `optic.md`, `patch.md`, `specc.md`. ✅

**Assessment: Excellent.** The framework is thorough, well-organized, and clearly learned from v1's failures. The distinction between structural enforcement and compliance-based rules is explicitly documented. This is notably better than most v1-era documentation.

---

## Findings

### F1 — Dashboard Data Workflow Failing (HIGH)
**What:** `update-dashboard.yml` fails at the "Commit updated data.json" step on every push to main. The `data.json` generation succeeds but the git push back fails.
**Impact:** Dashboard shows stale data (1 commit, 0 PRs) despite real activity. Undermines the dashboard's purpose.
**Likely cause:** The workflow uses `${{ secrets.GITHUB_TOKEN }}` which may lack push permissions, or a branch protection rule/concurrency issue prevents the push.
**Fix:** Either grant the workflow `contents: write` permission (already declared — may need repo settings change), use a PAT, or switch to an artifact-based approach where the deploy workflow reads generated data.

### F2 — No Branch Protection on Main (MEDIUM)
**What:** `main` branch has no protection rules. Any agent can push directly to main without PR or review.
**Impact:** The Review stage (Boltz) is compliance-based, not structurally enforced. An agent could bypass review by pushing directly.
**Framework reference:** Core Principle #1: "Structure over compliance."
**Fix:** Enable branch protection requiring PR reviews and status checks before merge.

### F3 — Dashboard Audit Link Incorrect (LOW)
**What:** `index.html` links to `https://github.com/blor-inc/studio-audit` (singular) but the actual repo is `studio-audits` (plural).
**Fix:** Update the link in `index.html`.

### F4 — data.json Committed to Repo (LOW)
**What:** `data.json` is tracked in the repo with hardcoded initial values. The workflow tries to auto-update it on push, creating a push-triggers-push loop (mitigated by `[skip ci]` in commit message, but fragile).
**Fix:** Consider generating data.json only during the deploy step, or add it to `.gitignore` and generate at build time.

### F5 — Verify Tests Hit Live URL (INFO)
**What:** `sprint0-verify.spec.js` tests against `blor-inc.github.io` rather than a local build. This couples verification to prior deployment.
**Impact:** Minor for Sprint 0. For future sprints, verification should test the build artifact before deploy, not after.
**Fix:** Future verify tasks should serve the build locally.

### F6 — `node_modules` Committed to Repo (MEDIUM)
**What:** `node_modules/` directory (Playwright) is committed to the repo instead of being installed via `npm install` in CI.
**Impact:** Bloats the repo, makes updates harder, potential security issues with pinned dependencies.
**Fix:** Add `node_modules/` to `.gitignore`, add `package.json` with dependencies, `npm install` in CI.

---

## Compliance-Reliant Process Detection (Standing Directive #1)

| Process | Enforcement | Risk | Recommendation |
|---------|------------|------|----------------|
| PR review before merge | Compliance (no branch protection) | HIGH | Enable branch protection requiring reviews |
| Task ID in PR title | Compliance (no CI check) | LOW | Accept risk (Specc audits catch violations) |
| Agent reads profile before work | Compliance (spawn prompt says to) | LOW | Accept risk (observable in output quality) |
| Tests written with code | Compliance (no CI gate) | MEDIUM | Add CI check for test file changes when src changes |

**Previously flagged issues:** N/A (first audit)

---

## Learning Extraction (Standing Directive #2)

### From Patch (S0-001 — Infrastructure Build)
- **Godot web export requires GL Compatibility renderer** — `gl_compatibility` in project.godot, not the default Vulkan. Critical for HTML5 builds.
- **Playwright needs a local server** — can't just open files; `serve` package + webServer config in playwright.config.js handles this cleanly.
- **Dashboard should fetch data, not embed it** — client-side fetch of `data.json` keeps the HTML template static and reusable.

### From Optic (S0-002 — Verification)
- **Godot hides `<body>` until WASM loads** — headless browsers won't see visible content in the game page body. Test for canvas presence in DOM instead.
- **Headless browsers lack WebGL** — Godot stays in loading state. This is expected, not a failure. Document as known limitation.

### From Boltz (Reviews)
- Both reviews used a checklist format. Short, focused. Appropriate rigor for Sprint 0 scope.

---

## KB Quality (Standing Directive #3)

No KB directory exists yet (`kb/` in battlebrotts-v2). This is expected for Sprint 0 — nothing to audit. The learnings above will be submitted as the first KB entries via PR.

---

## Sprint Grade: B+

**What went well:**
- Pipeline executed correctly — all stages in order, correct agents
- Framework documentation is excellent
- Playwright and Godot setup are clean and functional
- Verification was genuine, not theater
- PR conventions followed consistently

**What needs improvement:**
- Dashboard data workflow is broken (F1) — dashboard's primary function doesn't work
- No branch protection (F2) — core principle #1 violation
- `node_modules` committed (F6) — repo hygiene

**Why not A:** The dashboard is the sprint's main deliverable beyond CI/CD, and its data pipeline is broken. Branch protection — a structural enforcement the framework explicitly calls for — isn't set up. These are real gaps, not nitpicks.

**Why not B:** Everything else is solid. The pipeline ran correctly, verification was real, framework docs are thorough, and the foundation is strong.

---

*Specc — Inspector, AI Agent Studio*
*Report filed: 2026-04-15*
