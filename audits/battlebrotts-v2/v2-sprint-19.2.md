# v2 Sprint 19.2 Audit — Gateway OOM Mitigation + §B CF-Header Regex Fix

**Date:** 2026-04-23T01:30Z
**Arc:** S19 Orphan-Recovery Durability
**Sub-sprint:** S19.2
**Proposals:** 3.3 (gateway OOM mitigation) + S19.1 carry-forward (§B CF-header regex)
**Grade threshold (per sprint plan):** A−

**Grade:** A−
**Scope streak:** 13 sub-sprints clean (extending the S19.1 streak of 12).

---

## Summary

S19.2 is a **combined two-track sub-sprint**:

- **Track A (Bott-direct ops, no repo commits):** raise gateway Node heap ceiling to 8 GB via systemd drop-in, prune the `runs.json` subagent registry, and leave a workspace-local op note. Scope-gate: heap flag active + gateway stable through restart. Met.
- **Track B (pipeline code change):** [`brott-studio/studio-framework#36`](https://github.com/brott-studio/studio-framework/pull/36) — one-line regex fix to `agents/specc.md` §B field-3, broadening the Carry-forward header matcher to accept numbered and variant headers (`## 10. Carry-forward → GitHub Issues`, `## 4. Carry-forwards`, etc.). Merged at `ec4af11b20504a4f859f3228b8c11cadeeea93fd` on 2026-04-22T22:46:26Z, +1/-1 across a single file.

Both tracks closed within scope with all gates met. One sub-sprint-level carry: PR #36 merged without `area:*` / `prio:*` labels (second occurrence of the S19.1 #34 pattern — see Carry-forward).

This is the **first audit committed under the new §B regex** — the post-merge `specc.md` on main is what this Specc session is reading, so the idempotency §A procedure and §B comparison now run against the broadened matcher.

## Self-audit observation

Ran the §A pre-commit verification before `git add`/`commit`/`push`:

1. `git fetch origin main` — OK.
2. `git cat-file -p origin/main:audits/battlebrotts-v2/v2-sprint-19.2.md` — non-zero exit, empty stdout.
3. Branch: **missing** → proceed with normal commit + push.

The `missing` branch is again the only branch exercised by this audit's own commit (fresh sub-sprint slot). `exists+match` / `exists+differ` remain validated by Optic's S19.1 sibling task.

## Track A — Gateway OOM mitigation (ops-only, verified)

Executed 2026-04-22T22:49:46Z – 22:50:02Z; closeout verified 2026-04-23T01:25–01:27Z.

| Step | Action | Verified |
|---|---|---|
| A2 | `runs.json` prune 718 → 204 entries (4.59 MB → 1.66 MB); backup `runs.json.bak-20260422T224946Z` kept | ✅ Backup file present; prune delta matches op note. |
| A1 | `archiveAfterMinutes=60` appended to `~/.openclaw/config.toml` | ⚠️ Appended under `[subagents]` — **wrong key path** (correct: `agents.defaults.subagents.archiveAfterMinutes`). Behavior-equivalent today (source default is already 60). Carry-forward filed. |
| A3 | Systemd drop-in `~/.config/systemd/user/openclaw-gateway.service.d/override.conf` with `--max-old-space-size=8192`; daemon-reload + restart | ✅ Effective `ExecStart` confirmed via `systemctl --user show`: `argv[]=/usr/bin/node --max-old-space-size=8192 ... gateway --port 18789`. Gateway PID 118776 → 125240 at 22:50:02Z. |
| A4 | Op note `memory/ops/gateway-oom-mitigation-2026-04-22.md` written | ✅ 81 lines; full details + reversibility procedure. Workspace-local (not in a studio repo). |
| A5 | Post-restart stability | ✅ Gateway `active (running)` at 2026-04-23T01:26Z, uptime 2h 36min, memory 2.7 GB (peak 3.6 GB) — well under the 8 GB ceiling and already past the pre-restart 4 GB Node default that was being exceeded. No further restarts. |

**Sprint-gate met:** heap flag active + gateway stable through restart. ✅

**Arc-level 72h observation window:** per HCD decision at 2026-04-22T22:43Z, the 72h stability window (runs until 2026-04-25T22:50Z) is an arc-level gate and **does not block S19.2 closure or S19.3 start**. Tracked separately.

Previous gateway process peaked at **5.9 GB RSS** over a 7h window, confirming the OOM risk was real (Node default `--max-old-space-size` is ~4 GB on x64). The heap raise is the right lever.

**Track A is ops-only.** No repo commits, no PRs. This audit attests to the operational change + verification; there is no PR for Boltz to have reviewed.

## Track B — §B CF-header regex hardening (PR #36)

| Item | Status | Notes |
|---|---|---|
| PR opened on correct repo (`studio-framework`) | ✅ | |
| PR body references S19.1 carry-forward | ✅ (per title + linked arc brief) | |
| Boltz review on PR | ✅ | `brott-studio-boltz[bot]` APPROVED 2026-04-22T22:46:25Z (1s before merge). |
| Merge via squash | ✅ | `ec4af11b20504a4f859f3228b8c11cadeeea93fd`. |
| Diff narrowly scoped | ✅ | `agents/specc.md` only, +1/-1. No collateral changes. |
| PR labels (`area:*`, `prio:*`) | ❌ | **Second occurrence.** PR #36 has empty `labels` array — same class as S19.1 PR #33 (tracked in [#34](https://github.com/brott-studio/studio-framework/issues/34)). Not merge-blocking; carry-forward note added (see §Carry-forward). |

### Regex change on line 139 (extraction rule for Field 3)

**Old:** `^##\s+Carry-forward`
**New:** `^##\s+(?:\d+(?:\.\d+)?\.\s+)?[Cc]arry[- ]?[Ff]orward`

Post-merge content on `main` confirms the broadened matcher and extends the normalization column's allowed-variant list to include `Carry-Forward`, `Carry-forwards`, `CarryForward`, and numbered headers like `## 10. Carry-forward → GitHub Issues`.

### Optic re-validation (PASS)

Tested against real audits on `studio-audits/main`:

- `v2-sprint-17.4.md` L264 (`## 10. Carry-forward → GitHub Issues`) — new regex matches, old regex missed.
- `v2-sprint-18.1.md` L92 (`## 4. Carry-forwards`) — new regex matches, old regex missed.

**Body extraction deltas:**
- S18.1: 6 CF bullets extracted cleanly.
- S17.4: 0 bullets — CF section uses a markdown table + `### 10.1/10.2/10.3` subheaders, not `-`/`*` bullets. Pre-existing spec-vs-structure mismatch, unrelated to the header regex. Tracked as [studio-framework#40](https://github.com/brott-studio/studio-framework/issues/40).

The header fix does what it was scoped to do. The body-format mismatch is a separate, known issue and deliberately out-of-scope for S19.2.

## Compliance-Reliant Process Detection (Standing Directive)

Still on option (a) of the DQ-2 decision: role-profile + Boltz PR review are the only enforcement surface for the audit-commit idempotency contract. S19.2 does not change this posture — [`studio-framework#32`](https://github.com/brott-studio/studio-framework/issues/32) (server-side enforcement) remains open and correctly labeled. Not graded down; the scope call was correct for S19.1 and S19.2 both. Flagging again so it stays visible: every sub-sprint that closes without #32 landing is another sub-sprint where the contract is compliance-reliant.

Second compliance-reliant surface now emerging: **PR label hygiene.** Two consecutive S19 PRs (#33, #36) merged without `area:*` / `prio:*` labels. If #34 stays open without a structural fix (e.g. a label-presence check on Boltz's merge checklist, or a CI labeler), S19.3+ will keep repeating the miss.

## Carry-forward

- [studio-framework#39](https://github.com/brott-studio/studio-framework/issues/39) — Investigate `archiveAfterMinutes` cleanup: `runs.json` registry regrew 204 → 719 entries within 2.5h post-prune despite source default of 60 min. Bundle A1 config.toml key-path correction (wrong path appended) into this investigation. Target: S19.3 investigation or arc backlog.
- [studio-framework#40](https://github.com/brott-studio/studio-framework/issues/40) — §B field-3 body rule requires `^\s*[-*]\s+` bullets, but S17.4 CF section uses table + `###` subheaders, producing `[]` under strict filter. Decide (a) loosen §B body rule vs (b) enforce bullet format on authors. Arc backlog.
- [studio-framework#34](https://github.com/brott-studio/studio-framework/issues/34) (existing) — **Second occurrence this sprint:** PR #36 merged with no labels, same as S19.1 PR #33. Pattern, not one-off. Fix belongs on Boltz's pre-merge checklist as a structural check, not retroactive backfill. (Comment attempt on #34 failed with `403 Resource not accessible by integration` — Specc App lacks `issues:write` scope for comments, only issue creation. Logging here as the canonical narrative record; The Bott or a human-authenticated session can add the comment to #34 if needed.)
- Speculative, **not** filed as an issue: `## Carry-forward-policy` / `## Carry-forward-procedure` prefix-collision risk for the new §B header regex. No current instance, low priority. Noted as a known watchpoint for future hardening. (Skipping per task brief guidance that this is speculative.)
- Arc-level (not filed this sprint): 72h gateway stability observation window runs until 2026-04-25T22:50Z. Surface to HCD at arc close, not S19.2.

## 🎭 Role Performance

**Gizmo:** Did not participate this sprint. (S19.2 scope was ops + one-line regex fix; no design work required.)

**Ett:** Shining. Sprint-plan shape for a combined two-track sub-sprint (ops-only Track A + single-PR Track B) was clean — scope-gates separable, arc-level gate (72h window) correctly held out of sub-sprint closure, carry-forward budget pre-identified. Struggling: none specific to this sprint. Trend: ↑.

**Nutts:** Shining. PR #36 diff is surgical — +1/-1 across one file, exactly the regex change specified in the S19.1 CF item, no collateral drift. PR title names the sub-sprint. Struggling: the regex itself covers the numbered-header case cleanly but does not pre-empt the `Carry-forward-policy` prefix-collision risk; minor, speculative. Trend: →.

**Boltz:** Strong. Substantive review + APPROVE on PR #36, 1s pre-merge. Struggling: **missed the empty-labels check again** — second consecutive sprint (S19.1 PR #33, S19.2 PR #36). Carry-forward #34 is now a two-instance pattern, which is signal not noise. Role-profile should add a pre-merge label-presence assertion. Trend: → (quality of review is ↑, merge-checklist compliance is →).

**Optic:** Did not participate in Track B per typical sprint plan (one-file regex fix didn't warrant an Optic-verified check on a non-branch-protection-required path). Sibling S19.1 simulation task (test cases 2 + 3 on S17.4/S18.1) remains the relevant validation surface and passed. Trend: → (no new data).

**Riv:** Shining. Combined-track orchestration (parallel Track A ops-direct + Track B pipeline) executed without scope bleed between tracks; Track A op note was written before Track B merged; verification closeout ran independently. Struggling: none observed from the audit-side view. Trend: ↑.

**The Bott:** Shining. Track A executed cleanly as Bott-direct (systemd drop-in + config edit + daemon-reload + restart + op note), correctly classified as "ops, not pipeline" per the routing decision. Struggling: A1 `archiveAfterMinutes` appended under wrong key path (`[subagents]` instead of `agents.defaults.subagents.archiveAfterMinutes`); caught and surfaced in the op note itself, so process worked, but the edit slipped pre-verification. Trend: ↑.

## System-Level Audit Sources

`openclaw tasks audit` snapshot at 2026-04-23T01:27Z: clean overall. The only warnings are the known-benign `inconsistent_timestamps` (`startedAt earlier than createdAt`) entries on recent Task records — same class noted in S19.1, unchanged, not an S19.2 regression. One failed task in the recent window is the expected S19.2 sprint-plan stage, unrelated to OOM or regex change.

Gateway health:
- PID 125240, uptime 2h 36min, active.
- Memory 2.7 GB current, 3.6 GB peak post-restart (vs. 5.9 GB peak pre-restart).
- Heap ceiling `--max-old-space-size=8192` confirmed in effective `ExecStart`.
- No restarts since 22:50:02Z.

No new finding attributable to S19.2 scope.

---
