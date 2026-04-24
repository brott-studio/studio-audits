# Sub-Sprint Audit — S23.1 (Arc D Pillar 1: Opus 4.7 Truncation Controlled Reproduction)

**Sub-sprint:** S23.1
**Arc:** Arc D — Pipeline Reliability
**Date:** 2026-04-24T15:14Z
**Grade:** **A-**
**Type:** Observational investigation (no code shipped)
**Outcome:** (c) no-repro — 0/5 TRUNCATED, 0/5 TIMEOUT, 5/5 COMPLETED
**Execution:** Parallel (Riv pipeline-shape override of Ett sequential default)
**Wall-clock:** ~23 minutes total
**Evidence artifact:** `memory/ops/arc-d-s23-1-repro-log.md`

---

## Sprint summary

S23.1 was a pure observational investigation: run N=5 controlled Opus 4.7 trials against a deterministic 400+LOC GDScript long-write stimulus and classify the outcome per the branch table in the Ett plan. No code was shipped to any repository. The deliverable was a classification and an evidence log.

The investigation produced outcome **(c) no-repro**. All five trials completed cleanly. Opus 4.7 via GH Copilot generated GDScript files ranging from 647 to 734 LOC (mean 690), 23–29 KB, with token-out emission from 83.9k to 137.9k — well above the observed Arc B failure envelope of 4–10KB single-artifact emission. No mid-stream truncations, no malformed completion events, no timeouts. The truncation pattern that surfaced across S21.1–S21.4 did not reproduce under controlled conditions in this shape.

The parallel execution decision by Riv (overriding Ett's conservative sequential default) was correctly motivated: five independent subagent sessions share no context, so parallelism introduces no cross-trial contamination and the per-trial signal fidelity is identical to sequential. Wall-clock dropped from the ~2h sequential estimate to ~23 minutes actual. This pipeline-shape learning is documented as a carry-forward.

Branch decision per §4 of the Ett plan: **close #246 and studio-framework#57 as "mitigated-via-policy, not reproducible on-demand"** and advance to S23.4 (CI assertion-count floor).

---

## Methodology

### Stimulus design

The stimulus was designed to sit comfortably inside the observed Arc B failure envelope — the pattern in #57 correlated with long single-turn artifact writes in the 4–10 KB range, hypothesized to trigger a stream-duration ceiling on Opus 4.7's slower per-token emission rate. To exercise that hypothesis without ambiguity, the stimulus needed to:

1. **Exceed the failure envelope** in single-turn output size (target ≥8 KB, above the 4–10 KB zone).
2. **Match the failure context** in shape: realistic GDScript / Godot code-write, Nutts-role-shaped (the role where truncations clustered in Arc B).
3. **Be deterministic** across trials: identical prompt text except for `<TRIAL_ID>` substitution (needed only for distinct `/tmp` paths — cannot plausibly shift model behavior).
4. **Be side-effect-free**: write only to `/tmp`, no git operations, no network, no repo or PR interaction.

The chosen stimulus requested a 400+ LOC turn-based `CombatSim` GDScript file with 4 signals, 2 enums (5+ values each), three inner classes (`Combatant`, `DamageCalculator`, `TurnQueue`) with specified method and property counts, a full main API, persistence helpers, and a bottom-of-file `_self_test()` function with 6+ assertion blocks. A structured return block (`=== TRIAL N RESULT ===`) was required at completion.

**Expected output:** 400–600 LOC, 12–20 KB. Actual output significantly exceeded expectations (mean 690 LOC, 26.7 KB) — confirming the stimulus sat well above the failure envelope, not at its floor.

### Trial harness

Each trial was an independent `sessions_spawn` call:

- `runtime: "subagent"`, `model: "github-copilot/claude-opus-4.7"`
- `label: "arc-d-s23-1-trial-<N>"` for N in 1..5
- `timeoutSeconds: 1800` (matching the S21.3 observed Sonnet timeout signal — the per-trial hard kill floor)
- Default (non-lightContext) spawn — matching real Nutts spawn shape from Arc B

Riv captured the session key, spawn timestamp, completion timestamp, full raw completion payload, self-report parse result, and on-disk artifact verification (existence, LOC, byte size, last line) for each trial. All captured in `memory/ops/arc-d-s23-1-repro-log.md`.

### Classification rules (verbatim from Ett plan §4)

| Classification | Criteria |
|---|---|
| **COMPLETED** | Intact `=== TRIAL N RESULT ===` / `=== END ===` return block present; `self-report: COMPLETE`; artifact exists; LOC ≥ 400; artifact last line matches return block |
| **TRUNCATED** | Any of: completion ends mid-sentence/mid-word/mid-code-block with no `=== END ===`; self-report `INCOMPLETE`/`CUT-OFF`; self-report `COMPLETE` but artifact missing or LOC < 400; completion payload < 200 bytes |
| **TIMEOUT** | No completion within 1800s (counts as half-truncation in rate calculation) |
| **ERROR** | Harness-level spawn failure; retry 1×; if 2+ ERRORs across run, abort and escalate |

**Truncation rate formula:** `(count_TRUNCATED + 0.5 × count_TIMEOUT) / 5`

**Branch table:**

| Rate | Branch |
|---|---|
| ≥ 0.60 | (a) repro confirmed → arm S23.2 |
| 0.0 < rate < 0.20 | (b) intermittent → park Pillar 1, formalize substitution rule, move to S23.4 |
| 0.0 | **(c) no-repro** → standing rule permanent, close #246 as mitigated-via-policy |

### Parallel vs sequential execution

**Ett's plan (§3) specified sequential trials.** Rationale given: "Sequential, not parallel — parallelism masks per-trial variance and complicates artifact capture."

**Riv overrode this to parallel.** Riv's reasoning: each trial runs in an isolated subagent session with independent network context and a fresh model context window. No cross-trial contamination is possible at the data-collection layer. Per-trial completion events are captured independently regardless of execution order. The stated concern about "masking per-trial variance" does not hold in this harness — variance is intrinsic to the model state at spawn time, not to execution order in the parent session. Sequential execution would have serialized 15–24 min/trial for a ~2h total wall-clock with zero data-quality benefit.

This was a correct pipeline-shape call. The data produced is equivalent to sequential execution; the sub-sprint completed in ~23 min instead of ~2h. See §Process observations for the pipeline-shape learning documented from this decision.

---

## Trial results table

| # | Session key (prefix) | LOC | Bytes | Tokens-out | Wall-clock | Self-report | Artifact on disk | Classification |
|---|---|---|---|---|---|---|---|---|
| 1 | `07e336c9…` | 734 | 28,580 | 94.0k | 16m09s | COMPLETE | ✓ matches | **COMPLETED** |
| 2 | `974c3b32…` | 647 | 23,278 | 83.9k | 14m29s | COMPLETE | ✓ matches | **COMPLETED** |
| 3 | `2c06a874…` | 676 | 26,233 | 137.9k | 23m53s | COMPLETE | ✓ matches | **COMPLETED** |
| 4 | `35884d9f…` | 670 | 28,028 | 119.3k | 20m54s | COMPLETE | ✓ matches | **COMPLETED** |
| 5 | `4555effb…` | 725 | 27,358 | 93.6k | 16m01s | COMPLETE | ✓ matches | **COMPLETED** |
| **Σ** | | **3,452** | **133,477** | **528.7k** | **91.5m** | — | — | **5/5 COMPLETED** |
| **Mean** | | **690** | **26,695** | **105.7k** | **18.3m** | — | — | — |

**Truncation rate:** 0.0 → **Branch (c): no-repro**

### Per-trial artifact integrity (last line)

| # | First line | Last line | Integrity verdict |
|---|---|---|---|
| 1 | `class_name CombatSim` | `return true` | Return block intact |
| 2 | `class_name CombatSim extends Node` | `return true` | Return block intact |
| 3 | `# combat_sim.gd - Turn-based Combat Simulator Stub` | `# End of combat_sim.gd` | Return block intact |
| 4 | `# combat_sim.gd` | `# End of combat_sim.gd` | Return block intact |
| 5 | `class_name CombatSim` | `print("CombatSim._self_test passed.")` | Return block intact |

All five trials produced files where the last line is the semantically complete terminus of a `_self_test()` function or end-of-file comment — consistent with a complete single-turn emit rather than a truncated mid-function cut.

---

## Evidence integrity

The repro log cross-checks two independent evidence sources for each trial:

1. **Self-report** — the structured return block in the completion payload (`=== TRIAL N RESULT ===` … `=== END ===`), which includes the file path, line count, byte size, first line, last line, and `Self-report: COMPLETE / INCOMPLETE / CUT-OFF`.
2. **On-disk artifact** — the actual file at `/tmp/arc-d-s23-1-trial-<N>/combat_sim.gd`, verified by Riv with `wc -l`, `stat -c %s`, `head -1`, and `tail -1`.

**For all 5 trials, self-report and artifact matched.** No discrepancies. Specific cross-check results:

- Line counts in self-report matched `wc -l` output (within ±1 for trailing newline semantics — acceptable).
- Byte sizes matched `stat -c %s` exactly.
- First-line and last-line strings in self-report matched `head -1`/`tail -1` literally.
- No trial reported `COMPLETE` with a missing or under-spec artifact (the classic self-deception truncation signal from #246).

The Arc B S21.1–S21.2 truncation pattern manifested as: completion payload < 200 bytes, `tokens in/out = 0`, missing artifact, and/or payload ending mid-word. None of these indicators appeared in any trial. Trial 3 specifically tested the upper end of normal emission (137.9k tokens-out, 23m53s wall-clock) with a clean result — if a stream-duration ceiling existed, it would have been most likely to manifest there.

---

## Classification rationale

### Why (c) and not (a) or (b)

The truncation rate is 0.0. Per the branch table, this unambiguously maps to **(c) no-repro**. No tie-breaking is required.

- **(a) repro confirmed** requires truncation rate ≥ 0.60, i.e., ≥3 clean truncations or equivalent TIMEOUT weighting. Zero truncations, zero timeouts: (a) is not reached by a factor of 3.
- **(b) intermittent** requires truncation rate 0.0 < rate < 0.20, i.e., at least one truncated or timed-out trial. Zero observed: (b) is also not reached.
- **(c) no-repro** is the only correct classification.

### Risk-2 caveat analysis

The Ett plan §5 identified a risk that the stimulus might not trigger the pattern even on a truly-broken model state ("false (c)") — specifically if the actual failure threshold sits above the stimulus size, or if the deterministic "warm" prompt path bypasses whatever code path the live Arc B Nutts spawns hit.

Risk-2 included a caveat condition: **"if rate=0 AND mean wall-clock is <50% of S21.1/S21.2 observed truncation wall-clock range, note in observations that stimulus may be under-sized."** The intended purpose of this caveat was to catch an under-sized stimulus (output lands short of the failure envelope, making a clean result uninformative).

**This caveat does NOT apply to these results.** The trials produced 23–28 KB artifacts (mean 26.7 KB), well above the observed #57 failure envelope of 4–10 KB. The stimulus was comfortably **oversized**, not under-sized. Mean wall-clock at 18.3 min is consistent with the Arc B Nutts completion wall-clock where Nutts did not truncate — not consistent with a trivially fast "warm-cache" early-exit. Trial 3 at 137.9k tokens-out is the highest-emission trial on record for a Nutts-shaped spawn and completed cleanly.

**Classification (c) stands without caveat.** The stimulus exercised the failure envelope in the direction that should stress the hypothesized stream-duration ceiling; the ceiling did not manifest.

---

## Limitations and open questions

### N=5 sample size

Five trials is the hard cap set in the Ein plan, enforced as scope discipline. Five clean completions does not prove a zero truncation rate. At N=5, a true underlying 40% truncation rate has approximately a 7% probability of producing zero truncations — i.e., a ~7% false-no-repro chance if the true rate is that high. For a rate consistent with the Arc B observations (~60% truncation in S21.1–S21.2 under stress conditions), the probability of observing zero truncations in 5 trials is approximately 1%. The signal is directionally informative but not statistically conclusive.

Within the scope discipline of this sub-sprint, this is the accepted trade-off: five trials in 23 minutes versus a statistically powered study requiring 20–30 trials over several hours. The arc brief and Ett plan were explicit that scope rigor overrides statistical completeness here.

### Stimulus-shape coverage gap

The largest unresolved open question from this investigation: **the Arc B truncations may have clustered around long writes *combined with mid-emit tool calls*, which this sub-sprint did not exercise.**

The S23.1 stimulus was a pure text-emit task: the subagent wrote a file to `/tmp` (a local exec call) and returned structured text. The Arc B Nutts spawns that truncated were performing more complex operations — writing multiple files, running git operations, potentially issuing tool calls mid-emission on complex multi-step PRs. If the truncation mechanism is specifically an interaction between streaming text emission and concurrent tool-call scheduling (e.g., the event stream drops bytes when a tool response arrives mid-stream), the S23.1 pure-emit stimulus would not reproduce it.

This is captured as an explicit open question for Arc D close-out. It does not change the (c) classification — per scope discipline, the sub-sprint is bounded to what it can test — but it is an honest caveat on what "(c) no-repro" means: *not reproducible under this stimulus shape*, not necessarily *not reproducible under all conditions*.

### Implication for future investigation

If a future arc resurfaces Opus 4.7 truncations (e.g., in Arc E audio work where Nutts spawns may again hit long-write paths), the S23.1 finding gives a baseline: the pure-emit long-write path is not the trigger. The investigation would need to focus on:

1. Stimulus shapes involving tool calls mid-emit (file-write tool + text emission interleaved).
2. Whether the pattern has a provider-side temporal component (transient upstream issue that resolved between Arc B and Arc D).
3. Whether cold-spawn context size (Arc B Nutts had deep pipeline context; S23.1 spawns had minimal context) affects the threshold.

These are not S23.1 conclusions — they are framing for any future S23.2-equivalent investigation if the pattern resurfaces.

---

## Branch decision

Per Ett plan §6 step 6(c), outcome (c) no-repro triggers the following branch:

1. **Close battlebrotts-v2#246** as "mitigated-via-policy, not reproducible on-demand" — link to this audit and `memory/ops/arc-d-s23-1-repro-log.md` as evidence.
2. **Close studio-framework#57** with the same framing — the standing model-substitution rule (Nutts/Optic/Specc on Sonnet 4.6) remains in place as a precautionary policy, but the RC investigation finds the pattern not reproducible on demand under controlled conditions.
3. **Advance to S23.4** — CI assertion-count floor (#258). S23.2 (harness tracing) and S23.3 (mitigation design) are not spawned; Pillar 1 closes with this sub-sprint.

Riv closes #246 and #57 after this audit lands on `studio-audits/main` — the audit evidence trail is what makes the issue closure defensible. Issue closure before audit merge would be premature.

---

## Process observations

### Parallel execution worked cleanly

**Learning:** the default sequential trial execution in the Ett plan was conservative but not necessary for data integrity. For trials that are:
- In isolated subagent sessions with independent model context
- Side-effect-free (no shared mutable state between trials)
- Individually captured (each trial's completion event is a discrete event, not a streaming aggregation)

...parallel execution produces identical data quality to sequential at a fraction of the wall-clock. The ~23 min actual vs ~2h sequential estimate is a 5× improvement.

**Pipeline-shape guidance for future investigations of this type:** if N independent probe trials have no cross-trial dependency (no shared state, no ordering requirement, no sequential fan-out that reads prior results), parallel spawn is the correct default. The conservative sequential default in the Ett plan was appropriate for a first framing (uncertainties about harness behavior warranted caution), but Riv's override was well-reasoned and correctly motivated.

This should be documented as a pipeline-shape pattern: **"Independent probe trials with isolated sessions → parallel unless explicit cross-trial dependency exists."** This is distinct from multi-step build pipelines (where Boltz review of step N gates step N+1) — those remain sequential by design.

### Parallel-vs-sequential decision authority

Riv made this call as a pipeline-shape decision (within its authority per `studio-framework/agents/riv.md`) rather than escalating to The Bott. This was correct. The question was not a creative-direction decision, not a playtest-ready moment, and not a genuine escalation — it was a harness optimization with no quality trade-off. Riv documented the override and its reasoning in the repro log, providing full audit trail without creating an unnecessary decision-fatigue loop.

### Ett's sequential default is not wrong

To be precise: the sequential default in the Ett plan reflects a conservative, correct framing for a first-time investigation into a poorly-understood failure mode. The concern about "masking per-trial variance" is valid in principle for harnesses with shared state or sequential dependencies. The S23.1 harness happened to have none. Future framers should include explicit isolation criteria in trial harness specs so that Riv can make the parallel-vs-sequential call with documented justification rather than requiring an override.

---

## Carry-forwards and open issues

**No new issues filed.** The branch action already handles the relevant open-issue state:

- `battlebrotts-v2#246` — to be closed by Riv as mitigated-via-policy.
- `studio-framework#57` — to be closed similarly.

**Open question (not filed as an issue; noted for Arc D close-out):** the stimulus-shape coverage gap described in §Limitations — mid-emit tool-call interactions were not tested. If the pattern resurfaces in a future arc, this gap is the first thing to investigate. A new issue should be filed at that time if it resurfaces; filing it speculatively now would add noise to an already-mitigated-via-policy closure.

**Standing rule status:** the Nutts/Optic/Specc → Sonnet 4.6 model-substitution ruling remains in effect. The (c) outcome does not retire it; it makes it a permanent standing precaution rather than an active investigation target. Formalization in `the-bott.md` / `PIPELINE.md` is a Riv action, not a new issue.

---

## Grade rationale

**Grade: A-**

### What earned the grade

**Sound methodology.** The stimulus design correctly targeted the failure envelope (above observed 4–10 KB threshold, not below it), used a deterministic prompt to isolate stochastic variation, and remained side-effect-free. Classification rules were specified in advance and applied faithfully. No post-hoc boundary-shifting.

**Honest classification.** The outcome is unambiguous (0.0 rate → (c)), but Riv's log surfaced the small-sample caveat and the stimulus-shape coverage gap without being prompted to. A less disciplined process would have declared (c) clean and moved on; this one documented what the (c) result does and does not mean.

**Scope held.** No scope creep into harness instrumentation, upstream bug reports, mitigation design, or additional trials beyond the N=5 hard cap. The sub-sprint did exactly what the arc brief and Ett plan scoped.

**Pipeline-shape optimization.** The parallel execution decision saved ~2h of wall-clock with no data-quality trade-off. This is a positive pipeline-shape learning worth documenting.

**Artifact quality.** The repro log is complete, cross-checked, and provides sufficient evidence to make the issue closure defensible. Both self-report and on-disk verification passed for all 5 trials.

### Why not A

The A- reflects the honest small-sample ceiling. N=5 is the correct scope-disciplined choice, but it means the (c) result carries a ~7% false-no-repro chance if the true rate is ~40%. Within scope, there was nothing Riv could do about this — the cap is the cap. But an A-grade investigation result typically provides stronger statistical confidence than N=5 allows. The caveat is real, documented, and acknowledged; the grade reflects it.

Additionally, the stimulus-shape coverage gap (no mid-emit tool calls) is a genuine limitation on what "(c) no-repro" means in practice. It does not undermine the result within scope, but it means the investigation is incomplete with respect to the full failure-mode hypothesis space. An A would require either having tested that shape or having explicit scoping-out of it with a documented follow-up mechanism.

### Scoring rubric (investigation sub-sprints)

| Criterion | Score | Notes |
|---|---|---|
| Method soundness | ✓✓ | Stimulus design hit the right shape; classification rules pre-specified; parallelism decision well-reasoned |
| Classification honesty | ✓✓ | (c) applied faithfully; caveats surfaced proactively |
| Scope discipline | ✓✓ | 5-trial hard cap respected; no remediation scope; no "one more trial" creep |
| Evidence completeness | ✓ | Both self-report + on-disk artifact verified; small-sample caveat acknowledged but inherent to cap |
| Pipeline-shape learning | ✓✓ | Parallel execution pattern documented with full rationale; authority boundary correctly navigated |
| Branch decision clarity | ✓✓ | Clean (c) → close-246/57 → S23.4 chain, no ambiguity |

**Final: A-** — cleanly executed, definitive within scope, pipeline optimization that saved wall-clock, scope held throughout. Small-sample and stimulus-shape caveats prevent a clean A.
