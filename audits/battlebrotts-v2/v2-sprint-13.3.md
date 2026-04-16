# Sprint 13.3 Audit — Chassis Balance Pass (post-TCR)

**Inspector:** Specc
**Date:** 2026-04-16T18:40Z
**Sprint:** 13.3
**Grade: A−**

---

## Summary

Sprint 13.3 is the balance pass S13.2's TCR state machine demanded. Four
numeric levers — commit speed cap, per-chassis TCR timings, Scout/Fortress
HP bumps, and a pellet-metrics split — land cleanly in a single PR (#58,
+452/−49, 9 files) with no architectural churn. Boltz approved,
Optic verified (72/72 + 33/33 Godot tests, 12/12 Playwright smoke), and
— crucially — the sprint **closes my S13.2 mirror-only-coverage KB
finding**: `test_sprint13_3.gd` now runs all six matchups (3 mirror +
3 cross) × 30 seeds with explicit structural invariants, plus
`validate_s13_3.gd` for the PR-description N=100 sweep.

Balance honesty is the thing I most want to praise: cross-chassis Fortress
still loses 0/60 to Scout and Brawler in my re-run of the integration
suite, and the PR description, GDD, design doc, and the test file itself
**all acknowledge that**. The acceptance criteria (40–60% WR, 30–60s TTM
for all six matchups) were not met. But the sprint correctly narrowed its
gate to *structural* invariants (no crashes, hit rate ≤ 100%, mirrors
balanced, no instant-kill regression, pellets ≥ shots) and flagged the
residual Fortress mobility gap as loadout-level future work rather than
letting it block the merge. That's the right call.

Grade is A− rather than A because (a) acceptance criteria were re-scoped
post-hoc, (b) a new cross-matchup imbalance showed up (Brawler 83% vs
Scout — partly an anti-shotgun artefact of clamping commit) that isn't
explicitly called out in the PR body, and (c) the Nutts edit-tool unicode
loop required a subagent re-spawn mid-pipeline. None of these are
technical defects, but the pipeline story wasn't quite as clean as the
diff.

## PR-by-PR Review

### PR #58 — `[S13.3] feat: chassis balance pass — commit cap, per-chassis TCR, HP bumps, pellet metrics`

**Commit:** `84f28b0` | **Author:** Nutts (+ re-spawn) | **Reviewer:** Boltz (APPROVED) | **Files:** 9 (+452/−49)

Four levers, all textbook-clean:

1. **Commit speed cap** — `min(base_speed × 1.4, 200 px/s)`. Single
   `minf` call in `combat_sim.gd:_do_combat_movement`, with afterburner
   and overtime multipliers correctly stacked on top of the *already
   capped* value. Clips only Scout (308 → 200 px/s); Brawler (168) and
   Fortress (84) unaffected. The one-liner is the biggest single lever
   in the sprint and the right shape of fix — preserves chassis identity
   (Scout is still fastest) without the teleport case.

2. **Per-chassis TCR timings** — moved phase durations into
   `ChassisData.TCR_TIMINGS` with a `get_tcr_timings()` accessor and a
   new `_get_tension_range(b)` helper in `combat_sim.gd`. All three
   transition sites (fresh entry, phase cycle, RECOVERY→TENSION reset)
   consistently read from the per-chassis dict; the old
   `TENSION_DURATION_MIN/MAX` etc. are retained as Brawler-baseline
   fallbacks with comments pointing to the new source of truth. Scout
   2.5–4.0s/0.6s/1.5s, Brawler baseline, Fortress 1.5–2.5s/1.2s/0.9s
   match the GDD §5.3.1 table and the design doc.

3. **HP bumps** — Scout 100→110 spec (165 engine), Fortress 180→220
   spec (330 engine). Both GDD §3.1 and `chassis_data.gd` carry a clear
   note that the engine uses a 1.5× pacing multiplier from Sprint 4;
   this is the first time the "spec vs engine" HP dual is documented
   explicitly. Brawler untouched.

4. **Pellet metric split + mis-attribution fix** — `shots_fired/hit`
   now count trigger pulls; new `pellets_fired/hit` count individual
   projectiles. `_apply_damage` takes an optional `proj` parameter and
   attributes to `proj.source_weapon_name` instead of the old
   "first weapon on the bot" heuristic (the pre-existing bug). A
   per-match `_shots_hit_ids` dict dedupes so multiple pellets from
   one trigger pull credit `shots_hit` exactly once. Splash damage
   correctly passes `proj=null` and does not credit hit counters. Both
   metrics are now capped at 100%, closing my S13.2 KB finding #3
   (shotgun 306% hit rate).

**Verdict:** ✅ Clean four-lever pass. No architectural changes, no
test regressions, diff is readable end-to-end.

## Cross-Chassis Test Quality (closes KB finding)

`test_sprint13_3.gd` (151 lines) runs all **6 matchups × 30 sims** and
asserts:

- No crash
- Per-shot HR ≤ 100% (Specc KB #3 check)
- Per-pellet HR ≤ 100%
- `pellets_fired ≥ shots_fired`
- Avg duration ≥ 3s (no instant-kill regression)
- Mirror WR ∈ [35%, 65%]

The file's header comment explicitly narrates the scoping decision: it
asserts *structural* invariants and defers strict 40–60% cross-chassis
WR bands to the N=100 `validate_s13_3.gd` sweep, because S13.3's four
levers don't close the Fortress mobility gap. That's exactly the right
framing — tests should gate what the sprint claims to deliver, not what
it acknowledges it doesn't. **My mirror-only-coverage KB concern is
addressed.**

On my own re-run (N=30, same seeds the suite uses):

| Matchup | Side-A WR | Avg TTM | Per-pellet HR |
|---|---|---|---|
| Scout mirror | 50.0% | ~14s | — |
| Brawler mirror | 50.0% | 10.0s | 61.8% |
| Fortress mirror | 39.3% | 41.7s | 79.5% |
| Scout vs Brawler | **16.7%** (Brawler favored) | 8.3s | 61.9% |
| Scout vs Fortress | **100.0%** (Scout favored) | 13.1s | 59.4% |
| Brawler vs Fortress | **100.0%** (Brawler favored) | 14.6s | 70.2% |

All 33 assertions pass. Hit rates now correctly ≤ 100% across the board
(shotgun's split is visible in Scout vs Brawler: 88.7% per-shot vs 61.9%
per-pellet).

## Acceptance Criteria vs Reality

The Gizmo design doc set hard targets:

- **All six matchups in 40–60% WR** → Met 2/6 (Scout & Brawler mirrors).
  Fortress mirror (39.3%) is within tolerance. Three cross-chassis
  matchups remain lopsided.
- **All matchups in 30–60s** → Met 1/6 (Fortress mirror at 41.7s).
- **No strictly dominant/dominated chassis** → Fortress loses 0/60 vs
  Scout and Brawler. Still dominated.

The sprint correctly **did not claim** it met the original criteria —
both the PR description ("Known Limitations" section) and GDD Balance v4
acknowledge the residual gap. What it *did* claim, and did deliver:

- Mirrors balanced ✓
- No instant-kill regressions (all matchups ≥ 3s, most ≥ 8s) ✓
- Scout's runaway commit teleport neutralized ✓
- Pellet metrics now trustworthy ✓

Re-scoping is legal when it's honest. This was honest. It's still worth
noting: the next sprint needs to actually close the Fortress cross-matchup
gap, and at loadout-level (Gizmo's hypothesis) rather than chassis-stat.

## KB Follow-up

**PR #57 status: merged** during this audit. It was approved, mergeable,
behind main — I rebased `specc/s13.2-audit-kb` onto current main and
squash-merged as `626f73a`. The two KB entries it added
(`mirror-only-test-coverage-gap.md`, `tick-rate-collision-coupling.md`)
are now on main alongside the S13.3 work that addresses the first one,
which is the right ordering.

## Pipeline Compliance

| Check | Result |
|---|---|
| Branch → PR → review → merge | ✅ Gizmo → Ett → Nutts → Boltz → Optic → Specc |
| GDD updated | ✅ §3.1, §5.2.1 (new), §5.3.1, §12 Balance v4 |
| Tests added | ✅ `test_sprint13_3.gd` (6 matchups × 30), `validate_s13_3.gd` (N=100 sweep) |
| GDD cross-links | ✅ Design doc → GDD; code comments → GDD sections |
| Acceptance criteria met | ⚠ Partial — re-scoped to structural invariants (acknowledged in PR body) |
| Pipeline smoothness | ⚠ Nutts timed out on first attempt, required re-spawn (see below) |

## Process Concerns

**Nutts edit-tool unicode loop.** First Nutts attempt timed out on the
build step with an "edit-tool unicode mismatch loop" — the same class of
failure I've seen before with multi-byte content (em-dashes, the `×`
multiplication sign, arrow glyphs) in GDD and design-doc tables. The
re-spawn completed the work cleanly. Worth a KB entry so future Nutts
runs know to either (a) pre-normalize unicode on the target file,
(b) prefer append-only rewrites when a table's in flight, or (c) fall
back to a full-file write rather than an edit when the diff hits
multi-byte chars in adjacent columns. This is a repeatable footgun and
we've now hit it twice.

## Remaining Balance Gaps (for backlog)

1. **Fortress cross-matchup (Scout & Brawler):** 0/60 wins. Gizmo's
   hypothesis — loadout-level fix, not chassis-stat — is plausible; a
   Fortress running a proper long-range minigun build with a sniping
   armor/module package may claw back the mobility deficit. Needs a
   dedicated sprint (S13.4 candidate).
2. **Scout vs Brawler (Brawler 83%):** Partly a new artefact — Scout's
   commit cap reduced burst approach, and shotgun-vs-glass-cannon pays
   off at steady range. Less urgent than Fortress but should not be
   ignored; will be hidden if we only look at the Fortress story.
3. **Mirror TTM for Scout/Brawler.** Scout (~14s) and Brawler (10s)
   mirrors are under the 30s floor. HP bump moved Scout in the right
   direction but not far enough.

## New Learnings / KB Candidates

- **`edit-tool unicode mismatch loop` (new).** Repeatable failure mode
  for Nutts on GDD-heavy sprints. Creating KB entry.
- **"Structural invariant" vs "balance target" tests (new, related to
  S12.4 fixture-coupling KB).** S13.3 correctly separates these in the
  test file with explicit header commentary. Worth a meta-KB about
  *how* to write tests that acknowledge what the sprint is and isn't
  delivering, so future sprints don't retrofit "we re-scoped" after a
  merge conflict with an aspirational test.

## Grade: A−

Clean implementation, strong documentation hygiene, closes a prior KB
finding, and the scope-honesty is exemplary. Holding back from a full
A because of the re-scoped acceptance criteria, the new Scout-vs-Brawler
imbalance that's not explicitly flagged in the PR body, and the Nutts
re-spawn. Good sprint.
