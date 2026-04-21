# Overnight Handoff — 2026-04-21

**Shift:** 2026-04-20 ~20:30 UTC → 2026-04-21 ~09:30 UTC
**Driver (final leg):** Riv
**Status at handoff:** S17.1 closed; S17.2 mostly landed; S17.2-003 escalated to HCD; arc-complete pending.

---

## 1. Arc State Snapshot

| Unit | Status | Notes |
|------|--------|-------|
| **S17.1** (Shop/Loadout/Event UX) | ✅ **Closed** | All 6 tasks merged + verified. Retroactive Specc audit merged (studio-audits #11, grade **B+**). |
| **S17.2-001** (wall-stuck investigation) | ✅ Merged (#181) | |
| **S17.2-002** (wall-stuck fix) | ✅ Merged (#182) + verify (#183) | |
| **S17.2-003** (scout feel) | 🟡 **Escalated to HCD** | 3 Nutts impl attempts + 1 Gizmo tuning pass failed to hit Scout mirror WR target band. Structural, not tuning. Code PR #188 + Riv decision PR #189 open. Spec revisions #184 + #187 merged. |
| **S17.2-004** (velocity debug overlay, dev-only) | 🟡 PR #190 open, auto-merge armed | Blocked on required approving review (studio-lead-dev sweep pending). See §4. |
| **S17.2 close-out audit** (Specc) | ⏸ **Blocked** on S17.2-003 disposition |
| **S17.3** | ⏸ Not started |
| **S17 arc-complete** | ⏸ **Blocked** on S17.2 close-out |

---

## 2. Open PRs Table

### brott-studio/battlebrotts-v2

| # | Title | State | Action needed | Decides |
|---|-------|-------|---------------|---------|
| **190** | [S17.2-004] Dev-only velocity debug overlay | open, auto-merge armed, `mergeable_state=blocked` | Required approving review (no reviewer assigned; studio-lead-dev[bot] has auto-approved prior pipeline PRs at 08:19 UTC in sweeps). If not auto-approved by next sweep, HCD can merge manually — it's dev-only, OFF by default, very low risk. | studio-lead-dev sweep / HCD |
| **189** | Riv's Decision: defer S17.2-003 to S17.3 | open | **HCD disposition**: accept defer vs scope-down vs accept current impl | HCD |
| **188** | [S17.2-003] Scout feel code PR | open | Tied to #189; holds pending disposition | HCD |
| 177 | (non-S17.2 chore/docket) | open | Leave for HCD triage | HCD |
| 173 | (non-S17.2 chore/docket) | open | Leave for HCD triage | HCD |
| 152 | (non-S17.2 chore/docket) | open | Leave for HCD triage | HCD |

### Other repos

- All studio-audits, studio-framework, brott-studio.github.io PRs from the shift are merged. No handoff items.

---

## 3. HCD Decisions Required (Morning Review)

1. **🔴 S17.2-003 disposition (#189).** Primary blocker for S17.2 close-out and arc-complete. Options as framed by Riv in PR #189:
   - **A. Accept defer to S17.3** (Riv's recommendation): escalate to a fresh sub-sprint with spec-level rework since the issue is structural, not tuning.
   - **B. Scope down in-place**: accept AC-T3 relaxation, re-tune with current architecture, close S17.2-003 as-is.
   - **C. Accept current impl**: declare current Scout feel "good enough" and ship.
2. **PR #190 merge disposition.** If the studio-lead-dev sweep hasn't auto-approved by the time HCD reviews, decide: manual approve + merge, or wait. Low-risk (dev-flag-gated, OFF by default).
3. **Triage PRs #177, #173, #152.** Non-S17.2 chores/dockets that predate this shift.

---

## 4. Framework Option A Validation — PENDING

studio-framework #20 landed the Phase 3e sub-sprint audit-gate enforcement (fix(pipeline): enforce sub-sprint audit close-out in Riv and Ett). **This new rule has NOT been exercised yet** in an actual close-out, because:

- S17.1 close-out happened *before* #20 landed → retroactive audit ran after the fact (studio-audits #11, which itself was the first validation event, but the *gate* wasn't in front of Riv during that close-out).
- S17.2 close-out is blocked on HCD's S17.2-003 disposition, so the gate has not yet been invoked live.

**Next opportunity to validate:** whenever HCD unblocks S17.2-003 and Riv runs S17.2 close-out, Phase 3e should require the Specc audit commit on studio-audits/main *before* Riv can mark the sub-sprint closed. Watch for this being exercised correctly.

---

## 5. Timeline of the Night (UTC)

### Phase 1 — S17.1 shop/loadout/event UX polish (20:30 → 23:53)

- 20:32 studio-framework #12 — PIPELINE rule: require audit file on studio-audits/main before sub-sprint close
- 20:33 v2 #155 — KB extension: per-agent-apps reviewer-roles-readiness note
- 21:22 v2 #156 — S17 Eve Polish Arc brief
- 21:28 v2 #157 — S17.1 sub-sprint plan
- 21:43 → 23:07 v2 #158–#163 — S17.1-001 (shop scroll) + S17.1-002 (Loadout overlap) design → fix → verify
- 23:00 → 23:17 v2 #164, #165 — S17.1-003 visible tooltips + energy legend design + fix
- 23:23 → 23:37 v2 #167, #168 — S17.1-004 first-encounter HUD design + impl
- 23:42 → 23:53 v2 #170, #171 — S17.1-005 random-event popup design + impl

### Phase 2 — S17.1 close-out + S17.2 kickoff (02:07 → 05:51)

- 02:07 → 02:17 v2 #174, #175, #176 — S17.1-006 first-run crate design + impl + verify
- 02:17 v2 #172 — S17.1-005 verify (post-hoc)
- 03:01 v2 #178 — S17.2 Spec: scout feel — nimble, not magical
- 04:39 → 05:01 v2 #181, #182, #183 — S17.2-001 (investigation) + S17.2-002 (wall-stuck fix + verify)
- 04:47 → 05:01 studio-framework #14–#17 — decide-first rule for Ett; the-bott profile; no-channel-post rule for Riv; housekeeping auto-merge rule
- 05:50 → 05:51 studio-framework #18, #19 + v2 #185, #186 — dashboard retirement + README redirects to public site

### Phase 3 — Site polish (06:06 → 08:05)

- 06:06 → 06:26 site #2–#10 — Astro scaffold, homepage mission, gallery, Treasure Mountain page, rainbow polish, loop diagram upgrade
- 07:20 → 08:05 site #11–#17 — merge team cards into pipeline diagram, agent card rewrites, emoji disambiguation, per-node polish, agent count fix

### Phase 4 — S17.2 push + Framework Option A (07:52 → 08:41)

- 07:52 studio-framework #20 — **Option A**: Phase 3e sub-sprint audit-gate enforcement in Riv + Ett
- 08:11 studio-audits #11 — **S17.1 retroactive audit (grade B+)**
- 08:19 → 08:24 v2 #166, #169, #179 — S17.1-003/004 Verify + S17.2 plan reconciled (studio-lead-dev sweep approvals)
- 08:20 → 08:41 v2 #184, #187 — S17.2-003 spec revision + revision #2 (AC-T3 tension resolved; merged by brotatotes)

### Phase 5 — S17.2-004 + Riv escalation + handoff (08:41 → 09:30)

- ~08:45 v2 #188 — S17.2-003 code PR (held)
- ~08:50 v2 #189 — Riv decision: defer S17.2-003 to S17.3 (awaits HCD)
- ~09:00 v2 #190 — S17.2-004 velocity debug overlay (auto-merge armed, awaiting review sweep)
- 09:12 Handoff run begins (Riv final leg)

---

## 6. Open Questions for HCD's Morning Review

1. **S17.2-003 disposition** — which of A/B/C above? (Primary blocker.)
2. **PR #190** — manual approve + merge if studio-lead-dev sweep hasn't fired, or wait?
3. **When S17.2-003 lands**, should Specc run S17.2 close-out audit immediately, or batch it with S17 arc-complete retrospective?
4. **Framework #20 Phase 3e** — should we add a dry-run / self-test to validate the gate before relying on it live? Or let it exercise naturally on next close-out?
5. **Triage**: PRs #177, #173, #152 — close, keep, or re-scope?

---

## 7. What This Run Did NOT Do (by design)

- ❌ **Did NOT run Specc close-out for S17.2.** Gated on S17.2-003 disposition; HCD's call.
- ❌ **Did NOT mark S17 arc-complete.** Depends on S17.2 close-out.
- ❌ **Did NOT override #189.** HCD escalation stays open for disposition.
- ❌ **Did NOT post to Discord.** Morning digest email at 12:00 UTC per guardrails.

---

_Prepared by Riv (S17 arc driver, final leg) — 2026-04-21 ~09:30 UTC._
