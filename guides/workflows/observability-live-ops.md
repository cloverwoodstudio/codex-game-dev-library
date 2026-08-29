# Telemetry, crash reporting and live operations

Reviewed: 2026-08-29

Observability should answer a product or reliability question, not collect everything. Design it before launch, minimize personal data, document consent/retention, and verify the pipeline without relying on production players.

## Four complementary records

- **Product events:** what players attempt and where loops fail.
- **Metrics:** aggregate rates, latency, concurrency and resource use.
- **Logs:** bounded diagnostic facts with severity and context.
- **Traces/crashes:** request paths, stack traces, breadcrumbs and build symbols.

OpenTelemetry standardizes traces, metrics and logs for services. A game client also needs domain events and platform crash tooling; do not force every gameplay event into a backend trace.

## Event contract

Every event needs a stable name and version, UTC timestamp, anonymous/session identifier, build/content/platform identifiers, schema-valid properties and privacy classification. Never send authentication tokens, chat contents, raw save data or unrestricted user text.

Maintain a data dictionary with owner, question answered, trigger, properties, sampling, retention and deletion policy. Version schemas additively when possible. Reject or quarantine malformed events server-side.

## Minimum launch dashboard

- sessions, successful starts and time-to-play;
- crash-free sessions by build/platform/device tier;
- load failures and save corruption/recovery;
- core-loop funnel and win/fail/restart transitions;
- server request error/latency and matchmaking health;
- frame-time distribution, memory pressure and disconnect causes where consent permits.

Averages hide stutter and rare failures. Track distributions and tail percentiles, segmented by build and representative hardware.

## Crash pipeline

Upload symbols privately for each exact build, attach release/build IDs, preserve symbol retention as long as supported builds, group crashes cautiously, strip sensitive fields and verify a deliberate test crash in a non-production channel. Unreal creates crash reports but requires a receiving/symbolication service; Unity Cloud Diagnostics can collect crash and exception reports.

## Live-ops change safety

Remote configuration, events and economy changes need typed schemas, validation, approvals, audit history, staged rollout, kill switches, rollback and expiry. The client must have safe defaults when configuration is missing or invalid. Never let a remote value bypass server authority or grant unrestricted commands.

## Incident loop

`detect → confirm player impact → mitigate/rollback → communicate → repair → verify → postmortem → prevention`

Define severity, owner and response target before launch. A blameless postmortem still assigns concrete actions with owners and deadlines.

## Sources

- OpenTelemetry signals: https://opentelemetry.io/docs/concepts/signals/
- Unreal crash reporting: https://dev.epicgames.com/documentation/en-us/unreal-engine/crash-reporting-in-unreal-engine
- Unity crash and exception reporting: https://docs.unity.com/en-us/cloud-diagnostics/crash-and-exception-reporting/setting-up-crash-and-exception-reporting
- PlayFab events and consumption guidance: https://learn.microsoft.com/en-us/xbox/playfab/pricing/consumption-best-practices
