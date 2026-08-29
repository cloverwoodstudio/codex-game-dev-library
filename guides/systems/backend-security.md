# Secure game backend and authoritative operations

Reviewed: 2026-08-29

Assume the client is observable, modifiable and replayable. It may request an action; it must not be the authority for valuable state.

## Authority map

For every action, record who validates and commits it. Purchases, inventory grants, progression, competitive results, matchmaking ratings and shared-world state normally require server authority. Client prediction may improve feel but cannot finalize rewards.

## Request boundary

1. Authenticate the session and authorize the specific action.
2. Validate schema, types, ranges, ownership, state preconditions and rate limits.
3. Bind price/reward/configuration to a server-known version; never trust client totals.
4. Use idempotency keys for retried mutations.
5. Commit atomically or compensate explicitly.
6. Return the canonical state/version and log an audit event.

Secrets and privileged API keys belong only in server-side secret storage. Signed data is not automatically trustworthy if the signing key ships in the client.

## Abuse resistance

- enforce per-account, per-device/IP risk and global service limits;
- use nonces/expiry where replay matters;
- validate sequence and state transitions, not only numeric bounds;
- cap payload, decompression, list and query costs;
- isolate user-generated parsers and scan uploads;
- separate detection from automatic punishment and retain appeal evidence;
- design degraded modes for dependency failure rather than granting success.

## Economy transaction shape

`request(idempotency_key, offer_id, expected_offer_version) → authenticate → load canonical offer/player → validate eligibility/funds → atomic debit+grant+receipt → emit audit event → canonical response`

Test duplicate requests, concurrent purchases, timeout after commit, stale offers, negative/overflow values, forged ownership, partial dependency failure and rollback/reconciliation.

## Operational minimum

Use least-privilege service identities, environment separation, dependency pinning, secret rotation, encrypted transport, backup restoration drills, structured audit logs and alerts on unusual grant/error rates. Threat-model before implementation and revisit after every new trust boundary.

## Sources

- OWASP Game Security Framework: https://owasp.org/www-project-gamesec-framework/OGSF
- PlayFab server-side CloudScript API: https://learn.microsoft.com/en-us/rest/api/playfab/cloudscript/server-side-cloud-script
- OpenTelemetry observability primer: https://opentelemetry.io/docs/concepts/observability-primer/
