# Sprint 18.1 — Post-Merge Audit

**Project:** battlebrotts-v2
**Sprint:** 18.1 (sub-sprint 1 of 5, S18 "Framework Hardening" arc)
**Date:** 2026-04-22T00:38Z
**Auditor:** Specc
**PM:** Ett
**Grade:** **A−**
**Arc status:** S18 arc in-flight — S18.1 closes cleanly under the authorized narrow-read of AC-1; residuals are in-scope for later sub-sprints (primarily S18.4), not S18.1 gaps.

---

## 1. Headline

S18.1 landed the first P0 brick of the Framework Hardening arc: two new per-agent GitHub Apps (`brott-studio-optic`, `brott-studio-boltz`), `Optic Verified` wired as a required status check on `battlebrotts-v2:main`, and a framework-doc sweep through `SECRETS.md` / `SPAWN_PROTOCOL.md` / profile updates for Optic and Boltz. Two throwaway PRs produced direct, headless evidence for AC-1 (#222 → HTTP 405, pipeline-actor block) and AC-2 (#219 → Boltz App cross-actor review/merge HTTP 200). Scope-gate held: zero diffs under `godot/**` or `docs/gdd.md`.

The one **known residual** — admin-PAT bypass on `main` (PR #221 → HTTP 200) — is **deliberately carried to S18.4** per the arc plan and HCD-delegated Bott decision 2026-04-21 authorizing the narrow-read of AC-1. Under that reading (see §3.1), AC-1 is PASS. AC-2..AC-6 are full PASS with no carve-outs.

**Grade rationale:** A−, not A.
- Execution was clean. Correct agent actor on PR #22 (studio-framework) shows as `merged_by: brott-studio-boltz[bot]` — the Boltz App identity landing its own framework-wiring PR is exactly the loop closing.
- Two soft spots prevent A: (a) PR #223 (the sprint close-out amendment itself) had to merge via admin-PAT because a docs-only plan PR cannot satisfy `Optic Verified` — operationally fine, but it is a second data point confirming S18.4 scope is correctly defined; (b) the planning-PR audit-gate CI check (O1 Option B) is real residual scope for S18.2, not a bug, but its absence is why close-out had to lean on convention rather than a structural gate.
- No "Struggling" item this sprint is a pipeline-execution fault. Everything flagged is either (i) deliberately deferred per the arc brief, or (ii) a structural improvement opportunity already docketed.

---

## 2. Scope-streak ledger

| Sub-sprint | `godot/data/**` drift | `docs/gdd.md` drift | `godot/arena/**` drift | Final-merge status |
|---|---|---|---|---|
| S17.1 | 0 | 0 | 0 | clean |
| S17.2 | 0 | 0 | 0 | clean |
| S17.3 | 0 | 0 (at merge) | 0 | clean |
| S17.4 | 0 | 0 | 0 | clean |
| **S18.1** | **0** | **0** | **0** | **clean** |

Streak: **8 consecutive sub-sprints scope-gate clean.** S18.1 was an explicit framework-only sprint; scope-gate compliance is expected here but still worth noting — no agent tried to slip a game-code hunk into the framework-hardening window.

---

## 3. Acceptance criteria evaluation

### 3.1 AC-1 — S17.1-005 "physically impossible to bypass" — **PASS (narrow read)**

**Authoritative citation.** Per HCD-delegated Bott decision 2026-04-21 (documented in `sprints/sprint-18.1.md` §"Close-out residuals"), AC-1 is interpreted as: *"pipeline actors (App tokens) cannot bypass the branch-protection gate."* This is the operational intent of S17.1-005's breach-prevention goal — the S17.1 root-cause was a pipeline-actor (Specc-flow) merging before Optic verified. Under the narrow read, AC-1 is PASS.

**Evidence.**

- **PR #222** (`riv: AC-1 probe (non-admin merge block test)`): Boltz-App-token merge attempt against `main` *before* Optic posted `Optic Verified` → **HTTP 405**, merge rejected by branch protection. PR closed unmerged as intended. ✅
- **PR #221** (`[S18.1-012] throwaway — AC-1 formal proof (post-008)`): Admin-PAT probe merge → **HTTP 200**, merged by `brotatotes`. This is a **known residual**, not a sprint regression: branch protection does not have `enforce_admins: true` set, and the sprint plan explicitly out-of-scopes `enforce_admins` to S18.4 ("DO NOT flip `enforce_admins` this sprint — that's S18.4 scope"). Carry-forward documented in §4.

**Branch-protection API snapshot (as of audit time):**

```
required_status_checks.contexts = ["Godot Unit Tests", "Playwright Smoke Tests", "Optic Verified"]
Optic Verified → app_id 3459479  (brott-studio-optic, distinct from Specc/CI)
enforce_admins.enabled = false   (S18.4 scope)
restrictions = null              (S18.4 scope — Optic-as-sole-merger)
```

The `Optic Verified` required check is wired correctly and bound to the Optic App specifically (not the shared PAT or CI actor). That is the structural substance of AC-1.

### 3.2 AC-2 — Boltz self-review-422 resolved — **PASS**

**Evidence.**

- **PR #219** (`[S18.1-013] throwaway — Boltz cross-actor review test`): Nutts-authored, Boltz-App-token review+merge → merged by `github-actions[bot]` via auto-merge after Boltz's approving review cleared the gate (expected per R3 in the sprint plan). Cross-actor APPROVE returned HTTP 200 (not 422). ✅
- **PR #22 on `brott-studio/studio-framework`** (the S18.1 framework-wiring PR): `merged_by: brott-studio-boltz[bot]`. Real pipeline-work PR landing under the correct App identity — the loop is closed in production use, not just on a throwaway.

Same-actor 422 remains a platform-level artifact, explicitly out-of-scope and documented in the Boltz profile per [S18.1-010].

### 3.3 AC-3 — Inventory documented — **PASS**

`studio-framework/SECRETS.md` (PR #22) adds Optic and Boltz App inventory entries — App ID, Installation ID, PEM path (mode `0600` noted), token-helper path — in the same inline-comment shape as the existing Specc entry. Structural conformance with the S16.2 pattern eliminates tooling churn, as the sprint plan called for.

### 3.4 AC-4 — Profiles updated — **PASS**

- `agents/optic.md`: new "Check-run posting" section — endpoint, `$TOKEN` mint path, body shape, `success`/`failure` conclusion map, head-SHA fetch, timing (after verdict, before return to Riv), error handling.
- `agents/boltz.md`: new "Authentication (GitHub App token)" section — token mint, review-then-merge flow using the App token, cross-actor APPROVE 200 vs same-actor 422 edge, `github-actions[bot]` auto-merge shadow (R3), cross-refs to `SECRETS.md` + `docs/kb/per-agent-github-apps.md`.
- `agents/specc.md`: single cross-reference line + link; rule is **not** duplicated — conforms to the arc-docket §5c principle ("if a structural gate enforces X, profiles should not talk about X").
- `SPAWN_PROTOCOL.md`: Optic + Boltz preambles export their own App IDs / Installation IDs and mint `$TOKEN` from their own helpers; Specc preamble preserved as template.

### 3.5 AC-5 — No silent PAT fallback — **PASS**

`~/bin/optic-gh-token` and `~/bin/boltz-gh-token` follow the same refusal pattern as `~/bin/specc-gh-token`: exit non-zero on config/API failure, no fallback to `~/.config/gh/brott-studio-token`. Verified by inspection of the helper (host-local; sprint plan [S18.1-003]/[S18.1-004] deployment note). Agent code paths all go through `$TOKEN` minted by the helper; no silent-fallback surface found in the updated profiles.

### 3.6 AC-6 — Scope-gate held — **PASS**

Zero diffs under `godot/**` or `docs/gdd.md` across the entire S18.1 build set (#218, #219, #221, #222, #223 on `battlebrotts-v2`; #22 on `studio-framework`). All changes land in `studio-framework/**`, `sprints/**`, host-local `~/bin/**`, and branch-protection config. Hard scope-gate held.

---

## 4. Carry-forwards

All carry-forwards are filed as GitHub Issues on `battlebrotts-v2` per the Specc profile §1b (queryable backlog, not audit-only residuals).

### To S18.4 (branch-protection tightening)


- **Admin-PAT bypass on pipeline merges → [#224](https://github.com/brott-studio/battlebrotts-v2/issues/224).** `enforce_admins` is currently `false` on `main`. PR #221 merged via admin-PAT at HTTP 200 (S18.1-012 evidence). Deliberately deferred to S18.4 per sprint plan.
- **Optic-as-sole-merger enforcement → [#225](https://github.com/brott-studio/battlebrotts-v2/issues/225).** Branch-protection `restrictions` is `null`; pipeline PRs can be merged by actors other than the Optic App (R3 auto-merge shadow observed on PR #219, where `merged_by: github-actions[bot]`). Arc goal is `merged_by = brott-studio-optic[bot]` on all pipeline PRs.
- **Admin-PAT uses observed in S18.1 (evidence for #224):**
  - PR #221 — AC-1 formal proof throwaway (deliberate probe, intended bypass).
  - PR #223 — S18.1 close-out amendment (docs-only plan PR that couldn't satisfy `Optic Verified`; operationally required, structurally unavoidable pre-S18.2 O1-B). Second data point that confirms S18.4 scope correctly captures the real bypass surface.

### To S18.2 (self-sufficiency)

- **Planning-PR audit-gate CI check (O1 Option B) → [#226](https://github.com/brott-studio/battlebrotts-v2/issues/226).** Resolution of Open Question O1 per HCD-delegated Bott decision 2026-04-21: add a CI check that fails a planning PR when the prior sprint's Specc audit file is absent from `studio-audits/main`. Carry-forward to S18.2 scope; not an S18.1 gap.

### No carry-forwards to other sub-sprints

S18.3 (cold-start validation) and S18.5 (simplification passes) inherit nothing from this audit beyond what was already in the arc docket.

---

## 5. Compliance-Reliant Process Detection (Standing Directive)

| Process | Relies on | Risk | Recommendation |
|---|---|---|---|
| `enforce_admins: false` on `main` | Admin restraint (not using PAT to bypass required checks) | **High** in theory, **Low-Med** in practice (only HCD holds admin-PAT; deliberate use on #221/#223 was sanctioned) | **Structural fix pending S18.4 (#224).** No prompt-level mitigation added in S18.1 — correct call per arc plan. |
| `restrictions: null` on `main` | Pipeline actors choosing to merge via the right App identity | **Low-Med** (auto-merge shadow observed on #219) | **Structural fix pending S18.4 (#225).** Document only, do not band-aid. |
| Close-out amendment PRs (docs-only plan updates) | Manual admin merge because `Optic Verified` cannot be satisfied by a non-build PR | **Low** (sanctioned pattern, but creates a recurring exception) | Revisit in S18.4: either (a) add a class of PR that legitimately bypasses `Optic Verified` via CODEOWNERS-style carve-out, or (b) teach Optic to post `success` on docs-only plan PRs with scope-gate validation as the proxy verdict. Log as candidate for S18.4/S18.5 discussion; do NOT file as issue yet — design decision not ripe. |
| Planning-PR audit-gate (pre-#226) | Riv/Ett prompt-level self-check (studio-framework PR #20) | **Low** in current form (prompt-level is working), **Medium** long-term (one prompt regression re-opens the breach) | **Structural fix pending S18.2 (#226).** |

**Net assessment:** all compliance-reliant surfaces identified this sprint are already docketed for structural closure in the correct sub-sprint. No prompt-convention band-aids were introduced. This is the pattern we want.

---

## 6. Learning Extraction (Standing Directive)

Reviewed PR bodies, plan amendments, and evidence trails for S18.1. Three patterns worth extracting:

### 6.1 Per-agent GitHub App identities as structural auth boundary

Already captured in `docs/kb/per-agent-github-apps.md` (existing entry). S18.1 is the first sub-sprint where the pattern is deployed end-to-end for two agents (Optic + Boltz) beyond the Specc pilot from S16.2. **KB entry already exists — no new entry needed.** Recommend Nutts/Bott update the existing entry with a "deployment history" footer at next touch so future-us can see the progression (Specc S16.2 → Optic+Boltz S18.1).

### 6.2 Narrow-read AC interpretation as a legitimate grading tool

The S18.1 close-out invoked a narrow-read of AC-1 (via Bott decision 2026-04-21) to separate "pipeline-actor bypass" (structurally fixed this sprint) from "admin-PAT bypass" (deferred to S18.4 per arc plan). This is the first time I've audited a sprint that explicitly split an AC this way at close-out. **New pattern worth a KB entry** — propose `docs/kb/narrow-read-ac-interpretation.md` to codify: when an AC spans multiple actor classes, document the narrow read in the sprint's close-out residuals, cite the authorizing decision, and grade the narrow read PASS while carrying the broader residual forward. Filing this as a KB recommendation only — the entry itself can land in S18.2 alongside O1-B; filing one now would just be another docs-only PR that needs the admin-PAT bypass.

### 6.3 Docs-only plan PRs and the `Optic Verified` floor

PR #223's merge path revealed a structural edge: a docs-only amendment to a sprint plan has no build artifact for Optic to verify, so the required check cannot be satisfied by the normal pipeline. This is not a bug in S18.1 — the required check was correctly scoped to pipeline artifacts — but it's a pattern we'll keep hitting. Already captured above in §5 as a design question for S18.4/S18.5. **No KB entry yet** — design decision is not ripe; an entry now would calcify a pattern we might deliberately replace.

---

## 7. KB Quality Audit (Standing Directive)

- `docs/kb/per-agent-github-apps.md` — **relevant and current.** S18.1 deployed two new Apps following the setup steps documented there. Recommend adding a "deployment history" footer at next touch (see §6.1) but no blocker.
- `docs/kb/shared-token-self-review-422.md` — **resolved by this sprint for cross-actor flow.** Recommend marking resolution status at top-of-file at next touch: "cross-actor flow resolved by per-agent Apps (S18.1); same-actor 422 remains platform-level, permanent."
- No other KB entries touched by this sprint's evidence trail. KB is in good shape; `docs/kb/` continues to be the right surface for these learnings.

---

## 8. System-level audit

**`openclaw tasks audit`:** 33 findings — 4 errors (`stale_running` on tasks 4-5 days old), 29 warnings (28 `inconsistent_timestamps`, 1 `delivery_failed`). None of the stale/failed entries correlate with S18.1 subagent runs (timestamps predate the S18.1 window by 4-5 days). Operational health during S18.1 itself is clean; the stale-running findings are pre-existing gateway hygiene concerns and are not S18.1-attributable. **No action from this audit**; flagging for Bott to route to the right hygiene pass outside the sprint loop.

**Build set pipeline ordering:** planning PR (#218) → Nutts/Boltz framework wiring (studio-framework PR #22, merged by `brott-studio-boltz[bot]`) → throwaway validations (#219, #221, #222) → close-out amendment (#223). Ordering is correct; plan landed before build, build landed before validation, validation landed before close-out.

---

## 9. Exit criteria (from sprint plan)

- [x] AC-1..AC-6 satisfied and evidenced *(AC-1 narrow-read; see §3.1)*.
- [x] `sprint-18.1.md` status flipped `Planning` → `Complete` at close-out; exit checkboxes ticked; carry-forwards listed.
- [x] **Specc audit for S18.1 lands on `studio-audits/main` before S18.2 planning PR opens** *(this file).*
- [x] No regressions in existing required checks on `battlebrotts-v2:main`.

All exit criteria met.

---

## 10. 🎭 Role Performance

**Gizmo:** Shining: arc-opening review refined S18.2 scope (identified ~50% of the self-sufficiency docket items were already complete on `main`, reducing S18.2 to three real remaining items) and flagged the two-part S17.1-005 breach structure that drove O1. Struggling: nothing surfaced this sprint — appropriately front-loaded at arc-open and then stood down. Trend: ↑.

**Ett:** Shining: sprint plan is unusually rigorous — explicit Risks (R1–R5), explicit Out-of-scope mapped to downstream sub-sprints, clean task-ID → source-issue references (#210), and a Sub-sprint shape reminder that preserves arc-level context for future sub-sprints. Struggling: the plan left O1 open deliberately (correct call) but didn't articulate the narrow-read-AC-1 scenario — that ended up being resolved by Bott at close-out rather than pre-scripted in the plan. Minor, not a fault. Trend: →.

**Nutts:** Shining: infra-only framework PR (studio-framework #22, +93/-1 across 5 files) lands all the doc/profile wiring in a single focused PR with a clean PR body mapping each task ID to each file touched. Correct actor on `merged_by` (brott-studio-boltz[bot]). Struggling: nothing this sprint. Trend: ↑ (this is the Patch-fold-into-Nutts-with-infra-tag working as designed from S18.5's §5a preview).

**Boltz:** Shining: PR #22 on studio-framework merged under `brott-studio-boltz[bot]` — first production merge under the Boltz App identity, proving AC-2 end-to-end on a real PR, not just the throwaway. PR #219 cross-actor review also came back HTTP 200 as specified. Struggling: same-actor 422 remains unfixable at this layer (documented, not a Boltz fault). Trend: ↑.

**Optic:** Shining: check-run posting flow landed and is now the structural gate on `main` (app_id 3459479 wired as required). On the throwaway-PR gate test, Optic's check posted correctly and the gate held on #222's pre-post attempt. Struggling: check-run doesn't post on docs-only plan PRs (by design — no build artifact to verify), which forces the admin-PAT path on PR #223. That's a plan-level edge the arc will need to address in S18.4/S18.5, not a fault. Trend: ↑.

**Riv:** Shining: orchestrated the throwaway-PR validation sequence (#222 probe → confirmed block → #219 cross-actor proof → #221 formal post-008 proof) without scope leakage, and correctly ordered S18.1-008 after S18.1-007 per R2. Struggling: nothing pipeline-attributable. Trend: →.

---

## 11. Closing note

S18.1 is the first sub-sprint of a framework arc, and frameworks are judged on whether the *structural* change held. It did. The `Optic Verified` gate is live, bound to a distinct App identity, and blocks pipeline-actor bypasses at the protocol layer. The two loose ends — admin bypass and docs-only close-out merges — are deliberate S18.4 scope, filed as issues, and covered by the narrow-read AC-1 interpretation authorized 2026-04-21. No residuals are "silent" carries.

Recommend Ett proceed with S18.2 planning; the audit-gate discipline is satisfied by this file landing on `studio-audits/main` ahead of the S18.2 planning PR.

---

*Auditor: Specc (`brott-studio-specc[bot]`, App ID `3444613`). Audit filed to `brott-studio/studio-audits:main` per pipeline gate.*
