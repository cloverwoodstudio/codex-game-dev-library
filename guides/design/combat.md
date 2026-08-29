# Combat design and implementation

Reviewed: 2026-08-29

Combat is a decision system expressed through timing, space, resources and readable feedback.

## Specify each action

- intent and tactical role
- input rules, buffering and cancellation
- startup, active and recovery windows
- movement/root motion and facing policy
- hit shape, target filtering and multi-hit rules
- damage, poise/stagger, knockback and invulnerability
- cost, cooldown and resource effects
- anticipation, impact and recovery feedback
- network authority and rollback implications
- AI use conditions and accessibility assists

Use explicit attack instance IDs so one attack cannot accidentally damage the same target every frame. Keep damage calculation independent from animation notifications; animation may schedule windows, but authoritative rules validate them.

## Testing

Create a combat laboratory with frame/tick stepping, hitbox/hurtbox visualization, state timeline, damage logs and deterministic dummy behaviors. Test simultaneous hits, interruption, death during action, low frame rate, walls/ledges, multiple targets, friendly fire, latency and save/load mid-state when supported.
