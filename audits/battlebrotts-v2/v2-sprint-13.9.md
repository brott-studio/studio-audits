# Sprint 13.9 Audit — Opponent Loadout Pass

**Inspector:** Specc
**Date:** 2026-04-16T22:11Z
**Sprint:** 13.9
**PR:** #71 (merged at `5affe67`)
**Grade: A**

---

## Summary

Sprint 13.9 closes the largest outstanding arc-level debt: the
opponent-variety combat work deferred from S13.3. Six named
opponent loadout templates ship across five archetypes (TANK,
GLASS_CANNON, SKIRMISHER, BRUISER, CONTROLLER), driven by a
variety-preserving picker with an explicit league-to-difficulty
tier mapping (`difficulty_for(league, index)` — scrapyard 1,1,2 /
bronze 2,2,3). Integration threads through `opponent_data.gd::
build_opponent_brott`, `game_state.gd._last_opponent_archetype`,
and the two active callsites in `game_main.gd` and
`tools/test_harness.gd`. The legacy `get_opponent()` /
`get_league_opponents()` path is preserved deliberately so the
UI preview layer does not have to re-plumb in this slice. GDD
§6.3 Opponent Archetype Taxonomy lands as the doc anchor.

A counter-play hook (`_player_archetype_hint` parameter) is
reserved in the picker signature but intentionally unwired —
that's the S13.10 payoff.

Two durable process wins came out of this sprint. First,
**Gizmo caught a terminology collision before the brief
committed** — "Fortress" was the working name for the AI concept
in the spec, but "Fortress" was already a chassis name in the
codebase. Gizmo surfaced this during design verification; the
deliverable was renamed to "Opponent Loadouts" in-flight.
This is the **second** mission-critical catch of this shape
from Gizmo (first was S13.6 chassis archetype mapping), and it
is now a codifiable pattern. Second, **Boltz corrected the
parent orchestrator's own flagged concern** about `test_sprint2`
— parent flagged it as a possible regression; Boltz traced the
call path, confirmed it exercises the preserved legacy
`get_opponent()` route and is working as intended, and approved
the merge. Reviewer-as-check-on-orchestrator, not just reviewer-
as-check-on-Nutts.

313 tests pass across the combat suite (S13.4–S13.9), all green.
17/17 new in this sprint (10 from Nutts-A + 7 sub-asserts across
Nutts-B's 4 tests). Two non-blocking Boltz nits carry forward to
S13.10. One arc-level debt (S13.3 deferred combat) closes with
this merge.

## What Shipped

PR #71 (`5affe67`):

1. **Six opponent loadout templates** across five archetypes
   (TANK, GLASS_CANNON, SKIRMISHER, BRUISER, CONTROLLER). Named
   templates — no procedural generation in this slice, variety
   comes from the picker.
2. **Variety-preserving picker** with explicit league→difficulty
   tier mapping: `difficulty_for(league, index)` returns
   `[1, 1, 2]` for scrapyard and `[2, 2, 3]` for bronze. Index
   is the opponent's slot position in the league run, so the
   third opponent is always harder without RNG being able to
   collapse variety.
3. **Counter-play hook reserved** (`_player_archetype_hint`
   param on the picker signature). Threaded but unwired.
   Intentional — implementation lands in S13.10 as part of the
   arc wrap.
4. **Integration surface:**
   - `opponent_data.gd::build_opponent_brott` — picker entry
     point for the new path.
   - `game_state.gd._last_opponent_archetype` — state shim the
     counter-play hook will read from in S13.10.
   - `game_main.gd` + `tools/test_harness.gd` — both callsites
     migrated to the new build path.
5. **Legacy path preserved.** `get_opponent()` /
   `get_league_opponents()` remain — UI preview still uses them
   and re-plumbing was out of scope.
6. **GDD §6.3 Opponent Archetype Taxonomy** — the five
   archetypes documented with role and counter guidance.
   Archetype-tagged chassis (vs template-only) called out as a
   future direction, not committed.

17 new tests in `test_sprint13_9.gd`: 10 from A (template
integrity, picker determinism, tier mapping, variety guarantees)
+ 7 sub-asserts across B's 4 integration tests (build_opponent
path, state shim wiring, callsite parity, GDD cross-ref).

## Pipeline Compliance

Gizmo (direct-write design, ~280 LoC budget, **caught terminology
collision — rename in-flight**) → Ett (direct-write planning,
35s, accepted all 7 of Gizmo's flags, **recommended strict
serial A→B over parallel**) → Nutts-A (templates + picker + tests
1–10, 220 LoC) → Nutts-B (integration + GDD + tests 11–14 + PR,
142 insertions) → Boltz (APPROVE + merge, **corrected parent's
test_sprint2 concern**, 2 non-blocking nits) → Optic (parallel) →
Specc.

- **Gizmo terminology catch (F1, codify).** Spec said "Fortress,"
  codebase already had "Fortress" as a chassis. Gizmo flagged
  this during design verification, before the brief committed,
  and the deliverable was renamed to "Opponent Loadouts" in-
  flight. Second time Gizmo's pre-design verification has saved
  the sprint from a merge-time collision. Pattern is now
  codifiable — see F1 for the KB recommendation.
- **Ett strict-serial call (F4, codify).** Ett's planning pass
  accepted Gizmo's 7 flags and then made the non-obvious call
  to serialize A→B rather than parallelize, despite LoC volume
  suggesting the split was parallelizable. The rationale:
  B depends on A's exported types/signatures (templates +
  picker signature). Parallel execution would have saved ~10
  minutes and risked schema drift across the merge. The call
  was right; the sprint shipped clean with no integration
  churn.
- **Boltz corrected parent's flagged concern (F2, process win).**
  Parent flagged `test_sprint2` as potentially broken by this
  slice. Boltz traced the call path, confirmed it exercises the
  **preserved** legacy `get_opponent()` route (not the new
  build_opponent path), and documented the verdict in the
  review. Reviewer-as-check-on-orchestrator. Healthy pattern.
- **Boltz nits non-blocking.** Two nits landed as S13.10 carry-
  forward (F5): empty-pool guard for unreachable tiers (reachable
  only if template pool becomes sparse at an extreme tier —
  defensive), and a weight-cap validation test (proactive as the
  template pool grows). Neither is a merge blocker.
- **Direct-write dominates.** Gizmo, Ett, and Specc all ran
  direct-write. This is the third consecutive sprint where
  direct-write has been the default posture for exploratory
  agents, and it continues to reduce the timeout rate observed
  in S13.6/S13.8. The posture shift flagged in S13.8 F5 is now
  the de facto standard.

## Verification

- **Tests:** 17/17 pass in `test_sprint13_9.gd` (10 A + 7
  sub-asserts across B's 4). **Combat suite total: 313 tests
  green across S13.4–S13.9.** No regressions.
- **Optic:** PASS pending — running in parallel. Findings below
  are independent of Optic; anything it surfaces lands in S13.10
  backlog.
- **ACs:** Template count, picker semantics, integration
  surface, GDD §6.3 — all covered with tests.
- **Defects at merge:** none blocking. Parent's flagged
  `test_sprint2` concern was traced and dismissed by the
  reviewer (F2).

## Findings

### F1 — Gizmo terminology verification, second mission-critical catch (process win, codify)

Spec brief used "Fortress" as the working name for the AI
opponent concept. The codebase already had "Fortress" as a
chassis name. **Shipping the brief as-written would have produced
colliding "Fortress" references throughout opponent data,
archetype taxonomy, picker code, GDD, and tests** — a terminology
tangle that would have required a rename sprint of its own to
unwind. Gizmo surfaced this during pre-design verification
against the codebase and flagged the rename before the brief
committed. Deliverable renamed to "Opponent Loadouts" in-flight;
sprint shipped clean.

This is the **second** catch of this exact shape from Gizmo. The
first was S13.6's chassis archetype mapping, where a similar
pre-design codebase verification caught a naming assumption that
would have mis-wired the chassis-to-archetype layer. Two data
points in three sprints is a pattern, not a coincidence.

**Codify:** "design agent verifies key noun bindings against
codebase before brief commits." Extend Gizmo's design brief
template with an explicit pre-commit pass that greps the
codebase for every load-bearing noun in the spec and flags
collisions, shadows, or conflicting prior uses. Cheap to add,
mission-critical when it triggers. See KB PR note below for the
recommended trilogy framing with KB #68 and the S13.8 F2 CI
pattern.

### F2 — Boltz corrected orchestrator's own flagged concern (process win)

Parent flagged `test_sprint2` as a possible regression surface
for this slice — the new build path might break the legacy test
if the legacy `get_opponent()` route had been disturbed. Boltz
did not accept the framing on face value. He traced the call
path through `get_opponent()` → `get_league_opponents()` →
preserved legacy code, confirmed `test_sprint2` hits the legacy
path (not the new `build_opponent_brott` path), and documented
the verdict in the review. The concern was unfounded; the
reviewer was right and the orchestrator was wrong.

This is a **different** process win from the Boltz behaviors
captured in prior audits (S13.8 F2 "reviewer runs actual CI"):
that one was reviewer-as-check-on-merge-gate; this one is
**reviewer-as-check-on-orchestrator-assumptions.** Both are
healthy. The pattern here is that Boltz treats every flagged
concern as a hypothesis to verify, not an instruction to act on
— and when the hypothesis is wrong, he says so. That's exactly
what a reviewer should do.

No codification needed — this is Boltz doing his job well. But
worth naming so the pattern persists as a norm rather than
accident.

### F3 — S13.3 deferred combat work CLOSED

Called out for completeness. Opponent variety was the largest
outstanding arc-level debt when S13.3 deferred it (chassis/
archetype scaffolding landed there but opponent-side content
did not). This sprint retires that debt with the full template
+ picker + integration + GDD stack. **Arc going into S13.10
(the wrap) with no major pre-existing debts outstanding.**
S13.6 F4, S13.7 F2, and now S13.3 all closed. Clean lead-in to
the retrospective.

### F4 — Strict serial outperforms parallel for schema-coupled slices (lesson, codify)

Ett's planning pass made the non-obvious call: serialize A→B
instead of parallelize, despite a LoC split (220 + 142) that on
paper looked parallelizable. Rationale: B imports A's exported
types and picker signature; parallel execution risks schema
drift across the merge window, even if local tests green on
both branches. The call was right — sprint shipped with zero
integration churn.

Contrast with S13.8 F1, where true parallel Nutts shipped clean
because there was **no API dependency** between the modal-guard
work (A) and the toast plumbing (B). That was the right call
for that slice.

**Lesson:** parallelizability is a function of API coupling, not
LoC volume. Before defaulting to A∥B, ask whether B imports or
depends on any signature, type, or exported symbol from A. If
yes, serialize — the wall-clock savings from parallel are eaten
back (and then some) by schema-drift reconciliation at merge
time. If no, parallel is safe. This belongs in Ett's planning
heuristics as an explicit check.

### F5 — Carry-forward to S13.10 (backlog)

Five items, none blocking for this merge:

- **Counter-play implementation** using the reserved
  `_player_archetype_hint` param. The hook ships unwired in
  S13.9; wire it in S13.10 as part of the arc wrap deliverable.
- **Picker empty-pool guard** (Boltz nit). Defensive — reachable
  only if the template pool becomes sparse at an extreme tier.
  Current pool size makes this unreachable today, but the guard
  is cheap insurance for future template additions.
- **Weight-cap validation test** (Boltz nit). Proactive coverage
  against weight drift as the template pool grows.
- **Sprint 13 arc wrap audit rollup** (Specc cross-sprint
  synthesis). S13.0 → S13.10 retrospective, landing with S13.10.
- **Optional: `test_sprint2` legacy cleanup or deletion.** No
  urgency — Boltz confirmed the test is fine as-is. Bundle with
  any future legacy-test cleanup pass.

## Grade

**A.** Clean ship, biggest deferred arc debt (S13.3 combat
variety) closed, two durable process wins (Gizmo terminology
catch is now a two-data-point pattern; Boltz corrected the
orchestrator and was right to). Ett's strict-serial call was
right and the lesson is codifiable. No new debt introduced;
carry-forward to S13.10 is entirely non-blocking nits plus the
reserved counter-play hook that was always planned for S13.10.

Not A+: a minor — the counter-play hook threading is a small
speculative-generality risk (it exists but is unwired). The risk
is near-zero since S13.10 is the very next sprint and will wire
it, but strictly speaking an unwired param is a smell. Tolerable
here because the wiring cost is deferred by exactly one sprint
and the hook is a single parameter, not a framework.

## Backlog

- **S13.10 (arc wrap).** Counter-play implementation on the
  reserved hook. Picker empty-pool guard (Boltz nit). Weight-cap
  validation test (Boltz nit). Sprint 13 arc rollup audit. Playtest
  polish pass against observed arc friction. Optional: legacy
  `test_sprint2` cleanup or deletion (no urgency).
- **Post-arc (S14+).** Archetype-tagged chassis (vs template-
  only). Flagged in GDD §6.3 as a future direction; not
  committed. Revisit after playtest data from the S13.10 polish
  pass.

## KB PR Note

Strongly recommend landing a KB PR on battlebrotts-v2 codifying
F1: **"design agent verifies key noun bindings against codebase
before brief commits."** Two data points (S13.6 chassis archetype
mapping + S13.9 Fortress/Opponent rename) — pattern, not
coincidence.

This pairs naturally with KB #68 (TPM-verifies-spec-against-
codebase) and the S13.8 F2 pattern (reviewer-runs-actual-CI-on-
merged-branch) to form a **trilogy of pre-implementation
verification patterns** — design-time, plan-time, and merge-time.
Each pushes verification to where its failure mode actually
surfaces. Worth framing the KB PR with that arc-level structure
explicitly so the three patterns read as a coherent pipeline
philosophy rather than three isolated practices.

Keep the PR short: one paragraph for the pattern, one for the
trilogy framing, references to this audit and S13.6.
