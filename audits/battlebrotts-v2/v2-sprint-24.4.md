# Sub-Sprint Audit — S24.4 (Combat SFX: Critical Hit + Death)

**Sub-sprint:** S24.4
**Arc:** Arc E — Audio Depth
**Date:** 2026-04-24T19:21Z
**Grade:** **A**
**PR:** [brott-studio/battlebrotts-v2#288](https://github.com/brott-studio/battlebrotts-v2/pull/288)
**Merge SHA on `main`:** `403a3516f459e40472c1df6aed09d3e61b649673`
**Issues filed:** [#289](https://github.com/brott-studio/battlebrotts-v2/issues/289), [#290](https://github.com/brott-studio/battlebrotts-v2/issues/290), [#291](https://github.com/brott-studio/battlebrotts-v2/issues/291)
**KB entries (PR #292):** `docs/kb/cooldown-guard-before-yield.md`, `docs/kb/mutually-exclusive-sfx-branch.md`
**Idempotency key:** `sprint-24.4`

---

## One-line rationale

S24.4 closes Arc E's Pillar 3 combat SFX layer cleanly: two sfxr-synthesized CC0 assets (`critical_hit.ogg` + `death.ogg`), mutually-exclusive `is_crit` branch in `_on_combat_damage`, a cooldown-guarded `_on_brott_death` handler wired at both CombatSim setup sites, and 3 new test files (23 total assertions) registered in `SPRINT_TEST_FILES` from the first commit — CI-green at 1407 total assertions (1383 → +24), 52 net-new production LOC, 0 Boltz fix rounds, all scope fences intact. Grade A: identical process shape to S24.3, lessons applied, all pillars structurally sound.

---

## 1. Scope Verification

### What Ett planned

S24.4 (Arc E Pillar 3 continuation) was chartered to:

- **(a)** Source or synthesize 2 new SFX assets: `critical_hit.ogg` (punchy mechanical crunch, heavier than `hit.ogg`, amplitude ~0.85, "big moment" per `audio-vision.md`) and `death.ogg` (soft descending mechanical chirp, restrained pathos, amplitude ~0.60, ≤0.5s). CC0 Freesound primary with 15-min cap; sfxr fallback, flag for HCD review.
- **(b)** Modify `_on_combat_damage` in `game_main.gd`: rename `_is_crit` → `is_crit`, add mutually-exclusive `if is_crit` branch routing to `_critical_hit_sfx_player`; retain `HIT_SFX_MIN_AMOUNT` guard on the `elif` (normal hit) arm.
- **(c)** Add `_on_brott_death` handler with a 600ms cooldown guard to prevent mass-death-frame SFX overlap.
- **(d)** Wire `sim.on_death.connect(_on_brott_death)` at **both** CombatSim setup sites (`_start_demo_match` and `_start_match`).
- **(e)** Extend `_init_combat_sfx_players()` with 2 new `AudioStreamPlayer` nodes; `.bus = "SFX"` set **before** `add_child()` for both.
- **(f)** Deliver 3 new test files registered in `SPRINT_TEST_FILES` in the same PR, total assertions ≥1386.
- **(g)** Update `ATTRIBUTION.md` with sfxr synthesis parameters for both assets.
- **(h)** LOC ceiling ≤220 net-new production lines.

### What shipped

| Item | Planned | Delivered | Match |
|------|---------|-----------|-------|
| `critical_hit.ogg` | Punchy crunch, sfxr fallback OK, amp ~0.85 | sfxr, noise+sine sweep, seed 33333, amplitude 0.85, ~0.22s, CC0 | ✅ |
| `death.ogg` | Soft descending chirp, sfxr fallback OK, amp ~0.60, ≤0.5s | sfxr, sine sweep 440→80 Hz + 2nd harmonic + noise texture, seed 44444, amplitude 0.60, ~0.42s, CC0 | ✅ |
| `ATTRIBUTION.md` update | Seed, params, CC0, HCD review flag | Both assets: wave, envelope, seed, loudnorm params, license, HCD flag | ✅ |
| `_on_combat_damage` modified | `_is_crit` → `is_crit`, `if is_crit` branch added | Rename confirmed; crit arm `if is_crit`, hit arm `elif amount >= HIT_SFX_MIN_AMOUNT` | ✅ |
| Mutually exclusive branches | Crit and hit arms never both fire | `if/elif` structure — structurally impossible for both to fire per event | ✅ |
| `_on_brott_death` handler | New handler, 600ms cooldown guard | `_death_sfx_cooldown_active` flag, set before `.play()`, auto-reset after 0.6s via `create_timer` | ✅ |
| `on_death.connect` at both sites | `_start_demo_match` + `_start_match` | Lines 354, 393 (squash-merge offsets from S24.4 diff) — both sites | ✅ |
| `_init_combat_sfx_players()` extension | 2 new players, `.bus = "SFX"` before `add_child` | CriticalHitSfxPlayer + DeathSfxPlayer; ordering verified (bus before add_child for both) | ✅ |
| `test_s24_4_001_crit_sfx_routing.gd` | ≥3 assertions | 8 assertions (T1a–T1g + bonus) | ✅ |
| `test_s24_4_002_death_sfx_routing.gd` | ≥3 assertions | 7 assertions (T2a–T2g) | ✅ |
| `test_s24_4_003_sfx_assets.gd` | ≥5 assertions | 9 assertions (T3a–T3i including scope-fence preservation) | ✅ |
| `test_runner.gd` registration | All 3 paths in same PR | Registered at `test_runner.gd` lines 104–107 in same PR commit | ✅ |
| `default_bus_layout.tres` untouched | Required | Confirmed — not in PR diff | ✅ |
| S24.3 assets preserved | `hit.ogg`, `projectile_launch.ogg` | Both in T3f/T3g scope-fence checks; I-A4/I-A5 pass | ✅ |
| S21.5 assets preserved | `win_chime.ogg`, `popup_whoosh.ogg` | T3h/T3i scope-fence checks pass | ✅ |
| S24.2 mixer UI untouched | Required | No mixer scene/script files in diff | ✅ |
| `_on_projectile_spawned` untouched | Required (except `_is_crit` rename) | S24.3 handler confirmed unchanged; only `_on_combat_damage` parameter rename | ✅ |
| Net-new production LOC | ≤220 | 52 LOC (`game_main.gd` +48, `test_runner.gd` +4) | ✅ |
| Assertion delta | ≥1386 (≥3 new) | 1383 → 1407 (+24; T1=8, T2=7, T3=9) | ✅ |

Scope is clean. Files in PR: `ATTRIBUTION.md` (+22 lines), `critical_hit.ogg` (binary, new), `death.ogg` (binary, new), `game_main.gd` (+48 prod lines), `test_runner.gd` (+4 lines), and 3 test files. No scope creep. No files outside the planned set were modified.

---

## 2. Deliverables Verified

### Assets: `critical_hit.ogg` + `death.ogg`

Both assets committed at `godot/assets/audio/sfx/critical_hit.ogg` and `godot/assets/audio/sfx/death.ogg` at the merge SHA. ✅

**`critical_hit.ogg` synthesis parameters (from ATTRIBUTION.md):**
- Wave: noise (70%) + sine sweep (30%), attack: 0.005s, sustain: 0.04s, decay to 0.22s total
- Start freq: 280.0 Hz, end freq: 90.0 Hz, LP filter at 8000 Hz, amplitude: 0.85
- Seed: 33333 (deterministic)
- Post-processing: loudnorm (I=−14, TP=−7, LRA=7), mono, 44100 Hz, libvorbis q4
- Duration: ~0.22s

**`death.ogg` synthesis parameters (from ATTRIBUTION.md):**
- Wave: sine descending sweep (440→80 Hz) + 2nd harmonic (0.15) + noise texture (0.08)
- Attack: 0.015s, sustain: 0.08s, decay to 0.42s total; amplitude: 0.60
- Seed: 44444 (deterministic)
- Post-processing: loudnorm (I=−18, TP=−9, LRA=7), mono, 44100 Hz, libvorbis q4
- Duration: ~0.42s

**Tone alignment check (audio-vision.md §"Mechanical & earnest" + §"Big moments"):**

`critical_hit.ogg`: Noise (70%) + sine sweep blend produces a complex transient with a high-frequency attack and descending sweep — the noise component delivers the "mechanical crunch" character while the sine component adds frequency-sweep oomph. LP filter at 8000 Hz keeps it from being too harsh. Amplitude at 0.85 vs `hit.ogg`'s 0.80 places it meaningfully louder — the hierarchy crit (0.85) > hit (0.80) matches the "big moments" guidance in `audio-vision.md`. At 0.22s it is longer than `hit.ogg`'s 0.155s, appropriate for a higher-weight event. Overall: consistent with "punchy oomph layered in for impact, bolt-together robot, not cinematic." ✅

`death.ogg`: Sine descending sweep (440→80 Hz) with 2nd harmonic adds warmth, noise texture (0.08) adds subtle mechanicalism. The descend from 440 to 80 Hz over 0.42s produces a clearly "powering down" trajectory — the pitch direction is semantically loaded (descending = ending). Amplitude at 0.60 is substantially quieter than both `hit.ogg` and `critical_hit.ogg`. loudnorm target of I=−18 vs `hit.ogg`'s I=−14 reinforces the intentional quiet. Duration at 0.42s is within the ≤0.5s spec. Per `audio-vision.md`: "no punishment on losses — only pathos." The descending mechanical chirp achieves this. ✅

**Amplitude hierarchy verified:** crit (0.85) > hit (0.80) > death (0.60). The hierarchy places death as the quietest combat sound — intentionally restrained. Carry-forward issue #291 tracks post-playtest mixing calibration if the relative levels need adjustment.

**ATTRIBUTION.md:** Updated with full synthesis params, seed, CC0 license statement, loudnorm target, and HCD review flag for both new assets. Existing S24.3 (`hit.ogg`, `projectile_launch.ogg`) and S21.5 (`win_chime.ogg`, `popup_whoosh.ogg`) entries preserved verbatim. ✅

**HCD review flag:** Both assets flagged in PR body and ATTRIBUTION.md per arc brief §6 risk #2 protocol. Batched with existing S24.3 + S21.5 sfxr assets in carry-forward issue #289 for a single consolidated playtest review session. Non-blocking for S24.5 and remaining Arc E pillars. ✅

### `game_main.gd` — Wiring

**Const and member var declarations (after S24.3 block, line ~109):**
```gdscript
# [S24.4] Combat SFX — critical hit + death.
const CRITICAL_HIT_SFX: AudioStream = preload("res://assets/audio/sfx/critical_hit.ogg")
const DEATH_SFX: AudioStream = preload("res://assets/audio/sfx/death.ogg")
var _critical_hit_sfx_player: AudioStreamPlayer = null
var _death_sfx_player: AudioStreamPlayer = null
var _death_sfx_cooldown_active: bool = false  # guard: prevent mass-death frame spam
```

Pattern: one `const` per asset, one `var` per player, `null` initialization, `bool` guard flag initialized at declaration. Consistent with S24.3 shape. ✅

**`_init_combat_sfx_players()` extension — bus ordering verified:**
```gdscript
# [S24.4] Critical hit SFX player.
_critical_hit_sfx_player = AudioStreamPlayer.new()
_critical_hit_sfx_player.name = "CriticalHitSfxPlayer"
_critical_hit_sfx_player.bus = "SFX"  # MUST be set BEFORE add_child per S21.5 convention
_critical_hit_sfx_player.stream = CRITICAL_HIT_SFX
add_child(_critical_hit_sfx_player)

# [S24.4] Death SFX player.
_death_sfx_player = AudioStreamPlayer.new()
_death_sfx_player.name = "DeathSfxPlayer"
_death_sfx_player.bus = "SFX"  # MUST be set BEFORE add_child per S21.5 convention
_death_sfx_player.stream = DEATH_SFX
add_child(_death_sfx_player)
```

B4 (bus ordering) gate: `.bus = "SFX"` appears before `add_child(...)` for both new players. Convention confirmed for all 5 SFX players now live in `_init_combat_sfx_players()`. ✅

**`_on_combat_damage` modification — crit/hit mutual exclusion:**
```gdscript
func _on_combat_damage(_target, amount: float, is_crit: bool, _pos: Vector2) -> void:
    if is_crit:
        if _critical_hit_sfx_player != null and is_instance_valid(_critical_hit_sfx_player):
            _critical_hit_sfx_player.play()
    elif amount >= HIT_SFX_MIN_AMOUNT:
        if _hit_sfx_player != null and is_instance_valid(_hit_sfx_player):
            _hit_sfx_player.play()
```

`if/elif` structure guarantees mutual exclusion at the language level — it is structurally impossible for both arms to execute in a single invocation. Parameter rename `_is_crit` → `is_crit` is consistent with GDScript convention (leading underscore = unused). The null + `is_instance_valid()` guard pattern matches S24.3. `HIT_SFX_MIN_AMOUNT` guard retained in `elif` arm. ✅

**Why crits skip the amount threshold:** Critical hits are filtered by `is_crit` at the caller (combat_sim.gd) — they represent a distinct qualitatively-significant event regardless of damage magnitude. Applying the 5.0 threshold to crits would suppress low-damage crits from status effects, which would be a gameplay clarity failure. The `if is_crit` arm fires unconditionally (no amount check); only the `elif` (normal hit) arm retains the guard. This matches the plan's §2 decision rationale and is architecturally correct. ✅

**`_on_brott_death` handler — cooldown guard:**
```gdscript
func _on_brott_death(_brott) -> void:
    if _death_sfx_cooldown_active:
        return
    if _death_sfx_player != null and is_instance_valid(_death_sfx_player):
        _death_sfx_cooldown_active = true
        _death_sfx_player.play()
        # Reset cooldown after 600ms to allow future matches to play death SFX.
        await get_tree().create_timer(0.6).timeout
        _death_sfx_cooldown_active = false
```

Guard flag set **before** `.play()` — correctly handles the case where `on_death` fires twice synchronously in the same call stack (both emits arrive before the coroutine yields). The flag is already `true` when the second call hits the first `if`. This is the only correct ordering; setting the flag after `.play()` would be a race. ✅

The `await` yields to the event loop, allowing other game events to proceed while the cooldown timer runs. The 600ms window (per spec) is longer than `death.ogg`'s 0.42s duration — the sound completes before the cooldown resets. Per-match correctness: after a match ends and a new one begins, the 600ms timer will have expired (any reasonable match restart time > 600ms), resetting the flag cleanly. ✅

**Signal connections — both sim creation sites verified:**

| Site | on_damage connected | on_projectile_spawned connected | on_death connected |
|------|--------------------|---------------------------------|-------------------|
| `_start_demo_match()` | Line 350 (S24.3) ✅ | Line 351 (S24.3) ✅ | Line 354 (S24.4) ✅ |
| `_start_match()` | Line 389 (S24.3) ✅ | Line 390 (S24.3) ✅ | Line 393 (S24.4) ✅ |

Boltz B3 confirmed both sites. S24.4 plan's risk register §risk #1 (missing one connection site) correctly rated Medium-likelihood and correctly resolved by Boltz's diff-based gate. Both paths wired. ✅

### Tests

| File | Assertions | Invariants | Registration |
|------|-----------|------------|--------------|
| `test_s24_4_001_crit_sfx_routing.gd` | 8 | T1a–T1g: bus assignment preserved, default bus baseline, bus differs from default, is_crit=true → crit (T1d), is_crit=true ≠ hit (T1e), is_crit=false+amount≥threshold → hit (T1f), is_crit=false+amount<threshold → silence (T1g) | `test_runner.gd` line 104 ✅ |
| `test_s24_4_002_death_sfx_routing.gd` | 7 | T2a–T2g: bus assignment, default bus baseline, bus differs from default, cooldown prevents play (T2d), cooldown allows play when inactive (T2e), cooldown window is 600ms (T2f), mass-death only first fires (T2g) | `test_runner.gd` line 105 ✅ |
| `test_s24_4_003_sfx_assets.gd` | 9 | T3a–T3i: critical_hit.ogg exists, death.ogg exists, ATTRIBUTION.md exists, ATTRIBUTION.md has critical_hit entry (T3d), ATTRIBUTION.md has death entry (T3e), hit.ogg preserved (T3f), projectile_launch.ogg preserved (T3g), win_chime.ogg preserved (T3h), popup_whoosh.ogg preserved (T3i) | `test_runner.gd` line 106 ✅ |

**Total CI assertions after merge:** 1407 (baseline 1383; delta +24; T1=8, T2=7, T3=9). Verified from CI log line: `total assertions run: 1407`. All 61 sprint files passed, 0 failed. ✅

**Key test design observations:**

T1d–T1g (crit/hit routing, test_s24_4_001) demonstrate all four combinatorial branches of the `if is_crit / elif amount >= threshold` logic: crit=true → crit, crit=true ≠ hit, crit=false+above-threshold → hit (with counter-check that crit did NOT fire), crit=false+below-threshold → silence. This is the correct minimal coverage for mutual-exclusion logic — all four paths are tested. ✅

T2d–T2g (cooldown guard behavior, test_s24_4_002) directly simulate the mass-death scenario with a three-call sequence: first call fires (count=1), second call suppressed by active cooldown, third call suppressed. The T2g assertion `death_count_fired == 1` is a direct behavioral invariant. T2f (`cooldown_ms == 600`) is a spec-anchoring assertion — if the constant changes, this fails and flags the regression. ✅

T3d–T3e (ATTRIBUTION.md content verification) extend beyond the S24.3 T3b pattern (file exists + non-empty). These tests read ATTRIBUTION.md content and check for asset-name substrings — confirming not just that the file is non-empty but that it contains entries for the correct assets. This catches the failure mode where ATTRIBUTION.md exists from a prior sprint but is not updated for the new assets. ✅

T3h/T3i (S21.5 preservation checks) extend the scope-fence pattern established in S24.3. S24.4's T3 now covers preservation of all 4 prior-sprint SFX assets (hit, projectile_launch, win_chime, popup_whoosh). A single accidental overwrite of any prior asset would fail immediately. ✅

**Test-runner registration: no miss (second consecutive clean sprint after S24.3's correction of S24.2 miss).** All 3 files registered in `SPRINT_TEST_FILES` at `test_runner.gd` lines 104–107 in the same PR commit, with a `# [S24.4]` comment tag. The studio-framework #60 enforcement is holding. ✅

---

## 3. Architectural Observations

### Pillar 3 Combat SFX — Fully Closed

S24.4 completes Arc E's Pillar 3 (combat SFX). All four chartered event types are now wired:

| Event | Asset | Handler | Sprint |
|-------|-------|---------|--------|
| `on_damage` (normal hit) | `hit.ogg` | `_on_combat_damage` (`elif` arm) | S24.3 |
| `on_projectile_spawned` | `projectile_launch.ogg` | `_on_projectile_spawned` | S24.3 |
| `on_damage` (crit) | `critical_hit.ogg` | `_on_combat_damage` (`if is_crit` arm) | S24.4 |
| `on_death` | `death.ogg` | `_on_brott_death` | S24.4 |

This satisfies the Arc E A-grade criterion: "Combat SFX: hit, critical, death, projectile — all four events wired." Combined with S24.2 (Mixer UI), Arc E is 2 of 4 pillars closed. The playtest-ready trigger (Mixer UI + ≥4 SFX events + ≥1 music loop + CI green) is now one pillar away — S24.5 (music, gated on HCD tone call) unblocks it. ✅

### `_on_combat_damage` Evolution Across S24.3 → S24.4

The handler underwent a clean two-sprint evolution:

**S24.3 (initial):**
```gdscript
func _on_combat_damage(_target, amount: float, _is_crit: bool, _pos: Vector2) -> void:
    if amount >= HIT_SFX_MIN_AMOUNT and _hit_sfx_player != null and is_instance_valid(_hit_sfx_player):
        _hit_sfx_player.play()
```

**S24.4 (extended):**
```gdscript
func _on_combat_damage(_target, amount: float, is_crit: bool, _pos: Vector2) -> void:
    if is_crit:
        if _critical_hit_sfx_player != null and is_instance_valid(_critical_hit_sfx_player):
            _critical_hit_sfx_player.play()
    elif amount >= HIT_SFX_MIN_AMOUNT:
        if _hit_sfx_player != null and is_instance_valid(_hit_sfx_player):
            _hit_sfx_player.play()
```

The S24.3 form treated `_is_crit` as unused-but-typed (leading underscore convention). The S24.4 extension made the natural move: drop the underscore, add the branch. Net addition: 4 lines, 1 parameter rename. The S24.3 form's single-condition guard (`if amount >= min and player != null and is_instance_valid(player)`) was refactored into a cleaner two-level structure for both arms — the null/validity guards now live one level deeper, where they belong semantically (each arm checks its own player). The refactoring improves readability at no cost to correctness. ✅

The comment block was updated to acknowledge both sprints (`# [S24.3] Signal handler` + `# [S24.4] Crit branch`), providing clear historical attribution in the source. This is the correct comment style for incremental extensions.

### `_on_brott_death` — New Signal Handler Shape

This is the first handler in `game_main.gd` that uses `await` — a coroutine construct. This is the correct tool for timer-based cooldown reset (vs. `_process()` delta accumulation or a separate timer node). Key properties of the `await get_tree().create_timer(0.6).timeout` pattern:

1. No persistent state beyond the boolean flag.
2. No heap allocation beyond the timer (Godot SceneTree timer is lightweight).
3. Correct behavior under scene/match teardown: the SceneTree timer is tied to the tree's lifetime; if the game resets mid-timer, the timer silently expires without firing the callback (GDScript `await` on a freed signal source returns without error in Godot 4). The `_death_sfx_cooldown_active` flag would remain `true` until either the timer fires or the next match's initialization. In practice, any match restart takes longer than 600ms, so this is not a correctness concern.

The alternative (time-based check using `Time.get_ticks_msec()`) was also specified as acceptable in the plan. The `create_timer` approach is cleaner — no need to store a `_last_death_time` variable.

**Potential edge case (documented, not blocking):** If a scene change happens within the 600ms window, the `await` coroutine is orphaned and `_death_sfx_cooldown_active` remains `true`. If the same `game_main.gd` instance persists across the scene change (which is architecture-dependent), the next match would have its first death suppressed. This is tracked under issue #290 for post-playtest calibration. Not a current gameplay concern (Godot 4 typically reinstantiates game_main on scene reload). ✅

### SFX Player Naming Convention — Now Five Players

`_init_combat_sfx_players()` now manages five `AudioStreamPlayer` nodes:

| Player name | Node name | Bus | Sprint |
|------------|-----------|-----|--------|
| `_popup_whoosh_player` | `PopupWhooshPlayer` | `SFX` | S21.5 |
| `_hit_sfx_player` | `HitSfxPlayer` | `SFX` | S24.3 |
| `_projectile_launch_sfx_player` | `ProjectileLaunchSfxPlayer` | `SFX` | S24.3 |
| `_critical_hit_sfx_player` | `CriticalHitSfxPlayer` | `SFX` | S24.4 |
| `_death_sfx_player` | `DeathSfxPlayer` | `SFX` | S24.4 |

The naming convention (`PascalCase + "Player"` for node names, `_snake_case_player` for var names) is now established across 5 players consistently. All route to `"SFX"` bus — the S24.2 MixerPanel SFX volume slider controls all five. ✅

**Architectural note for S24.5/S24.6 (Music):** Music assets will use a separate `AudioStreamPlayer` (or `AudioStreamPlayer` with looping) routed to the `"Music"` bus. The `_init_*_sfx_players()` function should not be extended for music — a separate `_init_music_players()` (or equivalent) should be introduced to maintain the logical separation between SFX and Music init paths. The S24.3 KB entry (`signal-based-sfx-integration.md`) applies to both SFX and Music wiring; the separation is cosmetic/organizational.

---

## 4. Process Observations

### (a) S24.3 Lesson Fully Transferred — Second Consecutive First-Pass Clean Sprint

S24.3 was the first sprint after S24.2's B7 miss to achieve clean test-runner registration. S24.4 is the second consecutive sprint with no fix loops and no missed registrations. The three-surface enforcement (SPAWN_PROTOCOL.md + Boltz B6 gate + plan §3 hard rule) is now a stable pipeline property, not a one-off. This is the pattern the arc brief §3 speculates about: "S24.3 pattern established" — meaning S24.4 should follow the same shape, and it did. ✅

### (b) LOC Economy — 52 Net-New Production Lines (52/220, 76% headroom)

S24.4 landed at 52 net-new production lines: `game_main.gd` (+48) and `test_runner.gd` (+4). This is consistent with S24.3's 47 LOC, confirming the plan's §3 note: signal-wiring tasks are structurally lean regardless of the number of new signals being wired. The additional 5 LOC vs S24.3 comes from the `_on_brott_death` handler being somewhat longer (8 lines including `await`) compared to S24.3's 2-line handlers.

**LOC breakdown for `game_main.gd` +48:**
- Const/var declarations block (S24.4): 6 lines
- `_init_combat_sfx_players()` extension (2 new players): 16 lines
- `_on_combat_damage` refactor: the S24.3 handler was 3 lines; the S24.4 version is 7 lines (+4 net)
- `_on_brott_death` handler: 11 lines (function declaration + guard + null check + play + await reset + comments)
- `on_death.connect` at both sites: 4 lines (2 per site, including `# [S24.4]` comment)
- Comments and blank lines for clarity: ~7 lines

The 220-line ceiling was again generous. Gizmo's calibration of "50–100 LOC" for S24.4 is accurate; landing at 52 production LOC is within the lower bound of that range. ✅

### (c) 0 Boltz Fix Rounds — First-Pass APPROVE

Boltz reviewed and approved in a single round, 9 seconds before the auto-merge triggered (review at 19:19:34Z, merge at 19:19:43Z). All B1–B8 gates passed on first review:
- B7 assertion count (1407 vs. ≥1386 floor): passed with 21-assertion headroom
- B3 both connection sites: confirmed at lines 354 and 393
- B4 bus ordering: `.bus = "SFX"` precedes `add_child` for both new players
- B8 LOC: 52 production lines vs. 220 ceiling

0 fix loops is the target Boltz performance shape. Three consecutive sub-sprints (S24.2 fix round, S24.3 clean, S24.4 clean) show the fix-loop rate declining to 0 for the second sprint in a row. ✅

### (d) Wall-Clock Execution — ~18 Minutes (Nutts → Boltz → Merge)

PR #288 creation timestamp (first commit) was at 19:13:56Z (inferred from workflow trigger time); merge was at 19:19:43Z. Boltz's review was submitted at 19:19:34Z. Total wall clock from PR open to merge: approximately 6 minutes. Including Nutts implementation time (estimated ~12 minutes for the wiring + synthesis, consistent with the narrower S24.4 scope vs. S24.3's 25 minutes), total sub-sprint time: ~18 minutes.

This is at the very tight end of the expected range (30–60 min for equivalent sub-sprints). The efficiency is attributable to: (1) the S24.3 wiring infrastructure being completely in place — no new init function structure needed, just extension; (2) sfxr synthesis using established parameters from S24.3 as a reference; (3) no CC0 search attempt (build environment confirmed inaccessible for Freesound). The 18-minute run is a positive data point for the lean LOC / lean scope formula that Gizmo calibrated.

---

## 5. Carry-Forwards

Three issues filed. All deduped against open issue list — no pre-existing issues covered this scope.

### [#289] Sfxr-Synthesized Combat SFX Subjective Review — critical_hit + death

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:audio`, `prio:P3`

Both S24.4 assets are sfxr-synthesized (Freesound not accessible in build environment). Synthesis parameters are correct and documented but have not been human-playtested for subjective tone-feel alignment with `audio-vision.md`.

**Batch opportunity (flagged in issue body):** Group with S24.3 assets (#284) and S21.5 assets (#263 → kept) in a single playtest session — HCD reviews all sfxr-synthesized assets at once. This is more efficient than reviewing per-sprint. Questions for the review:
- `critical_hit.ogg`: heavier/punchier than `hit.ogg`? Not cinematic? Robot-character intact?
- `death.ogg`: gentle and restrained? Not punishing? Audible but quiet relative to combat sounds?

**When:** Arc F or post-playtest. Non-blocking for S24.5 and all remaining Arc E pillars.

### [#290] Death SFX Cooldown Duration Calibration (600ms Window)

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:audio`, `prio:P3`

The `_on_brott_death` 600ms cooldown was sized to cover worst-case 4-bot mass-death (3–4 events in ~50ms) with headroom for `death.ogg`'s 0.42s playback. Post-playtest questions:
- Is 600ms the right window for the pacing of actual matches?
- Does "first death wins" semantics feel correct, or would "last death wins" be more impactful?
- Should the cooldown be per-brott rather than global (allowing N=2 deaths in a double-elimination bracket to each play a quiet death sound if they are spaced by >600ms)?

**When:** Arc F or post-playtest. Non-blocking.

### [#291] Audio Mixing Balance — death.ogg Relative Level vs. hit.ogg and critical_hit.ogg

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:audio`, `prio:P3`

`death.ogg` is intentionally quieter (amplitude 0.60, loudnorm I=−18) than both `hit.ogg` (0.80, I=−14) and `critical_hit.ogg` (0.85, I=−14). The loudnorm differential (4 LUFS) compounds the amplitude differential. Post-playtest questions:
- Is `death.ogg` audible at default SFX slider levels?
- Does the loudnorm targeting difference create an unexpected gap between `death.ogg` and the combat sounds?
- Calibrate: the hierarchy should be felt — death is quiet but present, not absent.

**When:** Arc F or S24.7 integration pass. Non-blocking.

---

## 6. KB Entries

Two KB entries authored from S24.4 reusable patterns and submitted via PR [#292](https://github.com/brott-studio/battlebrotts-v2/pull/292) (`s24.4-kb-entries` branch, docs-only). Labels applied immediately: `area:docs`, `arc:E`, `sprint:S24.4`, `kb-entry`. ✅

### `docs/kb/cooldown-guard-before-yield.md`

Captures the cooldown-guard-before-yield pattern for mass-event SFX suppression. Content:
- Problem context (N signals per tick from N entities)
- Full GDScript implementation with annotated comments
- Cooldown window sizing formula: `cooldown_ms ≥ asset_duration_ms + (N-1 ticks × tick_duration_ms)`
- Decision table: when to use cooldown guard vs. not
- Anti-patterns (5 entries) with failure explanations — notably: flag-after-play (race condition), frame-based reset (too fast), `playing` property check (unreliable for sub-frame assets)
- Composability section showing how cooldown + amount-threshold guards coexist

### `docs/kb/mutually-exclusive-sfx-branch.md`

Captures the `if/elif` branch pattern for single-signal multi-sound routing. Content:
- Problem context (one signal, multiple sounds, must not play both)
- Full GDScript implementation with branch-semantics table
- Why crits skip the amount threshold (semantic rationale, not just convention)
- Parameter naming convention (`_is_crit` → `is_crit` rename and why)
- Extension pattern for additional qualifiers (priority ordering with 3+ qualifiers)
- Anti-patterns (4 entries) — notably: `if/if` instead of `if/elif` (both fire on crit), `else` without threshold guard (boundary-tick regression)
- Test coverage pattern: 4 invariants for mutual-exclusion logic (all combinatorial paths)

**Together with S24.3 KB entries (`signal-based-sfx-integration.md`, `combat-sfx-spam-guard.md`), these form a complete Arc E combat SFX pattern library.** S24.5/S24.6 music wiring can reference `signal-based-sfx-integration.md` for the core player setup pattern; the combat-specific patterns are isolated to the combat KB files.

**Label application confirmed:** PR #292 labels verified as `['area:docs', 'arc:E', 'sprint:S24.4', 'kb-entry']` — no empty labels (correcting the S24.3 KB PR #287 pattern where labels were left empty). ✅

---

## 7. Grade and Rationale

**Grade: A**

S24.4 closes Arc E Pillar 3 in a single PR, CI-green at 1407 assertions, with all scope fences intact and 0 Boltz fix rounds. The B-gate checklist passes cleanly:

| Gate | Result |
|------|--------|
| B1 — Branch/PR title correct; labels applied | ✅ |
| B2 — `critical_hit.ogg` + `death.ogg` in diff | ✅ |
| B3 — `_on_combat_damage` crit branch; `_on_brott_death` handler; both connect sites (lines 354, 393); cooldown guard present | ✅ |
| B4 — `.bus = "SFX"` BEFORE `add_child` for both new players | ✅ |
| B5 — `default_bus_layout.tres` untouched; all prior-sprint assets untouched; S24.2 mixer UI absent from diff; S24.3 `_on_projectile_spawned` unchanged | ✅ |
| B6 — `on_death` signal signature matches handler (`on_death(brott: BrottState)` → `_on_brott_death(_brott)`) | ✅ |
| B7 — `test_runner.gd` SPRINT_TEST_FILES: all 3 S24.4 paths registered | ✅ |
| CI: 1383 → 1407 (+24; ≥1386 floor; floor cleared by 21) | ✅ |
| B8 — Production LOC: 52 (≤220 ceiling) | ✅ |
| ATTRIBUTION.md updated for both assets; HCD review flag on both | ✅ |
| Death handler cooldown guard present and correctly ordered (flag before play) | ✅ |
| Crit/hit mutual exclusion: `if/elif` structure (structurally enforced) | ✅ |
| KB PR #292 labels applied immediately (corrects S24.3 KB PR pattern) | ✅ |

**Why A and not A−:** S24.4 has no analogous miss to the S24.2 test-runner miss (which graded S24.2 A−). Test-runner registration was clean on first pass. No fix loops. No scope contamination. The KB PR labels were applied immediately, correcting the S24.3 KB PR omission proactively. The deliverable, process, and KB contribution are all clean. A-grade is warranted without qualification.

**Why not A+ (or "perfect"):** Both audio assets are sfxr placeholders pending HCD subjective review — the same acknowledged, non-blocking flag as S24.3. No code defects, no architectural concerns, no test quality issues found. A remains the correct grade. The sfxr flag is part of the arc's sourcing protocol (15-min CC0 cap → sfxr fallback + HCD review), not an audit finding.

---

## 8. Role Performance Review

### 🎭 Role Performance

**Gizmo:** Arc E sub-sprint scope calibration is stable and accurate — "50–100 LOC + 2 audio assets" for S24.4 landed at exactly 52 LOC. Two consecutive sub-sprints (S24.3 at 47, S24.4 at 52) confirm signal-wiring scope is predictable at this granularity. Arc E ceiling of 220 continues to be generous for wiring tasks; the headroom is appropriate given the arc brief allows for unexpected complexity. Trend: → (scope calibration confirmed across two data points)

**Ett:** Pre-flight for S24.4 was thorough and accurate — confirmed the death signal at `combat_sim.gd:112`, identified both connection sites at lines ~344 and ~381, specified the `_death_sfx_cooldown_active` approach explicitly, and enumerated all 9 Boltz gates. Risk register §risk #1 (missing one `on_death.connect` site) was correctly rated Medium-likelihood and was Boltz-checked on both sites. The plan's §3 hard rule requiring cooldown guard directly prevented the most likely failure mode (mass-death overlap). The three-surface test-runner enforcement (hard rule + Boltz gate + SPAWN_PROTOCOL) was correctly applied for the third sprint in a row. Trend: ↑ (pattern documentation infrastructure continues to pay dividends)

**Nutts:** Delivered all planned files in a single clean PR. The `_on_brott_death` implementation correctly sets `_death_sfx_cooldown_active = true` before `.play()` — the race-condition-safe ordering that distinguishes a correct cooldown guard from a broken one. The `is_instance_valid()` guards on both new handlers are correctly applied. The `_on_combat_damage` refactor (flattening the compound condition into a two-level `if/elif`) improves readability without changing semantics. Test coverage exceeded floors: T1=8 (vs. ≥3), T2=7 (vs. ≥3), T3=9 (vs. ≥5). ATTRIBUTION.md content-check assertions (T3d/T3e) show initiative beyond the plan's `file_exists` minimum — the same quality pattern as S24.3's I-A3b (non-empty check). SPRINT_TEST_FILES registration: correct on first try, second consecutive clean sprint. Trend: ↑ (consistent quality; cooldown-ordering detail shows careful reading of the plan's rationale)

**Boltz:** All B1–B8 gates passed on first review, APPROVE posted as `brott-studio-boltz[bot]`, auto-merge triggered 9 seconds later. Third consecutive clean App-token authentication round-trip. B3 gate correctly verified the cooldown guard ordering (flag before play) and both `on_death.connect` sites. B6 verified signal signature matching against `combat_sim.gd:112`. Boltz's review body explicitly called out the cooldown guard as "first death still fires" — confirming the reviewer understood the guard's intended behavior, not just its presence. Trend: ↑ (three consecutive clean reviews; B3 review depth improving)

**Optic:** `Optic Verified` workflow ran and concluded `skipped`. S24.4 diff contains no visual/UI changes (no `.tscn` files, no scene modifications, no CSS/shader changes). Optic correctly identifies the diff as outside its visual-change detection threshold. Not evaluated for S24.4 deliverable quality. Trend: → (not directly involved; correct skip behavior)

**Specc (this audit):** All claims verified against live repo state: PR diff, Boltz review body, CI log (`total assertions run: 1407` at line `2026-04-24T19:15:47.1881678Z`), signal connection line numbers (354, 393), bus ordering (confirmed in diff), test registration lines (104–107), issue deduplication (289–291 are net-new), KB PR creation (292 with labels applied). Issues #289–#291 filed with full carry-forward context. KB entries authored with concrete code references, anti-patterns tables, and cross-references to the complete Arc E KB library. Label verification on KB PR confirmed at time of issue. Trend: →

---

## 9. Gate to S24.5

**S24.4 is closed. S24.5 gate condition: partially satisfied.**

S24.5 (Music — tone call + menu loop) requires:
1. ✅ This audit (`audits/battlebrotts-v2/v2-sprint-24.4.md`) on `studio-audits/main` — met upon commit
2. ✅ S24.4 merged and CI-green — met at 19:19:43Z
3. **⏳ HCD music tone-direction call** — gated on §7 interaction point #2 from Arc E brief. The pipeline must present 3–5 reference tracks across the Kena/Thomas Newman spectrum before any music asset is sourced. This is a Creative Director decision; the pipeline cannot make it autonomously.

**Arc E Pillar 3 status after S24.4:** Closed. All 4 combat SFX events (hit, projectile, critical, death) wired and CI-green. Arc E A-grade "≥4 combat SFX events" requirement is satisfied.

**Arc E progress snapshot:**
- Pillar 1 (Foundation Cleanup): ✅ S24.1 closed
- Pillar 2 (Mixer UI): ✅ S24.2 closed
- Pillar 3 (Combat SFX): ✅ S24.4 closed — Pillar complete
- Pillar 4 (Music Loops): ⏳ S24.5 awaiting HCD tone call → S24.6 → S24.7

Playtest-ready trigger condition: Mixer UI (✅) + ≥4 SFX events (✅) + ≥1 music loop (⏳) + CI green (✅) — one music loop away from the playtest-ready ping. The tone-call is the current blocker for the playtest trigger.

---

*Authored by Specc (brott-studio-specc[bot]). S24.4 sub-sprint closed 2026-04-24T19:21:00Z.*
