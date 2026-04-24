# Sub-Sprint Audit — S21.5 (Silent → Shipped)

**Sub-sprint:** S21.5
**Arc:** Arc B — Content & Feel
**Date:** 2026-04-24T04:21Z
**Grade:** **A−**
**PR:** [brott-studio/battlebrotts-v2#261](https://github.com/brott-studio/battlebrotts-v2/pull/261)
**Merge SHA on `main`:** `377fd088f22234834635e69b751fa1da9562c50b` (squash-merged 2026-04-24T04:14:54Z by Boltz bot)
**Branch:** `feat/s21.5-audio-foundation` (deleted post-merge)
**Idempotency key:** `sprint-21.5`
**Arc:** Final sub-sprint — see Arc B close-out section below.

---

## One-line rationale

S21.5 delivers BattleBrotts' first audio infrastructure from a standing start: 3-bus layout, 2 SFX hooks, mute toggle with persist — all in 419 lines within budget, 4 tests, 994-assertion full suite passing, zero regressions. Boltz caught a real latent gap (mute not applied on canonical game flow) pre-merge via a tight fix loop; Optic confirmed I1–I5 clean and flagged one pre-existing S13.5 bus-routing debt as carry-forward. The sole grade-drag from A to A− is the sfxr audio fallback: procedurally synthesized assets are technically correct but subjectively unreviewed — audio character is unknown until human playtest.

---

## Scope

### In scope (per Ett brief + Gizmo framing, 2026-04-24T03:51–03:55Z)

- **3-bus AudioServer layout:** Master (bus 0, 0dB), SFX (bus 1, 0dB, send=Master), Music (bus 2, −6dB, send=Master). Wired via `default_bus_layout.tres` resource (Godot 4.4 convention; Gizmo caught this during framing).
- **Two CC0 OGG SFX assets:** `win_chime.ogg` (victory) and `popup_whoosh.ogg` (random-event popup), both explicitly routed to SFX bus.
- **Match-win chime:** `ResultScreen.setup()`, victory-only, guarded by `_chime_played` flag (no double-fire).
- **Popup whoosh:** `game_main.show_random_event()`, fires after S21.4 dampening + duplicate guards, long-lived player (no leaks).
- **Mute toggle:** `FirstRunState` gains `[settings]` section with `get/set_audio_muted()`; `_apply_audio_settings()` applied at `_ready()` in both `main.gd` and `game_main.gd` (canonical flow).
- **4 tests** covering I1–I4.
- **Attribution log:** `res://assets/audio/sfx/ATTRIBUTION.md` documenting CC0 status, sfxr seeds, and synthesis params.

### NOT in scope (explicit brief exclusions)

- Music loops / ambient audio
- Combat SFX (weapons, hits, AI actions)
- Mixer UI (volume sliders, mute checkbox)
- Voice lines
- UI click SFX
- Silver/Gold audio content

---

## Invariants — S21.5

| ID | Invariant (verbatim) | Result | Evidence |
|----|----------------------|--------|----------|
| I1 | Audio bus layout has exactly 3 buses in order: Master (bus 0, 0dB), SFX (bus 1, 0dB, send=Master), Music (bus 2, −6dB, send=Master). | **PASS** | `test_s21_5_001_audio_bus_layout.gd` — 13 assertions. Boltz verified `default_bus_layout.tres` + `project.godot [audio]`. Optic runtime confirm. |
| I2 | Two OGG assets present at `res://assets/audio/sfx/`: `win_chime.ogg` and `popup_whoosh.ogg`. Attribution log at `res://assets/audio/sfx/ATTRIBUTION.md`. | **PASS** | `test_s21_5_002_audio_assets.gd` — 9 assertions (file-exists + size sanity + `.import` sidecar presence). Boltz confirmed `.import` in `.gitignore`, zero committed `.import` files repo-wide. Optic runtime confirm. |
| I3 | Both SFX AudioStreamPlayer nodes explicitly route to bus "SFX" (not "Master", not default). | **PASS** | `test_s21_5_003_sfx_routing.gd` — 4 assertions. `result_screen.gd:40` (`WinChimePlayer.bus = "SFX"`) and `game_main.gd:530` (`PopupWhooshPlayer.bus = "SFX"`) verified by Boltz review. Optic runtime confirm. Note: headless test emits `ERROR: Playback can only happen when a node is inside the scene tree` log noise; assertions on `.bus` still pass (4/4) — cosmetic only, not a failure. |
| I4 | Mute toggle applied at Master-bus level: `FirstRunState.set_audio_muted(true)` → `AudioServer.is_bus_mute(0) == true` after init hook. Conversely false → false. Persisted across game restart via `FirstRunState` ConfigFile `[settings]` section. | **PASS** | `test_s21_5_004_mute_toggle.gd` — 5 assertions. Initial Nutts build only wired `_apply_audio_settings()` in `main.gd` (demo route); Boltz review caught gap in `game_main.gd` (canonical flow). Fixed in commit `fa2c1143`. Full mute cycle verified on both routes. |
| I5 | No regression — all pre-existing Godot unit tests continue to pass. Baseline: 46 files at S21.4 close. | **PASS** | 50/50 files (46 prior + 4 new S21.5), 994 assertions, 0 failed. CI run confirmed by Boltz re-review. Full-run log shows real assertion counts (13 + 9 + 4 + 5 = 31 new asserts), no silent-0 files. |
| I6 | No combat-SFX creep — grep of `combat/weapons/ai` code for `AudioStreamPlayer` / `play_sfx` / `play_sound` returns zero matches. | **PARTIAL** (pre-existing debt only) | PR body scope-fence grep receipt: zero matches in combat/weapons/AI code — **S21.5 introduced zero combat-SFX creep.** Optic flagged one pre-existing instance: `shop_screen.gd:73` `_play_sfx()` helper (S13.5 code) creates `AudioStreamPlayer` without `.bus` assignment. Not in scope for S21.5; formalized as carry-forward issue #262. I6 is PASS for S21.5-introduced code; PARTIAL only for pre-existing debt. |

---

## Pipeline flow

| Stage | Agent | Verdict | Notes |
|-------|-------|---------|-------|
| **Phase 0** | Riv | Audit-gate PASS | S21.4 audit present on `studio-audits/main`. |
| **Ett ruling** | Ett | RULING A — CONTINUE | 2026-04-24T03:51Z. Confirmed audio foundation as the final Arc B scope-seed item. Brief: 3-bus, 2 SFX, mute toggle, explicit NOT-list, invariants I1–I6, ≤500 lines. |
| **Gizmo framing** | Gizmo | Zero questions surfaced | 2026-04-24T03:55Z. Grounded in `docs/kb/audio-vision.md` (WALL-E / Thomas Newman tone). Asset sourcing spec (CC0 freesound primary + sfxr fallback). Bus config as `.tres` resource (caught Godot 4.4 convention). FirstRunState: proposed parallel `[settings]` API rather than misusing `mark_seen` (clean ruling, reversible). Code sketches for both SFX triggers. |
| **Nutts build** | Nutts | PR #261 opened | 2026-04-24T04:04Z. 92 production lines + 327 test lines = 419 total. 4 tests. B4a threshold respected (≤350 code, ≤5 tests, no Riv ping needed). Freesound primaries not accessible in build env (require auth); sfxr Python synthesis fallback with deterministic seeds (12345, 67890). ATTRIBUTION.md documented. |
| **Boltz review #1** | Boltz | CHANGES_REQUESTED | 2026-04-24T04:08Z (review `4167760097`). B1–B7 all PASS including CI-sanity assertion-count floor verification. One 🔴 required change: `_apply_audio_settings()` present in `main.gd._ready()` (demo route only) but **absent** from `game_main.gd._ready()` (canonical flow per `run/main_scene = "res://game_main.tscn"`). Latent today (no mute UI yet), but the foundation must be wired clean before mute-toggle UI lands. |
| **Nutts fix** | Nutts | Commit `fa2c1143` | 2026-04-24T04:11Z. 11 net lines (9-line `_apply_audio_settings()` function + 1 call site in `_ready()` + 1 blank). Duplicate approach (rejected helper-extraction as over-engineering for one sprint — correct call). Implementation comment explains "Mirrors `main.gd`." |
| **Boltz re-review + merge** | Boltz | APPROVED, auto-merged | 2026-04-24T04:14Z (review `4167791136`). Fix verified: `_apply_audio_settings()` wired in `game_main.gd._ready()` after `_connect_league_signal()` and before URL-param routing. Scope clean (11 additions, only `game_main.gd` touched). CI confirmed: 50/50 files, 994 assertions, 0 failed. |
| **Optic post-merge verify** | Optic | I1–I5 PASS, I6 PARTIAL (pre-existing) | 2026-04-24T04:20Z. R1–R4 all PASS, Godot API regression check PASS. I6 PARTIAL for `shop_screen.gd._play_sfx()` (S13.5 debt, not S21.5 code). Optic explicitly flagged for Specc to formalize as carry-forward. |

### Boltz-caught gap: the review process working correctly

The Boltz CHANGES_REQUESTED on `_apply_audio_settings()` absence is the highest-value process event of this sub-sprint. The gap was **latent** (mute toggle has no UI yet; no user-visible mute state in S21.5's scope), but Boltz traced the canonical app entry point from `project.godot:run/main_scene` and caught the missing call before it became a "why doesn't mute work" report in a future sprint. The fix was tight (11 lines), the re-review was immediate, and CI confirmed the complete invariant. This is the review discipline working as designed.

---

## Metrics

| Metric | Value |
|--------|-------|
| Production lines (PR #261) | 92 |
| Test lines (PR #261) | 327 |
| Total lines | 419 (budget: ≤500) |
| Tests (new) | 4 (budget: ≤5) |
| Test count trigger (B4a: ≤350 code, ≤5 tests) | Respected — no Riv ping needed |
| Audio assets | 2 OGG files |
| Asset synthesis | sfxr Python fallback (seeds 12345, 67890) |
| New assertions (S21.5 tests) | 31 (13 + 9 + 4 + 5) |
| Total assertions (full suite at merge) | 994 |
| CI check-runs at merge | 6/6 PASS (Godot Unit Tests, Playwright Smoke, Post Optic Verified ×2, update, Detect changed paths) |
| Regressions | 0 |
| Fix loops | 1 (Boltz CHANGES_REQUESTED → Nutts fix → Boltz APPROVE; single loop, clean) |

---

## Grade

**A−**

### Rationale

S21.5 ships a complete audio foundation from zero infra: 3-bus layout, 2 SFX hooks, mute toggle with persistence, 4 tests, 31 new assertions, 994-assertion full suite all passing. All scope seeds from the brief are closed. Zero regressions. Boltz caught a real latent gap pre-merge and the single fix loop resolved it cleanly in 11 lines. Gizmo surfaced zero framing questions — the brief was tight and actionable. I6 PARTIAL is pre-existing S13.5 debt, not an S21.5 failure.

**Grade drag from A to A−:**

1. **Sfxr-synthesized assets — subjective quality unknown.** Freesound primaries (freesound.org/s/320775/, freesound.org/s/428156/) were inaccessible in the build environment (auth required). Python sfxr synthesis with deterministic seeds is technically correct (CC0, correct file format, correct bus routing), but the audio character of the two chimes has not been human-playtested. For a sprint themed "Silent → Shipped," the structural foundation is solid — but whether the audio *feels* right to the game's WALL-E / Thomas Newman tone is unknown. This is an intentional deferral (ett's brief acknowledged it), but it's the reason the grade doesn't reach A. Filed as carry-forward #263 for human review.

2. **Boltz review caught a real gap** — this is a positive sign (review discipline working), but the gap itself (missing `game_main.gd` init hook) could have been caught during Nutts self-review. The brief and Gizmo framing both named `game_main.gd` as the canonical flow. Not grade-draining on its own (single clean fix loop is standard), but combined with point 1, holds A−.

Not graded below A− because:
- All invariants PASS at audit close (I4 fully covered on both routes post-fix)
- Scope discipline is exemplary: 419/500 lines, 4/5 tests, explicit NOT-list enforced
- I6 PARTIAL is pre-existing debt, not a scope fence violation
- Boltz B7 (no silent-0-assertion) confirmed 31 real new asserts — the S21.4 PR-B-class CI gap did not recur
- Zero regressions across 994 assertions

**Scope streak:** Arc B: S21.1 (A−), S21.2 (B+), S21.3 (A−), S21.4 (B+), S21.5 (A−). Five sub-sprints, all merging cleanly with filed carry-forwards, no arc-stopping failures. ✅

---

## Carry-forwards

All filed as GitHub issues on `brott-studio/battlebrotts-v2`:

1. **shop_screen.gd audio bus-routing debt** ([#262](https://github.com/brott-studio/battlebrotts-v2/issues/262)) — `area:audio`, `prio:mid`. `godot/ui/shop_screen.gd:73` `_play_sfx()` helper (S13.5 code, lines 76+, called from lines 536, 655, 666) creates `AudioStreamPlayer` without `.bus` assignment. Defaults to Master. Will not respond to SFX-level volume or SFX-specific mute when those ship. Fix: `_shop_audio.bus = "SFX"` after creation. Latent until mixer UI sprint.

2. **Sfxr-synthesized audio subjective review** ([#263](https://github.com/brott-studio/battlebrotts-v2/issues/263)) — `area:audio`, `prio:low`. `win_chime.ogg` (seed 12345) and `popup_whoosh.ogg` (seed 67890) are procedurally synthesized. Human playtest should evaluate audio feel against WALL-E / Thomas Newman tone. Asset swap is code-unaffecting (same paths, just replace `.ogg` files). Freesound primaries documented in ATTRIBUTION.md if reachable.

**Issue closed this sprint:**
- **#94** (`[backlog] Audio foundation — first pass`) — closed at PR #261 merge. ✅

---

## openclaw tasks audit — S21.5 sprint window

`openclaw tasks audit` run at audit time: pre-existing pattern of stale_running (5 errors from earlier arcs, ages 23h–7d+), delivery_failed (1 warning, pre-existing), inconsistent_timestamps (bulk harness clock skew, pre-existing baseline). No new task health regressions attributable to S21.5. Sentinel-sweep cron (studio-framework#44) remains the standing remediation for stale_running entries.

---

## Compliance-reliant process detection

### 1. Freesound primary access — compliance-reliant fallback

The build environment lacks access to Freesound's authenticated download API. The sfxr fallback is procedurally documented and CC0-clean, but the decision to fall back (rather than, e.g., block the sprint on asset sourcing) is compliance-reliant: Nutts made the call per Ett's ">15min stall → fallback" ruling. **Risk: LOW** (the fallback rule is clear; the subjective-quality gap is tracked in #263). No structural fix proposed; the rule is sufficient for now.

### 2. `_apply_audio_settings()` wiring in new canonical flows — compliance-reliant

The pattern of calling `_apply_audio_settings()` in `_ready()` for any new top-level entry point is currently compliance-reliant (Boltz has to remember to check for it). This sub-sprint demonstrates the risk: Nutts initially wired it only in `main.gd` (demo route), and Boltz caught the `game_main.gd` gap. **Risk: LOW** (Boltz caught it before merge — the review gate worked). **Structural fix (proposed):** add an audio-settings-wiring check to the Boltz review checklist for audio-touching PRs. Low urgency; captured here for the KB.

---

## 🎭 Role Performance

**Gizmo:** Shining: Zero framing questions on a greenfield audio sub-sprint is a high bar — Gizmo surfaced the `.tres` bus resource (Godot 4.4 convention), proposed the `[settings]` API pattern that avoids misusing `mark_seen` (correct isolation), and produced code sketches for both SFX trigger sites. Framing was tight enough that Nutts needed no mid-build spec clarification. Struggling: Nothing S21.5-specific. Trend: ↑.

**Ett:** Shining: RULING A was clean and scoped correctly — identified audio foundation as the last Arc B scope-seed item with a crisp brief (3 buses, 2 SFX, mute toggle, explicit NOT-list, ≤500 lines). The NOT-list was specific enough that Nutts honored it (no combat SFX, no music, no mixer UI shipped). Struggling: Nothing S21.5-specific. Trend: →.

**Nutts:** Shining: 419/500 lines, 4/5 tests, B4a respected, ATTRIBUTION.md documented with seeds + ffmpeg params, `_chime_played` guard + long-lived `_popup_whoosh_player` anti-leak patterns, named constants throughout. The sfxr fallback decision was correct and documented. Commit `fa2c1143` (the fix) was 11 lines and scoped to exactly the issue. Struggling: Missing `game_main.gd` init hook on initial build — both `main.gd` and `game_main.gd` were named in the framing; a self-review against the spec before PR open would have caught it. Trend: → (clean fundamentals, consistent pattern of one missed edge case per sprint caught by Boltz).

**Boltz:** Shining: B1–B7 checklist applied with genuine thoroughness — the `game_main.gd` gap catch required tracing `project.godot:run/main_scene` to identify the canonical entry point, not just reading the diff. B7 (CI-sanity assertion-count floor) explicitly verified against the raw CI log to confirm no silent-0 regression (specifically checking against the S21.4 PR-B failure mode). `.import` sidecar convention verified across the entire repo. Re-review immediate and tight. Struggling: Nothing this sub-sprint. Trend: ↑ (clearest strong Boltz performance in Arc B; B7 self-check shows learning from S21.4).

**Optic:** Shining: I1–I5 all PASS with clean evidence; I6 PARTIAL correctly attributed to pre-existing S13.5 debt rather than to S21.5 scope. Explicit escalation ("Optic flagged as carry-forward for Specc to formalize") shows Optic operating correctly as the last structural gate. R1–R4 all PASS. Godot API regression check PASS. Struggling: Playwright screenshot evidence (#247) remains open — screenshot paths not in return payload. Pre-existing issue; not a S21.5 regression. Trend: → (reliable pass/fail judgment; structural payload hardening (#247) is the standing gap).

**Riv:** Shining: The arc-loop ran cleanly to close — Phase 0 audit-gate, Gizmo, Ett, Nutts, Boltz, Optic, Specc in correct sequence. Boltz fix loop was single-cycle. No truncation events on this sub-sprint. Struggling: Nothing S21.5-specific. Trend: → (stable; S21.5 was a clean execution sprint with no orchestration stress).

---

---

## Arc B — Content & Feel — Close-Out

*Arc B is now complete. This section provides the arc-level roll-up for HCD / Ett.*

### Sub-sprint grades

| Sub-sprint | Theme | Grade | PRs | Key outcome |
|------------|-------|-------|-----|-------------|
| S21.1 | Bronze Content Drop | A− | #242 | 6 opponent templates, `unlock_league` schema, D4-leak fix. 3×Optic cycle (legitimate retries). |
| S21.2 | UX Bundle (#103/#104/#107) | B+ | #244 | T1+T2 clean; T3 design-spec divergence missed by Boltz, corrected in S21.3. Truncation events. |
| S21.3 | Arena Onboarding (#107 real payload) | A− | #251 | In-arena HUD-element overlays, arena-entry sequencing, ▲ pointer. Nutts 1800s timeout (work landed clean). |
| S21.4 | Interruption → Flow (#105/#106/#108) | B+ | #254, #255, #256, #257 | 3 UX issues closed. PR-B shipped Engine.get_ticks_msec regression, caught by Optic, hot-patched. |
| S21.5 | Silent → Shipped (audio foundation) | A− | #261 | 3-bus layout, 2 SFX, mute toggle, 4 tests. Boltz caught missing init hook pre-merge. Sfxr fallback accepted. |

### Arc-level roll-up grade: **B+**

**Rationale:** Arc B delivered all three scope-seed items cleanly:
- ✅ Bronze content (#112) — 6 archetype-coherent opponent templates, D4-leak closed
- ✅ UX bundle (#103/#104/#107) — hover tooltips eliminated, scroll wrappers, in-arena onboarding (took S21.2 + S21.3 to complete correctly)
- ✅ Audio foundation — greenfield audio infra: 3 buses, 2 SFX, mute toggle

No sub-sprint failed. No scope seed was permanently dropped. All PRs merged with CI green.

Grade held from A− to B+ arc-level by two recurring patterns across the arc:
1. **Boltz review misses (S21.2, S21.4):** Two sub-sprints shipped substantive gaps past the Boltz gate — S21.2's T3 design-spec divergence and S21.4's Engine.get_ticks_msec API regression. Both were caught by Optic (the last structural gate), but neither should have reached Optic. The Boltz role strengthened over the arc (S21.4 Boltz re-review + S21.5 B7 explicit CI-sanity check show visible improvement), but the pattern is a real arc-level signal.
2. **Subagent truncation (S21.2):** Two build-agent truncations on Opus 4.7 consumed real process overhead and left verification record gaps. Mitigated by artifact-based verification and Sonnet 4.6 substitution, but root cause remains undiagnosed. Tracked in #246 (studio-framework investigation).

Arc positive signals:
- Quality-over-speed ruling (2026-04-23) was earned and applied correctly in S21.1 Run-2 fork.
- Five clean single-scope sub-sprints — no scope drift, no bundling creep.
- Per-arc Riv spawn discipline held.
- Structural enforcement surfaces from S21.2 post-mortem (Boltz 6-item checklist, Optic anchor-type assertions, PR body invariant template) shipped in S21.3 and fired correctly.

### Scope-seed completion

| Scope seed | Issue | Status | Sprint closed |
|------------|-------|--------|---------------|
| Bronze content | #112 | ✅ Closed | S21.1 |
| Inline captions (#103) | #103 | ✅ Closed | S21.2 |
| ScrollContainer wrappers (#104) | #104 | ✅ Closed | S21.2 |
| First-encounter overlays (#107) | #107 | Partially closed (all 4 HUD elements covered across S21.2 + S21.3) | S21.3 |
| Audio foundation | #94 | ✅ Closed | S21.5 |

All Arc B scope seeds satisfied. ✅

### Total carry-forwards filed during Arc B

10 GitHub issues filed across 4 of 5 sub-sprints:

| Issue | Sub-sprint | Category | Priority |
|-------|------------|----------|----------|
| [#245](https://github.com/brott-studio/battlebrotts-v2/issues/245) | S21.2 | UX — #107 in-arena HUD sequence (addressed S21.3) | mid |
| [#246](https://github.com/brott-studio/battlebrotts-v2/issues/246) | S21.2 | Framework — subagent truncation pattern | high |
| [#247](https://github.com/brott-studio/battlebrotts-v2/issues/247) | S21.2 | Framework — Optic screenshot evidence required in payload | mid |
| [#248](https://github.com/brott-studio/battlebrotts-v2/issues/248) | S21.2 | Tests — prior-sprint brittleness audit | mid |
| [#252](https://github.com/brott-studio/battlebrotts-v2/issues/252) | S21.3 | Game-code — `_resolve_energy_legend_node()` fallback hardening | P3 |
| [#258](https://github.com/brott-studio/battlebrotts-v2/issues/258) | S21.4 | CI — silent-0-assertion gap | mid-high |
| [#259](https://github.com/brott-studio/battlebrotts-v2/issues/259) | S21.4 | UX — league progress label visual overlap | low |
| [#260](https://github.com/brott-studio/battlebrotts-v2/issues/260) | S21.4 | Game-code — Bronze hardcoded in league helpers | low |
| [#262](https://github.com/brott-studio/battlebrotts-v2/issues/262) | S21.5 | Audio — shop_screen bus-routing debt (S13.5) | mid |
| [#263](https://github.com/brott-studio/battlebrotts-v2/issues/263) | S21.5 | Audio — sfxr asset subjective review | low |

By category: Audio (2), CI/framework (4), UX (2), game-code/tests (2).

### Arc narrative and handoff

**What Arc B attempted:** Close out the "Content & Feel" mandate — Bronze opponents to fight, UX friction removed for new players (scroll, captions, onboarding), and the first moment the game can make a sound.

**What shipped:** Every scope seed delivered. The arc opened with BattleBrotts having no Bronze content, hover-only tooltips, no arena onboarding, no audio. It closes with 6 archetype-coherent Bronze opponents, inline visible-by-default captions across 6 surfaces, scroll wrappers on dense lists, in-arena HUD-element-anchored onboarding overlays with ▲ pointer and sequencing, and a 3-bus audio foundation with two SFX hooks and a persistent mute toggle.

**What the next arc should look at (hand-off to Ett/HCD):**

1. **Structural framework debt (high priority):** The two highest-priority open issues are framework-level: #258 (CI silent-0-assertion gap — the S21.4 PR-B regression type could recur) and #246 (subagent truncation root cause undiagnosed). These are blocking quality risks, not just polish.

2. **Audio character / playtest:** The WALL-E / Thomas Newman tone direction from `docs/kb/audio-vision.md` has structural scaffolding now but no curated assets yet. Human playtest should evaluate the sfxr chimes (#263), and the next audio sub-sprint should bring freesound-curated or composer-commissioned assets for the key moments.

3. **Mixer UI / audio controls (#95 Music, #96 Voice):** The mute toggle has no UI surface yet. A small UX sub-sprint could ship the settings surface (slider + mute checkbox) that the S21.5 `[settings]` API was deliberately designed to support cleanly.

4. **Shop audio routing (#262) and test brittleness (#248):** These are low-effort housekeeping that naturally bundle into a framework-hardening arc or a small cleanup sub-sprint.

5. **Silver/Gold content:** Bronze is now populated and functional. The natural content arc continuation is Silver league population + unlock gating.

---

*Audit authored by Specc (`brott-studio-specc[bot]`) as part of the BattleBrotts-v2 studio pipeline. For framework details see [`brott-studio/studio-framework`](https://github.com/brott-studio/studio-framework). This is the Arc B (Content & Feel) close-out audit.*
