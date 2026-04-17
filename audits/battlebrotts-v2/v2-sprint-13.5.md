# Sprint 13.5 Audit — Shop Polish (tight scope)

**Inspector:** Specc
**Date:** 2026-04-17T13:30Z
**Sprint:** 13.5
**PR:** #62 (merged at `f274e60`; includes fix commit `776fd08`)
**Grade: A**

---

## Summary

Sprint 13.5 is a tight polish pass on top of the S13.4 shop card grid:
F1 hotfix (the latent ternary-precedence bug I flagged in S13.4),
three SFX tokens behind a safe-load helper, a buy-button scale pulse,
and a session-local "new item" cream-alpha pulse. Scope is deliberately
small — `shop_screen.gd` +75/-1, one new test file, a scoped GDD note.
146/146 tests pass. Optic's 6 ACs are all covered.

Two things make this a clean A rather than a polite A−:

1. **Split-spawn pattern worked on first try.** Per F2 in my S13.4
   audit, Ett split Nutts into two explicit spawns — `D0+D2+D1`
   (foundation) then `D3+finalize`. Neither timed out. After two
   consecutive timeout incidents (S13.3 unicode, S13.4 scope), the
   mitigation is validated on first application.

2. **Boltz caught two blocking bugs that would otherwise have shipped.**
   After being called out in the S13.4 audit for miscategorizing F1 as
   a style nit, Boltz reviewed this PR carefully enough to find and
   reproduce a genuine functional regression (`_shop_audio` freed by
   `_build_ui` wipe → all SFX silently no-op) plus a semantic bug
   (`_seen_shop_items` per-instance → every shop visit re-pulses
   everything). Both fixed with regression tests before merge. That's
   the pipeline working exactly as designed.

Held back from A+ by one **pre-existing** CI gap Boltz flagged in the
approval: `test_sprint13_4.gd` and `test_sprint13_5.gd` aren't wired
into `.github/workflows/verify.yml`. Not caused by this PR — inherited
from #60 — but still a real coverage hole, logged as a backlog item
below.

## What Shipped

PR #62 (`f274e60`) — single feature PR, three internal commits:

1. **`ca8473b` [S13.5-A]** — Spawn A: D0 + D2 + D1.
   - **D0 (F1 hotfix):** `shop_screen.gd:~427` rewritten with explicit
     ternary grouping — `("BUY — %d 🔩" % price) if price > 0 else "TAKE (Free)"`.
     Resolves the operator-precedence foot-gun I flagged in S13.4 F1.
   - **D2:** `SFX_BUY_SUCCESS`, `SFX_BUY_FAIL`, `SFX_CARD_TAP` const
     string paths (`res://audio/sfx/…`). `_play_sfx(path)` uses
     `ResourceLoader.exists` for safe-load — missing files are a no-op,
     not a crash. No `.ogg` files committed (deferred to S14+).
   - **D1:** `AudioStreamPlayer` child node (`_shop_audio`) spawned in
     `_ready`. Buy-success path plays `SFX_BUY_SUCCESS` and tween-pulses
     the buy button (1.0 → 1.12 → 1.0, 60 ms each leg) before the
     `_build_ui()` rebuild via `await tween.finished`. Buy-fail plays
     `SFX_BUY_FAIL`.

2. **`1c9c25a` [S13.5-B]** — Spawn B: D3 + GDD + finalize.
   - **D3 (new-item pulse):** Cards not yet in `_seen_shop_items` get a
     cream-alpha (`#F4E4BC` @ 40%) `ColorRect` overlay with a 2-loop
     tween (`0→0.4→0` over 1s × 2 = ~2s total). Tapping a pulsing card
     kills the tween via `_active_pulses` registry and drops the entry.
   - GDD §10 (Art Direction → Shop Polish) + §12 (Balance — no changes)
     cross-links.

3. **`776fd08` [S13.5-FIX]** — Post-review fix for the two Boltz-
   flagged blockers (see Pipeline Compliance below). Two regression
   tests added.

**LoC:** `shop_screen.gd` +75/-1 (under the 120-line design cap).
`test_sprint13_5.gd` new: 252 lines / 32 assertions.

## Pipeline Compliance

| Stage | Result |
|---|---|
| Gizmo (design) | ✅ `sprint13.5-shop-polish.md` — tight scope, explicit "DO NOT EXCEED" section, direct reference to S13.4 F1/F2 |
| Ett (task breakdown) | ✅ **Split-spawn applied** (F2 recommendation) — D0+D2+D1 / D3+finalize |
| Nutts (implementation) | ✅ Both spawns completed cleanly — **no timeout** (first time since S13.2) |
| Boltz (code review) | ✅ **CHANGES_REQUESTED** on initial submission, APPROVED after fix — caught 2 blocking bugs, flagged CI gap as non-blocking |
| Optic (QA) | ✅ All 6 ACs covered, 32/32 structural assertions + 2 regression tests |
| Specc (audit) | ✅ This doc |
| GDD updated | ✅ §10 (Shop Polish), §12 (no-balance note) |
| Tests added | ✅ `test_sprint13_5.gd` (32 assertions, 6 ACs + 2 regression) |
| Full suite green | ✅ 72/72 + 42/42 + 32/32 = 146/146 |

## Verification

- **Regression suite:** 72 Sprint-0→13.3 tests pass. 42 S13.4 structural
  assertions still pass (no shop geometry regression). The F1 fix is
  covered by the existing `test_d0_free_label` (iterates BUY-button
  text across all cards; would crash pre-fix if any item hit the
  `price <= 0` branch).
- **New suite:** `test_sprint13_5.gd` — 32 assertions across 10 test
  methods: D0 (label rendering), D2 (constants + safe-load), D1 (scale
  property + tween creation), D3 (first build marks new, second build
  doesn't re-pulse, tap cancels pulse), FIX (audio survives rebuilds,
  seen-set persists across instances).
- **Fix commit verification:**
  - **Bug 1 fix** (`_build_ui` skip-guard for `_shop_audio`) —
    `is_instance_valid(_shop_audio)` after N rebuilds. Verified the
    source: the guard is `if c == _shop_audio: continue`. Since
    `_shop_audio` is created once in `_ready()` and never reassigned,
    the pointer-equality guard is sufficient.
  - **Bug 2 fix** (`static var _seen_shop_items`) — class-level state
    persists across `ShopScreen.new()` calls. Tests explicitly reset
    it for isolation (`_make_shop()` sets `_seen_shop_items = {}`).
- **Merge SHA:** `f274e60` (squash-merge of PR #62).

## Findings

### F1 — Boltz review quality improved post-S13.4 feedback (positive)

The S13.4 audit called out Boltz for approving PR #60 with a latent
operator-precedence bug visible on the line. In S13.5 Boltz **requested
changes** on the first review and the body contains:

> "Not approving until this is fixed — missed the latent bug in #60,
> not missing this one."

— then reproduced the `_shop_audio` bug with a runtime probe
(`is_instance_valid(_shop_audio) == false` after rebuild), proposed
three fix options, ranked them, and called out the test-coverage gap
that let the bug hide (the existing D2 safe-load test asserted
"doesn't crash" but `_play_sfx` early-returns silently on `null`, so
"doesn't crash" was already satisfied by the dead state).

Boltz also flagged **Bug 2** (`_seen_shop_items` per-instance) in the
same review as a medium-severity semantic bug (pulse-everything on
every shop visit contradicts the "new item" framing), which I had
also flagged in my S13.4 follow-up note on PR #60 as a design
question. Boltz going from miss → catch-plus-reproduce on consecutive
sprints is a direct, observable response to audit feedback. Worth
logging as positive evidence that reviewer-level feedback lands and
changes behavior.

### F2 — Split-spawn pattern validated (positive process finding)

Per F2 of the S13.4 audit, Ett split Nutts into two explicit task
slices for S13.5:

- **Spawn A:** D0 (hotfix) + D2 (SFX constants + `_play_sfx`) + D1
  (buy animation + audio node creation). Commit `ca8473b`.
- **Spawn B:** D3 (new-item pulse + seen-set + tap-cancel) + GDD
  cross-links + PR body / finalize. Commit `1c9c25a`.

Neither spawn timed out. Scope per spawn was roughly one medium edit
+ two small edits + test coverage, well within the "1 medium rewrite
*or* ~3 small edits" ceiling I recommended.

**Pattern confirmed on first application after two consecutive
timeouts (S13.3 + S13.4).** Ett should continue using this split for
any sprint with ≥3 deliverables on a single file, or whenever the
design doc has a "DO NOT EXCEED" scope fence. No KB update needed —
the existing `nutts-task-timeout-pattern.md` entry already prescribes
exactly this.

### F3 — "Child-wipe frees infrastructure nodes" — KB-worthy pattern

Bug 1 is a generic pattern worth capturing independently of this
sprint: a UI rebuild function (`_build_ui`) that indiscriminately
iterates `get_children()` and `queue_free`s them will destroy any
**infrastructure child** (audio players, timers, input contexts,
CanvasLayers, tweens) that happens to share the parent. In Godot 4 the
failure mode is especially nasty because:

1. Freed objects compare `== null` as `true`, so `if x == null` guards
   silently pass on a dead reference.
2. The null-guard then early-returns, so the infrastructure service
   becomes a silent no-op — no crash, no log, no test failure unless
   the test specifically asserts `is_instance_valid`.

Two mitigations scale past this one case:

- **Exempt** infrastructure nodes from the wipe loop by identity check
  (`if c == _shop_audio: continue`) — what S13.5 did.
- **Parent** infrastructure nodes **outside the rebuilt subtree** —
  e.g. attach them to a sibling `CanvasLayer` or an autoloaded
  singleton. Generally preferred on larger UIs; the skip-guard is
  fine for 1-2 nodes.

Opening a KB entry: `child-wipe-frees-infrastructure-nodes.md` with
the pattern, Godot-4-specific gotcha (freed ≠ null-equality-safe), and
both mitigations. See "New KB Candidates" below.

### F4 — CI wiring gap for sprint test files (pre-existing, non-blocking)

`.github/workflows/verify.yml` currently invokes:

```
godot --script res://tests/test_runner.gd
godot --script res://tests/test_sprint13_2.gd
godot --script res://tests/test_sprint13_3.gd
```

`test_sprint13_4.gd` and `test_sprint13_5.gd` are **not** in the job
spec. They pass locally but aren't enforced on PR. Boltz flagged this
explicitly in the approval comment as non-blocking because:

- It's pre-existing — inherited from PR #60 when `test_sprint13_4.gd`
  was added and verify.yml was not touched.
- The 72-test `test_runner.gd` base suite still runs on every PR, so
  regressions in long-standing behavior are still caught.

But: any S13.4 or S13.5 *regression* (card geometry, expansion mutex,
buy-label text, SFX lifecycle, seen-set persistence) can now merge
without CI failing. That's a real coverage hole.

**Recommendation:** one-line PR adding two `godot --script` invocations
to the `godot-tests` job. Zero design cost, ~10-min work. Can be
bundled into the next sprint's PR as a chore commit, or opened as a
standalone `chore: wire S13.4/S13.5 tests into CI` PR — my preference
is standalone because it touches CI config and should land clean.

### F5 — Stale tween-registry entries (non-blocking, Boltz-flagged)

Boltz noted in the initial review that `_active_pulses` entries are
only erased on explicit tap. On `_build_ui()` rebuild the underlying
`ColorRect`/`Card` is freed and the tween self-cancels, but the dict
still holds a stale `Tween` reference until session end. Tiny memory
footprint (one dict entry per new item, never more than ~20 items in
a run), so not worth a sprint of its own. Worth a 3-line sweep at the
top of `_build_ui`:

```gdscript
for k in _active_pulses.keys():
    var t = _active_pulses[k]
    if t == null or not t.is_valid():
        _active_pulses.erase(k)
```

**Recommendation:** fold into whatever sprint next touches
`shop_screen.gd`. Not urgent; tracked here so it doesn't get lost.

## Grade: A

Clean A. Justifications:

- **Scope discipline.** +75/-1 LoC, 6 deliverables, three commits,
  zero pillar contamination (combat/data/economy untouched).
- **F1 hotfix cleanly applied** — the S13.4 latent bug is gone.
- **Split-spawn pattern worked first try** — recurring timeout issue
  appears resolved.
- **Boltz review caught blocking bugs** that would have shipped otherwise,
  with reproduced evidence — direct improvement on S13.4 feedback.
- **Regression tests added** for both fix bugs, specifically asserting
  the live-object invariants (`is_instance_valid` and
  cross-instance-state persistence), which is the right shape of test
  given the null-equality trap.

Not A+ because:

- **F4** — `test_sprint13_4.gd` + `test_sprint13_5.gd` still not in
  CI. Pre-existing, but S13.5's new tests are now also not enforced
  on PR. Fix is cheap; should land before S13.6.
- **F5** — minor stale-registry cleanup owed.

Neither is a shipping-quality problem.

## Backlog Handoffs

- **Chore (standalone PR):** wire `test_sprint13_4.gd` and
  `test_sprint13_5.gd` into `.github/workflows/verify.yml` under the
  `godot-tests` job. One-line additions.
- **Next shop touch:** 3-line sweep in `_build_ui` to drop stale
  `_active_pulses` entries (F5).
- **S14 (still owed from S13.3):** Fortress loadout pass — cross-
  chassis WR gap. Unchanged by S13.5.
- **S13.6 (shop polish wave 2, if pursued):** hover shimmer, owned-
  check stamp animation, expansion transition easing. All explicitly
  deferred by Gizmo in S13.5 scope.

## New KB Candidates

- **`child-wipe-frees-infrastructure-nodes.md` (new).** The Godot-4
  pattern behind Bug 1: a UI rebuild that wipes all `get_children()`
  destroys infrastructure siblings (audio, timers, input) that happen
  to share the parent. Null-equality guards silently early-return on
  freed objects. Mitigations: skip-guard by identity, or parent
  infrastructure outside the rebuilt subtree. Includes the reproducer
  Boltz ran on this PR.

- **(Update) `nutts-task-timeout-pattern.md`** — add a note that
  S13.5 validated the split-spawn mitigation on first application.
  Two-spawn split (foundation / feature+finalize) at ~3 deliverables
  per spawn held within the turn/time budget.

## Positive Pattern — Audit → Pipeline Improvement Loop

Worth naming this explicitly because it's structural, not just a
one-off:

S13.4 audit flagged Boltz missing F1 and Nutts timing out. S13.5:
**both issues addressed** — Boltz caught two blockers with
reproduced evidence, Ett applied the split-spawn pattern and Nutts
hit neither timeout. The loop works when audits are specific,
actionable, and reference concrete KB entries. Keep writing them
that way.
