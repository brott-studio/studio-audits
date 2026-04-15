# Sprint 11 End-of-Sprint Audit

**Inspector:** Specc
**Date:** 2026-04-14
**Sprint Goal:** Back to Features — Playable Web Build

---

## 1. PR #57 Code Quality — Playable Web Build

**Verdict: STRONG ✅**

PR #57 (`[S11-001] Playable Web Build — Full Campaign UI Flow`) delivers 878 lines across 16 files. Key observations:

### Architecture
- **CampaignUI** (`campaign_ui.gd`, 173 lines) — clean state-machine controller using an enum for 6 screens (MAIN_MENU → SHOP → LOADOUT → OPPONENT_SELECT → MATCH → RESULT). Visibility toggling via `_show_screen()` is simple and correct.
- **Screen separation** — Each screen is its own script (shop_screen_ui, opponent_select_ui, main_menu, result_screen). Clean separation of concerns with minimal coupling via `campaign_ui` back-reference.
- **Economy integration** — Shop screen wires through to CampaignController for catalog/buy operations. Bolt balance displayed and updated correctly.

### Issues (Minor)
1. **`result_screen.gd` still has Sprint 4 header comment** — stale attribution. The file was modified in this PR but the header wasn't updated.
2. **`_get_campaign_ui()` in main_menu.gd** — walks up the tree to find parent by method name. Works but is fragile; a typed reference (like shop/opponent screens use `setup()`) would be more consistent.
3. **No null guards on some `@onready` nodes** — `shop_screen_ui.gd` and `opponent_select_ui.gd` use `@onready` vars that could be null if scene tree structure changes. Some paths have guards, others don't (inconsistent).

### Positives
- Consistent file headers with sprint/task attribution
- Signal-based communication (screen_changed, match_tick, match_finished)
- Campaign loop is fully playable: new game → shop → loadout → opponent → match → result → loop
- `main.tscn` expanded (287 lines of scene changes) — proper scene-tree integration

## 2. Test Coverage — 387 Tests

**Verdict: GOOD with GAPS ⚠️**

### Coverage by count
| Test file | Count |
|---|---|
| test_integration.gd | 41 |
| test_data_validation.gd | 31 |
| test_arena.gd | 27 |
| test_campaign.gd | 25 |
| test_loadout_screen.gd | 25 |
| test_match_hud.gd | 24 |
| test_economy.gd | 24 |
| test_result_screen.gd | 23 |
| test_brott.gd | 22 |
| test_brottbrain.gd | 20 |
| test_league.gd | 20 |
| test_match_manager.gd | 16 |
| test_game_controller.gd | 15 |
| test_tick_system.gd | 13 |
| **test_campaign_ui.gd** | **12** |
| test_damage_calculator.gd | 12 |
| test_shop.gd | 12 |
| test_pathfinder.gd | 9 |
| test_steering.gd | 8 |
| test_projectile.gd | 8 |
| **Total** | **387** |

### New tests from PR #57
- `test_campaign_ui.gd` (12 tests) — covers screen enum, new game init, shop buy, catalog, loadout, opponent info, league progress. Good functional coverage of CampaignController integration.

### Gaps identified
- **main_menu.gd** — no dedicated test file. `_get_campaign_ui()` tree-walking logic untested.
- **opponent_select_ui.gd** — no dedicated test file. UI population logic untested.
- **shop_screen_ui.gd** — no dedicated test file. Category/item population untested.
- **arena_view** — no test file.

The campaign_ui tests cover the *controller logic* well but the individual UI screen scripts (shop_screen_ui, opponent_select_ui, main_menu) lack unit tests. These are thin UI wrappers so risk is moderate, but it's a gap.

## 3. Sprint-Config Auto-Tracking

**Verdict: PARTIALLY WORKING ⚠️**

### What works
- `sprint-config.json` correctly shows Sprint 11 as `active` with 6 tasks (S11-001 through S11-006).
- Sprint 10 is in history as `complete` with all 4 tasks done.
- Sprint open commit (`da02f7b`) properly updated config.

### What doesn't work
- **All S11 tasks still show `todo`** despite PR #57 being merged (which should mark S11-001 as `done`). The `update-sprint-status.yml` workflow was triggered (PR #54 was auto-generated) but Sprint 11's S11-001 status was NOT updated.
- **`data.json` is stale** — still shows Sprint 10 data (sprint number: 10, status: complete). The dashboard workflow ran after PR #55 but regenerated with old data. This means the dashboard auto-update ran *before* the Sprint 11 config was pushed, and hasn't re-run since.
- **Race condition**: PR #57 merged, then the sprint-open commit landed. The sprint-status workflow may have run against the old sprint-config (still Sprint 10) and found nothing to update.

**Root cause:** The sprint was opened in the same commit window as PR #57 merge. The workflow likely processed PR #57's merge against Sprint 10's config (already complete → skipped), then the sprint-open commit landed after.

## 4. Dashboard Currency

**Verdict: STALE ❌**

- `data.json` at repo root shows Sprint 10 data.
- Should show Sprint 11 with S11-001 done.
- Requires a manual workflow dispatch or another push to trigger `update-dashboard.yml`.

## 5. Process Compliance

**Verdict: GOOD ✅**

- PR #57 follows commit convention: `[S11-001] Playable Web Build — Full Campaign UI Flow`
- Tests included with the feature PR (12 new tests)
- Sprint planning done properly (S10-004 → backlog review → Sprint 11 tasks)
- Task IDs properly assigned with roles (devops, dev-01, playtest-lead, pm)
- Role-boundary-check workflow in place
- PR checklist workflow active

### Sprint velocity
- First feature sprint after 4 process sprints (S7-S10)
- Single large PR delivering the core campaign loop
- 6 tasks planned; 1 completed in sprint so far
- Remaining 5 tasks (S11-002 through S11-006) are still `todo`

## 6. KB Quality Audit

**Verdict: ADEQUATE ✅**

Current KB entries (4 total):
1. `kb/patterns/ops-role-checklist.md` — operational
2. `kb/patterns/sprint-config-as-source-of-truth.md` — process
3. `kb/postmortems/dashboard-three-fixes.md` — incident
4. `kb/troubleshooting/godot-classname-headless.md` — technical

Coverage is thin but focused. No stale entries detected. All remain relevant to active concerns.

### Learning extraction (Standing Directive #2)
No session transcripts available for Nutts/Boltz sessions from this sprint context. Unable to extract learnings without access to those sessions' outputs. **No KB entries warranted from available data.**

## Recommendations

1. **Fix dashboard staleness** — Trigger `update-dashboard.yml` manually or push a trivial commit to regenerate `data.json` for Sprint 11.
2. **Fix sprint-status for S11-001** — Run `update-sprint-status.yml` manually. The race condition between sprint-open and PR merge needs a sequencing fix (sprint-open should always precede feature PRs).
3. **Add UI screen tests** — main_menu, opponent_select_ui, and shop_screen_ui need at least basic test coverage. Target: +15-20 tests.
4. **Update result_screen.gd header** — Stale "Sprint 4" comment.
5. **Standardize parent-reference pattern** — Either use `setup(parent)` injection everywhere or tree-walking everywhere, not both.

---

**Overall Sprint 11 Grade: B+**

Strong feature delivery — the campaign UI loop is architecturally sound and well-tested at the controller level. Process compliance is good. The auto-tracking infrastructure built in Sprints 8-10 hit a race condition on its first real feature sprint, revealing a sequencing gap. Dashboard is stale but fixable with a workflow dispatch.
