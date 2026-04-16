# Sprint 13.7 Audit — Item Token Router + Trick Content Expansion

**Inspector:** Specc
**Date:** 2026-04-16T21:21Z
**Sprint:** 13.7
**PR:** #67 (merged at `43d3c12`)
**Grade: A**

---

## Summary

Sprint 13.7 closes the S13.6 F1 `ITEM_GRANT`/`ITEM_LOSE` stub debt
and expands the BrottBrain trick catalog without introducing new
debt. An `item_tokens.gd` router (Nutts-A, 91 LoC) landed as the
dispatch surface; `game_state.gd` wired `_grant_trick_item` and
`_lose_trick_item` into real inventory mutation (Nutts-B); three new
tricks (`crate_find`, `toll_goblin`, `scrap_trader`) ship functional
with full effect coverage; GDD §11 gains an item taxonomy that the
router reads against. As a bonus closure, the CI `verify.yml` gap
that quietly rode through S13.6 was also patched in the merge cycle
(Boltz caught it on review — not CI itself).

Execution was the cleanest arc run to date. **Ett caught three
material spec errors before a single line of code was written** —
wrong field names, a missing `CERAMIC` item class, and a
non-existent `MORALE_DELTA` effect kind — and rewrote the trick set
from 5 down to 3 aligned with the actual codebase. That pre-code
catch is the highest-leverage TPM work this arc has produced and is
worth codifying. The Nutts split-spawn pattern is now 3-for-3 clean
(A surface → B parallel-ready), and Boltz held the merge on the CI
gap + a flavor nit until both were resolved, then re-approved.

314/314 tests pass (240 carried + 74 new S13.7, 47 router + 27
wiring/tricks). Optic verdict pending as this audit writes; the
run is in parallel and findings are independent of that result.
`scavenger_kid`'s primary `ITEM_GRANT` effect is now functional,
closing S13.6 F1.

## What Shipped

PR #67 (`43d3c12`) — content + infrastructure sprint, five pieces:

1. **Item token router.** `item_tokens.gd` (91 LoC, Nutts-A) is the
   central dispatch for `ITEM_GRANT`/`ITEM_LOSE` effect kinds.
   Reads GDD §11 item taxonomy, validates item class on grant,
   no-ops cleanly on lose-when-absent. Parallel-ready surface for
   Nutts-B wiring.
2. **GameState wiring.** `_grant_trick_item` and `_lose_trick_item`
   replace the S13.6 stubs in `game_state.gd` with real inventory
   mutation (Nutts-B, 57 LoC production). `scavenger_kid`'s primary
   effect now executes end-to-end.
3. **Three new tricks.** `crate_find` (item grant on shop entry),
   `toll_goblin` (item lose, bolts delta offset), `scrap_trader`
   (item swap — grant one class, lose another). All three wire
   through the router; none regress existing tricks.
4. **GDD §11 item taxonomy.** Codified item classes the router
   reads against, aligning spec with codebase (this is the section
   Ett's pre-code audit surfaced gaps in).
5. **CI verify.yml patch.** Two-line fix to invoke both
   `test_sprint13_6.gd` and `test_sprint13_7.gd`. Closes the gap
   where S13.6 tests had shipped but were never run in CI — a
   debt that would have compounded into S13.8 unnoticed.

74 new tests in `test_sprint13_7.gd`: 47 router tests (grant/lose
dispatch, class validation, empty-pool guards, idempotency) + 27
wiring/trick integration tests covering the three new tricks and
the re-enabled `scavenger_kid` primary.

## Pipeline Compliance

Gizmo (direct-write ✓) → **Ett (caught 3 spec errors pre-code,
rewrote trick set 5→3)** → Nutts-A (router, 91 LoC) → Nutts-B
(wiring + 3 tricks + tests, 57 LoC prod, parallel-ready) →
Boltz round 1 (HOLD on CI gap + flavor inversion nit) → Nutts
CI-fix (2 lines yaml + flavor swap) → Boltz round 2 (APPROVE +
merge) → Optic (in parallel with Specc) → Specc.

- **Ett pre-code spec verification (F1, process win).** Ett's audit
  against the live codebase caught three spec errors before Nutts
  was spawned: incorrect field names, `CERAMIC` missing from the
  item class enum, and a `MORALE_DELTA` effect kind that does not
  exist. The trick set was rewritten 5→3 aligned to what the code
  can actually express. Every one of those would have been a
  Nutts failure mode — either a timeout on exploration or a
  Boltz-level rework. This is the best TPM work of the arc.
- **Gizmo direct-write posture held.** Per S13.6 F3, Gizmo
  defaulted to direct-write against a clear spec. No exploration
  timeout. Pattern is durable.
- **Split-spawn is 3-for-3.** Nutts-A produced the router as a
  stable surface; Nutts-B built against that surface in parallel
  with no coordination overhead. No timeouts, no rework.
- **Boltz review carrying process hygiene (F5 below).** Boltz
  caught the CI verify.yml gap on review — CI itself did not flag
  it because the gap was self-obscuring (missing invocations
  cannot fail the files they don't invoke). Review quality is
  effectively the only gate on this failure class right now.
- **Narrative flavor catch.** Boltz also flagged a narrative
  inversion on `toll_goblin` (copy implied the player was charging
  the goblin, not being charged). One-line fix landed with the
  CI patch. Correct layer for this review — not a blocker, but
  the right bar.

## Verification

- **Tests:** 314/314 pass. 240 carried forward (207 S0→S13.6 + 33
  already-wired paths) + 74 new S13.7 (47 router + 27
  wiring/tricks). CI green post-patch.
- **Optic:** PASS pending — running in parallel. Findings below
  are independent of the Optic result; if Optic surfaces anything,
  it'll land in S13.8 backlog.
- **ACs:** 10 acceptance criteria mapped to test coverage
  (router dispatch, grant/lose semantics, class validation,
  three-trick coverage, GDD §11 taxonomy parity, CI wiring, S13.6
  F1 closure). AC #9 (dynamic item-name toast) deferred to S13.8 —
  scope trim during Ett's pass, non-blocking.
- **Defects at merge:** none blocking. Findings below are
  forward-looking.

## Findings

### F1 — Ett pre-code spec verification (process win, codify)

Ett caught three material spec errors against the live codebase
before any Nutts spawn: wrong field names, missing `CERAMIC` item
class, and a non-existent `MORALE_DELTA` effect kind. Rewrote the
trick set 5→3 with coverage that the code can actually express.
Every one of those errors would have been a Nutts failure
downstream — exploration timeout or Boltz-level rework — at much
higher cost.

Codify the pattern: **"TPM verifies spec field names against
codebase before brief-out."** Before Ett hands a spec to Nutts,
Ett greps the target enums / classes / effect kinds against the
actual source of truth (GDD + code), not just against the feature
brief. This is a thirty-second check that prevents a
fifteen-minute-to-one-hour failure cascade.

Recommendation: land this as a KB pattern on battlebrotts-v2 (see
KB PR note at the end of this audit).

### F2 — CI verify.yml regression pattern (recurring risk — fix in S13.8)

The `verify.yml` gap is now on a two-sprint regression streak:

- S13.5 PR #64 patched the range for S13.5 tests.
- S13.6 test file shipped but its invocation was never added.
- S13.7 inherited the gap; Boltz caught it on review.

Root cause: `verify.yml` uses **explicit per-file invocations**.
Every new sprint test file requires an edit to the workflow.
That's a manual step that humans and agents both forget under
time pressure. This will regress again unless the pattern
changes.

Recommendation (S13.8): **switch to glob-based test discovery**
in `verify.yml`. Concretely:

```yaml
- name: Run sprint tests
  run: |
    for f in godot/tests/test_sprint*.gd; do
      godot --headless --script "$f" || exit 1
    done
```

or equivalent. Eliminates the manual edit step and the failure
mode. This is a ten-line workflow change with durable payoff.

### F3 — S13.6 F1 `ITEM_GRANT`/`ITEM_LOSE` stub debt CLOSED

Called out for completeness. `scavenger_kid`'s primary effect is
functional end-to-end as of this merge. S13.6 F1 is closed. No
carry-forward.

### F4 — Router test 16 (empty-pool guard) covered-by-invariant

Flagging for transparency, not as a defect. Test 16 in the router
suite asserts behavior on an empty item pool. The `POOLS` constant
in `item_tokens.gd` is declared `const` and is not mutated at
runtime, so the guard is unreachable in production. The test is
still worth keeping as a defensive check against future code that
might populate pools dynamically. Acceptable defensive code, but
document that the coverage is covered-by-invariant so future
readers don't assume the guard is load-bearing.

### F5 — Flavor review at Boltz layer is the right bar (keep it)

Boltz caught a narrative inversion on `toll_goblin` where the copy
read as if the player was extracting the toll rather than paying
it. This is exactly the layer flavor review should land at — not
Ett (too early, copy not finalized), not Optic (out of scope for
AC verification), and emphatically not CI. One-liner fix at
review time, zero cost. Keep this bar: Boltz reads narrative copy
alongside code diffs and holds the merge on inversions.

## Grade

**A.** Clean ship, process wins, real gap closed (S13.6 F1), CI
debt patched in the merge cycle, no new debt introduced. Ett's
pre-code spec verification + Boltz's CI catch materially raise
the floor on pipeline hygiene. The sprint produced both the
expected artifacts (router, wiring, tricks, GDD) and two durable
process improvements worth codifying. Not A+: AC #9 (dynamic
item-name toast) was scope-trimmed and the CI workflow fix is a
patch rather than the structural glob-discovery change it should
be. Both land in S13.8.

## Backlog

- **S13.8 — CI glob-based test discovery (F2).** Replace
  per-file invocations in `verify.yml` with a glob loop over
  `godot/tests/test_sprint*.gd`. Eliminates the regression class
  that hit S13.5/S13.6/S13.7.
- **S13.8 — Modal hardening (from S13.6 F4).** `_trick_shown`
  guard on the modal + apply-exception fix so signals can't stack
  and the modal can't orphan on throw.
- **S13.8 — Rematch semantics GDD line (from S13.6 F4a).**
  One-liner in §12 clarifying the trick applies to next combat
  only.
- **S13.8 — Dynamic item-name toast (AC #9 re-scoped).**
  Toast copy shows the specific item granted/lost rather than a
  generic string. Scope-trimmed out of S13.7 during Ett's pass.
- **S13.8 — BrottBrain voice guideline expansion (from S13.6
  F5).** Flesh out GDD §11 tone guardrails now that more
  BrottBrain-gated content is live.
- **S13.9 — S14 Fortress loadout pass.** Deferred from S13.3.
  Due soon.
- **S13.10 — Sprint 13 arc wrap + playtest polish.** Arc
  retrospective and a polish pass against observed playtest
  friction.
