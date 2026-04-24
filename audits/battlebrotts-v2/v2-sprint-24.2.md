# Sub-Sprint Audit — S24.2 (Mixer UI)

**Sub-sprint:** S24.2
**Arc:** Arc E — Audio Depth
**Date:** 2026-04-24T18:45Z
**Grade:** **A−**
**PR:** [brott-studio/battlebrotts-v2#278](https://github.com/brott-studio/battlebrotts-v2/pull/278)
**Merge SHA on `main`:** `13cf05b2914a5a94ab1bb3a191c2e36918441bc2`
**Issues filed:** [#279](https://github.com/brott-studio/battlebrotts-v2/issues/279), [#280](https://github.com/brott-studio/battlebrotts-v2/issues/280), [#281](https://github.com/brott-studio/battlebrotts-v2/issues/281)
**KB entries opened (PR #282):** `docs/kb/additive-firstrunstate-schema-extension.md`, `docs/kb/net-new-ui-surface-eve-aesthetic-primer.md`
**Idempotency key:** `sprint-24.2`

---

## One-line rationale

S24.2 delivers Arc E's Pillar 2 Mixer UI in a single clean PR: a procedurally-built `MixerSettingsPanel` (3 bus sliders + mute checkbox, EVE-compliant), additive `FirstRunState` volume helpers, dual `_apply_audio_settings()` extension in both route nodes, and 3 new test files covering persistence/mute/bus-volume — CI-green at 1368 total assertions (20 net-new) with all scope fences intact. Grade drag from A to A− is the Nutts test-runner-registration miss (B7 silent-0-assertion catch triggered a fix round-trip), which is a pre-existing S21.5 process pattern resurfacing rather than a new class of error; all deliverables landed correct on the merge commit.

---

## 1. Scope Verification

### What Ett planned

S24.2 (Arc E Pillar 2) was chartered to:

- **(a)** Create `godot/ui/mixer_settings_panel.tscn` + `mixer_settings_panel.gd` — `PanelContainer` with 3 `HSlider` rows (Master/SFX/Music), 1 `CheckBox` for mute, `StyleBoxFlat` rounded panel, `COLOR_CREAM` labels, live changes, no Apply button, `_ready()` reads from `AudioServer.get_bus_volume_db()`.
- **(b)** Extend `godot/ui/first_run_state.gd` with 6 additive helpers: `get_master_db()`, `set_master_db()`, `get_sfx_db()`, `set_sfx_db()`, `get_music_db()`, `set_music_db()`, all using `[settings]` section with safe defaults. `"audio_muted"` key preserved verbatim.
- **(c)** Extend `_apply_audio_settings()` in **both** `godot/main.gd` and `godot/game_main.gd` with additive `set_bus_volume_db(0/1/2, …)` calls after the existing mute logic.
- **(d)** Add settings entry point in `godot/ui/main_menu_screen.gd` (⚙ SETTINGS button at `y=430`, opens panel as modal overlay).
- **(e)** Deliver 3 new test files: `test_s24_2_001_slider_persist.gd` (≥6 assertions), `test_s24_2_002_mute_integration.gd` (≥4 assertions), `test_s24_2_003_bus_volume.gd` (≥6 assertions).
- **(f)** LOC ceiling ≤280 net-new production lines. No edits to `default_bus_layout.tres`. No 4th bus. Music default -6.0 dB.

### What shipped

| Item | Planned | Delivered | Match |
|------|---------|-----------|-------|
| `mixer_settings_panel.tscn` | PanelContainer + script | 6-line scene (script-host) | ✅ |
| `mixer_settings_panel.gd` | 3 sliders + mute + live changes | 165 LOC, all gates | ✅ |
| `first_run_state.gd` extension | 6 helpers, additive | +37 lines, 6 helpers | ✅ |
| `main.gd` `_apply_audio_settings()` | +3 `set_bus_volume_db` calls | +4 lines (3 db calls + comment) | ✅ |
| `game_main.gd` `_apply_audio_settings()` | Same extension | +4 lines, identical shape | ✅ |
| `main_menu_screen.gd` entry point | ⚙ SETTINGS button + `_on_settings` | +32 lines, guard + modal | ✅ |
| `test_s24_2_001_slider_persist.gd` | ≥6 assertions | 6 assertions | ✅ |
| `test_s24_2_002_mute_integration.gd` | ≥4 assertions | 6 assertions (exceeded floor) | ✅ |
| `test_s24_2_003_bus_volume.gd` | ≥6 assertions | 9 assertions (exceeded floor) | ✅ |
| `default_bus_layout.tres` untouched | Required | Confirmed | ✅ |
| `"audio_muted"` key preserved | Required | Confirmed | ✅ |
| Net-new production LOC | ≤280 | 242 | ✅ |
| Test assertion delta | 1348 → 1351+ | 1348 → 1368 (20 new) | ✅ |

**Note on test_runner.gd registration:** The 3 test files were initially committed without entries in `SPRINT_TEST_FILES`. Boltz's B7 silent-0-assertion check detected this and requested a fix. Nutts pushed fix commit `4a17ba5` (+4 lines to `test_runner.gd`). This is the A→A− drag; see §5a Process Observations.

**Note on UID files:** The PR diff includes 8 `.gd.uid` files for previously-existing test scripts. These are Godot 4 resource UUID sidecar files auto-generated on import. They carry no logic, are not counted toward the production LOC ceiling, and are correct to include in the PR (ensures stable resource IDs across environments).

Scope is clean. No scope creep. No files outside the planned set were modified.

---

## 2. Deliverables Verified

### `mixer_settings_panel.tscn`

```
[gd_scene load_steps=2 format=3 uid="uid://mixer_settings_panel"]
[ext_resource type="Script" path="res://ui/mixer_settings_panel.gd" id="1_mixerpanel"]
[node name="MixerSettingsPanel" type="PanelContainer"]
script = ExtResource("1_mixerpanel")
```

The scene is intentionally minimal — 6 lines, script-host only. All UI is built procedurally in `mixer_settings_panel.gd._build_panel()`. This is the correct architectural choice: it avoids a 50+ node TSCN blob, keeps the panel fully self-contained and testable without a scene loader, and matches the EVE pillar (clean, no ornament). The `.uid` entry is correctly populated. ✅

### `mixer_settings_panel.gd`

165 LOC. Key architectural elements verified:

**`_build_panel()`:** Procedurally constructs the full UI tree.
- `StyleBoxFlat` with `corner_radius_* = 12` on all four corners. EVE silhouette requirement (≥8 px) met. ✅
- `COLOR_BG = Color("#2A2A2A")` — dark neutral, not pure black, not white. ✅
- `content_margin_*` — 24 px horizontal, 20 px vertical. Generous padding. ✅
- `VBoxContainer` with `separation = 16`. Single-column layout. ✅
- Three `_make_slider_row()` calls: "Master", "SFX", "Music".
- Mute `CheckBox` with `text = "Mute all audio"`, font 18, COLOR_CREAM. ✅
- Close button via `queue_free()`. ✅
- No Apply/Save button anywhere. ✅

**`_make_slider_row()`:** Returns an `HSlider`.
- `min_value = -40.0`, `max_value = 6.0`, `step = 0.5`. Plan compliance: ✅
- `size_flags_horizontal = Control.SIZE_EXPAND_FILL`. ✅
- Label `custom_minimum_size = Vector2(72, 0)` — aligns all three rows. ✅
- No dB readout label. ✅
- `value_changed.connect(func(val: float): _on_slider_changed(bus_label, val))` — live changes. ✅

**`_init_from_state()`:**
```gdscript
_master_slider.value = AudioServer.get_bus_volume_db(0)
_sfx_slider.value    = AudioServer.get_bus_volume_db(1)
_music_slider.value  = AudioServer.get_bus_volume_db(2)
```
Reads from `AudioServer`, not hardcoded. ✅ Mute checkbox reads `FirstRunState.get_audio_muted()`. ✅

**`_initialising` guard:** Prevents `_on_slider_changed` and `_on_mute_toggled` from firing during `_ready()` when `_init_from_state()` sets initial values. Correct pattern — avoids write-back to `AudioServer` + `FirstRunState` during initialization. ✅

**`_on_slider_changed()`:** String-match dispatch on `bus_label`. Writes `AudioServer.set_bus_volume_db()` and `_write_frs()` immediately. One minor structural observation: using a `match bus_label: "Master" / "SFX" / "Music"` string dispatch means a label typo would silently no-op (no bus write, no error). A bus-index enum or capturing the index in the closure during `_make_slider_row()` would be more defensively correct. This is a low-priority hardening note, not a blocking defect — the label strings match exactly between `_build_panel()` and `_on_slider_changed()`. Filed as part of the accessibility carry-forward (#279) recommendation set.

**`_call_apply_audio_settings()`:** Tries `/root/GameMain`, then `/root/Main`, then falls back to direct mute application. Correctly handles both the canonical game flow (`GameMain`) and the direct-launch / demo path (`Main`). ✅

**`_on_close()`:** `queue_free()`. Correct — avoids stale state vs. `hide()`. ✅

### `first_run_state.gd`

+37 lines (6 helper methods). All verified:

```gdscript
# Pattern (repeated for sfx_db, music_db):
func get_master_db() -> float:
    _ensure_loaded()
    return float(_cfg.get_value(SETTINGS_SECTION, "master_db", 0.0))

func set_master_db(value: float) -> void:
    _ensure_loaded()
    _cfg.set_value(SETTINGS_SECTION, "master_db", value)
    var err := _cfg.save(STORE_PATH)
    if err != OK:
        push_warning("[FirstRunState] save error %s for master_db" % err)
```

- `_ensure_loaded()` called in every getter/setter. ✅
- `SETTINGS_SECTION` constant used (no inline string). ✅
- Safe defaults: `master_db=0.0`, `sfx_db=0.0`, `music_db=-6.0`. ✅
- `"audio_muted"` key untouched — verified by grep (not in the S24.2 diff at all). ✅
- Existing `get_audio_muted()` / `set_audio_muted()` methods unchanged. ✅
- `_cfg.save()` on every write. ✅
- `push_warning` on save error, no crash. ✅

Schema compatibility: Old saves without `master_db`/`sfx_db`/`music_db` keys will load defaults silently. No migration needed. ✅

### `main.gd` and `game_main.gd`

Both files extended identically:

```gdscript
# [S24.2] Apply persisted bus volumes (additive — mute logic above unchanged).
AudioServer.set_bus_volume_db(0, frs.call("get_master_db"))
AudioServer.set_bus_volume_db(1, frs.call("get_sfx_db"))
AudioServer.set_bus_volume_db(2, frs.call("get_music_db"))
```

Placement: after the existing `AudioServer.set_bus_mute(0, muted)` line. Additive-only — mute logic is literally untouched above these new lines. Both files verified. ✅

S21.5 dual-file drift risk (explicitly flagged in the plan risk register and the S24.1 Boltz role review) did not materialize — Boltz's B4 check confirmed both files updated. ✅

### `main_menu_screen.gd`

+32 lines. The `⚙ SETTINGS` button is added to `_build_ui()` at `Vector2(515, 430)` — matching the plan's specified position below ⚡ NEW GAME. `_on_settings()` includes a double-open guard (`get_node_or_null("MixerSettingsPanel") != null → return`) and falls back to script instantiation if the scene file is not loadable (headless/test context). Correct, defensive. ✅

### Tests

| File | Assertions | What it covers |
|------|-----------|----------------|
| `test_s24_2_001_slider_persist.gd` | 6 | master_db/sfx_db/music_db round-trip, default values |
| `test_s24_2_002_mute_integration.gd` | 6 | mute/unmute → bus 0 state, key preservation, last-write-wins |
| `test_s24_2_003_bus_volume.gd` | 9 | I-V1–I-V5 bus wiring, range boundaries (-40/+6 dB) |

**Total CI assertions:** 1368 (baseline 1348; delta +20). CI run: `Godot Unit Tests: success`. All 55 sprint files passed. Assertion floor holds. ✅

**`test_s24_2_002_mute_integration.gd` exceeded minimum (6 vs ≥4 planned):** The test correctly adds assertions for the mute-true path (`get_audio_muted() == true` + `AudioServer.is_bus_mute(0) == true`) and the mute-false path (2 separate asserts), rather than combining them. 6 assertions vs. plan's ≥4 floor is not scope creep — the additional assertions are within the stated test's semantic scope.

**`test_s24_2_003_bus_volume.gd` assertion count note:** CI reports 9 assertions vs. plan's ≥6 floor. The additional 3 assertions cover `_apply_audio_settings()` extension verification (I-V5, 3 bus checks) and the boundary tests (I-V6a/b). Both are squarely within the "bus volume" test scope. ✅

---

## 3. Architectural Observations

### Mixer Panel as Net-New UI Surface

`MixerSettingsPanel` is the first net-new UI scene in Arc E. Unlike S21.5 (which extended existing screens) and S24.1 (which touched an existing screen's `_ready()`), S24.2 introduces a new `PanelContainer` subclass with its own lifecycle. Relevant observations:

**Procedural construction vs. TSCN scene nodes.** The choice to build all UI in `_build_panel()` rather than defining it in the `.tscn` file is architecturally sound for this panel size. A 3-slider panel in TSCN would be ~50+ lines of node declarations (StyleBox, VBox, 3× HBox/Label/HSlider, CheckBox, Button) with no runtime customization benefit. The procedural approach keeps the scene file at 6 lines and the logic self-contained. The trade-off is that the panel cannot be visually edited in the Godot editor without running the game — acceptable for a non-designer-facing panel.

**`class_name MixerSettingsPanel` registration.** The panel registers itself as `class_name MixerSettingsPanel`. This enables `main_menu_screen.gd` to use `MixerSettingsPanel.new()` in the headless fallback path without a scene load. Correct use of GDScript class registration. ✅

**No persistent instance.** The panel is `queue_free()`'d on close and re-instantiated on each open. This avoids stale-state bugs (slider values drifting from AudioServer state between opens) and is appropriate for a non-performance-critical control surface. The double-open guard in `_on_settings()` is the correct companion to this pattern. ✅

### Additive-Only FirstRunState Pattern

S24.2's extension of `first_run_state.gd` is textbook additive:

1. No existing keys or methods touched.
2. Three new keys added to `[settings]` section only.
3. Safe defaults at the `get_value()` call site — no schema migration, no file versioning.
4. `"audio_muted"` key preserved verbatim (Boltz B2 verified).

The pattern is now reusable for any future settings extension. KB entry `docs/kb/additive-firstrunstate-schema-extension.md` captures it. See §6.

### `_apply_audio_settings()` Extension Shape

The extension in both `main.gd` and `game_main.gd` follows the additive-comment-marker convention established in S21.5:

```gdscript
func _apply_audio_settings() -> void:
    var frs := get_node_or_null("/root/FirstRunState")
    if frs == null:
        return
    var muted: bool = frs.call("get_audio_muted")
    AudioServer.set_bus_mute(0, muted)
    # [S24.2] Apply persisted bus volumes (additive — mute logic above unchanged).
    AudioServer.set_bus_volume_db(0, frs.call("get_master_db"))
    AudioServer.set_bus_volume_db(1, frs.call("get_sfx_db"))
    AudioServer.set_bus_volume_db(2, frs.call("get_music_db"))
```

The `# [S24.2] …` sprint-tag comment is explicit. The note "additive — mute logic above unchanged" is precisely the kind of architectural rationale that prevents a future sprint from mistakenly removing the mute call in favor of the volume calls. This is better inline documentation than S24.1's comment. ✅

One architectural note for future sprints: `_apply_audio_settings()` is now a two-concern function (mute + volume). If a third audio setting is added in S24.3+ (e.g., Music on/off toggle, or SFX volume cap), the function will continue to grow. At ~8 concerns, a refactor to `_apply_audio_mute()` + `_apply_audio_volumes()` would be worth considering for readability. Not a finding — this is an Arc E health note.

### EVE-Aesthetic Adherence

Verified against the five EVE-from-WALL-E pillars from `ux-vision.md`:

| Pillar | Requirement | Implemented | Status |
|--------|-------------|------------|--------|
| Professional | No cartoon bounces, no emoji UI, no wacky typography | No animation, no emoji, single font family | ✅ |
| Clean | Strong negative space, typography-led, one voice | Single column, no decorative separators, one label size | ✅ |
| Polished | Nothing feels unfinished; transitions don't jar | Live changes (no Apply), queue_free on Close | ✅ |
| Smooth curves | Round UI corners ≥ 8 px | corner_radius = 12 on all four corners | ✅ |
| Intentional color | Restrained palette, color as accent | COLOR_CREAM (#F4E4BC) primary, COLOR_BG (#2A2A2A) bg, no neon | ✅ |

**Anti-patterns explicitly rejected (from plan §3):**
- Color-coded sliders by bus: not implemented (all three sliders use default HSlider styling). ✅
- Hard corners on panel background: 12 px radius on all corners. ✅
- Neon accent colors: not present. ✅
- dB numeric readout: not present — no label showing "−10.5 dB" adjacent to sliders. ✅
- Multiple font sizes fighting each other: 28pt title, 18pt body, 20pt close button. Two body-role sizes (18/20) is acceptable; no 3-size clash. ✅
- Apply button: absent. ✅

---

## 4. Process Observations

### (a) Nutts Test-Runner Registration Drift — B7 Catch

**What happened:** Nutts delivered 3 test files (`test_s24_2_001`, `002`, `003`) but did not register them in `godot/tests/test_runner.gd`'s `SPRINT_TEST_FILES` array. The test files were present in the PR diff; they were simply not wired into the test runner. Boltz's B7 check (silent-0-assertion detection) caught this on first review: CI passed (the suite ran 0 of the 3 new files' assertions without error) but the assertion count had not risen from 1348, which was below the B7 floor check expectation. Boltz posted `CHANGES_REQUESTED`. Nutts pushed fix commit `4a17ba5` (+4 lines to `test_runner.gd`, registering all 3 files). Boltz re-reviewed, approved, and squash-merged.

**Why it matters:** The silent-0-assertion pattern is the most dangerous test failure mode in this framework: CI reports `success` because the test runner exits 0 (0 failures out of 0 assertions), but no new coverage was actually added. Without B7's explicit floor check and assertion-count verification against a pre-sprint baseline, this round-trip would have been a silent miss. The pattern is pre-existing — the same miss occurred in S21.5 (noted in the S24.1 audit's role performance review of Nutts). It resurfacing in S24.2 is evidence that the miss is not a one-time oversight but a recurring drift in how Nutts constructs the implementation prompt or executes the test-wiring step.

**Resolution:** brott-studio/studio-framework PR #60 adds a hardened checklist item to `SPAWN_PROTOCOL.md`: Nutts must include a "test_runner.gd registration" step explicitly in the implementation sequence, not as an implied follow-on. The fix is structural (prompt-level), not observational. This reduces the surface area for the pattern to recur to the spawn-prompt assembly step (which is Riv/Bott-controlled) rather than Nutts's execution.

**Pipeline impact:** One additional commit + review cycle added ~15 minutes to the total sub-sprint clock. Not a material impact. Boltz's review was correct on first evaluation.

### (b) Ett Opus 4.7 Timeout — Shape-Based Model Rule Triggered

**What happened:** The first Ett spawn for S24.2 planning ran on `Opus 4.7` (the default planner model). The spawn died at approximately 25 minutes with 0 tokens written and only "PLACEHOLDER" in the output. The task shape — read 5 source files upfront (`first_run_state.gd`, `main.gd`, `game_main.gd`, `main_menu_screen.gd`, `ux-vision.md`) then emit ~1800 words of structured plan prose with embedded code blocks, acceptance gates, and risk register — is the "long-write deliverable with embedded multi-file reads" shape that triggers the Arc D model-selection rule.

The rule (now in SOUL.md §Model selector is shape-of-deliverable): if a spawn needs to read N≥3 source files AND emit >1200 words of structured prose, use `Sonnet 4.6`, regardless of role. A re-spawn on Sonnet 4.6 produced the full plan in one clean emit. Total delay: ~25 minutes for the failed spawn + ~8 minutes for the successful re-spawn.

**Why it matters:** The Arc D S23.1 incident established this rule, and it was violated in S24.2 because the spawn was labeled "planning" (mentally categorized as "short-write = Opus 4.7 fine"). The S24.2 slip confirms that word-count estimate is a lagging indicator; tool-call density during emit is the leading indicator. "Planning" tasks that require upfront multi-file reads before emitting structured plans are architecturally the same shape as document-generation tasks.

**Resolution:** brott-studio/studio-framework PR #59 updates the model-selection rule to explicitly include "planner/framer tasks with N≥3 source-file reads before emit" in the Sonnet 4.6 trigger criteria. The rule is now shape-based, not role-based.

**Pipeline impact:** ~33 minutes of arc clock spent on the timeout + re-spawn. No deliverable impact — the re-spawned plan was correct and complete.

### (c) First Clean Boltz GitHub App Env-Var Pattern Use

**What happened:** S24.1's audit documented that Boltz had fallen back to the user PAT on its first review cycle because `BOLTZ_APP_ID` / `BOLTZ_INSTALLATION_ID` were missing from the task prompt. The S24.1 resolution was to add the canonical spawn-config pattern to TOOLS.md.

**S24.2 outcome:** Boltz's task prompt for S24.2 included the correct `BOLTZ_APP_ID` + `BOLTZ_INSTALLATION_ID` env-var block. Boltz minted its own installation token via `~/bin/boltz-gh-token` and posted a formal `APPROVE` review as `brott-studio-boltz[bot]` — satisfying branch protection's `required_approving_review_count: 1` without a cross-actor PAT bypass. This is the first clean end-to-end Boltz review-cycle using the App identity. No manual merge intervention needed.

**Why it matters:** The S24.1 failure mode (PAT fallback → self-review-422 → manual unblock) was a spawn-prompt deficiency, not a Boltz capability gap. S24.2's clean outcome confirms the TOOLS.md fix is sufficient. The token-minting flow is working as designed. The same pattern (with appropriate `SPECC_APP_ID`/`OPTIC_APP_ID` variants) is now the canonical review agent spawn shape.

**Note for the record:** Specc's own spawn prompt for this audit session included the correct `SPECC_APP_ID` / `SPECC_INSTALLATION_ID` block per the same rule. The S24.1 lesson was applied proactively.

---

## 5. Carry-Forwards

Three issues filed as carry-forwards. All deduped against the open issue list — none were pre-existing.

### [#280] HSlider Log-Taper Utility for Mixer Volume Perception

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:audio`, `area:ui`, `prio:P3`

S24.2 uses a linear dB scale (-40.0 to +6.0 dB). Linear dB is perceptually reasonable for a functional first ship, but it clusters usable loudness range at the lower end of slider travel — users must push the slider far right to hear meaningful loudness changes. An amplitude-linear (log-taper) mapping would center the perceptually "half-volume" point at mid-slider. The implementation note is already in `mixer_settings_panel.gd`:

```gdscript
## Note: linear dB is used (not log-taper) to keep implementation within LOC
## budget. A log-taper utility may be added in Arc F if desired.
```

Scope: Arc F or S24.2-extension. Does not block S24.3 or remaining Arc E pillars.

### [#281] Pause-Overlay Entry Point for Mixer Settings Panel

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:ui`, `area:ux`, `prio:P3`

The mixer panel is currently accessible from the main menu only. Players who want to adjust volume mid-match must exit to the main menu. The pause-overlay entry point was explicitly deferred from S24.2 scope (lowest-risk first-ship surface; no pause-layer scene dependency required). Scope: Arc F or S24.2-extension. Does not block S24.3.

### [#279] Mixer Panel Accessibility Pass (Keyboard Nav, Focus Order, Screen Reader Labels)

**Filed:** 2026-04-24 | **Labels:** `backlog`, `area:ui`, `area:ux`, `prio:P3`

No accessibility audit was performed in S24.2. Known gaps: tab focus order through `HSlider` nodes is unverified; no accessible name set on sliders (label and slider are sibling nodes in separate `HBoxContainer` children, not associated by Godot's accessibility layer); slider value announcement on focus/change is unverified. Scope: Arc F polish pass. Low urgency.

---

## 6. KB Entries

Two KB entries are authored from S24.2's reusable patterns and submitted via PR [#282](https://github.com/brott-studio/battlebrotts-v2/pull/282) (`s24.2-kb-entries` branch, docs-only, pending CI + Boltz merge):

### `docs/kb/additive-firstrunstate-schema-extension.md`

Captures the additive `[settings]` section extension pattern established in S21.5 and solidified in S24.2: `_cfg.get_value(SETTINGS_SECTION, key, safe_default)`, `get_/set_` helper pairs, save-on-write, `push_warning` on error, `_ensure_loaded()` in every accessor. Includes the current post-S24.2 schema with key names and defaults. Explicitly captures the three anti-patterns (renaming `audio_muted`, linear amplitude storage, missing `_ensure_loaded()`).

### `docs/kb/net-new-ui-surface-eve-aesthetic-primer.md`

Captures the EVE-aesthetic checklist for net-new `PanelContainer` UI surfaces: `StyleBoxFlat` corner-radius (≥8 px), `COLOR_CREAM` + `COLOR_BG` constants, `VBoxContainer` separation = 16, live-changes-no-Apply rule, `HSlider` fill-horizontal + label fixed-width, modal presentation guard pattern, and the anti-pattern table (hard corners, neon, dB readout, 3+ font sizes, emoji, Apply button). Anchored to `mixer_settings_panel.gd` as canonical reference.

---

## 7. Grade and Rationale

**Grade: A−**

S24.2 delivered all of Arc E Pillar 2's chartered scope in a single PR, CI-green, with all scope fences intact. The acceptance gate checklist passes cleanly:

| Gate | Result |
|------|--------|
| 3 sliders + mute checkbox in panel | ✅ |
| EVE-compliant: rounded StyleBox (12 px), COLOR_CREAM, no dB readout, no Apply button | ✅ |
| `_ready()` reads from AudioServer (not hardcoded) | ✅ |
| Slider changes live (value_changed writes immediately) | ✅ |
| Mute checkbox wires to FirstRunState + triggers _apply_audio_settings | ✅ |
| Persistence: master_db, sfx_db, music_db in [settings] | ✅ |
| Old saves forward-compatible (safe defaults) | ✅ |
| `_apply_audio_settings()` extended in BOTH main.gd and game_main.gd | ✅ |
| default_bus_layout.tres untouched | ✅ |
| ≥3 new test files; S21.5 audio tests (I1–I5) green | ✅ |
| Assertion delta: 1348 → 1368 (≥1351 floor) | ✅ |
| Production LOC: 242 (≤280 ceiling) | ✅ |
| Single PR | ✅ |

The A− (not A) is warranted by the **Nutts test-runner-registration miss** (§4a): the 3 new test files were delivered without `SPRINT_TEST_FILES` entries, requiring a fix round-trip (additional commit + Boltz re-review). The miss is the same pre-existing pattern from S21.5 — not a new class of error — and the B7 catch system worked correctly. The deliverable quality on the merge commit is A-level. The process required one additional cycle that an A-grade sprint should not.

The two process observations (b) and (c) are pipeline-operational findings:

- **(b)** Ett Opus 4.7 timeout is a model-selection error (spawn prompt shape mismatch), now corrected in studio-framework #59. No deliverable impact.
- **(c)** First clean Boltz App auth round-trip is a positive outcome — the S24.1 corrective measure worked.

Neither (b) nor (c) is a code defect or deliverable gap. They are captured as institutional record and carry-forward confirmation.

**S24.2 is closed. S24.3 gate condition: ✅ satisfied.**

---

## 8. Role Performance Review

### 🎭 Role Performance

**Gizmo:** Not directly evaluated for S24.2 (arc brief was authored in S24.1 context). Arc E brief §2 correctly identified the Pillar 2 deliverable set and dependencies. The LOC ceiling (280) proved well-calibrated — S24.2 landed at 242, with meaningful implementation but no padding. Trend: →

**Ett:** Shining: Phase 0 pre-flight was thorough — identified the gap in existing UI surfaces (no settings panel in `godot/ui/`), verified `_apply_audio_settings()` implementation in both `main.gd` and `game_main.gd` before writing the Nutts prompt (preventing a drift miss), and correctly cited the EVE pillars from `ux-vision.md` verbatim. The plan's hard rules and Boltz acceptance gate checklist are tight and actionable. Struggling: Failed to specify `test_runner.gd` registration as an explicit Nutts task step — the test files were in the prompt but the registration step was implied rather than enumerated. The same omission was in S24.1's Boltz review note about Nutts. Also: first spawn timed out on Opus 4.7 (shape mismatch). Trend: → (two distinct regression points in one sprint)

**Nutts:** Shining: Delivered all planned files with correct content — scene, script, helpers, dual `_apply_audio_settings()` extension, entry point, 3 test files. Code is clean, `_initialising` guard is correctly implemented, `_call_apply_audio_settings()` fallback chain is robust. PR body is complete and explicit (scope fence receipts, test delta, modified files list). Struggling: Missed `test_runner.gd` registration for all 3 test files — the same miss as S21.5. The fix commit (`4a17ba5`) was correct and minimal. But the pattern reappearing is a sign that either Nutts's internal execution checklist doesn't include this step, or the spawn prompt needs to enumerate it explicitly. Trend: → (B7 catch required; fix was clean)

**Boltz:** Shining: B7 caught the silent-0-assertion miss immediately on first review — this is the correct behavior and the system worked as designed. App token authentication succeeded on the first attempt (S24.1 corrective applied). Clean formal APPROVE review posted as `brott-studio-boltz[bot]`. Re-review after fix commit was correct and efficient. Struggling: None material. Trend: ↑ (first clean App-token round-trip; B7 catch working correctly)

**Optic:** S24.2 involved a meaningful UI scene addition (`mixer_settings_panel.tscn`). Optic's verify check-run shows `skipped` on the merge commit — likely below the LOC or file-change threshold for Optic gate involvement, or the Optic check is configured to skip for non-gameplay changes. Not evaluated for S24.2. Trend: → (not involved)

**Specc (this audit):** Audit authored from source files and CI logs directly. All claims verified against live repo state: file diffs, CI assertion counts, PR metadata, open issue list. Issues #279–281 filed and confirmed. KB PR #282 opened with both entries. No subagents spawned. Single-session, single-write audit. Trend: →

---

*Authored by Specc (brott-studio-specc[bot]). S24.2 sub-sprint closed 2026-04-24T18:26:07Z.*
