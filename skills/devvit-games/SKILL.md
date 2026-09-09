---
name: devvit-games
description: "Build or review Devvit Web games with authoritative rounds, scoring, recovery, mobile animation performance, lifecycle handling, and accessible player feedback. Use for game mechanics and integrity."
---

# Devvit Games

Build games whose client feels immediate while the server remains authoritative for competitive outcomes.

## Establish the game contract

Before implementation:

1. Define the round state machine and the exact event that starts play.
2. Decide whether the inline entrypoint is a lightweight launch screen or the game itself, and define the boundary accordingly.
3. Decide which facts are public, player-visible only after a transition, or permanently server-only.
4. Define the server-authoritative record, timing model, scoring rules, eligibility rules, and ranking tuple.
5. Separate competitive attempts from practice, replay, preview, tutorial, and spectator modes.
6. Decide how refresh, reconnect, backgrounding, user-initiated expanded-view closure, duplicate requests, and logged-out-to-logged-in transitions recover.
7. Identify every aggregate and index updated when a result becomes final.

Never accept client-calculated time, score, completion, identity, inventory, reward eligibility, or hidden-game facts as authoritative.

## Route by concern

- For choosing between a full inline game and a separate splash-to-game flow, including lightweight attraction, deferred loading, and state handoff, read [splash-to-game-boundary.md](references/splash-to-game-boundary.md).
- For round state, server clocks, hidden information, idempotency, replay, and recovery, read [authoritative-game-state.md](references/authoritative-game-state.md).
- For scoring, ranking, leaderboards, histories, and score graphs or distributions, read [scores-and-visualizations.md](references/scores-and-visualizations.md).
- For logged-out continuity, share deeplinks, recipient-specific landing UI, sound, and accessible feedback, read [sharing-and-player-experience.md](references/sharing-and-player-experience.md).
- For animation loops, frame-time stability, allocation, pooling, rendering cost, lifecycle suspension, and physical-device profiling, read [mobile-animation-performance.md](references/mobile-animation-performance.md).

## Cross-game rules

- Make state transitions explicit and testable; reject commands that are invalid for the canonical state.
- Give retryable mutations stable request IDs or idempotent semantics.
- Return canonical next state from mutations so the client does not reconstruct outcomes or immediately refetch them.
- Keep irreversible result finalization atomic with eligibility, ranking, and aggregate updates, or make partial work detectable and repairable.
- Rate-limit high-frequency actions without making ordinary latency or retries corrupt play.
- Keep loading, reconnecting, ending, finalized, expired, and unrecoverable states distinct.
- Treat expanded views as interruptible: users can close them at any time, and important progress must not depend on an unload callback.
- Treat share data, local storage, URL state, and display caches as untrusted hints.
- Preserve game mechanics when reduced motion, muted sound, keyboard control, or assistive technology changes presentation.
- Keep simulation correct when rendering slows, the webview is backgrounded, or a resumed frame reports a large elapsed interval. Bound catch-up work and re-resolve authoritative time after interruption.
- When the inline entrypoint is launch-only, keep it lightweight and move the core loop into the game entrypoint. A bounded, fast, gesture-compliant game may instead run directly inline.

## Build for player success

Treat these as the baseline quality bar for every game. Reddit also looks for them when deciding whether and how prominently to feature a game:

- Provide a compelling, custom first screen rather than a generic or unfinished entrypoint.
- Support both mobile and desktop with a clean, accessible viewport.
- Make the premise, controls, and next action self-explanatory so someone can learn, play, or participate from the post without outside context.
- Keep every screen usable in fullscreen, inline mobile, and inline desktop layouts. Avoid unnecessary scrolling; never require or allow scrolling within an inline webview.

Beyond baseline usability, design for the qualities that help a game succeed with players and strengthen its featuring potential:

- standout user experience: fast, intuitive, responsive play across devices;
- design and polish: cohesive visuals, an appealing first screen, and mobile-optimized layouts;
- community engagement: mechanics that encourage posts, comments, or user-generated content;
- innovation: mechanics or concepts that make playing on Reddit feel distinct;
- performance and retention: stable technical behavior and meaningful reasons for players to return; and
- iteration: regular improvements informed by player feedback.

## Verify

Test every state transition, invalid transition, duplicate command, boundary timestamp, concurrent finalization, refresh point, reconnect path, and eligibility mode. Confirm that hidden information never appears in client bundles, bootstrap payloads, share data, logs, or premature graphs. For every release, test the custom first screen, self-explanatory onboarding, and every game screen on inline mobile, inline desktop, and fullscreen viewports; confirm that inline play never depends on an internal scrollbar. Profile animation on physical mobile devices in the Reddit app, including background/resume and a long enough session to expose heat, memory growth, and intermittent frame-time spikes.
