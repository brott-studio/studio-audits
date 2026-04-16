# Sprint 13.x Arc Rollup — BattleBrotts v2

**Inspector:** Specc
**Date:** 2026-04-16
**Arc span:** Sprint 13.1 → 13.10
**Final merge SHA:** `4d63461` (PR #73)
**Status:** **CLOSED**
**Arc grade:** **A**

---

## 1. Arc thesis

Sprint 13 was the arc where BattleBrotts v2 stopped being a collection of systems and started being a **loop**. Entering 13.1, the pieces existed on paper but didn't hang together end-to-end; exiting 13.10, Eric could play a full Scrapyard league run and the shop → loadout → trick-choice → combat → opponent flow is coherent, legible, and — crucially — *surfaces its own remaining gaps* in the form of a real playtest bug/UX list rather than "I don't know what this game is yet."

Two things were done at once:

1. **Solidify the core loop** as a contiguous player experience — TCR combat, chassis archetypes, opponent loadouts, the trick-choice framework with flavor, BrottBrain voice, and shop hardening.
2. **Establish the process patterns** needed to scale this work — the verification trilogy (plan-time, design-time, merge-time), direct-write briefs as default, and parallel/serial discipline calibrated to the work type.

The second is the less visible but probably more durable deliverable. The studio came out of 13.x with not just more game, but a better process for making more game.

---

## 2. Per-sprint capsules

| Sprint | Grade | What shipped | KB born |
|---|---|---|---|
| 13.1 | A | Docs-only: merged S12 KB PR #53, GDD drift fixes PR #54 | — |
| 13.2 | B+ | TCR state machine (Tension→Commit→Recovery), cross-chassis projectile fix | — |
| 13.3 | A | TCR balance pass + chassis archetypes (foundational); Fortress loadout deferred | — |
| 13.4 | A | Combat outcome system + first content beats | — |
| 13.5 | A | Trick choice framework + initial Scrapyard tier content | — |
| 13.6 | A | BrottBrain LLM voice + first procedural trick (F1/F4 left open, closed later) | **#68** (plan-time spec verification) |
| 13.7 | A | Item token router + 3 new tricks + flavor system (PR #67); closes S13.6 F1 | — |
| 13.8 | A | Modal hardening + CI glob test discovery + dynamic item-name toast + GDD voice (PR #69); closes S13.6 F4 & S13.7 F2 | **#70** (merge-time CI verification) |
| 13.9 | A | Opponent loadout pass — 6 templates × 5 archetypes, variety picker, difficulty mapping (PR #71); closes S13.3 Fortress debt | **#72** (design-time noun verification) |
| 13.10 | A | Quiet arc wrap: picker empty-pool guard + weight-cap test + test_sprint2 cleanup + playtest capture + UX vision doc (PR #73 `4d63461`) | — |

---

## 3. Process patterns codified — the verification trilogy

Three KB entries born in this arc form a coherent pattern: **verify against ground truth at every phase boundary, not just at the implementation boundary.**

- **KB #68 — plan-time:** TPM verifies spec field names against the codebase before briefing engineers out. Catches "the brief references a field that doesn't exist" before Nutts burns a cycle on it.
- **KB #72 — design-time:** design agent verifies key noun bindings against the codebase before committing briefs. Catches "the design says `grip_slot` but the code calls it `handle_mount`" at the source.
- **KB #70 — merge-time:** reviewer runs actual CI on the merged branch before approving. Catches "CI was green on the feature branch but the merge commit breaks something" before it lands on main.

Why this matters: most studios treat verification as an implementation-phase concern (write tests, run CI). This trilogy **pushes verification upstream across three distinct phases** — planning, design, and merge. Each phase now has an explicit "does this match reality?" gate. The failure modes these catch are the ones that historically ate the most cycles: spec-code drift, design-code drift, and merge-base drift.

The trilogy is now complete. It should not be extended reflexively — a fourth would be forcing symmetry where the phase model doesn't warrant it.

---

## 4. Other process wins

- **Direct-write briefs became the default** for Gizmo/Ett/Specc. Explore-until-timeout failures dropped substantially when briefs arrived with enough context to execute rather than enough context to "go find out."
- **True parallel Nutts validated in S13.8** — first successful A/B parallel run with the merge-helper pattern end-to-end. The merge-helper spawn is now a repeatable pattern for A/B collision resolution.
- **Strict serial outperformed parallel for schema-coupled work** (S13.9 lesson). Parallel is not a free win; when two branches both touch the same data schema, the merge cost dominates the parallel savings. Serial is now the default for schema-coupled work; parallel is the choice for genuinely orthogonal work.
- **Reviewer-as-orchestrator-check:** in S13.9, Boltz caught the parent orchestrator's unfounded worry about `test_sprint2`. The reviewer role is now established as a check on orchestrator assumptions, not just on engineer output.

---

## 5. Debts closed this arc

- **S13.3 Fortress loadout pass** → closed in **S13.9** (opponent loadout pass)
- **S13.6 F1** ITEM_GRANT / ITEM_LOSE stubs → closed in **S13.7** (item token router)
- **S13.6 F4** modal hardening → closed in **S13.8**
- **S13.7 F2** CI regression pattern → closed in **S13.8** (glob test discovery)
- **S13.9 Boltz nits** → closed in **S13.10**

Five cross-sprint debts, all retired within the arc. No 13.x debt bleeding into 14.x — a healthy close.

---

## 6. Closing observations from playtest (Eric, end-of-arc run)

These are **observations**, not a todo list. S14 scoping happens separately, after the creative conversation.

### Critical blockers
- **League progression UI missing.** Eric beat Scrapyard and saw only a REMATCH button — dead-end. The tier ladder exists in content but has no exit ramp in UI.
- **Bots stuck on walls.** Repeatable nav/collision bug. Movement is the player's primary sensory read of the game; this is highly visible.

### UX pain
- Shop scroll too fast even at minimum; clicking jumps back to top.
- Tooltips are hover-only and went undiscovered.
- Loadout items cover the shop button when the loadout is full.
- Crate/trade popup frequency too high.
- First-shown crate-decision screen is context-less on first encounter.
- BrottBrain editor: drag doesn't work, delete is unintuitive, boxes overlap.
- Energy bar (blue) is unexplained in-game.

### Feel
- **Scout jerkiness is a smoothing problem, not a speed problem.** Turn rate, accel/decel curves, and direction-change lerp are the levers. Capping speed would lose the positive (fast, exciting).
- **Fight 3 feels long when losing.** Concede button or a shorter low-HP endgame are the two directions worth weighing.

### Braincard library
- **Missing:** aggressive/committal cards — "Charge," "Chase after." The library skews toward conditional/passive logic.
- **Present but unwanted:** abstract timing cards — "Clock time." These read as system-y rather than brott-y.

### Random events
- Feel bad-chaotic. Three candidate directions: reduce frequency, make skippable, or redesign the reward structure so the chaos feels earned.

### Overall
- Polish gap vs. target. Not a single-fix item — a cumulative texture thing. The core loop lands; the surface doesn't yet read as finished.

### Creative north stars (shaping, not planning)
- **Audio vision — WALL-E.** Established earlier in the arc.
- **UX vision — Eve from WALL-E** (codified S13.10 in `docs/kb/ux-vision.md`). Clean, purposeful, almost nothing on screen that isn't earning its place.

These are directional inputs for S14 creative framing. They are not roadmap items.

### Positives to preserve (do not regress in S14)
- **Shop is "super cool."** Don't let shop changes erode this.
- **Fight variance from the same loadout is fun.** This is a core positive and it's fragile — any tuning pass that flattens outcome variance kills it. Protect it explicitly.
- First scout fight is exciting.
- Beating fight 3 feels earned.
- BrottBrain crafting is "almost fun" — rewarding when the brott obeys the built logic. The crafting loop is closer than it feels.
- Watching the brott execute built logic is satisfying. This is the game's emotional core when it hits.

---

## 7. Latent risks (carry to S14 awareness, not necessarily action)

- **`game_main.gd:199`** — unguarded `enemy_brott.position = ...` assignment. If tier-1 templates are ever empty, the defensive `null` return upstream will crash at this call site. Pre-existing, not introduced in this arc. Boltz flagged it in S13.10. Worth a tracking note at S14 kickoff.

---

## 8. Arc grade — **A**

Making the case:

- **Scope shipped:** 10 sprints (13.1–13.10), all merged, no rollbacks.
- **Quality trend:** Grade A on every sprint from 13.3 onward. The one B+ (13.2) was a recoverable combat-rhythm fix that did its job.
- **Debt hygiene:** 5 cross-sprint debts opened and closed within the arc. Zero code debt bleeds into 14.x.
- **Major foundational debt retired:** S13.3 Fortress loadout, deferred for six sprints, closed decisively in S13.9.
- **Process deliverables:** 3 KB entries forming a coherent verification trilogy across plan/design/merge phases. Direct-write briefs validated as default. Parallel vs. serial discipline calibrated.
- **Playtest reached real player experience.** The bug/UX list coming out of S13.10 is the list you get from a game that works well enough to have legible failure modes — not from a game that doesn't work yet. That's a qualitative milestone.

Against an A:

- **Polish gap is real.** The arc closed with the core loop solid but the surface unfinished. An "A+" arc would have narrowed that gap.
- **Critical blockers surfaced late.** League progression dead-end and nav bugs should have been caught earlier — possibly by lighter-touch playtests mid-arc rather than only at arc close. S14 process could include a mid-arc playtest cadence.

Net: **A.** Strong, not perfect. Honest grade.

---

## 9. What S14 needs (framing only)

S14 planning is **deliberately paused** for creative alignment. Eric wants a creative conversation with the parent agent before Gizmo or anyone else touches the next sprint brief.

Framing notes for that conversation:

- The playtest surfaced **two distinct problem classes**: (a) blockers and UX bugs that are straightforwardly scope-able, and (b) feel / polish / creative-direction questions that require decisions before they can be scoped. S14 shouldn't mix these without explicit sequencing.
- The creative north stars (WALL-E / Eve) are **shaping inputs**, not feature specs. S14 should absorb them as aesthetic constraints on whatever is chosen, not as a feature list.
- The braincard library gap (aggressive/committal cards missing; abstract timing cards unwanted) is a **design question**, not an engineering one. It wants Ett before it wants Nutts.
- The "fight variance from same loadout is fun" positive is a **tuning guardrail** for any S14 combat/opponent work. Write it into whatever brief touches combat.
- The latent `game_main.gd:199` risk is cheap to guard and deserves a tracking note at S14 kickoff regardless of what else gets prioritized.

That's framing, not planning. The plan comes out of the creative conversation.

---

**Arc closed.**
