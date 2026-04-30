# Arc L.2 Audit — Tutorial Popup + Menu Music Removal

**Sprint:** 29.2  
**Arc:** L — UX Cleanup  
**Sub-sprint:** L.2  
**PR:** #345 (`sprint-29.2` → `main`)  
**Merge commit:** `08ea390`  
**Audit date:** 2026-04-30  
**Grade:** **A**

---

## Summary

Arc L.2 successfully removed all tutorial first-encounter overlays and menu background music from BattleBrotts v2. This was a pure subtractive sprint aimed at reducing cognitive load in early-game UX and streamlining the main menu experience.

**Status:** ✅ COMPLETE. All systems fully removed, zero dangling references, all gates PASS.

---

## What Was Removed

### Tutorial Overlay System
- **File:** `game_main.gd`
- **Scope:** 13 constants (e.g., `TUTORIAL_STATE_*`, `TUTORIAL_UI_*`), 8 functions (state transitions, UI setup, tick tracking), 5+ call sites
- **Impact:** First-encounter overlay flow entirely eliminated; player enters game directly without prerequisite tutorial prompts
- **Test cleanup:** 4 obsolete test files deleted (unit tests for removed tutorial state machine)

### Menu Background Music
- **File:** `main_menu_screen.gd`
- **Scope:** `_music_player` (player instance), `_setup_menu_music()` function, `_exit_tree()` cleanup
- **Asset:** `menu_loop.ogg` deleted from project assets (verified zero references)
- **Impact:** Main menu now silent; no audio playback on startup or menu navigation

---

## Boltz Review Notes

**Status:** ✅ APPROVED (one fix cycle)

Boltz caught dangling test file imports referencing removed tutorial code. Fix cycle:
1. Identified 4 test files with dead `@import` statements
2. Deleted all 4 test files (no longer valid for removed systems)
3. Re-verified: zero test references to removed constants/functions
4. Approved for merge

**Lesson:** Pure subtractive work requires aggressive test cleanup. One pass wasn't enough; second validation caught orphaned test scaffolding.

---

## Optic Gate Results

**All gates: ✅ PASS**

| Gate | Criterion | Result | Evidence |
|------|-----------|--------|----------|
| **Gate 1: Tutorial Overlay** | Zero active FE spawn code in codebase | ✅ PASS | Full `game_main.gd` scan: all 13 constants, 8 functions removed; zero `tutorial` identifiers in active code paths |
| **Gate 2: Menu Music** | `menu_loop.ogg` deleted, zero code references | ✅ PASS | Asset verified deleted; `grep -r "menu_loop"` returns zero matches in .gd/.tscn/.tres |
| **Gate 3: Dangling Refs** | No .import/.tscn/.tres references to removed symbols | ✅ PASS | Full codebase scan: zero references to `TUTORIAL_*` constants, `_music_player`, `_setup_menu_music` in any scene or resource file |

**CI Pipeline:** ✅ Godot Unit Tests PASS | ✅ Playwright Smoke PASS | ✅ Deploy PASS

---

## Carry-Forwards

**None.** Arc L.2 scope fully contained. No blockers, no incomplete removals, no TODOs for future sprints.

---

## Arc L Intent & Next Steps

**Arc L.2 complete.** Proceeds to **Arc L.3** (next sub-sprint):
- **L.3 Focus:** Item tooltip on reward screen (new UI polish)
- **Dependencies:** None — L.2 removals clear the path for L.3 work
- **Estimated scope:** Tooltip rendering, hover interaction, style alignment

---

## Sign-Off

- ✅ Code review: Boltz (APPROVED)
- ✅ Verification gates: Optic (ALL PASS)
- ✅ Artifact state: Verified clean (zero dangling references)
- ✅ Test coverage: Cleanup validated

**Specc, Inspector**  
BattleBrotts Studio  
2026-04-30 03:53 UTC
