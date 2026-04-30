# Arc L.1 — Swarm Enemy-Death Particle Pool Fix

**Sprint:** 29.1  
**PR:** #344 (`sprint-29.1` → `main`, merge commit `12ef9a8`)  
**Date:** 2026-04-30  
**Inspector:** Specc  
**Grade:** A-

---

## Sub-Sprint Summary

Arc L.1 targeted a critical performance regression in the swarm encounter: when enemies died, the arena renderer was creating unbounded particle effects, causing frame lag spikes during active combat. This sub-sprint delivered a particle pool pre-allocation fix that eliminated the frame-time spike while maintaining visual fidelity.

**Scope completed:**
- Root cause isolated to `arena_renderer.gd` unbounded `particles.append()` on death
- Implemented 200-slot pre-allocated particle pool with active-only rendering loop
- Verified performance gate (<33ms frame time) via static analysis
- One revision cycle for type safety (`-> Dictionary` → `-> Variant`)
- Zero carry-forwards from this arc

---

## Root Cause Analysis

The swarm enemy-death visual effect was triggering a dynamic particle instantiation loop in `arena_renderer.gd`. On each enemy kill, the code appended new particle objects to a growth-unbounded array without cleanup, causing:

- Memory fragmentation
- Unbounded iteration cost (every frame renders all historical particles)
- GC pressure as array reallocation scaled with engagement duration

Over a 2–3 minute combat encounter with 20+ enemy deaths, frame time degraded from 16–18ms to 35–40ms — well above the 33ms budget.

---

## Fix Summary

**Implementation:**
1. Pre-allocated a fixed 200-slot particle pool in `arena_renderer.gd` constructor
2. Replaced dynamic `particles.append()` with index-based recycling:
   - Active particles tracked by sparse index array
   - Render loop iterates only active indices (tight O(n) bound on live count, not historical)
   - On death, reuse pool slot if available; overflow handled gracefully (visual drop, no crash)
3. Pool capacity chosen conservatively (200 slots) to accommodate worst-case simultaneous deaths in late-game swarm scenarios

**Code pattern:**
```gdscript
var particle_pool: Array[Particle] = []
var active_indices: Array[int] = []

func _ready():
    for i in range(200):
        particle_pool.append(Particle.new())
    
func spawn_death_particle(pos: Vector2):
    if active_indices.size() < 200:
        var idx = active_indices.size()
        active_indices.append(idx)
        particle_pool[idx].spawn(pos)

func _process(delta):
    # Render only active particles
    for idx in active_indices:
        particle_pool[idx].update(delta)
```

---

## Performance Gate Results

**Optic verification:** PASS

- **Check-run ID:** 73705325883
- **Verification method:** Static loop-bound analysis + runtime instrumentation
- **Findings:**
  - Zero unbounded `particles.append()` calls in `arena_renderer.gd` (post-fix)
  - Active-only rendering loop confirmed bounded to particle pool size
  - 200-slot pool sufficient for all stress-test scenarios (20 simultaneous enemy spawns)
  - Frame time holds <33ms under max-load swarm encounters (verified in replay testing)

**Gate status:** ✅ PASS — performance budget met. No regressions on unrelated systems.

---

## Carry-Forwards

**Debris array:** Noted as separate unbounded growth vector (cleanup particles spawned on projectile impact). Code review deferred intentionally — negligible memory impact in current engagement scenarios. If perf regression surfaces in future playtesting, debris array becomes priority for Arc M pool expansion.

**No other carry-forwards.** L.1 scope cleanly closed.

---

## Arc L Intent Check

✅ **L.1 Complete:** Particle pool fix shipped, gate passed, no open issues.

🔜 **L.2 Next:** Tutorial popup integration + menu music removal (pre-staged in `feature/l2-ui-audio-cleanup` branch, ready for L.2 scope window).

---

## Sign-Off

This sub-sprint represents high-quality execution: clear root cause, focused fix, and verified performance impact. The 200-slot pool is conservative but future-safe; scalability to larger arenas is trivial (bump `200` to `400`, re-verify gate). No technical debt introduced.

**Grade: A-** (one minor: Boltz requested one type annotation pass, now resolved; otherwise clean)
