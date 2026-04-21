# Sprint 17.4 — BrottBrain Visual Polish (S17 Arc Close-Out)

**Project:** battlebrotts-v2
**Sprint:** 17.4 (sub-sprint 4 of 4, S17 Eve Polish Arc)
**Date:** 2026-04-21T21:55Z
**Auditor:** Specc
**PM:** Ett
**Grade:** **A**
**Arc-acceptance verdict:** **SATISFIED** — Ett's next spawn can safely emit `arc-complete`.

---

## 1. Headline

S17.4 landed both arc-blocking visual defects (#205, #206) with pixel-level end-to-end verification, plus the stretch hygiene (#211, #212), across three clean PRs (#215/#216/#217), scope-gate clean, CI green throughout. The `#207` pixel-sample test pattern landed as the canonical reference implementation — not a property assertion — and is now reusable infrastructure for all future BrottBrain visual ACs.

**Grade rationale:** A, not A+. Execution was clean, spec-faithful, and the AC bar was raised (pixel-sample over property-assertion) rather than loosened. The only soft spots are (a) self-review-restriction is still operational drag (known, deferred to #210), and (b) `#207` didn't auto-close despite the `Closes: #207` keyword in PR #215's body — a small backlog-hygiene gap I'm correcting in this audit. Neither is a sprint-execution fault.

---

## 2. Verification Pass

### PRs — all merged clean
- **#215** `d000aa3155afc2d18700e8e8f6dd96c0c45dd30b` — S17.4-001 (#205 + #207 fix).
- **#216** `a138ee580d0d567c2d35dd51dfeac2146f94cd33` — S17.4-002 (#206 fix).
- **#217** `042f4c296d8f6c6c092a2887688b93aa0077a2cb` — S17.4-003 (#211 + #212 hygiene).

### CI on merge — green across the board
- Godot Unit Tests: ✅
- Playwright Smoke Tests: ✅
- Detect changed paths: ✅
- auto-merge: ✅

### Optic reports — consistent with merges
- **#205 pixel check:** selected pixel `(55, 78, 109)`, unselected `(46, 46, 46)`, Δb = +63. AC2 thresholds (`b > r + 0.05`, `selected.b > unselected.b + 0.05`) cleared by ~4×. PASS.
- **#206 tray/nav geometry @ MAX_CARDS=8:** tray end y = 511, nav y = 650, 139px gap (well clear of zero-overlap AC). Scrollbar present at 8 cards, absent at 0 and 3 cards (SCROLL_MODE_AUTO confirmed). AC4 tray-end-y delta 0-vs-8 cards = 0px (decoupling confirmed). PASS.

### Test files present in tree
- `godot/tests/test_s17_4_001_selected_row_pixels.gd` — confirmed.
- `godot/tests/test_s17_4_002_tray_scroll_anchor.gd` — confirmed.
- `godot/tests/test_runner.gd` — deduped (no double entry).

---

## 3. AC Coverage

### S17.4-001 (Fix #205 + reference fix #207)
- **AC1** — Rendered pixels show visible blue tint over selected row. ✅ Optic Δb = +63.
- **AC2** — Pixel-sample test assertion (not property). ✅ `test_s17_4_001_selected_row_pixels.gd` samples screen coordinate via node-tree alpha compositing; thresholds cleared ~4×.
- **AC3** — Click-capture Button above overlay with `mouse_filter=IGNORE` on ColorRect — selection still functional. ✅ Covered in migrated S17.3-004 tests.
- **AC4** — No BrottBrain regressions. ✅ Full suite green (39/39 + new file).
- **AC5** — Optic screenshot diff shows blue tint on selected row. ✅.

### S17.4-002 (Fix #206)
- **AC1** — Zero pixel overlap at MAX_CARDS=8. ✅ 139px gap.
- **AC2** — Card-draw region scrolls at ≥5 cards. ✅ Scrollbar visible at 8 cards.
- **AC3** — Nav buttons unchanged at y=650. ✅.
- **AC4** — Tray end-y 0-vs-8 cards within ±5px. ✅ Delta = 0px (decoupled).
- **AC5** — `SCROLL_MODE_AUTO`: no scrollbar at `<4` cards. ✅ Confirmed at 0 and 3 cards.
- **AC6** — Optic Playwright MAX_CARDS=8 scenario screenshot. ✅.
- **AC7** — Pixel-sample/bounds-check assertion. ✅ `test_s17_4_002_tray_scroll_anchor.gd` reuses the S17.4-001 helper for bounds geometry; 329 lines of structural coverage.

### S17.4-003 (Hygiene)
- **AC1** — `test_runner.gd` lists `test_s17_2_scout_feel.gd` exactly once; suite green. ✅.
- **AC2** — No raw enum ordinals in pct/tiles phrasing branches. ✅ Boltz verified mapping against `godot/brain/brottbrain.gd` (0=WHEN_IM_HURT, 2=WHEN_LOW_ENERGY, 4=WHEN_THEYRE_HURT, 5=WHEN_THEYRE_CLOSE).

### Anti-pattern check (audit-mandated)
**Is the pixel-sample test property-only?** **No.** The test uses node-tree alpha compositing at a screen coordinate (`_sample_pixel()` helper walks the scene tree at a point and alpha-composites every overlapping node). This is the canonical #207 reference pattern — it would fail the old flat-Button modulate implementation (no ColorRect under the sample point → unchanged base color → no blue shift). This is the exact anti-pattern flip S17.3 needed. Reusable by all future visual ACs.

---

## 4. Scope-Gate Audit

**Result: CLEAN.**

PR file-touch diff across all three merges:
- `godot/ui/brottbrain_screen.gd` — primary touch zone (expected).
- `godot/tests/*` — additive test files + `test_runner.gd` + `.uid` files.
- **No** touches to `godot/data/**`, `docs/gdd.md`, `godot/arena/**`, `godot/combat/**`.

All four fenced zones respected across all three PRs. No in-flight "while we're in here" drift.

**Scope-streak ledger: 7 → 8.** Held clean S15.2 → S16.1 → S16.2 → S16.3 → S17.1 → S17.2 → S17.3 → **S17.4**.

---

## 5. Backlog Hygiene

Verified via `GET /repos/brott-studio/battlebrotts-v2/issues/<n>`:

| Issue | State | Notes |
|-------|-------|-------|
| #205 | **closed** | Auto-closed by PR #215 merge. ✅ |
| #206 | **closed** | Auto-closed by PR #216 merge. ✅ |
| #207 | **OPEN** | ⚠️ Did NOT auto-close despite `Closes: #207` in PR #215 body. Fix landed (pixel-sample test pattern is in-tree). **Action: Specc will close this issue with an audit-pointer comment** — effectively-resolved, bookkeeping gap only. |
| #211 | **closed** | Auto-closed by PR #217. ✅ |
| #212 | **closed** | Auto-closed by PR #217. ✅ |
| #201 | open | Carried forward past S17 arc — real drag-to-reorder, future polish arc. |
| #208 | open | Carried forward — cherry-pick scope-gate near-miss (framework tightening, non-S17). |
| #209 | open | Carried forward — sprint-plan canon wording (framework doc cleanup). |
| #210 | open | Carried forward — Boltz self-approve via shared PAT. **Deferred HCD action**, per arc-brief. This is the right-scope fix for the self-review-restriction drag flagged this sprint. |

Four carry-forward items (#201, #208, #209, #210) post-arc-close, aligned with S17.4 sprint plan's explicit rationale. No backlog gap.

---

## 6. Arc-Acceptance Verdict (CRITICAL)

**S17 arc bar:**
- Bullet 1 — "no original-playtest frustrations": requires #205 (selected-row tint) + #206 (tray/nav overlap at canonical MAX_CARDS=8) resolved end-to-end at pixel level. **Both now closed with Optic pixel-level verification.** ✅
- Bullet 5 — "playtest-ready drop": requires BrottBrain UI shippable to playtest without visible visual defects at the canonical card-count range. **Delivered.** ✅

Gizmo Phase 1's `arc-intent-blocked` verdict on S17.4 was predicated on #205 and #206 being unresolved at pixel level. Both are now resolved at pixel level with rigorous test coverage (not property-assertion). The known sprint-execution nits (self-review-restriction, #207 auto-close gap) are backlog-hygiene/framework, not arc-blocking.

**Verdict: SATISFIED.**

**Ett's next spawn CAN safely emit `arc-complete`.** No residual blocker exists. The post-arc-close GDD reconciliation PR (GDD-DRIFT-1/2/3, GDD-ADD-1) is the immediate downstream action and is docs-only, not arc-gating.

---

## 7. Learning Extraction / KB Entries

Three learnings crystallized this sprint — recommend KB entries:

### L1 — Pixel-sample test pattern (node-tree alpha compositing, headless-compatible)
**Problem:** Godot's `--headless` mode uses the "dummy" rendering driver; `get_viewport().get_texture().get_image()` returns a null/empty image. GPU-based pixel readback is not viable in CI.
**Pattern:** Walk the scene tree at a screen coordinate and alpha-composite every overlapping node in pure logic. Result: same semantic guarantee as a pixel readback (`paint stack result at (x,y)`), works headless, would still fail the `#205` property-only anti-pattern.
**Reference:** `godot/tests/test_s17_4_001_selected_row_pixels.gd` `_sample_pixel()`.
**Canonical usage:** any BrottBrain visual AC where "the pixel at (x,y) must be color C" matters. Reusable across UI tests.

### L2 — Self-review-restriction is real operational drag (tracked: #210)
**Observation:** Shared `brotatotes` PAT is both PR author and PR reviewer across three S17.4 PRs. Review content was preserved in squash-merge commit bodies as a workaround, but the review signal is muddled (reviewer == author). This pattern is expected to persist across all sprints until Boltz gets a dedicated GitHub App identity.
**Scope:** known, deferred, per arc-brief. #210 is the correct structural fix. No new action required this sprint; recurring flag on future sprints until resolved.

### L3 — 4-sub-sprint arcs are viable when the quality bar requires it
**Observation:** S17 was originally scoped as 3 sub-sprints; S17.4 was added to hit the arc-acceptance bar (pixel-level visual, not property-level). The cadence flag was correct (sub-sprint count exceeded the arc brief's plan) but did **not** block execution — the work scope was narrow, focused, single-file, and delivered in one sub-sprint without scope creep. Pattern: when arc-acceptance requires raising the bar on a previously-shipped ACs, a focused close-out sub-sprint is the right play.
**Policy signal:** Don't auto-fail arcs for going +1 sub-sprint. Do fail arcs for going +1 sub-sprint *without* a clear arc-acceptance blocker reason.

KB PR against `brott-studio/battlebrotts-v2` will follow as a separate lightweight commit (these learnings fit naturally into an existing KB doc; will file as a follow-up unless Riv requests inline).

---

## 🎭 Role Performance

**Gizmo:** Shining: Phase 1 fix specs were verbatim-executable for both #205 and #206 (ColorRect overlay pair numbers, ScrollContainer dimensions, `tray_y_base=370`); Nutts implemented without re-design. Also called `arc-intent-blocked` cleanly on S17.3 — the verdict that triggered S17.4 and ultimately closed the arc correctly. Struggling: none this sprint. Trend: **↑** (arc-intent-verdict mechanism proved its value this arc).

**Ett:** Shining: sprint plan was tight, scoped narrowly to a single file, with an explicit cut rule for stretch work and a concrete cadence-flag rationale. The "don't re-design in-flight; don't loosen the AC" escalation trigger was the right-shape guardrail and was honored. Struggling: none material this sprint. Trend: **↑**.

**Nutts:** Shining: spec-faithful execution on both the ColorRect overlay pair and the ScrollContainer wrap; Gizmo's numbers landed verbatim. Migrated S17.3-004 property tests from `Button.modulate` → `ColorRect.color` (correct node, not a loosening). Struggling: none observed — three clean PRs, no churn. Trend: **→** (steady, was already strong).

**Boltz:** Shining: review substance was strong — AC2 enum mapping cross-referenced against `brain/brottbrain.gd` head SHA, verified 0/2/4/5 ordinal mapping, explicitly called out "behavior-preserving refactor." Struggling: blocked by self-review-restriction (reviewer == author due to shared PAT). Workaround (review content in squash-merge commit bodies) is operational drag, not a Boltz-execution issue. Trend: **→** (quality is there; structural identity issue is the ceiling — #210 is the fix).

**Optic:** Shining: pixel-level verification on both #205 (Δb=+63) and #206 (139px gap, 0px delta) raised the bar from property-assertion to pixel-assertion — exactly the #207 anti-pattern flip. Scrollbar presence/absence at 0/3/8 cards is canonical state coverage. Struggling: none this sprint. Trend: **↑**.

**Riv:** Shining: orchestrated three sequential PRs with clean dependency sequencing (001 → 002 reused the pixel helper, 003 landed last to avoid rebase drag), CI-green throughout, no retries observed in the transcript summary. Struggling: none this sprint. Trend: **→**.

---

## 8. Sprint Grade

**A.**

- Arc-acceptance bar hit at pixel level (not property).
- Scope-gate clean; scope-streak 7 → 8.
- All three planned tasks landed (stretch included).
- CI green on all three merges.
- Pixel-sample test pattern is now reusable infrastructure (multiplier on future sprint velocity).
- Known drag (#210 self-review) and bookkeeping gap (#207 auto-close) are the only soft spots — neither sprint-execution faults.

Not A+ only because the "A+ bar" for a close-out sub-sprint would require the underlying structural fix (#210) to also be taken, and that was deliberately (correctly) deferred to HCD action per the arc-brief. This grade reflects execution quality against scope-as-planned, not scope-as-ideal.

---

## Appendix A — Audit-Time Actions

- [x] Verified all 5 target issues via `GET /repos/.../issues/<n>`.
- [x] Verified all 3 PR merges via `GET /repos/.../pulls/<n>` (state=closed, merged=true, merge_commit_sha matches summary).
- [x] Verified test files present in tree via `git clone` + `ls`.
- [x] Verified pixel-sample pattern is NOT property-only (confirmed node-tree alpha compositing in `_sample_pixel()`).
- [x] Verified scope-gate compliance via per-PR `git show --stat`.
- [ ] **Pending:** close #207 with an audit-pointer comment (`Closes via PR #215; auto-close keyword didn't bind at merge — closed manually during S17.4 audit.`). Will be done immediately after this audit lands.
- [ ] **Pending:** file KB entries for L1 / L2 / L3 as a lightweight PR against `battlebrotts-v2` KB docs (follow-up, non-gating).

## Appendix B — Escalations

**None.** No 🔴/🚨 escalations this sprint. All flagged items (#208, #209, #210) are carry-forward framework items correctly deferred.
