# Sub-Sprint Audit — S24.3 (Combat SFX: Hit + Projectile)

**Sub-sprint:** S24.3
**Arc:** Arc E — Audio Depth
**Date:** 2026-04-24T19:10Z
**Grade:** **A**
**PR:** [brott-studio/battlebrotts-v2#283](https://github.com/brott-studio/battlebrotts-v2/pull/283)
**Merge SHA on `main`:** `85a6bb0f8cb18f64169b7b202acfb3e5fbe02c6c`
**Issues filed:** [#284](https://github.com/brott-studio/battlebrotts-v2/issues/284), [#285](https://github.com/brott-studio/battlebrotts-v2/issues/285), [#286](https://github.com/brott-studio/battlebrotts-v2/issues/286)
**KB entries (PR #287):** `docs/kb/signal-based-sfx-integration.md`, `docs/kb/combat-sfx-spam-guard.md`
**Idempotency key:** `sprint-24.3`

---

## One-line rationale

S24.3 delivers Arc E's Pillar 3 combat SFX wiring in a single clean first-pass PR: two sfxr-synthesized CC0 assets (`hit.ogg` + `projectile_launch.ogg`), signal-based integration at both `on_damage` and `on_projectile_spawned` in `game_main.gd`, a boundary-spam guard (`HIT_SFX_MIN_AMOUNT = 5.0`), and 3 new test files covering bus routing and asset existence — all registered in `SPRINT_TEST_FILES` from the first commit, CI-green at 1383 total assertions (15 net-new), 0 Boltz fix rounds, all scope fences intact. Grade A: no process drag, no fix loops, and the S24.2 test-runner-registration lesson was applied correctly.

---

## 1. Scope Verification

### What Ett planned

S24.3 (Arc E Pillar 3) was chartered to:

- **(a)** Source or synthesize 2 new SFX assets: `hit.ogg` (small metallic thud/clunk, bolt-together robot hit) and `projectile_launch.ogg` (pneumatic puff / mechanical click-whir, handmade weapon sound). CC0 Freesound primary with 15-min cap; sfxr fallback acceptable, flag for HCD review.
- **(b)** Wire `CombatSim.on_damage` signal in `game_main.gd` with a boundary-spam guard (`amount >= HIT_SFX_MIN_AMOUNT`).
- **(c)** Wire `CombatSim.on_projectile_spawned` signal in `game_main.gd`.
- **(d)** Connect both signals at both sim creation sites (`_start_demo_match` + `_start_match`).
- **(e)** Follow the S21.5 ordering convention: `.bus = "SFX"` set **before** `add_child()` for every new `AudioStreamPlayer`.
- **(f)** Deliver 3 new test files registered in `SPRINT_TEST_FILES` in the same PR.
- **(g)** Update `ATTRIBUTION.md` with sfxr synthesis parameters for both assets.
- **(h)** LOC ceiling ≤220 net-new production lines.

### What shipped

| Item | Planned | Delivered | Match |
|------|---------|-----------|-------|
| `hit.ogg` | Small metallic thud/clunk; sfxr fallback OK | sfxr, noise wave, seed 11111, ~0.155s, CC0 | ✅ |
| `projectile_launch.ogg` | Pneumatic puff/click; sfxr fallback OK | sfxr, square wave, seed 22222, ~0.122s, CC0 | ✅ |
| `ATTRIBUTION.md` update | Seed, params, CC0, HCD review flag | Both assets documented with wave, envelope, seed, license, HCD flag | ✅ |
| `_init_combat_sfx_players()` | Init both players, `.bus="SFX"` before `add_child` | Dedicated init function, correct ordering on both players | ✅ |
| `on_damage` wiring (both sites) | Connect at `_start_demo_match` + `_start_match` | Lines 344–345 and 381–382 | ✅ |
| `on_projectile_spawned` wiring (both sites) | Same | Both sites confirmed | ✅ |
| Spam guard | `amount >= HIT_SFX_MIN_AMOUNT` before `.play()` | `const HIT_SFX_MIN_AMOUNT: float = 5.0`, placed before `.play()` | ✅ |
| `test_s24_3_001_hit_sfx_routing.gd` | ≥2 assertions | 4 assertions | ✅ |
| `test_s24_3_002_projectile_sfx_routing.gd` | ≥2 assertions | 5 assertions (exceeded floor) | ✅ |
| `test_s24_3_003_sfx_assets.gd` | ≥3 assertions | 6 assertions (exceeded floor) | ✅ |
| `test_runner.gd` registration | All 3 paths in same PR | Registered at lines 100–103 in same PR commit | ✅ |
| `default_bus_layout.tres` untouched | Required | Confirmed — not in PR diff | ✅ |
| S21.5 assets preserved | `popup_whoosh.ogg`, `win_chime.ogg` | Both in `test_s24_3_003` asset-preservation checks; I-A4/I-A5 pass | ✅ |
| S24.2 mixer UI untouched | Required | No mixer scene/script files in diff | ✅ |
| Net-new production LOC | ≤220 | 47 LOC (`game_main.gd` +43, `test_runner.gd` +4) | ✅ |
| Assertion delta | ≥1371 (≥3 new) | 1368 → 1383 (+15) | ✅ |

Scope is clean. Files in PR: `ATTRIBUTION.md` (+22), `hit.ogg`, `projectile_launch.ogg`, `game_main.gd` (+43), `test_runner.gd` (+4), and 3 test files. No scope creep. No files outside the planned set were modified.

---

## 2. Deliverables Verified

### Assets: `hit.ogg` + `projectile_launch.ogg`

Both assets are committed at `godot/assets/audio/sfx/hit.ogg` and `godot/assets/audio/sfx/projectile_launch.ogg` at the merge SHA. ✅

**`hit.ogg` synthesis parameters (from ATTRIBUTION.md):**
- Wave: noise, attack: 0.005, sustain: 0.03, decay: 0.12, start_freq: 180.0 Hz, slide: −60.0 Hz/s
- HP: 0.05, LP: 0.65, amplitude: 0.80
- Post-processing: loudnorm (peak −9 dBFS), mono, 44100 Hz, libvorbis q4
- Duration: ~0.155s

**`projectile_launch.ogg` synthesis parameters:**
- Wave: square, attack: 0.002, sustain: 0.02, decay: 0.10, start_freq: 320.0 Hz, slide: −120.0 Hz/s
- HP: 0.02, LP: 0.80, amplitude: 0.75
- Post-processing: loudnorm (peak −9 dBFS), mono, 44100 Hz, libvorbis q4
- Duration: ~0.122s

**Tone alignment check (audio-vision.md §"Mechanical & earnest"):**
- `hit.ogg`: Noise wave with fast decay (0.12s) and downward pitch slide (−60 Hz/s) produces a short percussive transient with frequency drop — consistent with "clunk" or "metallic thud" target. Not a sustained tone, not a meaty boom. ✅
- `projectile_launch.ogg`: Square wave with very fast attack (0.002), extremely short sustain (0.02), and steep downward slide (−120 Hz/s) on a mid-range starting pitch (320 Hz) — produces a sharp mechanical click-burst with pitch drop, consistent with "pneumatic puff / mechanical click-whir" target. Not a gunshot, not a sine-tone. ✅

Both assets flagged for HCD subjective review per arc brief §6 risk #2 (sfxr fallback flag required). This is non-blocking — the flag is in both the PR body and ATTRIBUTION.md. The tone judgment is HCD's call, captured in carry-forward issue #284.

**ATTRIBUTION.md:** Updated with full synthesis params, seed, CC0 license statement, and HCD review flag for both new assets. Existing S21.5 entries (`win_chime.ogg`, `popup_whoosh.ogg`) are preserved verbatim. ✅

### `game_main.gd` — Wiring

The `_init_combat_sfx_players()` function is declared at line 867 and called from `_ready()` at line 117.

**Const and member var declarations (lines 103–110):**
```gdscript
const HIT_SFX: AudioStream = preload("res://assets/audio/sfx/hit.ogg")
const PROJECTILE_LAUNCH_SFX: AudioStream = preload("res://assets/audio/sfx/projectile_launch.ogg")
var _hit_sfx_player: AudioStreamPlayer = null
var _projectile_launch_sfx_player: AudioStreamPlayer = null
const HIT_SFX_MIN_AMOUNT: float = 5.0
```

Pattern: one `const` per asset, one `var` per player, `null` initialization. Consistent with S21.5 `POPUP_WHOOSH` / `_popup_whoosh_player` shape. ✅

**`_init_combat_sfx_players()` (lines 867–878) — bus ordering verified:**
```gdscript
func _init_combat_sfx_players() -> void:
    _hit_sfx_player = AudioStreamPlayer.new()
    _hit_sfx_player.name = "HitSfxPlayer"
    _hit_sfx_player.bus = "SFX"        # ← line 870 — BEFORE add_child
    _hit_sfx_player.stream = HIT_SFX
    add_child(_hit_sfx_player)          # ← line 872 — after bus assignment

    _projectile_launch_sfx_player = AudioStreamPlayer.new()
    _projectile_launch_sfx_player.name = "ProjectileLaunchSfxPlayer"
    _projectile_launch_sfx_player.bus = "SFX"   # ← line 876 — BEFORE add_child
    _projectile_launch_sfx_player.stream = PROJECTILE_LAUNCH_SFX
    add_child(_projectile_launch_sfx_player)      # ← line 878 — after bus assignment
```

B4 (bus ordering) gate: `.bus = "SFX"` appears at lines 870 and 876; `add_child()` at lines 872 and 878. Ordering correct for both players. ✅

**Signal connections — both sim creation sites:**

| Site | on_damage connected | on_projectile_spawned connected |
|------|--------------------|---------------------------------|
| `_start_demo_match()` | Line 344 ✅ | Line 345 ✅ |
| `_start_match()` | Line 381 ✅ | Line 382 ✅ |

Both sites confirmed. The S24.3 plan's risk register §risk #1 (integration-point drift — connecting to wrong event) and Boltz B3 gate (both connection sites) both pass. ✅

**Signal handlers:**
```gdscript
func _on_combat_damage(_target, amount: float, _is_crit: bool, _pos: Vector2) -> void:
    if amount >= HIT_SFX_MIN_AMOUNT and _hit_sfx_player != null and is_instance_valid(_hit_sfx_player):
        _hit_sfx_player.play()

func _on_projectile_spawned(_proj) -> void:
    if _projectile_launch_sfx_player != null and is_instance_valid(_projectile_launch_sfx_player):
        _projectile_launch_sfx_player.play()
```

The `is_instance_valid()` guard on both handlers is correct — prevents a crash if the player is freed during match teardown while a signal fires late. ✅

The spam guard is placed on the first line of `_on_combat_damage` (before `.play()`), meaning boundary-tick damage events return in O(1) without reaching the null check or play call. Correct placement. ✅

**S24.4 extensibility note:** `_on_combat_damage` currently ignores `_is_crit`. S24.4 will extend this handler to branch on `is_crit: bool` for crit sound vs. normal hit sound. The current handler's `_is_crit` parameter (leading underscore = intentionally unused) is correctly typed as `bool` in the signal signature, matching `combat_sim.gd:110` — no signature change needed in S24.4. ✅

### Tests

| File | Assertions | Invariants | Registration |
|------|-----------|------------|--------------|
| `test_s24_3_001_hit_sfx_routing.gd` | 4 | I-H1–I-H4: bus assignment preserved; default is Master; HitSfxPlayer = SFX; not Master | `test_runner.gd` line 101 ✅ |
| `test_s24_3_002_projectile_sfx_routing.gd` | 5 | I-P1–I-P4: bus preserved; ProjectileLaunchSfxPlayer = SFX; not Master; two SFX players are independent | `test_runner.gd` line 102 ✅ |
| `test_s24_3_003_sfx_assets.gd` | 6 | I-A1–I-A5: hit.ogg exists; projectile_launch.ogg exists; ATTRIBUTION.md exists + non-empty; popup_whoosh preserved; win_chime preserved | `test_runner.gd` line 103 ✅ |

**Total CI assertions after merge:** 1383 (baseline 1368; delta +15). Verified from CI log line: `total assertions run: 1383`. All 47 sprint files passed. ✅

**Key test design observations:**

`test_s24_3_002_projectile_sfx_routing.gd` adds I-P4 (two SFX players independently holding "SFX" bus) — a valuable non-trivial assertion confirming that two simultaneously-live AudioStreamPlayers don't interfere with each other's bus assignment. This is not in the plan's minimum spec but is within the stated test's semantic scope. Clean. ✅

`test_s24_3_003_sfx_assets.gd` adds I-A3b (ATTRIBUTION.md non-empty size check) beyond the plan's simple `file_exists` minimum. The two-part assertion (exists + size > 0) prevents a silent failure where ATTRIBUTION.md is committed empty. Good test hygiene. ✅

`test_s24_3_001_hit_sfx_routing.gd` I-H2 (default AudioStreamPlayer bus is "Master") is an explicit confirmatory assertion that the SFX assignment is meaningful — if Godot's default changed, this test would flag it. Deliberate defensive assertion. ✅

**Test-runner registration: no miss.** All 3 files registered in `SPRINT_TEST_FILES` in the same PR commit, lines 100–103. This is the correct behavior learned from S24.2's B7-catch lesson. The S24.3 lesson has been applied. ✅

---

## 3. Architectural Observations

### Signal-Based Integration Shape

S24.3 establishes the canonical SFX integration pattern for Arc E combat events. The shape is identical to S21.5's popup whoosh pattern, extended for combat-domain signals:

1. `preload()` const for each asset at file top
2. `var _player: AudioStreamPlayer = null` for each player
3. Dedicated `_init_*_sfx_players()` function called from `_ready()`
4. `.bus = "SFX"` before `add_child()` in every player (S21.5 ordering convention)
5. Signal connection at all sim instantiation sites (not just one)
6. Handler with `is_instance_valid()` null guard

This shape is now documented in `docs/kb/signal-based-sfx-integration.md` (PR #287) for S24.4 and beyond. S24.4's crit/death SFX follow the identical shape with an `is_crit` branch in `_on_combat_damage`.

**Architectural coherence:** The addition of `_init_combat_sfx_players()` as a named function rather than inline code in `_ready()` is the right structural choice. `_ready()` in `game_main.gd` is already long; grouping the SFX initialization under a named function keeps it scannable. The naming convention (`_init_*_sfx_players`) mirrors the implicit pattern of `_play_popup_whoosh()` grouping audio logic. ✅

### Boundary-Spam Guard Design: Threshold vs. Cooldown

The S24.3 implementation chooses an **amount-threshold guard** (`HIT_SFX_MIN_AMOUNT = 5.0`) over a time-cooldown guard. This is the correct choice at S24.3 scope, for two reasons:

1. **Semantic correctness:** The threshold has physical meaning — it distinguishes "meaningful damage events" (real weapon hits, typically ≥10 DPS) from "negligible damage events" (boundary overtime ticks, typically 1–3 DPS). A cooldown guard would play for boundary spam at low-frequency-if-the-cooldown-is-long, regardless of damage amount.

2. **S24.4 composability:** S24.4 adds `crit_hit.ogg` on the same `on_damage` handler with `is_crit=true`. The amount guard naturally applies before the crit branch — no restructuring needed. A cooldown guard would require separate `_last_hit_time` and `_last_crit_time` vars to avoid the crit cooldown blocking normal hits and vice versa.

**Known limitation:** The threshold suppresses spread-weapon pellets if per-pellet damage < 5.0 (e.g., a 5-pellet shotgun dealing 4.0/pellet). This is a playtest-calibration issue captured in carry-forward issue #285. The pattern analysis (threshold vs. cooldown vs. combo) is documented in `docs/kb/combat-sfx-spam-guard.md`.

**Guard placement is correct:** `HIT_SFX_MIN_AMOUNT` is declared as a named const (not an inline magic number), the check is the first condition evaluated in the handler, and its comment (`# Guard: only play hit SFX for meaningful damage (≥5.0) to avoid boundary-tick / splash / reflect spam`) is the exact rationale from the risk register. This is better inline documentation than the S24.2 `_apply_audio_settings` comment convention. ✅

### `.bus` Ordering Convention Held

All three new `AudioStreamPlayer` nodes in S24.3 (including `PopupWhooshPlayer` as the pre-existing reference) set `.bus = "SFX"` before `add_child()`. The convention is now consistent across all 3 existing SFX players in `game_main.gd`:

| Player | `.bus` set at | `add_child()` at | Convention |
|--------|-------------|-----------------|------------|
| `PopupWhooshPlayer` (S21.5) | Line 861 | Line 862 | ✅ |
| `HitSfxPlayer` (S24.3) | Line 870 | Line 872 | ✅ |
| `ProjectileLaunchSfxPlayer` (S24.3) | Line 876 | Line 878 | ✅ |

The convention is fully established and consistently applied. Boltz B4 verification is working as a structural enforcer. ✅

### SFX Bus Routing Confirmed

Both new players route to `"SFX"` (bus index 1 in the 3-bus architecture: Master=0, SFX=1, Music=2). This means:
- S24.2's `MixerSettingsPanel` SFX slider controls the volume of both combat sounds. ✅
- `AudioServer.set_bus_volume_db(1, …)` in both `_apply_audio_settings()` functions (from S24.2) applies to these sounds. ✅
- Muting via `AudioServer.set_bus_mute(0, …)` (Master mute) also silences them through the bus graph. ✅
- Direct routing to Master bus would have bypassed the SFX volume control — correctly avoided. ✅

---

## 4. Process Observations

### (a) First-Pass Clean — Test-Runner Registration Lesson Applied

S24.2's core process failure was Nutts writing 3 test files without registering them in `test_runner.gd SPRINT_TEST_FILES`, requiring a Boltz fix round-trip. The fix (brott-studio/studio-framework PR #60) added an explicit checklist item to `SPAWN_PROTOCOL.md` and the S24.2 audit graded it A− specifically for this miss.

**S24.3 outcome:** All 3 test files registered in `SPRINT_TEST_FILES` in the same PR, at `test_runner.gd` lines 100–103, with a `# [S24.3]` comment tag. No fix round-trip. No B7 catch. CI assertion count rose from 1368 to 1383 on the first Boltz review.

This confirms the studio-framework #60 fix is functioning as intended. The three-surface enforcement (SPAWN_PROTOCOL.md + Boltz B6 gate + plan §3 hard rule) translated into Nutts's implementation. The S24.2 lesson was absorbed in a single sprint cycle.

**Grade implication:** S24.2 was graded A− because of this miss. S24.3 has no analogous miss. Combined with 0 Boltz fix rounds, the grade ceiling is A. No drag found on audit.

### (b) Sonnet 4.6 Nutts Shape — Model-Substitution Policy Working

Nutts ran on Sonnet 4.6 for S24.3, consistent with the medium-write implementation task profile (45–80 production LOC, 3 test files, signal wiring, asset synthesis). Wall clock: ~25 minutes, 21.4k output tokens, no truncation.

This is the same model and performance profile as S24.2's successful Nutts run. The model-substitution policy (established in Arc D S23.1, codified in SOUL.md §"Model selector is shape-of-deliverable") is holding:
- Medium-write implementation tasks → Sonnet 4.6 ✅
- No Opus 4.7 timeout on Nutts (the S24.2 Ett spawn timeout was a planner-level issue, not Nutts) ✅

The 25-minute wall clock is within the expected range for Sonnet 4.6 medium-write tasks (20–35 min from S17.3–S24.2 measurements). No anomalies.

### (c) LOC Landing at 47 vs. 220 Ceiling — Signal Wiring Is Structurally Lean

S24.3 landed at 47 net-new production lines against a 220 ceiling — 79% headroom. This is not surprising in retrospect but worth flagging: signal-based SFX wiring is structurally lean. The pattern requires:
- ~5 lines: const + var declarations per asset
- ~10 lines: `_init_*_sfx_players()` per pair of players
- ~5 lines: 2 signal handlers
- ~4 lines: 2 signal connections (per sim site × 2 sites = 4 connects)

Total: ~24 lines of structural code, plus comments, spacing, and the const guard. Landing at 47 LOC is consistent with the pattern.

**Implication for S24.4:** S24.4 extends the `_on_combat_damage` handler (is_crit branch) and adds `on_death` wiring — an identical structural shape to S24.3 plus one signal. Expected LOC delta: 30–50 production lines. The 220-line ceiling is well over the structural requirement. Gizmo's ceiling calibration remains accurate; the ceiling was generous, not miscalibrated.

**Future arc planning note:** If Arc F music loops require `AudioStreamPlayer` wiring, the same lean LOC profile will apply to the wiring layer. The actual LOC cost in Arc F will be dominated by the music control logic (looping, cross-fade, match-state-aware switching), not the signal connection boilerplate.

### (d) Integration-Point Verification by Boltz — B3 + B6 Discipline

Boltz's B3 gate explicitly named the two integration functions from the pre-flight and verified signal signatures against `combat_sim.gd:110-111`. The signal signatures from the plan are:
- `signal on_damage(target: BrottState, amount: float, is_crit: bool, pos: Vector2)` — verified handler matches: `_on_combat_damage(_target, amount: float, _is_crit: bool, _pos: Vector2)`. Parameter count, types, and ordering match. ✅
- `signal on_projectile_spawned(proj: Projectile)` — verified handler matches: `_on_projectile_spawned(_proj)`. Typed as `_proj` (unused in S24.3; S24.4 may use it for spatial audio). ✅

The leading-underscore convention on unused parameters (`_target`, `_is_crit`, `_pos`, `_proj`) is correct GDScript style — suppresses "unused parameter" warnings that could fail the warnings-as-errors CI policy. ✅

Boltz B6 (test registration) passed on first review — clean first-pass. APPROVE posted via `brott-studio-boltz[bot]` App identity (not user PAT), satisfying branch protection. Auto-merge triggered. ✅

---

## 5. Carry-Forwards

Three issues filed. All deduped against open issue list — none were pre-existing.

### [#284] Sfxr-Synthesized Combat SFX Subjective Review — Hit + Projectile Launch

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:audio`, `prio:P3`

Both S24.3 assets are sfxr-synthesized (Freesound not accessible in build environment per 15-min cap protocol). The synthesis parameters are correct (CC0, documented, deterministic seeds) but have not been human-playtested for subjective tone feel alignment with `audio-vision.md` ("Mechanical & earnest — servos, whirs, pneumatics, sparks, clunks").

**Batch opportunity:** This review should be grouped with the S21.5 assets (`win_chime.ogg`, `popup_whoosh.ogg` from closed issue #263) so HCD can review all four synthesized assets in a single playtest session. Options: accept sfxr tones as-is, re-tune sfxr parameters, or replace with CC0 sourced assets from a non-build Freesound session.

**When:** Arc F or post-playtest. Non-blocking for S24.4 and remaining Arc E pillars.

### [#285] Hit-SFX Boundary-Spam Guard Threshold Tuning (`HIT_SFX_MIN_AMOUNT = 5.0`)

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:audio`, `prio:P3`

The `5.0` threshold was chosen based on boundary-tick damage range (1–3 DPS) vs. typical weapon damage (10–40/hit). Known edge case: a 5-pellet spread weapon dealing 4.0/pellet would be suppressed. Post-playtest calibration may require adjusting the threshold down (to catch more pellet hits) or replacing the amount guard with a cooldown or combo guard. See `docs/kb/combat-sfx-spam-guard.md` for the full pattern analysis.

**When:** Arc F or post-playtest. Non-blocking.

### [#286] SFX Asset Directory Structure — Subdirs for Arc F Music Loops

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:audio`, `prio:P3`

`godot/assets/audio/sfx/` now holds 5 assets across two functional categories (UI SFX and combat SFX). Arc F is likely to add music loops and potentially ambient audio. At current scale a flat structure is appropriate; at ≥8 total assets or ≥3 categories, subdirs (`sfx/ui/`, `sfx/combat/`, `music/`) would improve organization. Flag for Arc F planning — any restructure requires updating all `preload()` paths in game code.

**When:** Arc F planning pass. Non-blocking for all Arc E sub-sprints.

---

## 6. KB Entries

Two KB entries authored from S24.3 reusable patterns and submitted via PR [#287](https://github.com/brott-studio/battlebrotts-v2/pull/287) (`s24.3-kb-entries` branch, docs-only):

### `docs/kb/signal-based-sfx-integration.md`

Captures the canonical pattern for wiring `AudioStreamPlayer` nodes to GDScript signals: const/var declaration shape, `_init_*_sfx_players()` dedicated init function, `.bus = "SFX"` before `add_child()` ordering rule, signal connection at all sim-creation sites, null + `is_instance_valid()` handler guards, player naming convention (`PascalCase + "Player"`), test coverage pattern (bus routing + asset existence), and an anti-patterns table (5 anti-patterns with correct approaches).

Anchored to `game_main.gd` S24.3 implementation as canonical reference.

### `docs/kb/combat-sfx-spam-guard.md`

Documents three guard approaches for high-frequency signal handlers:
1. **Amount threshold** (used in S24.3) — semantically meaningful, composable with crit branch, simple
2. **Cooldown guard** — rate-limited playback regardless of amount, catches low-damage pellets
3. **Combo guard** — threshold + cooldown, two calibration parameters

Includes decision guidance table, known edge cases, S24.4 extension note (is_crit branch with shared spam guard), and backlink to issue #285 for threshold calibration tracking.

---

## 7. Grade and Rationale

**Grade: A**

S24.3 delivered all of Arc E Pillar 3's chartered scope in a single PR, CI-green, with all scope fences intact. The acceptance gate checklist passes cleanly:

| Gate | Result |
|------|--------|
| B1 — Branch/PR title correct | ✅ |
| B2 — `hit.ogg` + `projectile_launch.ogg` in diff | ✅ |
| B3 — Wiring at `on_damage` + `on_projectile_spawned` in `game_main.gd`; both sim sites | ✅ |
| B4 — `.bus = "SFX"` BEFORE `add_child` for both new players | ✅ |
| B5 — `default_bus_layout.tres` untouched; S21.5/S24.1/S24.2 assets untouched | ✅ |
| B6 — `test_runner.gd` SPRINT_TEST_FILES: all 3 paths registered | ✅ |
| B7 — CI: 1368 → 1383 (≥1371 floor) | ✅ |
| B8 — Production LOC: 47 (≤220 ceiling) | ✅ |
| ATTRIBUTION.md updated for both assets | ✅ |
| Spam guard placed before `.play()` | ✅ |
| Labels applied | ✅ |
| Single PR | ✅ |

**Why A and not A−:** The only S24.2 grade drag — test-runner registration miss — was specifically fixed in studio-framework #60 before S24.3 ran. S24.3 had 0 Boltz fix rounds, 0 missed registrations, and all B-gates passed on first review. No process drag was found on audit. The deliverable is clean and the process was clean. A-grade is warranted without qualification.

**Why not A+ (or "perfect"):** The sfxr assets are functional placeholders pending HCD subjective review — this is an acknowledged, non-blocking flag per the arc brief's asset-sourcing protocol, not an audit finding. No code defects, no architectural concerns, and no test quality issues were found. A remains the correct grade.

---

## 8. Role Performance Review

### 🎭 Role Performance

**Gizmo:** Not re-evaluated for S24.3 (arc brief calibration is steady-state). LOC ceiling (220) for S24.3 was again generous — landed at 47 LOC. Two sub-sprints in a row (S24.2 at 242/280, S24.3 at 47/220) confirm signal-wiring tasks are structurally lean within Arc E ceilings. Gizmo may want to use 100-LOC ceilings for pure-wiring sub-sprints in future arcs. Trend: → (ceiling calibration acceptable; refinement opportunity noted)

**Ett:** Shining: Pre-flight was thorough — identified both integration points in `combat_sim.gd:110-111` correctly, verified signal signatures before writing Nutts prompt, specified the spam guard with a concrete threshold value (5.0) and rationale, and included explicit test-runner registration as a hard rule (§3 rule 6, the lesson from S24.2). The three-surface enforcement (SPAWN_PROTOCOL.md + Boltz B6 + plan) worked. Risk register §risk #2 (test-runner registration drift) was correctly rated Low-Medium and correctly resolved by belt-and-suspenders enforcement. Plan quality: high. Trend: ↑ (test-runner lesson applied proactively; risk register was accurate)

**Nutts:** Shining: All planned files delivered in a single clean PR. The `_init_combat_sfx_players()` function is a clean structural choice (named function, not inline `_ready()` code). The `is_instance_valid()` guards are correctly applied to both handlers — Nutts correctly anticipated the teardown-during-signal-fire scenario without being prompted. `HIT_SFX_MIN_AMOUNT` as a named const (not magic number) is good practice. Test files exceeded the floor (4, 5, 6 assertions vs. ≥2/2/3 planned) with meaningful additional assertions (I-H2 confirmatory, I-P4 independence check, I-A3b size check, I-A4/I-A5 preservation checks). SPRINT_TEST_FILES registration: correct on first try — the lesson held. Trend: ↑ (first clean registration; above-floor test quality)

**Boltz:** Shining: B6 and B7 both passed with no issues — clean first review. App token authentication working correctly (second clean round-trip since S24.1 fix). B3 verified both signal connection sites and confirmed parameter signatures match. APPROVE posted as `brott-studio-boltz[bot]`, auto-merge triggered. No CHANGES_REQUESTED cycle. This is the target Boltz performance shape. Trend: ↑ (two consecutive clean App-token round-trips; B3 integration verification discipline solid)

**Optic:** `Optic Verified` check ran and returned `success` (one run) and `skipped` (one run, likely the pre-merge trigger). S24.3 is combat-code adjacent but the diff is purely `game_main.gd` signal wiring and test files — likely below Optic's visual-change detection threshold. Not evaluated for S24.3 deliverable quality. Trend: → (not directly involved)

**Specc (this audit):** All claims verified against live repo state: PR diff, CI log assertion count (1383 confirmed), signal connection line numbers, bus ordering line numbers, test registration lines, issue deduplication, KB PR creation. Issues #284–#286 filed with full carry-forward context. KB entries authored with concrete code references and decision guidance. Single-session, single-write audit. Trend: →

---

## 9. Gate to S24.4

**S24.3 is closed. S24.4 gate condition: ✅ satisfied.**

S24.4 (Combat SFX — critical + death) requires this audit (`audits/battlebrotts-v2/v2-sprint-24.3.md`) on `studio-audits/main`. Gating is met.

**S24.4 scope (from arc brief §3 and ett-plan §9):**
- `crit_hit.ogg` — wired as `if is_crit` branch in `_on_combat_damage` (S24.3 handler extended)
- `death.ogg` — wired to `CombatSim.on_death` signal (a net-new signal connection site)
- Tone: "punchy oomph" (crit, per audio-vision.md "big moments"); "compassionate, no punishment" (death)
- Higher emotional weight → more sfxr tuning care or active CC0 search

**S24.4 structural benefits from S24.3:**
1. `_on_combat_damage` handler already exists and has the spam guard — S24.4 adds a branch, not a new handler.
2. `_init_combat_sfx_players()` establishes the init pattern — S24.4 appends 2 more players in the same function.
3. The signal-based integration KB entry and spam-guard KB entry are live documentation for the S24.4 Nutts spawn.
4. Test patterns (bus routing, asset existence, player independence) are established templates for S24.4's test files.

---

*Authored by Specc (brott-studio-specc[bot]). S24.3 sub-sprint closed 2026-04-24T19:10:00Z.*
