# Sprint 16 End-of-Sprint Audit (Covering Sprints 14–16)

**Inspector:** Specc  
**Date:** 2026-04-15  
**Sprint Range:** 14 (Balance + Infrastructure) → 15 (Aggressive Balance v2) → 16 (Final Balance v3)  

---

## 1. Balance Tuning Process Quality

**Verdict: ✅ EXCELLENT — The data-driven approach works.**

Three successive balance passes, each informed by 1,500+ headless simulations:

| Metric | S12 Baseline | S14 (v1) | S15 (v2) | S16 (v3) | Trend |
|--------|-------------|-----------|-----------|-----------|-------|
| Fortress WR | 80.3% | 78.6% | 72.9% | **64.4%** | 📉 Converging toward 55% |
| Scout WR | 15.7% | 20.1% | 20.4% | **30.5%** | 📈 Major jump in S16 |
| Brawler WR | 49.1% | 51.3% | 56.7% | **55.1%** | ✅ On target |
| Minigun Shot Share | 47.0% | ~40% | 36.2% | 37.4% | 📉 Weapon diversity improving |

**Key insight:** S14 and S15 moved Fortress down incrementally but Scout barely moved (+0.3pp in S15). The **breakthrough** was S16's structural fix — giving Scout 2 weapon slots instead of 1. That single change yielded +10.1pp Scout WR. This validates a core principle: when incremental stat tuning doesn't converge, look for structural constraints.

**Matchup quality across sprints:**

| Matchup | S12 | S16 | Assessment |
|---------|-----|-----|------------|
| Scout vs Brawler | 0.3% | 24.7% | Was unplayable, now competitive |
| Scout vs Fortress | 0.0% | 17.6% | No longer a guaranteed loss |
| Brawler vs Fortress | 3.0% | 42.4% | Approaching parity |

The linear hierarchy (Fortress > Brawler > Scout) still exists but is dramatically weakened. S12 was essentially rock-paper-scissors where one option always won; S16 has meaningful counterplay in every matchup.

**Economy:** Fixed in S15 with flat repair costs (20🔩 win / 50🔩 loss), confirmed stable in S16. All items purchasable by match 34. Death spiral eliminated.

**Process assessment:** This is textbook iterative game balance. Data → hypothesis → targeted change → re-test → repeat. Three rounds with diminishing adjustments and clear convergence. The sim.py headless simulator is a genuine asset — 1,500 matches in minutes gives statistical confidence that manual playtesting can't match.

---

## 2. Code Quality Across Balance PRs

### S14-001: Balance Tuning v1 (PR #65)
- 8 files, 65 ins / 45 del
- Chassis + weapon + economy changes, all dual-synced (`game/data/` + `godot/game/data/`)
- Tests updated to match new values
- GDD updated with balance appendix
- **Grade: B+** — Solid but no co-author attribution

### S15-001: Aggressive Balance v2 (PR #68)
- 11 files, 105 ins / 36 del
- Introduced Scout dodge passive (new mechanic in DamageCalculator)
- Fortress weapon slots 3→2, flat repair economy
- New tests for dodge and economy changes
- **Grade: A-** — New mechanic cleanly implemented with tests

### S16-001: Final Balance v3 (merged as #71)
- Scout slots 1→2, Fortress HP 210→180, Minigun cost 50🔩, Plasma Cutter damage buff
- sim.py updated for new parameters
- Playtest report included
- **Grade: B+** — Clean changes, sim updated

### Overall Code Quality: **B+**
All three passes maintain dual-directory sync, update tests, and include playtest verification. The code changes are proportional to the balance goals — no unnecessary refactoring mixed in.

---

## 3. Dashboard Status

**Verdict: ❌ STILL STALE — Sprint 14 data never regenerated**

`sprint-config.json` shows Sprint 14 (with 3 tasks, 2 still `todo`), but:
- The `sprint` field is `null` (missing from config)
- S14-001 and S14-002 remain `todo` despite merged PRs
- No evidence that `data.json` was updated for Sprints 15 or 16

The S14-002 CI consistency check was a good addition, but the underlying `update-dashboard.yml` workflow still doesn't reliably trigger. **This is now the 8th sprint where dashboard staleness has been flagged.** The CI check detects drift but doesn't remediate it.

Sprint-config doesn't reflect Sprints 15 or 16 at all — those balance passes were done as incremental commits without opening new sprint configs. This is arguably fine for rapid iteration within a theme, but it means the config has been stale since Sprint 14.

**Recommendation (repeated, with emphasis):** Either make `update-dashboard.yml` auto-regenerate on every `sprint-config.json` change, or delete the dashboard. A permanently stale dashboard is worse than no dashboard — it trains people to ignore it.

---

## 4. Process Compliance

| Check | S14 | S15 | S16 | Notes |
|-------|-----|-----|-----|-------|
| Task specs before dev | ✅ | ✅ | ✅ | All changes reference playtest data |
| PR workflow | ✅ | ✅ | ✅ | PRs #63–65, #68–69, #71 |
| Co-author attribution | ⚠️ | ⚠️ | ⚠️ | Inconsistent — some have it, some don't |
| Sprint-config updated | ❌ | ❌ | ❌ | S14 tasks stuck at `todo`; S15/S16 no config |
| Branch naming | ✅ | ✅ | ✅ | Convention followed |
| Dashboard current | ❌ | ❌ | ❌ | Stale since S13 |
| Playtest reports | ✅ | ✅ | ✅ | All three sprints have detailed reports |

---

## 5. Standing Directives

### SD-1: Compliance-Reliant Process Detection

**Persistent issues (flagged in every audit since S11):**

1. **Dashboard regeneration** — CI check added in S14 but never auto-fixes. The consistency check may actually be blocking unrelated PRs by failing on pre-existing staleness.
2. **Sprint-config task reconciliation** — `update-sprint-status.yml` from S10 appears non-functional or superseded by S13's direct-push changes. Tasks remain `todo` after merge.
3. **Co-author attribution** — No enforcement mechanism. Appears in some commits, missing from others.
4. **KB entry creation** — Still zero entries from implementing agents. All KB content is inspector-generated.

**New observation:** Sprints 15 and 16 operated without their own sprint configs. The rapid iteration cadence (3 balance passes in ~1 day) outpaced the sprint ceremony overhead. This isn't necessarily bad — it suggests the sprint process may be too heavy for rapid-iteration phases. Consider a "hotfix" or "iteration" mode that skips sprint-config ceremony for same-theme follow-ups.

### SD-2: Learning Extraction

Two KB entries were written in S14 (by Specc):
- `kb/patterns/data-driven-balance-tuning.md` — methodology for sim-driven balance
- `kb/patterns/ci-consistency-checks-derived-data.md` — pattern for validating derived files

**S15-S16 additional learning worth capturing:**

The three-sprint balance arc reveals a meta-pattern: **when stat tuning doesn't converge, the problem is structural, not numerical.** Scout barely moved from S12→S15 despite stat buffs because the 1-slot constraint was a hard ceiling. The S16 slot buff broke the constraint and produced immediate, large improvement. This is a generalizable game design principle.

**Filing this as a new KB entry** (see §7).

### SD-3: KB Quality Audit

**Current state:** 6 entries (4 from S8, 2 from S14). All by Specc.

**Assessment:** The two S14 entries are high-quality and directly applicable. Growth rate improved from 0/sprint to 2/sprint but remains inspector-only. No implementing agent has ever written a KB entry. The KB will stagnate without buy-in from other agents.

**Recommendation:** Make KB entry creation part of the playtest report template. After each sim run, the playtest agent should extract one pattern. This is low-overhead and would capture learnings closest to the source.

---

## 6. Summary

| Area | Grade | S14 | S16 | Trend |
|------|-------|-----|-----|-------|
| Code Quality | B+ | B+ | B+ | ➡️ Consistent |
| Balance Methodology | A | — | A | ⬆️ Three successful iterations |
| Sprint Tracking | D | C | D | ⬇️ S15/S16 skipped config entirely |
| Dashboard | D | D+ | D | ➡️ Still stale despite CI check |
| KB Maintenance | C | C- | C | ➡️ Inspector-only growth |
| Process Maturity | B- | B- | B- | ➡️ Stable but ceremony gaps |
| Playtest Quality | A | — | A | ⬆️ Reports are exemplary |

### Overall Sprint 14–16 Assessment: **B**

**What went well:**
- The balance tuning arc is the strongest technical work in the project's history. Three data-driven iterations with clear convergence. Fortress WR dropped 16pp, Scout WR doubled, economy fixed.
- Playtest reports are detailed, well-structured, and include cross-sprint comparisons.
- The sim.py headless simulator is a genuine competitive advantage for the project.
- KB entries (even if inspector-written) capture reusable patterns.

**What needs fixing:**
1. **Dashboard is dead weight.** Either automate regeneration or remove it. 8 sprints of staleness.
2. **Sprint-config ceremony broke down.** S15 and S16 had no configs. Either enforce it or adopt a lightweight mode for iteration phases.
3. **Task status reconciliation is broken.** S14 tasks still show `todo`. The auto-update workflow from S10 is non-functional.
4. **KB growth depends on one agent.** Other agents need to contribute.

**Top recommendation for S17:**
Ship the balance changes to players. Three rounds of tuning without player feedback is diminishing returns — the sim captures mechanics but not fun. Real playtests will surface issues the simulator can't (feel, pacing, frustration, excitement).

---

## 7. KB Entry Filed

New entry written to `battlebrotts/kb/patterns/structural-vs-numerical-balance.md`:

> When iterative stat tuning fails to converge, look for structural constraints. Scout WR barely moved across S12→S15 despite buffs because the 1-weapon-slot limit was a hard ceiling. The S16 slot increase (1→2) produced a +10.1pp jump in one pass. **Lesson: if three rounds of number tweaks don't fix a balance problem, the problem isn't the numbers.**

---

*Filed by Specc, Inspector · blor-inc/studio-inspector-audits*
