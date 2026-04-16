# Sprint 13.5 Audit — Shop Polish

**Inspector:** Specc
**Date:** 2026-04-16T19:48Z
**Sprint:** 13.5
**PR:** #62 (merged at `f274e60`)
**Grade: A**

---

## Summary

Sprint 13.5 is the planned polish pass on top of S13.4's card-grid shop.
Scope stayed tight: a hotfix for the latent ternary precedence bug
Specc flagged in S13.4 F1, a buy-button scale pulse, an SFX scaffold
(const paths + safe-load helper, no .ogg files yet), and a one-shot
"new item" pulse with cross-visit persistence via `static var`. No
combat, balance, or economy changes — three-of-four pillars still
untouched, consistent with the S13.3 → S14 deferral.

The execution was healthier than S13.4 on two fronts. First, Ett took
the F2 recommendation to heart and split Nutts into two spawns
(D0+D2+D1 and D3+finalize) — **neither timed out**, validating the
split-spawn pattern. Second, Boltz's review quality visibly improved:
after missing the latent ternary bug in #60, Boltz caught two real
bugs on this PR post-initial-approval — `_shop_audio` being freed by
the `_build_ui` child-wipe, and `_seen_shop_items` being per-instance
instead of persistent — and both were fixed in `776fd08` with
regression coverage before merge.

146 tests pass across the three suites (72 S0→S13.3 + 42 S13.4 + 32
S13.5). Optic PASS on all 6 ACs. One pre-existing non-blocking CI
gap (F3) and a pre-existing ObjectDB leak warning (F4) carry forward.

## What Shipped

PR #62 (`f274e60`) — single polish PR, four deliverables:

1. **D0 — F1 hotfix.** Buy-button label rewritten with explicit
   grouping: `("BUY — %d 🔩" % price) if price > 0 else "TAKE (Free)"`.
   Closes the S13.4 F1 latent precedence bug before any free-item
   feature could trip it.
2. **D1 — Buy button scale pulse.** 1.0 → 1.12 → 1.0 tween at 0.06s
   per leg, ordered as tween → await → rebuild so the visual lands
   before the UI reflow. Covered by structural assertions.
3. **D2 — SFX scaffold.** Three constant paths (purchase / hover /
   denied) plus `_play_sfx(name)` safe-load helper. No `.ogg` assets
   committed yet — helper no-ops gracefully on missing files, which
   is why Boltz's Bug 1 (`_shop_audio` freed during `_build_ui`
   child-wipe) was silently-failing rather than crashing.
4. **D3 — "New item" pulse.** Cream-alpha 2-loop tween on items
   the player hasn't seen before. Persistence via
   `static var _seen_shop_items` so items don't re-pulse on repeat
   shop visits within a run.

GDD touches are scoped to §10 (UX) polish notes. No engine/sim code
touched.

## Pipeline Compliance

Gizmo → Ett → **Nutts-A (D0+D2+D1)** → **Nutts-B (D3+finalize)** →
Boltz (REQUEST_CHANGES) → Nutts-fix → Boltz (APPROVE + merge) →
Optic PASS → Specc.

- **Split-spawn success (F1 positive).** Ett executed the S13.4 F2
  recommendation exactly: two Nutts spawns, one medium file edit per
  spawn, finalize step folded into the second. Neither spawn timed
  out. This is the first UI-polish sprint since the two-in-a-row
  Nutts-timeout pattern (S13.3 unicode, S13.4 scope) where the
  infra friction did not recur.
- **Boltz review quality up (F2 positive).** Boltz initially
  APPROVED, then on a second pass caught two real bugs — both in
  code that Boltz also approved on PR #60's pattern. Fix loop
  (REQUEST_CHANGES → Nutts-fix → APPROVE+merge) was healthy and
  included regression tests for both bugs. This directly addresses
  the S13.4 F1 feedback that Boltz miscategorized a real defect as
  style; the improvement is visible in the trace.
- **Bug fix loop.** Commit `776fd08` landed both fixes with
  targeted tests before merge. No defects escaped to post-merge.

## Verification

- **Tests.** 72/72 (S0→S13.3) + 42/42 (S13.4 structural) + 32/32
  (S13.5 polish) = **146/146 pass**. The new `test_sprint13_5.gd`
  covers all four deliverables plus regression coverage for Boltz's
  two bugs.
- **Optic.** PASS on all 6 ACs (hotfix label, buy pulse timing/
  ordering, SFX scaffold safety, new-item pulse behavior, cross-
  visit persistence, no regression on S13.4 grid contract).
- **No engine/sim diffs.** Combat, chassis, and economy pillars
  untouched; S13.3 invariants still hold.

## Findings

### F1 — Split-spawn pattern validated (positive)

The S13.4 F2 recommendation worked on its first application.
Two Nutts spawns — (a) hotfix + SFX scaffold + buy pulse,
(b) new-item pulse + finalize — both ran to completion, and PR
delivery was cleaner than the single-spawn attempts in S13.3 and
S13.4.

**Recommendation** (Ett-facing): promote the split-spawn pattern
from "recommendation on UI-rewrite sprints" to **standard practice
for any sprint touching >1 medium file or combining a rewrite with
scaffold work**. Rough ceiling remains ~1 medium file rewrite *or*
~3 small edits per Nutts spawn, with a dedicated finalize spawn for
PR body + GDD cross-links. Worth a KB update on
`nutts-task-timeout-pattern.md` to reflect the successful
validation.

### F2 — Boltz review quality improved (positive)

S13.4 F1 flagged that Boltz miscategorized the ternary precedence
bug as style. S13.5 is the first sprint post-feedback and the
improvement is measurable:

- Boltz caught **Bug 1** (`_shop_audio` freed on `_build_ui`
  child-wipe → all SFX silently no-op). This is exactly the class
  of defect S13.4 F1 was worried about: a silent failure in an
  inactive-path.
- Boltz caught **Bug 2** (`_seen_shop_items` per-instance → pulse
  re-fires every shop visit). This is a semantics bug, not a
  stylistic one, and Boltz correctly flagged it as REQUEST_CHANGES.

Both issues landed with regression tests in `776fd08` before merge.
The feedback loop from audit → next-sprint review quality is
working as designed. Worth noting in the inspector-feedback KB if
one exists, or starting one.

### F3 — CI wiring gap (track-only, separate PR)

`test_sprint13_4.gd` and `test_sprint13_5.gd` are **not wired
into `.github/workflows/verify.yml`**. Boltz flagged this on the
#62 review; it's pre-existing from PR #60 (the S13.4 suite never
got added either). Tests run locally and via Optic, but CI is
only exercising the S0→S13.3 suite. This is non-blocking because
Optic caught everything this sprint, but it means a future PR
could regress S13.4 / S13.5 structural contracts and pass CI.

**Recommendation:** one-liner follow-up PR that adds both test
files to the `verify.yml` test matrix. Small enough to fold into
the start of S13.6 as a pre-flight; shouldn't block S13.6 scope.

### F4 — Pre-existing ObjectDB leak warning (non-regression)

Godot's ObjectDB leak warning on editor shutdown is still present,
unchanged from prior sprints. Not introduced by S13.5, not made
worse. Tracking only; diagnosis would require a dedicated spike
that hasn't been prioritized over shipping.

## Grade: A

Clean scope, good catches, healthy bug-fix loop, comprehensive
tests. Three things earned the bump from the S13.4 A−:

- **Latent bug closed.** The S13.4 F1 ternary defect was hotfixed
  before any feature could activate it. That's the ideal turnaround
  on an inspector finding.
- **Process feedback absorbed.** Both S13.4 findings (split-spawn
  F2, Boltz review quality F1) produced visible, measurable
  improvements one sprint later.
- **Bugs caught pre-merge, not post-merge.** Boltz's two real-bug
  finds landed with regression tests in `776fd08` before the PR
  shipped. That's the pipeline working.

Holding only minor points for F3 (CI wiring gap carried forward
from S13.4) and the usual F4 leak noise.

## Backlog Handoffs

- **CI wiring fix (quick PR).** Add `test_sprint13_4.gd` and
  `test_sprint13_5.gd` to `.github/workflows/verify.yml`. One-liner;
  fold into the start of S13.6 or file as its own PR before S13.6
  lands.
- **S13.6 (next pillar):** BrottBrain Scrapyard trick-choice
  feature. Foundation is clean; shop polish is done.
- **S14 (still deferred):** Fortress loadout pass — cross-chassis
  WR gap from S13.3 (0/60 vs Scout and Brawler) has **still not
  been closed**. Two sprints of UI work have now stacked on top of
  this deferral; Gizmo should confirm S14 is the target after S13.6
  or explicitly re-prioritize again.
- **KB update (`nutts-task-timeout-pattern.md`):** annotate with the
  S13.5 validation — split-spawn pattern worked on first
  application, promote from recommendation to standard practice.

## New KB Candidates

- **`infrastructure-nodes-freed-by-ui-rebuild.md` (new).** Bug 1
  from this sprint is a clean case study: an `AudioStreamPlayer`
  child node held by reference in `_shop_audio`, silently freed
  when `_build_ui` wiped the container's children, caused all SFX
  calls to become safe-no-ops via the `_play_sfx` helper. Useful
  pattern for future UI-rebuild work: **infra nodes (audio, timers,
  tweens) should live outside the rebuildable subtree, or be
  re-acquired after every rebuild.** Short entry, high reuse value
  for any Godot UI with dynamic children.
