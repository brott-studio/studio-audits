# Audit: v2-sprint-25.10 — Corporate-Ladder Opponent Title Re-skin

**Date:** 2026-04-26
**Sprint:** S25.10
**PR:** brott-studio/battlebrotts-v2#310
**Merge SHA:** 9aa417fdfd63daa7ac1eea097a0b5c276e07cf73
**Auditor:** brott-studio-specc[bot]

## Gate Results

| Gate | Status | Notes |
|---|---|---|
| G1: 19 non-boss corporate titles present | PASS | All 19 expected corporate titles found across 19 non-boss TEMPLATES entries. |
| G2: CEO Brott boss row untouched | PASS | `"display_name": "CEO Brott"` present on the boss encounter row (line 527); no boss-row changes in the diff. |
| G3: Name-strings-only diff | PASS | PR #310 touches one file (`godot/data/opponent_loadouts.gd`) with 19 additions / 19 deletions; every changed line is a `"name":` string. No mechanics, archetype, tier, chassis, weapons, armor, modules, stance, unlock_league, or behavior_cards changes. |
| G4: No duplicate titles | PASS | All 19 corporate titles are unique (verified by `sort \| uniq -c`). |
| G5: Tier-title mapping sensible | PASS | Tier 1 → Intern/Junior; Tier 2 → office/department mid-management (Office Manager, "Brott from X", District Sales Manager, Senior Account Manager, Temp); Tier 3 → VPs, Directors, Senior Analyst, Head of Internal Affairs; Tier 4 → C-suite (COO, CFO, Chief Strategy). Boss = CEO. Coherent corporate ladder. |

## Overall: PASS

## Title inventory

| template_id | tier | new name |
|---|---|---|
| tank_tincan | 1 | Intern Brott |
| skirmish_wasp | 1 | Junior Associate Brott |
| tank_ironclad | 2 | Office Manager Brott |
| glass_sniper | 2 | Brott from IT |
| bruiser_crusher | 2 | District Sales Manager Brott |
| tank_rustwall | 2 | Senior Account Manager Brott |
| glass_zap | 2 | Brott from Accounting |
| skirmish_scrapper | 2 | Temp Brott |
| bruiser_clanker | 2 | Brott from Compliance |
| controller_jammer | 3 | VP of IT Security Brott |
| control_static | 3 | Director of Operations Brott |
| control_prowler | 3 | Head of Internal Affairs Brott |
| tank_bulwark | 3 | VP of Infrastructure Brott |
| glass_trueshot | 3 | Senior Analyst Brott |
| skirmish_harrier | 3 | VP of Aggressive Sales Brott |
| bruiser_enforcer | 3 | Director of HR Brott |
| control_disruptor | 4 | COO Brott |
| tank_aegis | 4 | CFO Brott |
| glass_chrono | 4 | Chief Strategy Brott |
| (boss row) | — | CEO Brott (unchanged) |

## Carry-forwards
- `godot/game/opponent_data.gd` scrapyard hardcoded list ("Rusty"/"Tincan"/"Crusher") excluded from this sprint — scrapyard is pre-corporate-ladder intro league. Future refactor opportunity if scrapyard remains in shipped build.

## Notes
- Schema field is `"id"` (not `"template_id"`) per `TEMPLATES` definition; mapping above uses the actual field name.
- Diff is minimal and surgical: 19 add / 19 del on a single file, exactly matching the count of non-boss templates.
