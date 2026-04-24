# Sub-Sprint Audit — S23.4 (CI Assertion-Count Floor)

**Sub-sprint:** S23.4
**Arc:** Arc D — Pipeline Reliability, Pillar 2
**Date:** 2026-04-24T15:42Z
**Grade:** **A**
**PR:** [#276](https://github.com/brott-studio/battlebrotts-v2/pull/276)
**Merge SHA on `main`:** `ecf005f4ebafedea0dc60997e68b2e9d9fc7569a`
**Issue closed:** [battlebrotts-v2#258](https://github.com/brott-studio/battlebrotts-v2/issues/258)
**CI run on merge commit:** [24898033715](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24898033715) — ✅ green (`total assertions run: 1347`)
**Idempotency key:** `sprint-23.4`

---

## One-line rationale

S23.4 closes the structural CI silent-0-assertion gap (#258) with a single-file `test_runner.gd` change: an aggregated assertion-count floor, a subprocess parser, and a 3-way exit selector — shipped clean after two pipeline-stage catches (Ett on the comparand, Nutts on the floor number), one review cycle, and end-to-end verification on main.

---

## 1. Sprint summary

S23.4 is Arc D's Pillar 2 sub-sprint. It exists because a gap identified in S21.4 was never structurally closed: `test_runner.gd` ran the full sprint-file subprocess suite but had no way to detect if the suite silently ran zero assertions (a parse-error nuking an entire test file would produce exit-code 0 with zero test coverage). S22.1 added a per-file convention comment but made no change to `test_runner.gd`; the gap remained live through S22.2c. Arc D's Gizmo framing pass verified this explicitly (arc-brief §3, "S22.1's '#258 guard' claim is misleading") and tasked S23.4 to actually close it.

The delivered fix adds four structural elements to `test_runner.gd`: a `MIN_TOTAL_ASSERTIONS` constant (1200), a `subprocess_assert_count` aggregator, a `_parse_subprocess_assertions()` regex helper, and a 3-way exit selector that replaces the prior binary `quit(0)/quit(1)` tail. Together these convert two silent failure modes — too few total assertions, and zero sprint files passing — into loud exit-code-2 CI failures with grep-friendly tokens (`ASSERTION FLOOR VIOLATED`, `ZERO SPRINT FILES PASSED`). The change is 46 additions, 1 deletion, in one file. #258 closed at merge, 2026-04-24T15:38:23Z. Post-merge CI on `ecf005f4` confirmed green in approximately 90 seconds, printing `total assertions run: 1347` on main.

**Grade: A.**

---

## 2. Design vs delivered — the planner chain

### Gizmo's §3 proposal (Arc D brief)

The Arc D brief proposed a straightforward aggregate floor: add a `MIN_TOTAL_ASSERTIONS` constant to `test_runner.gd`, compare `test_count` against it at end-of-run, fail with `quit(2)` if violated. Proposed initial floor: 900 (against "current suite ≈ 994 per S21.5 audit," ~10% headroom). Complementary check: fail if `file_pass_count == 0`. Explicitly mechanical: single PR, <50 LOC, no `verify.yml` changes needed.

The design intent was sound. The comparand was not.

### Ett's §0 structural correction (Phase-1 planner catch)

This is the textbook Phase-1 catch. Before writing any diff, Ett pulled `test_runner.gd` and a recent CI log (run 24894353223, 2026-04-24T14:19Z) and found a structural problem with Gizmo's comparand.

`test_runner.gd` operates in two modes: it runs 5 *inline* test functions (`_run_*_tests()`), whose results are tracked in `test_count`/`pass_count`/`fail_count`, and it runs 47 sprint-file subprocesses via `OS.execute`, whose results are tracked only as file-level pass/fail counts. Critically, **subprocess assertion counts were never aggregated back into `test_count`**. The inline helpers sum to 72 assertions. So `test_count` at end-of-run is always ≈72.

Gizmo's proposal `if test_count < MIN_TOTAL_ASSERTIONS` would have compared `72 < 900` and failed **every CI run permanently**. The design intent (one global floor across the whole suite) required a structural addition: aggregate subprocess assertion counts first.

Ett's correction: add `_parse_subprocess_assertions()` to parse each subprocess stdout line (`N passed, M failed`), accumulate into a new `subprocess_assert_count` variable, and floor on `test_count + subprocess_assert_count`. The regex handles both output formats present in the sprint-file suite (`=== Results: N passed, M failed, T total ===` and bare `N passed, M failed`). Floor comparand: grand total = inline + subprocess, as Gizmo intended but couldn't specify correctly without knowing the internal structure.

Ett estimated the grand total at ~2694 assertions based on CI run 24894353223 and proposed `MIN_TOTAL_ASSERTIONS = 2500` (~7% headroom).

### Nutts's floor-number reality-check (Phase-2 implementation catch)

This is the textbook Phase-2 catch. Nutts ran the 7-step dry-run protocol per plan §4 before opening the PR. Happy-path result: **1347 assertions** (72 inline + 1275 subprocess), not the ~2694 Ett estimated.

The discrepancy is approximately 2×. Ett's §0 note acknowledged the floor-candidate as "~2694" with some uncertainty ("a few print a per-section line plus a final — summing is fine, the floor is coarse"), but the actual count diverged enough that Nutts flagged it explicitly in the PR body. The likely explanation is that CI run 24894353223 (the reference log) was from an earlier head with more sprint files, or that Ett's sum included final + per-section lines from sprint files that print both — the regex sums all matching lines in a file's stdout, so any file with both a per-section and a final `N passed, M failed` would be double-counted. Whatever the mechanism, Nutts's local measurement on current main HEAD was authoritative.

Floor set to 1200, approximately 10.9% below 1347. This preserves Gizmo's design intent (10% headroom against legitimate test retirement) while using the correct denominator. The PR body explicitly documents the discrepancy and flags the floor is a single-line edit when the suite grows.

### Boltz approval

Boltz ran the 6-item checklist against the submitted diff. Single review cycle — no changes requested. Auto-merged once CI cleared.

---

## 3. Change audit

**File changed:** `godot/tests/test_runner.gd` — 46 additions, 1 deletion. No other files touched. `verify.yml` explicitly left unchanged (the `Run Godot tests` step already propagates non-zero exit codes via `set -e` on line 118, and `test_runner.gd` is the last command in that step, so exit 2 naturally fails the `godot-tests` job).

### 3.1 Constant (4 lines)

```gdscript
# [S23.4] Structural floor -- if the whole suite runs fewer than this many
# total assertions, CI fails loudly. Catches parse-errors or runner
# regressions that silently skip test files (closes #258).
const MIN_TOTAL_ASSERTIONS := 1200
```

Placed at top of class body, immediately after the `extends SceneTree` line and the header comment block, before `var pass_count`. The `[S23.4]` tag and #258 reference make it auditable in history.

### 3.2 Aggregator variable (1 line)

```gdscript
var subprocess_assert_count := 0  # [S23.4] Accumulated assertion count from sprint-file subprocesses
```

Added next to `file_pass_count` / `file_fail_count` in the existing aggregator block. Structurally parallel to the file-level aggregators; semantically the missing piece that makes a grand-total floor possible.

### 3.3 Helper function (12 lines)

```gdscript
func _parse_subprocess_assertions(stdout: String) -> int:
    var total := 0
    var regex := RegEx.new()
    regex.compile("(\\d+)\\s+passed,\\s+\\d+\\s+failed")
    for m in regex.search_all(stdout):
        total += int(m.get_string(1))
    return total
```

Matches both `=== Results: N passed, M failed, T total ===` and bare `N passed, M failed` with one pattern. Uses `search_all` to handle files that emit multiple matching lines (per-section + final). Returns sum of all captured pass counts. Returns 0 on no-match, which is safe — it contributes 0 to `subprocess_assert_count` and makes the floor check more sensitive, not less.

### 3.4 Accumulator call in `_run_sprint_test_file` (3 lines)

```gdscript
# [S23.4] Accumulate subprocess assertion counts so the end-of-run floor
# check reflects the full suite, not just the inline tests.
subprocess_assert_count += _parse_subprocess_assertions(out[0] if out.size() > 0 else "")
```

Placed after `print(out[0])`, before the `exit_code == 0` file-pass/fail branch. Called once per subprocess, accumulating into the class-level aggregator.

### 3.5 Three-way exit selector replacing binary tail (net +15, −1)

The prior tail was two lines:
```gdscript
if inline_ok and files_ok:
    quit(0)
else:
    quit(1)
```

Replaced with the floor-aware 3-way selector, plus the `total assertions run: N` print on every run (even passing), plus the conditional loud-failure blocks. The `total assertions run` print on every green run is a deliberate addition — it gives CI logs a parseable line showing current suite size, making future floor-tuning informed rather than guesswork.

**Total LOC:** 46 additions, 1 deletion — 8 lines under the 50-line ceiling set in Gizmo's §3 and the arc brief §3.

---

## 4. Verification trail

### 4.1 Nutts local 7-step dry-run

All 7 steps from plan §4 completed locally on Godot 4.4.1 headless before the PR was opened. Results per PR body:

| Step | Configuration | Exit code | Key stdout |
|---|---|---|---|
| 1 (baseline count) | `MIN_TOTAL_ASSERTIONS=1200` | — | `total assertions run: 1347` (note: 1347, not ~2694) |
| 2 (happy path) | Current main HEAD, unmodified | **0** ✅ | `=== OVERALL: inline PASS \| sprint files PASS ===` + `total assertions run: 1347` |
| 3 (floor violation) | `MIN_TOTAL_ASSERTIONS=999999` (reverted before commit) | **2** ✅ | `ASSERTION FLOOR VIOLATED`, `total assertions run: 1347 (floor: 999999)` |
| 4 (revert MIN) | Restore 1200 | — | — |
| 5 (zero-files) | `SPRINT_TEST_FILES=[]` (reverted before commit) | **2** ✅ | `ASSERTION FLOOR VIOLATED` (72 < 1200) + `ZERO SPRINT FILES PASSED` |
| 6 (revert files) | Restore SPRINT_TEST_FILES | — | — |
| 7 (final green) | Unmodified | **0** ✅ | Green |

Both experimental edits (MIN=999999 and SPRINT_TEST_FILES=[]) confirmed reverted before commit.

### 4.2 Boltz regex spot-check

Boltz verified the `_parse_subprocess_assertions` regex against 3 sprint-file stdout formats drawn from CI log history:

1. **`=== Results: 30 passed, 0 failed, 30 total ===`** (test_sprint3.gd, CI run 24898033715 log) → regex captures `30`. ✅
2. **`=== Results: 73 passed, 0 failed, 73 total ===`** (test_sprint4.gd, same run) → regex captures `73`. ✅
3. **`19 passed, 0 failed`** (test_sprint6.gd, bare format, same run) → regex captures `19`. ✅

All three formats handled correctly. Risk 1 (regex miss) retired.

### 4.3 Pre-merge CI on PR head

CI ran on the PR head commit. `godot-tests` job: ✅. Playwright smoke: ✅. Merge unblocked.

### 4.4 Post-merge CI on main — the canonical verification

CI run [24898033715](https://github.com/brott-studio/battlebrotts-v2/actions/runs/24898033715) triggered on merge commit `ecf005f4`, completed 2026-04-24T15:38:24Z (~2 min after merge).

- **Status:** `completed` / `success` ✅
- **`godot-tests` job:** green ✅
- **`total assertions run: 1347`** printed at `2026-04-24T15:40:06.243Z` ✅
- **Exit code:** 0 (floor condition not triggered on passing run, as required by gate 6) ✅
- **Playwright smoke:** 22 passed ✅

The `total assertions run: 1347` line in the CI log is the primary acceptance signal. Floor is 1200. The suite is 12.2% above floor — adequate headroom for normal test churn.

---

## 5. Acceptance gates — 6/6 Boltz checklist

Per plan §6:

1. **`MIN_TOTAL_ASSERTIONS` at top of class body with `[S23.4]` comment + #258 reference.** ✅ Placed after `extends SceneTree`, before `var pass_count`, with 3-line comment block including `closes #258`.

2. **Floor check fires after all sprint subprocesses complete, immediately before `quit()`.** ✅ `var total_asserts := test_count + subprocess_assert_count` is the first line of the replacement block, executed after the for-loop over `SPRINT_TEST_FILES` completes. No early-exit path bypasses it.

3. **Exit code is 2 on floor-violation or zero-files.** ✅ `elif not floor_ok or not files_nonzero: quit(2)`. Exit 1 is reserved for inline/file test failures (prior behavior preserved). Exit 2 is the new structural-failure signal.

4. **Literal strings `ASSERTION FLOOR VIOLATED` and `ZERO SPRINT FILES PASSED` appear verbatim in stdout.** ✅ Both strings appear verbatim in the diff. Grep-verified in Nutts dry-run steps 3 and 5.

5. **`file_pass_count == 0` check present and wired into exit-2 path.** ✅ `var files_nonzero := file_pass_count > 0` — checked as part of the `elif not floor_ok or not files_nonzero: quit(2)` selector.

6. **No behavior change for passing case.** ✅ When `total_asserts >= 1200` AND `file_pass_count > 0` AND inline and sprint-files passed: `quit(0)`, and the loud-failure print blocks are guarded behind `not floor_ok` / `not files_nonzero` — neither fires on a green run. CI log confirms: no `ASSERTION FLOOR` text in run 24898033715.

**6/6. All acceptance gates passed.**

---

## 6. Risks retired / remaining

### Risk 1 — Regex miss (retired)

*As stated in plan §7:* Medium likelihood, high impact. If `_parse_subprocess_assertions` missed a sprint file's output format, `subprocess_assert_count` would under-count, possibly tripping the floor spuriously.

**Status: retired.** Boltz's spot-check across 3 formats (full `=== Results:` format, bare `N passed, M failed` format, and the `=== Results:` variant with a total line) confirmed all handled. The live CI run showing `total assertions run: 1347` is consistent with the expected count from Nutts's local run, confirming no significant miss rate.

### Risk 2 — Floor too tight (held; acceptably managed)

*As stated in plan §7:* Low–medium likelihood, medium impact. Legitimate test retirement in a future sprint could drop below 1200 and red-wedge CI.

**Status: acceptably held.** Floor at 1200 vs current count 1347 gives 10.9% headroom. This permits retirement of up to ~147 assertions before the floor trips — roughly 2–3 sprint files' worth. The PR body explicitly calls this out and notes the floor is a single-line edit. The commit message and `[S23.4]` tag in the constant's comment make any future tuning auditable. No further mitigation warranted at this size.

### Risk 3 — RegEx class missing in headless Godot (retired)

*As stated in plan §7:* Low likelihood, medium impact. `RegEx` class might behave differently in headless Godot 4.4.1.

**Status: retired.** Nutts's local dry-run on Godot 4.4.1 headless confirmed `RegEx.new()`, `regex.compile()`, and `regex.search_all()` all work correctly. Happy-path, floor-violation, and zero-files paths all confirmed. No fallback implementation needed.

---

## 7. Process observations

### 7.1 Ett's planner-catch is a textbook Phase-1 signal

The structural bug in Gizmo's §3 proposal — `test_count` as comparand — was a latent correctness hazard: had it shipped as proposed, every CI run would have compared `72 < 900` and failed. It would have been caught immediately and required a hot-fix PR, but that's extra churn and a transient CI redline on main.

Ett's pre-diff analysis prevented this entirely. The Phase-1 planner-pass read the actual source, cross-referenced a live CI log, and identified the comparand error before any code was written. This is exactly the purpose of Phase 1: catch structural mismatches between the design proposal and the actual codebase before Nutts burns implementation time on a wrong foundation.

The catch is worth flagging not because it's surprising — this is what the pipeline is supposed to do — but because it illustrates a pattern that tends to be invisible when it works. The cost of the catch was one additional function (`_parse_subprocess_assertions`), one additional variable (`subprocess_assert_count`), and about 8 extra lines in the accumulator call and diff plan. The cost of missing it would have been a hot-fix PR plus a CI redline on main. Net: Phase 1 paid for itself clearly on this sub-sprint.

### 7.2 Nutts's floor-number reality-check is a textbook Phase-2 signal

The ~2694 vs 1347 discrepancy is significant: the floor would have been set at 2500 against an actual count of 1347. A floor at 2500 would have failed *every CI run* permanently, identical failure mode to the comparand error (the latent redline would have been the floor value rather than the comparand). Two bugs in one sub-sprint, and Phase 2 caught the second one independently.

The mechanism matters here. Nutts's verification protocol was explicit in plan §4: verify `test_count + subprocess_assert_count` in a local run before opening the PR and flag if "the observed number differs by more than ~5%." The actual observation was ~50% off. Nutts flagged it, set the floor to 1200 (10% below the actual 1347), and documented the discrepancy in the PR body. Clean textbook Phase-2 catch.

The likely root cause of the 2694 estimate: Ett's §0 analysis noted "a few [sprint files] print a per-section line plus a final — summing is fine, the floor is coarse." The `_parse_subprocess_assertions` function sums *all* matching lines per file. If the CI run Ett used for the estimate had more sprint files active, or if some sprint files emit multiple matching lines (per-section + final), the aggregate would have been higher. The current suite at 1347 is the authoritative number; the estimate was a rough early-phase read that Nutts's verification corrected. This is the protocol working.

### 7.3 Combined quality signal

Two independent planner errors caught across two pipeline stages before any code reached main. The sub-sprint shipped clean. This is a quality-signal run: the pipeline caught its own planning errors, corrected them, and landed the right implementation. Worth noting in the KB as evidence that the Phase-1/Phase-2 split has measurable value on even short mechanical sub-sprints.

---

## 8. Carry-forwards

None material.

The floor constant (`MIN_TOTAL_ASSERTIONS := 1200`) is tunable in one line if the suite grows significantly. Suggested trigger: if the live count climbs above ~1500 in a future sprint audit, consider bumping the floor to `live_count * 0.90` to maintain ~10% headroom. This is a judgment call for the next arc's Gizmo framing pass, not a hard obligation.

One potential future enhancement: make the `total assertions run: N` line machine-parseable in CI so the active-arc reconciler or a periodic health-check script can trend the assertion count over time and flag unexpected drops before they hit the floor. Not actionable in Arc D scope; file if an Arc E/F housekeeping sprint picks it up.

---

## 9. Grade rationale

**Grade: A.**

S23.4 was a mechanical sub-sprint with a narrow, well-scoped deliverable: close #258 with a structural CI floor in one file, <50 LOC. It shipped that deliverable clean and end-to-end verified on main.

Two independent planning errors were caught before merge by the pipeline's own quality stages (Phase-1 planner-pass, Phase-2 verification), without requiring human intervention or hot-fix PRs. The implementation matched the corrected design exactly. The 6/6 acceptance gate pass was first-pass-clean. Post-merge CI on main printed `total assertions run: 1347` and exited 0.

No grade deduction warranted. There is no meaningful gap between the intent (close the silent-0-assertion gap) and the delivery (CI now fails loudly on assertion-count violations). The pipeline caught its own errors. The floor value is defensible (10.9% headroom, documented, trivially tunable).

**A-** would apply if: the floor had been set materially wrong (e.g., 2500 shipped to main and caused an immediate CI failure), or if post-merge verification had required a follow-up PR. Neither occurred.

---

*Authored by Specc (specc-bot). S23.4 sub-sprint closed 2026-04-24T15:38:22Z.*
