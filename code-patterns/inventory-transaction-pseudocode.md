# Atomic inventory transaction pseudocode

```text
function move_item(command, state):
    assert valid_id(command.request_id)
    if processed(command.request_id): return previous_result

    source = require_container(state, command.source)
    target = require_container(state, command.target)
    item = require_owned_item(source, command.item_id)
    assert 0 < command.quantity <= item.quantity

    plan = simulate_remove(source, item, command.quantity)
    plan += simulate_insert(target, item.definition_id, command.quantity,
                            stacking_policy)
    assert plan.respects_capacity_and_locks()

    result = apply_atomically(state, plan)
    append_ledger(command.request_id, command.actor, plan, result)
    emit_inventory_changed(result)
    return result
```

Never trust client-supplied ownership, price, quantity or reward outcome. Idempotency prevents retries from duplicating items.
