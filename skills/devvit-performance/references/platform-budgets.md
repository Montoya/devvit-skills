# Platform Budgets

Use explicit budgets before optimizing implementation details. Reddit's [Limits and Policies FAQ](https://developers.reddit.com/docs/guides/faq#limits-and-policies) currently documents these ceilings:

| Capability | Documented limit |
| --- | --- |
| Redis | 5 GB storage per installation, 5 MB per request, 40,000 commands per second |
| Devvit Web | 30 seconds per request, 4 MB request payload, 10 MB response payload |
| Post data | 2 KB per post |
| Settings and secrets | 2 KB per setting value |
| Realtime | 1 MB per message and 100 messages per second per installation |
| Scheduler | 10 live recurring actions per installation; `runJob()` has additional documented limits |
| Media uploads | 20 MB per upload and a 30-second timeout |

These limits can change. Confirm the current documentation and installed Devvit version when a design depends on a boundary.

## Design below the ceilings

- Do not make the documented maximum the ordinary payload or batch size. Leave headroom for encoding, schema growth, retries, and slower networks.
- Split large request and response bodies into bounded pages or domain operations. A request that times out before the 30-second ceiling still fails from the user's perspective.
- Keep Redis commands proportional to the requested page or mutation. Batch within request limits, avoid command-per-item loops over unbounded collections, and measure contested transaction retries.
- Use `postData` only for small shared JSON associated with one post. Use Redis for larger, indexed, private, or durable state.
- Use settings for configuration values, not application records or growing JSON documents. Store secrets only in the supported secret mechanism.
- Coalesce high-frequency realtime changes, send deltas or invalidation signals instead of full state when appropriate, and define backpressure or resynchronization behavior.
- Consolidate related recurring work when the installation could approach the scheduler cap. Track one-off `runJob()` usage separately from recurring actions.
- Compress and resize media well below 20 MB. An upload near 10 MB can still time out on a slow connection even though it is below the size ceiling.
- Do not hotlink arbitrary remote images into Devvit UI. Use bundled assets, Reddit-hosted URLs, or supported SVG data URLs; upload remote media to Reddit first when required.
- Do not rely on browser `localStorage` for state that must survive app updates. Persist canonical state in Redis and treat browser storage as a disposable acceleration hint.

## Verify boundary behavior

Test just below, at, and above every limit the app can approach. Cover timeout, partial batch, retry, duplicate delivery, backpressure, and recovery behavior. Instrument payload sizes, Redis operation counts, realtime send rates, media upload duration, and scheduled-action count before they become production failures.
