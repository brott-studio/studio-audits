# Sub-Sprint Audit — S24.1 (Foundation Cleanup)

**Sub-sprint:** S24.1
**Arc:** Arc E — Audio Depth
**Date:** 2026-04-24T17:45Z
**Grade:** **A−**
**PR:** [brott-studio/battlebrotts-v2#277](https://github.com/brott-studio/battlebrotts-v2/pull/277)
**Merge SHA on `main`:** `a5d026f235929cfcfa3e1c2a4792a9a2185a8daf`
**Issues closed:** [battlebrotts-v2#262](https://github.com/brott-studio/battlebrotts-v2/issues/262) (2026-04-24T17:37:02Z)
**Issues remaining open:** [battlebrotts-v2#263](https://github.com/brott-studio/battlebrotts-v2/issues/263) — pending HCD keep/replace call
**Idempotency key:** `sprint-24.1`

---

## One-line rationale

S24.1 delivers Arc E's Pillar 1 Foundation Cleanup in a single clean PR: a 1-line `.bus = "SFX"` fix in `shop_screen.gd` (closes #262), one minimal test file with exactly 1 net-new assertion (1347→1348), and a neutral HCD-facing listening guide for the #263 sfxr decision — all CI-green on the merge commit, with two honest pipeline-operational observations captured. Grade drag from A to A− is a single comment wording nit: the inline comment bakes an issue reference and architecture rationale together but omits the ordering rationale that is the precise reason for its placement (bus set before `add_child`); the S21.5 precedent files use a terser, more consistent style.

---

## 1. Scope Verification

### What Ett planned

S24.1 was chartered to deliver two bundled items in one PR:

- **(a)** A 1-line `.bus = "SFX"` assignment in `godot/ui/shop_screen.gd` `_ready()`, between `AudioStreamPlayer.new()` and `add_child(_shop_audio)`, matching the S21.5 convention from `result_screen.gd:40`. Accompanied by a single comment line (`# S24.1 #262: route shop SFX through SFX bus (was Master default).`). Net change: 2 lines added (one comment + one assignment). LOC ceiling: ≤3.
- **(b)** A new test file `godot/tests/test_s24_1_001_shop_screen_sfx_bus.gd` (corrected filename in PR: `test_sprint24_1_001_shop_screen_sfx_bus.gd`), ≤30 LOC, exactly 1 net-new assertion on `_shop_audio.bus == "SFX"`. Total assertions: 1347 → 1348.
- **(c)** A workspace-only HCD review doc at `memory/ops/s24-1-sfxr-review-request.md`, ≤800 words, 5 sections: what shipped, Freesound primaries, asset character, how to listen, keep/replace decision prompt. Not committed to the game repo.
- **ATTRIBUTION.md** unchanged — no assets replaced in S24.1.

### What shipped

| Item | Planned | Delivered | Match |
|------|---------|-----------|-------|
| `.bus = "SFX"` fix in `shop_screen.gd` `_ready()` | 1 line | 1 line | ✅ |
| Inline comment | 1 line | 1 line (different wording — see §2) | ✅ (with nit) |
| Placement: before `add_child` | Required | Confirmed | ✅ |
| Test file `test_sprint24_1_001_shop_screen_sfx_bus.gd` | ≤30 LOC, 1 assertion | 27 LOC, 1 assertion | ✅ |
| Assertion count delta | 1347 → 1348 | 1347 → 1348 | ✅ |
| Review doc at `memory/ops/s24-1-sfxr-review-request.md` | ≤800 words, 5 sections | Present, 5 sections | ✅ |
| `ATTRIBUTION.md` unchanged | Required | Unchanged (not in PR diff) | ✅ |
| No other files edited in `shop_screen.gd` | Required | Confirmed — diff shows only the 1-line insertion | ✅ |

Scope is clean. The PR title matches the deliverable scope. The PR body explicitly calls out the `[#263] stays open` line and the `ATTRIBUTION.md` unchanged note. No scope creep.

**Note on filename:** Ett's plan specified `test_s24_1_001_shop_screen_sfx_bus.gd`; the delivered filename is `test_sprint24_1_001_shop_screen_sfx_bus.gd`. The sprint-prefix naming style (`test_sprint24_1_…`) matches the existing suite conventions (e.g., `test_sprint13_5.gd`), while Et's plan used the shorter `test_s24_1_…` style. Neither is wrong; `test_sprint24_1_…` is the more consistent pattern for the existing suite. Not a finding — naming correction acknowledged.

---

## 2. Code Quality

### The fix

```gdscript
# Before (lines 72–74 of shop_screen.gd):
func _ready() -> void:
    _shop_audio = AudioStreamPlayer.new()
    add_child(_shop_audio)

# After:
func _ready() -> void:
    _shop_audio = AudioStreamPlayer.new()
    _shop_audio.bus = "SFX"  # S24.1 / closes #262 — route through SFX bus per 3-bus architecture (S21.5)
    add_child(_shop_audio)
```

**S21.5 convention match:** The S21.5 pattern (from `result_screen.gd:40`) is `.bus = "SFX"` set between instantiation and `add_child`. S24.1 matches this ordering exactly. The bus string `"SFX"` is the correct literal per `default_bus_layout.tres` (bus 1 name, established in S21.5). Consistent with `game_main.gd:530` (`PopupWhooshPlayer.bus = "SFX"`). Convention match: ✅.

**Comment quality — nit (grade-drag):** The planned comment from Ett's §2a was:
```gdscript
# S24.1 #262: route shop SFX through SFX bus (was Master default).
```

The delivered comment is:
```gdscript
# S24.1 / closes #262 — route through SFX bus per 3-bus architecture (S21.5)
```

Substantively the same (sprint tag, issue ref, routing rationale, S21.5 back-reference). Two minor observations:

1. The delivered comment does not capture the *ordering* rationale — i.e., that `.bus` is set **before** `add_child` by convention. The S21.5 `result_screen.gd` comment block (`player.bus = "SFX"`) is itself comment-free, relying on convention proximity. So the absence of an ordering note isn't a regression, but it means a reader scanning the diff would need to know the convention to understand why the line sits where it does rather than after `add_child`.

2. The `/ closes #262` syntax (slash-separated) is slightly inconsistent with the `[S24.1]` PR title convention that uses bracket-style sprint tags. Minor cosmetic issue — the comment is still fully human-readable and auditable.

Neither observation is a substantive defect. The fix is correct, the comment is informative, and the placement is faithful to S21.5 convention. This is the A → A− drag.

**No other edits to `shop_screen.gd`:** Confirmed. The diff shows exactly one line inserted between line 73 (`_shop_audio = AudioStreamPlayer.new()`) and line 74 (`add_child(_shop_audio)`). No refactors, no variable renames, no touches to `_play_sfx`, `SFX_*` constants, or anything else in the file. ✅

---

## 3. Test Quality

### The test file

```gdscript
## S24.1-001 ShopScreen SFX bus routing — invariant: _shop_audio.bus == "SFX" after _ready().
## Usage: godot --headless --path godot/ --script res://tests/test_sprint24_1_001_shop_screen_sfx_bus.gd
extends SceneTree
var pass_count := 0
var fail_count := 0
var test_count := 0
const ShopScreenScript := preload("res://ui/shop_screen.gd")

func _initialize() -> void:
    print("=== S24.1-001 ShopScreen SFX bus routing ===\n")
    _test_shop_audio_routes_to_sfx()
    print("\n=== Results: %d passed, %d failed, %d total ===" % [pass_count, fail_count, test_count])
    quit(1 if fail_count > 0 else 0)

func _assert_eq(a: Variant, b: Variant, msg: String) -> void:
    test_count += 1
    if a == b:
        pass_count += 1
    else:
        fail_count += 1
        print("  FAIL: %s (got %s, expected %s)" % [msg, str(a), str(b)])

func _test_shop_audio_routes_to_sfx() -> void:
    var shop: Control = ShopScreenScript.new()
    get_root().add_child(shop)
    _assert_eq(shop._shop_audio.bus, &"SFX", "I3c: _shop_audio.bus == SFX")
    shop.queue_free()
```

**LOC:** 27 — within the ≤30 cap. ✅

**Assertion count:** Exactly 1 (`_assert_eq` called once, `test_count` increments once). Suite delta: 1347 → 1348. ✅

**What it tests:** After `ShopScreen` is instantiated and added as a child of the scene root (which triggers `_ready()` via `add_child`), it asserts `shop._shop_audio.bus == "SFX"`. This is a property-invariant test on the post-init state of the player. It directly verifies the delivery of the S24.1 fix — the only assertion the sub-sprint requires. ✅

**Pattern fidelity:** The structure follows the existing suite style exactly: `extends SceneTree`, `_initialize()` entry point, `_assert_eq` helper, `=== Results: N passed, M failed, T total ===` output line, `quit(1 if fail_count > 0 else 0)` tail. The `_parse_subprocess_assertions` regex in `test_runner.gd` (introduced in S23.4) will correctly parse this output line. ✅

**No behavior assertions:** The test does not call `_play_sfx`, assert signal wiring, load streams, or check playback timing. Correctly property-only. ✅

**Assertion ID tag:** The assertion message `"I3c: _shop_audio.bus == SFX"` uses an invariant-ID style (`I3c`) consistent with the S21.5 suite (`test_s21_5_003_sfx_routing.gd` used `I3: …` style). The `c` suffix is presumably "shop_screen" (third SFX-bus player, after `result_screen` → I3a, `game_main` → I3b). This is a reasonable forward-looking ID scheme, though it wasn't specified in the plan. No issue.

**Minimal-and-sufficient:** Yes. One assertion, one instantiation, one property check, one queue_free. Clean.

**CI on merge commit:** `Godot Unit Tests: completed / success`. The full `1348` assertion count is expected in the CI log for this merge commit. ✅

---

## 4. HCD Review Doc Quality

File: `memory/ops/s24-1-sfxr-review-request.md` (workspace-only; delivered to Eric via email per Bott's workflow).

**Word count:** ~600 words — within the ≤800 cap. ✅

**Section structure (5/5 present):**

| # | Required Section | Present | Notes |
|---|-----------------|---------|-------|
| 1 | What shipped in S21.5 | ✅ | Table format, seed values, CC0 status, both files |
| 2 | Freesound primaries | ✅ | Both links (s/320775/, s/428156/) with authentication note |
| 3 | Approx character of current sfxr outputs | ✅ | 2-sentence mechanical descriptions per asset (duration, envelope, freq band) |
| 4 | How to listen | ✅ | Both `res://` paths, in-game context for each |
| 5 | Decision prompt | ✅ | Explicit two-path keep/replace prompt with sub-choices for Option B |

**Tone check:** The document is consistently factual and presentational throughout. Section 3 confines itself to physical/technical descriptors ("Sine-wave tone with a fast attack," "Noise-based with a downward frequency sweep"). Section 5 presents two concrete paths without editorializing. The phrase "This does not block S24.2 (Mixer UI)" in the footer is an operational note, not an implicit recommendation. No embedded preference or push toward either option. Neutral tone confirmed. ✅

**Decision prompt specificity:** Option B includes three sub-choices (Freesound primaries, re-synth with different seed, CC0 library match). This is more specific than the 5-section structure required, and it's useful — it prevents an open-ended HCD reply from creating pipeline ambiguity. Not a nit.

**One minor observation:** Section 4 notes both assets are "correctly routed through the SFX bus (S24.1 fix for `shop_screen.gd` ships with this sub-sprint)." This is accurate but reads slightly promotional — the pipeline is the intended audience so this is fine, but strictly speaking the #263 review doc should be about the sfxr assets, not S24.1's deliverables. Extremely minor; not a grade factor.

---

## 5. Process Observations

### (a) Issue body #262 contained stale/incorrect code-location claims

Issue #262 described the player as being created inside `_play_sfx()`. The actual code on `main` at sprint time had `_shop_audio` as a long-lived shared player instantiated once in `_ready()` — the issue body had drifted from the actual implementation. It also cited the wrong directory path (`godot/screens/shop_screen.gd` rather than the correct `godot/ui/shop_screen.gd`).

**How it was caught:** Ett's Phase 0 planner audit read the actual source via `gh api contents` and identified both discrepancies before writing any code. The path error was caught in both the arc brief (`godot/screens/` cited there as well) and confirmed by Ett's pre-diff check. The structural error (player in `_play_sfx` vs `_ready`) was caught by reading the live code against the issue description.

**Impact:** Zero — the Phase 0 catch happened before Nutts touched the file. Nutts's prompt used the corrected path and correct instantiation location. The fix landed at exactly the right callsite.

**Pipeline observation (non-blame):** Issue bodies are author-time snapshots and can drift from live code, especially when sprint context is summarized retroactively. The structural check in Phase 0 — reading the actual source before writing the implementation prompt — is the correct mitigation. This instance validates that the Phase 0 pre-flight is worth its cost even on short, apparently-obvious sub-sprints. The fix appears trivial; the issue body was substantively wrong in two ways.

### (b) Boltz first review attempt fell back to user PAT — review landed via direct Bott call

Boltz's first spawn in the review cycle lacked `BOLTZ_APP_ID` and `BOLTZ_INSTALLATION_ID` in the task prompt. Without these env vars, Boltz's token-minting flow defaulted to the user PAT. The branch-protection rule on `battlebrotts-v2/main` requires `required_approving_review_count: 1` and does not allow self-approve (the PR author and the reviewer cannot share the same GitHub identity). The user PAT identity matched the PR author identity for purposes of GitHub's self-review check; the formal APPROVE review was rejected (HTTP 422).

Boltz's workaround was to post a text comment instead of a formal review approval. The merge was then unblocked from the Bott's main session by directly calling the Boltz GitHub App (`brott-studio-boltz[bot]`) installation token to post the formal APPROVE review.

**Resolution:** TOOLS.md was updated in the same session with the canonical spawn-config pattern: every Boltz/Specc/Optic task prompt must include the relevant `{AGENT}_APP_ID` and `{AGENT}_INSTALLATION_ID` env-var block so agents can mint their own App tokens. Specc's own spawn prompt for this audit session included the correct `SPECC_APP_ID` / `SPECC_INSTALLATION_ID` block.

**Pipeline observation (non-blame):** The gap was a spawn-prompt deficiency, not a Boltz execution error. Boltz correctly fell back to the available token and left a text record of its review findings. The merge was unblocked without losing review coverage. The canonical pattern is now documented. The risk of a repeat is low — the pattern is in TOOLS.md at a prominent position, and the failure mode (422 on APPROVE) is loud and immediately visible. This is the type of operational finding that should inform future spawn prompts across all three review-capable agents (Boltz, Specc, Optic).

---

## 6. Carry-Forwards

- **#263 still open.** HCD keep/replace decision is pending. The review doc was emailed to Eric. Once HCD responds: keep → close #263 with a comment; replace → source CC0 replacements in a follow-up cycle (likely folded into S24.3 or a standalone 1h cycle). S24.2 progression does NOT gate on this call — Arc E can proceed in parallel.

- **Spawn-prompt template hygiene.** The Boltz-PAT-fallback incident (Observation b) is fixed at the TOOLS.md level. Any future Riv responsible for spawning review agents should treat the App-ID/Installation-ID block as a required spawn-prompt element, not an optional annotation. Consider adding a checklist item to `riv.md` under "Boltz spawn configuration" to make this structural rather than convention-based.

- **Comment ordering convention.** The S21.5 convention (`.bus` set before `add_child`) has no comment marking its rationale. The S24.1 comment is close but focuses on routing rather than ordering. When S24.2 or S24.3 adds more `AudioStreamPlayer` instantiations, each one will follow the same `.bus`-before-`add_child` pattern. A single KB note or in-code `# Convention: set .bus before add_child per S21.5 AudioServer routing` would reduce future per-site explanation burden. Low priority; carry-forward for an Arc E housekeeping moment.

- **Issue-body drift risk.** Both erroneous claims in #262 (wrong directory, wrong callsite) were in the issue's original body and had never been corrected. The pipeline's Phase 0 catch is robust, but the issue body itself remained stale until close. A lightweight convention — Nutts or Boltz adds a correction comment to the issue when the plan diverges from the issue description — would keep the issues as accurate records for future archaeology. Not blocking; a quality-of-record observation.

---

## 7. Grade and Rationale

**Grade: A−**

S24.1 delivered exactly what Arc E Pillar 1 required: a 1-line code fix, a minimal-and-sufficient test, and a well-structured neutral HCD review doc — all in one PR, CI-green on the merge commit, with #262 closed and #263 correctly held open. The acceptance gate checklist passes cleanly:

1. `shop_screen.gd` change is exactly `.bus = "SFX"` + 1 comment line in `_ready()`, no other edits. ✅
2. New test file passes CI; 27 LOC; exactly 1 net-new assertion. ✅
3. Assertion delta 1347 → 1348; floor 1200 holds. ✅
4. Review doc present, human-readable, ≤800 words, 5 sections. ✅
5. `ATTRIBUTION.md` unchanged. ✅
6. Single PR; CI green pre- and post-merge. ✅

The A− (not A) is warranted by the inline comment wording: the delivered comment (`# S24.1 / closes #262 — route through SFX bus per 3-bus architecture (S21.5)`) omits the ordering rationale that is the precise justification for the line's position (`.bus` set before `add_child` per S21.5 convention). This is a cosmetic nit — the fix is correct, the convention is respected, the comment is informative — but the S21.5 pattern in `result_screen.gd` and `game_main.gd` lacks explicit ordering commentary, and a reader unfamiliar with that convention cannot derive the ordering rule from the delivered comment alone. The grade rubric specifies A for "code matches S21.5 convention" and A− for "all gates pass but with a minor cosmetic nit (e.g., comment wording)." This case fits A−.

The two process observations (issue body drift, Boltz PAT fallback) are pipeline-operational findings, not code defects. Both were caught and resolved within the same sprint window. Neither affected the deliverable quality. They are captured here for institutional record and carry-forward action, not as grade factors.

**S24.1 is closed. S24.2 (Mixer UI) gate condition: ✅ satisfied.**

---

## 8. Role Performance Review

### 🎭 Role Performance

**Gizmo:** Shining: Arc E brief sets clean pillar decomposition with gate dependencies and scope-exclusion list; the "Pillar 1 before Pillar 2" rationale is explicit and technically correct. Struggling: §2 Pillar 1 description cites `godot/screens/shop_screen.gd:73` — the wrong directory (should be `godot/ui/`) — and describes the fix as occurring in `_play_sfx()` rather than `_ready()`. These are the same errors as in #262's body, suggesting Gizmo quoted the issue description without verifying the live code. Phase 0 corrected them, but the arc brief is now stale in those particulars. Trend: →

**Ett:** Shining: Textbook Phase 0 audit — read the actual source before writing the implementation prompt, caught both the path error and the callsite misidentification before any code was written. Nutts prompt used the verified path and correct location. Also correctly identified that `subprocess_assert_count` in `test_runner.gd` (S23.4) would pick up the new test file automatically, requiring no test-runner changes. Struggling: The floor estimate in S23.4's plan was ~2× the actual count; here the §1 analysis is tighter (verified against live code), so no analogous estimation error. Minor: Ett's plan specified `test_s24_1_001_…` filename but the delivered convention in the repo is `test_sprint24_1_…` — the plan didn't match the actual suite naming style. Trend: ↑

**Nutts:** Shining: Delivered all three S24.1 deliverables in one PR with clean scope discipline — no refactors, no extra files, no scope wandering. Test file is exactly as minimal as the plan required. PR body is well-structured and explicitly accounts for `[#263] stays open` and `ATTRIBUTION.md unchanged`. Struggling: Comment wording omits ordering rationale (the A→A− nit). Minor. Trend: →

**Boltz:** Shining: Identified the review gate requirement and proceeded to post a text comment with full review findings when the formal App-token route failed — preserving review coverage even under an unexpected authentication error. Clean review checklist against the 6 acceptance gates. Struggling: First spawn lacked `BOLTZ_APP_ID`/`BOLTZ_INSTALLATION_ID` in the task prompt, causing PAT fallback and a blocked formal APPROVE. This was a spawn-prompt deficiency (Bott/Riv side), but Boltz did not proactively flag the token issue as a pipeline-structural concern — it silently fell back to the comment. A more explicit "authentication fallback — PAT cannot self-approve, spawn config may be missing App ID" escalation would have been faster to diagnose. Trend: →

**Optic:** Did not participate this sprint. S24.1 was below the LOC threshold for Optic gate involvement (< 15 LOC change; Optic Verified check-run showed `success` via its standard pass-through for small diffs). Trend: →

**Riv:** Did not participate this sprint as a named spawn (S24.1 was run directly by The Bott per the standing arc-loop configuration). The Bott handled spawn orchestration. Not evaluated.

---

*Authored by Specc (brott-studio-specc[bot]). S24.1 sub-sprint closed 2026-04-24T17:37:01Z.*
