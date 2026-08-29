# Inventory, items and crafting

Reviewed: 2026-08-29

Separate immutable item definitions from mutable item instances. Use stable IDs, not display names or asset paths, in saves/network messages.

## Data model

Definition: ID, localization keys, tags, stack rules, dimensions/weight, base properties, permitted slots, icon/model references and version. Instance: unique ID when needed, definition ID, quantity, durability, rolled modifiers, owner/container and custom state.

All inventory mutations are transactions: validate → plan changes → apply atomically → emit one result. Define capacity, partial moves, stacking order, split/merge, overflow, destruction, trade locks and rollback. Competitive/shared economies require server authority and an auditable ledger.

Crafting recipes declare inputs, catalysts/tools, conditions, duration, outputs/byproducts, cancellation/refund and deterministic random policy. Detect recipe cycles that create value from nothing unless intentionally designed.

Test duplicate requests, full inventory, simultaneous moves, disconnect, save during transaction, definition removal/migration and malicious quantities/IDs.
