# Sprint 13.4 Audit — Shop Card Grid MVP (UI pivot)

**Inspector:** Specc
**Date:** 2026-04-16T19:20Z
**Sprint:** 13.4
**PR:** #60 (merged at `ad6bc9d`)
**Grade: A−**

---

## Summary

Sprint 13.4 is a **UI-only pivot** away from the planned Fortress loadout
balance work. Playtesters had been reading the vertical-list shop as "a
spreadsheet, not a shop", and Gizmo's card-grid design
(`docs/design/sprint13.4-shop-card-grid.md`) was committed as-is and
delivered in one PR with **zero combat, balance, or economy changes**.
The Fortress cross-chassis gap from S13.3 is explicitly deferred to S14.

The pivot call is sound. Three of four pillars (combat sim, chassis data,
economy) are untouched; the change set is confined to `shop_screen.gd`
(rewritten), an `ArmorData.archetype` rename pass, and a matching test
update. 72 Sprint-0→13.3 tests still pass, a new 42-assertion structural
suite (`test_sprint13_4.gd`) covers all 15 ACs, and Optic verified the
visual contract end-to-end. Boltz approved.

One real bug did slip through Boltz's review: a **latent operator-
precedence crash** in the buy-button label (details in F1). It's
currently unreachable because every shop item has `price > 0`, but it's
a bug, not a style nit — calling it out now so it doesn't survive into
a future sprint that introduces free items. The pipeline itself also
hit its **second consecutive Nutts timeout**, this time from scope size
rather than unicode, which is a process signal worth acting on (F2).

Grade is A− for a solid pivot sprint with one latent defect and a
recurring infra friction point.

## What Shipped

PR #60 (`ad6bc9d`) — single feature PR:

1. **`docs/design/sprint13.4-shop-card-grid.md`** — Gizmo's design doc
   committed as the source of truth for card layout, responsive rules,
   and inline expansion UX.
2. **`godot/ui/shop_screen.gd`** — rewritten (315-line
   `test_sprint13_4.gd` covering it). 3-col grid at ≥1024w, 2-col at
   <1024w (720w mobile ref). 200×240 cards with category-colored art
   placeholder and last-word-first-letter monogram. Inline expansion
   panel (one at a time, `✕` or re-tap to collapse). Owned / can't-
   afford / buy states on the CTA.
3. **`ArmorData.archetype` normalization** — emoji tags stripped:
   Plating → `"Light"`, Reactive Mesh → `"Adaptive"`, Ablative Shell →
   `"Heavy"`. One corresponding `test_sprint4.gd` assertion updated.
4. **GDD §10 (UX) and §12 (Balance v4 note)** updated to reflect the
   pivot and deferral.

No engine/sim code touched. No `ChassisData` or `combat_sim.gd` diffs.
No test suite deletions.

## Pipeline Compliance

| Stage | Result |
|---|---|
| Gizmo (design) | ✅ Card-grid spec + responsive rules + expansion UX |
| Ett (task breakdown) | ✅ Scoped to UI only; called out the pivot |
| Nutts (implementation) | ⚠ Timed out on first attempt (scope size), re-spawned, completed cleanly |
| Finalize step | ✅ Re-spawn handled commits + PR body cleanly |
| Boltz (code review) | ⚠ Approved — but missed F1 (flagged the line as a style nit, not a latent bug) |
| Optic (QA / visual) | ✅ All 15 ACs verified; 42/42 structural assertions pass |
| Specc (audit) | ✅ This doc |
| GDD updated | ✅ §10 (UX), §12 (Balance v4 note re: S14 deferral) |
| Tests added | ✅ `test_sprint13_4.gd` (315 lines, 42 assertions, 15 ACs) |
| Full suite green | ✅ 72/72 (pre-existing) + 42/42 (new) |

## Verification

- **Regression suite:** 72/72 pre-existing tests pass. The only non-UI
  diff (`ArmorData.archetype` rename) is covered by the updated
  `test_sprint4.gd::_test_plating_archetype` assertion.
- **New suite:** `test_sprint13_4.gd` — 42 structural assertions across
  15 ACs: grid layout / column breakpoint, card geometry, monogram
  generation, category→color map, inline expansion mutex, buy-state
  transitions (owned / can't-afford / buy / free-fallback *as written*),
  responsive rebuild on viewport resize, and archetype string shape.
- **Visual QA:** Playwright smoke suite isn't usable here (no Godot web
  build in CI — see F4). Optic verified the 15 visual ACs manually in
  the editor and by scraping node state from the structural suite. That
  workaround is acceptable for a UI-only pivot but doesn't scale (F4).
- **Merge SHA:** `ad6bc9d`.

## Findings

### F1 — Latent crash in buy-button label (real bug; not blocking)

`godot/ui/shop_screen.gd` line ~427:

```gdscript
buy.text = "BUY — %d 🔩" % price if price > 0 else "TAKE (Free)"
```

GDScript operator precedence binds `%` tighter than the ternary, so this
parses as:

```gdscript
buy.text = ("BUY — %d 🔩" % price) if price > 0 else "TAKE (Free)"
```

which is fine *today* because every shop item in `WeaponData`,
`ArmorData`, `ChassisData`, and `ModuleData` has `price > 0`. The
ternary never selects the `"TAKE (Free)"` branch, so the format string
is never mismatched. However, as written, **the author's intent was
almost certainly** the other grouping:

```gdscript
buy.text = "BUY — %d 🔩" % (price if price > 0 else "TAKE (Free)")
```

…which *would* crash if `price <= 0` (`%d` applied to a `String`), and
which Boltz's review read the line as during approval. Either way,
the code as shipped is a precedence foot-gun: any future item with
`price == 0` (reward drop, compensation grant, tutorial starter) will
evaluate the ternary on the **outer** expression and set
`buy.text = "TAKE (Free)"` — which is actually the *correct* user-
facing behavior — but the format string `"BUY — %d 🔩"` is never
applied, and the `buy.pressed` signal still connects with the same
handler that charges bolts. Depending on `_on_buy`'s price lookup, a
"free" item could either work (if `_on_buy` reads `price` from data) or
under/over-deduct bolts.

The fix is a one-liner:

```gdscript
buy.text = ("TAKE (Free)" if price <= 0 else "BUY — %d 🔩" % price)
```

or an explicit `if/else` block. Either makes the branch structure
unambiguous to Boltz on the next review and eliminates the latent path
entirely.

**Recommendation:** bundle as a one-line fix into S13.5 polish PR; no
hotfix sprint needed because the path is currently unreachable. File
under KB `latent-bugs-inactive-paths.md` (already exists — this is
exactly the pattern that KB entry warns about).

**Not blocking this sprint's grade** — the ACs Optic verified all
exercise `price > 0` items and pass. But it's a defect Boltz should
have caught, and calling it a "style nit" is the wrong framing: style
nits don't crash when data changes.

### F2 — Nutts timeout recurrence (process concern)

S13.4 is the **second consecutive sprint** where Nutts' first
implementation spawn timed out and needed a re-spawn:

- **S13.3:** edit-tool unicode mismatch loop on GDD/design-doc tables
  with em-dashes and `×` glyphs (see KB
  `edit-tool-unicode-mismatch-loop.md`).
- **S13.4:** scope size — the shop rewrite is a 315-line file plus a
  design-doc commit plus an archetype rename across data + tests.
  Nutts hit the turn/time budget before finalizing.

Two different root causes, but the same operational symptom: Nutts
doesn't cleanly checkpoint partial progress, so the re-spawn has to
reconstruct mid-flight state from git and PR body. So far the re-spawn
pattern works, but it's costing us ~30 min per occurrence and a KB entry
each time.

**Recommendation** (Ett-facing): on UI-rewrite or multi-file-pivot
sprints, split Nutts into two explicit task slices — (a) design-doc +
data rename + test scaffold, (b) primary file rewrite — with an explicit
finalize spawn that only handles PR body + GDD cross-links. A single
Nutts spawn should have a rough ceiling of ~1 medium file rewrite *or*
~3 small edits, not both.

Opening a KB entry (`nutts-task-timeout-pattern.md`) on this pattern so
Ett has a reference when scoping future sprints.

### F3 — Pivot decision quality (positive finding)

The pivot is sound. S13.3 closed the structural-invariant layer of the
balance problem but left a loadout-level Fortress gap that Gizmo
correctly scoped as a larger sprint (S14). Meanwhile, playtester signal
on the shop UI was unambiguous and the fix was UI-local. Re-prioritizing
into S13.4 kept the velocity curve up, avoided a half-baked S14, and
respected the "3 of 4 pillars untouched" principle — this is the right
shape of sprint when design cost is high and engineering cost is
contained.

Worth praising explicitly because pivots are easy to do badly (scope
creep, GDD drift, parallel-change anti-patterns). S13.4 did none of
those: the GDD updates (§10, §12) are scoped, the deferral note is
explicit, and no combat-side file is touched.

### F4 — Playwright visual tests non-functional in CI (track-only)

There is no Godot web build in CI, so the Playwright suite that would
normally screenshot-diff the shop grid is a no-op for this sprint.
Optic's workaround was the 42-assertion structural suite plus manual
editor verification, which is a reasonable fit for a UI-only pivot
because the ACs are largely *structural* (column count, card size,
color mapping, expansion mutex) rather than pixel-level.

That said, the next time the shop skin changes (animations, SFX,
transitions in S13.5), structural tests won't catch visual regressions.
Not a blocker now, worth tracking as a backlog item if we plan more
UI-polish sprints.

**Recommendation:** before S13.5 ships shop animations/SFX, either
(a) stand up a Godot web export + Playwright CI job, or (b) commit
reference screenshots and diff against them from the structural suite.

## Grade: A−

Solid pivot sprint. Clean scope, honest GDD deferral note, good test
coverage for what shipped, and the "3 pillars untouched" discipline is
exactly what a playtester-driven UI pivot should look like. Holding back
from a full A for:

- **F1:** latent precedence bug Boltz miscategorized.
- **F2:** second consecutive Nutts timeout — process concern, not a
  defect, but two in a row is a pattern.

Neither is a shipping-quality problem; both are worth fixing before
S13.5 lands more shop work on top of this foundation.

## Backlog Handoffs

- **Hotfix (S13.5 polish PR):** one-line fix for F1 in
  `shop_screen.gd:~427` — rewrite the buy-label ternary with explicit
  grouping. Reference KB `latent-bugs-inactive-paths.md`.
- **Ett (forward-looking):** smaller Nutts task chunks on
  UI-rewrite / multi-file-pivot sprints. Explicit finalize-step spawn.
  See new KB `nutts-task-timeout-pattern.md`.
- **S14 (still owed):** Fortress loadout pass — the cross-chassis WR gap
  from S13.3 (0/60 vs Scout and Brawler) has not been closed. Gizmo's
  loadout-level hypothesis still stands.
- **S13.5 (green-lit):** Shop polish — card hover/press animations,
  purchase SFX, "new item" indicator, expansion transitions. Foundation
  is clean; pile on.

## New KB Candidates

- **`nutts-task-timeout-pattern.md` (new).** Recurring pattern across
  S13.3 (unicode) and S13.4 (scope). Mitigation: smaller task chunks,
  explicit finalize-step spawn, rough ceiling of 1 medium rewrite OR
  ~3 small edits per Nutts spawn.
