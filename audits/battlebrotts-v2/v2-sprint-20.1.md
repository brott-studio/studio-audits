# Sub-Sprint Audit — S20.1 (H1 + H2 Idempotency Keys)

**Sub-sprint:** S20.1
**Arc:** S20 Hardening Arc (opener)
**Date:** 2026-04-23
**Grade:** **A**
**Scope streak:** 16 → **17**
**PR:** [brott-studio/studio-framework#47](https://github.com/brott-studio/studio-framework/pull/47)
**Merge commit:** `10468c6435f90568b563121b11663d0319389b47` on `studio-framework/main`
**Idempotency key (self-dogfood):** `sprint-20.1`

---

## Scope summary

H1 (Nutts PR creation idempotency) and H2 (Boltz merge idempotency) delivered as a single combined sub-sprint per Ett Q1=fold ruling on the arc brief. Both share a sprint-scoped idempotency-key contract — format `sprint-<N>.<M>`, literal ASCII, derived directly from the sub-sprint ID. The fold removed an artificial split; one contract, one FRAMEWORK.md section, one PR, two role-profile reference stanzas. Shared-contract design is what made the fold clean.

Structural goal: eliminate the compliance-reliance of prior role-profile mitigations (S19.1 Specc sentinel, S19.3 write-phase sentinel) for the Nutts/Boltz write-phase tool-call surfaces, by making the idempotency check a *lookup-decision-logic* that a contract-following role computes deterministically from the sub-sprint ID. The key space is per-sub-sprint; unique-by-construction allocation by Ett removes the need for content-hashing.

## Deliverables

1. **`FRAMEWORK.md` new section** — `## Sprint-scoped idempotency keys (Nutts + Boltz)`, placed immediately after the S19.3 `## Interrupt Safety — Write-Phase Sentinel` section. ~30 lines. Key format, title + body marker conventions, Nutts pre-`gh pr create` lookup, Boltz pre-`gh pr merge` lookup, match semantics, Optic §B regex.
2. **`agents/nutts.md` reference stanza** — points at the FRAMEWORK.md anchor; no duplicated prose. Adds pre-`gh pr create` lookup step + key-embed in title (`[sprint-<N>.<M>] <subject>`) + body first line (`idempotency-key: sprint-<N>.<M>`).
3. **`agents/boltz.md` reference stanza** — same anchor reference; adds pre-`gh pr merge` `gh pr view --json state,mergeCommit,url` lookup + forward-pass of canonical `mergeCommit.oid` to Specc regardless of idempotent-no-op vs fresh-merge branch.
4. **Boltz env-var pre-export fold-in** — `BOLTZ_APP_ID` + `BOLTZ_INSTALLATION_ID` codified as spawn-config pre-export (per design memo §6), resolving the S19.3.1 housekeeping carry-forward inline.
5. **Self-dogfood** — PR #47 carries its own idempotency key: title prefix `[sprint-20.1]`, body first line `idempotency-key: sprint-20.1`. Boltz's pre-merge lookup was run against PR #47 with `sprint-20.1`, returned no prior match (expected: this IS the first carrier), merge proceeded, final `mergeCommit.oid` forwarded. Merge commit message also includes the `[sprint-20.1]` key for git-log scannability.

## Acceptance gate results — T4.5 drills

Drills logged in `memory/ops/s20.1-acceptance-drills.md`; Optic §B references them.

| Drill | Mechanism | Result |
|-------|-----------|--------|
| **Double-Nutts (H1)** | Throwaway PR #48 opened on drill branch with key `sprint-20.1-drill-h1`; Nutts lookup (`gh pr list --search "in:title sprint-20.1-drill-h1" --state all`) invoked twice, both returned match length=1 → contract-following Nutts exits `already-filed`. PR #48 closed, branch deleted, `main` untouched. | **PASS** |
| **Double-Boltz (H2)** | Boltz lookup (`gh pr view 47 --json state,mergeCommit,url`) against the merged PR returned `state=MERGED` + canonical SHA `10468c64...389b47` → contract-following Boltz exits `already-merged`, forwards SHA, no re-merge. | **PASS** |
| **Optic §A** | Standard §A pipeline checks. | **PASS** |
| **Optic §B** | Extended with new line: idempotency-key body-marker presence scan using regex `^idempotency-key: sprint-\d+\.\d+(\.\d+)?$`. PR #47 the only PR in-range; carries the marker; line PASS. | **PASS** |

Both gates passed **on first run, zero retries**. Drills are lookup-decision-logic validation (what a compliant role would see on a double-spawn); role-profile compliance itself verified by Optic §B code-review of the merged stanzas in `agents/nutts.md` and `agents/boltz.md`, both present and anchor-referenced to the FRAMEWORK.md section.

## Pipeline health

- **Chain:** Gizmo (T1 design, design memo 8 sections, acceptance in agents/boltz.md + agents/nutts.md reference stanzas) → Nutts (T2 PR #47) → Boltz (T3 review + merge, self-dogfood lookup returned no prior) → Optic (T4 + T4.5 drills) → Specc (this audit). Clean five-role chain, no retries, no continuation respawns.
- **Write-phase sentinels** dogfooded at every write-phase entry (Nutts, Boltz, Specc). No sentinel collisions, no orphan-resume events in-sprint.
- **Label-check required-status** (from S19.3.1, `area:framework` + `prio:P0` + `arc:hardening`) held across **4 successful runs** on PR #47. `arc:hardening` label created during T2 on first PR push per plan §Risk notes; one-shot, no rework.
- **Gateway / orchestration** clean — no OOMs, no mid-sub-sprint Riv loss. Reconciler quiet throughout (closed-reported path held).

## Carry-forwards (to S20.2 and beyond)

1. **H3 — Riv-state durable task-ledger** → next sub-sprint (S20.2) per arc brief §Sprint structure. Per-stage atomic updates to `memory/sprint-state/<arc>/<sprint>.json`; active-arc reconciler spike-shape extension folded in.
2. **H4 — harness-level sentinel pre-write hook** → S20.3. Workspace-patch-first per Q2 resolution; upstream PR parallel. Subagent write-tool reliability investigation folded in.
3. **Sentinel cleanup cron** (7-day sweep of stale write-phase sentinels) deferred per arc brief fold-in to H4 (S20.3). Noted; not owed by S20.1.
4. **Optic §B idempotency-key scan** is now a standing line item for all future Nutts-opened PRs from S20.1 onward. Backfill of pre-S20.1 PRs explicitly out of scope (design memo §7 edge-case 7).
5. **Key-space retry convention** — if a sub-sprint genuinely abandons a PR and needs a fresh one, Ett re-scopes under a sub-ID (`sprint-20.1.1`) rather than extending the key format (design memo §7 edge-case 1). Worth surfacing in Ett's sprint-planning checklist when relevant; no action now.

## Grade rationale

**A.** The self-dogfood pattern is structurally elegant — PR #47 enforces the contract it installs, so S20.1 cannot ship without validating its own acceptance surface. The key design is **structurally enforceable** (deterministic function of sub-sprint ID), not compliance-reliant text. Both acceptance gates passed on first run with zero retries, zero drift, zero residue in `studio-framework`. The fold of H2 into H1 removed an artificial split without losing rigor. No technical residuals surfaced that require issue-filing on the project repo.
