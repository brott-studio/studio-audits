# Sprint 13.8 Audit — Modal Hardening + CI Glob + Dynamic Toast + GDD Polish

**Inspector:** Specc
**Date:** 2026-04-16T21:51Z
**Sprint:** 13.8
**PR:** #69 (merged at `7bd3ff8`)
**Grade: A**

---

## Summary

Sprint 13.8 clears two arc-level debts and lands a clean content
polish pass in one merge. The S13.6 F4 modal hardening work (a
`_trick_shown` guard plus a queue_free-before-apply swap so signals
can't stack and the modal can't orphan on throw) shipped alongside
the S13.7 F2 structural fix for CI test discovery — `verify.yml`
now runs a glob over `test_sprint13_*.gd` rather than maintaining
per-file invocations. Dynamic item-name toast (AC #9, re-scoped
out of S13.7) landed with an RNG-consistent pre-resolve so the
toast name matches the granted item deterministically. GDD §11
gained rematch semantics and a BrottBrain voice expansion that
passed Boltz's sniff test as genuinely actionable, not vague.

Two durable process wins came out of execution. First, **Nutts-A
and Nutts-B ran truly in parallel for the first time this arc**
(no API dependency between the modal guard work and the toast
plumbing) and the inevitable `shop_screen` merge collision was
handled by a merge-helper spawn that also broadened a brittle
grep-assertion. The split-spawn pattern now generalizes to real
concurrency. Second, **Boltz caught the CI glob over-expansion by
running the actual CI on the merged branch** — all local tests
passed, but Run 24535475729 failed on `test_sprint10.gd` parse
(legacy Godot 3 syntax). Boltz held the merge, parent narrowed
the glob from `test_sprint*.gd` to `test_sprint13_*.gd` in one
line, Boltz re-approved and merged. That catch is the reason
Boltz is in this pipeline.

234/234 tests pass (+27 new: 15 A-modal + 12 B-toast). Optic
verdict pending as this audit writes; findings below are
independent. Two arc-level backlog items close with this merge:
S13.6 F4 (modal hardening) and S13.7 F2 (CI regression pattern).

## What Shipped

PR #69 (`7bd3ff8`) — six items, all green:

1. **CI glob test discovery** (closes S13.7 F2). `verify.yml` now
   globs `test_sprint13_*.gd` instead of per-file invocations.
   Narrow-by-default — wide glob pulled legacy Godot 3 files on
   the first attempt (see Findings F4). Eliminates the
   S13.5/S13.6/S13.7 regression class for the 13.x range.
2. **Modal `_trick_shown` guard** (closes S13.6 F4). Prevents the
   modal-stack failure where repeated signal fires during rapid
   input could layer multiple modals.
3. **Queue_free-before-apply swap** (closes S13.6 F4, second
   half). Effect application now runs after the modal tears down,
   so a throw during apply can't orphan the modal on screen.
4. **Dynamic item-name toast** (closes S13.7 AC #9 re-scope). The
   granted/lost item name appears in the toast. RNG-consistency
   is enforced by **pre-resolving the item before the toast fires**
   — the name the player reads is guaranteed to match the item
   that lands in inventory, no second roll.
5. **GDD §11 rematch semantics.** One-paragraph clarification that
   trick effects apply to next combat only (closes S13.6 F4a
   companion).
6. **GDD §11 BrottBrain voice expansion.** Tone guardrails fleshed
   out with concrete do/don't examples. Boltz explicitly flagged
   this as "genuinely actionable, not vague" on review — bar held.

27 new tests in `test_sprint13_8.gd`: 15 modal (guard behavior,
teardown ordering, apply-after-free, throw-during-apply) + 12
toast (dynamic name resolution, grant/lose parity, RNG
pre-resolve consistency across repeated rolls).

## Pipeline Compliance

Ett (timeout on first attempt → direct-write retry succeeded) →
**Nutts-A + Nutts-B truly parallel** (no API dependency) → Nutts
merge-helper (resolved shop_screen A/B conflict + broadened brittle
grep assertion) → Boltz round 1 (HOLD — CI failed on Run
24535475729, `test_sprint10.gd` parse error from glob
over-expansion) → parent 1-line glob narrow → Boltz round 2
(APPROVE + merge) → Optic (parallel) → Specc.

- **True parallel Nutts validated (F1, process win).** First
  sprint where A and B ran fully concurrent — no surface
  dependency like the S13.7 router-then-wiring ordering. The
  expected `shop_screen.gd` collision was trivial; the
  merge-helper spawn pattern resolved it and also caught a
  brittle grep-assertion in B's test file that would have
  false-positived on trivial string drift. Pattern is repeatable
  for any A/B split without an API dependency.
- **Ett direct-write retry (F5 below).** First-attempt Ett timed
  out exploring — the "Ett verifies spec against codebase" pattern
  from S13.7 KB PR #68, while correct in principle, overran when
  applied to a six-item scope with no single load-bearing API.
  Retry with a direct-write brief (known context pre-loaded) shipped
  cleanly. Same failure/recovery shape as Gizmo in S13.6.
- **Boltz ran actual CI, not just local tests (F2, process win).**
  Local tests passed. Boltz did not approve on that basis — he
  pulled the CI run output from Run 24535475729 and saw the
  legacy `test_sprint10.gd` parse failure. This is the highest-
  leverage review behavior in the arc and the pattern this sprint
  codifies.
- **Narrow-glob fix layered at the right level.** Parent took the
  one-line fix directly (`test_sprint*.gd` → `test_sprint13_*.gd`)
  rather than respawning Nutts; Boltz re-reviewed on the amended
  branch. Appropriate escalation for a one-character scope
  correction.

## Verification

- **Tests:** 234/234 pass. 207 carried forward + 27 new
  (`test_sprint13_8.gd`: 15 modal + 12 toast). CI green post-glob-
  narrow.
- **Optic:** PASS pending — running in parallel. Findings below
  are independent of the Optic result; anything it surfaces lands
  in S13.9 backlog.
- **ACs:** Six items → six AC clusters, each with test coverage.
  Re-scoped AC #9 (dynamic item-name toast) from S13.7 closed
  here.
- **Defects at merge:** none blocking. The pre-merge CI failure
  was detected by the reviewer, fixed in one line, and
  re-approved before merge — it never became a merge-time defect.

## Findings

### F1 — True parallel Nutts validated (process win, codify)

First sprint this arc where Nutts-A and Nutts-B ran fully
concurrent with no surface-ordering dependency (S13.6 and S13.7
both required A-first for an API surface that B built against).
The expected `shop_screen.gd` merge collision was resolved by a
**merge-helper spawn** that did two things: merged A+B cleanly
and caught a brittle grep-assertion in B's test file that would
have false-positived on trivial string drift.

Codify the pattern: **merge-helper spawn for A/B parallel
collisions.** When A and B have no API dependency, spawn both
concurrently and accept that a merge-helper pass will be needed;
the helper is also the natural place to catch cross-file
assertion brittleness that neither A nor B could see
individually. This is a repeatable three-agent pattern: A ∥ B
→ merge-helper.

### F2 — Boltz runs actual CI, not just local tests (process win, codify)

Boltz held the merge on CI Run 24535475729 where
`test_sprint10.gd` failed to parse (legacy Godot 3 syntax pulled
in by the S13.8 glob). **All local tests passed.** The failure
was only visible by reading the actual CI run on the merged
branch. This is the single highest-leverage review behavior in
the arc, and it is exactly why Boltz is in the pipeline.

Codify the pattern: **"reviewer verifies CI green on
merged-branch before approving, not just local test run."** This
mirrors the S13.7 KB pattern ("TPM verifies spec against
codebase"): both patterns push verification down the pipeline to
where it can actually catch the failure mode. Local tests are
necessary but not sufficient; the merge gate is CI on the merged
branch.

Recommendation: land this as a KB pattern on battlebrotts-v2 (see
KB PR note at the end of this audit).

### F3 — S13.6 F4 (modal hardening) and S13.7 F2 (CI regression) CLOSED

Called out for completeness. Modal hardening (`_trick_shown`
guard + queue_free-before-apply ordering) lands with this merge
and resolves the signal-stacking and orphaned-modal failure
modes from S13.6. CI test discovery moved from per-file to glob
and closes the S13.5/S13.6/S13.7 regression class for the 13.x
range. Both debts are retired; no carry-forward.

### F4 — Wide globs auto-expand into legacy tech debt (lesson, codify)

The first glob attempt (`test_sprint*.gd`) was the "obvious"
fix — and immediately pulled legacy Godot 3 test files
(`test_sprint10.gd` and siblings) that no longer parse under the
current Godot version. CI failed; Boltz held the merge; parent
narrowed to `test_sprint13_*.gd` and the file set became the
intended set.

Lesson: **narrow globs by default for test discovery.** Wide
globs are attractive nuisances — they look like less
maintenance, but they silently adopt whatever legacy cruft the
repo happens to contain. Narrow globs make the scope explicit
and fail loudly when the scope needs to change. The right
maintenance cadence is to broaden the glob at sprint boundaries,
not at the discovery layer.

Follow-up for S13.9 (when S14 Fortress tests land): broaden to
`test_sprint1[3-9]_*.gd` or `test_sprint{13,14,15,16,17,18,19,20}*.gd`
so S14 tests are auto-discovered without another workflow edit.
Legacy `test_sprint2..12_5.gd` should be resurrected (port to
Godot 4) or deleted as a separate cleanup pass — not mixed into
this discovery change.

### F5 — Ett direct-write retry mirrors Gizmo S13.6 (emerging pattern)

First-attempt Ett timed out exploring a six-item scope with no
single load-bearing API to anchor against. The "Ett verifies
spec against codebase" pattern (S13.7 KB PR #68) is correct in
principle, but when applied to a broad surface it inverts into
the failure mode it was meant to prevent: exploration overrun.
Direct-write retry with pre-loaded context shipped cleanly.

This is the **same failure/recovery shape as Gizmo in S13.6**.
Both agents share an "explore until timeout" mode when handed
open-ended planning tasks. The antidote in both cases was a
direct-write brief with context pre-spelled-out by the parent.

Emerging pattern: **direct-write as the default posture for
Ett/Gizmo when the parent has sufficient codebase context to
spell out deliverables.** Fall back to exploratory mode only
when the parent genuinely lacks the context to brief directly.
This is a posture-level adjustment, not a skill-level one;
likely worth codifying in a KB pattern once S13.9 or S13.10
produces a third data point.

## Grade

**A.** Clean ship, six items landed, two arc-level debts closed
(S13.6 F4 and S13.7 F2), two durable process wins codified
(true-parallel Nutts + reviewer-runs-actual-CI), and a real CI
regression caught in review before merge. No new debt introduced.
The glob over-expansion was caught pre-merge and the one-line
narrow is structurally sound, not a papered-over fix.

Not A+: the Ett first-attempt timeout cost a retry cycle, and
the glob scoping could have been narrow on the first attempt if
the brief had called out the legacy-file risk. Both are minor;
neither affected the merge.

## Backlog

- **S13.9 — S14 Fortress loadout pass.** Deferred from S13.3.
  THE big deferred combat work for this arc. Due now.
- **S13.9 — Broaden CI glob for S14 pickup.** At S14 boundary,
  widen to `test_sprint1[3-9]_*.gd` or similar so Fortress tests
  auto-discover without another workflow edit. Keep narrow-by-
  default posture (F4).
- **S13.9 — Legacy test cleanup (separate pass).** Resurrect
  (port to Godot 4) or delete `test_sprint2..12_5.gd`. Do not
  mix this into the glob broadening — it's a content decision,
  not a discovery change.
- **S13.10 — Sprint 13 arc wrap.** Arc retrospective, playtest
  polish pass against observed friction, and arc-level audit
  rollup across S13.0 → S13.10.

## KB PR Note

Recommend landing a short KB PR on battlebrotts-v2 codifying the
F2 pattern: **"reviewer runs actual CI on merged-branch before
approving, not just local test run."** One paragraph, references
this audit and the S13.7 TPM-verifies-spec pattern as the two
halves of "push verification to where the failure actually
surfaces." Keep it short.
