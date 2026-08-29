# Economy, progression and balancing

Reviewed: 2026-08-29

An economy controls sources, sinks, conversions, storage and access over time. Balance player decisions and pacing, not just spreadsheet equality.

## Economy map

For every resource record source, sink, cap, conversion, cadence, ownership, loss/recovery, tradability, server authority and purpose. Draw the graph and identify positive feedback loops, dead currencies, infinite loops and mandatory bottlenecks.

## Model first

Use a deterministic simulation with player archetypes and seeded strategies. Track time-to-goal distributions, income/spend velocity, inventory accumulation, failure recovery, dominant choices and sensitivity to each parameter. Version the balance configuration separately from code.

For real-money or competitive economies, validate purchases and grants server-side, keep an append-only transaction ledger, use idempotency keys, reconcile balances and plan rollback/support tools. Avoid manipulative dark patterns; disclose odds and costs where law/platform policy requires it.

## Experiments

State hypothesis, primary metric, guardrails, minimum effect, sample-size/power plan, population and stop criteria before exposure. Do not repeatedly peek and select a winner; qualitative playtesting still explains why a metric moved.

Sources:

- PlayFab Economy overview: https://learn.microsoft.com/en-us/gaming/playfab/economy-monetization/economy-what-is
- Unity A/B testing: https://docs.unity.com/en-us/game-overrides/ab-testing
