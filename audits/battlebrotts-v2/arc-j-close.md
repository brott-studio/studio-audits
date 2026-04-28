# Arc J Close Audit — "T1 Balance & Scrapyard Variety"

**Arc:** J — T1 Balance & Scrapyard Variety
**Started:** 2026-04-28
**Status:** ⚠️ HALTED — R1 escalation active
**Reason:** 0% chassis win-rate across all 3 T1 chassis (target: 30–70%); ~6s median battle duration (target: 20–60s)
**Auditor:** Specc

---

## Sub-sprint summary

| Sub-sprint | Sprint # | PR | Grade | Description |
|---|---|---|---|---|
| J.1 | sprint-28.1 | #333 | A- | T1 HP buff (80→120) — chassis survivability fix |
| J.2 | sprint-28.2 | #334 | A | Scrapyard template variety (4 templates, 4 archetypes) |
| J.3 | sprint-28.3 | #335 | A | Scrapyard variety test + Bronze regression guard |
| J.4 | sprint-28.4 | — | A- | Optic holistic validation (R1 trigger) |
| CF-J1-001 | — | #336 | — | sim_aggregate.py parse fix (merged this session) |

---

## Success criterion status (arc brief §5)

| # | Criterion | Status | Notes |
|---|---|---|---|
| 1 | Issue #314 closed (T1 win-rate ≥15% per chassis) | ⚠️ BLOCKED | Code landed (HP 80→120) but sim shows 0% win-rate / 6s median battles — empirical verification PENDING. #314 NOT closed. |
| 2 | Issue #295 closed (Scrapyard variety) | ✅ READY | 4 templates, 4 archetypes, variety test 100%, no Bronze regression. #295 can be closed. |
| 3 | E2E smoke green | ✅ PASS | `bb-test-run-e2e.spec.js` passes in CI (PARTIAL_COVERAGE headless), wired into arc-close gate. |
| 4 | J.4 holistic pass | ⚠️ PARTIAL | AutoDriver (Gate 2) + Vision (Gate 4) + E2E (Gate 3) all pass; R1 fired on Gate 1 sim win-rate. |

---

## J.4 Optic gate results

| Gate | Name | Result | Detail |
|---|---|---|---|
| Gate 1 | T1 sim histogram | ⚠️ R1 ESCALATION | 14/20 parsed (6 errored); 0% run win-rate and 0% battle win-rate all 3 chassis; ~6s median battle duration |
| Gate 2 | AutoDriver suite | ✅ PASS | All 4 flows green |
| Gate 3 | E2E spec | ✅ PASS | 1/3 post-J.3 runs evaluated, PARTIAL_COVERAGE as designed |
| Gate 4 | Vision screenshots | ✅ PASS | 29 screenshots, arena canvas confirmed |

---

## R1 escalation details

### Sim data
- **Chassis tested:** 3 T1 chassis
- **Runs parsed:** 14/20 (6 still errored post CF-J1-001 fix)
- **Run win-rate:** 0% across all 3 chassis
- **Battle win-rate:** 0% across all 3 chassis
- **Median battle duration:** ~6s (target: 20–60s)
- **R1 trigger condition (arc brief §4):** Any chassis <15% win-rate → halt arc-close, escalate to The Bott

### Hypothesis: Sim infra vs. real balance
The 0% win-rate and 6s battle duration are anomalous given that J.1's HP buff (80→120) was the intended fix. Two competing hypotheses:

1. **Sim infrastructure artifact:** The combat sim agent (`sim_single_run.gd`) may be running battles under conditions that don't reflect live gameplay (e.g., enemy scaling, AI configuration, or arena state not seeded correctly post-J.1). The 6-parse errors on 20 runs, even after CF-J1-001, suggest the sim harness itself may still have reliability issues that corrupt result data.

2. **Real balance signal:** The HP buff alone was insufficient. Enemy DPS may be too high relative to the buffed HP, resulting in T1 chassis still dying too fast to accumulate wins. The ~6s duration (vs. 20–60s target) is consistent with instant defeats rather than competitive battles.

The CF-J1-001 fix addressed a parse-side regression; the underlying battle outcome data requires HCD review before a conclusion can be drawn.

---

## Open questions for HCD / The Bott

1. **Sim artifact or real signal?** Is the 0% win-rate a genuine gameplay signal indicating T1 chassis are still unviable, or is the sim harness running battles under misconfigured conditions that don't reflect real gameplay?

2. **Extend J.1's fix?** Should the fix be broadened beyond HP (80→120) to also reduce enemy DPS for T1 encounters — addressing survivability from both sides of the damage equation?

3. **Is 6s acceptable?** HCD previously noted that short T1 battles felt "exciting." Is the ~6s median battle duration acceptable as a design choice for T1, making the 0% win-rate the only concern? Or does a 6s battle definitively indicate a sim/config bug rather than intended gameplay?

---

## Carry-forwards into next arc

From arc brief §6 + new items surfaced during Arc J:

| ID | Item | Source | Priority |
|---|---|---|---|
| CF-J1-001 | sim_aggregate.py parse errors (6/20 still failing post-fix) | Gate 1 regression | HIGH |
| CF-J1-002 | T1 balance empirical verification — re-run sim after HCD direction on tuning approach | R1 escalation | HIGH (blocking #314) |
| CF-J1-003 | Enemy DPS tuning for T1 tier (pending HCD decision on scope of fix) | Open question 2 | MEDIUM |
| CF-J2-001 | Scrapyard template pool expansion beyond 4 (variety headroom) | Arc brief §6 | LOW |
| CF-I8-001 | AutoDriver flake tuning (S(I).8 optional — trigger if flake rate >5%) | Arc I carry-forward | LOW |

---

## What's needed to re-open arc-close

1. **HCD / The Bott weigh in** on the three open questions above (artifact vs. signal; scope of fix; duration acceptability).
2. **Optic re-runs Gate 1 sim** after HCD direction on tuning approach is applied (whether DPS reduction, sim config fix, or acceptance of current duration).
3. **Win-rate per chassis lands in 30–70% range** across ≥5 valid parsed runs — confirms J.1's fix is empirically complete.
4. **Parse error rate drops to 0/20** (all runs successfully parsed) — confirms CF-J1-001 fix is fully effective.
5. Once steps 3 + 4 are satisfied, **Specc declares arc-close** and closes issue #314.

---

*Audit written by Specc. Arc-close HALTED pending R1 resolution. Issue #295 may be closed independently.*
