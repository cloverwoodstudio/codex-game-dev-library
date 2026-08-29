# Inspectable utility AI pseudocode

```text
function choose_action(context, actions):
    scored = []
    for action in actions:
        if not action.preconditions(context):
            continue
        considerations = action.considerations(context)
        score = action.base_weight
        for c in considerations:
            normalized = clamp01(c.input(context))
            contribution = c.response_curve(normalized)
            score *= clamp01(contribution)
        scored.append({ action, score, considerations })

    winner = deterministic_argmax(scored)
    debug_log(context.tick, scored, winner)
    return winner.action
```

Normalize inputs, visualize response curves, log rejected preconditions and use deterministic tie-breaking. Add hysteresis or commitment windows to prevent rapid action oscillation; do not hide it with arbitrary randomness.
