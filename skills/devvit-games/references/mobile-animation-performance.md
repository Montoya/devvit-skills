# Mobile Animation Performance

Devvit Web games usually run inside a Reddit mobile-app webview. Optimize for stable frame delivery on a representative phone, not only for a high average frame rate in a desktop browser. A brief smooth run can hide garbage-collection pauses, first-use shader or asset work, memory growth, and thermal throttling.

## Set a measured frame budget

- Choose a target refresh rate for the game and express it as a frame-time budget: about 16.7 ms at 60 Hz or 33.3 ms at 30 Hz. Leave headroom for the host app and operating system.
- Record frame-time percentiles and visible long frames, not only average frames per second. A stable 30 fps can feel better than an oscillating 40–60 fps.
- Treat renderer-specific figures such as a device-pixel-ratio cap of 2 or draw calls in the low hundreds as starting heuristics, not Devvit guarantees. Tune them against the actual game, renderer, device set, and thermal behavior.
- Make quality tiers explicit. Reduce decorative density, filter resolution, shadows, or particle counts before compromising input, collision, timing, legibility, or competitive rules.

## Keep the loop deterministic and bounded

- Drive visual work with `requestAnimationFrame`; do not use timer frequency as a game clock.
- Derive elapsed time from a monotonic clock. Clamp an abnormally large delta after backgrounding, resize, debugger pauses, or webview interruption.
- For physics or collision that needs fixed steps, accumulate elapsed time, run a bounded number of fixed updates, and discard or reconcile excess backlog rather than entering an unbounded catch-up spiral. Interpolate rendering when it materially improves motion.
- Keep authoritative round time on the server. Suspending animation or dropping visual frames must not pause, extend, or rewrite competitive time.
- Avoid duplicate loops. Make start, stop, visibility change, remount, and teardown idempotent, and cancel the outstanding animation frame when a scene stops.

## Remove allocation from hot paths

Aim for near-zero steady-state allocation after warmup in frame update, input sampling, physics, collision, AI, animation, particle, and render traversal code.

- Reuse scratch vectors, matrices, collision results, arrays, event payloads, and formatted labels. Let helpers fill caller-owned output instead of returning new objects.
- Avoid allocating array helpers, spread, object or array literals, closures, string construction, and `Array.shift()` in per-frame work. Use indexed loops, retained buffers, cursors, ring buffers, or swap-remove where appropriate.
- Create sprites, text, graphics, filters, and scene nodes once; mutate stable objects and update text only when its value changes.
- Pool bursty objects such as projectiles, particles, enemies, and score popups. Bound and prewarm each pool for a measured peak, overwrite all state on acquire, release objects back to the pool, and define what happens at exhaustion. Dropping a low-value decorative effect is safer than allocating beyond the cap.
- Do not apply these rules indiscriminately to menus, setup, loading, or other cold paths. Optimize code that measurements show runs frequently enough to affect play.

## Bound rendering work

- Separate logical game coordinates, CSS display size, and canvas backing-store size. Cap effective device pixel ratio when fill rate is expensive; recompute on a real size change rather than resizing the canvas every frame.
- Cull objects before expensive update and render ownership. Moving an object offscreen, clipping it, masking it, or setting alpha to zero does not necessarily stop its CPU or GPU cost.
- Use texture atlases and batching for repeated 2D art. In 3D, merge static geometry and instance repeated meshes when supported. Retain scene children and toggle their state instead of adding and removing them every frame.
- Watch transparent overdraw from particles, fog, glows, and full-screen layers. Prefer baked lighting and effects over dynamic shadows or many per-pixel lights on mobile.
- Avoid rebuilding vector graphics or causing text rasterization every frame. Redraw only when the underlying shape or value changes.
- In DOM overlays, animate compositor-friendly transforms and opacity when practical. Batch layout reads before writes and avoid alternating measurements with mutations inside a frame.

## Warm up without bloating startup

- Decode and prepare assets needed for the first interaction before play begins. Defer later levels and optional effects so performance work does not make initial entry slower.
- Prewarm measured pool capacity and representative first-use rendering paths during an existing loading boundary. Do not hide a long synchronous warmup behind an apparently interactive screen.
- Use compact atlases and appropriately sized textures. Budget decoded memory as well as transfer size: compressed bytes on the network can expand substantially in memory.
- Keep simultaneous audio voices and effect instances bounded, and release scene-specific resources on teardown.

## Respect the webview lifecycle

When the Devvit view becomes non-visible, stop requesting visual frames, suspend decorative simulation, and mute or suspend audio. Preserve only the state needed to recover. On return:

1. re-read visibility and viewport measurements;
2. reconcile canonical round state and time;
3. clear stale input and clamp the first visual delta; and
4. resume exactly one loop if play is still valid.

Do not depend on unload callbacks to save important progress. The host can close or reclaim an embedded view without a reliable final callback.

Reduced motion is also a performance-friendly presentation mode, but it must preserve rules and feedback. Replace or shorten decorative movement, keep final states immediately perceivable, and never use the preference to change competitive timing.

## Diagnose on the real path

Profile a production build on physical mobile devices inside Reddit whenever possible. Cover inline and expanded entrypoints, because they can have different viewport, lifecycle, and loading behavior.

- Capture startup, active play, a worst-case burst, background/resume, and a sustained session long enough to reveal heat or memory growth.
- Correlate long frames with JavaScript tasks, garbage collection, style/layout, texture upload, shader compilation, draw calls, and transparent overdraw. In-app timing counters can preserve evidence when remote inspection of the webview is unavailable.
- Do not use a `requestAnimationFrame` FPS counter as the only signal. It can miss compositor behavior, variable refresh, input delay, and the cause of a missed frame; combine it with traces, long-task or interaction data, and game-specific timing.
- Instrument active entity counts, pool utilization and exhaustion, per-system update time, render time, canvas resolution, and quality-tier changes in development builds.
- Use variants that disable labels, filters, effects, culling, pooling, or rebuilds to isolate a cause. These are diagnostic controls, not silent production fixes.
- Change one bottleneck at a time, repeat the same scenario, and report observed improvement separately from expected improvement.

## Release checks

- No duplicate animation loop appears after remount, visibility changes, or reconnect.
- A long resumed delta cannot cause a physics jump or catch-up spiral.
- Steady play does not continually allocate or grow pools, listeners, scene nodes, textures, or audio objects.
- Worst-case action density stays within the intended frame budget or enters an explicit, mechanically safe quality tier.
- Low-value effects degrade gracefully at pool or rendering limits while controls and authoritative rules remain intact.
- A sustained mobile session has stable memory and acceptable frame-time tails, not merely a good average.

## Sources and further reading

- NixieFX: [Holding 60 fps on the mobile web](https://nixiefx.com/html5-game-performance/), the basis for the allocation, pooling, draw-call, pixel-ratio, overdraw, culling, and root-cause profiling guidance above.
- MDN: [`requestAnimationFrame`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame), [Page Visibility API](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API), and [Optimizing canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas).
- web.dev: [Rendering performance](https://web.dev/articles/rendering-performance) and [Towards an animation smoothness metric](https://web.dev/articles/smoothness).

Treat numeric heuristics from any general web guide as starting points and validate them in the target Reddit webview.
