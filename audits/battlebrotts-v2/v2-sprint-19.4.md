# BattleBrotts-v2 Sprint Audit — v2-sprint-19.4

**Date:** 2026-04-23T06:35Z
**Auditor:** Specc (`brott-studio-specc[bot]`, App ID `3444613`)
**Sub-sprint:** S19.4 — LangGraph Feasibility Spike (3.6)
**Arc:** Orphan-Recovery Durability Arc
**Scope:** Workspace-only design-spike audit (doc quality + decision-grade attestation)
**Grade:** **A−**
**Scope streak:** 16

---

## 1. Summary

S19.4 delivered a single workspace artifact — `memory/ops/3.6-langgraph-feasibility-spike.md` — a decision-grade feasibility synthesis on migrating the studio pipeline to LangGraph. Per the S19.4 spike plan §6 Q1 Option A scope call by Ett, this was **doc-only**: no studio-framework PR, no Optic verification, no build, no CI. Specc's audit correspondingly attests to **artifact presence + decision-grade quality only**.

The doc is structurally complete (all 9 required sections), analytically honest (explicitly corrects the arc-brief's 3–5wk preliminary to 6–10wk with reasoning), and gives HCD a clean go/no-go framing. It overshoots the 1500–2000 word target at 2,676 words, but remains readable inside ~12min and the structure is tight — the word count is the only meaningful deduction against an A.

All three escalation-relevant framings the spike plan required are present and surfaced prominently: 🔴 cost divergence, 🟡 architectural-commitment framing, and explicit fork-autonomy-clear confirmation.

## 2. Scope

**In-scope (per S19.4 plan §5 audit checklist):**
- Artifact presence at declared path
- Section completeness (9 sections)
- Decision-grade quality per section (TL;DR recommendation, concrete topology, validated cost range, named-problem mapping, concrete losses, ≥2 alternatives, explicit recommendation, HCD go/no-go readability)
- Carry-forward extraction attestation
- Escalation-flag surfacing

**Explicitly out of scope:** code correctness (no code), test coverage (no tests), CI compliance (no CI changes), build-green (no build), Optic simulation (no Optic artifact for doc-only spike), studio-framework PR review (no PR).

**Downstream audit target:** `memory/ops/3.6-langgraph-feasibility-spike.md` (workspace-only; not committed to any git repo).

## 3. Findings

### 3.1 Existence checks

| Check | Result | Evidence |
|---|---|---|
| Artifact exists at declared path | ✅ PASS | `memory/ops/3.6-langgraph-feasibility-spike.md` present |
| Word count in 1500–2000 target | ⚠️ OVER | 2,676 words (~34% over the upper bound) |
| Decision-readable in ≤15 min | ✅ PASS | Structure is tight (TL;DR + 9 clearly-scoped sections, tables for dense comparisons); 12-min stated read-time is realistic. Over-count is from thoroughness, not filler. |

**Verdict on the over-count:** the S19.4 plan flagged 1500–2000 as a *decision-grade brevity* target, not a hard cap. The doc stays decision-grade at 2,676 because the overflow is load-bearing (cost phase decomposition table, alternatives comparison table, cutover options table) rather than padding. Not grade-deducting on its own, but noted as a calibration signal: future spikes should land closer to the target unless overflow is similarly load-bearing.

### 3.2 Section completeness

All 9 required sections present and non-stub:

| § | Section | Substantive content? |
|---|---|---|
| 1 | TL;DR | ✅ Explicit recommendation + 5 bulleted headline reasons |
| 2 | What would change concretely | ✅ Concrete topology: services, infra additions, deploy story, pipeline semantics — not abstract |
| 3 | Migration cost estimate | ✅ 6-phase decomposition table, total range (6.5–10wk parallel), explicit arc-brief validation, risk surfaces, rollback story, cutover options matrix |
| 4 | What we'd gain | ✅ 7-row table mapping each gain to a *named* current problem (e.g., "S19.2 OOM driver," "S18.3 grandchild-propagation failure," "Specc commits running twice") |
| 5 | What we'd lose | ✅ 6 concrete losses (simplicity, single-language deploy, current harness capabilities, migration risk-window, sentinel-as-reminder, opportunity cost) + explicit "not lost" list |
| 6 | Alternatives | ✅ 3 alternatives covered (stay-current+harden, Temporal, roll-our-own) + summary comparison table |
| 7 | Recommendation | ✅ 3-part explicit recommendation: no-go on migration, go on H1–H4 hardening, park LangGraph as live option |
| 8 | Open questions for HCD | ✅ 4 numbered questions, each with explicit decision-vs-input scope tagging |
| 9 | Carry-forwards | ✅ 6 carry-forwards enumerated; §9 explicitly attests no GitHub Issues required now |

No stubs. Every section has ≥3 substantive sentences or equivalent tabular content.

### 3.3 Decision-grade quality (per spike-plan checklist)

| Check | Result | Notes |
|---|---|---|
| §1 TL;DR has explicit recommendation + headline reasons | ✅ | "NO-GO on full migration now. YES on the 1.5–2.5wk hardening baseline." + 5 reasons |
| §2 describes concrete topology (services/infra/deploy) | ✅ | Named services, Postgres sizing estimate, systemd deploy shape, pipeline-semantics delta enumerated |
| §3 gives cost range in weeks AND validates/refutes Bott's 3–5wk preliminary | ✅ | 6.5–10wk total (parallel-run), 5.5–7wk (rip-and-replace); §3.2 explicitly "undershoots by ~2×" with 3 enumerated sources of the gap |
| §4 gains each map to a *named* current problem | ✅ | Each row references a specific incident or driver (2026-04-22 OOM failure, S18.3 grandchild propagation, S19.2 runs.json growth, Specc double-commit, HCD-escalation token cost) |
| §5 losses are concrete (not "may have downsides") | ✅ | Each loss is named, scoped, and honestly framed; "not lost" list prevents straw-man |
| §6 covers ≥2 alternatives with same gain/lose framing | ✅ | 3 alternatives (hardening, Temporal-hybrid, roll-our-own) each with cost, gains, losses, verdict; §6.4 summary table |
| §7 recommendation is explicit (not hedge-only) | ✅ | 3-part numbered recommendation; one explicit hedge ("HCD decides" on platform-investment framing) is appropriate scope escalation, not hedging on the pipeline-level call |
| HCD can make go/no-go from this doc alone | ✅ | No LangGraph code reading required; T1+T2 research archives are referenced but not load-bearing for the decision |

### 3.4 Carry-forward extraction

§9 identifies 6 carry-forwards:

1. Reconciler post-S19.3.1 incident-rate data pull (The Bott action)
2. H1–H4 hardening proposal sketch (follow-on arc brief, not this spike's close)
3. Idempotency-key contract on Nutts/Boltz (H1/H2 — no-regret even under migration)
4. LangGraph research archive (T1+T2 docs stay in place for ~12mo re-open)
5. `sync` durability performance benchmark (deferred, migration-conditional)
6. LangGraph.js feature-lag inventory (deferred, migration-conditional)

§9 explicitly attests **no new GitHub Issues required** for this spike's close. H1–H4 would be filed at hardening-arc kickoff, not here. **Attestation: correct.** This is a workspace-only design output; the carry-forwards are either decision-gated on HCD's go/no-go (items 2, 5, 6) or natural follow-on actions by named owners (1, 3, 4). No artifact-gap forces an Issue now.

### 3.5 Escalation-flag attestations

| Flag | Required by S19.4 plan | Surfaced in doc? | Specc attestation |
|---|---|---|---|
| 🔴 Cost divergence (6–10wk vs 3–5wk preliminary) | Yes — must be prominent | ✅ §1 TL;DR first bullet ("6–10 weeks, not 3–5"); §3.2 explicit "undershoots by ~2×" with 3-source diagnosis; §3.2 carries 🔴 flag text itself; Q4 in §8 raises whether HCD wants the spike re-framed around the corrected number | **Prominently surfaced.** TL;DR placement + §3.2 explicit flagging + §8 Q4 re-framing question means no reader can miss it. |
| 🟡 Architectural-commitment framing | Yes — should be naturally expressed | ✅ §1 final bullet ("platform-investment decision, not a durability-fix decision"); §7 rationale explicitly reframes ("LangGraph wins if we re-scope the question from 'fix durability' to 'invest in a platform for future scale'"); §8 Q1 asks HCD to pick the framing | **Naturally expressed.** The framing duality is the doc's central analytic move and is surfaced without flag-ceremony, which is the right register for a 🟡. |
| Fork-autonomy: NOT at risk | Yes — must confirm no-go on fork-autonomy escalation | ✅ §1 bullet 4 ("Fork-autonomy: not at risk"); §2.1 ("LangGraph OSS library + self-hosted Postgres is fully viable; no LangChain commercial dependency required"); §5 "Not lost" list ("fork autonomy (OSS library is self-contained; no hosted dependency required)") | **Confirmed no-go on escalation.** Three independent mentions, each with the OSS-library-self-contained reasoning. Fork-autonomy is not a live risk and does not warrant a separate escalation. |

### 3.6 Minor findings (non-grade-affecting)

- **F1 — Word count overrun (2,676 vs 1,500–2,000 target).** Structurally load-bearing, not filler. Noted as a calibration datum for future spike-brief sizing.
- **F2 — §3.1 total-range arithmetic.** The phase decomposition sums to 6.5–10 weeks; the doc states "6–10" in the TL;DR and "6.5–10" in §3.1. Minor rounding. Does not affect the 🔴 cost-divergence framing (both numbers refute 3–5wk by ~2×). No action required.
- **F3 — §3.5 feature-flag-per-arc cutover option** is listed but carries an implicit "probably not what HCD wants" steer. Framing is fine for a decision doc; noting for completeness that the option is present but down-weighted.
- **F4 — §7 scope-escalation is cleanly drawn.** "HCD decides. This is a creative-direction-adjacent call" is exactly the right Ett-scope boundary per the Bott/Ett authority framework. Good pipeline discipline.

## 4. Carry-forwards (audit-level, beyond doc's §9)

The following are pipeline- and process-level carry-forwards surfaced by this audit (not superseding or replacing the doc's §9 content):

1. **Word-count calibration for future spike briefs.** The S19.4 plan's 1500–2000 target is a useful brevity anchor, but load-bearing tables (cost phase decomposition, alternatives comparison) will push a genuinely decision-grade doc past it. Recommend future spike plans either (a) lift the target to ~2500 for 3+ alternative comparisons, or (b) explicitly allow tabular overflow. No Issue required; this is a planning-calibration note.
2. **Arc-brief cost estimate methodology.** §3.2's 2× undershoot diagnosis (thin-adapter assumption + unbudgeted tooling-rewrite + unbudgeted cutover overhead) is generalizable. Future arc briefs estimating multi-week migrations should explicitly budget tooling-rewrite and cutover as named phases rather than roll-ups. No Issue required; captured here for the framework docs cycle.
3. **No GitHub Issues required by this audit.** Confirms §9's attestation. The H1–H4 hardening items will be issued at hardening-arc kickoff if HCD green-lights that path; they are not yet committed work.

**No new GitHub Issues required.** Consistent with the doc's §9 position and the S19.4 plan's doc-only scope.

## 5. Grade with rationale

**Grade: A−**

**Why not A:**
- Word count overrun is real (34% over upper bound). The doc is decision-grade regardless, but a clean A would have either hit the target or negotiated an explicit extension in the plan.

**Why not B+:**
- All 9 sections are substantive and structurally complete.
- Every checklist item on the S19.4 plan §5 audit checklist passes.
- All three escalation-relevant framings (🔴, 🟡, fork-autonomy-clear) are surfaced prominently and correctly.
- HCD can make a go/no-go call from this doc alone, which is the load-bearing criterion for decision-grade.
- The analytic honesty of §3.2 (explicitly correcting the arc-brief's own preliminary) is exactly the behavior the spike was commissioned to produce.

**Calibration note:** The S19.4 plan itself signaled that word count should be graded on read-time not raw count — on that criterion, the doc reads in ~12min as stated, which is within the 15min decision-grade window. If the spike plan's word target is treated as advisory-only, this is a full A. Specc's A− reflects that the overage was real but the outcome is strong.

## 6. Pipeline discipline notes

- **Scope streak:** 16 sub-sprints clean (carries S19.3.1's 15 forward).
- **Out-of-scope probes:** none — this was a workspace-doc audit with no CI, no build, no PR, so no scope creep was possible beyond the doc itself.
- **Sentinel hold:** first tool call on Specc entry was a harmless sentinel-latch (`echo specc-s19.4-t4-entry-sentinel...`); held.
- **Verify-before-write idempotency (S19.1 contract):** GET on `audits/battlebrotts-v2/v2-sprint-19.4.md?ref=main` returned HTTP 404 before commit. Safe to create; no duplicate-commit risk. Contract satisfied.
- **Commit mechanics:** audit written via GitHub Contents API using Specc App installation token (via `~/bin/specc-gh-token`). No `write` tool used for commit content.

## 7. Closing

S19.4 achieved its scope cleanly: a doc-only design spike that gives HCD a decision-grade go/no-go on a platform-investment question. The 6–10wk vs 3–5wk cost correction is the most consequential finding in the doc, and its prominent surfacing is the single biggest quality signal. The sub-sprint exits with no blocking carry-forwards and one follow-on decision gate (HCD's Q1/Q4 responses in §8) rather than a pipeline action.

Arc-close readiness: the Orphan-Recovery Durability Arc sits 4-of-5 sub-sprints complete (S19.1 A−, S19.2 and S19.3 folded, S19.3.1 A, S19.4 A−). Per §7 of the doc, Ett recommends a small H1–H4 hardening arc as a separate follow-on rather than a rolled-in S19.5, which keeps this arc's close-out crisp. HCD-level call.

## 10. Carry-forward → GitHub Issues

No new Issues required by this audit. Consistent with §4 of this audit and §9 of the doc itself. Any Issues arising from HCD's §8 go/no-go responses would be filed at the decision event, not at this audit's commit.

---

**End of audit.** Scope streak: 16. Arc: Orphan-Recovery Durability (4 of 5 sub-sprints complete).
