# Sprint 13.6 Audit — BrottBrain Scrapyard Trick Choice

**Inspector:** Specc
**Date:** 2026-04-16T20:21Z
**Sprint:** 13.6
**PR:** #65 (merged at `e1b6402`)
**Grade: A−**

---

## Summary

Sprint 13.6 delivers Pillar 3 of the "first 5 minutes" plan: a
BrottBrain-gated trick choice modal that triggers on shop entry when
the player's current brott has ≥1 unlocked trick. Three trick effects
ship functional (HP consume, pellet modifier, bolts secondary), one
effect (`ITEM_GRANT`/`ITEM_LOSE`) lands as a documented stub — making
`scavenger_kid`'s primary effect non-functional while its secondary
bolts effect still fires. The trick is not dead, just thin, and the
stub is explicitly deferred to S13.7.

Execution was clean. The split-spawn pattern held across a three-way
slice (Nutts-A: data + modal UI, Nutts-B: integration + tests, Nutts-C:
targeted fix-pass for HP/pellet wiring gaps that Nutts-B flagged). No
Nutts timeouts. Gizmo's first spec attempt did time out on an
exploration rathole — resolved on retry with a direct-write pass,
matching the S13.5 Specc retry pattern. Boltz review quality remains
solid: APPROVE on the merge pass with three non-blocking flags
(rematch semantics, `pressed.connect` stacking risk on instance
reuse, modal-orphan on apply-exception) — all real, none
merge-blocking.

207/207 tests pass (146 carried + 61 new S13.6). Optic PASS on all
10 ACs with per-AC test mapping. The ObjectDB leak warning and the
CI gap from S13.5 carry forward unchanged.

## What Shipped

PR #65 (`e1b6402`) — single-PR system sprint, four moving pieces:

1. **Data layer.** `trick_choices.gd` declares the trick catalog and
   the effect kinds (`HP_CONSUME`, `PELLET_MOD`, `BOLTS_DELTA`,
   plus stub `ITEM_GRANT`/`ITEM_LOSE`). Per-brott trick lists drive
   modal contents.
2. **Modal UI.** `trick_choice_modal.tscn` + `.gd` handle the
   three-option presentation, signal-based selection, and dismiss on
   confirm. Wires into shop entry via `shop_screen.gd` hook.
3. **Integration + sim wiring.** `game_state.gd` gains the
   `_tricks_applied` tracker and `apply_trick(id)` dispatch.
   `brott_state.gd` consumes HP for `HP_CONSUME`. `combat_sim.gd`
   reads pellet modifiers from the applied-trick bag for the next
   combat. Wiring landed across two Nutts slices (B + C).
4. **GDD §11 + §12.** §11 adds BrottBrain voice guidance (thin —
   see F5). §12 documents the trick catalog, effect kinds, rematch
   semantics (the trick applies to the next combat only), and the
   `ITEM_GRANT`/`ITEM_LOSE` stub status.

61 new tests in `test_sprint13_6.gd` cover catalog integrity, modal
signal contract, apply-trick dispatch, HP consume math, pellet mod
merge into combat, and the bolts secondary path on `scavenger_kid`
while the primary item grant is stubbed.

## Pipeline Compliance

Gizmo (timeout → retry direct-write) → Ett → **Nutts-A (data +
modal, 112 LoC)** → **Nutts-B (integration + tests, 104 LoC, gaps
flagged)** → **Nutts-C (HP + pellet wiring fix-pass, +22 LoC)** →
Boltz (APPROVE + merge) → Optic (PASS 10/10 ACs) → Specc.

- **Split-spawn + targeted fix-pass validated (F2 positive).** The
  S13.5 two-Nutts split generalized cleanly to a system sprint:
  data/UI slice → integration slice → targeted gap-fill. Nutts-B
  explicitly flagged the HP/pellet wiring gaps rather than
  over-reaching, and Nutts-C closed them in 22 LoC. This is the
  cleanest Nutts pipeline run since the timeout era. No spawn
  overran the context budget.
- **Gizmo exploration timeout pattern (F3).** Gizmo's first pass
  timed out walking the codebase for context that the spec already
  contained. Direct-write retry succeeded. This mirrors the
  pre-split Nutts timeout pattern: the fix is process, not capacity.
- **Boltz quality holding (F4).** APPROVE pass with three real,
  non-blocking flags. No post-merge regressions. The S13.4→S13.5
  improvement trajectory continues.

## Verification

- **Tests:** 207/207 pass. 146 carried forward (72 S0→S13.3 +
  42 S13.4 + 32 S13.5) + 61 new S13.6.
- **Optic:** PASS with explicit per-AC test mapping for all 10
  acceptance criteria.
- **Defects at merge:** none blocking. Three Boltz flags tracked
  below.

## Findings

### F1 — `ITEM_GRANT` / `ITEM_LOSE` stub debt (must address in S13.7)

`scavenger_kid`'s primary effect is `ITEM_GRANT` and currently
no-ops with a documented stub. The trick still has a functional
bolts secondary effect, so it's not dead on arrival, but shipping
any additional tricks that depend on item mutation before the
router exists will compound the debt. Two clean paths:

- **(a)** Implement an item router in `game_state.gd` that
  `apply_trick` can dispatch `ITEM_GRANT`/`ITEM_LOSE` into against
  the existing inventory model. Nutts's preferred option.
- **(b)** Swap `scavenger_kid`'s primary to an already-implemented
  effect kind and defer the router until a trick actually needs it.

Recommendation: **(a)** in S13.7. It unblocks trick expansion
without design churn and the inventory model is stable.

### F2 — Split-spawn + targeted fix-pass pattern validated (positive)

Three-way Nutts slice (data/UI → integration → gap-fill) with
Nutts-B explicitly flagging gaps rather than forcing completion is
now a proven pattern for system sprints. Codify it in the pipeline
KB: when a slice spans data + integration + sim wiring, default to
three spawns and budget the third for gap-fill that the second
slice surfaces.

### F3 — Gizmo exploration timeout (process, not capacity)

Gizmo's first attempt timed out on exploratory reads the spec
already covered. The retry succeeded by skipping exploration and
writing directly against the provided context. This is the same
class of failure Nutts hit pre-split. Recommendation: when the
spec scope is clear, default Gizmo to a "direct-write" posture —
exploration only if the spec explicitly leaves a question open.

### F4 — Boltz non-blocking flags (track, don't block)

Three real observations from Boltz's review, none merge-blocking:

- **(a) Rematch semantics.** The trick applies to the next combat
  only, but the GDD §12 copy doesn't spell this out. One-line GDD
  clarification in S13.7.
- **(b) `pressed.connect` stacking.** If `show_trick` is called
  twice on the same modal instance, button signal connections
  would stack. Not currently reachable — the modal is constructed
  fresh per show — but a `_trick_shown` guard on the modal would
  harden against future reuse.
- **(c) Modal orphan on apply-exception.** If `apply_trick` throws
  mid-selection, the modal could be left in the tree. Not
  currently reachable either; wrap `apply_trick` in try/guard or
  ensure `queue_free` is scheduled before dispatch.

### F5 — BrottBrain voice guidelines thin in GDD §11

§11 lands the voice section but it's minimal — a handful of
stylistic bullets. As more BrottBrain-gated content ships
(trick choices today, item dialogue and audio next), the voice
spec needs weight so writers and Nutts can match tone without
re-deriving it each time. Expand in S13.7 alongside the item
router work; the two land naturally together.

## Backlog (for S13.7+)

- **S13.7 — `ITEM_GRANT`/`ITEM_LOSE` router (F1).** Option (a): add
  the dispatch in `game_state.gd` against the existing inventory
  model. Restores `scavenger_kid`'s primary effect and unblocks
  future item-touching tricks.
- **S13.7 — BrottBrain voice doc expansion (F5).** Flesh out GDD
  §11 with tone guardrails, example phrasings, and
  do/don't patterns.
- **S13.7 — Audio / voice vision (Pillar 4).** Original
  "first 5 minutes" plan had Pillar 4 as audio/voice. Now due.
- **Modal hardening (F4b/c).** Add `_trick_shown` guard and
  tighten `apply_trick` error path so the modal cannot stack
  signals or orphan on exception. Small sprint or fold into
  S13.7 item-router work.
- **GDD §12 rematch line (F4a).** One-liner clarifying trick
  applies to next combat only.
