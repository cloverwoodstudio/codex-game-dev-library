# Versioned telemetry event pattern

Reviewed: 2026-08-29

```text
EventEnvelope {
  event_name: "run_completed"
  schema_version: 2
  occurred_at_utc: timestamp
  anonymous_player_id: opaque_id
  session_id: opaque_id
  build_id: string
  content_version: string
  platform: enum
  consent_class: enum
  properties: {
    run_id: opaque_id
    duration_ms: bounded_integer
    terminal_state: enum(win, fail, abandon)
    difficulty_id: stable_id
  }
}

emit(event):
  assert event matches local schema
  assert no secret, unrestricted text, raw save or direct identity is present
  enqueue_with_bounded_disk_buffer(event)

ingest(event):
  authenticate_title_build()
  enforce payload/rate limits
  validate known schema version and property bounds
  add server receive timestamp
  route invalid events to bounded quarantine
  store according to consent and retention policy
```

Keep domain event schemas in source control. Offline queues need byte/count/age limits and must tolerate duplicates; downstream aggregation should use stable event/run IDs where exact-once meaning matters.
