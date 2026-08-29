# Stable streamed-entity lifecycle

Reviewed: 2026-08-29

```text
WorldRecord { stable_id, schema_version, cell_id, persistent_state }

request_cell(cell_id, generation):
  ticket = new CancellationTicket(cell_id, generation)
  async load dependencies and records
  if ticket cancelled or generation is stale: release results; return
  validate complete cell
  atomically activate presentation instances from WorldRecords

deactivate_cell(cell_id):
  mark instances non-interactive
  cancel pending async work
  for instance in deterministic_order(cell.instances):
    commit allowlisted persistent fields to WorldRecord
    destroy transient presentation instance
  release dependencies

resolve(stable_id):
  if active instance exists: return ActiveHandle(instance)
  if persistent record exists: return DeferredHandle(stable_id)
  return MissingHandle(stable_id)
```

The loaded engine object is never the durable identity. Async completions carry a generation/ticket so an old request cannot reactivate a cell after teleport or unload.
