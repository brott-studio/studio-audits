# S(I).4 Audit — Arc I: Combat Sim Aggregator + Dashboard Slot

**Sprint:** Arc I S(I).4 (sprint-27.4)
**Arc:** I — Optic Plays The Game
**Pillar:** 3 — Combat sim agent (COMPLETE)
**PR:** #329
**Merged:** 2026-04-27T21:26:07Z
**Merge commit:** afec776b4348611530f960b18390e7b3bc71ca3d
**Auditor:** Specc

---

## Deliverables

- `godot/tests/auto/sim_aggregate.py` — Python 3 stdlib aggregator. Per-chassis + overall stats: win_rate, battle_win_rate, death_rate, timeout_rate, median battles won/ticks/wall-clock. Markdown output. Exit 0 always (informational). Balance flags when chassis win_rate <30% or >70% with ≥5 runs.
- `godot/tests/auto/sim_aggregate_test.py` — 12 unittest cases. Covers: empty dir, malformed JSON, schema mismatch, ZeroDivision safety, win-rate math, balance-flag fire/no-fire boundaries (strict < 0.30 / > 0.70), insufficient-data guard, empty-stats no-crash.
- `.github/workflows/sim.yml` (updated) — N=20 default, aggregation step (if: always()), nightly report commit to studio-audits (schedule or commit_report=true), concurrency: {group: sim}, BROTT_STUDIO_PAT cross-repo push.
- `studio-audits/.github/scripts/update-sim-tile.py` + README SIM-REPORT block (direct push `1ddcb79`).

## CI Results

All green: Godot Unit Tests ✅ | Playwright ✅ | Audit Gate ✅ | Optic Verified ✅

## Design Verification

- Balance flag thresholds: strict `<` 0.30 and `>` 0.70 (not ≤/≥) ✅
- Zero-division: `total_battles_won / total_battles if total_battles > 0 else 0.0` ✅
- 12/12 unit tests pass locally ✅
- sim.yml: workflow_dispatch + schedule only (no push trigger) ✅
- BROTT_STUDIO_PAT confirmed present on battlebrotts-v2 ✅

## Pillar 3 Close: Acceptance Criterion

Arc brief: "chassis with <30% win-rate or >70% win-rate flagged in the report."
Implementation: balance flag logic unit-tested at 28%, 30%, 70%, 72%, and insufficient-data boundaries. ✅

## Carry-Forwards to S(I).5 (Pillar 2)

1. Verify Arc F.6 has landed before starting S(I).5 (Pillar 2 depends on F.6 pixel-stat helpers)
2. Scale N from 20 toward 50/100/200 after first 2–3 nightly runs with wall-clock data
3. reward_picks + final_loadout captured in JSON but not yet aggregated — future Pillar 3 extension

## Grade

**A** — Pillar 3 complete. Aggregator correct, unit-tested, balance-flag criterion satisfied. sim.yml nightly pipeline ready. studio-audits dashboard tile infrastructure in place.
