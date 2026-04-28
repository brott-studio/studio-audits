# Sprint Audit — Arc J · Sub-Sprint J.2 (sprint-28.2)

| Field | Value |
|---|---|
| **Arc** | J |
| **Sub-Sprint** | J.2 (sprint-28.2) |
| **PR** | #334 — `[sprint-28.2] Scrapyard opponent variety fix (#295)` |
| **Merge Commit** | `b12c96c2cc18c4b1d6438ecf16cc415c0d85630e` |
| **Merged At** | 2026-04-28T04:12:24Z |
| **Grade** | **A** |

---

## What Landed

### SI2-001 — New Scrapyard Legacy Templates
Added three new opponent entries to `godot/data/opponent_loadouts.gd` TEMPLATES:

| Template Key | Archetype | Tier | Weapon | Zone |
|---|---|---|---|---|
| `glass_junksniper` | GLASS_CANNON | T1 | ARC_EMITTER | scrapyard |
| `skirmish_buzzsaw` | SKIRMISHER | T1 | MINIGUN | scrapyard |
| `bruiser_scrapdog` | BRUISER | T2 | SHOTGUN | scrapyard |

### SI2-002 — `brawler_rush` Archetype Added
Added `brawler_rush` archetype to ARCHETYPE_TEMPLATES in `godot/data/opponent_loadouts.gd`.
T1 archetype weights updated:

| Archetype | Old Weight | New Weight |
|---|---|---|
| `standard_duel` | — | 40 |
| `small_swarm` | — | 15 |
| `large_swarm` | — | 10 |
| `glass_cannon_blitz` | — | 15 |
| `brawler_rush` | *(new)* | 20 |

Total ARCHETYPE_TEMPLATES count: 7 → 8.

### SI2-003 — Variety Test Suite (New File)
`godot/tests/test_s28_2_scrapyard_variety.gd` — NEW test file:
- 200-run legacy TEMPLATES variety test (scrapyard zone)
- 200-run T1 archetype variety test
Registered in `godot/tests/test_runner.gd`.

### SI2-004 — GDD Documentation
`docs/gdd.md` — `brawler_rush` row added to §13.4 archetype table, keeping documentation in sync with implementation.

### Supporting Test Updates
- `godot/tests/test_multi_target_ai.gd` — ARCHETYPE_TEMPLATES count assertion updated 7→8
- `godot/tests/test_s28_1_t1_weights.gd` — T1 weight assertions updated to reflect J.2 distribution

---

## Verification Results

| Gate | Description | Result |
|---|---|---|
| Gate 1 | ≥4 Scrapyard templates | ✅ PASS — 4 templates confirmed |
| Gate 2 | ≥3 distinct archetypes in Scrapyard | ✅ PASS — 4 archetypes (TANK, GLASS_CANNON, SKIRMISHER, BRUISER) |
| Gate 3 | Variety test pass_rate ≥95% | ✅ PASS — pass_rate=1.000 (100%) for both 200-run suites |
| Gate 4 | No Bronze regression | ✅ PASS — Bronze templates unchanged (count 7: 6 original + `bruiser_scrapdog` additive via rank filter, no templates removed) |
| Gate 3e.5 | Deploy freshness | ✅ PASS — Last-Modified 2026-04-28T04:13:57Z (~1.5 min post-merge) |

All 5 gates pass. No regressions detected.

---

## Grade Rationale

**Grade: A**

All 5 verification gates passed cleanly post-merge. The variety test achieved a perfect pass_rate of 1.000 (100% over 200 runs), exceeding the 95% threshold. Scrapyard zone now has 4 templates spanning 4 distinct archetypes, satisfying the opponent variety goal. Bronze templates are unaffected. Documentation and tests are in sync.

---

## Issue #295 Status

Issue #295 was referenced (not auto-closed) in PR #334. All gates defined for this issue are now satisfied. **Recommend: close issue #295 as resolved.**

---

## Test Fix Iterations

The PR required **3 fix commits** after initial PR open before CI was fully green:

1. **Fix 1 — Exit API:** `OS.exit` replaced with `quit(1)` (correct Godot 4 API for test exit).
2. **Fix 2 — Count assertion:** `test_multi_target_ai.gd` ARCHETYPE_TEMPLATES count updated 7→8 to match the new `brawler_rush` entry.
3. **Fix 3 — Bronze legality:** `glass_junksniper` weapon changed RAILGUN→ARC_EMITTER and `skirmish_buzzsaw` weapon changed FLAK_CANNON→MINIGUN to satisfy the `bronze_legality` test (weapons must be valid for the assigned tier/archetype).

Net result: all tests green at merge.

---

## Learning Extractions

**Pattern 1 — Bronze legality gate catches weapon mismatches early.**
The `bronze_legality` test enforced weapon validity constraints that were not apparent from the loadout design alone. When adding new templates, weapon–archetype–tier compatibility should be cross-checked against the legality table *before* opening the PR to avoid iterative fix commits.

**Pattern 2 — Archetype count assertions require coordinated updates.**
Adding a new archetype entry (ARCHETYPE_TEMPLATES count change) requires updating all tests that assert the total count. A shared constant or single-source count reference would eliminate the need for manual assertion updates across multiple test files (`test_multi_target_ai.gd`, `test_s28_1_t1_weights.gd`).

---

*Audit produced by Specc (Inspector) · 2026-04-28*
