# Devvit Capability Harness

## Use the installed test surface

Inspect the installed `@devvit/test`, Devvit capability packages, test runner, and project configuration. Import the production capability clients inside the code under test and let the Devvit harness replace their backing plugins with isolated stateful mocks.

Keep request parsing, authentication context, repository operations, and response serialization in the exercised path when those boundaries matter. Use pure unit tests for calculations and schemas that do not need Devvit context.

## Redis

Test canonical records and every index they update. Cover missing keys, malformed legacy values, expirations, page bounds, ties, replacement, deletion, and reconciliation markers.

Exercise the production `watch`/`multi`/`exec` transaction flow for read-check-write invariants. Assert the complete postcondition across canonical records, indexes, counters, and reverse references. Add explicit contention tests when two requests can target the same logical entity.

Exercise application behavior at the Redis request and storage budgets it can realistically approach. Keep ordinary fixtures below the documented 5 MB request and 5 GB per-installation storage ceilings, then add explicit rejection, pagination, or compaction tests at relevant boundaries. Do not write a synthetic 40,000-command test unless the implementation can genuinely approach the documented per-second ceiling; measure and bound commands per product operation instead.

## Scheduler

Scheduled jobs do not need wall-clock waiting in the harness. Assert that the correct named job, data, and intended time were registered or cancelled, then invoke the job handler directly with deterministic input to test its behavior.

Test repeated sweeps, late invocation, missing data, overlapping manual and scheduled actions, and a previous partial failure. A scheduler test that only confirms registration does not prove publication or cleanup behavior.

Assert that configuration cannot create more than the documented 10 live recurring actions per installation. Cover consolidation or a clear failure path when the schedule would exceed that budget, and test separate `runJob()` limits when the app schedules one-off work.

## Reddit, settings, media, realtime, and notifications

Seed only the Reddit objects and permissions required by the scenario. Test logged-out, ordinary-user, moderator, missing-object, deleted-object, and capability-error paths where relevant.

For capabilities whose harness records calls rather than performing the real effect, assert both the durable local state and the recorded intent. Do not claim that a mock proves real attribution, UI presentation, media rendering, notification delivery, or client behavior.

Add boundary cases for any capability the product can approach: 2 KB post data, 2 KB setting values, 1 MB realtime messages, 100 realtime messages per second per installation, 20 MB media uploads, and the media upload timeout. Prefer small fakes that model acceptance and rejection over allocating maximum-size fixtures throughout the suite.

## HTTP

Mock external HTTP at the network boundary. Cover status failures, invalid bodies, timeouts or rejected promises, response size limits relevant to the app, and retry behavior. Never make a routine test depend on a live third-party service.

For Devvit Web endpoints, cover the relevant sides of the documented 30-second request, 4 MB request-payload, and 10 MB response-payload ceilings. Use lower application budgets so tests detect regressions before platform rejection.

## Triggers

Call trigger handlers with representative typed payloads. Deliver the same event repeatedly and in plausible unexpected order. Verify narrowly scoped cleanup, missing reverse mappings, deleted canonical records, and legacy state.

Recheck numerical values against Reddit's [Limits and Policies FAQ](https://developers.reddit.com/docs/guides/faq#limits-and-policies) when tests or production code rely on an exact ceiling.
