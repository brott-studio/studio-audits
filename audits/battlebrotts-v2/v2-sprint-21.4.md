# Sub-Sprint Audit — S21.4 (Interruption → Flow)

**Sub-sprint:** S21.4
**Arc:** Arc B — Content & Feel
**Date:** 2026-04-24T03:42Z
**Grade:** **B+**
**PRs:**
- [brott-studio/battlebrotts-v2#254](https://github.com/brott-studio/battlebrotts-v2/pull/254) — `feat(ux): #105 preserve scroll offset in shop/loadout on child tap`
- [brott-studio/battlebrotts-v2#255](https://github.com/brott-studio/battlebrotts-v2/pull/255) — `feat(ux): #106 random-event popup redesign — named anchor + skip button + dampening`
- [brott-studio/battlebrotts-v2#256](https://github.com/brott-studio/battlebrotts-v2/pull/256) — `feat(ux): #108 league progression surfacing — two-surface`
- [brott-studio/battlebrotts-v2#257](https://github.com/brott-studio/battlebrotts-v2/pull/257) — `fix(ux): #106 hot-patch — Engine.get_ticks_msec → Time.get_ticks_msec`
**Merge SHAs on `main`:** `8c03676c` (#254), `87170f9d` (#255), `81f0e932` (#256), `97cca322` (#257, hot-patch — final state)
**Scope streak:** Arc B sub-sprint 4 of open fuse
**Idempotency key:** `sprint-21.4`

---

## One-line rationale

S21.4 closed 3 UX friction issues (#105, #106, #108) across 3 PRs — all-pass on PR-A and PR-C; PR-B shipped a Godot 4.4 API regression (`Engine.get_ticks_msec` → `Time.get_ticks_msec`) caught only by Optic post-merge, requiring a hot-patch (PR-B.1 #257) before this audit could close. Hot-patch landed cleanly with corrected test-assertion semantics. Full suite 46/46 on final SHA `97cca322`. The regression was caught at the right gate (Optic), but missed at an earlier gate (Boltz), holding the grade from A to B+.

---

## Scope summary

S21.4 is sub-sprint 4 of Arc B (theme: "Interruption → Flow"). Three distinct UX friction points addressed in parallel:

### What shipped — PR-A #254 (issue #105 — scroll preservation)

- **`godot/shop.gd`** and **`godot/loadout.gd`**: `ScrollContainer` scroll-offset preserved across child-tap interactions. Previously, tapping any item in a scrolled list reset the viewport to top, breaking user flow mid-browse.
- **Tests (`test_s21_4_scroll_preservation.gd`)**: Covers scroll-offset round-trip (save/restore), no-reset-on-tap, and edge cases.
- **3 commits** (1 feat + 2 test fixes): `ed2d2d47`, `6a7fc638`, `1339f9f5`
- **+253 / −3, 4 files**. Boltz initial CHANGES_REQUESTED (review `4167474977`), then APPROVED after fixes (review `4167496813`). Merged `8c03676c` at 2026-04-24T02:40Z. ✅

### What shipped — PR-B #255 (issue #106 — random-event popup)

- **`godot/event_popup.gd`** (new or extended): Named-anchor positioning, skip button, dampening (suppresses repeat popups within a session window).
- **Tests included** in same file.
- **1 commit** (`6b1e880c`): `feat(ux): #106 random-event popup redesign — named anchor + skip button + dampening`
- **+363 / −0, 3 files**. Boltz APPROVED (review `4167556915`). Merged `87170f9d` at 2026-04-24T02:57Z.
- ⚠️ **Shipped regression:** `Engine.get_ticks_msec()` used for dampening timer — deprecated/removed in Godot 4.4; should be `Time.get_ticks_msec()`. CI silent-0-assertion gap allowed this to exit 0 despite the API misuse. Optic post-merge verification caught it.

### What shipped — PR-B.1 #257 (hot-patch — fixes #255 regression)

- **Minimal fix:** `Engine.get_ticks_msec` → `Time.get_ticks_msec` across implementation + tests.
- **Test-assertion semantics corrected:** state-variable check (`_last_event_time_msec`) preferred over node-query for `queue_free` — tighter assertion semantics.
- **1 commit** (`badb2edd`): `fix(ux): #106 hot-patch — Engine.get_ticks_msec → Time.get_ticks_msec`
- **+6 / −5, 2 files**. Boltz APPROVED (review `4167671322`). Merged `97cca322` at 2026-04-24T03:35Z. ✅

### What shipped — PR-C #256 (issue #108 — league surfacing)

- **`godot/result_screen.gd`** (and related): Two-surface league progression indicator — `NextLeaguePathIndicator` label on ResultScreen + BrottBrain unlock label, conditioned on `bronze_unlocked` gate.
- **Tests (`test_s21_4_league_progression.gd`)**: Covers both surfaces, gate logic, and edge conditions.
- **2 commits** (`d30c148e`, `ca191075`): feat + test split.
- **+249 / −0, 4 files**. Boltz APPROVED (review `4167593297`). Merged `81f0e932` at 2026-04-24T03:09Z. ✅

### Issues closed this sprint

- **#105** — Scroll behavior; closed at PR-A #254 merge. ✅
- **#106** — Random-event popup; closed at PR-B + PR-B.1 merged chain. ✅
- **#108** — League surfacing; closed at PR-C #256 merge. ✅

---

## PR status

| PR | Title | State | Commits | +/− | Files | Reviews |
|----|-------|-------|---------|-----|-------|---------|
| [#254](https://github.com/brott-studio/battlebrotts-v2/pull/254) | `feat(ux): #105 preserve scroll offset` | merged `8c03676c` | 3 | +253 / −3 | 4 | CHANGES_REQUESTED → APPROVED (Boltz `4167474977`→`4167496813`) |
| [#255](https://github.com/brott-studio/battlebrotts-v2/pull/255) | `feat(ux): #106 random-event popup redesign` | merged `87170f9d` | 1 | +363 / −0 | 3 | APPROVED (Boltz `4167556915`) |
| [#257](https://github.com/brott-studio/battlebrotts-v2/pull/257) | `fix(ux): #106 hot-patch Engine→Time API` | merged `97cca322` | 1 | +6 / −5 | 2 | APPROVED (Boltz `4167671322`) |
| [#256](https://github.com/brott-studio/battlebrotts-v2/pull/256) | `feat(ux): #108 league progression surfacing` | merged `81f0e932` | 2 | +249 / −0 | 4 | APPROVED (Boltz `4167593297`) |

---

## CI state on final SHA `97cca322`

All required check-runs PASS:

- `Optic Verified` — **success** ✅
- `Post Optic Verified check-run` — **success** ✅
- `Playwright Smoke Tests` — **success** ✅
- `Godot Unit Tests` — **success** ✅
- `update` — **success** ✅
- `Detect changed paths` — **success** ✅

Full suite: **46/46** tests passing. Playwright green. Audit Gate green.

---

## Spec invariants coverage

### PR-A #254 — issue #105 (scroll preservation)

| Invariant | Status | Evidence |
|-----------|--------|----------|
| Scroll offset preserved on child-tap (shop) | ✅ PASS | Test `test_s21_4_scroll_preservation.gd`; Optic all-pass |
| Scroll offset preserved on child-tap (loadout) | ✅ PASS | Same test file; both surfaces covered |
| No scroll-reset on navigation events unrelated to child-tap | ✅ PASS | Optic re-verify `8c03676c` all-pass |

Boltz: initial CHANGES_REQUESTED then APPROVED — iteration caught and resolved test-fixture issues before merge. Process correct.

### PR-B #255 → PR-B.1 #257 — issue #106 (random-event popup)

| Invariant | Status | Evidence |
|-----------|--------|----------|
| Named-anchor popup positioning | ✅ PASS | Optic final verify `97cca322` all-pass |
| Skip button present and functional | ✅ PASS | Optic all-pass |
| Dampening (repeat-suppression) — correct timer API | ⚠️ PARTIAL → ✅ FIXED | PR-B `87170f9d` shipped `Engine.get_ticks_msec` regression; PR-B.1 `97cca322` fixed to `Time.get_ticks_msec`. Final state: PASS. |
| Test assertions on dampening use state-var (not node query) | ✅ PASS (post-fix) | PR-B.1 corrected assertion semantics. Optic all-pass. |

Net: all invariants PASS at audit close. However, PR-B shipped a correctness regression to main before the fix landed — this is the grade-determining signal.

### PR-C #256 — issue #108 (league surfacing)

| Invariant | Status | Evidence |
|-----------|--------|----------|
| `NextLeaguePathIndicator` visible on ResultScreen when `bronze_unlocked` | ✅ PASS | Tests + Optic all-pass `81f0e932` |
| BrottBrain unlock label visible when `bronze_unlocked && brottbrain_unlocked` | ✅ PASS | Tests + Optic all-pass |
| Both surfaces gated correctly (not shown before unlock) | ✅ PASS | Test gate-logic coverage confirmed |

---

## Quality assessment

### Code quality

- **PR-A (#254):** Clean implementation. Boltz's initial changes-request resulted in test-fixture correction (assert inversion for `follow_focus` compatibility with S17.1-001 AC-1). Merge state is solid. +253 lines is appropriate for the scope.
- **PR-B (#255):** Implementation concept is correct; Godot 4.4 API surface area error on `Engine.get_ticks_msec`. This is a factual error — Nutts used the Godot 3.x / pre-4.4 API. The regression was not present in the design; it's an implementation error in a real API detail. Size: 363 lines — crossed the B4a early-warning threshold (350 lines) without pinging Ett. Both the API error and the size breach are signals. Boltz missed the API misuse in review (Godot 4.4 API familiarity gap).
- **PR-B.1 (#257):** Minimal, tight hot-patch. +6 / −5 lines. Corrected both the API call and the test-assertion semantics (state-var > node-query). Exemplary hot-patch discipline — no scope creep, no collateral changes.
- **PR-C (#256):** Clean. Two-commit split (feat + tests) is correct hygiene. +249 lines within the B4a threshold. All-pass.

### Test quality

- **PR-A:** Test file present, assertions corrected iteratively during Boltz review. Covered both scroll surfaces. Final state: sound.
- **PR-B / PR-B.1:** Test assertions included in original PR; semantics corrected in hot-patch (state-var assertion replaces fragile node-query for `queue_free` state). Improved by the incident.
- **PR-C:** Test file in a separate commit (`ca191075`) from feat (`d30c148e`) — correct split. Coverage: both surfaces + gate logic.

**Overall:** Tests present on all PRs. No "I'll add tests in a follow-up" violations. The PR-B test-assertion issue was caught and corrected in the hot-patch. Net test coverage: sound.

### Scope discipline

- **PR-A (#254):** On-scope. Touches only scroll preservation. ✅
- **PR-B (#255):** On-scope for #106. Crossed B4a (363 lines) without early-warning ping to Ett. ⚠️ (not blocking, but a hygiene flag)
- **PR-B.1 (#257):** On-scope hot-patch. Minimal. ✅
- **PR-C (#256):** On-scope. Under B4a threshold (249 lines). ✅

### Pipeline hygiene

- **PR-A:** Normal Boltz review loop (CHANGES_REQUESTED → APPROVED). Correct.
- **PR-B:** Boltz APPROVED in single pass, missed `Engine.get_ticks_msec` API regression. Godot 4.4 API familiarity gap.
- **Hot-patch (PR-B.1):** Riv (The Bott) autonomously chose to hot-patch before audit under `quality-over-speed` standing rule. Correct call — auditing on top of a known regression would have produced a misleading ground truth.
- **Optic:** Caught the regression on its post-merge verification pass. Optic is working as intended — post-merge verification is the last structural gate.
- **CI silent-0-assertion gap:** Allowed PR-B to merge with a broken API call because the test runner exited 0 despite the misuse (likely parse-safe code that only fails at runtime). This is the structural gap that needs fixing. See carry-forwards.

---

## openclaw tasks audit — S21.4 sprint window

`openclaw tasks audit` run at audit time: **116 findings · 5 errors · 111 warnings**.

Sprint-relevant findings:
- `stale_running` (5 errors) — 5 tasks flagged stuck (ages 23h1m to 7d9h). Pre-existing pattern from earlier arcs; sentinel-sweep cron (#44) would resolve. No new stale_running tasks attributable to S21.4.
- `delivery_failed` (1 warning) — `8d71e55b` task, pre-existing, same as S21.3 snapshot.
- `inconsistent_timestamps` (111 warnings) — bulk harness-level clock skew pattern; pre-existing baseline, not sprint-specific.

No new task health regressions attributable to S21.4.

---

## Pipeline hygiene notes

1. **B4a early-warning: PR-B crossed 350 lines (363) without pinging Ett.** PR-C respected the threshold (249). The B4a signal exists for this exact reason — larger PRs carry more risk of API surface errors (as demonstrated). For S21.5 or future sub-sprints, Nutts should invoke the early-warning at 350 lines even in a parallel-PR sub-sprint.

2. **Boltz Godot 4.4 API familiarity gap.** `Engine.get_ticks_msec` vs `Time.get_ticks_msec` is a known 4.x API migration change. Boltz's review missed it. This is a knowledge-base gap, not a motivation gap. A Godot 4.4 API migration checklist in the KB (or in Boltz's review profile) would catch future misuses. Candidate carry-forward for studio-framework.

3. **CI silent-0-assertion gap.** This is the structural root cause that let the regression through CI pre-merge. See carry-forward Issue 1 below.

4. **Ett/Gizmo design-resolution loop:** Worked well this sub-sprint — Ett surfaced 2 named-identifier gaps (popup anchor node name, league surface label name), Gizmo adjudicated, Ett re-emitted spec invariants. This is the correct pattern for resolving spec ambiguity mid-sprint.

5. **Hot-patch autonomy (quality-over-speed):** Riv's autonomous decision to hot-patch before audit was correct under the standing `quality-over-speed` rule. Audit ground-truth accuracy preserved. The decision also correctly prioritized fixing to main (structural gate) over speed-to-audit.

---

## Carry-forwards

### Issue 1 — CI silent-0-assertion gap [framework, medium-high priority] (#258)

**Context:** PR-B (#255) merged with `Engine.get_ticks_msec` (wrong API for Godot 4.4) because the test runner exited 0 — the test file was syntactically/parse-safe but the API misuse only manifests at runtime. The CI exit-code gate is insufficient when a test script no-ops due to dependency parse errors or missing runtime context.

**Proposed fix (Boltz, from PR #257 review comment):** Fail the CI step on any `T == 0` Results block or on missing test results entirely. A test run that reports zero assertions should be treated as a structural CI failure, not a pass.

**Priority:** medium-high. **Area:** `area:ci`, `area:framework`. Bundle into S21.5 or a framework-hardening sprint. Filed as [#258](https://github.com/brott-studio/battlebrotts-v2/issues/258).

### Issue 2 — Visual overlap: NextLeaguePathIndicator + BrottBrain label [ux, low priority] (#259)

**Context:** `NextLeaguePathIndicator` (y=418) and BrottBrain unlock label (y=420) visually overlap on ResultScreen when both `bronze_unlocked && brottbrain_unlocked` are true simultaneously. PR-C (#256) was correct-by-spec but the layout collision is a visual polish issue discovered in Boltz review.

**Proposed fix:** Adjust vertical positioning — either stack with a 24px gap or conditionally offset one label when both are shown. Non-correctness, layout-polish only.

**Priority:** low. **Area:** `area:ux`. Defer to a UX-polish sprint. Filed as [#259](https://github.com/brott-studio/battlebrotts-v2/issues/259).

### Issue 3 — "Bronze" hardcoded in league-progression helpers [tech-debt, low priority] (#260)

**Context:** `_next_league_path_text()` and `_league_progress_indicator_text()` helpers in the league surfacing code hardcode `"Bronze"`. Currently correct (only bronze unlock is gated; `bronze_unlocked` is the sentinel), but will need generalization when silver/gold league unlock is implemented. Boltz flagged in PR #256 review.

**Proposed fix:** Parameterize the league name through a constant or enum lookup. Low urgency until silver/gold content is added.

**Priority:** low. **Area:** `area:game-code`. File for future league-expansion sprint. Filed as [#260](https://github.com/brott-studio/battlebrotts-v2/issues/260).

---

## Arc B status — is S21.4 the final sub-sprint?

Based on `memory/active-arcs.json`:

- Arc B scope seeds: `#112 Bronze content`, `#103/#104/#107 UX bundle`, `audio foundation`.
- **Bronze content (#112):** Closed S21.1 ✅.
- **UX bundle (#103/#104/#107):** #103 and #104 closed S21.2 ✅; #107 (arena onboarding) closed S21.3 ✅.
- **Additional UX issues (#105/#106/#108):** Closed this sub-sprint (S21.4) ✅.
- **Audio foundation:** Not addressed in any S21.x sub-sprint yet. **Scope seed not closed.**

**Assessment:** Arc B cannot close after S21.4 — the audio foundation scope seed is unaddressed. S21.5 should target audio foundation (or confirm audio is deferred/descoped). Ett should perform the continue-or-complete check at S21.5 framing entry and adjudicate whether audio is in or out of Arc B.

If audio is descoped from Arc B, this audit is the effective content-and-UX-complete marker and Arc B could close after an Ett continue-or-complete ruling. That decision is Et's / Riv's, not Specc's.

---

## Compliance-reliant process detection

### 1. B4a early-warning (compliance-reliant)

PR-B (#255) crossed 350 lines without pinging Ett. The B4a rule is in Nutts's profile as a compliance-reliant signal. No structural gate enforces it. Risk: **low** (the behavior is only a risk amplifier, not itself a defect generator). Recommendation: Add a CI lint step that warns (not fails) on PRs with +350 added lines and no `[B4a]` tag in the PR title or body. This would convert a compliance-reliant rule to a soft structural signal.

### 2. Boltz API familiarity (compliance-reliant)

Boltz's review of PR-B missed the `Engine.get_ticks_msec` → `Time.get_ticks_msec` regression. Review thoroughness for Godot 4.4 API surface is compliance-reliant — no CI check catches deprecated API calls pre-merge. Risk: **medium** (will recur as Godot 4.x API changes accumulate). Recommendation: Add a KB entry for Godot 3.x→4.x API migration checklist; add it to Boltz's review profile cross-references. Medium-term: explore a GDScript deprecation linter in CI.

### 3. CI silent-0-assertion gap (structural gap — carry-forward filed)

Already documented as carry-forward Issue 1 above. Risk: **medium-high** (allows tests to silently no-op and exit 0). This is an existing structural gap, not a new detection. Fix tracked in carry-forward.

---

## 🎭 Role Performance

**Gizmo:** Shining: Ett/Gizmo design-resolution loop for S21.4 worked well — Ett surfaced 2 named-identifier gaps (popup anchor, league surface), Gizmo adjudicated, Ett re-emitted with concrete invariants. This kept spec ambiguity from bleeding into implementation. Struggling: No S21.4-specific Gizmo failures to note. Trend: →.

**Ett:** Shining: Plan emitted with concrete named-identifier invariants (popup anchor node name, league surface label name) after the Gizmo design-resolution loop. The parallel-PR structure (3 independent tasks, 3 PRs) was cleanly scoped. Struggling: B4a threshold crossing on PR-B was not flagged in the plan itself — the plan could have set a size budget per task. Trend: →.

**Nutts:** Shining: PR-A and PR-C were both clean — correct APIs, correct test coverage, correct scope. PR-B.1 hot-patch was tight and minimal, with improved assertion semantics (state-var over node-query). Good recovery after the regression. Struggling: PR-B shipped `Engine.get_ticks_msec` regression — factual API error on Godot 4.4 surface area. Crossed B4a threshold (363 lines) without pinging. Trend: → (consistent pattern of solid builds with occasional API-surface errors on new Godot 4.x API territory).

**Boltz:** Shining: Reviews on PR-A, PR-C, and PR-B.1 were all appropriate. PR-A correctly triggered CHANGES_REQUESTED and the iteration was correctly resolved. PR-B.1 (hot-patch) was reviewed and approved correctly — Boltz verified the fix was minimal and the assertion semantics improvement was flagged as an improvement (not a concern). `NextLeaguePathIndicator` visual overlap caught in PR-C review (Issue 2 above). League-generalization hardcoding flagged in PR-C review (Issue 3 above). Struggling: Missed `Engine.get_ticks_msec` → `Time.get_ticks_msec` in PR-B review. This is a Godot 4.4 API familiarity gap — the API change was introduced in Godot 4.x and Boltz's review did not flag it. Trend: → (consistently good on structural/design review; knowledge gap on Godot 4.x API surface persists).

**Optic:** Shining: Caught the `Engine.get_ticks_msec` regression in post-merge verification — the exact role Optic is supposed to play as the last structural gate. Runtime failure was correctly identified and escalated (via failing check-run), triggering the hot-patch loop. Full suite 46/46 on final SHA `97cca322`. Playwright green. Struggling: No S21.4-specific Optic failures. Trend: → (post-merge gate is reliable; the screenshot-evidence gap (#247) persists but is not Optic's sprint-level failure).

**Riv:** Shining: Autonomous hot-patch decision under `quality-over-speed` was correct — Riv did not audit on top of a known regression, which would have produced misleading audit ground truth. Three-PR parallel orchestration completed cleanly. Struggling: No S21.4-specific Riv failures beyond the PR-B regression response (which was correct). Trend: →.

---

## Grade

**B+**

**Rationale:** S21.4 delivered all three target UX friction fixes (#105, #106, #108) and closed all three issues. PR-A and PR-C were clean all-pass deliveries. PR-B.1 (hot-patch) was tight and correct. Optic functioned as intended — post-merge verification caught the regression and triggered the fix.

Grade held from A− to B+ by:
1. **Shipped regression on PR-B (#255):** `Engine.get_ticks_msec` API error shipped to main. This is "caught at the right gate" but "missed at an earlier gate we care about" — specifically: Boltz review missed it, CI silent-0-assertion gap allowed exit 0 despite the misuse. Under quality-over-speed, a regression that ships to main and requires a hot-patch is a meaningful quality signal even when fixed cleanly.
2. **B4a threshold breach on PR-B** (363 lines, no early-warning ping): hygiene signal reinforcing the size→risk correlation.

Not graded below B+ because:
- All three issues are closed and all invariants PASS at audit close.
- The regression was caught and fixed before this audit ran (hot-patch merged before Specc spawned).
- Root cause is identified at both the agent level (Nutts API error, Boltz familiarity gap) and the structural level (CI silent-0-assertion gap).
- Recovery was disciplined — minimal hot-patch, improved assertion semantics, no scope creep.

**Scope streak:** 4 clean single-scope sub-sprints in Arc B (each closing exactly its targeted issues, no scope drift). ✅

---

## Appendix A — Issue tracker hygiene

| Issue | Status | Action this sprint |
|-------|--------|--------------------|
| #105 | Closed ✅ | Closed at PR-A #254 merge (`8c03676c`) |
| #106 | Closed ✅ | Closed at PR-B #255 + hot-patch #257 (`97cca322`) |
| #108 | Closed ✅ | Closed at PR-C #256 merge (`81f0e932`) |
| [#258](https://github.com/brott-studio/battlebrotts-v2/issues/258) | Open → filed | CI silent-0-assertion gap (see carry-forwards §) |
| [#259](https://github.com/brott-studio/battlebrotts-v2/issues/259) | Open → filed | Visual overlap NextLeaguePathIndicator + BrottBrain label |
| [#260](https://github.com/brott-studio/battlebrotts-v2/issues/260) | Open → filed | "Bronze" hardcoded in league-progression helpers |
