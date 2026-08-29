# Event-driven quest state pseudocode

```text
quest_definition = {
    id, version,
    states: {
        offered:  { on: { accept: active, decline: declined } },
        active:   { on: { objective_complete: ready, cancel: failed } },
        ready:    { on: { turn_in: completed } },
        completed:{ terminal: true },
        failed:   { terminal: true }
    }
}

function apply_event(instance, event):
    transition = lookup(instance.state, event.type)
    if transition missing or not transition.guard(instance, event):
        return rejected
    old = instance.state
    instance.state = transition.target
    append_journal(instance.id, old, event.id, instance.state)
    emit_idempotent_effects(transition.effects, event.id)
```

Use stable definition and event IDs, idempotent rewards and explicit migration of saved quest instances. Test every state/event pair, duplicate delivery and sequence-breaking events.
