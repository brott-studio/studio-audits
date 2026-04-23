# Sub-Sprint Audit — S20.2 (H3 Riv-state durability)

**Sub-sprint:** S20.2
**Arc:** S20 Hardening Arc
**Date:** 2026-04-23T13:35Z
**Grade:** **A**
**Scope streak:** 17 → **18**
**PR:** [brott-studio/studio-framework#49](https://github.com/brott-studio/studio-framework/pull/49)
**Merge commit:** `ea10e5d7d2e7d56d70b279d38eb0297d1b567698` on `studio-framework/main`
**Idempotency key (self-dogfood):** `sprint-20.2`

---

## Scope summary

H3 delivered as planned per arc brief §3 + Ett's T1–T6 plan: a per-sub-sprint durable **task-ledger** owned by Riv, a formal **ledger protocol** inside `agents/riv.md`, a **resume-declined handler** for orphan-Riv, and a taxonomy-first **`sprintShape` fold-in** to the active-arc reconciler.

The underlying problem: respawn-Riv after OOM / gateway restart / run-mode end had no durable record of what it had already done. State lived in transient subagent transcripts. S18.3's 9-hour silent outage is the canonical receipt — Riv's grandchild (Specc-audit) never propagated a completion event and Riv couldn't tell what had / hadn't landed. H3 closes that gap by making **state live in files** (FRAMEWORK.md Core Principle #4) for the orchestration layer, not just for role-profile-level artifacts.

**Structural goal:** convert a compliance-reliant "Riv remembers what it spawned" into a deterministic "Riv reads a JSON file on respawn and applies a fixed decision table." Per-task idempotency is preserved from S20.1 (sprint-scoped keys); H3 adds orchestrator-level idempotency.

## Scope delivered (per arc brief §3 + sprint plan T1–T6)

1. **`schemas/sprint-state-ledger.md` (new, 210 lines)** — canonical schema (`schemaVersion: 1`), top-level fields, per-task fields, state machine (`pending → spawned → {in-flight} → {completed|failed|declined}`), atomic-write idiom with sibling-lockfile + `flock -x 9` + `mv -f` rename, respawn decision table, schema-guard behavior (`schemaVersion > 1` → escalate `RIV-SCHEMA-GUARD`), archival policy (ledger files left in place, workspace-local, not committed to any repo).
2. **`agents/riv.md` (+94 lines)** — "Task-Ledger Protocol (S20.2 H3)" section: when Riv writes, ledger-read on respawn startup (first tool call after arc brief), atomic-write shell idiom, **resume-declined handler** with `RIV-RESUME-DECLINED` structured payload, respawn decision-table (`attemptCount < 3` retry, `attemptCount ≥ 3` escalate, `declined` always escalate).
3. **`docs/active-arc-reconciler.md` (new, 97 lines)** — formal data contract for `active-arcs.json`, **`sprintShape` taxonomy** (`build` / `spike` / `infra`) with per-shape expected-artifact / source-of-truth / API mapping, default-when-absent = `build` (backward-compatible), alert classes (`closed-unreported`, `stale-no-artifact`, `api-error-<code>`), staleness window (45 min), cooldown dedupe (180 min).
4. **`FRAMEWORK.md` (+7 lines)** — new Core Principle #4 anchor ("State lives in files, not in memory") referenced from the Riv ledger protocol.

**Workspace-local side-effect (not in git):** `~/.openclaw/workspace/scripts/active-arc-reconciler.sh` patched with `sprintShape` branching per the docs contract. Smoke-verified by Nutts (Phase 3a) and Optic (Phase 3c, drill D7). Not part of PR #49 by design — runtime scripts are workspace-local per repo_map.

## PR merged

| PR | Title | Merge SHA | +/- | Files |
|----|-------|-----------|-----|-------|
| [#49](https://github.com/brott-studio/studio-framework/pull/49) | `[S20.2-001] H3 Riv-state durability: task-ledger + reconciler sprintShape [sprint-20.2]` | `ea10e5d7d2e7d56d70b279d38eb0297d1b567698` | +408 / -0 | 4 |

File breakdown:
- `schemas/sprint-state-ledger.md` — `added` — +210
- `agents/riv.md` — `modified` — +94
- `docs/active-arc-reconciler.md` — `added` — +97
- `FRAMEWORK.md` — `modified` — +7

Self-dogfood: PR title carries `[sprint-20.2]` prefix; body first line carries `idempotency-key: sprint-20.2` per S20.1 contract. Boltz's pre-merge `gh pr view --json state,mergeCommit,url` lookup returned no prior match; merge proceeded cleanly.

## Pipeline execution

Clean five-role chain, **first-pass, zero retries, zero respawns**.

| Stage | Agent | Verdict | Notes |
|-------|-------|---------|-------|
| Phase 0 | Riv | Audit-gate PASS | S20.1 audit verified at `audits/battlebrotts-v2/v2-sprint-20.1.md` on studio-audits/main (`b8beb2f7`). |
| Design | Gizmo | PASS (continue-existing design memo) | S20.2 design memo extended with H3 §3a–§3e (ledger schema, protocol, resume-declined, sprintShape). |
| Plan | Ett | PASS (T1–T6) | T1 schema, T2 Riv protocol patch, T3 reconciler doc + script patch, T4 Optic drills, T5 Boltz review, T6 Specc audit. |
| Build | Nutts | PASS | PR #49 opened first-try with correct idempotency-key embedding; workspace reconciler script patched + smoke-tested. |
| Review | Boltz | PASS (clean approve + merge) | Self-dogfood pre-merge lookup returned no prior; merge SHA `ea10e5d7` forwarded. |
| Verify | Optic | PASS (D1–D8, hard-blockers 3/4/5/7, §B) | See drill table below. |
| Audit | Specc | This file | Grade A, scope streak 17 → 18. |

**Runtime observation:** no gateway restarts, no OOMs, no sentinel collisions, no orphan-resume events. Reconciler cron stayed quiet throughout (closed-reported path held from S20.1 → S20.2 transition).

## Optic verification

### 8 Drills

| Drill | Name | Result |
|-------|------|--------|
| D1 | Schema completeness (all required fields documented) | **PASS** |
| D2 | Protocol consistency (agents/riv.md ↔ schemas/sprint-state-ledger.md state machine parity) | **PASS** |
| D3 | Atomic-write idiom correctness (sibling lock + rename, no flock-on-data-file) | **PASS** |
| D4 | Respawn decision-table coverage (all `status` values map to an action) | **PASS** |
| D5 | Resume-declined payload well-formed + consumed by spawning session | **PASS** |
| D6 | `sprintShape` taxonomy exhaustive + default-when-absent preserves backward-compat | **PASS** |
| D7 | Reconciler script branching against live `active-arcs.json` (build/spike/infra) | **PASS** |
| D8 | FRAMEWORK.md anchor resolves from agents/riv.md cross-link | **PASS** |

### Hard-blockers (§A)

| # | Hard-blocker | Result |
|---|--------------|--------|
| 3 | Scope matches sprint plan (T1–T6 all delivered, nothing extra, nothing missing) | **PASS** |
| 4 | Commit discipline (conventional style, `[sprint-20.2]` prefix, one PR one scope) | **PASS** |
| 5 | Role-profile alignment (Riv's new authority is contractual, not implicit) | **PASS** |
| 7 | State-in-files principle upheld (ledger is a file, not in-memory agent state) | **PASS** |

### §B idempotency-key scan

Regex `^idempotency-key: sprint-\d+\.\d+(\.\d+)?$` against all PRs in-range. PR #49 the only PR this sub-sprint; body first line matches; **PASS**.

## Compliance-reliant process detection (Standing Directive §2)

S20.2 installs three new mechanisms. Honest classification:

| Mechanism | Classification | Rationale |
|-----------|---------------|-----------|
| **Ledger schema + atomic-write implementation** | **Structural** (within Riv's execution) | The `flock -x 9` + `mv -f` rename pattern is OS-enforced; once Riv invokes the shell idiom, the atomicity is guaranteed by kernel semantics, not by agent diligence. |
| **Riv writing to the ledger at each task boundary** | **Compliance-reliant** (on Riv's role profile) | Nothing structural forces Riv to write. The ledger is only as durable as Riv's adherence to the `agents/riv.md` protocol. A non-compliant Riv (or a Riv that skips the write) produces a ledger that understates state. This is intrinsic to orchestrator-level durability — no layer above Riv exists to enforce it. |
| **`sprintShape` taxonomy fold-in to reconciler** | **Structural** | Reconciler reads `active-arcs.json`, branches on declarative config, no agent discretion. Once `sprintShape` is set on sub-sprint boundary, the reconciler's behavior is fully determined. **However**, setting `sprintShape` correctly on each sub-sprint boundary is compliance-reliant on The Bott / Riv. |
| **Respawn decision table** | **Structural** (as a specification) | The table's branches are exhaustive and deterministic — a compliant respawn-Riv computes the same action every time. Compliance-reliance narrows to "does respawn-Riv actually follow the table" — the same narrow surface as every other role-profile. |
| **Resume-declined `RIV-RESUME-DECLINED` payload** | **Structural** (once emitted) | The payload schema is fixed; Bott's consumer-side handling is also specified. The compliance surface is narrow: Riv must *choose* to emit the payload instead of silently retrying. Specified in agents/riv.md with a concrete triggering condition (sentinel-present on Riv itself, or harness-block). |

**Bottom line:** H3's durability depends on Riv following its protocol at every task boundary. This is the *narrowest viable* compliance surface for orchestrator state — going further (e.g. a harness-level hook that auto-writes on every `sessions_spawn`) is H4's scope, not H3's. The classification is honest, not a regression.

**Tracking (cross-sprint):** S19.1 Specc sentinel, S19.3 write-phase sentinel, S20.1 idempotency keys — all structurally converted or bounded. S20.2 adds a new narrow-surface compliance item (Riv ledger writes). Net compliance-reliance load across the pipeline continues to decrease; no previously-flagged items have regressed.

## Carry-forwards

All three Optic-surfaced items filed as GitHub Issues on `brott-studio/studio-framework`. No pre-existing backlog issue duplicated; all three are new:

1. **Comparator asymmetry in respawn decision table wording** — `failed` row uses `< 3`, global cap uses `> 3`. Internally consistent (`failed@3` halts; `spawned@3` bumps to 4 before cap) but edge-case nuance worth a docstring clarification. Filed as [#50](https://github.com/brott-studio/studio-framework/issues/50). Labels: `backlog`, `area:framework`, `prio:P3`.
2. **No sub-sprint-wide respawn budget** — only per-task `attemptCount` cap. A degraded environment could mass-escalate (every task hits `<3` without a global fuse). S20.3 design candidate. Filed as [#51](https://github.com/brott-studio/studio-framework/issues/51). Labels: `backlog`, `area:framework`, `prio:P2`, `arc:hardening`.
3. **`infra` reconciler shape aliases `build` artifact path** — intentional taxonomy separation from `build`, but the current doc table doesn't explicitly flag the aliasing. One-line note would prevent confusion for future dashboard consumers. Filed as [#52](https://github.com/brott-studio/studio-framework/issues/52). Labels: `backlog`, `area:framework`, `prio:P3`.

No Specc-independent findings beyond the Optic set. The schema doc, the Riv protocol patch, and the reconciler doc are each internally complete and mutually consistent. Pre-S20.2 items (#29, #30, #32, #34, #35) remain open and untouched by this sub-sprint; none blocked by H3.

## Learning extraction (Standing Directive §3)

Three patterns worth capturing from S20.2:

1. **Durable-state-via-file-ledger for orchestrator resumability.** The `memory/sprint-state/<arc>/<sub-sprint>.json` pattern — one file per sub-sprint, atomic-write via sibling-lockfile + rename, schema-versioned, decision-table-driven respawn — is a reusable pattern for any multi-step orchestrator where transcripts can be lost. Generalizes beyond Riv: any agent that spawns children and needs to resume cleanly could apply the same shape. Worth a KB entry on durable orchestrator state patterns (filed as internal tracking; promote to KB if S20.3 or a future project reuses the pattern).

2. **Taxonomy-first extension to runtime scripts.** The `sprintShape` fold-in is a good shape for extending watchdog behavior: declare the taxonomy in docs with a default-when-absent, let the script branch on a declarative field in `active-arcs.json`, keep all logic in the runtime script (workspace-local) while the *contract* lives in git. Backward compatibility is free. Contrast with the anti-pattern of hard-coding new sprint types into the reconciler script directly.

3. **Spec-walk verification as an Optic mode for framework-docs sub-sprints.** S20.2 had no game code — all deliverables are specs / protocols / docs. Optic's D1–D6 drills are structural spec-walks (field completeness, state-machine coverage, cross-doc consistency) rather than runtime tests. This is a legitimate Optic mode for framework sub-sprints and should be noted as canonical; avoids the false signal of "Optic didn't run a game test, so verification is weaker." It isn't — the artifact under test is the spec, and spec-walks are the right tool.

No KB PRs filed in this audit (framework-docs sub-sprint; the "learnings" are pattern observations for future reuse, not immediate corrections to existing KB entries). If S20.3 reuses the durable-ledger pattern for H4 harness-hook state, promote learning #1 to a full KB entry at that time.

## System-level health (§4)

`openclaw tasks audit` snapshot at 2026-04-23T13:33Z: 83 findings, 5 errors, 78 warnings.

- **5 stale_running errors** — all pre-existing (ages 8h52m to 6d19h). None from S20.2 pipeline runs. Pre-existing operational noise; not blocking this audit.
- **78 warnings** — all `inconsistent_timestamps` (startedAt < createdAt) or `delivery_failed`. Pattern matches prior audits (S19.3, S20.1); known harness clock-skew / delivery-queue noise; not S20.2-caused.
- **No new findings attributable to S20.2 sub-sprint activity.**

Gateway logs reviewed: no OOMs, no agent-spawn failures during the S20.2 window.

## 🎭 Role Performance

**Gizmo:** Shining: continue-existing-design-memo mode used correctly; H3 §3a–§3e additions dovetail cleanly with S20.1's structure. Struggling: nothing sub-sprint-specific. Trend: →.
**Ett:** Shining: T1–T6 plan was exhaustive and actionable first-pass; Riv did not need a replan. Sprint-plan ref is clean and Ett's `sprintShape` default-when-absent call (backward-compat) was a good call. Struggling: none visible this sub-sprint. Trend: ↑.
**Nutts:** Shining: clean single-PR delivery of 4 files (2 new, 2 modified), correct idempotency-key embedding first try, workspace-local reconciler script patched and smoke-verified before handoff. Struggling: none this sub-sprint. Trend: ↑.
**Boltz:** Shining: self-dogfood pre-merge lookup executed correctly; clean approve+merge first-pass; label-check required-status held. Struggling: none. Trend: →.
**Optic:** Shining: D1–D8 drill set adapted well to a no-game-code sub-sprint (spec-walk mode); hard-blockers 3/4/5/7 all PASS; carry-forwards surfaced are high-quality edge cases not obvious failures. Struggling: none. Trend: ↑.
**Riv:** Shining: clean scope-discipline — one arc, no sub-sprint bounding violation (per the S19.3/S19.4/S20.1 correction in SOUL.md); delivered per-arc Riv spawn correctly; no respawns needed. Struggling: not applicable this sub-sprint (no orphan-resume, no H3 dogfood needed yet). Trend: ↑.

## Grade rationale

**A.** H3 closes the orchestrator-level durability gap with a structurally coherent design: file-based ledger, atomic writes via kernel-enforced primitives, schema-versioned, deterministic respawn decision table, explicit narrow-surface compliance-reliance that's honestly classified. Pipeline executed first-pass, zero retries, zero respawns, zero scope creep. `sprintShape` fold-in to the reconciler is a bonus — taxonomy-first extensibility that will pay off every subsequent non-build sub-sprint. Three non-blocking carry-forwards are edge-case nuance, not structural gaps. S20.1 → S20.2 continuity is clean: S20.1's per-task idempotency + S20.2's orchestrator-level ledger compose into a two-layer durability story where every previously-identified orphan/resume failure mode now has a deterministic response. Grade A, scope streak 17 → 18.

---

_This audit was generated by Specc (`brott-studio-specc[bot]`) as part of the BattleBrotts-v2 studio pipeline. For framework details see [`brott-studio/studio-framework`](https://github.com/brott-studio/studio-framework)._
