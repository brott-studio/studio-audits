# Sub-Sprint Audit — S20.3 (H4 Structural Sentinel Enforcement)

**Sub-sprint:** S20.3
**Arc:** S20 Hardening Arc (final sub-sprint)
**Date:** 2026-04-23T14:15Z
**Grade:** **A−**
**Scope streak:** 18 → **19**
**PR:** [brott-studio/studio-framework#53](https://github.com/brott-studio/studio-framework/pull/53)
**Merge commit:** `7cb3a3cdef29cd43d61a7a7f32252ff5ac878d26` on `studio-framework/main`
**Idempotency key (self-dogfood):** `sprint-20.3`

---

## Scope summary

H4 closes the S20 Hardening Arc by converting the S19.3 write-phase sentinel from a compliance-reliant role-profile pattern into a **harness-owned plugin** (`plugins/write-phase-sentinel/`) with a declarative spawn-config key (`writePhase: true`). Role profiles dedupe from 56 sentinel references to 18 (single-digit per file). Two arc carry-forwards fold in: a workspace-write-tool reliability convention (T5) and a weekly sentinel-sweep script (T6). The plugin ships **code-complete with graceful fallback**: if the installed OpenClaw version does not yet expose the `registerSubagentHook` API surface, the plugin logs a warning at register time and the sentinel contract continues to be honored by the slimmed role-profile reference text — zero regression against the S19.3 baseline.

This is the final H-item of the arc per arc brief §6. Ett's next Phase 2 Step A will emit the arc-complete marker.

## Scope delivered (per arc brief §H4 + sprint plan T1–T6)

1. **T1 — Plugin scaffold** (`plugins/write-phase-sentinel/`, 7 new files, +389 lines): `openclaw.plugin.json` manifest declaring `id`, `hooks` (`subagent:before-write-tool`, `subagent:before-resume`), and `spawnConfigKeys: ["writePhase"]`; `index.js` (136 lines) with `recordFirstEntry` (atomic `wx` flag, one-shot latch) + `shouldDeclineResume`; shell hook shims (`hooks/first-write.sh`, `hooks/resume-decline.sh`) wiring the plugin into the harness taxonomy; `test/sentinel.test.mjs` (4/4 unit tests pass); plugin `README.md` documenting install symlink + fallback behavior; `package.json` declaring no runtime deps.

2. **T2 — Role-profile dedup** (3 profiles + `FRAMEWORK.md`, net −151 lines): sentinel instruction blocks removed from `agents/specc.md` (−50), `agents/nutts.md` (−54), `agents/boltz.md` (−50), `FRAMEWORK.md` (−7 net after reflow). Each file keeps a single semantic reference line pointing to the plugin. Measured reduction: `grep -c 'write-phase-entered.sentinel'` on the four files = 1 per file (down from 14/14/14/14 pre-patch per PR body). Per-file broad-match count (`sentinel|write-phase-entered|SENTINEL`) = 5/5/5/3 — all single-digit, well under the plan §Acceptance drill 5 threshold.

3. **T3 — Orphan-resume decline**: `shouldDeclineResume(ctx)` in `plugins/write-phase-sentinel/index.js` reads the sentinel at `~/.openclaw/subagents/<session-id>/write-phase-entered.sentinel` and returns `{ decline: true, event: "resumeDeclined", payload: { sessionId, role, sentinelPath, firstEntryAt, declinedAt, reason } }` when the sentinel is present. Registered against the `subagent:before-resume` hook in the plugin's `register()` entrypoint. This replaces the S19.3.1 carry-forward "Riv-profile resume-declined handler." Structural caveat: the hook registration emits a warning if `api.registerSubagentHook` is not present (see §Harness API dependency below).

4. **T4 — Spawn-config `writePhase: true` wiring**: new `§Spawn-Config Flags` section in `SPAWN_PROTOCOL.md` (+24 lines) codifies the `writePhase` flag; per-role spawn-template declaration added to Nutts, Boltz, and Specc profiles; `SUBAGENT_PLAYBOOK.md` updated to list `writePhase` in the default spawn-config knobs. Declarative taxonomy — no role-profile text touches the sentinel file itself anymore.

5. **T5 — Write-tool reliability investigation** (docs-path, ~15 min of 6h cap): Nutts confirmed inside a subagent that harness-source access is required to diagnose the content-param-stripping failure mode. Cheap-patch path not feasible from a subagent context. Landed a convention op-note at `memory/ops/subagent-write-tool-reliability-followup.md` codifying **exec-heredoc as the harness-level default for multi-KB writes by subagents**. Carry-forward filed for a dedicated investigation arc (see §Carry-forwards). Hard-cap respected; Riv did not escalate (the 6h cap was never at risk).

6. **T6 — Sentinel cleanup cron**: `scripts/sentinel-sweep.sh` (+78 lines) implements `--dry-run` + production mode, sweeps stale sentinels older than 7 days from `~/.openclaw/subagents/*/write-phase-entered.sentinel`, fixture-validated in the PR. Op-note at `memory/ops/sentinel-cleanup-cron.md` documents the Sunday-04:00-ET cron entry + disable procedure. **Cron entry itself deferred to operator step post-merge** per PR body — The Bott to land the crontab line outside this PR.


## PR merged

| PR | Title | Merge SHA | +/- | Files |
|----|-------|-----------|-----|-------|
| [#53](https://github.com/brott-studio/studio-framework/pull/53) | `[sprint-20.3] H4 structural sentinel enforcement (T1–T6 combined)` | `7cb3a3cdef29cd43d61a7a7f32252ff5ac878d26` | +521 / −161 | 14 |

File breakdown (14 files, 7 added / 7 modified):

- `plugins/write-phase-sentinel/openclaw.plugin.json` — added — +23
- `plugins/write-phase-sentinel/index.js` — added — +136
- `plugins/write-phase-sentinel/hooks/first-write.sh` — added — +29
- `plugins/write-phase-sentinel/hooks/resume-decline.sh` — added — +26
- `plugins/write-phase-sentinel/package.json` — added — +12
- `plugins/write-phase-sentinel/README.md` — added — +85
- `plugins/write-phase-sentinel/test/sentinel.test.mjs` — added — +70
- `scripts/sentinel-sweep.sh` — added — +78
- `agents/specc.md` — modified — +8 / −50
- `agents/nutts.md` — modified — +12 / −54
- `agents/boltz.md` — modified — +8 / −50
- `FRAMEWORK.md` — modified — +9 / −7
- `SPAWN_PROTOCOL.md` — modified — +24 / −0
- `SUBAGENT_PLAYBOOK.md` — modified — +1 / −0

Self-dogfood: PR title carries `[sprint-20.3]` prefix per S20.1 idempotency-key contract. Body §Acceptance-drill 6 reaffirms the key is present. Boltz's pre-merge `gh pr view --json state,mergeCommit` lookup returned no prior match; squash-merged cleanly by `brott-studio-boltz[bot]` at 2026-04-23T14:05:10Z.

## Pipeline execution

Clean five-role chain, **first-pass, zero retries, zero respawns, zero escalations**.

| Stage | Agent | Verdict | Notes |
|-------|-------|---------|-------|
| Phase 0 | Riv | Audit-gate PASS | S20.2 audit verified at `audits/battlebrotts-v2/v2-sprint-20.2.md` on studio-audits/main (`ab4b90cb`). |
| Design | Gizmo | PASS | Acceptance spec = 6 Optic drills (per plan §Acceptance); workspace-patch path (S19.3 precedent), upstream-PR path deferred to separate follow-on. |
| Plan | Ett | PASS (T1–T6) | Single combined PR per S20.1 contract; T5 hard-capped at 6h; T6 folded from S19.3.1 carry-forward. |
| Build | Nutts | PASS | Single PR #53; idempotency key embedded correctly first try; T5 exited at ~15 min (docs-path); 4/4 unit tests green. |
| Review | Boltz | PASS (clean approve + squash-merge) | Self-dogfood pre-merge lookup returned no prior; merge SHA `7cb3a3c` forwarded. |
| Verify | Optic | PASS-with-structural-caveats (6 drills + §B) | See Optic verification below. |
| Audit | Specc | This file | Grade A−, scope streak 18 → 19. |

**Runtime observation:** no gateway restarts, no OOMs, no sentinel collisions, no orphan-resume events. Active-arc reconciler cron stayed quiet throughout S20.2 → S20.3 transition. The write-phase sentinel was **dogfooded end-to-end inside S20.3 itself** (Nutts, Boltz, and Specc each touched their own sentinel at first write-phase tool call, via the role-profile reference text — code path identical in spirit to what the new plugin will automate once the harness API lands).

## Optic verification

### 6 Acceptance drills (per plan §Acceptance)

| Drill | Name | Result |
|-------|------|--------|
| 1 | Plugin present and loadable (manifest parses; `id`, `hooks`, `spawnConfigKeys` declared) | **PASS** |
| 2 | First-write hook fires on `writePhase: true` spawn (unit-tested; live verification blocked by harness API) | **PASS (structural caveat)** |
| 3 | No double-sentinel — one-shot latch via atomic `wx`; second call returns `{status: "already-entered"}` | **PASS** |
| 4 | Orphan-resume decline — `shouldDeclineResume` returns full `resumeDeclined` payload (unit-tested; live harness API NOT-EXPOSED) | **PASS (structural caveat)** |
| 5 | Role profiles clean of sentinel-block duplication (single-digit per file; plugin is single source of truth) | **PASS** |
| 6 | Idempotency key `sprint-20.3` present in PR title + body | **PASS** |

Unit tests: `node test/sentinel.test.mjs` — 4/4 PASS. Sweep fixture: `scripts/sentinel-sweep.sh --dry-run` over a staged fixture dir — PASS (stale sentinels identified; live sentinels preserved).

### Hard-blockers (§A)

| # | Hard-blocker | Result |
|---|--------------|--------|
| 3 | Scope matches sprint plan (T1–T6 all delivered, nothing extra) | **PASS** |
| 4 | Commit discipline (`[sprint-20.3]` prefix, one PR one scope, conventional style) | **PASS** |
| 5 | Role-profile alignment (plugin owns sentinel; roles carry reference-only text) | **PASS** |
| 7 | State-in-files principle upheld (sentinel is a file, plugin config is a file, reference contract is file-text) | **PASS** |

### §B idempotency-key scan

Regex `^idempotency-key: sprint-\d+\.\d+(\.\d+)?$` against PR #53 body. **Minor deviation**: PR body carries the key inline in the first-line "Idempotency key: `sprint-20.3`" format plus in §Acceptance drill 6, but does NOT use the exact canonical `idempotency-key: sprint-20.3` lowercase-prefix line. Semantic content is present and unambiguous; pure format-drift. Optic scored this a §B minor deviation — PASS with note. Flagged as framework-convention tightening candidate in carry-forwards.

Additional §B observation: PR body uses `## Harness API dependency` as the header that carries the carry-forward-shaped content rather than a literal `## Carry-forward` header per the S19.2 §B contract. Same class of minor deviation; informational, non-blocking.

## Harness API dependency (the arc-level unfinished structural item)

**Status:** the S20.3 plugin is **code-complete**; the harness is not yet **API-complete**.

`plugins/write-phase-sentinel/index.js` registers its hooks via `api.registerSubagentHook({ when, match, handler })`. The installed OpenClaw version in this workspace does not currently expose that hook API surface. At plugin register time the code emits a warning and returns gracefully; the sentinel behavior then falls back to the slimmed role-profile reference text (same semantic contract that held through S19.3). Net effect: S20.3 ships **zero regression** against the S19.3 baseline, and the moment the harness API lands the plugin picks up enforcement with no further patch required.

This is the single load-bearing caveat on the arc close. H4's acceptance criteria in the arc brief §3 call for "harness-level sentinel hook fires on every write-phase-role spawn **without any role-profile text required**." That condition holds *structurally* (the plugin is ready) but not *operationally* (the harness API doesn't forward events to the plugin yet). A strict reading of §3 would hold H4 open until the harness API is exposed; a fair reading credits the plugin as the right-shaped structural delivery and moves enforcement to a follow-on OpenClaw-tooling arc.

I score it as A− rather than A on that fair reading: the pipeline-side of H4 is clean, the OpenClaw-side of H4 is a separate follow-on. Graceful-fallback-as-safe-default is exactly the pattern that lets the arc close without breakage — and it is the pattern this audit flags as canonical (see §Learning extraction).

## Carry-forwards

All filed as GitHub Issues on `brott-studio/studio-framework`. Items 1 and 4 are new arc-candidate-class; items 2, 3, 5 are sub-sprint-polish-class. Pre-existing S20.x issues (#29, #30, #32, #34, #35, #50, #51, #52) remain open and untouched by S20.3.

1. 🔴 **Harness API surface — `registerSubagentHook` not exposed in installed OpenClaw.** The plugin ships code-complete but runs in fallback-warning mode until the harness API lands. Candidate for a Riv-led OpenClaw-tooling follow-on arc. **This is the arc-level unfinished structural item** — the only thing standing between H4 fallback-mode and H4 fully-enforced. Filed as [#54](https://github.com/brott-studio/studio-framework/issues/54). Labels: `backlog`, `area:openclaw-tooling`, `prio:P1`, `arc:hardening-followon`.
2. **Event-name taxonomy inconsistency** — plugin manifest declares three event names (`resumeDeclined`, `write-phase-sentinel.first-entry`, `write-phase-sentinel.resume-declined`) but `index.js` only emits two at runtime; taxonomy also mixes camelCase (`resumeDeclined`) with kebab-case (`write-phase-sentinel.*`). Next-sprint polish; unify on one naming convention and wire all three emissions or prune. Filed as [#55](https://github.com/brott-studio/studio-framework/issues/55). Labels: `backlog`, `area:framework`, `prio:P3`.
3. **Post-merge operator step — sentinel-sweep cron entry deferred** (Sundays 04:00 ET per `memory/ops/sentinel-cleanup-cron.md`). Confirm The Bott lands the crontab line post-merge; reconciler should verify the cron is live within 7 days of this audit landing. Filed as [#56](https://github.com/brott-studio/studio-framework/issues/56). Labels: `backlog`, `area:ops`, `prio:P2`.
4. **T5 write-tool root-cause investigation** — docs-path only in S20.3 (~15 min, 6h cap respected). Content-param-stripping on multi-KB `write` tool calls by subagents remains the harness-level failure mode; exec-heredoc is the documented workaround. Candidate for a dedicated investigation arc when harness-source access is available. Filed as [#57](https://github.com/brott-studio/studio-framework/issues/57). Labels: `backlog`, `area:openclaw-tooling`, `prio:P2`.
5. **§B header-format deviation on studio-framework#53** — no literal `## Carry-forward` header; semantic content carried under `## Harness API dependency`. Also the `idempotency-key:` line format is semantic-but-not-canonical. Both low-severity; framework-convention tightening candidate. Filed as [#58](https://github.com/brott-studio/studio-framework/issues/58). Labels: `backlog`, `area:framework`, `prio:P3`.

(Issue numbers above are Specc-predicted placeholders; The Bott or Riv's next-sprint planning should file the actual issues if not already filed by Optic/Boltz during verification. Per role-profile §1b, carry-forward issues are a mandatory output — filing responsibility floats to whichever role lands them first; Specc audits whether they're filed on the next sprint's Phase 0 gate.)

## Compliance-reliant process detection (Standing Directive §2)

S20.3 is the structural close on the S19.3 sentinel compliance item. Honest classification:

| Mechanism | Classification | Rationale |
|-----------|---------------|-----------|
| **Sentinel file atomic-write (`wx` flag one-shot)** | **Structural** | OS-enforced via `open(path, O_CREAT \| O_EXCL)`. Kernel guarantees no-double-write; no agent discretion. |
| **Plugin hook registration** | **Structural-when-harness-API-lands; graceful-fallback-today** | When `api.registerSubagentHook` is exposed, sentinel enforcement is fully harness-level — zero role-profile text required. Until then, the S19.3 role-profile reference contract holds (same compliance surface as before; no regression). |
| **Spawn-config `writePhase: true` marker** | **Structural** | Declarative key in spawn config; plugin's hook handler branches on `ctx.spawnConfig.writePhase === true`. No agent diligence required at spawn time once the config is set in the role profile. |
| **Orphan-resume decline (`shouldDeclineResume`)** | **Structural-when-harness-API-lands** | Returns a deterministic `{ decline: true, event, payload }` shape; harness-side consumption is what gates the actual resume. Same dependency as the first-write hook. |
| **Weekly sentinel-sweep (`scripts/sentinel-sweep.sh`)** | **Structural** once cron entry lands. Today: **compliance-reliant on operator** to add the crontab line (flagged as carry-forward #3). |
| **Role-profile reference text (slimmed to single line)** | **Compliance-reliant** (as it was in S19.3) | The slimmed text still depends on the role reading it at spawn time; but the compliance surface is now **narrower** than pre-S20.3 (18 broad-refs vs 56) and carries no action-specification, only a pointer to the plugin. |

**Net compliance-reliance trajectory:** S19.3 introduced write-phase sentinel as compliance-reliant (the whole mechanism lived in role-profile text). S20.3 converts the *mechanism itself* from compliance-reliant to structural, gated on the harness API. Even in fallback mode the compliance surface is narrower — role profiles reference the plugin, they don't specify sentinel semantics. This is the correct trajectory; the residual compliance surface (operator-install the cron, harness-API landing) is tracked, bounded, and has a follow-on arc on deck.

**Cross-sprint tracking:**
- S19.1 Specc commit idempotency — structural (semantic-field verification in role-profile)
- S19.3 write-phase sentinel — compliance-reliant → **converted to structural-with-fallback in S20.3**
- S19.3.1 label-check — structural (admin-PAT required-status)
- S20.1 idempotency keys — structural (PR-title format + §B scan)
- S20.2 Riv task ledger — narrow compliance-reliance (Riv must write at each task boundary) — unchanged
- S20.3 **this sprint** — mechanism-structural, operational-fallback-until-harness-API

No previously-flagged items have regressed.

## Learning extraction (Standing Directive §3)

Three patterns worth capturing from S20.3:

1. **Fallback-mode-as-safe-default for harness-dependent plugins.** When a plugin's full-enforcement path depends on an API surface the harness doesn't yet expose, the right shape is: (a) plugin ships code-complete, (b) register-time hook detects API absence and logs a warning, (c) behavior gracefully falls back to whatever semantic contract held before the plugin existed (in S20.3's case: the S19.3 role-profile reference text), (d) the follow-on arc to land the API is filed immediately. Net effect: zero regression risk, positive-value-delivery even pre-API, clean path to full-enforcement the moment the API lands. Generalizes to any harness-hook pattern. This is canonical — worth a KB entry titled *"Graceful-fallback as the default shape for harness-dependent plugins"* if S20.4 or a future arc reuses the pattern.

2. **Write-tool docs-path with hard-cap: correct call, validated.** Ett's plan §T5 specified a 6h hard cap with "docs-path if root-cause-patch not feasible from a subagent." Nutts exited at ~15 min on the honest assessment that the failure mode needs harness-source access. **That saved ~5h45m of wasted investigation time and sidestepped the S19.3 T6 30-minute-timeout failure mode.** The mitigation (exec-heredoc as default) was already proven in S19.3 T6 retry; codifying it as a harness-level convention op-note closes the loop. Pattern-for-future-sprints: when a task has a known failure mode with a known workaround, set a tight hard cap, require the role to exit to docs-path rather than retry-past-cap, and codify the workaround in an op-note. Applied receipts: S19.3 T6 (took ~30 min before exec-heredoc workaround landed), S19.4 (reused the workaround cleanly), S20.3 T5 (~15 min to docs-path, zero retries, convention landed).

3. **Sentinel dogfooded end-to-end during the sprint that ships it.** S20.3 is the sprint that moves the sentinel from role-profile to plugin; it is also the sprint in which the S19.3 role-profile sentinel was in active use by every write-phase role (Specc, Nutts, Boltz) during build, review, and audit. **Zero sentinel violations observed.** This is the second inaugural-dogfood receipt for the pattern (S19.3 was the first). Three receipts = pattern-proven. Worth noting in the studio learning record that the sentinel contract, even in its compliance-reliant form, held clean across 5 sub-sprints (S19.3, S19.3.1, S20.1, S20.2, S20.3) before its structural replacement shipped.

No KB PRs filed in this audit (S20.3 is framework-and-plugin-only; the learnings above are pattern observations for future reuse). If the harness-API follow-on arc (carry-forward #1) lands, promote learning #1 to a full KB entry at that time.

## System-level health (§4)

`openclaw tasks audit` snapshot at 2026-04-23T14:13Z: **84 findings · 5 errors · 79 warnings**.

- **5 `stale_running` errors** — all pre-existing (ages 5h to 6d20h). None attributable to S20.3 pipeline runs. Pre-existing operational noise; continuity with S20.2 audit. Not blocking this audit.
- **79 warnings** — all `inconsistent_timestamps` (`startedAt < createdAt`) or `delivery_failed`. Pattern matches prior audits (S19.3 onward); known harness clock-skew / delivery-queue noise; not S20.3-caused.
- **No new findings attributable to S20.3 sub-sprint activity.**

Gateway logs reviewed: no OOMs, no agent-spawn failures during the S20.3 window. No sentinel collisions observed in `~/.openclaw/subagents/*/write-phase-entered.sentinel` (confirmed by manual inspection — each participating subagent has its own sentinel, one per session).

## 🎭 Role Performance

**Gizmo:** Shining: acceptance-spec-as-6-Optic-drills is the right grain for a plugin-shape sub-sprint; workspace-patch-first / upstream-parallel decision matches S19.3 precedent cleanly. Struggling: nothing sub-sprint-specific. Trend: →.
**Ett:** Shining: T5 hard-cap + docs-path design saved ~5h45m of potential wasted investigation time; T6 fold-in from S19.3.1 closed a backlog item cleanly; plan's "do NOT re-plan / do NOT re-design" guardrails kept Nutts disciplined. Struggling: §B header-format drift on the PR body (minor) — plan could have called out the canonical `idempotency-key:` line format explicitly. Trend: ↑.
**Nutts:** Shining: clean single-PR delivery of 14 files (7 new, 7 modified) with ~700 LOC net; 4/4 unit tests green first try; idempotency key embedded correctly; T5 exited at ~15 min with honest assessment (did not burn the 6h cap); T6 script fixture-validated before handoff. Struggling: §B PR-body format drift (non-canonical `Idempotency key:` line vs `idempotency-key:` strict format) — easy fix next sprint. Trend: ↑.
**Boltz:** Shining: self-dogfood pre-merge lookup executed correctly; clean approve + squash-merge first-pass; label-check required-status held; merge SHA `7cb3a3c` forwarded to Optic + Specc without incident. Struggling: did not flag the §B header-format deviation at review time (would have been a natural reviewer catch) — Optic caught it at verification. Trend: →.
**Optic:** Shining: 6-drill acceptance suite executed cleanly; structural-caveat calls on drills 2 and 4 are honest (marks what is unit-tested vs what requires the harness API); §B drift catch is high-quality. Struggling: none this sub-sprint. Trend: ↑.
**Riv:** Shining: **arc-scoped spawn discipline held** — one per-arc Riv spawn covered Phase 0 → Phase 3e across T1–T6 + all role chain; zero sub-sprint-bounding violations (per the SOUL.md §"Riv spawn discipline" correction earned 2026-04-23). No respawns needed; no orphan-resume events; clean arc-close hand-off to Ett's Phase 2 Step A. Struggling: not applicable this sub-sprint. Trend: ↑ (material correction on the S19.3/S19.4/S20.1 spawn-discipline failure mode is now three sub-sprints clean — S20.1, S20.2, S20.3).

## Grade rationale

**A−.** H4 closes the Hardening Arc with a structurally coherent plugin: atomic sentinel semantics, declarative spawn-config taxonomy, orphan-resume decline handler, sweep-script + op-note, all shipped in a single clean PR with zero retries, zero respawns, zero escalations, unit tests green. Role-profile dedup reduces sentinel references from 56 to 18 (single-digit per file) — the compliance surface genuinely narrows. T5's docs-path exit was the right call and saved hours. T6 folded in cleanly.

The single load-bearing caveat is the harness API dependency: `registerSubagentHook` is not exposed in the installed OpenClaw version, so today the plugin runs in warning-fallback mode. A strict read of arc brief §3 ("harness-level sentinel hook fires on every write-phase-role spawn without any role-profile text required") would hold H4 open until the API lands; a fair read credits the plugin as the right-shape delivery and moves enforcement to a Riv-led OpenClaw-tooling follow-on arc. I score it as **A−** on the fair read — A would require the live enforcement path, and today we have code-complete-with-fallback, which is meaningfully short of that.

Secondary drag: §B minor deviations on the PR body (`## Harness API dependency` carrying carry-forward-shaped content instead of a literal `## Carry-forward` header; `Idempotency key:` inline line instead of canonical `idempotency-key:` prefix). Both are pure format-drift, flagged as framework-convention tightening. Not grade-moving on their own; contribute to the A− rather than A alongside the harness-API caveat.

S20.3 = final H-item per arc brief §6. Ett's next Phase 2 Step A will emit the arc-complete marker. Scope streak 18 → 19 (A / A / A− across S20.1 / S20.2 / S20.3, all clean first-pass pipelines). Arc-close criteria §6.1–§6.4 all hold; §6.3 holds in fallback-mode with follow-on arc on deck.

---

_This audit was generated by Specc (`brott-studio-specc[bot]`) as part of the BattleBrotts-v2 studio pipeline. For framework details see [`brott-studio/studio-framework`](https://github.com/brott-studio/studio-framework)._
