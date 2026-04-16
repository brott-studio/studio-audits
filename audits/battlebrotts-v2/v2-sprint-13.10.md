# Sprint 13.10 Audit — Quiet Arc Wrap

**Inspector:** Specc
**Date:** 2026-04-16T23:31Z
**Sprint:** 13.10
**PR:** #73 (merged at `4d63461`)
**Grade: A**

---

## Summary

Sprint 13.10 closes the Sprint 13.x arc. It is a deliberate
wrap sprint, not a build sprint — scope was polish, debt
closure, playtest capture, and creative framing for S14. Every
Boltz nit carried forward from S13.9 landed (picker empty-pool
guard, weight-cap validation test). The defensive fallback
chain in `build_opponent_brott` hardens a prod-unreachable path
against the sparse-pool case the picker guard covers. The
legacy `test_sprint2.gd` — flagged in S13.9 as dormant and
re-confirmed by Boltz — is deleted with a `docs/MIGRATION.md`
note. A new `test_sprint13_10.gd` asserts `TEMPLATES.size() <=
40`, giving the template pool 33%+ headroom over the aspirational
count of 30 (actual is 6).

Two sprint-shaping things happened outside the code. First,
**Eric ran a full Scrapyard playthrough (30–60m) and sent notes
back**, and those notes were captured as a repo artifact under
`docs/playtest/sprint13.10-arc-wrap.md` — first time this arc
has structured human playtest observations as a durable input
to the next arc's planning. Second, **a UX vision doc landed in
`docs/kb/ux-vision.md`** naming Eve from WALL-E as the polish
target, siblinged to the existing audio-vision doc (also
WALL-E). The two vision docs now form a coherent creative
frame for S14+ without committing to any spec.

The pipeline ran lighter than a build sprint: Gizmo direct-
wrote the spec (catching a count mismatch in the brief —
aspirational 30, actual 6), **no Ett** (Nutts pre-staged
directly — wrap-sprint lighter ceremony), Nutts single-slice
at 68 LoC, a playtest pause while Eric played, inline doc
authoring on the branch, then Boltz review and merge with CI
on the merged branch per KB #70. 195/195 tests green across
the combat suite at merge. One latent risk surfaced by Boltz
(`game_main.gd:199` unguarded position assignment) is tracked
for S14.

S14 is **deliberately paused** pending a creative conversation
between Eric and the orchestrator. No planning allowed until
that conversation happens. The arc closes clean; see
`v2-arc-13.x-rollup.md` (commit `f41fb3c`) for cross-sprint
synthesis.

## What Shipped

PR #73 (`4d63461`):

1. **Picker empty-pool guard** (Boltz S13.9 nit) in
   `godot/data/opponent_loadouts.gd` —
   `pick_opponent_loadout` returns `{}` when the pool empties
   after filters. Closes the defensive gap Boltz flagged at
   S13.9 merge.
2. **Builder fallback chain** in
   `godot/game/opponent_data.gd::build_opponent_brott` —
   empty → retry sans variety → retry tier-1 no filters → null.
   Defensive-only, prod-unreachable given the picker guard, but
   fails safe if the guard is ever bypassed.
3. **Weight-cap validation test** (Boltz S13.9 nit) in new
   `godot/tests/test_sprint13_10.gd` — asserts
   `TEMPLATES.size() <= 40`. Current count is 6, aspirational
   is 30, cap set to 40 for 33%+ headroom. Future template
   growth will tripwire this test before the weight distribution
   silently drifts.
4. **Legacy `test_sprint2.gd` deleted** with a
   `docs/MIGRATION.md` note. Boltz called this "dormant legacy"
   at S13.9; S13.10 retires it. Optional-cleanup item from
   S13.9 backlog, now closed.
5. **Playtest artifact** at `docs/playtest/sprint13.10-arc-
   wrap.md` — Eric's end-of-arc observations captured as repo
   input to S14 planning. First of its kind on this project.
6. **UX vision doc** at `docs/kb/ux-vision.md` — Eve from
   WALL-E as polish target. Pillars, anti-patterns, S14 polish
   checklist. Shaping doc, not a spec.
7. **Gizmo's S13.10 spec** at `docs/design/sprint13.10-arc-
   wrap-polish.md` — swept into the PR via `git add -A`; Boltz
   reviewed and approved keeping it as historical record.

5 new tests in `test_sprint13_10.gd`. No regressions in any
prior suite.

## Pipeline Compliance

Gizmo (direct-write spec, ~2m17s, **caught brief's 30-template
count mismatch — actual 6, cap set to 40 with headroom**) →
**no Ett** (Nutts pre-staged directly; wrap-sprint lighter
ceremony) → Nutts (single-slice, 2m16s, 68 LoC total in
budget) → **playtest pause** (Eric runs full Scrapyard, 30–60m)
→ parent orchestrator inline-authors `docs/playtest/...` and
`docs/kb/ux-vision.md` on the branch → Boltz (APPROVE + merge,
4m55s, **CI on merged branch per KB #70**, 195/195 green, one
latent risk tracked for S14) → Specc.

- **Gizmo count-mismatch catch.** Brief cited 30 templates;
  Gizmo verified against the codebase and reported actual is
  6. Cap set to 40 for 33%+ headroom over the aspirational
  number. Same shape as the S13.9 "Fortress" catch and the
  S13.6 chassis archetype catch — design-time codebase
  verification preventing a silent spec-vs-reality drift.
  **Third consecutive arc-level data point** for the F1
  codification now queued on the KB.
- **No Ett — wrap-sprint discipline.** Nutts pre-staged
  directly from Gizmo's spec. Wrap sprints are not build
  sprints; the planning-stage ceremony was appropriately
  shed. This is a posture call, not a skip-the-step shortcut
  — the decision was made deliberately and the scope
  supported it (68 LoC, all pre-approved deterministic work).
- **Pre-staging during human-wait (F1).** Orchestrator
  pre-staged the two Boltz nits and the legacy `test_sprint2`
  deletion while waiting on Eric's playtest. These were all
  zero-decision-surface items — pre-approved, no scope
  questions, no design calls. Kept the pipeline productive
  without risking scope creep during a human-dependency
  window.
- **Playtest capture is new (F3).** Eric's observations
  landed as a repo artifact, not chat ephemera. This is the
  first arc to do this, and it establishes the input channel
  for the next arc's planning. See F3.
- **Boltz ran CI on merged branch (KB #70).** Third
  consecutive sprint with this posture since S13.8 F2
  codification. 195/195 green, one latent risk noted — not
  introduced by this slice — tracked for S14.
- **Direct-write continues to dominate.** Gizmo direct-wrote.
  Specc direct-writes. The posture shift flagged in S13.8 F5
  is fully normalized.

## Verification

- **Tests:** 195/195 pass on the merged branch.
  - `test_sprint13_10` (new): 5/5
  - `test_sprint13_9`: 17/17
  - `test_sprint13_8_modal_hardening`: 15/15
  - `test_sprint13_8_toast`: 12/12
  - `test_sprint13_7`: 74/74
  - `test_runner`: 72/72
- **CI:** Boltz ran CI on the merged branch per KB #70. Green.
- **ACs:** Picker empty-pool guard, builder fallback chain,
  weight-cap test, legacy cleanup, vision + playtest docs —
  all landed.
- **Defects at merge:** none blocking. One latent risk
  (`game_main.gd:199`) surfaced by Boltz — pre-existing, not
  introduced here, tracked for S14.

## Findings

### F1 — Pre-staging during human-wait windows (process win, codify)

Sprint 13.10 had a hard human-dependency in the middle: Eric's
playtest. That's a 30–60m window where the pipeline could have
idled. The orchestrator instead pre-staged three items — the
two Boltz S13.9 nits (picker guard, weight-cap test) and the
legacy `test_sprint2` deletion — all of which were
**pre-approved, zero-decision-surface** work. No scope calls,
no design questions, no ambiguity that could have grown during
execution. The playtest came back, the docs landed inline on
the branch, and Boltz merged a complete wrap sprint in one
pass.

The pattern worth codifying: **during human-dependency pauses,
pre-stage only work that meets two criteria — (a) explicitly
pre-approved (here: Boltz's S13.9 nits and the S13.9 optional
cleanup item) and (b) zero decision surface (nothing the human
might want to weigh in on).** Pre-staging exploratory or
scope-adjacent work during a human-wait is a scope-creep
hazard, because the human could come back with a direction
that invalidates the in-flight work. The S13.10 pre-stage
hewed to the safe lane and shipped clean.

### F2 — Arc debt closure (clean finish)

Every S13.9 carry-forward closed:
- Picker empty-pool guard ✓
- Weight-cap validation test ✓
- Legacy `test_sprint2` cleanup (optional in S13.9, executed in
  S13.10) ✓

Plus counter-play — explicitly deferred to S14 by Eric rather
than carried as debt. Debt deferral with owner consent is not
debt; it's scoping. Arc closes with zero outstanding Boltz
nits and zero unresolved process flags.

### F3 — Playtest-as-repo-artifact (new channel, codify)

First time this arc has captured structured human playtest
observations as a durable repo artifact
(`docs/playtest/sprint13.10-arc-wrap.md`). Chat-based playtest
notes evaporate; a repo file persists and can be referenced by
the next arc's planning pass directly. This establishes the
**playtest → repo → next-arc-input** channel that future arcs
can use without re-inventing it.

The doc itself is observational, not prescriptive — reads
like a field report, not a spec. That's the right shape: it
becomes a planning input, not a planning decision. See the
Backlog section below for the specific observations Eric
surfaced.

**Codify:** "end-of-arc playtest lands as a repo artifact
under `docs/playtest/` and feeds the next arc's planning." One
paragraph in the KB is enough.

### F4 — UX vision codified (creative framing, shaping doc)

`docs/kb/ux-vision.md` names **Eve from WALL-E** as the UX
polish target. Pillars, anti-patterns, an S14 polish
checklist. It pairs with the pre-existing audio-vision doc
(also WALL-E) to form a coherent creative frame: the game
wants to **feel** WALL-E-tier in both visual/UX polish and
audio polish. Neither doc is a spec. They are shaping
documents — inputs to future spec writing, not specs
themselves.

The distinction matters: shaping docs give design agents
(Gizmo) and the orchestrator a shared vocabulary and
aesthetic target to point at during S14+ spec writing. They
do not commit scope. That's the right level of commitment at
the end of an arc where S14 is deliberately paused pending a
creative conversation.

### F5 — Latent risk surfaced by Boltz, not introduced (tracked for S14)

Boltz flagged `game_main.gd:199` — an unguarded
`enemy_brott.position = ...` assignment that will null-crash
at the call site if `build_opponent_brott` ever returns null
(i.e., if the picker's defensive fallback chain all the way
through tier-1 no-filters returns empty, which the weight-cap
test and template invariants make effectively unreachable in
prod). Pre-existing — not introduced by S13.10 — and the
defensive chain in the builder now makes a return-null case
require multiple simultaneous invariant violations.

Tracking for S14 rather than patching in S13.10 is the right
call. S13.10 is a wrap sprint with an explicit DO-NOT-EXCEED
list. Reaching into a pre-existing callsite in a wrap sprint
is exactly the kind of scope-creep the wrap posture is
designed to refuse. Tracked; not ignored.

### F6 — Wrap-sprint discipline (process win)

The DO-NOT-EXCEED list held. Counter-play was not smuggled in
— it was explicitly deferred to S14 per Eric. The pre-staged
work was the pre-approved work, not the adjacent work.
Playtest capture and vision docs were additive-only (no spec
commitments). One latent risk was surfaced, documented, and
deferred rather than patched.

This is the exemplary shape of a wrap sprint: close debt,
capture signal, frame the next arc, don't build. Worth
naming explicitly because "quiet sprints" are easy to
under-value and easy to let creep. This one did neither. It
is the quietest sprint of the arc and arguably the cleanest.

## Grade Justification

**A.** The quietest sprint of the arc, but nothing is broken,
nothing was smuggled in, every debt closed, and the
playtest/vision capture lands the arc with clean context for
S14. Pipeline ran lighter than a build sprint by design (no
Ett, single-slice Nutts), and the lighter ceremony was the
right call for the scope. Boltz ran CI on the merged branch
per KB #70 and caught a latent risk that's now tracked for
S14. Process wins codifiable: F1 (pre-staging during human-
wait), F3 (playtest as repo artifact).

Not A+: this is a fill-and-frame sprint, not a deliverable-
heavy one. The graded output is discipline and closure, not
code volume, and A+ is reserved for sprints that combine
discipline with significant shipped scope. S13.10 is the
right shape for what it was asked to do; A is the honest
grade.

## Backlog

Observations from Eric's playtest doc, captured here as
planning inputs for S14 (not commitments):

- **Critical blockers:** league progression UI missing; bots
  stuck on walls.
- **UX pain:** shop scroll + click-jump; hover-only tooltips;
  loadout overlaps; popup frequency; BrottBrain drag; energy
  bar unexplained.
- **Feel:** Scout smoothing (speed is fine — jerkiness is the
  problem; turn rate + accel/decel are the levers); long
  fights when losing.
- **Cards:** missing aggressive/committal plays (Charge,
  Chase); unwanted abstract-timing cards.
- **Events:** random events feel bad-chaotic — candidates
  are reduce frequency, skip option, or redesign.
- **Latent:** `game_main.gd:199` unguarded position assignment
  (F5).
- **Creative direction:** UX polish pass toward Eve-tier
  (per `docs/kb/ux-vision.md`); audio pass toward WALL-E-tier
  (per the existing audio-vision doc).

**S14 is paused** pending creative conversation between Eric
and the orchestrator. No planning allowed until that
conversation happens. This backlog is input to that
conversation, not a pre-committed plan.

## Arc Closure

Sprint 13.10 closes the Sprint 13.x arc. Every flagged nit
retired, every arc-level debt closed, counter-play explicitly
deferred with owner consent. See
[`v2-arc-13.x-rollup.md`](./v2-arc-13.x-rollup.md) (commit
`f41fb3c`) for cross-sprint synthesis and arc-level findings.

## KB PR Note

The F1 pre-staging pattern is narrow enough to piggyback on
the arc rollup's KB PR rather than requiring its own —
recommend a one-paragraph addition under "wrap-sprint
patterns" with the two criteria (pre-approved + zero decision
surface) spelled out.

The F3 playtest-as-repo-artifact pattern is worth a standalone
KB note: one paragraph naming the channel
(`docs/playtest/<sprint>.md` at end-of-arc) and its role as
input to the next arc's planning. Cheap to codify, high
leverage across future arcs.

Both can land in the same KB PR as the arc rollup's
recommendations — no need to fragment.
